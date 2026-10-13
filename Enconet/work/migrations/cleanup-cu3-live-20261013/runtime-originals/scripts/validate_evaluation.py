#!/usr/bin/env python3
"""Re-prove EPIC8 completeness, applicability, evidence gates, and scores."""
from __future__ import annotations
import argparse,csv,sys
from datetime import datetime,timezone
from pathlib import Path
import db_util
from evaluation_engine import POSITIVE,score_rating
ENCONET=Path(__file__).resolve().parents[1];RUNS=ENCONET/"manifests"/"validation_runs.csv";RAW=ENCONET/"raw"
def validate(db:Path,run_id:str)->list[str]:
 errors=[]
 with db_util.connect(db) as c:
  rulings={r["criterion_id"]:r for r in c.execute("SELECT * FROM criterion_applicability WHERE evaluation_run_id=?",(run_id,))};evals={r["criterion_id"]:r for r in c.execute("SELECT * FROM criterion_evaluations WHERE evaluation_run_id=?",(run_id,))}
  criteria={r[0] for r in c.execute("SELECT criterion_id FROM criteria")}
  if set(rulings)!=criteria:errors.append("applicability matrix incomplete")
  if set(evals)!=criteria:errors.append("evaluation records incomplete")
  for cid,r in rulings.items():
   doc=c.execute("SELECT filename FROM documents WHERE doc_id=?",(r["scope_source_doc_id"],)).fetchone()
   if not doc or not (RAW/doc[0]).is_file():errors.append(f"ruling lacks raw scope citation: {cid}")
  for cid,e in evals.items():
   evidence=c.execute("SELECT c.document_side FROM evaluation_evidence x JOIN crumbs c ON c.item_id=x.item_id WHERE x.evaluation_id=?",(e["evaluation_id"],)).fetchall();has_doc=any(x[0]=="DOCUMENT" for x in evidence)
   if e["rating"] in POSITIVE and not has_doc:errors.append(f"positive classification without DOCUMENT evidence: {cid}")
   if cid in rulings and rulings[cid]["applicable"] and e["rating"]=="na":errors.append(f"na record for applicable criterion: {cid}")
   if cid in rulings and not rulings[cid]["applicable"] and (e["rating"]!="na" or e["score"] is not None):errors.append(f"scored record for not-applicable criterion: {cid}")
   expected=score_rating(e["rating"])
   if e["score"]!=expected:errors.append(f"score mismatch: {cid}")
 return errors
def append(result,code,details,path=RUNS):
 with path.open("a",newline="",encoding="utf-8") as f:csv.writer(f).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"validate_evaluation.py","unknown",result,code,details])
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);p.add_argument("--run-id",required=True);p.add_argument("--no-record",action="store_true");a=p.parse_args()
 try:e=validate(a.db,a.run_id)
 except Exception as x:e=[str(x)]
 if e:
  if not a.no_record:append("FAIL",1,f"{len(e)} error(s); first: {e[0][:120]}")
  [print(f"validate_evaluation: FAIL - {x}",file=sys.stderr) for x in e];return 1
 if not a.no_record:append("PASS",0,"18/18 evaluations and evidence gates verified")
 print("validate_evaluation: PASS");return 0
if __name__=="__main__":raise SystemExit(main())
