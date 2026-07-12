#!/usr/bin/env python3
"""Register one promoted raw document in SQLite and raw_sources.csv."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import db_util
from source_registry import RAW, register


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--title", required=True)
    parser.add_argument("--supplier", required=True)
    parser.add_argument("--doc-date", default="n-a")
    parser.add_argument("--language", required=True, choices=["sl", "en", "hr"])
    parser.add_argument("--side", required=True, choices=["RULE", "DOCUMENT"])
    parser.add_argument("--source-url", default="n-a")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    try:
        doc_id = register(RAW / args.filename, db_path=args.db, title=args.title,
                          supplier=args.supplier, doc_date=args.doc_date,
                          language=args.language, side_hint=args.side,
                          source_url=args.source_url, notes=args.notes)
        print(f"register_document: PASS - {doc_id}")
        return 0
    except Exception as exc:  # CLI boundary
        print(f"register_document: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
