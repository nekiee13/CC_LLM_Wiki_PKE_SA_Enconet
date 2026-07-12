#!/usr/bin/env python3
"""Validate raw files against the document registry and immutable manifest."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import db_util
from source_registry import MANIFEST, RAW, is_write_locked, read_manifest, sha256_file


def validate(*, db_path: Path, raw_root: Path = RAW,
             manifest_path: Path = MANIFEST) -> list[str]:
    errors: list[str] = []
    rows = read_manifest(manifest_path)
    by_name = {row["filename"]: row for row in rows}
    if len(by_name) != len(rows):
        errors.append("duplicate filename in raw_sources.csv")
    actual = {path.name: path for path in raw_root.iterdir() if path.is_file()}
    for name in sorted(actual.keys() - by_name.keys()):
        errors.append(f"unregistered raw file: {name}")
    for name in sorted(by_name.keys() - actual.keys()):
        errors.append(f"registered raw file missing: {name}")
    with db_util.connect(db_path) as conn:
        db_rows = {row["filename"]: row for row in conn.execute("SELECT * FROM documents")}
        for name in sorted(db_rows.keys() - by_name.keys()):
            errors.append(f"DB document missing from manifest: {name}")
        for name, manifest in by_name.items():
            path = actual.get(name)
            if path:
                checksum = sha256_file(path)
                if checksum != manifest["sha256"]:
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
                if manifest[field] != value:
                    errors.append(f"registry mismatch {name}.{field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    args = parser.parse_args()
    try:
        errors = validate(db_path=args.db)
    except Exception as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"validate_raw_sources: FAIL - {error}", file=sys.stderr)
        return 1
    print("validate_raw_sources: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
