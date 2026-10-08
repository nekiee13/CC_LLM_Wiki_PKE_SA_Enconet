import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import seed_requirements as tool


def _db(tmp_path: Path) -> Path:
    path = tmp_path / "audit.sqlite"
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE criteria (criterion_id TEXT PRIMARY KEY);
        CREATE TABLE sieve_runs (
            run_id TEXT PRIMARY KEY, is_active INTEGER NOT NULL
        );
        CREATE TABLE crumbs (
            item_id TEXT PRIMARY KEY, criterion_id TEXT NOT NULL,
            sieve_run_id TEXT NOT NULL, document_side TEXT NOT NULL,
            item_type TEXT, statement TEXT NOT NULL
        );
        CREATE TABLE requirements (
            requirement_id TEXT PRIMARY KEY, criterion_id TEXT NOT NULL,
            requirement_text TEXT NOT NULL, source_item_id TEXT NOT NULL,
            parent_requirement_id TEXT, is_subrequirement INTEGER NOT NULL
        );
        """
    )
    conn.executemany("INSERT INTO criteria VALUES (?)", [("APP_B_I",), ("APP_B_II",)])
    conn.execute("INSERT INTO sieve_runs VALUES ('RUN-1', 1)")
    conn.executemany(
        "INSERT INTO crumbs VALUES (?,?,?,?,?,?)",
        [
            ("CRUMB-DOC-0001-APP_B_I-0001", "APP_B_I", "RUN-1", "RULE", "requirement", "First rule"),
            ("CRUMB-DOC-0001-APP_B_I-0002", "APP_B_I", "RUN-1", "RULE", "requirement", "First rule"),
            ("CRUMB-DOC-0001-APP_B_II-0001", "APP_B_II", "RUN-1", "RULE", "requirement", "Second rule"),
        ],
    )
    conn.commit()
    conn.close()
    return path


def test_preview_is_read_only_and_deduplicates_text(tmp_path, monkeypatch):
    db = _db(tmp_path)
    monkeypatch.setattr(tool, "local_path", lambda value: Path(value))
    monkeypatch.setattr(tool.db_util, "local_path", lambda value: Path(value), raising=False)
    result = tool.seed(db=db, run_id='RUN-1')
    assert result["mode"] == "preview"
    assert result["planned"] == 2
    assert sqlite3.connect(db).execute("SELECT COUNT(*) FROM requirements").fetchone()[0] == 0


def test_apply_is_idempotent_and_uses_rule_sources(tmp_path, monkeypatch):
    db = _db(tmp_path)
    monkeypatch.setattr(tool, "local_path", lambda value: Path(value))
    monkeypatch.setattr(tool.db_util, "local_path", lambda value: Path(value), raising=False)
    first = tool.seed(db=db, apply=True, run_id='RUN-1')
    second = tool.seed(db=db, apply=True, run_id='RUN-1')
    assert first["inserted"] == 2
    assert second["inserted"] == 0
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM requirements").fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM requirements WHERE source_item_id LIKE 'CRUMB-%'").fetchone()[0] == 2


def test_missing_criterion_is_rejected(tmp_path, monkeypatch):
    db = _db(tmp_path)
    conn = sqlite3.connect(db)
    conn.execute("DELETE FROM crumbs WHERE criterion_id='APP_B_II'")
    conn.commit()
    conn.close()
    monkeypatch.setattr(tool, "local_path", lambda value: Path(value))
    with pytest.raises(ValueError, match="no active RULE crumb"):
        tool.seed(db=db, run_id='RUN-1')


def test_foreign_database_is_refused_before_open(tmp_path):
    with pytest.raises(ValueError, match="local to project"):
        tool.seed(db=tool.ROOT.parent / "foreign-supplier-seed-boundary.sqlite")


def test_explicit_run_selection_excludes_other_active_rules(tmp_path, monkeypatch):
    db = _db(tmp_path)
    with sqlite3.connect(db) as conn:
        conn.execute("INSERT INTO sieve_runs VALUES ('RUN-2',1)")
        conn.execute("INSERT INTO crumbs VALUES (?,?,?,?,?,?)",
                     ('CRUMB-DOC-0002-APP_B_I-0001','APP_B_I','RUN-2','RULE','requirement','Other governing duty'))
    monkeypatch.setattr(tool, "local_path", lambda value: Path(value))
    assert tool.seed(db=db, run_id='RUN-1')['planned'] == 2


def test_missing_run_selection_is_refused(tmp_path, monkeypatch):
    db = _db(tmp_path)
    monkeypatch.setattr(tool, "local_path", lambda value: Path(value))
    with pytest.raises(ValueError, match="explicit RULE run"):
        tool.seed(db=db)
