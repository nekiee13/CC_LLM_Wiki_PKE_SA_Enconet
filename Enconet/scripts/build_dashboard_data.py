#!/usr/bin/env python3
"""Build the deterministic EPIC12 dashboard-data projection from one package."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import db_util
from build_evaluation_package import validate_package, validate_source
from finding_workflow import APPROVALS
from generate_report import approved_ids, canonical_bytes

ENCONET = Path(__file__).resolve().parents[1]
SCHEMA = ENCONET / "schemas" / "dashboard_schema.yml"
TAXONOMY = ENCONET / "schemas" / "app_b_taxonomy.yml"
PATTERNS = ENCONET / "schemas" / "id_patterns.yml"
OUTPUTS = ENCONET / "outputs"


def _contracts() -> tuple[dict, list[dict], dict[str, str]]:
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    criteria = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))["criteria"]
    patterns = yaml.safe_load(PATTERNS.read_text(encoding="utf-8"))["patterns"]
    return schema, criteria, {name: spec["regex"] for name, spec in patterns.items()}


def _action_criterion(action: dict, gaps: dict[str, dict], findings: dict[str, dict],
                      evaluations: dict[str, dict]) -> str | None:
    gap_id = action.get("gap_id")
    if not gap_id and action.get("finding_id") in findings:
        gap_id = findings[action["finding_id"]].get("gap_id")
    gap = gaps.get(gap_id or "", {})
    evaluation = evaluations.get(gap.get("evaluation_id", ""), {})
    return evaluation.get("criterion_id")


def build(package: dict, *, generated_date: str, dash_id: str) -> dict:
    """Project package values into the renderer contract without rescoring them."""
    package_errors = validate_package(package)
    if package_errors:
        raise ValueError("invalid evaluation package: " + "; ".join(package_errors))
    _, taxonomy, _ = _contracts()
    expected_ids = [row["criterion_id"] for row in taxonomy]
    evaluations = {row.get("criterion_id"): row for row in package["evaluations"]}
    applicability = {row.get("criterion_id"): row for row in package["applicability"]}
    if set(evaluations) != set(expected_ids) or set(applicability) != set(expected_ids):
        raise ValueError("package must contain exactly the canonical 18 criteria")

    criteria = []
    for order, taxon in enumerate(taxonomy, 1):
        criterion_id = taxon["criterion_id"]
        evaluation = evaluations[criterion_id]
        ruling = applicability[criterion_id]
        rating = evaluation.get("classification")
        applicable = bool(ruling.get("applicable"))
        if applicable == (rating == "na"):
            raise ValueError(f"applicability/rating mismatch: {criterion_id}")
        for field in ("affirmative_summary", "contrary_summary", "judge_ruling"):
            if not isinstance(evaluation.get(field), str):
                raise ValueError(f"package evaluation missing {field}: {criterion_id}")
        score = evaluation.get("score")
        if (applicable and not isinstance(score, (int, float))) or (not applicable and score is not None):
            raise ValueError(f"package score/applicability mismatch: {criterion_id}")
        judge = evaluation["judge_ruling"]
        if not applicable:
            justification = ruling.get("justification")
            source = ruling.get("scope_source_doc_id")
            if not justification or not source:
                raise ValueError(f"not-applicable criterion lacks justification reference: {criterion_id}")
            judge = f"{judge} [applicability:{justification}] [document:{source}]".strip()
        criteria.append({
            "n": criterion_id, "order": order, "title": taxon["criterion_name"],
            "rating": rating, "score": score,
            "refs": list(evaluation.get("evidence_ids", [])),
            "aff": evaluation["affirmative_summary"],
            "con": evaluation["contrary_summary"], "judge": judge, "verify": [],
        })

    gaps = {row["gap_id"]: row for row in package["gaps"]}
    findings = {row["finding_id"]: row for row in package["findings"]}
    evaluation_ids = {row.get("evaluation_id"): row for row in package["evaluations"]}
    approvals = approved_ids(package)
    priority_actions = []
    by_criterion = {row["n"]: row for row in criteria}
    for action in sorted(package["actions"], key=lambda row: row["action_id"]):
        if (action.get("approval_status") != "approved" or action.get("action_id") not in approvals
                or not action.get("priority")):
            continue
        criterion_id = _action_criterion(action, gaps, findings, evaluation_ids)
        refs = [value for value in (action.get("finding_id"), action.get("gap_id")) if value]
        projected = {
            "action_id": action["action_id"], "priority": action["priority"],
            "description": action["description"], "criterion_id": criterion_id,
            "refs": refs,
        }
        priority_actions.append(projected)
        if criterion_id in by_criterion:
            by_criterion[criterion_id]["verify"].append(action["action_id"])

    metrics = package["metrics"]
    run = package["run"]
    data = {
        "schema_version": "1.0", "supplier": run.get("supplier"),
        "generated_date": generated_date, "dash_id": dash_id,
        "run_id": run.get("run_id"),
        "deliverable_language": run.get("deliverable_language"),
        "weighted_score": metrics.get("consolidated_score"),
        "applicable_count": metrics.get("applicable_count"),
        "classification_counts": metrics.get("classification_counts"),
        "classification": metrics.get("classification"),
        "package_sha256": hashlib.sha256(canonical_bytes(package)).hexdigest(),
        "criteria": criteria, "priority_actions": priority_actions,
    }
    errors = validate_data(data)
    if errors:
        raise ValueError("invalid dashboard data: " + "; ".join(errors))
    return data


def validate_data(data: dict) -> list[str]:
    schema, taxonomy, patterns = _contracts()
    errors: list[str] = []
    required_top = schema["top_level_metrics"]["required_fields"]
    for field in required_top:
        if field not in data:
            errors.append(f"dashboard data missing top-level field: {field}")
    if data.get("schema_version") != schema["schema_version"]:
        errors.append("dashboard schema_version mismatch")
    for field, pattern in (("dash_id", "dashboard_id"), ("run_id", "run_id")):
        if not re.fullmatch(patterns[pattern], str(data.get(field, ""))):
            errors.append(f"invalid {field}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(data.get("generated_date", ""))):
        errors.append("invalid generated_date")
    if data.get("deliverable_language") not in {"sl", "en", "hr"}:
        errors.append("invalid deliverable_language")
    criteria = data.get("criteria")
    expected_ids = [row["criterion_id"] for row in taxonomy]
    if not isinstance(criteria, list) or len(criteria) != schema["criterion_object"]["count"]:
        errors.append("dashboard data must contain exactly 18 criteria")
        criteria = criteria if isinstance(criteria, list) else []
    fields = list(schema["criterion_object"]["required_fields"])
    if [row.get("n") for row in criteria] != expected_ids:
        errors.append("dashboard criteria differ from canonical regulation order")
    ratings = {"fully", "substantially", "partially", "minimally", "unmet", "undetermined", "na"}
    for index, row in enumerate(criteria, 1):
        if set(row) != set(fields):
            errors.append(f"criterion object fields mismatch: {row.get('n', index)}")
        if row.get("order") != index:
            errors.append(f"criterion order mismatch: {row.get('n', index)}")
        if row.get("rating") not in ratings:
            errors.append(f"invalid dashboard rating: {row.get('n', index)}")
        score = row.get("score")
        if row.get("rating") == "na" and score is not None:
            errors.append(f"not-applicable criterion score must be null: {row.get('n', index)}")
        elif row.get("rating") != "na" and not isinstance(score, (int, float)):
            errors.append(f"applicable criterion score must be numeric: {row.get('n', index)}")
        for field in ("refs", "verify"):
            if not isinstance(row.get(field), list):
                errors.append(f"criterion {field} must be a list: {row.get('n', index)}")
    counts = data.get("classification_counts")
    if not isinstance(counts, dict):
        errors.append("classification_counts must be an object")
    elif set(counts) != ratings or any(not isinstance(value, int) or value < 0 for value in counts.values()):
        errors.append("classification_counts must contain non-negative counts for every rating")
    elif sum(counts.values()) != len(criteria):
        errors.append("classification_counts total must equal criterion count")
    if not isinstance(data.get("priority_actions"), list):
        errors.append("priority_actions must be a list")
    return errors


def default_output(package: dict) -> Path:
    supplier = re.sub(r"[^a-z0-9_-]+", "-", package["run"].get("supplier", "supplier").casefold()).strip("-")
    return OUTPUTS / f"{supplier}_appendix_b_dashboard_data.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--generated-date", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--dash-id")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    args = parser.parse_args()
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"))
        source_errors = validate_source(package, args.db, args.approvals)
        if source_errors:
            raise ValueError(source_errors[0])
        compact_date = args.generated_date.replace("-", "")
        dash_id = args.dash_id or f"DASH-{compact_date}-0001"
        data = build(package, generated_date=args.generated_date, dash_id=dash_id)
        output = args.output or default_output(package)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8", newline="\n")
        print(f"build_dashboard_data: PASS - {output}")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI fail-closed boundary
        print(f"build_dashboard_data: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
