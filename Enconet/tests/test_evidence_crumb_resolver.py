"""EA1.1 tests for read-only, complete, fail-closed crumb resolution."""
from __future__ import annotations

import hashlib
import sqlite3
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import db_util  # noqa: E402
import evidence_resolver  # noqa: E402
import init_db  # noqa: E402


CRUMB_ID = "CRUMB-DOC-0001-APP_B_I-0001"


@pytest.fixture
def evidence_db(tmp_path: Path) -> Path:
    database = tmp_path / "evidence.sqlite"
    init_db.initialize(database)
    with db_util.connect(database) as connection:
        for doc_id, checksum in (("DOC-0001", "a" * 64), ("DOC-0002", "b" * 64)):
            db_util.insert(connection, "documents", {
                "doc_id": doc_id,
                "filename": f"{doc_id}.md",
                "title": "Življenjski cikel — dokaz" if doc_id == "DOC-0001" else "Other",
                "supplier": "Enconet",
                "language": "sl" if doc_id == "DOC-0001" else "en",
                "document_side": "DOCUMENT",
                "sha256": checksum,
            })
            db_util.insert(connection, "sieve_runs", {
                "run_id": f"RUN-2026090{1 if doc_id == 'DOC-0001' else 2}-01",
                "doc_id": doc_id,
                "prompt_version": "v1",
                "document_side": "DOCUMENT",
            })
        for sequence, text, start, end in (
            (1, "Točen dokaz za kakovost.", 0, 25),
            (2, "Normaliziran   dokaz\nza sledljivost.", 25, 62),
        ):
            db_util.insert(connection, "document_chunks", {
                "chunk_id": f"CHUNK-DOC-0001-{sequence:04d}",
                "doc_id": "DOC-0001",
                "heading_path": f"Chapter {sequence}",
                "chunk_text": text,
                "char_start": start,
                "char_end": end,
                "source_sha256": "a" * 64,
            })
        db_util.insert(connection, "document_chunks", {
            "chunk_id": "CHUNK-DOC-0002-0001",
            "doc_id": "DOC-0002",
            "heading_path": "Other",
            "chunk_text": "Other evidence.",
            "char_start": 0,
            "char_end": 15,
            "source_sha256": "b" * 64,
        })
        db_util.insert(connection, "crumbs", {
            "item_id": CRUMB_ID,
            "doc_id": "DOC-0001",
            "sieve_run_id": "RUN-20260901-01",
            "criterion_id": "APP_B_I",
            "document_side": "DOCUMENT",
            "statement": "Dokaz določa kakovost in sledljivost.",
            "item_type": "control",
            "quote_language": "sl",
        })
        quotes = (
            ("QUOTE-DOC-0001-0001-01", "Točen dokaz za kakovost.", "1", "CHUNK-DOC-0001-0001", "EXACT", 1.0),
            ("QUOTE-DOC-0001-0002-01", "Normaliziran dokaz za sledljivost.", "2", "CHUNK-DOC-0001-0002", "NORMALIZED", 0.875),
        )
        for quote_id, text, locator, chunk_id, method, confidence in quotes:
            db_util.insert(connection, "crumb_quotes", {
                "quote_id": quote_id,
                "item_id": CRUMB_ID,
                "quote_original": text,
                "quote_language": "sl",
                "source_locator": locator,
            })
            db_util.insert(connection, "crumb_chunk_links", {
                "item_id": CRUMB_ID,
                "quote_id": quote_id,
                "chunk_id": chunk_id,
                "link_method": method,
                "confidence": confidence,
            })
        db_util.insert(connection, "evaluation_runs", {
            "run_id": "RUN-20260903-01",
            "supplier": "enconet",
            "deliverable_language": "hr",
            "scoring_model_version": "v1",
        })
        db_util.insert(connection, "criterion_evaluations", {
            "evaluation_id": "EVAL-APP_B_I",
            "evaluation_run_id": "RUN-20260903-01",
            "criterion_id": "APP_B_I",
            "rating": "fully",
            "score": 100.0,
            "coverage": 1.0,
            "completeness": 1.0,
            "accuracy": 1.0,
            "clarity": 1.0,
            "alignment": 1.0,
            "evidence_supported": 1,
            "affirmative_summary": "yes",
            "contrary_summary": "none",
            "judge_ruling": "pass",
            "rationale": "evidence",
        })
        db_util.insert(connection, "evaluation_evidence", {
            "evaluation_id": "EVAL-APP_B_I",
            "item_id": CRUMB_ID,
        })
    return database


def _corrupt(database: Path, sql: str, parameters: tuple = ()) -> None:
    with sqlite3.connect(database) as connection:
        connection.execute(sql, parameters)


def test_resolves_complete_typed_projection_with_unicode_and_all_links(evidence_db: Path):
    resolved = evidence_resolver.resolve_crumb(evidence_db, CRUMB_ID)
    assert resolved is not None
    assert resolved["crumb"] == {
        "crumb_id": CRUMB_ID,
        "document_id": "DOC-0001",
        "criterion_id": "APP_B_I",
        "document_side": "DOCUMENT",
        "statement": "Dokaz določa kakovost in sledljivost.",
        "item_type": "control",
        "quote_ids": ["QUOTE-DOC-0001-0001-01", "QUOTE-DOC-0001-0002-01"],
        "chunk_ids": ["CHUNK-DOC-0001-0001", "CHUNK-DOC-0001-0002"],
        "evaluation_ids": ["EVAL-APP_B_I"],
        "viewer_target": f"#evidence/crumb/{CRUMB_ID}",
    }
    assert resolved["document"]["title"] == "Življenjski cikel — dokaz"
    assert resolved["document"]["viewer_target"] == "#evidence/document/DOC-0001"
    assert [row["source_order"] for row in resolved["quotes"]] == [1, 2]
    assert [row["link_method"] for row in resolved["quotes"]] == ["EXACT", "NORMALIZED"]
    assert [row["confidence"] for row in resolved["quotes"]] == [1.0, 0.875]
    assert [row["chunk_id"] for row in resolved["quotes"]] == [
        "CHUNK-DOC-0001-0001", "CHUNK-DOC-0001-0002"
    ]
    assert [row["chunk_id"] for row in resolved["chunks"]] == [
        "CHUNK-DOC-0001-0001", "CHUNK-DOC-0001-0002"
    ]


def test_connection_is_mode_ro_query_only_and_database_bytes_do_not_change(
    evidence_db: Path, monkeypatch: pytest.MonkeyPatch
):
    before = hashlib.sha256(evidence_db.read_bytes()).hexdigest()
    real_connect = sqlite3.connect
    calls: list[tuple[object, bool]] = []

    def recording_connect(database, *args, **kwargs):
        calls.append((database, kwargs.get("uri", False)))
        return real_connect(database, *args, **kwargs)

    monkeypatch.setattr(evidence_resolver.sqlite3, "connect", recording_connect)
    assert evidence_resolver.resolve_crumb(evidence_db, CRUMB_ID) is not None
    with evidence_resolver._connect_readonly(evidence_db) as connection:
        assert connection.execute("PRAGMA query_only").fetchone()[0] == 1
        with pytest.raises(sqlite3.OperationalError):
            connection.execute("CREATE TABLE forbidden_write(value TEXT)")
    assert hashlib.sha256(evidence_db.read_bytes()).hexdigest() == before
    assert len(calls) == 2
    assert all(str(database).endswith("?mode=ro") for database, _uri in calls)
    assert all(uri is True for _database, uri in calls)


def test_single_quote_projection_remains_complete(evidence_db: Path):
    with sqlite3.connect(evidence_db) as connection:
        connection.execute(
            "DELETE FROM crumb_chunk_links WHERE quote_id=?",
            ("QUOTE-DOC-0001-0002-01",),
        )
        connection.execute(
            "DELETE FROM crumb_quotes WHERE quote_id=?",
            ("QUOTE-DOC-0001-0002-01",),
        )
    resolved = evidence_resolver.resolve_crumb(evidence_db, CRUMB_ID)
    assert resolved is not None
    assert [row["quote_id"] for row in resolved["quotes"]] == [
        "QUOTE-DOC-0001-0001-01"
    ]
    assert resolved["crumb"]["chunk_ids"] == ["CHUNK-DOC-0001-0001"]


def test_unknown_inactive_and_sql_injection_like_ids_return_no_match(evidence_db: Path):
    assert evidence_resolver.resolve_crumb(evidence_db, "CRUMB-DOC-0001-APP_B_I-9999") is None
    assert evidence_resolver.resolve_crumb(evidence_db, "' OR 1=1; DROP TABLE crumbs; --") is None
    with sqlite3.connect(evidence_db) as connection:
        assert connection.execute("SELECT count(*) FROM crumbs").fetchone()[0] == 1
        connection.execute(
            "UPDATE sieve_runs SET status='superseded', is_active=0 WHERE run_id=?",
            ("RUN-20260901-01",),
        )
    assert evidence_resolver.resolve_crumb(evidence_db, CRUMB_ID) is None


def test_missing_database_is_not_created(tmp_path: Path):
    absent = tmp_path / "absent.sqlite"
    with pytest.raises(sqlite3.OperationalError):
        evidence_resolver.resolve_crumb(absent, CRUMB_ID)
    assert not absent.exists()


@pytest.mark.parametrize(
    "sql,parameters,message",
    (
        ("DELETE FROM crumb_chunk_links", (), "missing chunk link"),
        ("DELETE FROM crumb_chunk_links; DELETE FROM crumb_quotes", (), "missing quote"),
        (
            "UPDATE crumb_chunk_links SET chunk_id='CHUNK-DOC-0001-9999' WHERE quote_id=?",
            ("QUOTE-DOC-0001-0001-01",),
            "missing chunk",
        ),
        (
            "UPDATE crumb_chunk_links SET chunk_id='CHUNK-DOC-0002-0001' WHERE quote_id=?",
            ("QUOTE-DOC-0001-0001-01",),
            "cross-document",
        ),
        (
            "UPDATE document_chunks SET source_sha256=? WHERE chunk_id=?",
            ("c" * 64, "CHUNK-DOC-0001-0001"),
            "source hash mismatch",
        ),
    ),
)
def test_traceability_defects_fail_closed(
    evidence_db: Path, sql: str, parameters: tuple, message: str
):
    if ";" in sql:
        with sqlite3.connect(evidence_db) as connection:
            connection.executescript(sql)
    else:
        _corrupt(evidence_db, sql, parameters)
    with pytest.raises(evidence_resolver.EvidenceIntegrityError, match=message):
        evidence_resolver.resolve_crumb(evidence_db, CRUMB_ID)


def test_one_quote_cannot_ambiguously_link_to_multiple_chunks(evidence_db: Path):
    _corrupt(
        evidence_db,
        "INSERT INTO crumb_chunk_links(item_id,quote_id,chunk_id,link_method,confidence) "
        "VALUES(?,?,?,?,?)",
        (CRUMB_ID, "QUOTE-DOC-0001-0001-01", "CHUNK-DOC-0001-0002", "NORMALIZED", 0.5),
    )
    with pytest.raises(evidence_resolver.EvidenceIntegrityError, match="ambiguous chunk links"):
        evidence_resolver.resolve_crumb(evidence_db, CRUMB_ID)


def test_complete_production_sample_resolves_all_three_quotes():
    database = ENCONET / "db" / "nqa_audit.sqlite"
    crumb_id = "CRUMB-DOC-0021-APP_B_I-0003"
    resolved = evidence_resolver.resolve_crumb(database, crumb_id)
    assert resolved is not None
    assert resolved["crumb"]["crumb_id"] == crumb_id
    assert len(resolved["quotes"]) == 3
    assert {row["chunk_id"] for row in resolved["quotes"]} == {"CHUNK-DOC-0021-0105"}
