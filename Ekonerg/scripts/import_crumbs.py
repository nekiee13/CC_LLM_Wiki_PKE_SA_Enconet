#!/usr/bin/env python3
"""Strictly validate and transactionally import local crumb JSON into one run."""
from __future__ import annotations

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path
import sieving_lib  # noqa: F401 - makes the copied json_extractor package importable
from json_extractor.crumb_validation import validate_file

ROOT = Path(__file__).resolve().parents[1]
CONTEXT_ANCHORS = ("project_ref", "contract_ref", "supplier_ref", "source_revision", "evidence_date")


def _validate_context_requirements(items: list[dict]) -> None:
    """Require at least one source anchor when an evidence type is declared."""
    for index, item in enumerate(items):
        if "evidence_type" not in item:
            continue
        context = item.get("context")
        if not isinstance(context, dict) or not any(
            isinstance(context.get(field), str) and context[field].strip()
            for field in CONTEXT_ANCHORS
        ):
            raise ValueError(
                f"items[{index}].evidence_type requires at least one source context anchor"
            )


def import_file(db: Path, json_path: Path, *, run_id: str) -> int:
    if db_util.id_patterns()["run_id"].fullmatch(run_id) is None:
        raise ValueError(f"invalid sieve run ID: {run_id}")
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    source = local_path(json_path)
    if not source.is_relative_to(ROOT / "sieving"):
        raise ValueError("crumb JSON must be inside the local sieving folder")
    payload, result = validate_file(source, strict=True)
    if not result.passed:
        raise ValueError("strict crumb validation failed: " + "; ".join(result.errors))
    document, items = payload["document"], payload["items"]
    _validate_context_requirements(items)
    with closing(db_util.connect(database)) as conn, conn:
        db_util.ensure_crumb_context_schema(conn)
        run = db_util.lookup(conn, "sieve_runs", "run_id", run_id)
        if run is None:
            raise ValueError(f"unknown sieve run: {run_id}")
        if run["document_side"] != document["document_side"]:
            raise ValueError("JSON side does not match sieve run side")
        if document.get("doc_id") != run["doc_id"]:
            raise ValueError("JSON doc_id does not match sieve run document")
        if run["completed_at"] is not None or conn.execute(
            "SELECT 1 FROM crumbs WHERE sieve_run_id=?", (run_id,)
        ).fetchone():
            raise ValueError("sieve run is already completed; generations are immutable")
        criterion_ordinals: dict[str, int] = {}
        for row in conn.execute(
            "SELECT criterion_id,item_id FROM crumbs WHERE doc_id=?", (run["doc_id"],)
        ):
            criterion_ordinals[row["criterion_id"]] = max(
                criterion_ordinals.get(row["criterion_id"], 0),
                int(row["item_id"].rsplit("-", 1)[1]),
            )
        quote_group = max((int(row[0].rsplit("-", 2)[1]) for row in conn.execute(
            "SELECT q.quote_id FROM crumb_quotes q JOIN crumbs c ON c.item_id=q.item_id "
            "WHERE c.doc_id=?", (run["doc_id"],)
        )), default=0)
        for item in items:
            criterion = item["criterion_id"]
            criterion_ordinals[criterion] = criterion_ordinals.get(criterion, 0) + 1
            quote_group += 1
            crumb_id = f"CRUMB-{run['doc_id']}-{criterion}-{criterion_ordinals[criterion]:04d}"
            quotes = item["evidence_quotes"]
            db_util.insert(conn, "crumbs", {
                "item_id": crumb_id, "doc_id": run["doc_id"], "sieve_run_id": run_id,
                "criterion_id": criterion, "document_side": document["document_side"],
                "statement": item["statement"], "item_type": item.get("item_type"),
                "quote_language": quotes[0]["quote_language"],
            })
            sources = item.get("sources", item.get("source"))
            if isinstance(sources, dict):
                sources = [sources]
            for source_row in sources:
                db_util.insert(conn, "crumb_sources", {
                    "item_id": crumb_id, "source_locator": source_row["source_locator"],
                    "source_page": source_row.get("source_page"),
                    "source_heading_path": source_row.get("source_heading_path"),
                })
            default_locator = sources[0]["source_locator"]
            for qordinal, quote in enumerate(quotes, 1):
                db_util.insert(conn, "crumb_quotes", {
                    "quote_id": f"QUOTE-{run['doc_id']}-{quote_group:04d}-{qordinal:02d}",
                    "item_id": crumb_id, "quote_original": quote["quote_original"],
                    "quote_language": quote["quote_language"],
                    "source_locator": quote.get("source_locator", default_locator),
                })
            refs = item.get("authority_references", document["authority_references"])
            for ref in refs:
                db_util.insert(conn, "crumb_authority_refs", {
                    "item_id": crumb_id, "authority_role": ref["authority_role"],
                    "source_code": ref["source_code"], "source_locator": ref["source_locator"],
                    "applicability": ref.get("applicability", "APPLICABLE"),
                    "applicability_basis": ref.get("applicability_basis"),
                })
            context = item.get("context") or {}
            context_values = {
                "item_id": crumb_id,
                "evidence_type": item.get("evidence_type"),
                **{field: context.get(field) for field in (
                    "project_ref", "contract_ref", "supplier_ref", "source_revision", "evidence_date"
                )},
            }
            if any(value is not None for key, value in context_values.items() if key != "item_id"):
                db_util.insert(conn, "crumb_context", context_values)
        conn.execute("UPDATE sieve_runs SET completed_at=CURRENT_TIMESTAMP WHERE run_id=?", (run_id,))
    return len(items)


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        count = import_file(args.db, args.json_file, run_id=args.run_id)
        print(f"import_crumbs: PASS - {count} crumb(s); quote linking and metrics remain pending")
        return 0
    except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"import_crumbs: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
