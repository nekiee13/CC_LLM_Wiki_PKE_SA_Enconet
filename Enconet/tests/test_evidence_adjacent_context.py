"""EA1.3 tests for bounded, same-document adjacent chunk context."""
from __future__ import annotations

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
QUOTE_ID = "QUOTE-DOC-0001-0003-01"


@pytest.fixture
def context_db(tmp_path: Path) -> Path:
    database = tmp_path / "context.sqlite"
    init_db.initialize(database)
    with db_util.connect(database) as connection:
        for doc_id, checksum in (("DOC-0001", "a" * 64), ("DOC-0002", "b" * 64)):
            db_util.insert(connection, "documents", {
                "doc_id": doc_id,
                "filename": f"{doc_id}.md",
                "title": doc_id,
                "supplier": "Enconet",
                "language": "en",
                "document_side": "DOCUMENT",
                "sha256": checksum,
            })
            db_util.insert(connection, "sieve_runs", {
                "run_id": f"RUN-2026090{1 if doc_id == 'DOC-0001' else 2}-01",
                "doc_id": doc_id,
                "prompt_version": "v1",
                "document_side": "DOCUMENT",
            })
        # Character offsets, not insertion order or identifier sorting, define source order.
        for chunk_id, start in (
            ("CHUNK-DOC-0001-0001", 0),
            ("CHUNK-DOC-0001-0002", 10),
            ("CHUNK-DOC-0001-0004", 30),
            ("CHUNK-DOC-0001-0003", 20),
            ("CHUNK-DOC-0001-0005", 40),
        ):
            db_util.insert(connection, "document_chunks", {
                "chunk_id": chunk_id,
                "doc_id": "DOC-0001",
                "heading_path": chunk_id,
                "chunk_text": f"source {chunk_id}",
                "char_start": start,
                "char_end": start + 9,
                "source_sha256": "a" * 64,
            })
        db_util.insert(connection, "document_chunks", {
            "chunk_id": "CHUNK-DOC-0002-0001",
            "doc_id": "DOC-0002",
            "heading_path": "other",
            "chunk_text": "other document",
            "char_start": 15,
            "char_end": 29,
            "source_sha256": "b" * 64,
        })
        db_util.insert(connection, "crumbs", {
            "item_id": CRUMB_ID,
            "doc_id": "DOC-0001",
            "sieve_run_id": "RUN-20260901-01",
            "criterion_id": "APP_B_I",
            "document_side": "DOCUMENT",
            "statement": "middle evidence",
            "item_type": "evidence",
        })
        db_util.insert(connection, "crumb_quotes", {
            "quote_id": QUOTE_ID,
            "item_id": CRUMB_ID,
            "quote_original": "source",
            "quote_language": "en",
            "source_locator": "middle",
        })
        db_util.insert(connection, "crumb_chunk_links", {
            "item_id": CRUMB_ID,
            "quote_id": QUOTE_ID,
            "chunk_id": "CHUNK-DOC-0001-0003",
            "link_method": "EXACT",
            "confidence": 1.0,
        })
    return database


def _chunks(database: Path, radius: int = 1) -> list[dict]:
    resolved = evidence_resolver.resolve_crumb(database, CRUMB_ID, context_radius=radius)
    assert resolved is not None
    return resolved["chunks"]


def test_middle_chunk_gets_one_previous_and_next_in_source_order(context_db: Path):
    chunks = _chunks(context_db)
    assert [row["chunk_id"] for row in chunks] == [
        "CHUNK-DOC-0001-0002", "CHUNK-DOC-0001-0003", "CHUNK-DOC-0001-0004"
    ]
    middle = chunks[1]
    assert middle["previous_chunk_id"] == "CHUNK-DOC-0001-0002"
    assert middle["next_chunk_id"] == "CHUNK-DOC-0001-0004"
    assert middle["context_truncated_before"] is False
    assert middle["context_truncated_after"] is False


def test_context_edges_distinguish_truncation_from_document_edges(context_db: Path):
    radius_one = _chunks(context_db, 1)
    assert radius_one[0]["previous_chunk_id"] is None
    assert radius_one[0]["context_truncated_before"] is True
    assert radius_one[-1]["next_chunk_id"] is None
    assert radius_one[-1]["context_truncated_after"] is True

    full_document = _chunks(context_db, 2)
    assert full_document[0]["previous_chunk_id"] is None
    assert full_document[0]["context_truncated_before"] is False
    assert full_document[-1]["next_chunk_id"] is None
    assert full_document[-1]["context_truncated_after"] is False


@pytest.mark.parametrize(
    "linked_chunk,expected_ids,edge_field",
    (
        (
            "CHUNK-DOC-0001-0001",
            ["CHUNK-DOC-0001-0001", "CHUNK-DOC-0001-0002"],
            "context_truncated_before",
        ),
        (
            "CHUNK-DOC-0001-0005",
            ["CHUNK-DOC-0001-0004", "CHUNK-DOC-0001-0005"],
            "context_truncated_after",
        ),
    ),
)
def test_first_and_last_linked_chunks_have_explicit_document_edges(
    context_db: Path, linked_chunk: str, expected_ids: list[str], edge_field: str
):
    with sqlite3.connect(context_db) as connection:
        connection.execute(
            "UPDATE crumb_chunk_links SET chunk_id=? WHERE quote_id=?",
            (linked_chunk, QUOTE_ID),
        )
    chunks = _chunks(context_db)
    assert [row["chunk_id"] for row in chunks] == expected_ids
    edge = chunks[0] if linked_chunk.endswith("0001") else chunks[-1]
    pointer = "previous_chunk_id" if linked_chunk.endswith("0001") else "next_chunk_id"
    assert edge[pointer] is None
    assert edge[edge_field] is False


def test_radius_zero_is_bounded_and_explicitly_truncated(context_db: Path):
    chunks = _chunks(context_db, 0)
    assert [row["chunk_id"] for row in chunks] == ["CHUNK-DOC-0001-0003"]
    assert chunks[0]["previous_chunk_id"] is None
    assert chunks[0]["next_chunk_id"] is None
    assert chunks[0]["context_truncated_before"] is True
    assert chunks[0]["context_truncated_after"] is True


def test_maximum_radius_is_enforced_before_database_access(tmp_path: Path):
    absent = tmp_path / "must-not-be-opened.sqlite"
    for invalid in (-1, evidence_resolver.MAX_CONTEXT_RADIUS + 1, True, 1.5, "1"):
        with pytest.raises(ValueError, match="context_radius"):
            evidence_resolver.resolve_crumb(absent, CRUMB_ID, context_radius=invalid)
    assert not absent.exists()


def test_adjacent_context_never_crosses_document_boundary(context_db: Path):
    chunks = _chunks(context_db, evidence_resolver.MAX_CONTEXT_RADIUS)
    assert {row["document_id"] for row in chunks} == {"DOC-0001"}
    assert "CHUNK-DOC-0002-0001" not in {row["chunk_id"] for row in chunks}
    assert len(chunks) <= 2 * evidence_resolver.MAX_CONTEXT_RADIUS + 1


def test_hash_inconsistent_adjacent_context_fails_closed(context_db: Path):
    with sqlite3.connect(context_db) as connection:
        connection.execute(
            "UPDATE document_chunks SET source_sha256=? WHERE chunk_id=?",
            ("c" * 64, "CHUNK-DOC-0001-0002"),
        )
    with pytest.raises(evidence_resolver.EvidenceIntegrityError, match="context chunk"):
        evidence_resolver.resolve_crumb(context_db, CRUMB_ID, context_radius=1)


def test_overlapping_production_windows_merge_to_reciprocal_links():
    registry = evidence_resolver.build_entity_registry(
        ENCONET / "db" / "nqa_audit.sqlite", "RUN-20260728-01"
    )
    chunks = {
        reference.split(":", 1)[1]: entity["data"]
        for reference, entity in registry["entities"].items()
        if reference.startswith("chunk:")
    }
    for chunk_id, chunk in chunks.items():
        previous = chunk["previous_chunk_id"]
        following = chunk["next_chunk_id"]
        if previous is not None:
            assert chunks[previous]["next_chunk_id"] == chunk_id
        if following is not None:
            assert chunks[following]["previous_chunk_id"] == chunk_id
