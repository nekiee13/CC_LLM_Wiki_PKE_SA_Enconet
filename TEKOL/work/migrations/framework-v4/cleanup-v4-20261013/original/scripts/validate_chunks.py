#!/usr/bin/env python3
"""Recheck local chunk IDs, source hashes, text slices, and owners."""
from __future__ import annotations

import argparse
import csv
from contextlib import closing
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import db_util
from project_paths import local_path

ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "derived"
VALIDATION_MANIFEST = ROOT / "manifests" / "validation_runs.csv"
RUN_HEADER = ["run_utc", "validator", "phase", "result", "exit_code", "details"]


def validate(*, db_path: Path, derived_root: Path = DERIVED) -> list[str]:
    database = local_path(db_path)
    derived = local_path(derived_root)
    if not database.is_file():
        return [f"local database is missing: {database}"]
    pattern = db_util.id_patterns()["chunk_id"]
    doc_pattern = db_util.id_patterns()["doc_id"]
    errors: list[str] = []
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT c.*, d.sha256 AS document_sha FROM document_chunks c "
            "LEFT JOIN documents d ON d.doc_id = c.doc_id ORDER BY c.chunk_id"
        ).fetchall()
        if not rows:
            return ["database has no document chunks"]
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
            if doc_pattern.fullmatch(doc_id) is None:
                errors.append(f"invalid document ID in chunk: {chunk_id}")
                continue
            if doc_id not in texts:
                path = local_path(derived / f"{doc_id}.txt")
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
    state_file = local_path(ROOT / "project-state.yml")
    if state_file.is_file():
        state = yaml.safe_load(state_file.read_text(encoding="utf-8"))
        if isinstance(state, dict):
            phase = str(state.get("phase", "unknown"))
    with local_path(manifest).open("r+", newline="", encoding="utf-8") as handle:
        if next(csv.reader(handle), None) != RUN_HEADER:
            raise ValueError("validation manifest header is missing or invalid")
        handle.seek(0, 2)
        csv.writer(handle).writerow([
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
    except (OSError, ValueError, KeyError, sqlite3.Error, yaml.YAMLError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"validate_chunks: FAIL - {error}", file=sys.stderr)
    code = int(bool(errors))
    if not args.no_record:
        try:
            append_result("FAIL" if code else "PASS", code,
                          f"{len(errors)} error(s); first: {errors[0][:120]}" if errors
                          else "all chunks verified")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            print(f"validate_chunks: FAIL - record could not be written: {exc}", file=sys.stderr)
            return 1
    if not code:
        print("validate_chunks: PASS - all chunks verified")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
