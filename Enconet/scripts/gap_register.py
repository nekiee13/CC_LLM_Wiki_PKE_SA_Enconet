#!/usr/bin/env python3
"""Write one EPIC9 gap and automatically hook missing evidence to an action."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import db_util
STATUSES={"covered","mostly-covered","partially-covered","minimally-covered","not-covered","not-applicable","undetermined","missing-evidence"}
def write_gap(db:Path,record:dict)->str|None:
 with db_util.connect(db) as c:
  if record["status"] not in STATUSES:raise ValueError("invalid gap status")
  if db_util.id_patterns()["gap_id"].fullmatch(record["gap_id"]) is None:raise ValueError("invalid gap ID")
  evidence=record.get("evidence_item_id");missing=record.get("missing_evidence_ref")
  if bool(evidence)==bool(missing):raise ValueError("exactly one weak/missing evidence pointer required")
  if evidence and not db_util.exists(c,"crumbs","item_id",evidence):raise ValueError("unknown evidence crumb")
  db_util.insert(c,"gaps",{"gap_id":record["gap_id"],"evaluation_id":record["evaluation_id"],"status":record["status"],"description":record["description"],"evidence_item_id":evidence,"missing_evidence_ref":missing})
  if record["status"]!="missing-evidence":return None
  action_type=record.get("action_type") or ("document_request" if "document" in missing.casefold() else "verification")
  if action_type not in {"verification","document_request"}:raise ValueError("missing-evidence action must be verification or document_request")
  existing=[int(r[0].split("-")[1]) for r in c.execute("SELECT action_id FROM auditor_actions")]
  aid=f"ACT-{max(existing,default=0)+1:04d}"
  db_util.insert(c,"auditor_actions",{"action_id":aid,"gap_id":record["gap_id"],"action_type":action_type,"description":record.get("action_description") or f"Resolve {missing}"})
  return aid
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("record",type=Path);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);a=p.parse_args()
 try:aid=write_gap(a.db,json.loads(a.record.read_text(encoding="utf-8")));print(f"gap_register: PASS - action={aid or 'not-required'}");return 0
 except Exception as e:print(f"gap_register: FAIL - {e}",file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
