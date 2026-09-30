#!/usr/bin/env python3
"""Canonical phase-checked EPIC17 command dispatcher for both agents."""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

import yaml

from audit_state import DEFAULT_STATE, StateError, load_state
import db_util
from project_paths import LocalPathError, configure_standard_streams, local_path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "schemas" / "audit_commands.yml"
RUNS = ROOT / "manifests" / "validation_runs.csv"
GATE_BY_PHASE = {
    "setup": "G1", "sieved": "G2", "evidence_reviewed": "G3",
    "findings_drafted": "G4", "findings_approved": "G5",
    "report_ready": "G6", "dashboard_ready": "G7",
}
# Path-valued options in the pinned stage CLIs. Positional inputs and paths
# derived from IDs must also be guarded by each stage during its adaptation.
PATH_OPTIONS = {
    "--db", "--state", "--runs", "--registry", "--approvals", "--log",
    "--exceptions", "--vocabularies", "--json-file", "--output-root",
    "--candidates", "--metrics-root", "--output", "--viewer-output",
    "--wiki-output", "--evidence-bundle", "--outputs", "--data-root",
    "--app-b-json", "--template", "--project-root", "--validate",
}


def _local_arguments(arguments: list[str]) -> list[str]:
    """Normalize explicit path options; require full names, not abbreviations."""
    values = list(arguments)
    index = 0
    while index < len(values):
        option, separator, inline = values[index].partition("=")
        if (option.startswith("--") and len(option) > 2 and option not in PATH_OPTIONS
                and any(full.startswith(option) for full in PATH_OPTIONS)):
            raise StateError(f"use the full path option name, not {option}")
        if option in PATH_OPTIONS:
            if separator:
                target = inline
            elif index + 1 < len(values) and not values[index + 1].startswith("--"):
                target = values[index + 1]
            else:
                raise StateError(f"{option} requires a local path")
            if not target:
                raise StateError(f"{option} requires a local path")
            resolved = local_path(target)
            if separator:
                values[index] = option + "=" + str(resolved)
            else:
                values[index + 1] = str(resolved)
                index += 1
        index += 1
    return values


def load_registry(path: Path = REGISTRY) -> dict[str, dict[str, object]]:
    path = local_path(path)
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
    values = values[1:] if values and values[0] == "--" else values
    misplaced = next((value for value in values if value in {"--dry-run", "--describe"}), None)
    if misplaced:
        raise StateError(
            f"dispatcher option {misplaced} must precede the audit command; "
            f"example: audit_command.py {misplaced} audit-status"
        )
    return values


def _stage_script(spec: dict[str, object]) -> Path:
    """Derive the executable from the canonical registry, with no parallel script map."""
    scripts = spec["scripts"]
    if not isinstance(scripts, list) or not scripts:
        raise StateError("command contract has no stage script")
    relative = Path(str(scripts[-1]))
    if relative.parent != Path("scripts") or relative.suffix != ".py":
        raise StateError(f"unsafe stage script contract: {relative}")
    return local_path(ROOT / relative)


def _run(command: list[str], *, cwd: Path, dry_run: bool) -> int:
    rendered = subprocess.list2cmdline(command)
    print(f"invoke: {rendered}")
    if dry_run:
        return 0
    return subprocess.run(command, cwd=local_path(cwd), check=False).returncode


def _open_actions(database: Path) -> int:
    database = local_path(database)
    if not database.exists():
        return 0
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as connection:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='auditor_actions'"
        ).fetchone()
        if not exists:
            return 0
        columns = {row[1] for row in connection.execute("PRAGMA table_info(auditor_actions)")}
        action_state = "state" if "state" in columns else "status" if "status" in columns else None
        if action_state is None:
            return 0
        return int(connection.execute(
            f"SELECT count(*) FROM auditor_actions WHERE {action_state}='open'"
        ).fetchone()[0])


def _last_validation(path: Path) -> str:
    path = local_path(path)
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
    state_path, database, runs, registry_path = map(
        local_path, (state_path, database, runs, registry_path))
    registry = load_registry(registry_path)
    if command not in registry:
        raise StateError(f"unknown audit command: {command}")
    if command == "audit-status":
        return show_status(state_path, database, runs)
    state = load_state(state_path)
    phase = str(state["phase"])
    spec = registry[command]
    _require_phase(command, phase, spec)
    arguments = _local_arguments(_arguments(arguments))
    if command == "audit-gate":
        _gate_args(arguments, phase)
    if command == "audit-close":
        expected = ["scripts/run_all_validations.py", "scripts/make_handoff.py"]
        if spec["scripts"] != expected:
            raise StateError("unsafe local audit-close script contract")
        scripts = [local_path(ROOT / name) for name in expected]
        for script in scripts:
            if not script.is_file():
                raise StateError(f"audit-close unavailable: missing {script.name}")
        # Reject foreign handoff roots before even starting validation.
        for index, value in enumerate(arguments):
            option, separator, inline = value.partition("=")
            if option in {"--project-root", "--validate"}:
                if separator:
                    target = inline
                elif index + 1 < len(arguments):
                    target = arguments[index + 1]
                else:
                    raise StateError(f"{option} requires a local path")
                target_path = local_path(target)
                if option == "--project-root" and target_path != ROOT:
                    raise StateError("handoff project root must be the local project root")
        validate = [sys.executable, str(scripts[0]), "--no-record"]
        result = _run(validate, cwd=ROOT, dry_run=dry_run)
        if result:
            print("STOP: validation failed; handoff was not published", file=sys.stderr)
            return result
        handoff = [sys.executable, str(scripts[1]), *arguments]
        return _run(handoff, cwd=ROOT, dry_run=dry_run)
    script = _stage_script(spec)
    if not script.exists():
        dependency = spec.get("requires_epic", "its implementation dependency")
        raise StateError(f"{command} is reserved but unavailable until {dependency}: missing {script.name}")
    return _run([sys.executable, str(script), *arguments], cwd=ROOT, dry_run=dry_run)


def main(argv: list[str] | None = None) -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
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
        args.state, args.db, args.runs, args.registry = map(
            local_path, (args.state, args.db, args.runs, args.registry))
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
    except (OSError, sqlite3.Error, StateError, LocalPathError, KeyError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
