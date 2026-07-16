#!/usr/bin/env python3
"""Create a guarded EPIC5 sieve run with ADR-0020 authority references."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import db_util
import sieving_lib  # noqa: F401
from json_extractor.crumb_validation import ValidationResult, check_authority_references


def create_run(db: Path, *, run_id: str, doc_id: str, prompt_version: str,
               document_side: str, authorities: list[dict], rejected_item_count: int = 0,
               failed_item_count: int = 0) -> dict[str, object]:
    if document_side not in {"RULE", "DOCUMENT"}:
        raise ValueError(f"invalid document_side: {document_side!r}")
    if document_side == "RULE" and not authorities:
        raise ValueError("RULE run requires authority references")
    if document_side == "DOCUMENT" and authorities:
        raise ValueError("DOCUMENT run forbids authority references")
    if rejected_item_count < 0 or failed_item_count < 0:
        raise ValueError("rejected/failed item counts cannot be negative")
    checked = ValidationResult()
    check_authority_references(authorities, "run", checked)
    if checked.errors:
        raise ValueError("; ".join(checked.errors))
    with db_util.connect(db) as conn:
        document = db_util.lookup(conn, "documents", "doc_id", doc_id)
        if document is None:
            raise ValueError(f"unknown document: {doc_id}")
        if document["document_side"] != document_side:
            raise ValueError("run side does not match registered document side")
        columns = {row[1] for row in conn.execute("PRAGMA table_info(sieve_runs)")}
        if "generation" not in columns:
            raise ValueError("EPIC18 generation schema is missing; run reviewed migrate_db.py workflow")
        prior = conn.execute(
            "SELECT * FROM sieve_runs WHERE doc_id=? ORDER BY generation", (doc_id,)
        ).fetchall()
        active = [row for row in prior if row["is_active"]]
        if prior and len(active) != 1:
            raise ValueError(f"document {doc_id} must have exactly one active generation")
        generation = max((int(row["generation"]) for row in prior), default=0) + 1
        previous = active[0] if active else None
        warning = None
        if previous and previous["prompt_version"] == prompt_version:
            warning = f"unchanged prompt version {prompt_version}; no-op tuning candidate"
        legacy = next((r["source_code"] for r in authorities if r["authority_role"] == "GOVERNING"), None)
        db_util.insert(conn, "sieve_runs", {"run_id": run_id, "doc_id": doc_id,
                       "prompt_version": prompt_version, "document_side": document_side,
                       "source_rule": legacy, "generation": generation,
                       "status": "candidate" if previous else "active",
                       "is_active": 0 if previous else 1,
                       "supersedes_run_id": previous["run_id"] if previous else None,
                       "rejected_item_count": rejected_item_count,
                       "failed_item_count": failed_item_count})
        for ref in authorities:
            db_util.insert(conn, "sieve_run_authorities", {"run_id": run_id,
                "authority_role": ref["authority_role"], "source_code": ref["source_code"],
                "source_locator": ref["source_locator"],
                "applicability": ref.get("applicability", "APPLICABLE"),
                "applicability_basis": ref.get("applicability_basis")})
        return {"generation": generation, "status": "candidate" if previous else "active",
                "supersedes_run_id": previous["run_id"] if previous else None,
                "warning": warning}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--prompt-version", required=True)
    parser.add_argument("--document-side", required=True)
    parser.add_argument("--authority-json", action="append", default=[], help="one JSON authority object; repeatable")
    parser.add_argument("--rejected-item-count", type=int, default=0)
    parser.add_argument("--failed-item-count", type=int, default=0)
    args = parser.parse_args()
    try:
        refs = [json.loads(value) for value in args.authority_json]
        result = create_run(args.db, run_id=args.run_id, doc_id=args.doc_id,
                   prompt_version=args.prompt_version, document_side=args.document_side,
                   authorities=refs, rejected_item_count=args.rejected_item_count,
                   failed_item_count=args.failed_item_count)
        print(f"sieve_run: PASS - {args.run_id}; generation={result['generation']}; status={result['status']}")
        if result["warning"]:
            print(f"WARNING: {result['warning']}")
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"sieve_run: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
