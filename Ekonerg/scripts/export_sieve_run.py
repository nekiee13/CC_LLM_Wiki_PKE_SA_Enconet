#!/usr/bin/env python3
"""Export one completed local sieve run without changing the database."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3

import db_util
from project_paths import local_path


ROOT = Path(__file__).resolve().parents[1]


def export_run(db: Path, run_id: str) -> dict[str, object]:
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    with db_util.connect(database) as conn:
        run = db_util.lookup(conn, "sieve_runs", "run_id", run_id)
        if run is None or run["completed_at"] is None:
            raise ValueError("run is missing or incomplete")
        document = db_util.lookup(conn, "documents", "doc_id", run["doc_id"])
        if document is None:
            raise ValueError("run document is missing")
        authorities = [dict(row) for row in conn.execute(
            "SELECT authority_role,source_code,source_locator,applicability,"
            "applicability_basis FROM sieve_run_authorities WHERE run_id=? "
            "ORDER BY authority_role,source_code,source_locator", (run_id,)
        )]
        items: list[dict[str, object]] = []
        rows = conn.execute(
            "SELECT c.*, cr.criterion_name FROM crumbs c "
            "JOIN criteria cr ON cr.criterion_id=c.criterion_id "
            "WHERE c.sieve_run_id=? ORDER BY c.item_id", (run_id,)
        ).fetchall()
        for crumb in rows:
            sources = [dict(row) for row in conn.execute(
                "SELECT source_locator,source_page,source_heading_path "
                "FROM crumb_sources WHERE item_id=? ORDER BY source_id",
                (crumb["item_id"],),
            )]
            quotes = [dict(row) for row in conn.execute(
                "SELECT quote_original,quote_language,source_locator "
                "FROM crumb_quotes WHERE item_id=? ORDER BY quote_id",
                (crumb["item_id"],),
            )]
            context_row = conn.execute(
                "SELECT evidence_type,project_ref,contract_ref,supplier_ref,"
                "source_revision,evidence_date FROM crumb_context WHERE item_id=?",
                (crumb["item_id"],),
            ).fetchone()
            item: dict[str, object] = {
                "item_id": crumb["item_id"],
                "criterion_id": crumb["criterion_id"],
                "criterion_name": crumb["criterion_name"],
                "statement": crumb["statement"],
                "item_type": crumb["item_type"],
                "entities": {},
                "sources": sources,
                "evidence_quotes": quotes,
            }
            if context_row is not None:
                context = {key: context_row[key] for key in (
                    "project_ref", "contract_ref", "supplier_ref",
                    "source_revision", "evidence_date") if context_row[key]}
                if context_row["evidence_type"] or context:
                    item["evidence_type"] = context_row["evidence_type"]
                    item["context"] = context
            items.append(item)
        return {
            "prompt_version": run["prompt_version"],
            "document": {
                "doc_id": document["doc_id"], "name": document["filename"],
                "date": document["doc_date"] or "n-a",
                "document_side": document["document_side"],
                "authority_references": authorities,
            },
            "items": items,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = export_run(args.db, args.run_id)
    output = local_path(args.output)
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8", newline="\n")
    print(f"export_sieve_run: PASS - {args.run_id}; items={len(payload['items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
