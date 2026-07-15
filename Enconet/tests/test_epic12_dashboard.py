"""EPIC12 package projection, offline rendering, consistency, and JS smoke tests."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import build_dashboard_data  # noqa: E402
import evaluation_engine  # noqa: E402
import generate_dashboard  # noqa: E402
import validate_dashboard  # noqa: E402


def package(language: str = "en") -> dict:
    taxonomy = yaml.safe_load((ENCONET / "schemas" / "app_b_taxonomy.yml").read_text(encoding="utf-8"))["criteria"]
    evaluations, applicability = [], []
    for index, taxon in enumerate(taxonomy):
        criterion_id = taxon["criterion_id"]
        rating = "na" if index == 17 else ("partially" if index == 0 else "undetermined")
        evaluations.append({
            "evaluation_id": f"EVAL-{criterion_id}", "criterion_id": criterion_id,
            "criterion_name": taxon["criterion_name"], "classification": rating,
            "score": evaluation_engine.score_rating(rating),
            "affirmative_summary": "Supplier evidence reviewed </script>" if index == 0 else "No affirmative evidence",
            "contrary_summary": "Additional verification is needed",
            "judge_ruling": "Evidence is insufficient", "rationale": "Reviewed evidence",
            "evidence_ids": ["CRUMB-DOC-0001-APP_B_I-0001"] if index == 0 else [],
        })
        applicability.append({
            "criterion_id": criterion_id, "applicable": 0 if rating == "na" else 1,
            "justification": "Approved scope exclusion" if rating == "na" else "Approved scope",
            "scope_source_doc_id": "DOC-0001",
        })
    metrics = evaluation_engine.metrics([{"rating": row["classification"]} for row in evaluations])
    run_id = "RUN-20260715-01"
    approvals = [{
        "object_id": f"{gate}-{run_id}", "decision": "approved", "date": "2026-07-15",
        "reviewer": "owner", "notes": "fixture",
    } for gate in ("G2", "G3", "G4")] + [{
        "object_id": object_id, "decision": "approved", "date": "2026-07-15",
        "reviewer": "owner", "notes": "fixture",
    } for object_id in ("FIND-0001", "ACT-0001")]
    return {
        "schema_version": "1.0",
        "run": {"run_id": run_id, "supplier": "enconet", "deliverable_language": language,
                "scoring_model_version": "fixture-1"},
        "applicability": applicability, "evaluations": evaluations, "metrics": metrics,
        "gaps": [{"gap_id": "GAP-APP_B_I-01", "evaluation_id": "EVAL-APP_B_I",
                  "description": "Need broader sample", "evidence_item_id": None,
                  "missing_evidence_ref": "supplier sample"}],
        "findings": [{"finding_id": "FIND-0001", "status": "approved", "title": "Sample gap",
                      "body": "The sample is incomplete", "evidence_item_id": None,
                      "gap_id": "GAP-APP_B_I-01"}],
        "actions": [{"action_id": "ACT-0001", "approval_status": "approved", "priority": 1,
                     "description": "Expand sample", "finding_id": "FIND-0001", "gap_id": None}],
        "approvals": approvals,
    }


def dashboard_data(language: str = "en") -> tuple[dict, dict]:
    source = package(language)
    data = build_dashboard_data.build(
        source, generated_date="2026-07-15", dash_id="DASH-20260715-0001"
    )
    return source, data


def test_builder_projects_exact_contract_and_na_justification():
    source, data = dashboard_data()
    assert len(data["criteria"]) == 18
    assert data["weighted_score"] == source["metrics"]["consolidated_score"]
    assert data["classification_counts"] == source["metrics"]["classification_counts"]
    assert data["criteria"][-1]["rating"] == "na"
    assert "[applicability:Approved scope exclusion]" in data["criteria"][-1]["judge"]
    assert data["priority_actions"][0]["criterion_id"] == "APP_B_I"
    assert data["criteria"][0]["verify"] == ["ACT-0001"]
    assert build_dashboard_data.validate_data(data) == []
    reloaded = json.loads(json.dumps(data, sort_keys=True))
    assert build_dashboard_data.validate_data(reloaded) == []


def test_builder_normalizes_package_lexical_order_to_regulation_order():
    source = package()
    source["evaluations"] = sorted(source["evaluations"], key=lambda row: row["criterion_id"])
    source["applicability"] = sorted(source["applicability"], key=lambda row: row["criterion_id"])
    data = build_dashboard_data.build(
        source, generated_date="2026-07-15", dash_id="DASH-20260715-0001"
    )
    assert [row["order"] for row in data["criteria"]] == list(range(1, 19))
    assert data["criteria"][8]["n"] == "APP_B_IX"


@pytest.mark.parametrize("language,translated", [("en", "Executive summary"),
                                                   ("sl", "Povzetek"),
                                                   ("hr", "Sažetak")])
def test_renderer_is_deterministic_localized_self_contained_and_valid(language: str, translated: str):
    source, data = dashboard_data(language)
    first = generate_dashboard.render(data)
    second = generate_dashboard.render(data)
    assert first == second
    assert translated in first
    assert "\\u003c/script>" in first and "Supplier evidence reviewed </script>" not in first
    assert "DASH-20260715-0001" in first and "2026-07-15" in first
    assert "http://" not in first and "https://" not in first
    assert validate_dashboard.validate(source, data, first) == []


def test_validator_rejects_package_mismatch_invalid_rating_forbidden_content_and_broken_js():
    source, data = dashboard_data()
    html = generate_dashboard.render(data)
    altered = copy.deepcopy(data)
    altered["weighted_score"] = 99.9
    assert "dashboard/package mismatch: weighted_score" in validate_dashboard.validate(source, altered, html)
    altered = copy.deepcopy(data)
    altered["criteria"][0]["rating"] = "excellent"
    assert any("invalid dashboard rating" in error for error in validate_dashboard.validate(source, altered, html))
    forbidden = html.replace("Offline audit dashboard", "login.microsoftonline.com")
    assert any("forbidden dashboard pattern" in error for error in validate_dashboard.validate(source, data, forbidden))
    broken = html.replace("function filterCriteria(", "function removedFilterCriteria(")
    assert "missing dashboard JS function: filterCriteria" in validate_dashboard.validate(source, data, broken)


def test_builder_fails_closed_on_incomplete_or_inconsistent_package_projection():
    source = package()
    del source["evaluations"][0]["judge_ruling"]
    with pytest.raises(ValueError, match="judge_ruling"):
        build_dashboard_data.build(source, generated_date="2026-07-15", dash_id="DASH-20260715-0001")
    source = package()
    source["applicability"][-1]["applicable"] = 1
    with pytest.raises(ValueError, match="applicability/rating mismatch"):
        build_dashboard_data.build(source, generated_date="2026-07-15", dash_id="DASH-20260715-0001")
