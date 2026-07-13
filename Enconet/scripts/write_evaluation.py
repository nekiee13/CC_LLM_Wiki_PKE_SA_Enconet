#!/usr/bin/env python3
"""Write one human judgment through the EPIC8 evidence gate."""
import argparse,json,sys
from pathlib import Path
import db_util
from evaluation_engine import write_evaluation
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("record",type=Path);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);p.add_argument("--run-id",required=True);p.add_argument("--evidence",action="append",default=[]);p.add_argument("--auto-downgrade",action="store_true");a=p.parse_args()
 try:r=write_evaluation(a.db,run_id=a.run_id,record=json.loads(a.record.read_text(encoding="utf-8")),evidence_ids=a.evidence,auto_downgrade=a.auto_downgrade);print(f"write_evaluation: PASS - classification={r}");return 0
 except Exception as e:print(f"write_evaluation: FAIL - {e}",file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
