import hashlib
import sys
import sqlite3
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import evaluation_engine


def test_applicability_accepts_registered_document_scope_source(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    raw.mkdir()
    source = raw / "qms.md"
    source.write_text("# Controlled QMS procedure\n", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE documents (doc_id TEXT, filename TEXT, sha256 TEXT, document_side TEXT)"
    )
    conn.execute(
        "INSERT INTO documents VALUES (?,?,?,?)",
        ("DOC-0012", source.name, digest, "DOCUMENT"),
    )
    monkeypatch.setattr(evaluation_engine, "RAW", raw)
    monkeypatch.setattr(evaluation_engine, "local_path", lambda path: Path(path))

    evaluation_engine._raw_document(conn, "DOC-0012")


def test_applicability_rejects_rule_scope_without_governing_source(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    raw.mkdir()
    source = raw / "appendix-b.md"
    source.write_text("# Appendix B\n", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE documents (doc_id TEXT, filename TEXT, sha256 TEXT, document_side TEXT)"
    )
    conn.execute(
        "CREATE TABLE approved_sources (source_sha256 TEXT, authority_role TEXT)"
    )
    conn.execute(
        "INSERT INTO documents VALUES (?,?,?,?)",
        ("RULE-001", source.name, digest, "RULE"),
    )
    monkeypatch.setattr(evaluation_engine, "RAW", raw)
    monkeypatch.setattr(evaluation_engine, "local_path", lambda path: Path(path))

    with pytest.raises(ValueError, match="approved governing-source"):
        evaluation_engine._raw_document(conn, "RULE-001")


def test_legacy_applicability_rows_are_migrated_to_explicit_conditional_state():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE criterion_applicability ("
        "evaluation_run_id TEXT, criterion_id TEXT, applicable INTEGER, "
        "justification TEXT NOT NULL)"
    )
    conn.execute(
        "INSERT INTO criterion_applicability VALUES (?,?,?,?)",
        ("RUN-1", "APP_B_VIII", 1, "Owner-approved G2: conditional and kept in scope."),
    )
    evaluation_engine._ensure_applicability_guard_schema(conn)
    row = conn.execute(
        "SELECT applicability_state, conditional_confirmation_ref "
        "FROM criterion_applicability"
    ).fetchone()
    assert row == ("conditional", None)


def test_conditional_evaluation_requires_confirmation():
    ruling = {
        "applicability_state": "conditional",
        "conditional_confirmation_ref": None,
    }
    with pytest.raises(ValueError, match="requires confirmation"):
        evaluation_engine._check_conditional_evaluation(ruling, "fully")
    evaluation_engine._check_conditional_evaluation(ruling, "undetermined")
    confirmed = {
        "applicability_state": "applicable",
        "conditional_confirmation_ref": "G2-CONFIRM-001",
    }
    evaluation_engine._check_conditional_evaluation(confirmed, "fully")


def test_confirm_applicability_records_owner_approval(tmp_path, monkeypatch):
    db = tmp_path / "audit.sqlite"
    conn = sqlite3.connect(db)
    conn.execute(
        "CREATE TABLE criterion_applicability ("
        "evaluation_run_id TEXT, criterion_id TEXT, applicable INTEGER, "
        "justification TEXT NOT NULL, applicability_state TEXT NOT NULL, "
        "conditional_confirmation_ref TEXT, approved_by TEXT, approved_date TEXT)"
    )
    conn.execute(
        "INSERT INTO criterion_applicability VALUES (?,?,?,?,?,?,?,?)",
        ("RUN-20261003-32", "APP_B_VIII", 1, "conditional", "conditional", None, "Owner", "2026-10-03"),
    )
    conn.execute(
        "CREATE TABLE criterion_evaluations (evaluation_run_id TEXT, criterion_id TEXT)"
    )
    conn.commit()
    conn.close()
    monkeypatch.setattr(evaluation_engine, "_approval", lambda ref: {
        "reviewer": "Owner", "date": "2026-10-04"
    })
    def connect(_path, *, write):
        local = sqlite3.connect(db)
        local.row_factory = sqlite3.Row
        return local
    monkeypatch.setattr(evaluation_engine, "_connect", connect)
    result = evaluation_engine.confirm_applicability(
        db, run_id="RUN-20261003-32", criterion_id="APP_B_VIII",
        confirmation_ref="G2-CONFIRM-001", apply=True,
    )
    assert result["mode"] == "apply"
    conn = sqlite3.connect(db)
    assert conn.execute(
        "SELECT applicability_state, conditional_confirmation_ref "
        "FROM criterion_applicability"
    ).fetchone() == ("applicable", "G2-CONFIRM-001")
