from __future__ import annotations

import csv
import sqlite3
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_command  # noqa: E402
import validate_agent_interfaces  # noqa: E402
from audit_state import StateError  # noqa: E402


EXPECTED = {
    "audit-status", "audit-register", "audit-chunk", "audit-sieve",
    "audit-resieve", "audit-link", "audit-eval", "audit-report",
    "audit-dashboard", "audit-validate", "audit-gate", "audit-close",
}


def state_file(tmp_path: Path, phase: str) -> Path:
    path = tmp_path / "project-state.yml"
    gates = {
        f"G{index}": {"status": "pending", "date": None, "decision_ref": None}
        for index in range(1, 8)
    }
    path.write_text(yaml.safe_dump({
        "phase": phase, "supplier": "fixture", "deliverable_language": None,
        "gates": gates, "benchmarks_locked": True,
    }, sort_keys=False), encoding="utf-8")
    return path


def test_registry_is_complete_and_documented() -> None:
    commands = audit_command.load_registry()
    assert set(commands) == EXPECTED
    for spec in commands.values():
        assert spec["purpose"] and spec["stage"]
        assert spec["phases"] and spec["scripts"] and spec["outputs"]


def test_wrong_phase_refuses_before_stage_process(tmp_path: Path, capsys) -> None:
    state = state_file(tmp_path, "setup")
    with pytest.raises(StateError, match="refuses phase setup"):
        audit_command.dispatch("audit-chunk", ["DOC-0001"], state_path=state, dry_run=True)
    assert "invoke:" not in capsys.readouterr().out


def test_correct_phase_routes_exact_script_in_dry_run(tmp_path: Path, capsys) -> None:
    state = state_file(tmp_path, "registered")
    assert audit_command.dispatch(
        "audit-chunk", ["--", "DOC-0001"], state_path=state, dry_run=True
    ) == 0
    output = capsys.readouterr().out
    assert "chunk_document.py" in output
    assert "DOC-0001" in output


def test_status_reports_phase_gates_actions_and_last_validation(
    tmp_path: Path, capsys,
) -> None:
    state = state_file(tmp_path, "setup")
    database = tmp_path / "audit.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE auditor_actions(action_id TEXT, status TEXT)")
        connection.executemany("INSERT INTO auditor_actions VALUES (?, ?)", [
            ("ACT-0001", "open"), ("ACT-0002", "closed"), ("ACT-0003", "open"),
        ])
    runs = tmp_path / "validation_runs.csv"
    with runs.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "run_utc", "validator", "phase", "result", "exit_code", "details",
        ])
        writer.writeheader()
        writer.writerow({"run_utc": "2026-07-16T00:00:00Z", "validator": "fixture.py",
                         "phase": "setup", "result": "PASS", "exit_code": "0",
                         "details": "fixture"})
    assert audit_command.dispatch(
        "audit-status", [], state_path=state, database=database, runs=runs
    ) == 0
    output = capsys.readouterr().out
    assert "phase: setup" in output
    assert "G1: pending | none" in output
    assert "open_actions: 2" in output
    assert "last_validation: 2026-07-16T00:00:00Z | fixture.py | PASS | 0" in output


def test_gate_matches_current_phase_and_stops_at_packet_creation(
    tmp_path: Path, capsys,
) -> None:
    state = state_file(tmp_path, "report_ready")
    with pytest.raises(StateError, match="requires G6, not G5"):
        audit_command.dispatch(
            "audit-gate", ["create", "--gate", "G5"], state_path=state, dry_run=True
        )
    assert audit_command.dispatch(
        "audit-gate", ["create", "--gate", "G6"], state_path=state, dry_run=True
    ) == 0
    assert "gate_packet.py create --gate G6" in capsys.readouterr().out


def test_resieve_exposes_epic18_dependency_fail_closed(tmp_path: Path) -> None:
    state = state_file(tmp_path, "sieved")
    with pytest.raises(StateError, match="unavailable until EPIC18"):
        audit_command.dispatch("audit-resieve", [], state_path=state, dry_run=True)


def test_close_validates_before_handoff(tmp_path: Path, capsys) -> None:
    state = state_file(tmp_path, "findings_drafted")
    assert audit_command.dispatch(
        "audit-close", ["--source-agent", "codex", "--status", "partial"],
        state_path=state, dry_run=True,
    ) == 0
    output = capsys.readouterr().out
    assert output.index("run_all_validations.py") < output.index("make_handoff.py")
    assert "--no-record" in output


def test_cross_agent_validator_detects_and_accepts_canonical_adapters(tmp_path: Path) -> None:
    specs = audit_command.load_registry()
    agents = tmp_path / "AGENTS.md"
    rows = []
    claude = tmp_path / ".claude" / "commands"
    claude.mkdir(parents=True)
    for name, spec in specs.items():
        phases = ", ".join(spec["phases"])
        rows.append(f"`{name}` | `{phases}` | audit_command.py {name}")
        (claude / f"{name}.md").write_text(
            f"{phases}\npython scripts/audit_command.py {name} -- $ARGUMENTS\n",
            encoding="utf-8",
        )
    agents.write_text("\n".join(rows), encoding="utf-8")
    assert validate_agent_interfaces.validate(agents=agents, claude_commands=claude) == []
    (claude / "audit-chunk.md").write_text("bypass", encoding="utf-8")
    errors = validate_agent_interfaces.validate(agents=agents, claude_commands=claude)
    assert any("audit-chunk.md" in error for error in errors)
