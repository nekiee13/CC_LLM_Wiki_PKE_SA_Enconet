from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[2]
EXPECTED_FIELDS = {"project_ref", "contract_ref", "supplier_ref", "source_revision", "evidence_date"}


def load_context():
    return yaml.safe_load((PROJECT / "schemas" / "evidence_context.yml").read_text(encoding="utf-8"))


def test_context_contract_has_only_optional_source_anchors():
    data = load_context()
    assert set(data["context_fields"]) == EXPECTED_FIELDS
    assert all(spec["type"] == "string" for spec in data["context_fields"].values())


def test_evidence_types_separate_objective_records_from_leads():
    types = load_context()["evidence_types"]
    assert len(types) == len(set(types))
    assert "objective_record" in types
    assert "candidate_lead" in types
