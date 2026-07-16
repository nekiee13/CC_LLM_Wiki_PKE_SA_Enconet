#!/usr/bin/env python3
"""Canonical phase-checked EPIC17 command dispatcher for both agents."""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import yaml

from audit_state import DEFAULT_STATE, StateError, load_state
import db_util


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
REGISTRY = ROOT / "schemas" / "audit_commands.yml"
RUNS = ROOT / "manifests" / "validation_runs.csv"
GATE_BY_PHASE = {
    "setup": "G1", "sieved": "G2", "evidence_reviewed": "G3",
    "findings_drafted": "G4", "findings_approved": "G5",
    "report_ready": "G6", "dashboard_ready": "G7",
}
SCRIPT_BY_COMMAND = {
    "audit-register": "promote_source.py",
    "audit-chunk": "chunk_document.py",
    "audit-sieve": "sieve_run.py",
    "audit-resieve": "resieve_run.py",
    "audit-link": "link_crumbs.py",
    "audit-eval": "write_evaluation.py",
    "audit-report": "generate_report.py",
    "audit-dashboard": "generate_dashboard.py",
    "audit-validate": "run_all_validations.py",
    "audit-gate": "gate_packet.py",
}


def load_registry(path: Path = REGISTRY) -> dict[str, dict[str, object]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    commands = data.get("commands") if isinstance(data, dict) else None
    if not isinstance(commands, dict) or not commands:
        raise StateError("audit command registry has no commands")
    required = {"purpose", "stage", "phases", "scripts", "outputs"}
    for name, spec in commands.items():
        if not isinstance(spec, dict) or required - set(spec):
            raise StateError(f"incomplete command contract: {name}")
    return commands


def _arguments(values: list[str]) -> list[str]:
    return values[1:] if values and values[0] == "--" else values


def _run(command: list[str], *, cwd: Path, dry_run: bool) -> int:
    rendered = subprocess.list2cmdline(command)
    print(f"invoke: {rendered}")
    if dry_run:
        return 0
    return subprocess.run(command, cwd=cwd, check=False).returncode


def _open_actions(database: Path) -> int:
    if not database.exists():
        return 0
    with sqlite3.connect(database) as connection:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='auditor_actions'"
        ).fetchone()
        if not exists:
            return 0
        columns = {row[1] for row in connection.execute("PRAGMA table_info(auditor_actions)")}
        if "status" not in columns:
            return 0
        return int(connection.execute(
            "SELECT count(*) FROM auditor_actions WHERE status='open'"
        ).fetchone()[0])


def _last_validation(path: Path) -> str:
    if not path.exists():
        return "none"
    # utf-8-sig accepts the historical manifest's optional BOM while remaining
    # compatible with newly created plain UTF-8 manifests.
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return "none"
    row = rows[-1]
    return " | ".join(
        str(row.get(key, "")) for key in ("run_utc", "validator", "result", "exit_code")
    )


def show_status(state_path: Path, database: Path, runs: Path) -> int:
    state = load_state(state_path)
    print(f"phase: {state['phase']}")
    for gate, record in state["gates"].items():
        print(f"{gate}: {record['status']} | {record.get('decision_ref') or 'none'}")
    print(f"open_actions: {_open_actions(database)}")
    print(f"last_validation: {_last_validation(runs)}")
    return 0


def _require_phase(command: str, phase: str, spec: dict[str, object]) -> None:
    phases = [str(item) for item in spec["phases"]]
    if phase not in phases:
        raise StateError(
            f"{command} refuses phase {phase}; allowed phases: {', '.join(phases)}"
        )


def _gate_args(arguments: list[str], phase: str) -> None:
    if not arguments or arguments[0] != "create":
        raise StateError("audit-gate only assembles packets: first argument must be create")
    expected = GATE_BY_PHASE.get(phase)
    if expected is None:
        raise StateError(f"no human gate can be assembled from phase {phase}")
    try:
        supplied = arguments[arguments.index("--gate") + 1]
    except (ValueError, IndexError) as exc:
        raise StateError(f"audit-gate requires --gate {expected} at phase {phase}") from exc
    if supplied != expected:
        raise StateError(f"phase {phase} requires {expected}, not {supplied}")


def dispatch(
    command: str, arguments: list[str], *, state_path: Path = DEFAULT_STATE,
    database: Path = db_util.DEFAULT_DB, runs: Path = RUNS, registry_path: Path = REGISTRY,
    dry_run: bool = False,
) -> int:
    registry = load_registry(registry_path)
    if command not in registry:
        raise StateError(f"unknown audit command: {command}")
    if command == "audit-status":
        return show_status(state_path, database, runs)
    state = load_state(state_path)
    phase = str(state["phase"])
    spec = registry[command]
    _require_phase(command, phase, spec)
    arguments = _arguments(arguments)
    if command == "audit-gate":
        _gate_args(arguments, phase)
    if command == "audit-close":
        validate = [sys.executable, str(ROOT / "scripts" / "run_all_validations.py"), "--no-record"]
        result = _run(validate, cwd=ROOT, dry_run=dry_run)
        if result:
            print("STOP: validation failed; handoff was not published", file=sys.stderr)
            return result
        handoff = [sys.executable, str(WORKSPACE / "scripts" / "make_handoff.py"), *arguments]
        return _run(handoff, cwd=WORKSPACE, dry_run=dry_run)
    script = ROOT / "scripts" / SCRIPT_BY_COMMAND[command]
    if not script.exists():
        dependency = spec.get("requires_epic", "its implementation dependency")
        raise StateError(f"{command} is reserved but unavailable until {dependency}: missing {script.name}")
    return _run([sys.executable, str(script), *arguments], cwd=ROOT, dry_run=dry_run)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--runs", type=Path, default=RUNS)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--describe", action="store_true")
    parser.add_argument("command", nargs="?")
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        registry = load_registry(args.registry)
        if args.describe:
            if args.command:
                print(json.dumps({args.command: registry[args.command]}, indent=2))
            else:
                print(json.dumps(registry, indent=2))
            return 0
        if not args.command:
            parser.error("command is required unless --describe is used")
        return dispatch(args.command, args.arguments, state_path=args.state, database=args.db,
                        runs=args.runs, registry_path=args.registry, dry_run=args.dry_run)
    except (OSError, sqlite3.Error, StateError, KeyError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
