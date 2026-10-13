#!/usr/bin/env python3
"""Validate the independent EPIC16 scoring and dashboard benchmark classes."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml

ENCONET = Path(__file__).resolve().parents[1]
SCRIPTS = ENCONET / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_dashboard_data  # noqa: E402
import evaluation_engine  # noqa: E402
import generate_dashboard  # noqa: E402
import validate_dashboard  # noqa: E402

ROOT = Path(__file__).resolve().parent
SCORING = ROOT / "scoring"
DASHBOARD = ROOT / "dashboard_rendering"
MODEL = ENCONET / "schemas" / "scoring_model.yml"
TAXONOMY = ENCONET / "schemas" / "app_b_taxonomy.yml"
RATINGS = {"fully", "substantially", "partially", "minimally", "unmet", "undetermined", "na"}


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"benchmark root must be an object: {path}")
    return value


def validate_scoring() -> list[str]:
    source, expected = _load(SCORING / "input.yml"), _load(SCORING / "expected.yml")
    errors: list[str] = []
    ratings = source.get("ratings", {})
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))["criteria"]
    criterion_ids = [row["criterion_id"] for row in taxonomy]
    if source.get("benchmark_class") != "scoring" or expected.get("benchmark_class") != "scoring":
        errors.append("scoring benchmark_class mismatch")
    if list(ratings) != criterion_ids:
        errors.append("scoring fixture must contain all 18 criteria in canonical order")
    if set(ratings.values()) != RATINGS:
        errors.append("scoring fixture must represent every rating exactly as a set")
    model = evaluation_engine.model()
    if expected.get("scoring_model_version") != model.get("model_version"):
        errors.append("scoring fixture model version differs; re-approval and fixture bump required")
    digest = hashlib.sha256(MODEL.read_bytes()).hexdigest()
    if expected.get("scoring_model_sha256") != digest:
        errors.append("scoring model checksum differs; re-approval and fixture bump required")
    actual_scores = {criterion_id: evaluation_engine.score_rating(rating)
                     for criterion_id, rating in ratings.items()}
    if actual_scores != expected.get("per_criterion_scores"):
        errors.append("per-criterion scores differ from locked expected values")
    actual_metrics = evaluation_engine.metrics([{"rating": rating} for rating in ratings.values()])
    if actual_metrics != expected.get("metrics"):
        errors.append("consolidated scoring metrics differ from locked expected values")
    if not expected.get("verification", {}).get("verified_at_creation"):
        errors.append("scoring fixture lacks hand-verification evidence")
    return errors


def validate_dashboard_rendering() -> list[str]:
    package, contract = _load(DASHBOARD / "package.yml"), _load(DASHBOARD / "expected.yml")
    errors: list[str] = []
    if (package.get("benchmark_class") != "dashboard_rendering"
            or contract.get("benchmark_class") != "dashboard_rendering"):
        errors.append("dashboard benchmark_class mismatch")
    ratings = [row.get("classification") for row in package.get("evaluations", [])]
    if len(ratings) != 18 or set(ratings) != RATINGS:
        errors.append("dashboard fixture must contain 18 criteria and every rating")
    try:
        data = build_dashboard_data.build(
            package, generated_date=contract["generated_date"], dash_id=contract["dash_id"]
        )
        errors.extend(build_dashboard_data.validate_data(data))
        html = generate_dashboard.render(data)
        errors.extend(validate_dashboard.validate(package, data, html))
    except Exception as exc:  # noqa: BLE001 - benchmark collects one stable failure
        return errors + [f"dashboard benchmark execution failed: {exc}"]
    expected = contract["expected"]
    properties = {
        "criterion_card_count": len(data["criteria"]),
        "matrix_row_count": len(data["criteria"]),
        "weighted_score": data["weighted_score"],
        "applicable_count": data["applicable_count"],
        "classification": data["classification"],
        "classification_counts": data["classification_counts"],
    }
    for name, value in properties.items():
        if value != expected.get(name):
            errors.append(f"dashboard expected property differs: {name}")
    for section in expected["sections"]:
        if f'id="{section}"' not in html:
            errors.append(f"dashboard expected section missing: {section}")
    for function in expected["functions"]:
        if f"function {function}(" not in html:
            errors.append(f"dashboard expected function missing: {function}")
    for hook in expected["hooks"]:
        if hook not in html:
            errors.append(f"dashboard expected hook missing: {hook}")
    for binding in expected["bindings"]:
        if f'data-bind="{binding}"' not in html:
            errors.append(f"dashboard expected binding missing: {binding}")
    return list(dict.fromkeys(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--scoring", action="store_true")
    group.add_argument("--dashboard", action="store_true")
    args = parser.parse_args()
    selected = (["scoring"] if args.scoring else ["dashboard"] if args.dashboard
                else ["scoring", "dashboard"])
    failed = False
    for name in selected:
        errors = validate_scoring() if name == "scoring" else validate_dashboard_rendering()
        if errors:
            failed = True
            for error in errors:
                print(f"benchmark_{name}: FAIL - {error}", file=sys.stderr)
        else:
            print(f"benchmark_{name}: PASS")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
