#!/usr/bin/env python3
"""Validate EPIC10 finding/action links, enums, approvals, and wiki projections."""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

import db_util
from finding_workflow import (
    ACTIONS_DIR, APPROVALS, FINDINGS_DIR, ACTION_TEMPLATE, FINDING_TEMPLATE,
    action_page_values, approval_rows, finding_page_values, parse_frontmatter,
    render_template, vocabularies,
)

ENCONET = Path(__file__).resolve().parents[1]
RUNS = ENCONET / "manifests" / "validation_runs.csv"


def _compare_page(path: Path, expected: dict[str, object], expected_text: str,
                  errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"wiki page missing: {path.name}")
        return
    try:
        actual = parse_frontmatter(path)
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        return
    for key, value in expected.items():
        if str(actual.get(key)) != str(value):
            errors.append(f"page/DB mismatch {path.name}: {key}")
    if path.read_text(encoding="utf-8") != expected_text:
        errors.append(f"page/DB content mismatch: {path.name}")


def validate(db: Path, *, approvals: Path = APPROVALS,
             findings_dir: Path = FINDINGS_DIR, actions_dir: Path = ACTIONS_DIR) -> list[str]:
    errors: list[str] = []
    voc = vocabularies()
    decisions = {row.get("object_id"): row for row in approval_rows(approvals)
                 if row.get("decision", "").casefold() == "approved"}
    finding_ids, action_ids = set(), set()
    with db_util.connect(db) as conn:
        for raw in conn.execute("SELECT * FROM findings ORDER BY finding_id"):
            row = dict(raw); finding_id = row["finding_id"]; finding_ids.add(finding_id)
            if db_util.id_patterns()["finding_id"].fullmatch(finding_id) is None:
                errors.append(f"invalid finding ID: {finding_id}")
            if row["severity"] not in voc["finding_severities"]:
                errors.append(f"invalid finding severity: {finding_id}")
            if row["confidence"] not in voc["finding_confidences"]:
                errors.append(f"invalid finding confidence: {finding_id}")
            if row["verification_status"] not in voc["verification_statuses"]:
                errors.append(f"invalid verification status: {finding_id}")
            if bool(row["evidence_item_id"]) == bool(row["gap_id"]):
                errors.append(f"finding evidence/gap link invalid: {finding_id}")
            evaluation = conn.execute(
                "SELECT evaluation_id FROM criterion_evaluations WHERE evaluation_run_id=? AND criterion_id=?",
                (row["evaluation_run_id"], row["criterion_id"]),
            ).fetchone()
            if not evaluation:
                errors.append(f"finding run/criterion link invalid: {finding_id}")
            elif row["evidence_item_id"] and not conn.execute(
                "SELECT 1 FROM evaluation_evidence WHERE evaluation_id=? AND item_id=?",
                (evaluation["evaluation_id"], row["evidence_item_id"]),
            ).fetchone():
                errors.append(f"finding evidence is not linked to evaluation: {finding_id}")
            elif row["gap_id"] and not conn.execute(
                "SELECT 1 FROM gaps WHERE gap_id=? AND evaluation_id=?",
                (row["gap_id"], evaluation["evaluation_id"]),
            ).fetchone():
                errors.append(f"finding gap is not linked to evaluation: {finding_id}")
            if row["status"] == "approved" and (
                row["approval_ref"] != finding_id or finding_id not in decisions
            ):
                errors.append(f"finding approval mismatch: {finding_id}")
            if row["status"] == "draft" and row["approval_ref"] is not None:
                errors.append(f"draft finding has approval_ref: {finding_id}")
            expected = finding_page_values(row)
            _compare_page(findings_dir / f"{finding_id}.md", {
                "id": expected["id"], "type": "finding", "status": expected["status"],
                "content_origin": "mixed", "source": expected["source"],
                "evaluation_run": expected["evaluation_run"], "criterion_id": expected["criterion_id"],
                "severity": expected["severity"], "confidence": expected["confidence"],
                "evidence_refs": expected["evidence_refs"], "basis": expected["basis"],
                "verification_status": expected["verification_status"],
                "approval_ref": expected["approval_ref"],
            }, render_template(FINDING_TEMPLATE, expected), errors)
        for raw in conn.execute("SELECT * FROM auditor_actions ORDER BY action_id"):
            row = dict(raw); action_id = row["action_id"]; action_ids.add(action_id)
            if db_util.id_patterns()["action_id"].fullmatch(action_id) is None:
                errors.append(f"invalid action ID: {action_id}")
            if row["action_type"] not in voc["action_types"]:
                errors.append(f"invalid action type: {action_id}")
            if row["state"] not in voc["action_states"]:
                errors.append(f"invalid action state: {action_id}")
            if bool(row["finding_id"]) == bool(row["gap_id"]):
                errors.append(f"action finding/gap link invalid: {action_id}")
            if row["finding_id"] and not conn.execute(
                "SELECT 1 FROM findings WHERE finding_id=? AND evaluation_run_id=?",
                (row["finding_id"], row["evaluation_run_id"]),
            ).fetchone():
                errors.append(f"action finding/run link invalid: {action_id}")
            if row["gap_id"] and not conn.execute(
                "SELECT 1 FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) "
                "WHERE g.gap_id=? AND e.evaluation_run_id=?",
                (row["gap_id"], row["evaluation_run_id"]),
            ).fetchone():
                errors.append(f"action gap/run link invalid: {action_id}")
            if row["approval_status"] == "approved" and (
                row["approval_ref"] != action_id or action_id not in decisions
            ):
                errors.append(f"action approval mismatch: {action_id}")
            expected = action_page_values(row)
            _compare_page(actions_dir / f"{action_id}.md", {
                "id": expected["id"], "type": "action", "status": expected["approval_status"],
                "content_origin": "mixed", "source": expected["source"],
                "evaluation_run": expected["evaluation_run"], "action_type": expected["action_type"],
                "linked_to": expected["linked_to"], "state": expected["state"],
                "priority": expected["priority"], "approval_ref": expected["approval_ref"],
            }, render_template(ACTION_TEMPLATE, expected), errors)
        for violation in conn.execute("PRAGMA foreign_key_check"):
            errors.append(f"foreign key violation: {tuple(violation)}")
    for path in findings_dir.glob("FIND-*.md") if findings_dir.is_dir() else []:
        if path.stem not in finding_ids:
            errors.append(f"orphan finding page: {path.name}")
    for path in actions_dir.glob("ACT-*.md") if actions_dir.is_dir() else []:
        if path.stem not in action_ids:
            errors.append(f"orphan action page: {path.name}")
    return errors


def append(result: str, code: int, details: str, path: Path = RUNS,
           phase: str = "verification") -> None:
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_findings.py", phase, result, code, details,
        ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--findings-dir", type=Path, default=FINDINGS_DIR)
    parser.add_argument("--actions-dir", type=Path, default=ACTIONS_DIR)
    parser.add_argument("--no-record", action="store_true")
    parser.add_argument("--phase", default="verification")
    args = parser.parse_args()
    try:
        errors = validate(args.db, approvals=args.approvals,
                          findings_dir=args.findings_dir, actions_dir=args.actions_dir)
    except Exception as exc:  # noqa: BLE001 - report all validator failures
        errors = [str(exc)]
    if errors:
        if not args.no_record:
            append("FAIL", 1, f"{len(errors)} error(s); first: {errors[0][:120]}", phase=args.phase)
        for error in errors:
            print(f"validate_findings: FAIL - {error}", file=sys.stderr)
        return 1
    if not args.no_record:
        append("PASS", 0, "finding/action links, approvals, and pages verified", phase=args.phase)
    print("validate_findings: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
