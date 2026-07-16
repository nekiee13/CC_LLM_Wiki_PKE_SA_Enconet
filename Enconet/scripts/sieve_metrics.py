#!/usr/bin/env python3
"""Generate deterministic JSON and Markdown quality metrics for one sieve generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import db_util


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "sieving" / "runs"


def _rate(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 1) if denominator else 0.0


def calculate(db: Path, run_id: str) -> dict[str, object]:
    with db_util.connect(db) as conn:
        run = db_util.lookup(conn, "sieve_runs", "run_id", run_id)
        if run is None:
            raise ValueError(f"unknown sieve run: {run_id}")
        criteria = [row[0] for row in conn.execute("SELECT criterion_id FROM criteria ORDER BY rowid")]
        counts = {criterion: 0 for criterion in criteria}
        crumbs = conn.execute(
            "SELECT * FROM crumbs WHERE sieve_run_id=? ORDER BY criterion_id,item_id", (run_id,)
        ).fetchall()
        complete_statement = complete_item_type = complete_language = complete_sources = complete_quotes = 0
        quote_total = linked_quotes = 0
        for crumb in crumbs:
            counts[crumb["criterion_id"]] += 1
            complete_statement += bool(crumb["statement"].strip())
            complete_item_type += bool(crumb["item_type"] and crumb["item_type"].strip())
            complete_language += bool(crumb["quote_language"])
            sources = conn.execute("SELECT count(*) FROM crumb_sources WHERE item_id=?", (crumb["item_id"],)).fetchone()[0]
            quotes = conn.execute("SELECT count(*) FROM crumb_quotes WHERE item_id=?", (crumb["item_id"],)).fetchone()[0]
            linked = conn.execute(
                "SELECT count(DISTINCT quote_id) FROM crumb_chunk_links WHERE item_id=?", (crumb["item_id"],)
            ).fetchone()[0]
            complete_sources += sources > 0
            complete_quotes += quotes > 0
            quote_total += quotes
            linked_quotes += linked
        total = len(crumbs)
        previous = None
        if run["supersedes_run_id"]:
            previous_total = conn.execute(
                "SELECT count(*) FROM crumbs WHERE sieve_run_id=?", (run["supersedes_run_id"],)
            ).fetchone()[0]
            previous = {"run_id": run["supersedes_run_id"], "crumb_count": previous_total,
                        "crumb_delta": total - previous_total}
        return {
            "schema_version": "1.0", "run_id": run_id, "doc_id": run["doc_id"],
            "generation": run["generation"], "prompt_version": run["prompt_version"],
            "status": run["status"], "crumb_count": total,
            "crumbs_per_criterion": counts,
            "zero_crumb_criteria": [key for key, value in counts.items() if value == 0],
            "field_completeness_percent": {
                "statement": _rate(complete_statement, total),
                "item_type": _rate(complete_item_type, total),
                "quote_language": _rate(complete_language, total),
                "source": _rate(complete_sources, total),
                "evidence_quote": _rate(complete_quotes, total),
            },
            "quote_verification": {"linked": linked_quotes, "total": quote_total,
                                   "rate_percent": _rate(linked_quotes, quote_total)},
            "rejected_item_count": run["rejected_item_count"],
            "failed_item_count": run["failed_item_count"],
            "previous_generation": previous,
        }


def render_markdown(metrics: dict[str, object]) -> str:
    completeness = metrics["field_completeness_percent"]
    verification = metrics["quote_verification"]
    previous = metrics["previous_generation"]
    lines = [
        f"# Sieve metrics — {metrics['run_id']}", "",
        f"- Document: `{metrics['doc_id']}`", f"- Generation: {metrics['generation']}",
        f"- Prompt: `{metrics['prompt_version']}`", f"- Status: `{metrics['status']}`",
        f"- Crumbs: {metrics['crumb_count']}",
        f"- Quote verification: {verification['linked']}/{verification['total']} ({verification['rate_percent']}%)",
        f"- Rejected items: {metrics['rejected_item_count']}",
        f"- Failed items: {metrics['failed_item_count']}", "",
        "## Zero-crumb criteria", "",
        ", ".join(metrics["zero_crumb_criteria"]) or "None", "",
        "## Field completeness", "", "| Field | Complete |", "|---|---:|",
    ]
    lines.extend(f"| {field} | {value}% |" for field, value in completeness.items())
    lines.extend(["", "## Crumbs per criterion", "", "| Criterion | Count |", "|---|---:|"])
    lines.extend(f"| {criterion} | {count} |" for criterion, count in metrics["crumbs_per_criterion"].items())
    lines.extend(["", "## Previous generation", ""])
    lines.append("None" if previous is None else
                 f"`{previous['run_id']}`: {previous['crumb_count']} crumbs; delta {previous['crumb_delta']:+d}")
    return "\n".join(lines) + "\n"


def generate(db: Path, run_id: str, output_dir: Path | None = None) -> tuple[Path, Path, dict[str, object]]:
    metrics = calculate(db, run_id)
    directory = output_dir or RUNS / run_id
    directory.mkdir(parents=True, exist_ok=True)
    json_path, markdown_path = directory / "metrics.json", directory / "metrics.md"
    json_path.write_text(json.dumps(metrics, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(metrics), encoding="utf-8")
    return json_path, markdown_path, metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    try:
        json_path, markdown_path, _ = generate(args.db, args.run_id, args.output_dir)
        print(f"sieve_metrics: PASS - {json_path}; {markdown_path}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"sieve_metrics: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
