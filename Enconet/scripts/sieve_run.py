#!/usr/bin/env python3
"""Create a guarded EPIC5 sieve run with ADR-0020 authority references."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import db_util


def create_run(db: Path, *, run_id: str, doc_id: str, prompt_version: str,
               document_side: str, authorities: list[dict]) -> None:
    if document_side not in {"RULE", "DOCUMENT"}:
        raise ValueError(f"invalid document_side: {document_side!r}")
    if document_side == "RULE" and not authorities:
        raise ValueError("RULE run requires authority references")
    if document_side == "DOCUMENT" and authorities:
        raise ValueError("DOCUMENT run forbids authority references")
    from validate_app_b_json import ValidationResult, _check_refs
    checked = ValidationResult()
    _check_refs(authorities, "run", checked)
    if checked.errors:
        raise ValueError("; ".join(checked.errors))
    with db_util.connect(db) as conn:
        document = db_util.lookup(conn, "documents", "doc_id", doc_id)
        if document is None:
            raise ValueError(f"unknown document: {doc_id}")
        if document["document_side"] != document_side:
            raise ValueError("run side does not match registered document side")
        legacy = next((r["source_code"] for r in authorities if r["authority_role"] == "GOVERNING"), None)
        db_util.insert(conn, "sieve_runs", {"run_id": run_id, "doc_id": doc_id,
                       "prompt_version": prompt_version, "document_side": document_side,
                       "source_rule": legacy})
        for ref in authorities:
            db_util.insert(conn, "sieve_run_authorities", {"run_id": run_id,
                "authority_role": ref["authority_role"], "source_code": ref["source_code"],
                "source_locator": ref["source_locator"],
                "applicability": ref.get("applicability", "APPLICABLE"),
                "applicability_basis": ref.get("applicability_basis")})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--prompt-version", required=True)
    parser.add_argument("--document-side", required=True)
    parser.add_argument("--authority-json", action="append", default=[], help="one JSON authority object; repeatable")
    args = parser.parse_args()
    try:
        refs = [json.loads(value) for value in args.authority_json]
        create_run(args.db, run_id=args.run_id, doc_id=args.doc_id,
                   prompt_version=args.prompt_version, document_side=args.document_side,
                   authorities=refs)
        print(f"sieve_run: PASS - {args.run_id}")
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"sieve_run: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
