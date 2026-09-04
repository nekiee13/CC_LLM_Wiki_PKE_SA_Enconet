"""EA5.4 fixed Owner UAT packet and human-gate preflight tests."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import validate_evidence_access_uat as uat  # noqa: E402


CONTRACT = ENCONET / "schemas" / "evidence_access_uat.yml"
PACKET = ENCONET / "docs" / "acceptance" / "EA5.4_OWNER_UAT.md"
PACKAGE_ROOT = ENCONET / "outputs" / "candidates" / "evidence_access" / "portable_package"


def test_corrected_uat_contract_has_exact_ten_step_owner_workflow():
    contract = uat.load_contract(CONTRACT)
    assert contract["schema_version"] == "1.0"
    assert contract["uat_id"] == "EA5.4-RUN-20260728-01"
    assert contract["status"] == "approved"
    assert contract["run_id"] == "RUN-20260728-01"
    assert [step["id"] for step in contract["steps"]] == [f"UAT-{n}" for n in range(1, 11)]
    assert [step["action"] for step in contract["steps"]] == [
        "open_report", "open_multi_quote_crumb", "confirm_source_identity",
        "navigate_adjacent_context", "copy_traceable_citation", "print_evidence_card",
        "open_second_criterion", "select_run_from_workspace",
        "open_document_record", "open_package_record",
    ]
    assert contract["primary_crumb_id"] == "CRUMB-DOC-0021-APP_B_I-0003"
    assert contract["secondary_crumb_id"] == "CRUMB-DOC-0021-APP_B_II-0002"
    assert contract["owner_decision"] == {
        "decision": "approve", "decided_at_utc": "2026-09-04T19:34:59Z",
        "decision_reference": "Owner chat approval on 2026-09-04: Owner approved corrected ten-step UAT",
        "observed_defects": [],
    }


def test_packet_and_artifacts_validate_without_mutation():
    before = {path: path.read_bytes() for path in PACKAGE_ROOT.rglob("*") if path.is_file()}
    errors, summary = uat.validate(CONTRACT, PACKET, ENCONET)
    assert errors == []
    assert summary == {"steps": 10, "artifacts": 4, "decision": "approve"}
    assert {path: path.read_bytes() for path in before} == before


def test_packet_is_plain_language_and_requires_human_decision():
    text = PACKET.read_text(encoding="utf-8")
    assert "No command line is needed" in text
    assert "Owner decision: **APPROVED**" in text
    assert "earlier approval remains historical evidence" in text
    for number in range(1, 11):
        assert f"### {number}." in text
    assert "Pass: [x]" in text
    assert "Decision: **APPROVE**" in text


def test_validator_rejects_artifact_tamper_and_incomplete_approval(tmp_path: Path):
    root = tmp_path / "project"
    shutil.copytree(PACKAGE_ROOT, root / "outputs" / "candidates" / "evidence_access" / "portable_package")
    (root / "schemas").mkdir(parents=True)
    (root / "docs" / "acceptance").mkdir(parents=True)
    contract_target = root / "schemas" / CONTRACT.name
    packet_target = root / "docs" / "acceptance" / PACKET.name
    shutil.copyfile(CONTRACT, contract_target)
    shutil.copyfile(PACKET, packet_target)
    viewer = root / "outputs" / "candidates" / "evidence_access" / "portable_package" / "RUN-20260728-01" / "evidence_explorer.html"
    viewer.write_text(viewer.read_text(encoding="utf-8") + "tamper", encoding="utf-8")
    errors, _summary = uat.validate(contract_target, packet_target, root)
    assert any("artifact hash mismatch" in error and "evidence_explorer.html" in error for error in errors)

    contract = uat.load_contract(CONTRACT)
    contract["status"] = "approved"
    contract["owner_decision"]["decision_reference"] = None
    contract_target.write_text(json.dumps(contract), encoding="utf-8")
    errors, _summary = uat.validate(contract_target, PACKET, ENCONET)
    assert "approved UAT requires a complete Owner decision" in errors


def test_cli_preflight_reports_human_gate(capsys):
    assert uat.main([
        "--contract", str(CONTRACT), "--packet", str(PACKET), "--project-root", str(ENCONET)
    ]) == 0
    output = capsys.readouterr().out
    assert "validate_evidence_access_uat: PASS" in output
    assert "steps=10 artifacts=4 decision=approve" in output
