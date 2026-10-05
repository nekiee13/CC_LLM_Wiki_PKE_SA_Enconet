"""Contract checks for the pre-score UMBRA evidence dashboard."""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_evidence_dashboard import build_data, render


ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "db" / "nqa_audit.sqlite"
MATRIX = ROOT / "out" / "2026-10-05" / "MIN-3.1-evidence-matrix-v4.json"
STATE = ROOT / "project-state.yml"


def test_dashboard_uses_current_evidence_and_withholds_score() -> None:
    data = build_data(DB, MATRIX, STATE, "RUN-20261003-32", "2026-10-05", "DASH-20261005-0001")
    assert data["metrics"]["qms_files"] == 24
    assert data["metrics"]["vendor_crumbs"] == 189
    assert data["metrics"]["active_quotes"] == 321
    assert data["metrics"]["quote_exact_records"] == 319
    assert data["metrics"]["quote_non_exact_records"] == 2
    assert data["metrics"]["criteria_with_vendor_crumbs"] == 13
    assert len(data["criteria"]) == 18
    assert len(data["batches"]) == 10
    assert data["score_state"] == "Withheld"
    assert data["classification_state"] == "Withheld"
    assert data["metrics"]["judgments"] == 0


def test_dashboard_html_is_offline_and_has_no_false_failure_label() -> None:
    data = build_data(DB, MATRIX, STATE, "RUN-20261003-32", "2026-10-05", "DASH-20261005-0001")
    raw_page = render(data)
    page = raw_page.casefold()
    for forbidden in ("login.microsoftonline.com", "oauth", "signin", "https://cdn.", "unpkg.com"):
        assert forbidden not in page
    assert "withheld" in page
    assert "no direct vendor crumb" in page
    assert 'id="judgments"' in page
    assert "fill-undetermined" in page
    assert "export-judgments" in page
    assert 'id="export-judgments" disabled' in page
    assert "updateexportstate" in page
    assert "judgment-rows" in page
    assert "<span class=\"tag blocked\">fail</span>" not in page
    assert json.loads(raw_page.split('id="dashboard-data" type="application/json">', 1)[1].split("</script>", 1)[0]) == data
