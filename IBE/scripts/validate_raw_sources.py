#!/usr/bin/env python3
"""Check local raw files against their manifest and database rows."""
from __future__ import annotations

import argparse
from contextlib import closing
import sqlite3
import sys
from pathlib import Path

import db_util
from project_paths import local_path
from source_registry import MANIFEST, RAW, is_write_locked, read_manifest, sha256_file


def validate(*, db_path: Path, raw_root: Path = RAW,
             manifest_path: Path = MANIFEST) -> list[str]:
    database = local_path(db_path)
    raw = local_path(raw_root)
    manifest_file = local_path(manifest_path)
    if not database.is_file():
        return [f"local database is missing: {database}"]
    rows = read_manifest(manifest_file)
    if not rows:
        return ["raw source manifest has no registered documents"]
    errors: list[str] = []
    by_name = {row["filename"]: row for row in rows}
    if len(by_name) != len(rows):
        errors.append("duplicate filename in raw_sources.csv")
    if len({row["doc_id"] for row in rows}) != len(rows):
        errors.append("duplicate document ID in raw_sources.csv")
    actual = {path.name: path for path in raw.iterdir()
              if path.is_file() and path.name != ".gitkeep"}
    for name in sorted(actual.keys() - by_name.keys()):
        errors.append(f"unregistered raw file: {name}")
    for name in sorted(by_name.keys() - actual.keys()):
        errors.append(f"registered raw file missing: {name}")
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        db_rows = {row["filename"]: row for row in conn.execute("SELECT * FROM documents")}
        for name in sorted(db_rows.keys() - by_name.keys()):
            errors.append(f"DB document missing from manifest: {name}")
        for name, row in by_name.items():
            path = actual.get(name)
            if path:
                if sha256_file(path) != row["sha256"]:
                    errors.append(f"checksum mismatch: {name}")
                if not is_write_locked(path):
                    errors.append(f"raw file is writable: {name}")
            db_row = db_rows.get(name)
            if db_row is None:
                errors.append(f"manifest document missing from DB: {name}")
                continue
            comparisons = {
                "doc_id": db_row["doc_id"], "title": db_row["title"],
                "supplier": db_row["supplier"], "doc_date": db_row["doc_date"] or "n-a",
                "language": db_row["language"], "side_hint": db_row["document_side"],
                "sha256": db_row["sha256"], "promoted_utc": db_row["promoted_utc"],
                "source_url": db_row["source_url"], "notes": db_row["notes"],
            }
            for field, value in comparisons.items():
                if row[field] != value:
                    errors.append(f"registry mismatch {name}.{field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    args = parser.parse_args()
    try:
        errors = validate(db_path=args.db)
    except (OSError, ValueError, RuntimeError, KeyError, sqlite3.Error) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"validate_raw_sources: FAIL - {error}", file=sys.stderr)
    if errors:
        return 1
    print("validate_raw_sources: PASS")
    return 0


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
