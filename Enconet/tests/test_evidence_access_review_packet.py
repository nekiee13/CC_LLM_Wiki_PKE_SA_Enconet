"""EA6.3 independent-review packet preparation tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import validate_evidence_access_review_packet as review  # noqa: E402


CONTRACT = ENCONET / "schemas" / "evidence_access_review_protocol.yml"
PACKET = ENCONET / "docs" / "reviews" / "EA6.3_CLAUDE_REVIEW_PACKET.md"


def test_protocol_pins_independent_reviewer_scope_and_blank_decision():
    contract = review.load_contract(CONTRACT)
    assert contract["schema_version"] == "1.0"
    assert contract["review_id"] == "EA6.3-RUN-20260728-01"
    assert contract["status"] == "awaiting_claude"
    assert contract["reviewer"] == "claude-code"
    assert contract["implementation_tip"] == "459e2412b99d529ab3e9268dbffdd74859b12b4e"
    assert contract["run_id"] == "RUN-20260728-01"
    assert len(contract["commands"]) == 8
    assert len(contract["risk_checks"]) >= 8
    assert contract["review_decision"] == {
        "decision": None, "reviewed_at_utc": None, "message_id": None, "findings": [],
    }


def test_packet_is_complete_and_current_but_does_not_self_approve():
    errors, summary = review.validate(CONTRACT, PACKET, ENCONET)
    assert errors == []
    assert summary == {"commands": 8, "risks": 10, "decision": "awaiting_claude"}
    text = PACKET.read_text(encoding="utf-8")
    assert "Claude must execute these checks independently" in text
    assert "Reviewer decision: **AWAITING CLAUDE**" in text
    assert "Codex must not complete the reviewer decision" in text


def test_packet_drift_and_premature_decision_fail_closed(tmp_path: Path):
    broken_packet = tmp_path / "packet.md"
    broken_packet.write_text(
        PACKET.read_text(encoding="utf-8").replace("review-command:aggregate", "review-command:removed"),
        encoding="utf-8",
    )
    errors, _ = review.validate(CONTRACT, broken_packet, ENCONET)
    assert "review packet missing command: aggregate" in errors

    value = review.load_contract(CONTRACT)
    value["review_decision"]["decision"] = "approve"
    broken_contract = tmp_path / "protocol.yml"
    broken_contract.write_text(json.dumps(value), encoding="utf-8")
    errors, _ = review.validate(broken_contract, PACKET, ENCONET)
    assert "awaiting review contains a premature reviewer decision" in errors


def test_cli_reports_pending_independent_gate(capsys):
    assert review.main([
        "--contract", str(CONTRACT), "--packet", str(PACKET), "--project-root", str(ENCONET),
    ]) == 0
    output = capsys.readouterr().out
    assert "validate_evidence_access_review_packet: PASS" in output
    assert "commands=8 risks=10 decision=awaiting_claude" in output
