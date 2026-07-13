#!/usr/bin/env python3
"""Build the deterministic single-source EPIC8-11 evaluation package."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

import db_util
from evaluation_engine import metrics
from finding_workflow import APPROVALS, approval_rows

SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "evaluation_package_schema.yml"


def validate_package(package: dict) -> list[str]:
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    errors: list[str] = []
    for key in schema["required_top_level"]:
        if key not in package:
            errors.append(f"missing top-level field: {key}")
    if package.get("schema_version") != schema["schema_version"]:
        errors.append("schema_version mismatch")
    evaluations = package.get("evaluations", [])
    if len(evaluations) != schema["evaluation_count"]:
        errors.append(f"expected {schema['evaluation_count']} evaluations")
    for evaluation in evaluations:
        if evaluation.get("classification") not in schema["ratings"]:
            errors.append(f"invalid classification: {evaluation.get('classification')}")
    if evaluations and package.get("metrics") != metrics([
        {"rating": evaluation["classification"]} for evaluation in evaluations
    ]):
        errors.append("metrics do not recompute")
    for finding in package.get("findings", []):
        if finding.get("status") not in schema["finding_statuses"]:
            errors.append(f"invalid finding status: {finding.get('finding_id')}")
    for action in package.get("actions", []):
        if action.get("approval_status") not in schema["action_approval_statuses"]:
            errors.append(f"invalid action approval status: {action.get('action_id')}")
    if not isinstance(package.get("approvals", []), list):
        errors.append("approvals must be a list")
    return errors


def build(db: Path, run_id: str, approvals: Path = APPROVALS) -> dict:
    with db_util.connect(db) as conn:
        run = dict(conn.execute(
            "SELECT * FROM evaluation_runs WHERE run_id=?", (run_id,)
        ).fetchone() or {})
        applicability = [dict(row) for row in conn.execute(
            "SELECT * FROM criterion_applicability WHERE evaluation_run_id=? ORDER BY criterion_id",
            (run_id,),
        )]
        evaluations = []
        for row in conn.execute(
            "SELECT e.*,c.criterion_name FROM criterion_evaluations e "
            "JOIN criteria c USING(criterion_id) WHERE evaluation_run_id=? ORDER BY criterion_id",
            (run_id,),
        ):
            item = dict(row)
            item["classification"] = item.pop("rating")
            item["evidence_ids"] = [value[0] for value in conn.execute(
                "SELECT item_id FROM evaluation_evidence WHERE evaluation_id=? ORDER BY item_id",
                (item["evaluation_id"],),
            )]
            evaluations.append(item)
        gaps = [dict(row) for row in conn.execute(
            "SELECT g.* FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) "
            "WHERE e.evaluation_run_id=? ORDER BY gap_id", (run_id,),
        )]
        findings = [dict(row) for row in conn.execute(
            "SELECT * FROM findings WHERE evaluation_run_id=? ORDER BY finding_id", (run_id,),
        )]
        actions = [dict(row) for row in conn.execute(
            "SELECT * FROM auditor_actions WHERE evaluation_run_id=? ORDER BY action_id", (run_id,),
        )]
    object_ids = {f"G{gate}-{run_id}" for gate in (2, 3, 4)}
    object_ids.update(row["finding_id"] for row in findings)
    object_ids.update(row["action_id"] for row in actions)
    relevant_approvals = [row for row in approval_rows(approvals)
                          if row.get("object_id") in object_ids]
    relevant_approvals.sort(key=lambda row: (row.get("object_id", ""), row.get("date", "")))
    return {
        "schema_version": "1.0", "run": run, "applicability": applicability,
        "evaluations": evaluations,
        "metrics": metrics([{"rating": row["classification"]} for row in evaluations]),
        "gaps": gaps, "findings": findings, "actions": actions,
        "approvals": relevant_approvals,
    }


def validate_source(package: dict, db: Path, approvals: Path = APPROVALS) -> list[str]:
    """Prove that a package is the canonical projection of its controlled sources."""
    run_id = package.get("run", {}).get("run_id")
    if not run_id:
        return ["package run_id missing for source verification"]
    rebuilt = build(db, run_id, approvals)
    if render(rebuilt) != render(package):
        return ["package/source mismatch: canonical DB and approvals projection differs"]
    return []


def render(package: dict) -> bytes:
    errors = validate_package(package)
    if errors:
        raise ValueError("invalid evaluation package: " + "; ".join(errors))
    return (json.dumps(package, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = build(args.db, args.run_id, args.approvals)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(render(package))
    print(f"build_evaluation_package: PASS - {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
