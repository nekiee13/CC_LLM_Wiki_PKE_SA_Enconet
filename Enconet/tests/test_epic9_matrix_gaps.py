"""EPIC9 matrix, gap register, action rule, and validator tests."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ENCONET=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ENCONET/"scripts"))
import build_matrix,db_util,gap_register,init_db,validate_gaps  # noqa:E402
@pytest.fixture
def audit(tmp_path:Path):
 db=tmp_path/"audit.sqlite";init_db.initialize(db)
 with db_util.connect(db) as c:
  db_util.insert(c,"documents",{"doc_id":"DOC-0001","filename":"x","title":"x","supplier":"x","language":"en","document_side":"RULE","sha256":"a"*64})
  db_util.insert(c,"sieve_runs",{"run_id":"RUN-20260713-01","doc_id":"DOC-0001","prompt_version":"v","document_side":"RULE","source_rule":"10CFR50_APPB"})
  db_util.insert(c,"crumbs",{"item_id":"CRUMB-DOC-0001-APP_B_I-0001","doc_id":"DOC-0001","sieve_run_id":"RUN-20260713-01","criterion_id":"APP_B_I","document_side":"RULE","statement":"rule"})
  db_util.insert(c,"evaluation_runs",{"run_id":"RUN-20260713-02","supplier":"x","deliverable_language":"en","scoring_model_version":"test"})
  db_util.insert(c,"criterion_evaluations",{"evaluation_id":"EVAL-APP_B_I","evaluation_run_id":"RUN-20260713-02","criterion_id":"APP_B_I","rating":"undetermined","score":0,"coverage":0,"completeness":0,"accuracy":0,"clarity":0,"alignment":0,"evidence_supported":0,"affirmative_summary":"","contrary_summary":"","judge_ruling":"x","rationale":"x"})
 return db
def test_matrix_has_18_rows_and_matching_renderers(audit):
 rows=build_matrix.build(audit,"RUN-20260713-02");assert len(rows)==18 and rows[0]["rule_evidence_count"]==1
 assert len(build_matrix.render_json(rows))>0 and build_matrix.render_md(rows).count("\n")==20
def test_missing_evidence_gap_automatically_creates_action(audit):
 aid=gap_register.write_gap(audit,{"gap_id":"GAP-APP_B_I-01","evaluation_id":"EVAL-APP_B_I","status":"missing-evidence","description":"Need procedure","missing_evidence_ref":"supplier procedure document"})
 assert aid=="ACT-0001" and validate_gaps.validate(audit)==[]
 with db_util.connect(audit) as c:c.execute("DELETE FROM auditor_actions")
 assert "missing-evidence gap without action: GAP-APP_B_I-01" in validate_gaps.validate(audit)
def test_gap_requires_exactly_one_pointer(audit):
 with pytest.raises(ValueError,match="exactly one"):
  gap_register.write_gap(audit,{"gap_id":"GAP-APP_B_I-01","evaluation_id":"EVAL-APP_B_I","status":"undetermined","description":"x"})

def test_action_id_uses_max_not_count(audit):
 assert gap_register.write_gap(audit,{"gap_id":"GAP-APP_B_I-01","evaluation_id":"EVAL-APP_B_I","status":"missing-evidence","description":"first","missing_evidence_ref":"record"})=="ACT-0001"
 gap_register.write_gap(audit,{"gap_id":"GAP-APP_B_I-02","evaluation_id":"EVAL-APP_B_I","status":"undetermined","description":"weak","evidence_item_id":"CRUMB-DOC-0001-APP_B_I-0001"})
 with db_util.connect(audit) as c:
  db_util.insert(c,"auditor_actions",{"action_id":"ACT-0002","evaluation_run_id":"RUN-20260713-02","gap_id":"GAP-APP_B_I-02","action_type":"verification","description":"verify weak evidence"})
  c.execute("DELETE FROM auditor_actions WHERE action_id='ACT-0001'")
 assert gap_register.write_gap(audit,{"gap_id":"GAP-APP_B_I-03","evaluation_id":"EVAL-APP_B_I","status":"missing-evidence","description":"third","missing_evidence_ref":"record"})=="ACT-0003"
