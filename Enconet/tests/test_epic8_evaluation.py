"""EPIC8 gates, evidence invariants, scoring, package, and validator tests."""
from __future__ import annotations
import csv,sys
from pathlib import Path
import pytest
ENCONET=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ENCONET/"scripts"))
import build_evaluation_package,db_util,evaluation_engine,init_db,validate_evaluation  # noqa:E402

@pytest.fixture
def evaluated(tmp_path:Path):
 db=tmp_path/"audit.sqlite";init_db.initialize(db);approvals=tmp_path/"approvals.csv"
 approvals.write_text("object_id,decision,date,reviewer,notes\nG2-RUN-20260713-02,approved,2026-07-13,owner,test\n",encoding="utf-8")
 with db_util.connect(db) as c:
  db_util.insert(c,"documents",{"doc_id":"DOC-0019","filename":"Title_10_CFR_Part_50_-_Appendix_B.md","title":"scope","supplier":"NRC","language":"en","document_side":"RULE","sha256":"a"*64})
  db_util.insert(c,"documents",{"doc_id":"DOC-0001","filename":"NQA-1_REQ_02_-_Quality_Assurance_Program.md","title":"evidence","supplier":"Enconet","language":"en","document_side":"DOCUMENT","sha256":"b"*64})
  db_util.insert(c,"sieve_runs",{"run_id":"RUN-20260713-01","doc_id":"DOC-0001","prompt_version":"v1","document_side":"DOCUMENT","source_rule":None})
  db_util.insert(c,"crumbs",{"item_id":"CRUMB-DOC-0001-APP_B_I-0001","doc_id":"DOC-0001","sieve_run_id":"RUN-20260713-01","criterion_id":"APP_B_I","document_side":"DOCUMENT","statement":"evidence"})
 with db_util.connect(db) as c:criteria=[r[0] for r in c.execute("SELECT criterion_id FROM criteria ORDER BY criterion_id")]
 rulings=[{"criterion_id":cid,"applicable":cid!="APP_B_XVIII","justification":"Scope source DOC-0019","scope_source_doc_id":"DOC-0019"} for cid in criteria]
 evaluation_engine.write_rulings(db,run_id="RUN-20260713-02",supplier="enconet",language="en",rulings=rulings,approvals=approvals)
 base={"coverage":0,"completeness":0,"accuracy":0,"clarity":0,"alignment":0,"affirmative_summary":"none","contrary_summary":"none","judge_ruling":"human ruling","rationale":"test"}
 for cid in criteria:
  rating="fully" if cid=="APP_B_I" else ("na" if cid=="APP_B_XVIII" else "undetermined")
  evaluation_engine.write_evaluation(db,run_id="RUN-20260713-02",record={**base,"criterion_id":cid,"classification":rating},evidence_ids=["CRUMB-DOC-0001-APP_B_I-0001"] if cid=="APP_B_I" else [])
 return db,approvals

def test_gate_and_positive_evidence_refuse(tmp_path:Path):
 db=tmp_path/"x.sqlite";init_db.initialize(db)
 with pytest.raises(ValueError,match="Gate G2"):
  evaluation_engine.write_rulings(db,run_id="RUN-20260713-02",supplier="x",language="en",rulings=[],approvals=tmp_path/"missing.csv")

def test_evaluation_validator_scores_and_stable_package(evaluated):
 db,_=evaluated;assert validate_evaluation.validate(db,"RUN-20260713-02")==[]
 package=build_evaluation_package.build(db,"RUN-20260713-02")
 assert len(package["evaluations"])==18 and package["metrics"]["applicable_count"]==17
 assert package["metrics"]["classification_counts"]["na"]==1
 assert build_evaluation_package.render(package)==build_evaluation_package.render(build_evaluation_package.build(db,"RUN-20260713-02"))
 assert build_evaluation_package.validate_package(package)==[]
 broken=dict(package);broken.pop("actions")
 assert "missing top-level field: actions" in build_evaluation_package.validate_package(broken)

def test_positive_without_document_evidence_and_ruling_change_refused(evaluated):
 db,_=evaluated
 with db_util.connect(db) as c:
  with pytest.raises(Exception,match="delete affected evaluation"):
   c.execute("UPDATE criterion_applicability SET applicable=0 WHERE evaluation_run_id='RUN-20260713-02' AND criterion_id='APP_B_I'")
 with db_util.connect(db) as c:c.execute("DELETE FROM criterion_evaluations WHERE criterion_id='APP_B_II'")
 record={"criterion_id":"APP_B_II","classification":"fully","judge_ruling":"x","rationale":"x"}
 with pytest.raises(ValueError,match="DOCUMENT crumb"):
  evaluation_engine.write_evaluation(db,run_id="RUN-20260713-02",record=record,evidence_ids=[])
 assert evaluation_engine.write_evaluation(db,run_id="RUN-20260713-02",record=record,evidence_ids=[],auto_downgrade=True)=="undetermined"

def test_validator_rejects_tampered_na_on_applicable_criterion(evaluated):
 db,_=evaluated
 with db_util.connect(db) as c:c.execute("UPDATE criterion_evaluations SET rating='na',score=NULL WHERE criterion_id='APP_B_I'")
 assert "na record for applicable criterion: APP_B_I" in validate_evaluation.validate(db,"RUN-20260713-02")
