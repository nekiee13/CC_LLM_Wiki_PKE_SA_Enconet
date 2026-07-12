"""EPIC3 raw intake, registry, extraction, and immutability tests."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import db_util  # noqa: E402
import extract_text  # noqa: E402
import init_db  # noqa: E402
import promote_source  # noqa: E402
import source_registry  # noqa: E402
import validate_raw_sources  # noqa: E402


@pytest.fixture
def intake(tmp_path: Path, monkeypatch):
    incoming, raw, derived = (tmp_path / name for name in ("incoming", "raw", "derived"))
    for path in (incoming, raw, derived):
        path.mkdir()
    manifest = tmp_path / "raw_sources.csv"
    with manifest.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(source_registry.HEADER)
    db = tmp_path / "audit.sqlite"
    init_db.initialize(db)
    monkeypatch.setattr(source_registry, "RAW", raw)
    monkeypatch.setattr(promote_source, "RAW", raw)
    monkeypatch.setattr(promote_source, "ENCONET", tmp_path)
    return incoming, raw, derived, manifest, db


def metadata(manifest: Path, db: Path) -> dict:
    return dict(db_path=db, title="Supplier QA", supplier="enconet", doc_date="2026-07-12",
                language="en", side_hint="DOCUMENT", source_url="n-a", notes="reviewed",
                manifest_path=manifest)


def test_promotion_registers_identical_checksum_and_locks_source(intake):
    incoming, raw, _, manifest, db = intake
    source = incoming / "supplier.txt"
    source.write_text("Controlled quality evidence", encoding="utf-8")
    doc_id = promote_source.promote(source, **metadata(manifest, db))
    assert doc_id == "DOC-0001"
    promoted = raw / source.name
    assert promoted.is_file() and not source.exists()
    assert source_registry.is_write_locked(promoted)
    row = source_registry.read_manifest(manifest)[0]
    with db_util.connect(db) as conn:
        db_row = db_util.lookup(conn, "documents", "doc_id", doc_id)
    assert row["sha256"] == db_row["sha256"] == source_registry.sha256_file(promoted)
    assert row["title"] == db_row["title"]
    assert row["side_hint"] == db_row["document_side"]


def test_duplicate_filename_and_checksum_are_rejected(intake):
    incoming, raw, _, manifest, db = intake
    first = incoming / "same.txt"
    first.write_text("same bytes", encoding="utf-8")
    promote_source.promote(first, **metadata(manifest, db))
    duplicate_name = incoming / "same.txt"
    duplicate_name.write_text("different", encoding="utf-8")
    with pytest.raises(FileExistsError, match="duplicate raw filename"):
        promote_source.promote(duplicate_name, **metadata(manifest, db))
    duplicate_hash = raw / "copy.txt"
    duplicate_hash.write_text("same bytes", encoding="utf-8")
    with pytest.raises(ValueError, match="checksum already registered"):
        source_registry.register(duplicate_hash, **metadata(manifest, db))


def test_text_extraction_records_method_and_rejects_empty(intake):
    incoming, raw, derived, manifest, db = intake
    source = incoming / "document.txt"
    source.write_text("Reviewable text\n", encoding="utf-8")
    doc_id = promote_source.promote(source, **metadata(manifest, db))
    output = extract_text.extract(doc_id, db_path=db, raw_root=raw, derived_root=derived)
    assert output.name == "DOC-0001.txt"
    assert output.read_text(encoding="utf-8") == "Reviewable text\n"
    with db_util.connect(db) as conn:
        row = db_util.lookup(conn, "documents", "doc_id", doc_id)
        assert row["extraction_method"] == "utf-8-text:txt"
        assert row["extracted_at"]

    empty = incoming / "empty.txt"
    empty.write_text("  \n", encoding="utf-8")
    empty_id = promote_source.promote(empty, **metadata(manifest, db))
    with pytest.raises(ValueError, match="empty extraction output"):
        extract_text.extract(empty_id, db_path=db, raw_root=raw, derived_root=derived)


def test_validator_names_tamper_unregistered_and_missing(intake):
    incoming, raw, _, manifest, db = intake
    source = incoming / "registered.txt"
    source.write_text("original", encoding="utf-8")
    promote_source.promote(source, **metadata(manifest, db))
    assert validate_raw_sources.validate(db_path=db, raw_root=raw, manifest_path=manifest) == []

    registered = raw / "registered.txt"
    registered.chmod(0o600)
    registered.write_text("tampered", encoding="utf-8")
    (raw / "extra.txt").write_text("extra", encoding="utf-8")
    errors = validate_raw_sources.validate(db_path=db, raw_root=raw, manifest_path=manifest)
    assert "checksum mismatch: registered.txt" in errors
    assert "raw file is writable: registered.txt" in errors
    assert "unregistered raw file: extra.txt" in errors

    registered.unlink()
    errors = validate_raw_sources.validate(db_path=db, raw_root=raw, manifest_path=manifest)
    assert "registered raw file missing: registered.txt" in errors
