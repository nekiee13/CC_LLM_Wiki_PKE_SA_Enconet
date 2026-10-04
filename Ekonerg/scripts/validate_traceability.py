#!/usr/bin/env python3
"""Validate local crumb quotes against local chunks or recorded exceptions."""
from __future__ import annotations

import argparse
import csv
from contextlib import closing
from datetime import date, datetime, timezone
from pathlib import Path
import sqlite3
import sys

from project_paths import local_path
import db_util
from evidence_matching import quote_matches

ROOT = Path(__file__).resolve().parents[1]
EXCEPTIONS = ROOT / "manifests" / "link_exceptions.csv"
RUNS = ROOT / "manifests" / "validation_runs.csv"
EXCEPTION_HEADER = ["crumb_id", "quote_id", "reason", "approved_by", "date"]
RUN_HEADER = ["run_utc", "validator", "phase", "result", "exit_code", "details"]


def _exceptions(path: Path) -> tuple[set[tuple[str, str]], list[str]]:
    approved: set[tuple[str, str]] = set()
    errors: list[str] = []
    with local_path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXCEPTION_HEADER:
            raise ValueError("link exception ledger header is missing or invalid")
        for row in reader:
            key = (row.get("crumb_id", ""), row.get("quote_id", ""))
            if None in row or not all((row.get(field) or "").strip() for field in EXCEPTION_HEADER):
                errors.append(f"incomplete exception: {key}")
                continue
            try:
                date.fromisoformat(row["date"])
            except ValueError:
                errors.append(f"invalid exception date: {key}")
                continue
            if key in approved:
                errors.append(f"duplicate exception: {key}")
            approved.add(key)
    return approved, errors


def validate(db_path: Path, *, exceptions_path: Path = EXCEPTIONS,
             active_only: bool = False) -> list[str]:
    database = local_path(db_path)
    approved, errors = _exceptions(local_path(exceptions_path))
    if not database.is_file():
        return errors + [f"local database is missing: {database}"]
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        scope = " JOIN sieve_runs r ON r.run_id=c.sieve_run_id" if active_only else ""
        active_clause = " WHERE r.is_active=1" if active_only else ""
        quotes = conn.execute(
            "SELECT q.*, c.doc_id FROM crumb_quotes q JOIN crumbs c ON c.item_id=q.item_id"
            + scope + active_clause
        ).fetchall()
        if not quotes:
            errors.append("database has no crumb quotes")
        quote_keys = {(row["item_id"], row["quote_id"]) for row in quotes}
        for key in sorted(approved - quote_keys):
            errors.append(f"exception has no local quote: {key[1]}")
        for quote in quotes:
            key = (quote["item_id"], quote["quote_id"])
            links = conn.execute(
                "SELECT l.*, ch.doc_id AS chunk_doc, ch.chunk_text, ch.source_sha256, "
                "d.sha256 AS document_sha FROM crumb_chunk_links l "
                "LEFT JOIN document_chunks ch ON ch.chunk_id=l.chunk_id "
                "LEFT JOIN documents d ON d.doc_id=ch.doc_id "
                "WHERE l.item_id=? AND l.quote_id=?", key,
            ).fetchall()
            if not links and key not in approved:
                errors.append(f"quote without link or approved exception: {key[1]}")
            for link in links:
                if link["chunk_doc"] is None:
                    errors.append(f"orphan link: {key[1]}")
                    continue
                if link["chunk_doc"] != quote["doc_id"]:
                    errors.append(f"cross-document link: {key[1]} -> {link['chunk_id']}")
                if link["source_sha256"] != link["document_sha"]:
                    errors.append(f"checksum chain mismatch: {link['chunk_id']}")
                if not quote_matches(quote["quote_original"], link["chunk_text"]) and key not in approved:
                    errors.append(f"quote absent from linked chunk: {key[1]}")
        crumbs_query = "SELECT c.item_id FROM crumbs c"
        if active_only:
            crumbs_query += " JOIN sieve_runs r ON r.run_id=c.sieve_run_id WHERE r.is_active=1"
        for crumb in conn.execute(crumbs_query):
            if not conn.execute("SELECT 1 FROM crumb_quotes WHERE item_id=?", (crumb[0],)).fetchone():
                errors.append(f"crumb without quote: {crumb[0]}")
        for row in conn.execute("PRAGMA foreign_key_check"):
            errors.append(f"foreign key violation: {tuple(row)}")
    return errors


def append_result(result: str, code: int, details: str, path: Path = RUNS) -> None:
    with local_path(path).open("r+", newline="", encoding="utf-8") as handle:
        if next(csv.reader(handle), None) != RUN_HEADER:
            raise ValueError("validation manifest header is missing or invalid")
        handle.seek(0, 2)
        csv.writer(handle).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_traceability.py", "unknown", result, code, details,
        ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--exceptions", type=Path, default=EXCEPTIONS)
    parser.add_argument("--active-only", action="store_true",
                        help="validate only quotes in active sieve generations")
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(args.db, exceptions_path=args.exceptions,
                          active_only=args.active_only)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"validate_traceability: FAIL - {error}", file=sys.stderr)
    code = int(bool(errors))
    if not args.no_record:
        try:
            append_result("FAIL" if code else "PASS", code,
                          f"{len(errors)} error(s); first: {errors[0][:120]}" if errors
                          else "all crumb quotes linked or recorded exceptions")
        except (OSError, ValueError) as exc:
            print(f"validate_traceability: FAIL - record could not be written: {exc}",
                  file=sys.stderr)
            return 1
    if not code:
        print("validate_traceability: PASS")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
