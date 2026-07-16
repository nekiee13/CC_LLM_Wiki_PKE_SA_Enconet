#!/usr/bin/env python3
"""Run the EPIC13 phase-aware Enconet validation spine with one verdict."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import yaml

import db_util

ENCONET = Path(__file__).resolve().parents[1]
SCRIPTS = ENCONET / "scripts"
STATE = ENCONET / "project-state.yml"
RUNS = ENCONET / "manifests" / "validation_runs.csv"
OUTPUTS = ENCONET / "outputs"
DATA = ENCONET / "sieving" / "DATA"
BENCHMARKS = ENCONET / "benchmarks" / "validate_benchmarks.py"
VOCABULARIES = ENCONET / "schemas" / "vocabularies.yml"
AUDIT_STATES = yaml.safe_load(VOCABULARIES.read_text(encoding="utf-8"))["vocabularies"]["audit_states"]["values"]
PHASES = [state for state in AUDIT_STATES if state != "failed"]

# Monotonic applicability matrix. Once activated, a validator remains active in every
# later phase. `failed` runs the closed-phase superset for diagnostic completeness.
MINIMUM_PHASE = {
    "raw_sources": "registered", "chunks": "chunked", "traceability": "sieved",
    "app_b_json": "sieved", "requirements": "evidence_reviewed",
    "evaluation": "evaluated", "findings": "findings_drafted",
    "structure": "setup", "frontmatter": "evidence_reviewed",
    "report": "report_ready", "dashboard": "dashboard_ready",
}
ORDER = ["raw_sources", "chunks", "traceability", "app_b_json", "requirements",
         "evaluation", "findings", "structure", "frontmatter", "report", "dashboard"]
BENCHMARK_ORDER = ["benchmark_scoring", "benchmark_dashboard"]


@dataclass(frozen=True)
class Check:
    name: str
    state: str
    code: int | None
    detail: str


def phase_rank(phase: str) -> int:
    if phase == "failed":
        return len(PHASES) - 1
    if phase not in PHASES:
        raise ValueError(f"unknown project phase: {phase}")
    return PHASES.index(phase)


def applicable(name: str, phase: str) -> bool:
    return phase_rank(phase) >= phase_rank(MINIMUM_PHASE[name])


def benchmarks_required(phase: str, requested: bool = False) -> bool:
    """Benchmarks are explicit early, and mandatory before the G5 transition onward."""
    return requested or phase_rank(phase) >= phase_rank("findings_approved")


def benchmark_commands() -> dict[str, list[str]]:
    return {
        "benchmark_scoring": [sys.executable, str(BENCHMARKS), "--scoring"],
        "benchmark_dashboard": [sys.executable, str(BENCHMARKS), "--dashboard"],
    }


def discover_run_id(db: Path) -> str | None:
    with db_util.connect(db) as conn:
        row = conn.execute("SELECT run_id FROM evaluation_runs ORDER BY run_id DESC LIMIT 1").fetchone()
    return row[0] if row else None


def discover_app_b_json(root: Path) -> Path | None:
    paths = sorted(path for path in root.rglob("*.json") if path.is_file()) if root.is_dir() else []
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict) and "document" in payload and "items" in payload:
            return path
    return None


def commands(*, phase: str, supplier: str, db: Path, outputs: Path,
             run_id: str | None, app_b_json: Path | None,
             no_record: bool = False) -> dict[str, list[str] | None]:
    py = sys.executable
    package = outputs / f"{supplier}_appendix_b_evaluation_package.json"
    report = outputs / f"{supplier}_appendix_b_evaluation_report.md"
    dashboard_data = outputs / f"{supplier}_appendix_b_dashboard_data.json"
    dashboard = outputs / f"{supplier}_appendix_b_dashboard.html"
    app_b = [py, str(SCRIPTS / "validate_app_b_json.py"), str(app_b_json)] if app_b_json else None
    if app_b is not None and phase_rank(phase) >= phase_rank("evaluated"):
        app_b.append("--strict")
    result = {
        "raw_sources": [py, str(SCRIPTS / "validate_raw_sources.py"), "--db", str(db)],
        "chunks": [py, str(SCRIPTS / "validate_chunks.py"), "--db", str(db)],
        "traceability": [py, str(SCRIPTS / "validate_traceability.py"), "--db", str(db)],
        "app_b_json": app_b,
        "requirements": [py, str(SCRIPTS / "validate_requirements.py"), "--db", str(db)],
        "evaluation": ([py, str(SCRIPTS / "validate_evaluation.py"), "--db", str(db),
                        "--run-id", run_id] if run_id else None),
        "findings": [py, str(SCRIPTS / "validate_findings.py"), "--db", str(db), "--phase", phase],
        "structure": [py, str(SCRIPTS / "validate_structure.py"), "--phase", phase],
        "frontmatter": [py, str(SCRIPTS / "validate_frontmatter.py"), "--phase", phase],
        "report": [py, str(SCRIPTS / "validate_report.py"), str(package), str(report),
                   "--db", str(db), "--phase", phase],
        "dashboard": [py, str(SCRIPTS / "validate_dashboard.py"), str(package),
                      str(dashboard_data), str(dashboard), "--db", str(db), "--phase", phase],
    }
    if no_record:
        for name in ("chunks", "traceability", "requirements", "evaluation", "findings",
                     "structure", "frontmatter", "report", "dashboard"):
            if result[name] is not None:
                result[name].append("--no-record")
    return result


def execute(command: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(command, cwd=ENCONET, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=900)
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, f"could not execute: {exc}"
    lines = (result.stdout + result.stderr).strip().splitlines()
    return result.returncode, lines[-1] if lines else "no output"


def run(phase: str, command_map: dict[str, list[str] | None],
        executor: Callable[[list[str]], tuple[int, str]] = execute) -> list[Check]:
    checks: list[Check] = []
    for name in ORDER:
        if not applicable(name, phase):
            checks.append(Check(name, "SKIPPED", None, f"SKIPPED(phase={phase})"))
            continue
        command = command_map[name]
        if command is None:
            checks.append(Check(name, "FAIL", 1, "required input could not be discovered"))
            continue
        code, detail = executor(command)
        checks.append(Check(name, "PASS" if code == 0 else "FAIL", code, detail))
    return checks


def append(checks: list[Check], phase: str, code: int, *, path: Path = RUNS) -> None:
    failed = [check.name for check in checks if check.state == "FAIL"]
    skipped = [check.name for check in checks if check.state == "SKIPPED"]
    details = f"failed={','.join(failed) or 'none'}; phase-skipped={','.join(skipped) or 'none'}"
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     "run_all_validations.py", phase,
                                     "PASS" if code == 0 else "FAIL", code, details])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=STATE)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--outputs", type=Path, default=OUTPUTS)
    parser.add_argument("--data-root", type=Path, default=DATA)
    parser.add_argument("--run-id")
    parser.add_argument("--app-b-json", type=Path)
    parser.add_argument("--benchmarks", action="store_true",
                        help="run both supplier-independent EPIC16 benchmark classes")
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        state = yaml.safe_load(args.state.read_text(encoding="utf-8"))
        phase = state["phase"]
        phase_rank(phase)
        supplier = state["supplier"]
        run_id = args.run_id or (discover_run_id(args.db) if applicable("evaluation", phase) else None)
        app_b_json = args.app_b_json or (discover_app_b_json(args.data_root) if applicable("app_b_json", phase) else None)
        check_commands = commands(phase=phase, supplier=supplier, db=args.db, outputs=args.outputs,
                                  run_id=run_id, app_b_json=app_b_json,
                                  no_record=args.no_record)
        checks = run(phase, check_commands)
        if benchmarks_required(phase, args.benchmarks):
            for name, command in benchmark_commands().items():
                code, detail = execute(command)
                checks.append(Check(name, "PASS" if code == 0 else "FAIL", code, detail))
    except Exception as exc:  # noqa: BLE001 - aggregate boundary fails closed
        print(f"aggregate: FAIL - {exc}", file=sys.stderr)
        return 1
    for check in checks:
        suffix = f" exit={check.code}" if check.code is not None else ""
        print(f"[{check.state}] {check.name}{suffix} - {check.detail}")
    failed = [check.name for check in checks if check.state == "FAIL"]
    code = int(bool(failed))
    print(f"aggregate: {'FAIL (' + ', '.join(failed) + ')' if failed else 'PASS'}")
    if not args.no_record:
        append(checks, phase, code)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
