"""EPIC4 heading parser, atomic writer, quality, and validator tests."""
from __future__ import annotations

import csv
import sqlite3
import sys
from pathlib import Path

import pytest

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import chunk_document  # noqa: E402
import db_util  # noqa: E402
import init_db  # noqa: E402
import validate_chunks  # noqa: E402


@pytest.fixture
def project(tmp_path: Path):
    db = tmp_path / "audit.sqlite"
    derived = tmp_path / "derived"
    derived.mkdir()
    init_db.initialize(db)
    with db_util.connect(db) as conn:
        db_util.insert(conn, "documents", {
            "doc_id": "DOC-0001", "filename": "source.txt", "title": "QA manual",
            "supplier": "enconet", "language": "en", "document_side": "DOCUMENT",
            "sha256": "a" * 64, "promoted_utc": "2026-07-12T00:00:00Z",
        })
        conn.commit()
    return db, derived


def test_parser_level_one_two_offsets_and_level_three_containment():
    text = "Preamble\n1. Scope\nAlpha\n1.1 Detail\nBeta\n1.1.1 Nested\nGamma\n2. Control\nDelta\n"
    chunks, warnings = chunk_document.parse_chunks(text)
    assert [chunk.heading_path for chunk in chunks] == ["1", "1 > 1.1", "2"]
    assert "1.1.1 Nested" in chunks[1].text
    assert warnings == []
    for chunk in chunks:
        assert text[chunk.char_start:chunk.char_end] == chunk.text


def test_whole_document_fallback_size_warning_and_rejections():
    chunks, warnings = chunk_document.parse_chunks("No numeric headings here", max_chars=5)
    assert chunks[0].heading_path == "whole-document"
    assert len(warnings) == 2
    assert "whole-document fallback" in warnings[0]
    assert "manual split required" in warnings[1]
    with pytest.raises(ValueError, match="empty document"):
        chunk_document.parse_chunks(" \n")
    with pytest.raises(ValueError, match="duplicate heading path: 1"):
        chunk_document.parse_chunks("1. First\ntext\n1. Repeated\ntext\n")


def test_writer_ids_offsets_and_atomic_replacement(project):
    db, derived = project
    text = "1. First\nA\n1.1 Child\nB\n2. Second\nC\n"
    (derived / "DOC-0001.txt").write_text(text, encoding="utf-8")
    count, warnings = chunk_document.write_chunks("DOC-0001", db_path=db, derived_root=derived)
    assert count == 3 and warnings == []
    with db_util.connect(db) as conn:
        rows = conn.execute("SELECT * FROM document_chunks ORDER BY chunk_id").fetchall()
    assert [row["chunk_id"] for row in rows] == [
        "CHUNK-DOC-0001-0001", "CHUNK-DOC-0001-0002", "CHUNK-DOC-0001-0003",
    ]
    assert all(text[row["char_start"]:row["char_end"]] == row["chunk_text"] for row in rows)

    replacement = "1. Replacement\nOnly one\n"
    (derived / "DOC-0001.txt").write_text(replacement, encoding="utf-8")
    assert chunk_document.write_chunks("DOC-0001", db_path=db, derived_root=derived)[0] == 1
    with db_util.connect(db) as conn:
        assert conn.execute("SELECT count(*) FROM document_chunks").fetchone()[0] == 1

    (derived / "DOC-0001.txt").write_text("1. A\ntext\n1. B\ntext\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate heading"):
        chunk_document.write_chunks("DOC-0001", db_path=db, derived_root=derived)
    with db_util.connect(db) as conn:
        row = conn.execute("SELECT chunk_text FROM document_chunks").fetchone()
    assert row[0] == replacement


def test_validator_detects_offset_checksum_and_orphan_and_logs(project, tmp_path: Path):
    db, derived = project
    text = "1. Heading\nEvidence\n"
    (derived / "DOC-0001.txt").write_text(text, encoding="utf-8")
    chunk_document.write_chunks("DOC-0001", db_path=db, derived_root=derived)
    assert validate_chunks.validate(db_path=db, derived_root=derived) == []

    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE document_chunks SET char_end = char_end - 1, source_sha256 = ?", ("b" * 64,))
        conn.execute(
            "INSERT INTO document_chunks VALUES (?,?,?,?,?,?,?)",
            ("CHUNK-DOC-9999-0001", "DOC-9999", "9", "orphan", 0, 6, "c" * 64),
        )
    errors = validate_chunks.validate(db_path=db, derived_root=derived)
    assert "offset slice mismatch: CHUNK-DOC-0001-0001" in errors
    assert "source checksum mismatch: CHUNK-DOC-0001-0001" in errors
    assert "orphan chunk: CHUNK-DOC-9999-0001" in errors

    manifest = tmp_path / "validation_runs.csv"
    manifest.write_text("run_utc,validator,phase,result,exit_code,details\n", encoding="utf-8")
    validate_chunks.append_result("FAIL", 1, "3 errors", manifest)
    with manifest.open(newline="", encoding="utf-8") as fh:
        row = list(csv.DictReader(fh))[0]
    assert row["validator"] == "validate_chunks.py"
    assert row["result"] == "FAIL" and row["exit_code"] == "1"
