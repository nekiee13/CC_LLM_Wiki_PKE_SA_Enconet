#!/usr/bin/env python3
"""Promote a reviewed incoming file to immutable raw storage and register it."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import db_util
from project_paths import ROOT as ENCONET
from source_registry import RAW, register, write_lock


def promote(source: Path, *, preserve_incoming: bool = False, preview: bool = False, **metadata) -> str:
    if preserve_incoming:
        from copy_incoming_source import promote as copy_source
        return copy_source(source.name, apply=not preview, **metadata)
    if preview:
        raise ValueError('--preview requires --preserve-incoming')
    source = source.resolve()
    incoming = (ENCONET / "incoming").resolve()
    if source.parent != incoming or not source.is_file():
        raise ValueError(f"source must be a file directly under incoming/: {source}")
    destination = RAW / source.name
    if destination.exists():
        raise FileExistsError(f"duplicate raw filename: {source.name}")
    RAW.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), destination)
    try:
        write_lock(destination)
        return register(destination, **metadata)
    except Exception:
        destination.chmod(destination.stat().st_mode | 0o200)
        shutil.move(str(destination), source)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename")
    parser.add_argument('--preserve-incoming', action='store_true', help='Copy instead of move; keep owner originals intact')
    parser.add_argument('--preview', action='store_true', help='Read-only copy preview; requires --preserve-incoming')
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
        doc_id = promote(ENCONET / "incoming" / args.filename,
                         preserve_incoming=args.preserve_incoming, preview=args.preview, db_path=args.db,
                         title=args.title, supplier=args.supplier,
                         doc_date=args.doc_date, language=args.language,
                         side_hint=args.side, source_url=args.source_url, notes=args.notes)
        print(f"promote_source: PASS - {doc_id}")
        return 0
    except Exception as exc:  # CLI boundary
        print(f"promote_source: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
