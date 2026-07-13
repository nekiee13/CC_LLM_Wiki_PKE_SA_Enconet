"""Shared fail-closed EPIC8 evaluation operations."""
from __future__ import annotations
import csv,json
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
import yaml
import db_util
ENCONET=Path(__file__).resolve().parents[1]; APPROVALS=ENCONET/"manifests"/"approvals.csv"; MODEL=ENCONET/"schemas"/"scoring_model.yml"; RAW=ENCONET/"raw"
POSITIVE={"fully","substantially"}; RATINGS={"fully","substantially","partially","minimally","unmet","undetermined","na"}
def approval(run_id:str,path:Path=APPROVALS)->dict|None:
    if not path.is_file(): return None
    with path.open(newline="",encoding="utf-8-sig") as f:
        return next((r for r in csv.DictReader(f) if r["object_id"]==f"G2-{run_id}" and r["decision"].lower()=="approved"),None)
def write_rulings(db:Path,*,run_id:str,supplier:str,language:str,rulings:list[dict],approvals:Path=APPROVALS)->None:
    a=approval(run_id,approvals)
    if not a: raise ValueError("Gate G2 approval missing")
    with db_util.connect(db) as c:
        criteria=[r[0] for r in c.execute("SELECT criterion_id FROM criteria ORDER BY criterion_id")]
        if sorted(r["criterion_id"] for r in rulings)!=sorted(criteria) or len(rulings)!=18: raise ValueError("exactly one ruling for each of 18 criteria required")
        db_util.insert(c,"evaluation_runs",{"run_id":run_id,"supplier":supplier,"deliverable_language":language,"scoring_model_version":model()["model_version"]})
        for r in rulings:
            doc=db_util.lookup(c,"documents","doc_id",r["scope_source_doc_id"])
            if doc is None or not (RAW/doc["filename"]).is_file(): raise ValueError(f"scope citation is not a raw document: {r['scope_source_doc_id']}")
            db_util.insert(c,"criterion_applicability",{"evaluation_run_id":run_id,"criterion_id":r["criterion_id"],"applicable":int(r["applicable"]),"justification":r["justification"],"scope_source_doc_id":r["scope_source_doc_id"],"approved_by":a["reviewer"],"approved_date":a["date"],"decision_ref":f"G2-{run_id}"})
def model()->dict:return yaml.safe_load(MODEL.read_text(encoding="utf-8"))
def score_rating(rating:str)->float|None:
    w=model()["rating_weights"][rating];return None if w is None else float(Decimal(str(100*w)).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP))
def write_evaluation(db:Path,*,run_id:str,record:dict,evidence_ids:list[str],auto_downgrade:bool=False)->str:
    cid=record["criterion_id"]
    with db_util.connect(db) as c:
        ruling=c.execute("SELECT * FROM criterion_applicability WHERE evaluation_run_id=? AND criterion_id=?",(run_id,cid)).fetchone()
        if not ruling: raise ValueError("approved applicability ruling missing")
        rating=record["classification"]
        if rating not in RATINGS: raise ValueError("invalid classification")
        if not ruling["applicable"] and rating!="na": raise ValueError("not-applicable criterion requires minimal na record")
        if ruling["applicable"] and rating=="na": raise ValueError("applicable criterion cannot be na")
        document_evidence=[]
        for item in evidence_ids:
            row=c.execute("SELECT document_side FROM crumbs WHERE item_id=?",(item,)).fetchone()
            if not row: raise ValueError(f"unknown evidence crumb: {item}")
            if row[0]=="DOCUMENT": document_evidence.append(item)
        downgraded=False
        if rating in POSITIVE and not document_evidence:
            if not auto_downgrade: raise ValueError("positive classification requires linked DOCUMENT crumb")
            rating="undetermined";downgraded=True
        eid=f"EVAL-{cid}"
        db_util.insert(c,"criterion_evaluations",{"evaluation_id":eid,"evaluation_run_id":run_id,"criterion_id":cid,"rating":rating,"score":score_rating(rating),"coverage":record.get("coverage",0),"completeness":record.get("completeness",0),"accuracy":record.get("accuracy",0),"clarity":record.get("clarity",0),"alignment":record.get("alignment",0),"evidence_supported":int(bool(document_evidence)),"affirmative_summary":record.get("affirmative_summary","") ,"contrary_summary":record.get("contrary_summary","") ,"judge_ruling":record.get("judge_ruling","") ,"rationale":record.get("rationale","")})
        for item in evidence_ids: db_util.insert(c,"evaluation_evidence",{"evaluation_id":eid,"item_id":item})
        if downgraded:
            gap_id=f"GAP-{cid}-01"
            db_util.insert(c,"gaps",{"gap_id":gap_id,"evaluation_id":eid,"status":"missing-evidence","description":"Positive classification downgraded: no linked DOCUMENT evidence","missing_evidence_ref":"linked supplier DOCUMENT crumb"})
            existing=[int(r[0].split("-")[1]) for r in c.execute("SELECT action_id FROM auditor_actions")]
            db_util.insert(c,"auditor_actions",{"action_id":f"ACT-{max(existing,default=0)+1:04d}","gap_id":gap_id,"action_type":"document_request","description":"Obtain linked supplier DOCUMENT evidence"})
        return rating
def metrics(rows:list[dict])->dict:
    m=model(); applicable=[r for r in rows if r["rating"]!="na"]; counts={x:0 for x in RATINGS}
    for r in rows:counts[r["rating"]]+=1
    raw=0 if not applicable else 100*sum(m["rating_weights"][r["rating"]] for r in applicable)/len(applicable)
    consolidated=float(Decimal(str(raw)).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP))
    classification=next(t["class"] for t in m["classification_thresholds"] if consolidated>=t["min_score"])
    return {"consolidated_score":consolidated,"classification":classification,"classification_counts":dict(sorted(counts.items())),"applicable_count":len(applicable)}
