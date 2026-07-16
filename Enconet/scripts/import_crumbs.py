#!/usr/bin/env python3
"""Transactionally import validated EPIC5 crumb JSON into SQLite."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import db_util
import sieving_lib  # noqa: F401
from json_extractor.crumb_validation import validate_file


def import_file(db: Path, json_path: Path, *, run_id: str, strict: bool = False) -> int:
    payload, result = validate_file(json_path, strict=strict)
    if not result.passed:
        raise ValueError("validation failed: " + "; ".join(result.errors))
    document, items = payload["document"], payload["items"]
    with db_util.connect(db) as conn:
        run = db_util.lookup(conn, "sieve_runs", "run_id", run_id)
        if run is None:
            raise ValueError(f"unknown sieve run: {run_id}")
        if run["document_side"] != document["document_side"]:
            raise ValueError("JSON side does not match sieve run side")
        if document.get("doc_id") and document["doc_id"] != run["doc_id"]:
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
                criterion_ordinals.get(row["criterion_id"], 0), int(row["item_id"].rsplit("-", 1)[1])
            )
        quote_group = max((int(row[0].rsplit("-", 2)[1]) for row in conn.execute(
            "SELECT q.quote_id FROM crumb_quotes q JOIN crumbs c ON c.item_id=q.item_id "
            "WHERE c.doc_id=?", (run["doc_id"],)
        )), default=0)
        for ordinal, item in enumerate(items, 1):
            criterion_ordinals[item["criterion_id"]] = criterion_ordinals.get(item["criterion_id"], 0) + 1
            crumb_ordinal = criterion_ordinals[item["criterion_id"]]
            quote_group += 1
            crumb_id = f"CRUMB-{run['doc_id']}-{item['criterion_id']}-{crumb_ordinal:04d}"
            quotes = item["evidence_quotes"]
            db_util.insert(conn, "crumbs", {"item_id": crumb_id, "doc_id": run["doc_id"],
                "sieve_run_id": run_id, "criterion_id": item["criterion_id"],
                "document_side": document["document_side"], "statement": item["statement"],
                "item_type": item.get("item_type"), "quote_language": quotes[0]["quote_language"]})
            sources = item.get("sources", item.get("source"))
            if isinstance(sources, dict):
                sources = [sources]
            for source in sources:
                db_util.insert(conn, "crumb_sources", {"item_id": crumb_id,
                    "source_locator": source["source_locator"], "source_page": source.get("source_page"),
                    "source_heading_path": source.get("source_heading_path")})
            default_locator = sources[0]["source_locator"]
            for qordinal, quote in enumerate(quotes, 1):
                db_util.insert(conn, "crumb_quotes", {"quote_id": f"QUOTE-{run['doc_id']}-{quote_group:04d}-{qordinal:02d}",
                    "item_id": crumb_id, "quote_original": quote["quote_original"],
                    "quote_language": quote["quote_language"],
                    "source_locator": quote.get("source_locator", default_locator)})
            refs = item.get("authority_references", document["authority_references"])
            for ref in refs:
                db_util.insert(conn, "crumb_authority_refs", {"item_id": crumb_id,
                    "authority_role": ref["authority_role"], "source_code": ref["source_code"],
                    "source_locator": ref["source_locator"],
                    "applicability": ref.get("applicability", "APPLICABLE"),
                    "applicability_basis": ref.get("applicability_basis")})
        conn.execute("UPDATE sieve_runs SET completed_at=CURRENT_TIMESTAMP WHERE run_id=?", (run_id,))
        return len(items)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--metrics-dir", type=Path)
    args = parser.parse_args()
    try:
        count = import_file(args.db, args.json_file, run_id=args.run_id, strict=args.strict)
        import sieve_metrics
        metrics_json, _, _ = sieve_metrics.generate(args.db, args.run_id, args.metrics_dir)
        print(f"import_crumbs: PASS - {count} crumb(s); metrics={metrics_json}")
        return 0
    except (ValueError, OSError) as exc:
        print(f"import_crumbs: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
