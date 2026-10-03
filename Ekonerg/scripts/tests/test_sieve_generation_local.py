"""Regression tests for the local, approval-gated generation stage."""

from __future__ import annotations

import sys
import shutil
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import db_util  # noqa: E402
import init_db  # noqa: E402
import project_paths  # noqa: E402
import sieve_generation  # noqa: E402


def _database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "db").mkdir()
    (tmp_path / "schemas").mkdir()
    shutil.copyfile(ROOT.parent / "db" / "schema.sql", tmp_path / "db" / "schema.sql")
    shutil.copyfile(ROOT.parent / "schemas" / "id_patterns.yml", tmp_path / "schemas" / "id_patterns.yml")
    monkeypatch.setattr(project_paths, "ROOT", tmp_path)
    monkeypatch.setattr(init_db, "ROOT", tmp_path)
    monkeypatch.setattr(init_db, "SCHEMA", tmp_path / "db" / "schema.sql")
    monkeypatch.setattr(db_util, "ROOT", tmp_path)
    monkeypatch.setattr(db_util, "PATTERNS", tmp_path / "schemas" / "id_patterns.yml")
    db_util.id_patterns.cache_clear()
    database = tmp_path / "audit.sqlite"
    init_db.initialize(database)
    with db_util.connect(database) as conn:
        db_util.insert(conn, "documents", {
            "doc_id": "DOC-0001", "filename": "source.txt", "title": "Source",
            "supplier": "Ekonerg", "language": "undetermined",
            "document_side": "DOCUMENT", "sha256": "a" * 64,
        })
        db_util.insert(conn, "sieve_runs", {
            "run_id": "RUN-20261003-01", "doc_id": "DOC-0001",
            "prompt_version": "appb_document_v1", "document_side": "DOCUMENT",
            "status": "candidate", "is_active": 0,
        })
    return database


def test_generation_stage_requires_an_approved_decision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = _database(tmp_path, monkeypatch)
    approvals = tmp_path / "approvals.csv"
    approvals.write_text(
        "object_id,decision,date,reviewer,notes\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="approved decision missing"):
        sieve_generation.decide(
            database,
            run_id="RUN-20261003-01",
            operation="reject",
            decision_ref="PROMPT-UNAPPROVED",
            reason="test guard",
            approvals=approvals,
        )
