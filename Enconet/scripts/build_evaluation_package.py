#!/usr/bin/env python3
"""Build the deterministic single-source EPIC8 evaluation package."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import db_util
from evaluation_engine import metrics
import yaml
SCHEMA=Path(__file__).resolve().parents[1]/"schemas"/"evaluation_package_schema.yml"
def validate_package(package:dict)->list[str]:
 schema=yaml.safe_load(SCHEMA.read_text(encoding="utf-8"));errors=[]
 for key in schema["required_top_level"]:
  if key not in package:errors.append(f"missing top-level field: {key}")
 if package.get("schema_version")!=schema["schema_version"]:errors.append("schema_version mismatch")
 evaluations=package.get("evaluations",[])
 if len(evaluations)!=schema["evaluation_count"]:errors.append(f"expected {schema['evaluation_count']} evaluations")
 for e in evaluations:
  if e.get("classification") not in schema["ratings"]:errors.append(f"invalid classification: {e.get('classification')}")
 if evaluations and package.get("metrics")!=metrics([{"rating":e["classification"]} for e in evaluations]):errors.append("metrics do not recompute")
 return errors
def build(db:Path,run_id:str)->dict:
 with db_util.connect(db) as c:
  run=dict(c.execute("SELECT * FROM evaluation_runs WHERE run_id=?",(run_id,)).fetchone() or {})
  applicability=[dict(r) for r in c.execute("SELECT * FROM criterion_applicability WHERE evaluation_run_id=? ORDER BY criterion_id",(run_id,))]
  evaluations=[]
  for row in c.execute("SELECT e.*,c.criterion_name FROM criterion_evaluations e JOIN criteria c USING(criterion_id) WHERE evaluation_run_id=? ORDER BY criterion_id",(run_id,)):
   item=dict(row);item["classification"]=item.pop("rating");item["evidence_ids"]=[x[0] for x in c.execute("SELECT item_id FROM evaluation_evidence WHERE evaluation_id=? ORDER BY item_id",(item["evaluation_id"],))];evaluations.append(item)
  gaps=[dict(r) for r in c.execute("SELECT g.* FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) WHERE e.evaluation_run_id=? ORDER BY gap_id",(run_id,))]
  actions=[dict(r) for r in c.execute("SELECT a.* FROM auditor_actions a LEFT JOIN gaps g ON g.gap_id=a.gap_id LEFT JOIN criterion_evaluations e ON e.evaluation_id=g.evaluation_id WHERE e.evaluation_run_id=? ORDER BY action_id",(run_id,))]
 return {"schema_version":"1.0","run":run,"applicability":applicability,"evaluations":evaluations,"metrics":metrics([{"rating":e["classification"]} for e in evaluations]),"gaps":gaps,"actions":actions}
def render(package:dict)->bytes:
 errors=validate_package(package)
 if errors:raise ValueError("invalid evaluation package: "+"; ".join(errors))
 return (json.dumps(package,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);p.add_argument("--run-id",required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(render(build(a.db,a.run_id)));print(f"build_evaluation_package: PASS - {a.output}");return 0
if __name__=="__main__":raise SystemExit(main())
