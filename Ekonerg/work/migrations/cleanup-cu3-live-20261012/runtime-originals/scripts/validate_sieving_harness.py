#!/usr/bin/env python3
"""Check local sieving run, prompt, playbook, skill, and golden-set readiness."""
from __future__ import annotations

import argparse
import csv
from contextlib import closing
from pathlib import Path
import re
import sqlite3
import sys

import yaml

import db_util
from source_revision_intake import pending_revision_documents
from source_revision_promote import retired_documents
from project_paths import local_path
from validate_sieving_skill_drift import validate as validate_skill_drift

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "sieving" / "prompts" / "active.yml"
CHANGELOG = ROOT / "sieving" / "prompts" / "CHANGELOG.md"
PLAYBOOK = ROOT / "sieving" / "SIEVING_PLAYBOOK.md"
GOLDEN = ROOT / "benchmarks" / "sieving_golden" / "manifest.yml"
APPROVALS = ROOT / "manifests" / "approvals.csv"
SKILLS = ROOT / ".agents" / "skills"
RUNS = ROOT / "sieving" / "runs"
STAGES = ("sieve_run.py", "import_crumbs.py", "link_crumbs.py", "resieve_run.py",
          "sieve_metrics.py", "sieve_diff.py", "score_sieving.py", "sieve_generation.py")
REQUIRED_COLUMNS = {"generation", "status", "is_active", "supersedes_run_id",
                    "completed_at", "decision_ref", "rejected_item_count", "failed_item_count"}


def _approved(reference: str, approvals: Path) -> bool:
    path = local_path(approvals)
    if not path.is_file():
        return False
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        if rows.fieldnames != ["object_id", "decision", "date", "reviewer", "notes"]:
            return False
        return any(row.get("object_id") == reference and row.get("decision") == "approved"
                   and row.get("date") and row.get("reviewer") for row in rows)


def validate(db: Path, *, active: Path = ACTIVE, changelog: Path = CHANGELOG,
             playbook: Path = PLAYBOOK, golden: Path = GOLDEN,
             approvals: Path = APPROVALS, skills: Path = SKILLS, runs: Path = RUNS,
             allow_pending_claude: bool = False) -> tuple[list[str], list[str]]:
    database = local_path(db)
    run_root = local_path(runs)
    if not database.is_file():
        return [f"local database is missing: {database}"], []
    errors: list[str] = []
    notes: list[str] = []
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        columns = {row[1] for row in conn.execute("PRAGMA table_info(sieve_runs)")}
        if missing := REQUIRED_COLUMNS - columns:
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
            pending_revisions = pending_revision_documents(conn)
            retired = retired_documents(conn)
            if any(row['doc_id'] not in pending_revisions | retired for row in no_active):
                errors.append("document with sieve history lacks exactly one active generation")
            if retired:
                notes.append('retained historical source identities: '+', '.join(sorted(retired)))
            if pending_revisions:
                notes.append('inactive source-revision candidates (predecessors remain active): '+', '.join(sorted(pending_revisions)))
            view = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='view' AND name='active_crumbs'"
            ).fetchone()
            if not view:
                errors.append("active_crumbs view is missing")
            elif conn.execute("SELECT count(*) FROM active_crumbs").fetchone()[0] != conn.execute(
                "SELECT count(*) FROM crumbs c JOIN sieve_runs r ON r.run_id=c.sieve_run_id "
                "WHERE r.is_active=1"
            ).fetchone()[0]:
                errors.append("active_crumbs leaks inactive generations")
            pattern = db_util.id_patterns()["run_id"]
            for row in conn.execute("SELECT run_id FROM sieve_runs WHERE completed_at IS NOT NULL"):
                run_id = row["run_id"]
                if pattern.fullmatch(run_id) is None:
                    errors.append(f"invalid completed run ID: {run_id}")
                    continue
                for filename in ("metrics.json", "metrics.md"):
                    if not local_path(run_root / run_id / filename).is_file():
                        errors.append(f"completed run lacks {filename}: {run_id}")

    active_data = yaml.safe_load(local_path(active).read_text(encoding="utf-8"))
    if not isinstance(active_data, dict) or not isinstance(active_data.get("active"), dict):
        raise ValueError("active prompt registry is missing or invalid")
    registry_text = local_path(changelog).read_text(encoding="utf-8")
    for side in ("RULE", "DOCUMENT"):
        version = active_data["active"].get(side)
        if not version:
            errors.append(f"active prompt is missing for {side}")
        elif not isinstance(version, str) or re.fullmatch(r"[a-z0-9_]+", version) is None:
            errors.append(f"invalid active prompt version for {side}")
        elif version not in registry_text:
            errors.append(f"active prompt {version} has no CHANGELOG entry")
        elif not local_path(ROOT / "sieving" / "prompts" / f"{version}.md").is_file():
            errors.append(f"active prompt file is missing: {version}.md")

    playbook_text = local_path(playbook).read_text(encoding="utf-8")
    for script in STAGES:
        if script not in playbook_text:
            errors.append(f"playbook does not document {script}")
        if not local_path(ROOT / "scripts" / script).is_file():
            errors.append(f"local sieving stage is missing: {script}")
    required_skills = {
        "sieving-run": ["SIEVING_PLAYBOOK.md", "failure"],
        "crumb-quality": ["V / VI / XVII", "IV / VII", "X / XI"],
        "sieving-tuning": ["promotion-ready", "deposit"],
    }
    codex_root = local_path(skills)
    for name, markers in required_skills.items():
        path = local_path(codex_root / name / "SKILL.md")
        if not path.is_file():
            errors.append(f"missing Codex skill: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{name} skill lacks required marker: {marker}")
    errors.extend(validate_skill_drift(codex=codex_root,
                                       allow_pending_claude=allow_pending_claude))

    golden_data = yaml.safe_load(local_path(golden).read_text(encoding="utf-8"))
    if not isinstance(golden_data, dict):
        raise ValueError("golden-set manifest is missing or invalid")
    status = golden_data.get("status")
    if status == "approved":
        reference = golden_data.get("approval_ref")
        if (not isinstance(reference, str) or not reference
                or not golden_data.get("document") or not golden_data.get("expected_crumbs")
                or not _approved(reference, approvals)):
            errors.append("golden set claims approval without a complete local approved record")
    elif status == "pending_human_approval":
        if golden_data.get("approval_ref"):
            errors.append("pending golden set cannot cite approval")
        notes.append("golden calibration set remains pending human approval")
    else:
        errors.append("golden-set status is invalid")
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
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, yaml.YAMLError) as exc:
        errors, notes = [str(exc)], []
    for note in notes:
        print(f"NOTE: {note}")
    for error in errors:
        print(f"validate_sieving_harness: FAIL - {error}", file=sys.stderr)
    if errors:
        return 1
    print("validate_sieving_harness: PASS - readiness checks only; no source approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
