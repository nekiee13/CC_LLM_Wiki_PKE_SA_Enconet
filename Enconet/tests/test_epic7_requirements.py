"""EPIC7 deterministic Appendix B ingestion and registry tests."""
from __future__ import annotations
import shutil,sys
from pathlib import Path
import pytest
ENCONET=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ENCONET/"scripts"))
import db_util,ingest_appendix_b,init_db,validate_chunks,validate_requirements,validate_traceability  # noqa:E402

@pytest.fixture
def registry(tmp_path:Path):
    db=tmp_path/"audit.sqlite";derived=tmp_path/"derived";derived.mkdir();init_db.initialize(db)
    shutil.copy2(ENCONET/"derived"/"DOC-0019.txt",derived/"DOC-0019.txt")
    with db_util.connect(db) as c: db_util.insert(c,"documents",{"doc_id":"DOC-0019","filename":"Title_10_CFR_Part_50_-_Appendix_B.md","title":"Appendix B","supplier":"NRC","language":"en","document_side":"RULE","sha256":"a"*64})
    assert ingest_appendix_b.ingest(db,derived_root=derived)==18
    exceptions=tmp_path/"exceptions.csv";exceptions.write_text("crumb_id,quote_id,reason,approved_by,date\n",encoding="utf-8")
    return db,exceptions,derived

def test_ingestion_covers_all_criteria_and_traceability(registry):
    db,exceptions,derived=registry
    with db_util.connect(db) as c:
        assert c.execute("SELECT count(*) FROM document_chunks").fetchone()[0]==18
        assert c.execute("SELECT count(*) FROM crumbs").fetchone()[0]==18
        assert c.execute("SELECT count(*) FROM requirements").fetchone()[0]==18
        assert c.execute("SELECT count(distinct criterion_id) FROM requirements").fetchone()[0]==18
        assert c.execute("SELECT count(*) FROM crumb_chunk_links").fetchone()[0]==18
    assert validate_requirements.validate(db)==[]
    assert validate_traceability.validate(db,exceptions_path=exceptions)==[]
    assert validate_chunks.validate(db_path=db,derived_root=derived)==[]

def test_requirement_validator_fails_missing_criterion_and_non_rule_link(registry):
    db,_,_=registry
    with db_util.connect(db) as c: c.execute("DELETE FROM requirements WHERE criterion_id='APP_B_XVIII'")
    assert "criterion without requirement: APP_B_XVIII" in validate_requirements.validate(db)
