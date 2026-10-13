#!/usr/bin/env python3
"""Re-prove document chunk identity, offsets, provenance, and ownership."""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import db_util
from source_registry import ENCONET

DERIVED = ENCONET / "derived"
VALIDATION_MANIFEST = ENCONET / "manifests" / "validation_runs.csv"


def validate(*, db_path: Path, derived_root: Path = DERIVED) -> list[str]:
    errors: list[str] = []
    pattern = db_util.id_patterns()["chunk_id"]
    with db_util.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT c.*, d.sha256 AS document_sha FROM document_chunks c "
            "LEFT JOIN documents d ON d.doc_id = c.doc_id ORDER BY c.chunk_id"
        ).fetchall()
        texts: dict[str, str] = {}
        for row in rows:
            chunk_id = row["chunk_id"]
            if pattern.fullmatch(chunk_id) is None:
                errors.append(f"invalid chunk ID: {chunk_id}")
            if row["document_sha"] is None:
                errors.append(f"orphan chunk: {chunk_id}")
                continue
            if row["source_sha256"] != row["document_sha"]:
                errors.append(f"source checksum mismatch: {chunk_id}")
            if not row["chunk_text"].strip():
                errors.append(f"empty chunk: {chunk_id}")
            doc_id = row["doc_id"]
            if doc_id not in texts:
                path = derived_root / f"{doc_id}.txt"
                if not path.is_file():
                    errors.append(f"derived text missing: {doc_id}")
                    texts[doc_id] = ""
                else:
                    texts[doc_id] = path.read_text(encoding="utf-8")
            text = texts[doc_id]
            start, end = row["char_start"], row["char_end"]
            if start < 0 or end <= start or end > len(text) or text[start:end] != row["chunk_text"]:
                errors.append(f"offset slice mismatch: {chunk_id}")
    return errors


def append_result(result: str, exit_code: int, details: str,
                  manifest: Path = VALIDATION_MANIFEST) -> None:
    phase = "unknown"
    try:
        phase = yaml.safe_load((ENCONET / "project-state.yml").read_text(encoding="utf-8"))["phase"]
    except Exception:
        pass
    with manifest.open("a", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_chunks.py", phase, result, exit_code, details,
        ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(db_path=args.db)
    except Exception as exc:
        errors = [str(exc)]
    if errors:
        if not args.no_record:
            append_result("FAIL", 1, f"{len(errors)} error(s); first: {errors[0][:120]}")
        for error in errors:
            print(f"validate_chunks: FAIL - {error}", file=sys.stderr)
        return 1
    if not args.no_record:
        append_result("PASS", 0, "all chunks verified")
    print("validate_chunks: PASS - all chunks verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
