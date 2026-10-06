"""Preview and atomically activate a source replacement with all 18 assessments.

No source or crumb is edited. Old evaluation rows/links are retained in an
append-only database revision and an exclusive-create external journal.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

import yaml
from evaluation_engine import DIMENSIONS, SUMMARIES, score_rating, metrics
from source_revision_intake import local, sha, encoded, read_json, write_new, approval, insert
from sieve_generation import _changelog_has_lesson
from score_sieving import _keys

ROOT=Path(__file__).resolve().parents[1]
FIVE={'fully','substantially','partially','minimally','unmet'}
SCHEMA=[
    '''CREATE TABLE IF NOT EXISTS source_revision_activations (
       old_doc_id TEXT PRIMARY KEY REFERENCES documents, new_doc_id TEXT NOT NULL UNIQUE REFERENCES documents,
       old_run_id TEXT NOT NULL REFERENCES sieve_runs, new_run_id TEXT NOT NULL UNIQUE REFERENCES sieve_runs,
       decision_ref TEXT NOT NULL, plan_sha256 TEXT NOT NULL, recorded_at TEXT NOT NULL) STRICT''',
    '''CREATE TABLE IF NOT EXISTS evaluation_revisions (
       revision_id TEXT PRIMARY KEY, evaluation_run_id TEXT NOT NULL REFERENCES evaluation_runs,
       decision_ref TEXT NOT NULL, before_json TEXT NOT NULL, after_json TEXT NOT NULL,
       recorded_at TEXT NOT NULL) STRICT''',
    '''CREATE TRIGGER IF NOT EXISTS prevent_retired_source_update BEFORE UPDATE OF is_active ON sieve_runs
       WHEN NEW.is_active=1 AND EXISTS(SELECT 1 FROM source_revision_activations WHERE old_doc_id=NEW.doc_id)
       BEGIN SELECT RAISE(ABORT,'cannot activate a retired source'); END''',
    '''CREATE TRIGGER IF NOT EXISTS prevent_retired_source_insert BEFORE INSERT ON sieve_runs
       WHEN NEW.is_active=1 AND EXISTS(SELECT 1 FROM source_revision_activations WHERE old_doc_id=NEW.doc_id)
       BEGIN SELECT RAISE(ABORT,'cannot activate a retired source'); END''',
]
for table in ('source_revision_activations','evaluation_revisions'):
    for operation in ('UPDATE','DELETE'):
        SCHEMA.append(f"CREATE TRIGGER IF NOT EXISTS immutable_{table}_{operation} BEFORE {operation} ON {table} BEGIN SELECT RAISE(ABORT,'immutable revision history'); END")


def rows(c, sql, args=()):
    return [dict(r) for r in c.execute(sql,args)]


def retired_documents(c):
    if not c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='source_revision_activations'").fetchone(): return set()
    events=list(c.execute('SELECT old_doc_id,new_doc_id,old_run_id,new_run_id FROM source_revision_activations'))
    retired=set()
    # Resolve chains from the current source back to its retained predecessors.
    for _ in events:
        for old,new,oldrun,newrun in events:
            lineage=c.execute('SELECT old_doc_id,new_doc_id,old_run_id,new_run_id FROM source_revision_intakes WHERE new_run_id=?',(newrun,)).fetchone()
            previous=c.execute('SELECT status,is_active FROM sieve_runs WHERE run_id=? AND doc_id=?',(oldrun,old)).fetchone()
            active=c.execute('SELECT count(*) FROM sieve_runs WHERE doc_id=? AND is_active=1 AND completed_at IS NOT NULL',(new,)).fetchone()[0]
            oldactive=c.execute('SELECT count(*) FROM sieve_runs WHERE doc_id=? AND is_active=1',(old,)).fetchone()[0]
            if lineage and tuple(lineage)==(old,new,oldrun,newrun) and previous and tuple(previous)==('superseded',0) and oldactive==0 and (active==1 or new in retired): retired.add(old)
    return retired


def prepare(root, assessment):
    root=Path(root).resolve();config_path=local(root,assessment);cfg=read_json(config_path)
    database=local(root,'db/nqa_audit.sqlite');before=sha(database.read_bytes())
    inputs={}
    def bind(path):
        p=local(root,path);inputs[p.relative_to(root).as_posix()]=sha(p.read_bytes());return p
    bind(config_path);bind('manifests/approvals.csv')
    decision=cfg['decision_ref'];approval(root,decision)
    run=cfg['run_id'];approval(root,'G2-'+run);approval(root,'G3-'+run)
    model=yaml.safe_load(bind('schemas/scoring_model.yml').read_text(encoding='utf-8'))
    if model.get('calibration_status')!='approved' or model.get('approval_ref')!='G3-'+run:
        raise ValueError('approved scoring model required')
    import csv
    with local(root,'manifests/approvals.csv').open(encoding='utf-8-sig',newline='') as f:
        g3=next(r for r in csv.DictReader(f) if r['object_id']=='G3-'+run)
    if model['model_version'] not in g3['notes'] or 'placeholder' in model['model_version'].lower(): raise ValueError('model version not approved')
    expected=yaml.safe_load(bind(cfg['golden']).read_text(encoding='utf-8'))
    if expected.get('status')!='approved': raise ValueError('approved golden required')
    approval(root,expected['approval_ref'])
    prompts=yaml.safe_load(bind('sieving/prompts/active.yml').read_text(encoding='utf-8'))
    changelog=bind('sieving/prompts/CHANGELOG.md')
    with closing(sqlite3.connect(database.as_uri()+'?mode=ro',uri=True)) as c:
        c.row_factory=sqlite3.Row
        relation=rows(c,'SELECT * FROM source_revision_intakes WHERE new_run_id=?',(cfg['new_run_id'],))
        if len(relation)!=1: raise ValueError('verified source intake required')
        relation=relation[0];oldrun=relation['old_run_id'];newrun=relation['new_run_id']
        approval(root,relation['decision_ref'])
        old=c.execute('SELECT * FROM sieve_runs WHERE run_id=?',(oldrun,)).fetchone()
        new=c.execute('SELECT * FROM sieve_runs WHERE run_id=?',(newrun,)).fetchone()
        if not old or not new or old['status']!='active' or old['is_active']!=1 or new['status']!='candidate' or new['is_active'] or not new['completed_at'] or new['supersedes_run_id']!=oldrun:
            raise ValueError('completed active predecessor and inactive candidate required')
        if old['doc_id']!=relation['old_doc_id'] or new['doc_id']!=relation['new_doc_id'] or old['document_side']!='DOCUMENT' or new['document_side']!='DOCUMENT': raise ValueError('source lineage mismatch')
        if new['prompt_version']!=prompts['active']['DOCUMENT'] or not _changelog_has_lesson(changelog,new['prompt_version']): raise ValueError('active prompt and lesson required')
        bind('sieving/prompts/'+new['prompt_version']+'.md')
        if expected['document']['doc_id']!=new['doc_id']: raise ValueError('golden identity mismatch')
        actual=[]
        for crumb in rows(c,'SELECT * FROM crumbs WHERE sieve_run_id=? ORDER BY item_id',(newrun,)):
            quotes=rows(c,'SELECT * FROM crumb_quotes WHERE item_id=?',(crumb['item_id'],))
            if not quotes: raise ValueError('candidate lacks quotes')
            for q in quotes:
                links=rows(c,'SELECT ch.* FROM crumb_chunk_links l JOIN document_chunks ch USING(chunk_id) WHERE l.item_id=? AND l.quote_id=?',(crumb['item_id'],q['quote_id']))
                if not links or any(ch['doc_id']!=new['doc_id'] or ch['source_sha256']!=relation['source_sha256'] or not q['quote_original'] or q['quote_original'] not in ch['chunk_text'] for ch in links): raise ValueError('quote not exact in replacement chapter')
            actual.append({**crumb,'evidence_quotes':quotes})
        if _keys(actual,'actual')!=_keys(expected['expected_crumbs'],'golden'): raise ValueError('database candidate differs from golden')
        # Validate every registered raw source used by this audit, including the predecessor.
        texts={}
        for doc in rows(c,'SELECT * FROM documents'):
            raw=bind('raw/'+doc['filename']).read_bytes()
            if sha(raw)!=doc['sha256']: raise ValueError('raw source hash changed: '+doc['doc_id'])
            texts[doc['doc_id']]=raw.decode('utf-8-sig')
        for ch in rows(c,'SELECT * FROM document_chunks WHERE doc_id=?',(new['doc_id'],)):
            if ch['chunk_text']!=texts[new['doc_id']][ch['char_start']:ch['char_end']]: raise ValueError('chapter differs from source')
        meta=c.execute('SELECT * FROM evaluation_runs WHERE run_id=?',(run,)).fetchone()
        if not meta or meta['scoring_model_version']!=model['model_version']: raise ValueError('evaluation model mismatch')
        criteria={r[0] for r in c.execute('SELECT criterion_id FROM criteria')}
        supplied=cfg['evaluations']
        if len(criteria)!=18 or len(supplied)!=18 or {r['criterion_id'] for r in supplied}!=criteria: raise ValueError('exactly 18 assessments required')
        prior=rows(c,'SELECT * FROM criterion_evaluations WHERE evaluation_run_id=? ORDER BY criterion_id',(run,))
        evidence=rows(c,'SELECT e.* FROM evaluation_evidence e JOIN criterion_evaluations v USING(evaluation_id) WHERE v.evaluation_run_id=? ORDER BY evaluation_id,item_id',(run,))
        if len(prior)!=18: raise ValueError('exactly 18 previous evaluations required')
        for table in ('gaps','findings','auditor_actions'):
            if c.execute('SELECT count(*) FROM '+table).fetchone()[0]: raise ValueError('downstream records need explicit reconciliation: '+table)
        # Keep reviewed non-manual links and use the full new control set. Leads
        # stay visible in the evidence pool but are not links supporting scores.
        pool=rows(c,"SELECT c.*,x.evidence_type FROM crumbs c JOIN sieve_runs r ON r.run_id=c.sieve_run_id LEFT JOIN crumb_context x USING(item_id) WHERE c.document_side='DOCUMENT' AND ((r.is_active=1 AND r.run_id<>?) OR r.run_id=?)",(oldrun,newrun))
        oldids={r['item_id'] for r in evidence}
        usable=[r for r in pool if (r['sieve_run_id']==newrun or r['item_id'] in oldids) and r['evidence_type']!='candidate_lead' and not r['statement'].startswith('candidate_lead:')]
        after=[]
        for entry in supplied:
            cid=entry['criterion_id'];rating=entry['rating']
            if rating not in FIVE: raise ValueError('each criterion needs one of the five ratings')
            ruling=c.execute('SELECT * FROM criterion_applicability WHERE evaluation_run_id=? AND criterion_id=?',(run,cid)).fetchone()
            if not ruling or not ruling['applicable'] or (ruling['applicability_state']=='conditional' and not ruling['conditional_confirmation_ref']): raise ValueError('applicability not confirmed')
            if ruling['conditional_confirmation_ref']: approval(root,ruling['conditional_confirmation_ref'])
            selected=sorted(r['item_id'] for r in usable if r['criterion_id']==cid)
            if rating!='unmet' and not selected: raise ValueError('nonzero rating needs vendor controls')
            for field in SUMMARIES:
                if not isinstance(entry.get(field),str) or not entry[field].strip(): raise ValueError('assessment explanation required: '+field)
            score=score_rating(rating,scoring_model=model)
            row={'evaluation_id':next(r['evaluation_id'] for r in prior if r['criterion_id']==cid),'evaluation_run_id':run,'criterion_id':cid,'rating':rating,'score':score,'evidence_supported':int(bool(selected)),**{k:entry[k].strip() for k in SUMMARIES},**{k:score/100 for k in DIMENSIONS}}
            after.append({'row':row,'evidence_ids':selected})
        count=c.execute("SELECT count(*) FROM active_crumbs WHERE document_side='DOCUMENT'").fetchone()[0]
        oldcount=c.execute('SELECT count(*) FROM crumbs WHERE sieve_run_id=?',(oldrun,)).fetchone()[0]
        history={'evaluations':prior,'evidence':evidence,'run':dict(meta)}
    if sha(database.read_bytes())!=before: raise ValueError('database changed during preview')
    return {'schema':'source_revision_promotion/1','root':str(root),'assessment':config_path.relative_to(root).as_posix(),'database_sha256':before,'inputs':inputs,'relation':relation,'decision_ref':decision,'run_id':run,'before':history,'after':after,'active_vendor_before':count,'active_vendor_after':count-oldcount+len(actual),'golden_found':len(actual),'metrics':metrics([a['row'] for a in after],scoring_model=model)}


def apply(root,plan,output,*,before_commit=None):
    root=Path(root).resolve();output=local(root,output);db=local(root,'db/nqa_audit.sqlite')
    if output==root/'out' or not output.is_relative_to(root/'out'): raise ValueError('journal must be under project out')
    digest=sha(encoded(plan));newrun=plan['relation']['new_run_id']
    if (output/'completed.json').exists():
        receipt=read_json(output/'completed.json')
        if receipt['plan_sha256']!=digest: raise ValueError('retry plan changed')
        with closing(sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)) as c:
            event=c.execute('SELECT plan_sha256 FROM source_revision_activations WHERE new_run_id=?',(newrun,)).fetchone()
            history=c.execute('SELECT before_json,after_json FROM evaluation_revisions WHERE revision_id=?',(newrun,)).fetchone()
            if not event or event[0]!=digest or not history or json.loads(history[0])!=plan['before'] or json.loads(history[1])!=plan['after']: raise ValueError('retry history mismatch')
        for name,value in receipt['journal_hashes'].items():
            if sha(local(root,output/name).read_bytes())!=value: raise ValueError('journal changed')
        return {**receipt,'status':'already_applied'}
    if output.exists(): raise ValueError('incomplete journal; inspect transaction history before recovery')
    if prepare(root,plan['assessment'])!=plan: raise ValueError('preview is stale or altered')
    stamp=datetime.now(timezone.utc).isoformat();relation=plan['relation']
    with closing(sqlite3.connect(db.as_uri()+'?mode=rw',uri=True)) as c:
        c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');c.execute('BEGIN IMMEDIATE')
        if sha(db.read_bytes())!=plan['database_sha256']: raise ValueError('database changed before transaction')
        for path,value in plan['inputs'].items():
            if sha(local(root,path).read_bytes())!=value: raise ValueError('input changed before transaction')
        output.mkdir(parents=True,exist_ok=False)
        write_new(output/'intent.json',encoded(plan));write_new(output/'before.json',encoded(plan['before']))
        try:
            for sql in SCHEMA: c.execute(sql)
            c.execute("UPDATE sieve_runs SET status='superseded',is_active=0 WHERE run_id=?",(relation['old_run_id'],))
            c.execute("UPDATE sieve_runs SET status='active',is_active=1,decision_ref=? WHERE run_id=?",(plan['decision_ref'],newrun))
            insert(c,'source_revision_activations',{k:relation[k] for k in ('old_doc_id','new_doc_id','old_run_id','new_run_id')}|{'decision_ref':plan['decision_ref'],'plan_sha256':digest,'recorded_at':stamp})
            insert(c,'evaluation_revisions',{'revision_id':newrun,'evaluation_run_id':plan['run_id'],'decision_ref':plan['decision_ref'],'before_json':encoded(plan['before']).decode(),'after_json':encoded(plan['after']).decode(),'recorded_at':stamp})
            for entry in plan['after']:
                row=entry['row'];eid=row['evaluation_id'];keys=[k for k in row if k!='evaluation_id']
                c.execute('UPDATE criterion_evaluations SET '+','.join(k+'=?' for k in keys)+' WHERE evaluation_id=?',[row[k] for k in keys]+[eid])
                c.execute('DELETE FROM evaluation_evidence WHERE evaluation_id=?',(eid,))
                for item in entry['evidence_ids']: insert(c,'evaluation_evidence',{'evaluation_id':eid,'item_id':item})
            insert(c,'sieve_generation_events',{'doc_id':relation['new_doc_id'],'from_run_id':relation['old_run_id'],'to_run_id':newrun,'operation':'promote','decision_ref':plan['decision_ref'],'reason':'Approved full-source replacement with atomic 18-criterion reassessment; previous results retained in evaluation_revisions.'})
            if c.execute('PRAGMA foreign_key_check').fetchall(): raise ValueError('foreign key violation')
            if c.execute('SELECT count(*) FROM evaluation_evidence e LEFT JOIN active_crumbs a USING(item_id) WHERE a.item_id IS NULL').fetchone()[0]: raise ValueError('inactive evaluation evidence')
            count=c.execute("SELECT count(*) FROM active_crumbs WHERE document_side='DOCUMENT'").fetchone()[0]
            if count!=plan['active_vendor_after']: raise ValueError('unexpected active count')
            if before_commit: before_commit()
            c.commit()
        except Exception:
            c.rollback();write_new(output/'failed.json',encoded({'status':'rolled_back'}));raise
    receipt={'status':'completed','new_run_id':newrun,'active_vendor':count,'plan_sha256':digest,'database_before_sha256':plan['database_sha256'],'database_after_sha256':sha(db.read_bytes()),'metrics':plan['metrics'],'journal_hashes':{name:sha((output/name).read_bytes()) for name in ('intent.json','before.json')}}
    write_new(output/'completed.json',encoded(receipt));return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,default=ROOT)
    p.add_argument('--assessment');p.add_argument('--apply-plan');p.add_argument('--output',required=True)
    a=p.parse_args();root=a.project.resolve()
    if a.apply_plan: result=apply(root,read_json(local(root,a.apply_plan)),a.output)
    else:
        result=prepare(root,a.assessment);write_new(local(root,a.output),encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k in ('status','active_vendor','active_vendor_after','golden_found','metrics')}))

if __name__=='__main__': main()
