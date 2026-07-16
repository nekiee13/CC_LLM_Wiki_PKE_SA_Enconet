#!/usr/bin/env python3
"""Create a new immutable sieve generation, then import, link, measure, and diff it."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import db_util
import import_crumbs
import link_crumbs
import sieve_diff
import sieve_metrics
import sieve_run
import sieving_lib  # noqa: F401
from json_extractor.crumb_validation import validate_file


ROOT = Path(__file__).resolve().parents[1]


def execute(
    db: Path, *, run_id: str, doc_id: str, prompt_version: str,
    document_side: str, json_file: Path, authorities: list[dict],
    output_root: Path, candidates: Path, rejected_item_count: int = 0,
    failed_item_count: int = 0,
) -> dict[str, object]:
    _, validation = validate_file(json_file, strict=True)
    if not validation.passed:
        raise ValueError("strict crumb validation failed: " + "; ".join(validation.errors))
    created = sieve_run.create_run(
        db, run_id=run_id, doc_id=doc_id, prompt_version=prompt_version,
        document_side=document_side, authorities=authorities,
        rejected_item_count=rejected_item_count, failed_item_count=failed_item_count,
    )
    previous = created["supersedes_run_id"]
    if previous is None:
        raise ValueError("audit-resieve requires a previous active generation; use audit-sieve first")
    imported = import_crumbs.import_file(db, json_file, run_id=run_id, strict=True)
    links, unmatched = link_crumbs.link(db, candidates_path=candidates)
    metrics_json, metrics_md, metrics = sieve_metrics.generate(db, run_id, output_root / run_id)
    diff_json, diff_md, _ = sieve_diff.generate(db, str(previous), run_id, output_root / run_id)
    return {"run_id": run_id, "previous_run_id": previous, "imported": imported,
            "links": links, "unmatched": len(unmatched), "metrics": str(metrics_json),
            "metrics_markdown": str(metrics_md), "diff": str(diff_json),
            "diff_markdown": str(diff_md), "warning": created["warning"],
            "quote_verification_rate": metrics["quote_verification"]["rate_percent"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--prompt-version", required=True)
    parser.add_argument("--document-side", choices=["RULE", "DOCUMENT"], required=True)
    parser.add_argument("--json-file", type=Path, required=True)
    parser.add_argument("--authority-json", action="append", default=[])
    parser.add_argument("--output-root", type=Path, default=ROOT / "sieving" / "runs")
    parser.add_argument("--candidates", type=Path,
                        default=ROOT / "manifests" / "link_exception_candidates.csv")
    parser.add_argument("--rejected-item-count", type=int, default=0)
    parser.add_argument("--failed-item-count", type=int, default=0)
    args = parser.parse_args()
    try:
        result = execute(
            args.db, run_id=args.run_id, doc_id=args.doc_id,
            prompt_version=args.prompt_version, document_side=args.document_side,
            json_file=args.json_file, authorities=[json.loads(value) for value in args.authority_json],
            output_root=args.output_root, candidates=args.candidates,
            rejected_item_count=args.rejected_item_count,
            failed_item_count=args.failed_item_count,
        )
        print("resieve_run: PASS - " + json.dumps(result, sort_keys=True))
        print("STOP: candidate generation is not active; inspect metrics, diff, and golden score")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"resieve_run: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
