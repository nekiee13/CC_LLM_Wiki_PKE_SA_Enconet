import csv
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reconcile_run_metadata as tool


def _db(tmp_path: Path, run_id: str = tool.DEFAULT_RUN_ID,
        version: str = tool.DEFAULT_OLD) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "audit.sqlite"
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE evaluation_runs (run_id TEXT PRIMARY KEY, supplier TEXT NOT NULL, "
        "deliverable_language TEXT NOT NULL, scoring_model_version TEXT NOT NULL, "
        "started_at TEXT, completed_at TEXT)"
    )
    conn.execute(
        "INSERT INTO evaluation_runs VALUES (?,?,?,?,?,?)",
        (run_id, "Ekonerg", "hr", version, "2026-10-04", None),
    )
    conn.commit()
    conn.close()
    return path


def _approval(tmp_path: Path, ref: str) -> Path:
    path = tmp_path / "approvals.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("object_id", "decision", "date", "reviewer", "notes"))
        writer.writerow((ref, "approved", "2026-10-04", "Owner", "test"))
    return path


def test_dry_run_is_read_only_and_records_matching_hashes(tmp_path, monkeypatch):
    monkeypatch.setattr(tool.db_util, "local_path", lambda value: Path(value))
    db = _db(tmp_path)
    result = tool.reconcile(db=db)
    assert result["mode"] == "dry-run"
    assert result["changed"] is False
    assert result["before_hash"] == result["after_hash"]
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT scoring_model_version FROM evaluation_runs").fetchone()[0] == tool.DEFAULT_OLD


def test_apply_requires_approval_and_changes_only_target_value(tmp_path, monkeypatch):
    monkeypatch.setattr(tool.db_util, "local_path", lambda value: Path(value))
    db = _db(tmp_path)
    ref = "G3-METADATA-RECONCILE-20261004-OWNER"
    result = tool.reconcile(db=db, decision_ref=ref, approvals=_approval(tmp_path, ref), apply=True)
    assert result["changed"] is True
    assert result["before_hash"] != result["after_hash"]
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT scoring_model_version FROM evaluation_runs").fetchone()[0] == tool.DEFAULT_NEW


def test_refuses_other_run_or_wrong_current_value(tmp_path, monkeypatch):
    monkeypatch.setattr(tool.db_util, "local_path", lambda value: Path(value))
    ref = "G3-METADATA-RECONCILE-20261004-OWNER"
    with pytest.raises(ValueError, match="only controlled target"):
        tool.reconcile(db=_db(tmp_path / "other", run_id="RUN-OTHER"), run_id="RUN-OTHER")
    with pytest.raises(ValueError, match="exact expected old value"):
        tool.reconcile(db=_db(tmp_path / "wrong", version="other-version"))
    with pytest.raises(ValueError, match="approved decision missing"):
        tool.reconcile(db=_db(tmp_path / "missing"), decision_ref=ref, apply=True,
                       approvals=tmp_path / "missing.csv")
