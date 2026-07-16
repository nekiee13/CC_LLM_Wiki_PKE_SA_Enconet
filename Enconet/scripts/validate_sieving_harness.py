#!/usr/bin/env python3
"""Validate EPIC18 generation, prompt, golden-set, playbook, and skill invariants."""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

import yaml

import db_util
from validate_sieving_skill_drift import validate as validate_skill_drift


ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "sieving" / "prompts" / "active.yml"
CHANGELOG = ROOT / "sieving" / "prompts" / "CHANGELOG.md"
PLAYBOOK = ROOT / "sieving" / "SIEVING_PLAYBOOK.md"
GOLDEN = ROOT / "benchmarks" / "sieving_golden" / "manifest.yml"
APPROVALS = ROOT / "manifests" / "approvals.csv"
SKILLS = ROOT / ".agents" / "skills"
RUNS = ROOT / "sieving" / "runs"


def _approved(reference: str, approvals: Path) -> bool:
    with approvals.open(encoding="utf-8-sig", newline="") as handle:
        return any(row["object_id"] == reference and row["decision"].lower() == "approved"
                   for row in csv.DictReader(handle))


def validate(
    db: Path, *, active: Path = ACTIVE, changelog: Path = CHANGELOG,
    playbook: Path = PLAYBOOK, golden: Path = GOLDEN, approvals: Path = APPROVALS,
    skills: Path = SKILLS, runs: Path = RUNS, allow_pending_claude: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    with db_util.connect(db) as conn:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(sieve_runs)")}
        required = {"generation", "status", "is_active", "supersedes_run_id", "completed_at",
                    "decision_ref", "rejected_item_count", "failed_item_count"}
        if missing := required - columns:
            errors.append("sieve_runs generation schema missing: " + ", ".join(sorted(missing)))
        else:
            duplicates = conn.execute(
                "SELECT doc_id FROM sieve_runs WHERE is_active=1 GROUP BY doc_id HAVING count(*)<>1"
            ).fetchall()
            if duplicates:
                errors.append("document has multiple active sieve generations")
            no_active = conn.execute(
                "SELECT doc_id FROM sieve_runs GROUP BY doc_id HAVING sum(is_active)<>1"
            ).fetchall()
            if no_active:
                errors.append("document with sieve history lacks exactly one active generation")
            view = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='view' AND name='active_crumbs'"
            ).fetchone()
            if not view:
                errors.append("active_crumbs view is missing")
            elif conn.execute("SELECT count(*) FROM active_crumbs").fetchone()[0] != conn.execute(
                "SELECT count(*) FROM crumbs c JOIN sieve_runs r ON r.run_id=c.sieve_run_id WHERE r.is_active=1"
            ).fetchone()[0]:
                errors.append("active_crumbs leaks inactive generations")
            for row in conn.execute("SELECT run_id FROM sieve_runs WHERE completed_at IS NOT NULL"):
                for filename in ("metrics.json", "metrics.md"):
                    if not (runs / row["run_id"] / filename).is_file():
                        errors.append(f"completed run lacks {filename}: {row['run_id']}")
    active_data = yaml.safe_load(active.read_text(encoding="utf-8"))
    registry_text = changelog.read_text(encoding="utf-8")
    for side in ("RULE", "DOCUMENT"):
        version = active_data.get("active", {}).get(side)
        if not version:
            errors.append(f"active prompt is missing for {side}")
        elif version not in registry_text:
            errors.append(f"active prompt {version} has no CHANGELOG entry")
        elif not (ROOT / "sieving" / "prompts" / f"{version}.md").is_file():
            errors.append(f"active prompt file is missing: {version}.md")
    playbook_text = playbook.read_text(encoding="utf-8")
    for script in ("sieve_run.py", "import_crumbs.py", "link_crumbs.py", "resieve_run.py",
                   "sieve_metrics.py", "sieve_diff.py", "score_sieving.py", "sieve_generation.py"):
        if script not in playbook_text:
            errors.append(f"playbook does not document {script}")
    required_skills = {
        "sieving-run": ["SIEVING_PLAYBOOK.md", "failure"],
        "crumb-quality": ["V / VI / XVII", "IV / VII", "X / XI"],
        "sieving-tuning": ["promotion-ready", "deposit"],
    }
    for name, markers in required_skills.items():
        path = skills / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing Codex skill: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{name} skill lacks required marker: {marker}")
    errors.extend(validate_skill_drift(codex=skills, allow_pending_claude=allow_pending_claude))
    golden_data = yaml.safe_load(golden.read_text(encoding="utf-8"))
    if golden_data.get("status") == "approved":
        reference = golden_data.get("approval_ref")
        if not reference or not _approved(str(reference), approvals):
            errors.append("golden set claims approval without an approved manifest row")
    else:
        notes.append("golden calibration set remains pending human approval")
    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--runs", type=Path, default=RUNS)
    parser.add_argument("--allow-pending-claude", action="store_true")
    args = parser.parse_args()
    try:
        errors, notes = validate(args.db, runs=args.runs,
                                 allow_pending_claude=args.allow_pending_claude)
    except (OSError, sqlite3.Error, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"validate_sieving_harness: FAIL - {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    for note in notes:
        print(f"NOTE: {note}")
    if errors:
        print(f"validate_sieving_harness: FAIL - {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("validate_sieving_harness: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
