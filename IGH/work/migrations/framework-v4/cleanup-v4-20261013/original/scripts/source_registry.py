"""Project-local source registry helpers; importing this does not ingest data."""
from __future__ import annotations

import csv
import hashlib
import stat
from datetime import datetime, timezone
from pathlib import Path

import db_util
from project_paths import local_path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
MANIFEST = ROOT / "manifests" / "raw_sources.csv"
HEADER = [
    "doc_id", "filename", "title", "supplier", "doc_date", "language",
    "side_hint", "sha256", "promoted_utc", "source_url", "notes",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with local_path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_lock(path: Path) -> None:
    source = local_path(path)
    source.chmod(source.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def is_write_locked(path: Path) -> bool:
    return not bool(local_path(path).stat().st_mode &
                    (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def read_manifest(path: Path = MANIFEST) -> list[dict[str, str]]:
    with local_path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != HEADER:
            raise RuntimeError(f"unexpected raw source manifest header: {reader.fieldnames}")
        rows = list(reader)
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise RuntimeError("malformed raw source manifest row")
        return rows


def next_doc_id(conn) -> str:
    numbers = []
    for row in conn.execute("SELECT doc_id FROM documents"):
        numbers.append(int(row[0].split("-")[1]))
    if numbers and max(numbers) >= 9999:
        raise RuntimeError("DOC ID space exhausted")
    return f"DOC-{max(numbers, default=0) + 1:04d}"


def register(raw_file: Path, *, db_path: Path, title: str, supplier: str,
             doc_date: str, language: str, side_hint: str,
             promoted_utc: str | None = None, source_url: str = "n-a",
             notes: str = "", manifest_path: Path = MANIFEST) -> str:
    """Register only a direct local raw file; promotion remains a later task."""
    source = local_path(raw_file)
    manifest = local_path(manifest_path)
    if source.parent != local_path(RAW) or manifest != local_path(MANIFEST):
        raise ValueError("source and manifest must be the project's raw registry")
    if not source.is_file():
        raise FileNotFoundError(source)
    database = local_path(db_path)
    if not database.is_file():
        raise FileNotFoundError(f"local database is missing: {database}")
    checksum = sha256_file(source)
    rows = read_manifest(manifest)
    if any(row["sha256"] == checksum for row in rows):
        raise ValueError(f"checksum already registered: {checksum}")
    with db_util.connect(database) as conn:
        if conn.execute("SELECT 1 FROM documents WHERE sha256 = ?", (checksum,)).fetchone():
            raise ValueError(f"checksum already registered: {checksum}")
        doc_id = next_doc_id(conn)
        timestamp = promoted_utc or utc_now()
        values = {
            "doc_id": doc_id, "filename": source.name, "title": title,
            "supplier": supplier, "doc_date": None if doc_date == "n-a" else doc_date,
            "language": language, "document_side": side_hint, "sha256": checksum,
            "promoted_utc": timestamp, "source_url": source_url, "notes": notes,
        }
        db_util.insert(conn, "documents", values)
        manifest_row = {**{key: str(values.get(key, "")) for key in HEADER},
                        "doc_date": doc_date, "side_hint": side_hint}
        manifest_row.pop("document_side", None)
        with manifest.open("a", newline="", encoding="utf-8") as handle:
            csv.DictWriter(handle, fieldnames=HEADER).writerow(manifest_row)
        conn.commit()
    return doc_id
