from __future__ import annotations

import csv
import sqlite3
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_state  # noqa: E402
import gate_packet  # noqa: E402
import session_continuity  # noqa: E402
import db_util  # noqa: E402
import validate_frontmatter  # noqa: E402


def state_fixture(tmp_path: Path, phase: str = "setup") -> Path:
    path = tmp_path / "project-state.yml"
    text = (ROOT / "project-state.yml").read_text(encoding="utf-8")
    text = text.replace("phase: setup", f"phase: {phase}", 1)
    path.write_text(text, encoding="utf-8")
    return path


def approvals_fixture(tmp_path: Path, rows: list[list[str]] | None = None) -> Path:
    path = tmp_path / "approvals.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["object_id", "decision", "date", "reviewer", "notes"])
        writer.writerows(rows or [])
    return path


def test_legal_successors_derive_from_canonical_vocabulary() -> None:
    states = audit_state.audit_states()
    assert audit_state.legal_successors("setup", states) == ["registered", "failed"]
    assert audit_state.legal_successors("chunked", states) == ["sieved", "failed"]
    assert audit_state.legal_successors("closed", states) == ["failed"]
    assert audit_state.legal_successors("failed", states) == []


def test_illegal_transition_names_current_and_legal_successors(tmp_path: Path) -> None:
    state = state_fixture(tmp_path)
    with pytest.raises(audit_state.StateError, match=r"from setup to sieved.*registered, failed"):
        audit_state.transition("sieved", state_path=state,
                               approvals=approvals_fixture(tmp_path),
                               log=tmp_path / "log.md")


def test_gate_must_be_recorded_then_approved_before_transition(tmp_path: Path) -> None:
    state = state_fixture(tmp_path)
    approvals = approvals_fixture(
        tmp_path, [["G1-RUN-test", "approved", "2026-07-16", "Owner", "go"]]
    )
    log = tmp_path / "log.md"
    log.write_text("# Log\n", encoding="utf-8")
    with pytest.raises(audit_state.StateError, match="G1 approval must be recorded"):
        audit_state.transition("registered", state_path=state, approvals=approvals, log=log)
    audit_state.record_gate_decision("G1", "G1-RUN-test", state_path=state,
                                     approvals=approvals, log=log)
    assert yaml.safe_load(state.read_text(encoding="utf-8"))["phase"] == "setup"
    audit_state.transition("registered", state_path=state, approvals=approvals, log=log)
    data = yaml.safe_load(state.read_text(encoding="utf-8"))
    assert data["phase"] == "registered"
    assert data["gates"]["G1"]["status"] == "approved"
    assert str(data["gates"]["G1"]["date"]) == "2026-07-16"
    assert data["gates"]["G1"]["decision_ref"] == "G1-RUN-test"
    assert "gate-decision" in log.read_text(encoding="utf-8")
    assert "setup -> registered" in log.read_text(encoding="utf-8")


@pytest.mark.parametrize("decision", ["rejected", "deferred"])
def test_non_approval_never_advances(decision: str, tmp_path: Path) -> None:
    state = state_fixture(tmp_path)
    approvals = approvals_fixture(
        tmp_path, [["G1-RUN-stop", decision, "2026-07-16", "Owner", "stop"]]
    )
    log = tmp_path / "log.md"
    log.write_text("", encoding="utf-8")
    audit_state.record_gate_decision("G1", "G1-RUN-stop", state_path=state,
                                     approvals=approvals, log=log)
    with pytest.raises(audit_state.StateError, match="G1 approval must be recorded"):
        audit_state.transition("registered", state_path=state, approvals=approvals, log=log)
    assert yaml.safe_load(state.read_text(encoding="utf-8"))["phase"] == "setup"


def test_failed_is_reachable_but_requires_reason(tmp_path: Path) -> None:
    state = state_fixture(tmp_path, "sieved")
    approvals = approvals_fixture(tmp_path)
    log = tmp_path / "log.md"
    log.write_text("", encoding="utf-8")
    with pytest.raises(audit_state.StateError, match="requires --reason"):
        audit_state.transition("failed", state_path=state, approvals=approvals, log=log)
    audit_state.transition("failed", state_path=state, approvals=approvals,
                           log=log, reason="integrity check failed")
    assert yaml.safe_load(state.read_text(encoding="utf-8"))["phase"] == "failed"


def test_status_reports_state_pending_gate_and_open_exceptions(tmp_path: Path) -> None:
    state = state_fixture(tmp_path, "chunked")
    exceptions = tmp_path / "exceptions.csv"
    exceptions.write_text("id,status\nA,open\nB,resolved\n", encoding="utf-8")
    text = audit_state.status_text(state_path=state, exceptions=exceptions)
    assert text == "current_state: chunked\npending_gate: G2\nopen_exceptions: 1"


def test_gate_packet_is_standalone_unique_and_recording_does_not_advance(tmp_path: Path) -> None:
    packet = tmp_path / "G1-enconet.md"
    gate_packet.create_packet(
        gate="G1", supplier="enconet", decision_ref="G1-RUN-packet",
        summary="Registry reviewed.", evidence="- manifests/documents.csv",
        validation="- PASS: registry validator", output=packet,
    )
    text = packet.read_text(encoding="utf-8")
    for heading in ("## Summary", "## Evidence pointers", "## Validation results",
                    "## Options and ELI5 explanation", "## Decision record"):
        assert heading in text
    assert "decision: pending" in text
    with pytest.raises(audit_state.StateError, match="already exists"):
        gate_packet.create_packet(
            gate="G1", supplier="enconet", decision_ref="G1-RUN-packet",
            summary="x", evidence="x", validation="x", output=packet,
        )
    with pytest.raises(audit_state.StateError, match="supplier enconet"):
        gate_packet.create_packet(
            gate="G1", supplier="enconet", decision_ref="G1-RUN-another",
            summary="x", evidence="x", validation="x", output=tmp_path / "G1-other.md",
        )
    state = state_fixture(tmp_path)
    approvals = approvals_fixture(
        tmp_path, [["G1-RUN-packet", "approved", "2026-07-16", "Owner", "go"]]
    )
    log = tmp_path / "log.md"
    log.write_text("", encoding="utf-8")
    gate_packet.record_packet(packet, state=state, approvals=approvals, log=log)
    assert yaml.safe_load(state.read_text(encoding="utf-8"))["phase"] == "setup"
    frontmatter, _ = gate_packet.split_frontmatter(packet.read_text(encoding="utf-8"))
    assert frontmatter["decision"] == "approved"
    assert frontmatter["reviewer"] == "Owner"


def test_session_start_reports_drift_in_progress_and_unfinished_run(tmp_path: Path) -> None:
    handoff = tmp_path / "HANDOFF.md"
    handoff.write_text("**Git:** `abc123`\n", encoding="utf-8")
    current = tmp_path / "current-status.md"
    current.write_text("phase: **setup**\n\n## Next action\nResume safely.\n", encoding="utf-8")
    index = tmp_path / "index.md"
    index.write_text("# Index\n", encoding="utf-8")
    state = state_fixture(tmp_path, "evaluated")
    database = tmp_path / "audit.db"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE evaluation_runs (run_id TEXT, completed_at TEXT)")
        connection.execute("INSERT INTO evaluation_runs VALUES ('RUN-open', NULL)")
    info, warnings = session_continuity.inspect_start(
        handoff=handoff, current_status=current, index=index, state=state,
        database=database, actual_head="def456789",
    )
    joined = "\n".join(info + warnings)
    assert "Git divergence" in joined
    assert "state divergence" in joined
    assert "IN-PROGRESS STATE evaluated" in joined
    assert "RESUME" in joined and "ROLLBACK" in joined
    assert "RUN-open" in joined


def test_session_continuity_uses_canonical_production_database() -> None:
    assert session_continuity.DATABASE == db_util.DEFAULT_DB
    assert session_continuity.DATABASE.name == "nqa_audit.sqlite"


@pytest.mark.parametrize(
    ("decision", "expected_status"),
    [("rejected", "closed"), ("deferred", "draft")],
)
def test_non_approved_packet_uses_valid_page_status(
    decision: str, expected_status: str, tmp_path: Path,
) -> None:
    packet = tmp_path / f"G1-{decision}.md"
    gate_packet.create_packet(
        gate="G1", supplier="enconet", decision_ref=f"G1-RUN-{decision}",
        summary="Reviewed.", evidence="- evidence", validation="- PASS", output=packet,
    )
    state = state_fixture(tmp_path)
    approvals = approvals_fixture(
        tmp_path,
        [[f"G1-RUN-{decision}", decision, "2026-07-16", "Owner", "decision"]],
    )
    log = tmp_path / "log.md"
    log.write_text("", encoding="utf-8")
    gate_packet.record_packet(packet, state=state, approvals=approvals, log=log)
    frontmatter, _ = gate_packet.split_frontmatter(packet.read_text(encoding="utf-8"))
    assert frontmatter["status"] == expected_status
    assert frontmatter["status"] in validate_frontmatter.STATUSES
    assert frontmatter["decision"] == decision
    assert yaml.safe_load(state.read_text(encoding="utf-8"))["phase"] == "setup"
