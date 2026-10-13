#!/usr/bin/env python3
"""Extract inspectable UTF-8 text from a registered plain-text source."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import db_util
from source_registry import ENCONET, RAW, sha256_file, utc_now

DERIVED = ENCONET / "derived"
TEXT_SUFFIXES = {".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm"}


def extract(doc_id: str, *, db_path: Path, raw_root: Path = RAW,
            derived_root: Path = DERIVED) -> Path:
    with db_util.connect(db_path) as conn:
        row = db_util.lookup(conn, "documents", "doc_id", doc_id)
        if row is None:
            raise ValueError(f"unknown document: {doc_id}")
        source = raw_root / row["filename"]
        if not source.is_file():
            raise FileNotFoundError(f"registered raw source missing: {source}")
        if sha256_file(source) != row["sha256"]:
            raise ValueError(f"checksum mismatch for {source.name}")
        if source.suffix.lower() not in TEXT_SUFFIXES:
            raise ValueError(f"unsupported extraction type {source.suffix!r}; convert with an approved extractor")
        text = source.read_text(encoding="utf-8-sig")
        if not text.strip():
            raise ValueError(f"empty extraction output for {source.name}")
        derived_root.mkdir(parents=True, exist_ok=True)
        output = derived_root / f"{doc_id}.txt"
        output.write_text(text, encoding="utf-8", newline="\n")
        conn.execute(
            "UPDATE documents SET extraction_method = ?, extracted_at = ? WHERE doc_id = ?",
            (f"utf-8-text:{source.suffix.lower().lstrip('.')}", utc_now(), doc_id),
        )
        conn.commit()
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doc_id")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    args = parser.parse_args()
    try:
        output = extract(args.doc_id, db_path=args.db)
        print(f"extract_text: PASS - {output}")
        return 0
    except Exception as exc:  # CLI boundary
        print(f"extract_text: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
