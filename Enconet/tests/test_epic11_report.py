"""EPIC11 deterministic generation, gates, localization, and consistency tests."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import evaluation_engine  # noqa: E402
import generate_report  # noqa: E402
import validate_report  # noqa: E402


def package(language: str = "en") -> dict:
    evaluations = []
    applicability = []
    romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
              "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"]
    for index, roman in enumerate(romans):
        criterion = f"APP_B_{roman}"
        classification = "partially" if index == 0 else "undetermined"
        evaluations.append({
            "evaluation_id": f"EVAL-{criterion}", "criterion_id": criterion,
            "criterion_name": f"Criterion {roman}", "classification": classification,
            "rationale": "Reviewed evidence", "evidence_ids": ["CRUMB-DOC-0001-APP_B_I-0001"] if index == 0 else [],
        })
        applicability.append({
            "criterion_id": criterion, "applicable": 1, "justification": "Approved scope",
            "scope_source_doc_id": "DOC-0001",
        })
    metrics = evaluation_engine.metrics([{"rating": row["classification"]} for row in evaluations])
    run_id = "RUN-20260713-02"
    approvals = [
        {"object_id": f"{gate}-{run_id}", "decision": "approved", "date": "2026-07-13", "reviewer": "owner", "notes": "ok"}
        for gate in ("G2", "G3", "G4")
    ] + [
        {"object_id": object_id, "decision": "approved", "date": "2026-07-13", "reviewer": "owner", "notes": "ok"}
        for object_id in ("FIND-0001", "ACT-0001")
    ]
    return {
        "schema_version": "1.0",
        "run": {"run_id": run_id, "supplier": "enconet", "deliverable_language": language,
                "scoring_model_version": "approved-1"},
        "applicability": applicability, "evaluations": evaluations, "metrics": metrics,
        "gaps": [{"gap_id": "GAP-APP_B_I-01", "description": "Need broader sample",
                  "evidence_item_id": "CRUMB-DOC-0001-APP_B_I-0001", "missing_evidence_ref": None}],
        "findings": [{"finding_id": "FIND-0001", "status": "approved", "title": "Sample gap",
                      "body": "The sample is incomplete", "evidence_item_id": None,
                      "gap_id": "GAP-APP_B_I-01"}],
        "actions": [{"action_id": "ACT-0001", "approval_status": "approved", "priority": 1,
                     "description": "Expand sample", "finding_id": "FIND-0001", "gap_id": None}],
        "approvals": approvals,
    }


def test_report_is_deterministic_localized_and_consistent():
    data = package("sl")
    first = generate_report.render(data)
    second = generate_report.render(data)
    assert first == second
    assert "## Povzetek" in first and "## Priporočila" in first
    assert "FIND-0001" in first and "ACT-0001" in first
    assert validate_report.validate(data, first) == []


def test_report_refuses_missing_gate_and_unapproved_objects_are_excluded():
    data = package()
    data["approvals"] = [row for row in data["approvals"] if row["object_id"] != "G4-RUN-20260713-02"]
    with pytest.raises(ValueError, match="G4"):
        generate_report.render(data)
    data = package()
    data["approvals"] = [row for row in data["approvals"] if row["object_id"] not in {"FIND-0001", "ACT-0001"}]
    report = generate_report.render(data)
    assert "FIND-0001" not in report and "ACT-0001" not in report


def test_validator_rejects_score_section_and_citation_tamper():
    data = package()
    report = generate_report.render(data)
    broken_score = report.replace(f"**{data['metrics']['consolidated_score']} / 100**", "**99.9 / 100**")
    assert "visible consolidated score mismatch" in validate_report.validate(data, broken_score)
    broken_citation = report.replace("[gap:GAP-APP_B_I-01]", "")
    assert "citation-less recommendation" in validate_report.validate(data, broken_citation)
