"""EPIC6 migration, linking, exceptions, and traceability validation tests."""
from __future__ import annotations

import csv, hashlib, sqlite3, sys
from pathlib import Path
import pytest

ENCONET=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ENCONET/"scripts"))
import db_util, init_db, link_crumbs, migrate_db, validate_traceability  # noqa: E402


def _legacy(db: Path) -> None:
    init_db.initialize(db)
    with sqlite3.connect(db) as c:
        c.execute("DROP TABLE crumb_chunk_links"); c.execute("DROP TABLE crumb_authority_refs"); c.execute("DROP TABLE sieve_run_authorities")
        c.execute("CREATE TABLE crumb_chunk_links(item_id TEXT NOT NULL REFERENCES crumbs(item_id), chunk_id TEXT NOT NULL REFERENCES document_chunks(chunk_id), link_method TEXT NOT NULL, confidence REAL, PRIMARY KEY(item_id,chunk_id))")
        c.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) VALUES('DOC-0001','x','x','x','en','RULE',?)",("a"*64,))


def test_migration_dry_run_backup_and_apply(tmp_path: Path):
    db=tmp_path/"legacy.sqlite"; _legacy(db); before=hashlib.sha256(db.read_bytes()).hexdigest()
    actions, backup=migrate_db.migrate(db,apply=False,backup_dir=tmp_path/"backups")
    assert len(actions)==3 and backup is None and hashlib.sha256(db.read_bytes()).hexdigest()==before
    actions, backup=migrate_db.migrate(db,apply=True,backup_dir=tmp_path/"backups")
    assert backup and backup.is_file()
    with sqlite3.connect(db) as c:
        assert c.execute("SELECT count(*) FROM documents").fetchone()[0]==1
        assert "quote_id" in {r[1] for r in c.execute("PRAGMA table_info(crumb_chunk_links)")}
        assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"


def test_migration_failure_restores_backup_byte_for_byte(tmp_path: Path, monkeypatch):
    db=tmp_path/"legacy.sqlite"; _legacy(db)
    broken=tmp_path/"broken-schema.sql"; broken.write_text("THIS IS NOT SQL;",encoding="utf-8")
    monkeypatch.setattr(migrate_db,"SCHEMA",broken)
    with pytest.raises(sqlite3.Error):
        migrate_db.migrate(db,apply=True,backup_dir=tmp_path/"backups")
    backup=next((tmp_path/"backups").glob("*.sqlite.bak"))
    assert hashlib.sha256(db.read_bytes()).hexdigest()==hashlib.sha256(backup.read_bytes()).hexdigest()
    with sqlite3.connect(db) as c:
        assert c.execute("SELECT count(*) FROM documents").fetchone()[0]==1
        assert "quote_id" not in {r[1] for r in c.execute("PRAGMA table_info(crumb_chunk_links)")}


@pytest.fixture
def traced(tmp_path: Path):
    db=tmp_path/"trace.sqlite"; init_db.initialize(db)
    exceptions=tmp_path/"exceptions.csv"; exceptions.write_text("crumb_id,quote_id,reason,approved_by,date\n",encoding="utf-8")
    candidates=tmp_path/"candidates.csv"
    with db_util.connect(db) as c:
        db_util.insert(c,"documents",{"doc_id":"DOC-0001","filename":"x","title":"x","supplier":"x","language":"en","document_side":"RULE","sha256":"a"*64})
        db_util.insert(c,"sieve_runs",{"run_id":"RUN-20260713-01","doc_id":"DOC-0001","prompt_version":"v1","document_side":"RULE","source_rule":"10CFR50_APPB"})
        db_util.insert(c,"document_chunks",{"chunk_id":"CHUNK-DOC-0001-0001","doc_id":"DOC-0001","heading_path":"1","chunk_text":"The QA system shall control design inputs.","char_start":0,"char_end":42,"source_sha256":"a"*64})
        db_util.insert(c,"crumbs",{"item_id":"CRUMB-DOC-0001-APP_B_III-0001","doc_id":"DOC-0001","sieve_run_id":"RUN-20260713-01","criterion_id":"APP_B_III","document_side":"RULE","statement":"control inputs"})
        db_util.insert(c,"crumb_quotes",{"quote_id":"QUOTE-DOC-0001-0001-01","item_id":"CRUMB-DOC-0001-APP_B_III-0001","quote_original":"QA system  shall control\ndesign inputs","quote_language":"en","source_locator":"1"})
    return db,exceptions,candidates


def test_normalized_link_and_traceability_pass(traced):
    db,exceptions,candidates=traced; count,unmatched=link_crumbs.link(db,candidates_path=candidates)
    assert count==1 and unmatched==[]
    with db_util.connect(db) as c: assert c.execute("SELECT link_method FROM crumb_chunk_links").fetchone()[0]=="NORMALIZED"
    assert validate_traceability.validate(db,exceptions_path=exceptions)==[]


def test_unmatched_requires_complete_approved_exception(traced):
    db,exceptions,candidates=traced
    with db_util.connect(db) as c: c.execute("UPDATE crumb_quotes SET quote_original='OCR variant not present'")
    _,unmatched=link_crumbs.link(db,candidates_path=candidates); assert len(unmatched)==1
    errors=validate_traceability.validate(db,exceptions_path=exceptions); assert any("without link" in e for e in errors)
    with exceptions.open("a",newline="",encoding="utf-8") as fh:
        csv.writer(fh).writerow(["CRUMB-DOC-0001-APP_B_III-0001","QUOTE-DOC-0001-0001-01","OCR variance","owner","2026-07-13"])
    assert validate_traceability.validate(db,exceptions_path=exceptions)==[]
