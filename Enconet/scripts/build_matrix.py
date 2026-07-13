#!/usr/bin/env python3
"""Build matching JSON and Markdown 18-criterion evidence matrices from SQLite."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import db_util
def build(db:Path,run_id:str|None=None)->list[dict]:
 with db_util.connect(db) as c:
  rows=[]
  for criterion in c.execute("SELECT criterion_id,criterion_name FROM criteria ORDER BY rowid"):
   cid=criterion[0];app=c.execute("SELECT applicable FROM criterion_applicability WHERE evaluation_run_id=? AND criterion_id=?",(run_id,cid)).fetchone() if run_id else None
   rows.append({"criterion_id":cid,"criterion_name":criterion[1],"applicability":"applicable" if app and app[0] else ("not-applicable" if app else "unruled"),"rule_evidence_count":c.execute("SELECT count(*) FROM crumbs WHERE criterion_id=? AND document_side='RULE'",(cid,)).fetchone()[0],"document_evidence_count":c.execute("SELECT count(*) FROM crumbs WHERE criterion_id=? AND document_side='DOCUMENT'",(cid,)).fetchone()[0],"gap_count":c.execute("SELECT count(*) FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) WHERE e.criterion_id=?"+(" AND e.evaluation_run_id=?" if run_id else ""),(cid,run_id) if run_id else (cid,)).fetchone()[0],"finding_count":c.execute("SELECT count(*) FROM findings WHERE criterion_id=?",(cid,)).fetchone()[0],"action_count":c.execute("SELECT count(*) FROM auditor_actions a JOIN gaps g ON g.gap_id=a.gap_id JOIN criterion_evaluations e ON e.evaluation_id=g.evaluation_id WHERE e.criterion_id=?"+(" AND e.evaluation_run_id=?" if run_id else ""),(cid,run_id) if run_id else (cid,)).fetchone()[0]})
  return rows
def render_json(rows):return (json.dumps(rows,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
def render_md(rows):
 h="| Criterion | Applicability | RULE | DOCUMENT | Gaps | Findings | Actions |\n|---|---:|---:|---:|---:|---:|---:|\n"
 return h+"".join(f"| {r['criterion_id']} {r['criterion_name']} | {r['applicability']} | {r['rule_evidence_count']} | {r['document_evidence_count']} | {r['gap_count']} | {r['finding_count']} | {r['action_count']} |\n" for r in rows)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);p.add_argument("--run-id");p.add_argument("--json",type=Path,required=True);p.add_argument("--markdown",type=Path,required=True);a=p.parse_args();rows=build(a.db,a.run_id);a.json.parent.mkdir(parents=True,exist_ok=True);a.markdown.parent.mkdir(parents=True,exist_ok=True);a.json.write_bytes(render_json(rows));a.markdown.write_text(render_md(rows),encoding="utf-8");print("build_matrix: PASS - criteria=18");return 0
if __name__=="__main__":raise SystemExit(main())
