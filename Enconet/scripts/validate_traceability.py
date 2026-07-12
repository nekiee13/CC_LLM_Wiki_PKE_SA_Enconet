#!/usr/bin/env python3
"""Validate quote-level crumb-to-chunk traceability or approved exceptions."""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

import db_util
from link_crumbs import normalize

ENCONET = Path(__file__).resolve().parents[1]
EXCEPTIONS = ENCONET / "manifests" / "link_exceptions.csv"
RUNS = ENCONET / "manifests" / "validation_runs.csv"


def _exceptions(path: Path) -> tuple[set[tuple[str, str]], list[str]]:
    approved, errors = set(), []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            key = (row.get("crumb_id", ""), row.get("quote_id", ""))
            if not all((row.get(k) or "").strip() for k in ("crumb_id", "quote_id", "reason", "approved_by", "date")):
                errors.append(f"incomplete exception: {key}")
            else: approved.add(key)
    return approved, errors


def validate(db_path: Path, *, exceptions_path: Path = EXCEPTIONS) -> list[str]:
    approved, errors = _exceptions(exceptions_path)
    with db_util.connect(db_path) as conn:
        quotes = conn.execute("SELECT q.*, c.doc_id FROM crumb_quotes q JOIN crumbs c ON c.item_id=q.item_id").fetchall()
        for quote in quotes:
            key = (quote["item_id"], quote["quote_id"])
            links = conn.execute(
                "SELECT l.*, ch.doc_id chunk_doc, ch.chunk_text, ch.source_sha256, d.sha256 document_sha "
                "FROM crumb_chunk_links l LEFT JOIN document_chunks ch ON ch.chunk_id=l.chunk_id "
                "LEFT JOIN documents d ON d.doc_id=ch.doc_id WHERE l.item_id=? AND l.quote_id=?",
                key).fetchall()
            if not links and key not in approved:
                errors.append(f"quote without link or approved exception: {key[1]}")
            for link in links:
                if link["chunk_doc"] is None:
                    errors.append(f"orphan link: {key[1]}"); continue
                if link["chunk_doc"] != quote["doc_id"]:
                    errors.append(f"cross-document link: {key[1]} -> {link['chunk_id']}")
                if link["source_sha256"] != link["document_sha"]:
                    errors.append(f"checksum chain mismatch: {link['chunk_id']}")
                if normalize(quote["quote_original"]) not in normalize(link["chunk_text"]) and key not in approved:
                    errors.append(f"quote absent from linked chunk: {key[1]}")
        for crumb in conn.execute("SELECT item_id FROM crumbs"):
            if not conn.execute("SELECT 1 FROM crumb_quotes WHERE item_id=?", (crumb[0],)).fetchone():
                errors.append(f"crumb without quote: {crumb[0]}")
        for row in conn.execute("PRAGMA foreign_key_check"):
            errors.append(f"foreign key violation: {tuple(row)}")
    return errors


def append_result(result: str, code: int, details: str, manifest: Path = RUNS) -> None:
    with manifest.open("a", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_traceability.py", "unknown", result, code, details])


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--db",type=Path,default=db_util.DEFAULT_DB); parser.add_argument("--exceptions",type=Path,default=EXCEPTIONS); args=parser.parse_args()
    try: errors=validate(args.db, exceptions_path=args.exceptions)
    except Exception as exc: errors=[str(exc)]
    if errors:
        append_result("FAIL",1,f"{len(errors)} error(s); first: {errors[0][:120]}")
        for error in errors: print(f"validate_traceability: FAIL - {error}",file=sys.stderr)
        return 1
    append_result("PASS",0,"all crumb quotes linked or approved exceptions")
    print("validate_traceability: PASS"); return 0


if __name__ == "__main__": raise SystemExit(main())
