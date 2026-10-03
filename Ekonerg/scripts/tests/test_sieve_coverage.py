import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_sieve_coverage


def test_coverage_reports_missing_and_zero_crumb_documents(tmp_path, monkeypatch):
    db = tmp_path / "audit.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE documents (doc_id TEXT, filename TEXT, document_side TEXT)")
        conn.execute("CREATE TABLE sieve_runs (run_id TEXT, doc_id TEXT, is_active INTEGER)")
        conn.execute("CREATE TABLE crumbs (item_id TEXT, doc_id TEXT, sieve_run_id TEXT)")
        conn.executemany("INSERT INTO documents VALUES (?,?,?)", [
            ("DOC-0001", "one.md", "DOCUMENT"),
            ("DOC-0002", "two.md", "DOCUMENT"),
        ])
        conn.execute("INSERT INTO sieve_runs VALUES (?,?,?)", ("RUN-1", "DOC-0001", 1))
        conn.commit()
    monkeypatch.setattr(check_sieve_coverage, "local_path", lambda value: Path(value))

    def connect(path):
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn

    monkeypatch.setattr(check_sieve_coverage.db_util, "connect", connect)
    result = check_sieve_coverage.coverage(db)
    assert result["document_count"] == 2
    assert result["active_run_count"] == 1
    assert result["active_crumb_count"] == 0
    assert result["zero_crumb_active_runs"][0]["doc_id"] == "DOC-0001"
    assert result["missing_active_runs"][0]["doc_id"] == "DOC-0002"
