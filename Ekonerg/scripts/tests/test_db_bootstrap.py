"""Fresh audit databases must start empty and remain inside their project."""

from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT = Path(__file__).resolve().parents[2]
REQUIRED_TABLES = {
    "criteria", "documents", "document_chunks", "sieve_runs", "sieve_generation_events",
    "sieve_run_authorities", "crumbs", "crumb_sources", "crumb_quotes",
    "crumb_authority_refs", "crumb_chunk_links", "requirements", "evaluation_runs",
    "criterion_applicability", "criterion_evaluations", "evaluation_evidence", "gaps",
    "findings", "auditor_actions", "dashboard_runs", "validation_runs",
    "approved_sources",
}


def _copy_local_project(root: Path) -> None:
    (root / "scripts").mkdir(parents=True)
    (root / "db").mkdir()
    for name in ("init_db.py", "project_paths.py"):
        shutil.copyfile(PROJECT / "scripts" / name, root / "scripts" / name)
    shutil.copyfile(PROJECT / "db" / "schema.sql", root / "db" / "schema.sql")


def _run(root: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, "-B", str(root / "scripts" / "init_db.py"), *args],
        cwd=cwd, env=env, capture_output=True, text=True, check=False,
    )


@pytest.mark.parametrize(("company_name", "with_sibling"), [
    ("Audit Beta with spaces", False),
    ("Ekonerg ogled Čakovec", True),
])
def test_fresh_bootstrap_is_empty_local_and_repeatable(
    tmp_path: Path, company_name: str, with_sibling: bool,
) -> None:
    root = tmp_path / company_name
    _copy_local_project(root)
    sibling = tmp_path / "Enconet"
    sibling.mkdir()
    marker = sibling / "marker.txt"
    if with_sibling:
        marker.write_bytes(b"other-company")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
    first = _run(root, sibling)
    assert first.returncode == 0, first.stderr
    db = root / "db" / "nqa_audit.sqlite"
    assert db.is_file()
    with sqlite3.connect(db) as conn:
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        assert REQUIRED_TABLES <= tables
        assert conn.execute("PRAGMA user_version").fetchone()[0] == 1
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        for table in ("documents", "criteria", "approved_sources", "sieve_runs", "crumbs"):
            assert conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == 0
        source_fks = {row[2] for row in conn.execute(
            "PRAGMA foreign_key_list(sieve_run_authorities)"
        )}
        assert "approved_sources" in source_fks
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(
            "INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
            "VALUES (?,?,?,?,?,?,?)",
            ("DOC-0001", "invented.txt", "Invented", "Synthetic", "xx", "RULE", "a" * 64),
        )
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side,source_rule) "
                "VALUES (?,?,?,?,?)",
                ("RUN-20260930-01", "DOC-0001", "test", "RULE", "UNLISTED"),
            )
        conn.execute(
            "INSERT INTO approved_sources(source_code,authority_role,edition,source_sha256,"
            "approval_ref,approved_by,approved_date) VALUES (?,?,?,?,?,?,?)",
            ("DEMO_RULE", "GOVERNING", "test-only", "b" * 64,
             "TEST-ONLY", "Synthetic", "2026-09-30"),
        )
        conn.execute(
            "INSERT INTO approved_sources(source_code,authority_role,edition,source_sha256,"
            "approval_ref,approved_by,approved_date) VALUES (?,?,?,?,?,?,?)",
            ("DEMO_GUIDE", "INTERPRETIVE", "test-only", "c" * 64,
             "TEST-ONLY", "Synthetic", "2026-09-30"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side,source_rule) "
                "VALUES (?,?,?,?,?)",
                ("RUN-20260930-02", "DOC-0001", "test", "RULE", "DEMO_GUIDE"),
            )
        conn.execute(
            "INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side,source_rule) "
            "VALUES (?,?,?,?,?)",
            ("RUN-20260930-01", "DOC-0001", "test", "RULE", "DEMO_RULE"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO sieve_run_authorities(run_id,authority_role,source_code,source_locator) "
                "VALUES (?,?,?,?)",
                ("RUN-20260930-01", "INTERPRETIVE", "DEMO_RULE", "fictional"),
            )
        conn.execute(
            "INSERT INTO sieve_run_authorities(run_id,authority_role,source_code,source_locator) "
            "VALUES (?,?,?,?)",
            ("RUN-20260930-01", "GOVERNING", "DEMO_RULE", "fictional"),
        )
    original = (db.read_bytes(), db.stat().st_mtime_ns)
    second = _run(root, tmp_path)
    assert second.returncode == 0, second.stderr
    assert "preserved" in second.stdout
    assert (db.read_bytes(), db.stat().st_mtime_ns) == original
    assert not (root / "Enconet").exists()
    if with_sibling:
        assert (marker.read_bytes(), marker.stat().st_mtime_ns) == before
        assert sorted(path.name for path in sibling.iterdir()) == ["marker.txt"]
    else:
        assert list(sibling.iterdir()) == []


def test_source_choices_are_not_embedded_in_schema() -> None:
    sql = (PROJECT / "db" / "schema.sql").read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS approved_sources" in sql
    for inherited_choice in ("10CFR50_APPB", "10CFR21", "ASME_NQA1", "Enconet"):
        assert inherited_choice not in sql


def test_refuses_foreign_path_and_reset_without_touching_files(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta with spaces"
    sibling = tmp_path / "Enconet"
    sibling.mkdir()
    marker = sibling / "marker.txt"
    marker.write_bytes(b"other-company")
    before = (marker.read_bytes(), marker.stat().st_mtime_ns)
    _copy_local_project(root)
    foreign = sibling / "nqa_audit.sqlite"
    rejected = _run(root, sibling, "--db", str(foreign))
    assert rejected.returncode != 0
    assert not foreign.exists()
    assert (marker.read_bytes(), marker.stat().st_mtime_ns) == before
    reset = _run(root, sibling, "--reset")
    assert reset.returncode != 0
    assert not (root / "db" / "nqa_audit.sqlite").exists()


def test_refuses_incomplete_existing_database_without_overwrite(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta with spaces"
    _copy_local_project(root)
    db = root / "db" / "nqa_audit.sqlite"
    db.write_bytes(b"not a database")
    before = (db.read_bytes(), db.stat().st_mtime_ns)
    result = _run(root, tmp_path)
    assert result.returncode != 0
    assert (db.read_bytes(), db.stat().st_mtime_ns) == before


def test_refuses_existing_database_with_broken_references(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta with spaces"
    _copy_local_project(root)
    assert _run(root, tmp_path).returncode == 0
    db = root / "db" / "nqa_audit.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys = OFF")
        conn.execute(
            "INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side) "
            "VALUES (?,?,?,?)",
            ("RUN-20260930-01", "DOC-9999", "test", "RULE"),
        )
    before = (db.read_bytes(), db.stat().st_mtime_ns)
    result = _run(root, tmp_path)
    assert result.returncode != 0
    assert "foreign" in result.stderr.lower()
    assert (db.read_bytes(), db.stat().st_mtime_ns) == before
