#!/usr/bin/env python3
"""Preview or first-write UTF-8 text from one registered local raw file."""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path
from source_registry import RAW, is_write_locked, read_manifest, sha256_file, utc_now

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = frozenset({".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm"})


def _plan(db: Path, doc_id: str) -> tuple[dict, Path, str]:
    if db_util.id_patterns()["doc_id"].fullmatch(doc_id) is None:
        raise ValueError(f"invalid document ID: {doc_id}")
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        document = db_util.lookup(conn, "documents", "doc_id", doc_id)
        if document is None:
            raise ValueError(f"unknown document: {doc_id}")
        if document["extracted_at"] is not None or document["extraction_method"] is not None:
            raise ValueError("document was already extracted; prior evidence is immutable")
        if conn.execute("SELECT 1 FROM document_chunks WHERE doc_id=?", (doc_id,)).fetchone():
            raise ValueError("document already has chunks; extraction cannot replace evidence")
    filename = document["filename"]
    if not filename or Path(filename).name != filename or filename in {".", ".."}:
        raise ValueError("registered filename must be one direct raw file")
    source = local_path(RAW / filename)
    if source.parent != local_path(RAW) or not source.is_file():
        raise ValueError("registered raw source is missing or outside the local raw folder")
    if source.suffix.lower() not in TEXT_SUFFIXES:
        raise ValueError(f"unsupported extraction type {source.suffix!r}; use an approved extractor")
    if not is_write_locked(source):
        raise ValueError("registered raw source is not write-locked")
    rows = read_manifest()
    matches = [row for row in rows if row["doc_id"] == doc_id]
    if len(matches) != 1 or matches[0]["filename"] != filename or matches[0]["sha256"] != document["sha256"] or matches[0]["side_hint"] != document["document_side"]:
        raise ValueError("raw manifest and registered document do not match")
    if sha256_file(source) != document["sha256"]:
        raise ValueError("registered raw source checksum mismatch")
    text = source.read_text(encoding="utf-8-sig")
    if not text.strip():
        raise ValueError("empty extraction output")
    output = local_path(ROOT / "derived" / f"{doc_id}.txt")
    if output.exists():
        raise ValueError("derived output already exists; prior evidence is immutable")
    plan = {"mode": "preview", "doc_id": doc_id, "source": str(source),
            "source_sha256": document["sha256"], "output": str(output),
            "derived_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "extraction_method": f"utf-8-text:{source.suffix.lower().lstrip('.')}",
            "status": "derived-text-not-human-approved"}
    return plan, source, text


def extract(doc_id: str, *, db_path: Path, apply: bool = False) -> dict:
    plan, source, text = _plan(db_path, doc_id)
    if not apply:
        return plan
    database = local_path(db_path)
    output = local_path(plan["output"])
    output.parent.mkdir(parents=True, exist_ok=True)
    created = False
    with closing(db_util.connect(database)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            document = db_util.lookup(conn, "documents", "doc_id", doc_id)
            if (document is None or document["sha256"] != plan["source_sha256"]
                    or document["extracted_at"] is not None or document["extraction_method"] is not None):
                raise ValueError("registered document changed since preview")
            if sha256_file(source) != plan["source_sha256"] or not is_write_locked(source):
                raise ValueError("registered raw source changed since preview")
            if hashlib.sha256(source.read_text(encoding="utf-8-sig").encode("utf-8")).hexdigest() != plan["derived_sha256"]:
                raise ValueError("raw text changed since preview")
            with output.open("x", encoding="utf-8", newline="\n") as handle:
                created = True
                handle.write(text)
            conn.execute("UPDATE documents SET extraction_method=?, extracted_at=? WHERE doc_id=?",
                         (plan["extraction_method"], utc_now(), doc_id))
            conn.commit()
        except Exception:
            conn.rollback()
            if created:
                output.unlink()
            raise
    plan["mode"] = "apply"
    return plan


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doc_id")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(extract(args.doc_id, db_path=args.db, apply=args.apply),
                         ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, UnicodeError) as exc:
        print(f"extract_text: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
