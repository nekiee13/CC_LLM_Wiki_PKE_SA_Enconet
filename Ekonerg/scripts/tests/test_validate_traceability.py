"""Regression tests for live-run traceability scoping."""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_traceability  # noqa: E402


def _database(path: Path) -> None:
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE sieve_runs (
            run_id TEXT PRIMARY KEY,
            is_active INTEGER NOT NULL
        );
        CREATE TABLE crumbs (
            item_id TEXT PRIMARY KEY,
            doc_id TEXT NOT NULL,
            sieve_run_id TEXT NOT NULL
        );
        CREATE TABLE crumb_quotes (
            item_id TEXT NOT NULL,
            quote_id TEXT NOT NULL,
            quote_original TEXT NOT NULL
        );
        CREATE TABLE crumb_chunk_links (
            item_id TEXT NOT NULL,
            quote_id TEXT NOT NULL,
            chunk_id TEXT NOT NULL
        );
        CREATE TABLE document_chunks (
            chunk_id TEXT PRIMARY KEY,
            doc_id TEXT NOT NULL,
            chunk_text TEXT NOT NULL,
            source_sha256 TEXT NOT NULL
        );
        CREATE TABLE documents (
            doc_id TEXT PRIMARY KEY,
            sha256 TEXT NOT NULL
        );
        """
    )
    connection.executemany(
        "INSERT INTO sieve_runs(run_id, is_active) VALUES (?, ?)",
        [("RUN-LIVE", 1), ("RUN-HISTORIC", 0)],
    )
    connection.executemany(
        "INSERT INTO crumbs(item_id, doc_id, sieve_run_id) VALUES (?, ?, ?)",
        [("ITEM-LIVE", "DOC-LIVE", "RUN-LIVE"),
         ("ITEM-HISTORIC", "DOC-HISTORIC", "RUN-HISTORIC")],
    )
    connection.executemany(
        "INSERT INTO crumb_quotes(item_id, quote_id, quote_original) VALUES (?, ?, ?)",
        [("ITEM-LIVE", "QUOTE-LIVE", "controlled copy"),
         ("ITEM-HISTORIC", "QUOTE-HISTORIC", "historic wording")],
    )
    connection.execute(
        "INSERT INTO documents(doc_id, sha256) VALUES (?, ?)",
        ("DOC-LIVE", "sha-live"),
    )
    connection.execute(
        "INSERT INTO document_chunks(chunk_id, doc_id, chunk_text, source_sha256) "
        "VALUES (?, ?, ?, ?)",
        ("CHUNK-LIVE", "DOC-LIVE", "controlled copy", "sha-live"),
    )
    connection.execute(
        "INSERT INTO crumb_chunk_links(item_id, quote_id, chunk_id) VALUES (?, ?, ?)",
        ("ITEM-LIVE", "QUOTE-LIVE", "CHUNK-LIVE"),
    )
    connection.commit()
    connection.close()


def test_active_only_excludes_rejected_historical_runs(tmp_path, monkeypatch):
    database = tmp_path / "audit.sqlite"
    exceptions = tmp_path / "link_exceptions.csv"
    exceptions.write_text("crumb_id,quote_id,reason,approved_by,date\n", encoding="utf-8")
    _database(database)
    monkeypatch.setattr(validate_traceability, "local_path", lambda value: Path(value))

    strict_errors = validate_traceability.validate(
        database, exceptions_path=exceptions
    )
    live_errors = validate_traceability.validate(
        database, exceptions_path=exceptions, active_only=True
    )

    assert any("QUOTE-HISTORIC" in error for error in strict_errors)
    assert live_errors == []
