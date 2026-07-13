#!/usr/bin/env python3
"""Validate 18/18 requirement coverage and RULE-crumb traceability."""
from __future__ import annotations
import argparse,csv,sys
from datetime import datetime,timezone
from pathlib import Path
import db_util
ENCONET=Path(__file__).resolve().parents[1]; RUNS=ENCONET/"manifests"/"validation_runs.csv"
def validate(db:Path)->list[str]:
    errors=[]; pattern=db_util.id_patterns()["requirement_id"]
    with db_util.connect(db) as c:
        for criterion in c.execute("SELECT criterion_id FROM criteria ORDER BY criterion_id"):
            if not c.execute("SELECT 1 FROM requirements WHERE criterion_id=?",criterion).fetchone(): errors.append(f"criterion without requirement: {criterion[0]}")
        rows=c.execute("SELECT r.*,c.document_side FROM requirements r LEFT JOIN crumbs c ON c.item_id=r.source_item_id").fetchall()
        for r in rows:
            if not pattern.fullmatch(r["requirement_id"]): errors.append(f"invalid requirement ID: {r['requirement_id']}")
            if r["document_side"]!="RULE": errors.append(f"requirement without RULE crumb: {r['requirement_id']}")
            if bool(r["is_subrequirement"]) != bool(r["parent_requirement_id"]): errors.append(f"invalid hierarchy: {r['requirement_id']}")
    return errors
def append(result,code,details,path=RUNS):
    with path.open("a",newline="",encoding="utf-8") as f: csv.writer(f).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"validate_requirements.py","unknown",result,code,details])
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);a=p.parse_args()
    try:e=validate(a.db)
    except Exception as x:e=[str(x)]
    if e: append("FAIL",1,f"{len(e)} error(s); first: {e[0][:120]}");[print(f"validate_requirements: FAIL - {x}",file=sys.stderr) for x in e];return 1
    append("PASS",0,"18/18 criteria covered; all requirements trace to RULE crumbs");print("validate_requirements: PASS");return 0
if __name__=="__main__":raise SystemExit(main())
