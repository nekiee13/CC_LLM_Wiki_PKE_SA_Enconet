from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[2]
EXPECTED_IDS = [
    "ACT_CONTRACTING", "ACT_DESIGN", "ACT_COMMERCIAL_DEDICATION", "ACT_SOFTWARE_QA",
    "ACT_PROCUREMENT", "ACT_PRODUCTION_HANDLING", "ACT_SPECIAL_PROCESSES",
    "ACT_TESTING_INSPECTION", "ACT_DOCUMENT_CONTROL", "ACT_ORGANIZATION_PROGRAM",
    "ACT_NONCONFORMING_PART21", "ACT_INTERNAL_AUDITS", "ACT_CORRECTIVE_ACTION",
    "ACT_TRAINING_CERTIFICATION", "ACT_FIELD_SERVICES", "ACT_RECORDS", "ACT_ISO_CONTEXT",
]
EXPECTED_CRITERIA = {f"APP_B_{roman}" for roman in (
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
    "XIII", "XIV", "XV", "XVI", "XVII", "XVIII")}


def load_catalog():
    return yaml.safe_load((PROJECT / "schemas" / "activity_catalog.yml").read_text(encoding="utf-8"))


def test_catalog_preserves_historic_order_and_shape():
    data = load_catalog()
    rows = data["activities"]
    assert data["catalog_id"] == "SUPPLIER_AUDIT_ACTIVITIES"
    assert [row["activity_id"] for row in rows] == EXPECTED_IDS
    assert [row["report_order"] for row in rows] == list(range(1, 18))
    assert len(rows) == 17


def test_catalog_is_many_to_many_and_keeps_iso_context_outside_appendix_b():
    rows = load_catalog()["activities"]
    mapped = {criterion for row in rows for criterion in row["criterion_ids"]}
    assert mapped == EXPECTED_CRITERIA
    iso = next(row for row in rows if row["activity_id"] == "ACT_ISO_CONTEXT")
    assert iso["criterion_ids"] == []
    assert iso["out_of_baseline"] is True
    assert any(len(row["criterion_ids"]) > 1 for row in rows)
