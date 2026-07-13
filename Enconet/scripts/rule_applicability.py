#!/usr/bin/env python3
"""Import a human-approved 18-criterion applicability matrix."""
import argparse,json,sys
from pathlib import Path
import db_util
from evaluation_engine import write_rulings
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("matrix",type=Path);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);p.add_argument("--run-id",required=True);p.add_argument("--supplier",required=True);p.add_argument("--language",required=True);a=p.parse_args()
 try:write_rulings(a.db,run_id=a.run_id,supplier=a.supplier,language=a.language,rulings=json.loads(a.matrix.read_text(encoding="utf-8")));print("rule_applicability: PASS");return 0
 except Exception as e:print(f"rule_applicability: FAIL - {e}",file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
