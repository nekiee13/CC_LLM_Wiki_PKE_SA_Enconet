"""EPIC10 gate, link, projection, approval, and validator tests."""
from __future__ import annotations

import sys
import sqlite3
from pathlib import Path

import pytest

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import approve  # noqa: E402
import build_matrix  # noqa: E402
import db_util  # noqa: E402
import finding_workflow  # noqa: E402
import init_db  # noqa: E402
import migrate_db  # noqa: E402
import validate_findings  # noqa: E402


@pytest.fixture
def draft_context(tmp_path: Path):
    db = tmp_path / "audit.sqlite"
    init_db.initialize(db)
    approvals = tmp_path / "approvals.csv"
    approvals.write_text(
        "object_id,decision,date,reviewer,notes\n"
        "G2-RUN-20260713-02,approved,2026-07-13,owner,scope\n"
        "G3-RUN-20260713-02,approved,2026-07-13,owner,calibration\n",
        encoding="utf-8",
    )
    findings_dir, actions_dir = tmp_path / "findings", tmp_path / "actions"
    with db_util.connect(db) as conn:
        db_util.insert(conn, "documents", {
            "doc_id": "DOC-0001", "filename": "evidence.json", "title": "Evidence",
            "supplier": "enconet", "language": "en", "document_side": "DOCUMENT",
            "sha256": "a" * 64,
        })
        db_util.insert(conn, "sieve_runs", {
            "run_id": "RUN-20260713-01", "doc_id": "DOC-0001", "prompt_version": "v1",
            "document_side": "DOCUMENT", "source_rule": None,
        })
        db_util.insert(conn, "crumbs", {
            "item_id": "CRUMB-DOC-0001-APP_B_I-0001", "doc_id": "DOC-0001",
            "sieve_run_id": "RUN-20260713-01", "criterion_id": "APP_B_I",
            "document_side": "DOCUMENT", "statement": "Supplier evidence",
        })
        db_util.insert(conn, "evaluation_runs", {
            "run_id": "RUN-20260713-02", "supplier": "enconet",
            "deliverable_language": "en", "scoring_model_version": "approved-1",
        })
        db_util.insert(conn, "criterion_evaluations", {
            "evaluation_id": "EVAL-APP_B_I", "evaluation_run_id": "RUN-20260713-02",
            "criterion_id": "APP_B_I", "rating": "partially", "score": 50,
            "coverage": .5, "completeness": .5, "accuracy": .5, "clarity": .5,
            "alignment": .5, "evidence_supported": 1, "affirmative_summary": "some",
            "contrary_summary": "gap", "judge_ruling": "partial", "rationale": "evidence",
        })
        db_util.insert(conn, "evaluation_evidence", {
            "evaluation_id": "EVAL-APP_B_I", "item_id": "CRUMB-DOC-0001-APP_B_I-0001",
        })
    return db, approvals, findings_dir, actions_dir


def test_draft_write_approval_and_projection_validation(draft_context):
    db, approvals, findings_dir, actions_dir = draft_context
    finding_id = finding_workflow.write_finding(db, {
        "evaluation_run_id": "RUN-20260713-02", "criterion_id": "APP_B_I",
        "evidence_item_id": "CRUMB-DOC-0001-APP_B_I-0001", "title": "Control gap",
        "body": "The sampled control is incomplete.", "severity": "high",
        "confidence": "medium", "basis": "Documented sample evidence",
    }, approvals=approvals, wiki_dir=findings_dir)
    action_id = finding_workflow.write_action(db, {
        "evaluation_run_id": "RUN-20260713-02", "finding_id": finding_id,
        "action_type": "sample_test", "description": "Expand the sample",
        "priority": True,
    }, approvals=approvals, wiki_dir=actions_dir)
    assert (findings_dir / f"{finding_id}.md").is_file()
    assert (actions_dir / f"{action_id}.md").is_file()
    assert validate_findings.validate(
        db, approvals=approvals, findings_dir=findings_dir, actions_dir=actions_dir
    ) == []
    matrix = build_matrix.build(db, "RUN-20260713-02")
    assert matrix[0]["finding_count"] == 1 and matrix[0]["action_count"] == 1
    with pytest.raises(ValueError, match="manifest row"):
        approve.approve_object(db, finding_id, approvals=approvals,
                               findings_dir=findings_dir, actions_dir=actions_dir)
    with approvals.open("a", encoding="utf-8") as handle:
        handle.write(f"{finding_id},approved,2026-07-13,owner,accepted\n")
        handle.write(f"{action_id},approved,2026-07-13,owner,accepted\n")
    approve.approve_object(db, finding_id, approvals=approvals,
                           findings_dir=findings_dir, actions_dir=actions_dir)
    approve.approve_object(db, action_id, approvals=approvals,
                           findings_dir=findings_dir, actions_dir=actions_dir)
    assert validate_findings.validate(
        db, approvals=approvals, findings_dir=findings_dir, actions_dir=actions_dir
    ) == []
    with db_util.connect(db) as conn:
        assert conn.execute("SELECT status FROM findings").fetchone()[0] == "approved"
        assert conn.execute("SELECT approval_status FROM auditor_actions").fetchone()[0] == "approved"


def test_input_gates_and_links_fail_closed(draft_context, tmp_path: Path):
    db, approvals, findings_dir, _ = draft_context
    missing = tmp_path / "missing-g3.csv"
    missing.write_text(
        "object_id,decision,date,reviewer,notes\n"
        "G2-RUN-20260713-02,approved,2026-07-13,owner,scope\n", encoding="utf-8"
    )
    record = {
        "evaluation_run_id": "RUN-20260713-02", "criterion_id": "APP_B_I",
        "evidence_item_id": "CRUMB-DOC-0001-APP_B_I-0001", "title": "x", "body": "x",
        "severity": "low", "confidence": "low", "basis": "x",
    }
    with pytest.raises(ValueError, match="G3"):
        finding_workflow.write_finding(db, record, approvals=missing, wiki_dir=findings_dir)
    with pytest.raises(ValueError, match="exactly one"):
        finding_workflow.write_finding(
            db, {**record, "gap_id": "GAP-APP_B_I-01"}, approvals=approvals,
            wiki_dir=findings_dir,
        )


def test_validator_names_page_tamper(draft_context):
    db, approvals, findings_dir, actions_dir = draft_context
    finding_id = finding_workflow.write_finding(db, {
        "evaluation_run_id": "RUN-20260713-02", "criterion_id": "APP_B_I",
        "evidence_item_id": "CRUMB-DOC-0001-APP_B_I-0001", "title": "x", "body": "x",
        "severity": "low", "confidence": "high", "basis": "quoted \"basis\"",
    }, approvals=approvals, wiki_dir=findings_dir)
    page = findings_dir / f"{finding_id}.md"
    page.write_text(page.read_text(encoding="utf-8").replace("severity: \"low\"", "severity: \"high\""), encoding="utf-8")
    assert f"page/DB mismatch {finding_id}.md: severity" in validate_findings.validate(
        db, approvals=approvals, findings_dir=findings_dir, actions_dir=actions_dir
    )


def test_approval_refuses_missing_draft_page(draft_context):
    db, approvals, findings_dir, actions_dir = draft_context
    finding_id = finding_workflow.write_finding(db, {
        "evaluation_run_id": "RUN-20260713-02", "criterion_id": "APP_B_I",
        "evidence_item_id": "CRUMB-DOC-0001-APP_B_I-0001", "title": "x", "body": "x",
        "severity": "low", "confidence": "high", "basis": "basis",
    }, approvals=approvals, wiki_dir=findings_dir)
    with approvals.open("a", encoding="utf-8") as handle:
        handle.write(f"{finding_id},approved,2026-07-13,owner,accepted\n")
    (findings_dir / f"{finding_id}.md").unlink()
    with pytest.raises(ValueError, match="wiki page missing"):
        approve.approve_object(db, finding_id, approvals=approvals,
                               findings_dir=findings_dir, actions_dir=actions_dir)


def test_legacy_empty_epic10_tables_migrate_with_backup(tmp_path: Path):
    db = tmp_path / "legacy.sqlite"
    init_db.initialize(db)
    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys=OFF")
        conn.execute("DROP TABLE auditor_actions")
        conn.execute("DROP TABLE findings")
        conn.execute("CREATE TABLE findings(finding_id TEXT PRIMARY KEY, criterion_id TEXT, title TEXT, body TEXT, status TEXT)")
        conn.execute("CREATE TABLE auditor_actions(action_id TEXT PRIMARY KEY, action_type TEXT, description TEXT, status TEXT)")
    actions, backup = migrate_db.migrate(db, apply=False, backup_dir=tmp_path / "backups")
    assert actions == ["recreate empty EPIC10 finding/action tables"] and backup is None
    actions, backup = migrate_db.migrate(db, apply=True, backup_dir=tmp_path / "backups")
    assert backup and backup.is_file()
    with sqlite3.connect(db) as conn:
        assert "evaluation_run_id" in {row[1] for row in conn.execute("PRAGMA table_info(findings)")}
        assert "approval_status" in {row[1] for row in conn.execute("PRAGMA table_info(auditor_actions)")}
