#!/usr/bin/env python3
"""Preview or create one measured, inactive sieve candidate from local records."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

import db_util
import import_crumbs
import link_crumbs
from project_paths import configure_standard_streams, local_path
import sieve_diff
import sieve_metrics
import sieve_run
import sieving_lib  # noqa: F401 - copied extractor source is local
from json_extractor.crumb_validation import validate_file

ROOT = Path(__file__).resolve().parents[1]


def preflight(db: Path, *, run_id: str, doc_id: str, prompt_version: str,
              document_side: str, json_file: Path, authorities: list[dict]) -> dict:
    patterns = db_util.id_patterns()
    if patterns["run_id"].fullmatch(run_id) is None:
        raise ValueError(f"invalid sieve run ID: {run_id}")
    if patterns["doc_id"].fullmatch(doc_id) is None:
        raise ValueError(f"invalid document ID: {doc_id}")
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    source = local_path(json_file)
    if not source.is_relative_to(ROOT / "sieving"):
        raise ValueError("resieve JSON must be inside the local sieving folder")
    payload, validation = validate_file(source, strict=True)
    if not validation.passed:
        raise ValueError("strict crumb validation failed: " + "; ".join(validation.errors))
    if payload["document"].get("doc_id") != doc_id or payload["document"]["document_side"] != document_side:
        raise ValueError("JSON document identity or side differs from requested run")
    sieve_run._check_references(authorities, document_side)
    output = local_path(ROOT / "sieving" / "runs" / run_id)
    if output.exists():
        raise ValueError("candidate output path already exists; prior evidence is immutable")
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        document = db_util.lookup(conn, "documents", "doc_id", doc_id)
        if document is None or document["document_side"] != document_side:
            raise ValueError("registered document is missing or has a different side")
        if db_util.lookup(conn, "sieve_runs", "run_id", run_id) is not None:
            raise ValueError("run ID already exists; candidate generations are immutable")
        prior = conn.execute("SELECT run_id,status,is_active,completed_at FROM sieve_runs "
                             "WHERE doc_id=? ORDER BY generation", (doc_id,)).fetchall()
        active = [row for row in prior if row["is_active"]]
        if len(active) != 1 or active[0]["status"] != "active" or active[0]["completed_at"] is None:
            raise ValueError("resieve needs one completed active generation")
        if any(row["status"] == "candidate" for row in prior):
            raise ValueError("an earlier candidate needs a recorded decision before another resieve")
        if not conn.execute("SELECT 1 FROM criteria LIMIT 1").fetchone():
            raise ValueError("local criterion baseline is empty")
    sieve_run._check_prompt(document_side, prompt_version, is_candidate=True)
    return {"run_id": run_id, "doc_id": doc_id,
            "previous_run_id": active[0]["run_id"], "status": "candidate",
            "mode": "preview", "next": "apply only after reviewing the local source and prompt"}


def execute(db: Path, *, run_id: str, doc_id: str, prompt_version: str,
            document_side: str, json_file: Path, authorities: list[dict],
            rejected_item_count: int = 0, failed_item_count: int = 0,
            apply: bool = False) -> dict:
    if rejected_item_count < 0 or failed_item_count < 0:
        raise ValueError("rejected and failed item counts cannot be negative")
    plan = preflight(db, run_id=run_id, doc_id=doc_id,
                     prompt_version=prompt_version, document_side=document_side,
                     json_file=json_file, authorities=authorities)
    if not apply:
        return plan
    created = sieve_run.create_run(
        db, run_id=run_id, doc_id=doc_id, prompt_version=prompt_version,
        document_side=document_side, authorities=authorities,
        rejected_item_count=rejected_item_count, failed_item_count=failed_item_count,
    )
    if created["status"] != "candidate" or created["supersedes_run_id"] != plan["previous_run_id"]:
        raise ValueError("resieve race: created run does not match previewed predecessor")
    imported = import_crumbs.import_file(db, json_file, run_id=run_id)
    linked = link_crumbs.link(db, run_id, apply=True)
    plan.update(mode="apply", imported=imported, links=linked["links_to_add"],
                unmatched=len(linked["unmatched"]), warning=created["warning"])
    if linked["unmatched"]:
        plan["next"] = "inspect unmatched quotes; metrics and diff were not generated"
        return plan
    output = ROOT / "sieving" / "runs" / run_id
    metrics_json, metrics_md, metrics = sieve_metrics.generate(db, run_id, output)
    diff_json, diff_md, _ = sieve_diff.generate(db, plan["previous_run_id"], run_id, output)
    plan.update(metrics=str(metrics_json), metrics_markdown=str(metrics_md),
                diff=str(diff_json), diff_markdown=str(diff_md),
                quote_verification_rate=metrics["quote_verification"]["rate_percent"],
                next="review metrics, diff, golden score, and human decision; candidate is inactive")
    return plan


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--prompt-version", required=True)
    parser.add_argument("--document-side", choices=["RULE", "DOCUMENT"], required=True)
    parser.add_argument("--json-file", type=Path, required=True)
    parser.add_argument("--authority-json", action="append", default=[])
    parser.add_argument("--rejected-item-count", type=int, default=0)
    parser.add_argument("--failed-item-count", type=int, default=0)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        result = execute(args.db, run_id=args.run_id, doc_id=args.doc_id,
                         prompt_version=args.prompt_version, document_side=args.document_side,
                         json_file=args.json_file,
                         authorities=[json.loads(row) for row in args.authority_json],
                         rejected_item_count=args.rejected_item_count,
                         failed_item_count=args.failed_item_count, apply=args.apply)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 2 if args.apply and result.get("unmatched") else 0
    except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"resieve_run: FAIL - {exc}; inspect local candidate before retry", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
