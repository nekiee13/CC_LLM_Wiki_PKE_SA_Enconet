#!/usr/bin/env python3
"""Validate EPIC9 gap evidence pointers and missing-evidence action hooks."""
from __future__ import annotations
import argparse,csv,sys
from datetime import datetime,timezone
from pathlib import Path
import db_util
ENCONET=Path(__file__).resolve().parents[1];RUNS=ENCONET/"manifests"/"validation_runs.csv"
def validate(db:Path)->list[str]:
 errors=[];pattern=db_util.id_patterns()["gap_id"]
 with db_util.connect(db) as c:
  for g in c.execute("SELECT * FROM gaps"):
   if pattern.fullmatch(g["gap_id"]) is None:errors.append(f"invalid gap ID: {g['gap_id']}")
   if bool(g["evidence_item_id"])==bool(g["missing_evidence_ref"]):errors.append(f"gap evidence pointer invalid: {g['gap_id']}")
   if g["status"]=="missing-evidence":
    actions=c.execute("SELECT action_type FROM auditor_actions WHERE gap_id=?",(g["gap_id"],)).fetchall()
    if not actions:errors.append(f"missing-evidence gap without action: {g['gap_id']}")
    elif any(a[0] not in ("verification","document_request") for a in actions):errors.append(f"invalid missing-evidence action type: {g['gap_id']}")
  for row in c.execute("PRAGMA foreign_key_check"):errors.append(f"foreign key violation: {tuple(row)}")
 return errors
def append(result,code,details,path=RUNS):
 with path.open("a",newline="",encoding="utf-8") as f:csv.writer(f).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"validate_gaps.py","unknown",result,code,details])
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);a=p.parse_args()
 try:e=validate(a.db)
 except Exception as x:e=[str(x)]
 if e:append("FAIL",1,f"{len(e)} error(s); first: {e[0][:120]}");[print(f"validate_gaps: FAIL - {x}",file=sys.stderr) for x in e];return 1
 append("PASS",0,"all gaps have evidence pointers; missing-evidence gaps have actions");print("validate_gaps: PASS");return 0
if __name__=="__main__":raise SystemExit(main())
