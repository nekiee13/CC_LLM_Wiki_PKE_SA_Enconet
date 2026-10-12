#!/usr/bin/env python3
"""Run the local audit's phase-aware validation spine with one verdict."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import subprocess
import sys
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import yaml

import db_util
from project_paths import configure_standard_streams, local_path

PROJECT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT / "scripts"
STATE = PROJECT / "project-state.yml"
RUNS = PROJECT / "manifests" / "validation_runs.csv"
OUTPUTS = PROJECT / "outputs"
DATA = PROJECT / "sieving" / "DATA"
SIEVE_RUNS = PROJECT / "sieving" / "runs"
BENCHMARKS = PROJECT / "benchmarks" / "validate_benchmarks.py"
VOCABULARIES = PROJECT / "schemas" / "vocabularies.yml"
AUDIT_STATES = yaml.safe_load(VOCABULARIES.read_text(encoding="utf-8"))["vocabularies"]["audit_states"]["values"]
PHASES = [state for state in AUDIT_STATES if state != "failed"]

# Monotonic applicability matrix. Once activated, a validator remains active in every
# later phase. `failed` runs the closed-phase superset for diagnostic completeness.
MINIMUM_PHASE = {
    "raw_sources": "registered", "chunks": "chunked", "sieving_harness": "chunked", "traceability": "sieved",
    "app_b_json": "sieved", "requirements": "evidence_reviewed",
    "evaluation": "evaluated", "evidence_bundle": "evaluated", "findings": "findings_drafted",
    "structure": "setup", "frontmatter": "evidence_reviewed",
    "report": "report_ready", "report_links": "report_ready",
    "browser_evidence": "report_ready", "dashboard": "dashboard_ready",
    "review_package": "dashboard_ready", "evidence_budgets": "dashboard_ready",
}
ORDER = ["raw_sources", "chunks", "sieving_harness", "traceability", "app_b_json", "requirements",
         "evaluation", "evidence_bundle", "findings", "structure", "frontmatter", "report",
         "report_links", "browser_evidence", "dashboard", "review_package", "evidence_budgets"]
BENCHMARK_ORDER = ["benchmark_scoring", "benchmark_dashboard"]
RUN_HEADER = ["run_utc", "validator", "phase", "result", "exit_code", "details"]


def _safe_supplier(value: object) -> str:
    """Allow a readable filename stem, never a path or an inferred company."""
    if not isinstance(value, str) or value != value.strip() or not re.fullmatch(r"[\w -]{1,80}", value):
        raise ValueError("supplier must be a safe local filename stem")
    return value


def _safe_run_id(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", value):
        raise ValueError("run ID must be one safe path component")
    return value


@dataclass(frozen=True)
class Check:
    name: str
    state: str
    code: int | None
    detail: str
    command: tuple[str, ...] | None = None


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
        "benchmark_scoring": [sys.executable, str(local_path(BENCHMARKS)), "--scoring"],
        "benchmark_dashboard": [sys.executable, str(local_path(BENCHMARKS)), "--dashboard"],
    }


def discover_run_id(db: Path) -> str | None:
    db = local_path(db)
    # A validation read must not create an empty database as a side effect.
    with closing(sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)) as conn:
        row = conn.execute("SELECT run_id FROM evaluation_runs ORDER BY run_id DESC LIMIT 1").fetchone()
    return _safe_run_id(row[0]) if row else None


def discover_app_b_json(root: Path) -> Path | None:
    root = local_path(root)
    paths = sorted(path for path in root.rglob("*.json") if path.is_file()) if root.is_dir() else []
    for path in paths:
        path = local_path(path)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict) and "document" in payload and "items" in payload:
            return path
    return None


def discover_active_app_b_json(db: Path, runs_root: Path = SIEVE_RUNS) -> Path | None:
    """Prefer the exact JSON artifact for the active live generation."""
    db, runs_root = local_path(db), local_path(runs_root)
    with closing(sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)) as conn:
        table = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='sieve_runs'"
        ).fetchone()
        if table is None:
            return None
        row = conn.execute(
            "SELECT run_id FROM sieve_runs WHERE is_active=1 "
            "ORDER BY completed_at DESC, started_at DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return None
    path = local_path(runs_root / _safe_run_id(row[0]) / "generated.json")
    return path if path.is_file() else None


def commands(*, phase: str, supplier: str, db: Path, outputs: Path,
             run_id: str | None, app_b_json: Path | None,
             no_record: bool = False) -> dict[str, list[str] | None]:
    supplier, db, outputs = _safe_supplier(supplier), local_path(db), local_path(outputs)
    if run_id is not None:
        run_id = _safe_run_id(run_id)
    if app_b_json is not None:
        app_b_json = local_path(app_b_json)
    py = sys.executable
    package = outputs / f"{supplier}_appendix_b_evaluation_package.json"
    report = outputs / f"{supplier}_appendix_b_evaluation_report.md"
    dashboard_data = outputs / f"{supplier}_appendix_b_dashboard_data.json"
    dashboard = outputs / f"{supplier}_appendix_b_dashboard.html"
    evidence_root = outputs / "candidates" / "evidence_access"
    evidence_run = evidence_root / run_id if run_id else None
    bundle = evidence_run / "evidence_bundle.json" if evidence_run else None
    evidence_report = (
        evidence_run / f"{supplier}_appendix_b_evaluation_report.md" if evidence_run else None
    )
    evidence_viewer = (
        evidence_run / f"{supplier}_appendix_b_dashboard.html" if evidence_run else None
    )
    app_b = [py, str(SCRIPTS / "validate_app_b_json.py"), str(app_b_json)] if app_b_json else None
    if app_b is not None and phase_rank(phase) >= phase_rank("evaluated"):
        app_b.append("--strict")
    result = {
        "raw_sources": [py, str(SCRIPTS / "validate_raw_sources.py"), "--db", str(db)],
        "chunks": [py, str(SCRIPTS / "validate_chunks.py"), "--db", str(db)],
        "sieving_harness": [py, str(SCRIPTS / "validate_sieving_harness.py"), "--db", str(db)],
        "traceability": [py, str(SCRIPTS / "validate_traceability.py"), "--db", str(db),
                          "--active-only"],
        "app_b_json": app_b,
        "requirements": [py, str(SCRIPTS / "validate_requirements.py"), "--db", str(db)],
        "evaluation": ([py, str(SCRIPTS / "validate_evaluation.py"), "--db", str(db),
                        "--run-id", run_id] if run_id else None),
        "evidence_bundle": (
            [py, str(SCRIPTS / "validate_evidence_bundle.py"), str(bundle)] if bundle else None
        ),
        "findings": [py, str(SCRIPTS / "validate_findings.py"), "--db", str(db), "--phase", phase],
        "structure": [py, str(SCRIPTS / "validate_structure.py"), "--phase", phase],
        "frontmatter": [py, str(SCRIPTS / "validate_frontmatter.py"), "--phase", phase],
        "report": [py, str(SCRIPTS / "validate_report.py"), str(package), str(report),
                   "--db", str(db), "--phase", phase],
        "report_links": (
            [py, str(SCRIPTS / "validate_report_links.py"), str(evidence_report),
             str(evidence_viewer), str(package), "--project-root", str(PROJECT)]
            if evidence_report and evidence_viewer else None
        ),
        "browser_evidence": (
            [py, str(SCRIPTS / "browser_harness.py"), "check", str(evidence_viewer),
             "--artifacts", str(evidence_root / "validation_artifacts" / "browser_evidence"),
             "--require-interactive"] if evidence_viewer else None
        ),
        "dashboard": [py, str(SCRIPTS / "validate_dashboard.py"), str(package),
                      str(dashboard_data), str(dashboard), "--db", str(db), "--phase", phase],
        "review_package": [
            py, str(SCRIPTS / "validate_review_package.py"),
            str(evidence_root / "portable_package"),
        ],
        "evidence_budgets": [
            py, str(SCRIPTS / "validate_evidence_access_budgets.py"),
            str(evidence_root / "portable_package"),
            "--budgets", str(PROJECT / "schemas" / "evidence_access_budgets.yml"),
            "--browser-config", str(PROJECT / "schemas" / "browser_harness.yml"),
        ],
    }
    if no_record:
        for name in ("chunks", "traceability", "requirements", "evaluation", "findings",
                     "structure", "frontmatter", "report", "dashboard"):
            if result[name] is not None:
                result[name].append("--no-record")
    return result


def execute(command: list[str]) -> tuple[int, str]:
    try:
        if not command or command[0] != sys.executable or len(command) < 2:
            raise ValueError("validator command must use the approved Python interpreter")
        local_path(command[1])
        for value in command[2:]:
            candidate = value.partition("=")[2] if value.startswith("--") and "=" in value else value
            if Path(candidate).is_absolute():
                local_path(candidate)
        result = subprocess.run(command, cwd=PROJECT, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=900)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
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
        checks.append(Check(
            name, "PASS" if code == 0 else "FAIL", code, detail, tuple(command)
        ))
    return checks


def format_check(check: Check) -> str:
    """Render a lossless one-line aggregate record for operators and logs."""
    suffix = f" exit={check.code}" if check.code is not None else ""
    command = (
        f" command={json.dumps(list(check.command), ensure_ascii=False)}"
        if check.command is not None else " command=null"
    )
    return f"[{check.state}] {check.name}{suffix}{command} - {check.detail}"


def append(checks: list[Check], phase: str, code: int, *, path: Path = RUNS) -> None:
    path = local_path(path)
    failed = [check.name for check in checks if check.state == "FAIL"]
    skipped = [check.name for check in checks if check.state == "SKIPPED"]
    details = f"failed={','.join(failed) or 'none'}; phase-skipped={','.join(skipped) or 'none'}"
    # r+ refuses a missing manifest. Never make a headerless evidence log.
    with path.open("r+", newline="", encoding="utf-8") as handle:
        header = next(csv.reader(handle), None)
        if header:
            header[0] = header[0].lstrip("\ufeff")
        if header != RUN_HEADER:
            raise ValueError("validation manifest header is missing or invalid")
        handle.seek(0, 2)
        csv.writer(handle).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     "run_all_validations.py", phase,
                                     "PASS" if code == 0 else "FAIL", code, details])


def main() -> int:
    configure_standard_streams()
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
        args.state = local_path(args.state)
        args.db = local_path(args.db)
        args.outputs = local_path(args.outputs)
        args.data_root = local_path(args.data_root)
        if args.app_b_json is not None:
            args.app_b_json = local_path(args.app_b_json)
        state = yaml.safe_load(args.state.read_text(encoding="utf-8"))
        phase = state["phase"]
        phase_rank(phase)
        supplier = _safe_supplier(state["supplier"])
        run_id = args.run_id or (discover_run_id(args.db) if applicable("evaluation", phase) else None)
        app_b_json = args.app_b_json
        if app_b_json is None and applicable("app_b_json", phase):
            app_b_json = discover_active_app_b_json(args.db) or discover_app_b_json(args.data_root)
        check_commands = commands(phase=phase, supplier=supplier, db=args.db, outputs=args.outputs,
                                  run_id=run_id, app_b_json=app_b_json,
                                  no_record=args.no_record)
        checks = run(phase, check_commands)
        if benchmarks_required(phase, args.benchmarks):
            for name, command in benchmark_commands().items():
                code, detail = execute(command)
                checks.append(Check(
                    name, "PASS" if code == 0 else "FAIL", code, detail, tuple(command)
                ))
    except Exception as exc:  # noqa: BLE001 - aggregate boundary fails closed
        print(f"aggregate: FAIL - {exc}", file=sys.stderr)
        return 1
    for check in checks:
        print(format_check(check))
    failed = [check.name for check in checks if check.state == "FAIL"]
    code = int(bool(failed))
    if not args.no_record:
        try:
            append(checks, phase, code)
        except (OSError, ValueError) as exc:
            print(f"aggregate: FAIL - validation record could not be written: {exc}", file=sys.stderr)
            return 1
    print(f"aggregate: {'FAIL (' + ', '.join(failed) + ')' if failed else 'PASS'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
