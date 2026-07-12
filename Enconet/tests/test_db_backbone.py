"""EPIC2 SQLite backbone acceptance and negative-path tests."""
from __future__ import annotations

import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

import pytest

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import db_util  # noqa: E402
import init_db  # noqa: E402


REQUIRED_TABLES = {
    "documents", "document_chunks", "crumbs", "crumb_sources", "crumb_quotes",
    "crumb_chunk_links", "requirements", "criterion_applicability",
    "criterion_evaluations", "gaps", "findings", "auditor_actions", "sieve_runs",
    "evaluation_runs", "dashboard_runs", "validation_runs",
    "sieve_run_authorities", "crumb_authority_refs",
}


@pytest.fixture
def database(tmp_path: Path) -> Path:
    path = tmp_path / "nqa_audit.sqlite"
    assert init_db.initialize(path) == "initialized"
    return path


def _document() -> dict[str, object]:
    return {
        "doc_id": "DOC-0001", "filename": "supplier.pdf", "title": "Supplier QA",
        "supplier": "enconet", "language": "en", "document_side": "DOCUMENT",
        "sha256": "a" * 64,
    }


def test_initializer_creates_required_schema_and_seeds_taxonomy(database: Path):
    with closing(db_util.connect(database)) as conn:
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        assert REQUIRED_TABLES <= tables
        assert "criteria" in tables  # required target of criterion foreign keys
        assert conn.execute("SELECT count(*) FROM criteria").fetchone()[0] == 18
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert isinstance(conn.execute("SELECT * FROM criteria LIMIT 1").fetchone(), sqlite3.Row)


def test_schema_declares_required_foreign_key_spine(database: Path):
    expected = {
        "document_chunks": {("doc_id", "documents")},
        "crumbs": {("doc_id", "documents"), ("sieve_run_id", "sieve_runs")},
        "crumb_sources": {("item_id", "crumbs")},
        "crumb_quotes": {("item_id", "crumbs")},
        "sieve_run_authorities": {("run_id", "sieve_runs")},
        "crumb_authority_refs": {("item_id", "crumbs")},
        "crumb_chunk_links": {("item_id", "crumbs"), ("quote_id", "crumb_quotes"), ("chunk_id", "document_chunks")},
        "criterion_applicability": {("criterion_id", "criteria"), ("evaluation_run_id", "evaluation_runs")},
        "criterion_evaluations": {("criterion_id", "criteria"), ("evaluation_run_id", "evaluation_runs")},
        "gaps": {("evaluation_id", "criterion_evaluations")},
        "findings": {("criterion_id", "criteria"), ("evidence_item_id", "crumbs")},
        "auditor_actions": {("finding_id", "findings"), ("gap_id", "gaps")},
    }
    with closing(db_util.connect(database)) as conn:
        for table, required in expected.items():
            actual = {(row[3], row[2]) for row in conn.execute(f"PRAGMA foreign_key_list({table})")}
            assert required <= actual, f"{table}: missing {required - actual}"


def test_initializer_is_idempotent_and_reset_is_explicit(database: Path):
    with closing(db_util.connect(database)) as conn:
        db_util.insert(conn, "documents", _document())
        conn.commit()

    assert init_db.initialize(database) == "already initialized; existing data preserved"
    with closing(db_util.connect(database)) as conn:
        assert db_util.exists(conn, "documents", "doc_id", "DOC-0001")

    assert init_db.initialize(database, reset=True) == "initialized"
    with closing(db_util.connect(database)) as conn:
        assert not db_util.exists(conn, "documents", "doc_id", "DOC-0001")


def test_initializer_refuses_nonempty_unknown_database(tmp_path: Path):
    path = tmp_path / "other.sqlite"
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE unrelated(value TEXT)")
    with pytest.raises(RuntimeError, match="refusing to clobber"):
        init_db.initialize(path)
    result = subprocess.run(
        [sys.executable, str(ENCONET / "scripts" / "init_db.py"), "--db", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
    )
    assert result.returncode != 0
    assert "refusing to clobber" in result.stderr


def test_db_util_validates_ids_and_names_duplicate(database: Path):
    with closing(db_util.connect(database)) as conn:
        with pytest.raises(ValueError, match="invalid doc_id.*BAD-ID"):
            db_util.insert(conn, "documents", {**_document(), "doc_id": "BAD-ID"})
        db_util.insert(conn, "documents", _document())
        with pytest.raises(ValueError, match="DOC-0001"):
            db_util.insert(conn, "documents", _document())
        with pytest.raises(ValueError, match="unsafe SQL identifier"):
            db_util.lookup(conn, "documents; DROP TABLE documents", "doc_id", "DOC-0001")


def test_foreign_keys_and_vocab_checks_fail_closed(database: Path):
    with closing(db_util.connect(database)) as conn:
        with pytest.raises(ValueError, match="FOREIGN KEY constraint failed"):
            db_util.insert(conn, "document_chunks", {
                "chunk_id": "CHUNK-DOC-9999-0001", "doc_id": "DOC-9999",
                "heading_path": "1", "chunk_text": "text", "char_start": 0,
                "char_end": 4, "source_sha256": "b" * 64,
            })
        with pytest.raises(ValueError, match="CHECK constraint failed"):
            db_util.insert(conn, "documents", {**_document(), "document_side": "INVALID"})


def test_traceability_chain_and_action_exclusivity(database: Path):
    with closing(db_util.connect(database)) as conn:
        db_util.insert(conn, "documents", _document())
        db_util.insert(conn, "sieve_runs", {
            "run_id": "RUN-20260712-01", "doc_id": "DOC-0001",
            "prompt_version": "appb_document_v1", "document_side": "DOCUMENT",
            "source_rule": None,
        })
        db_util.insert(conn, "crumbs", {
            "item_id": "CRUMB-DOC-0001-APP_B_I-0001", "doc_id": "DOC-0001",
            "sieve_run_id": "RUN-20260712-01", "criterion_id": "APP_B_I",
            "document_side": "DOCUMENT", "statement": "Objective evidence",
        })
        db_util.insert(conn, "evaluation_runs", {
            "run_id": "RUN-20260712-02", "supplier": "enconet",
            "deliverable_language": "en", "scoring_model_version": "0.1-placeholder",
        })
        db_util.insert(conn, "criterion_evaluations", {
            "evaluation_id": "EVAL-APP_B_I", "evaluation_run_id": "RUN-20260712-02",
            "criterion_id": "APP_B_I", "rating": "undetermined", "score": 0,
            "rationale": "Pending review",
        })
        db_util.insert(conn, "gaps", {
            "gap_id": "GAP-APP_B_I-01", "evaluation_id": "EVAL-APP_B_I",
            "status": "missing-evidence", "description": "Need records",
        })
        with pytest.raises(ValueError, match="CHECK constraint failed"):
            db_util.insert(conn, "auditor_actions", {
                "action_id": "ACT-0001", "action_type": "document_request",
                "description": "Request records", "finding_id": None, "gap_id": None,
            })
        db_util.insert(conn, "auditor_actions", {
            "action_id": "ACT-0001", "action_type": "document_request",
            "description": "Request records", "gap_id": "GAP-APP_B_I-01",
        })
        assert db_util.lookup(conn, "auditor_actions", "action_id", "ACT-0001")["gap_id"] == "GAP-APP_B_I-01"
