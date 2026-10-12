#!/usr/bin/env python3
"""Preview/apply a source-specific, INACTIVE replacement evidence generation.

Keep all predecessor rows/files and current audit results unchanged. This is not
promotion: switching sources requires an atomic evaluation refresh as well.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
import stat

import yaml
import sieving_lib  # project-local extractor package
from json_extractor.crumb_validation import validate_payload

ROOT = Path(__file__).resolve().parents[1]
HEADER = ['doc_id','filename','title','supplier','doc_date','language','side_hint',
          'sha256','promoted_utc','source_url','notes']
REVISION_SQL = '''CREATE TABLE IF NOT EXISTS source_revision_intakes (
 new_doc_id TEXT PRIMARY KEY REFERENCES documents(doc_id),
 old_doc_id TEXT NOT NULL REFERENCES documents(doc_id),
 old_run_id TEXT NOT NULL REFERENCES sieve_runs(run_id),
 new_run_id TEXT NOT NULL UNIQUE REFERENCES sieve_runs(run_id),
 source_sha256 TEXT NOT NULL, candidate_sha256 TEXT NOT NULL,
 decision_ref TEXT NOT NULL, recorded_at TEXT NOT NULL,
 CHECK(new_doc_id<>old_doc_id)
) STRICT'''


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def local(root, path):
    root = Path(root).resolve()
    path = Path(path)
    value = path if path.is_absolute() else root / path
    for part in (value, *value.parents):
        if part.exists():
            info = part.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('redirected paths are forbidden')
            if part.is_file() and info.st_nlink>1:
                raise ValueError('hardlinked project files are forbidden')
    value = value.resolve()
    if not value.is_relative_to(root):
        raise ValueError('path leaves selected project')
    return value


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def approval(root, reference):
    rows = list(csv.DictReader(io.StringIO(local(root,'manifests/approvals.csv').read_text(encoding='utf-8-sig'))))
    found = [r for r in rows if r['object_id']==reference]
    if len(found)!=1 or found[0]['decision']!='approved' or not found[0]['reviewer'] or not found[0]['date']:
        raise ValueError('source intake approval missing or ambiguous')


def prepare(root, review, *, run_id, decision_ref):
    root = Path(root).resolve()
    review = local(root,review)
    if not review.is_relative_to(root/'sieving/candidates'):
        raise ValueError('review must be in project sieving/candidates')
    if not re.fullmatch(r'RUN-\d{8}-\d{2,}',run_id):
        raise ValueError('invalid run ID')
    approval(root,decision_ref)
    config = read_json(review/'review.json')
    bundle = review/'reviewed'
    manifest = read_json(bundle/'manifest.json')
    for name, digest in manifest['artifacts'].items():
        path = local(root,bundle/name)
        if path.parent != bundle or sha(path.read_bytes()) != digest:
            raise ValueError('review artifact checksum mismatch')
    payload = read_json(bundle/'candidate.json')
    validation=validate_payload(payload,strict=True)
    if not validation.passed:
        raise ValueError('strict candidate validation failed: '+'; '.join(validation.errors))
    source = local(root,config['source'])
    raw = source.read_bytes()
    if sha(raw)!=config['source_sha256'] or payload.get('source_sha256')!=sha(raw):
        raise ValueError('replacement source checksum mismatch')
    if payload['document']['doc_id']!=config['doc_id'] or payload['document']['document_side']!='DOCUMENT':
        raise ValueError('review document identity mismatch')
    prompt = payload['prompt_version']
    if not re.fullmatch('[a-z0-9_-]+',prompt):
        raise ValueError('invalid prompt')
    active = yaml.safe_load(local(root,'sieving/prompts/active.yml').read_text(encoding='utf-8'))
    if active['active']['DOCUMENT']!=prompt:
        raise ValueError('review prompt is not the active DOCUMENT prompt')
    prompt_path = local(root,f'sieving/prompts/{prompt}.md')
    text = raw.decode('utf-8')
    for item in payload['items']:
        context=item.get('context') or {}
        if item.get('evidence_type') and not context:
            raise ValueError('evidence type needs a source context anchor')
        if any(value not in text for value in context.values()):
            raise ValueError('context anchor is not verbatim in the source')
    # Existing derived-text readers normalize newlines. Refuse rather than
    # silently alter evidence if a later input needs an explicit normalization.
    if '\r' in text:
        raise ValueError('source uses CR newlines; explicit derived/quote normalization needed')
    lines = text.splitlines(keepends=True)
    offsets=[0]
    for line in lines: offsets.append(offsets[-1]+len(line))
    chunks=[]; cursor=1
    for section in config['sections']:
        a,b=section['start'],section['end']
        if a!=cursor or not a<=b<=len(lines) or not section['chapter'].strip():
            raise ValueError('chapter plan gap, overlap or invalid range')
        value=text[offsets[a-1]:offsets[b]]
        if not value.strip(): raise ValueError('empty chapter')
        chunks.append({'heading_path':section['chapter'],'chunk_text':value,
                       'char_start':offsets[a-1],'char_end':offsets[b]})
        cursor=b+1
    if cursor!=len(lines)+1: raise ValueError('chapter plan incomplete')
    database=local(root,'db/nqa_audit.sqlite')
    before=sha(database.read_bytes())
    with closing(sqlite3.connect(database.as_uri()+'?mode=ro',uri=True)) as conn:
        conn.row_factory=sqlite3.Row
        old=conn.execute('SELECT * FROM documents WHERE doc_id=?',(config['doc_id'],)).fetchone()
        if old is None or old['sha256']!=config['registered_sha256'] or old['document_side']!='DOCUMENT':
            raise ValueError('registered predecessor mismatch')
        old=dict(old)
        old_raw=local(root,'raw/'+old['filename'])
        if sha(old_raw.read_bytes())!=old['sha256']: raise ValueError('old raw changed')
        if conn.execute('SELECT 1 FROM documents WHERE sha256=?',(sha(raw),)).fetchone():
            raise ValueError('replacement already registered')
        if conn.execute('SELECT 1 FROM sieve_runs WHERE run_id=?',(run_id,)).fetchone():
            raise ValueError('run already exists')
        active_runs=conn.execute('SELECT * FROM sieve_runs WHERE doc_id=? AND is_active=1',(old['doc_id'],)).fetchall()
        if len(active_runs)!=1 or not active_runs[0]['completed_at']:
            raise ValueError('predecessor needs one completed active run')
        old_run=active_runs[0]['run_id']
        new_id=f"DOC-{max(int(r[0].split('-')[1]) for r in conn.execute('SELECT doc_id FROM documents'))+1:04d}"
        if not re.fullmatch(r'DOC-\d{4}',new_id): raise ValueError('document ID space exhausted')
        criteria={r[0] for r in conn.execute('SELECT criterion_id FROM criteria')}
        active_count=conn.execute("SELECT count(*) FROM active_crumbs WHERE document_side='DOCUMENT'").fetchone()[0]
        old_count=conn.execute('SELECT count(*) FROM crumbs WHERE sieve_run_id=?',(old_run,)).fetchone()[0]
    if before!=sha(database.read_bytes()): raise ValueError('database changed during preview')
    ordinals=Counter(); records=[]; source_ids=set()
    for number,item in enumerate(payload['items'],1):
        cid=item['criterion_id']
        if cid not in criteria or not item['statement'].strip() or not item.get('sources'):
            raise ValueError('invalid reviewed item')
        if item['item_id'] in source_ids: raise ValueError('duplicate review item ID')
        source_ids.add(item['item_id'])
        ordinals[cid]+=1
        crumb_id=f'CRUMB-{new_id}-{cid}-{ordinals[cid]:04d}'
        quotes=[]
        for qi,q in enumerate(item['evidence_quotes'],1):
            literal=q['quote_original']
            matches=[i for i,c in enumerate(chunks,1) if literal and literal in c['chunk_text']]
            if not matches: raise ValueError('quote not exact in a complete replacement chapter')
            quotes.append({**q,'quote_id':f'QUOTE-{new_id}-{number:04d}-{qi:02d}',
                           'chunks':[f'CHUNK-{new_id}-{i:04d}' for i in matches]})
        if not quotes: raise ValueError('item has no quote')
        records.append({'original_item_id':item['item_id'],'item_id':crumb_id,'item':item,'quotes':quotes})
    if not records: raise ValueError('empty candidate')
    new_raw=f"raw/{Path(old['filename']).stem}__{sha(raw)[:12]}.md"
    derived=f'derived/{new_id}.txt'; artifact=f'derived/chunks/{new_id}.json'
    for path in (new_raw,derived,artifact,f'sieving/runs/{run_id}'):
        if local(root,path).exists(): raise ValueError('new destination already exists')
    registry=local(root,'manifests/raw_sources.csv').read_bytes()
    reader=csv.DictReader(io.StringIO(registry.decode('utf-8-sig')))
    if reader.fieldnames!=HEADER: raise ValueError('source registry header mismatch')
    old_rows=[r for r in reader if r['doc_id']==old['doc_id']]
    if len(old_rows)!=1 or old_rows[0]['sha256']!=old['sha256']: raise ValueError('source registry predecessor mismatch')
    inputs={str(p.relative_to(root)).replace('\\','/'):sha(p.read_bytes()) for p in
            [source,review/'review.json',bundle/'manifest.json',prompt_path,
             local(root,'sieving/prompts/active.yml'),local(root,'manifests/approvals.csv'),old_raw,
             *[bundle/name for name in manifest['artifacts']]]}
    return {'schema':'source_revision_intake/1','mode':'preview','root':str(root),
            'review':str(review.relative_to(root)),'run_id':run_id,'decision_ref':decision_ref,
            'database_sha256':before,'registry_sha256':sha(registry),'inputs':inputs,
            'source':str(source.relative_to(root)),'source_sha256':sha(raw),
            'candidate_sha256':sha((bundle/'candidate.json').read_bytes()),
            'new_doc_id':new_id,'new_raw':new_raw,'derived':derived,'chunk_artifact':artifact,
            'predecessor':old,'old_run_id':old_run,'prompt_version':prompt,
            'chapters':chunks,'records':records,'active_vendor_before':active_count,
            'old_crumbs':old_count,'new_crumbs':len(records),
            'projected_active_vendor_after_promotion':active_count-old_count+len(records),
            'live_activation':False,'evaluation_modified':False}


def write_new(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream: stream.write(value)


def encoded(value):
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def insert(conn,table,values):
    keys=list(values)
    conn.execute(f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join('?' for _ in keys)})",[values[k] for k in keys])


def apply(root, plan, output, *, before_commit=None):
    root=Path(root).resolve();output=local(root,output)
    if not output.is_relative_to(root/'out') or output==root/'out':
        raise ValueError('journal must be under selected project out')
    receipt_path=output/'completed.json'
    if receipt_path.exists():
        receipt=read_json(receipt_path)
        if receipt['plan_sha256']!=sha(encoded(plan)): raise ValueError('retry plan differs')
        for path,digest in receipt['created_files'].items():
            if sha(local(root,path).read_bytes())!=digest: raise ValueError('retry artifact changed')
        with closing(sqlite3.connect(local(root,'db/nqa_audit.sqlite').as_uri()+'?mode=ro',uri=True)) as c:
            row=c.execute('SELECT source_sha256,candidate_sha256,decision_ref FROM source_revision_intakes WHERE new_run_id=?',(plan['run_id'],)).fetchone()
            if row!=(plan['source_sha256'],plan['candidate_sha256'],plan['decision_ref']): raise ValueError('retry database identity differs')
        return {**receipt,'status':'already_applied'}
    if output.exists(): raise ValueError('journal exists without completion; inspect for recovery, never retry blindly')
    expected=prepare(root,local(root,plan['review']),run_id=plan['run_id'],decision_ref=plan['decision_ref'])
    if plan!=expected: raise ValueError('preview is stale or altered; no write performed')
    database=local(root,'db/nqa_audit.sqlite');manifest=local(root,'manifests/raw_sources.csv')
    manifest_before=manifest.read_bytes();raw=local(root,plan['source']).read_bytes()
    stamp=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    old=plan['predecessor'];new=plan['new_doc_id'];run=plan['run_id']
    chunks=[{'chunk_id':f'CHUNK-{new}-{i:04d}','doc_id':new,'source_sha256':plan['source_sha256'],**c} for i,c in enumerate(plan['chapters'],1)]
    document={'doc_id':new,'filename':Path(plan['new_raw']).name,'title':old['title'],
              'supplier':old['supplier'],'doc_date':old['doc_date'],'language':old['language'],
              'document_side':'DOCUMENT','sha256':plan['source_sha256'],'promoted_utc':stamp,
              'source_url':old['source_url'],'notes':f"Fuller source extraction; predecessor {old['doc_id']}; intake {plan['decision_ref']}; candidate only.",
              'extraction_method':'owner-supplied Markdown; exact UTF-8 text','extracted_at':stamp}
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=HEADER,lineterminator='\n')
    writer.writerow({k:(document['document_side'] if k=='side_hint' else document.get(k) or ('n-a' if k=='doc_date' else '')) for k in HEADER})
    registry_after=manifest_before+(b'' if manifest_before.endswith(b'\n') else b'\n')+stream.getvalue().encode('utf-8')
    payload=read_json(local(root,plan['review'])/'reviewed/candidate.json')
    payload['document']['doc_id']=new
    payload['predecessor_doc_id']=old['doc_id']
    artifacts={plan['new_raw']:raw,plan['derived']:raw,
               plan['chunk_artifact']:encoded({'schema_version':'1.0','doc_id':new,'chunks':chunks}),
               f'sieving/runs/{run}/candidate.json':encoded(payload),
               f'sieving/runs/{run}/source-diff.json':encoded({k:plan[k] for k in ('old_run_id','run_id','old_crumbs','new_crumbs','source_sha256','candidate_sha256','new_doc_id')})}
    created=[];committed=False;manifest_written=False
    with closing(sqlite3.connect(database.as_uri()+'?mode=rw',uri=True)) as conn:
        conn.execute('PRAGMA foreign_keys=ON');conn.execute('BEGIN IMMEDIATE')
        if sha(database.read_bytes())!=plan['database_sha256'] or sha(manifest.read_bytes())!=plan['registry_sha256']:
            conn.rollback();raise ValueError('live state changed before transaction')
        try:
            output.mkdir(parents=True,exist_ok=False)
            write_new(output/'intent.json',encoded({'plan_sha256':sha(encoded(plan)),'plan':plan,
                'manifest_before':manifest_before.decode('utf-8-sig'),'manifest_after_sha256':sha(registry_after),
                'recovery':'Old source and DB rows untouched. If crash leaves no completed receipt, inspect transaction identity before restoring exact registry bytes/removing only recorded new artifacts.'}))
            conn.execute(REVISION_SQL)
            insert(conn,'documents',document)
            for row in chunks: insert(conn,'document_chunks',row)
            insert(conn,'sieve_runs',{'run_id':run,'doc_id':new,'prompt_version':plan['prompt_version'],
                'document_side':'DOCUMENT','generation':1,'status':'candidate','is_active':0,
                'supersedes_run_id':plan['old_run_id'],'decision_ref':plan['decision_ref']})
            for record in plan['records']:
                item=record['item'];cid=record['item_id']
                insert(conn,'crumbs',{'item_id':cid,'doc_id':new,'sieve_run_id':run,
                    'criterion_id':item['criterion_id'],'document_side':'DOCUMENT','statement':item['statement'],
                    'item_type':item.get('item_type'),'quote_language':record['quotes'][0]['quote_language']})
                for source in item['sources']:
                    insert(conn,'crumb_sources',{'item_id':cid,'source_locator':source['source_locator'],
                        'source_heading_path':source.get('source_heading_path'),'source_page':source.get('source_page')})
                for q in record['quotes']:
                    insert(conn,'crumb_quotes',{'quote_id':q['quote_id'],'item_id':cid,'quote_original':q['quote_original'],
                        'quote_language':q['quote_language'],'source_locator':q.get('source_locator',item['sources'][0]['source_locator'])})
                    for chunk_id in q['chunks']:
                        insert(conn,'crumb_chunk_links',{'item_id':cid,'quote_id':q['quote_id'],'chunk_id':chunk_id,'link_method':'EXACT','confidence':1.0})
                if item.get('evidence_type') or item.get('context'):
                    insert(conn,'crumb_context',{'item_id':cid,'evidence_type':item.get('evidence_type'),**(item.get('context') or {})})
            conn.execute('UPDATE sieve_runs SET completed_at=? WHERE run_id=?',(stamp,run))
            insert(conn,'source_revision_intakes',{'new_doc_id':new,'old_doc_id':old['doc_id'],
                'old_run_id':plan['old_run_id'],'new_run_id':run,'source_sha256':plan['source_sha256'],
                'candidate_sha256':plan['candidate_sha256'],'decision_ref':plan['decision_ref'],'recorded_at':stamp})
            if conn.execute('PRAGMA foreign_key_check').fetchall(): raise ValueError('foreign key check failed')
            if conn.execute("SELECT count(*) FROM active_crumbs WHERE document_side='DOCUMENT'").fetchone()[0]!=plan['active_vendor_before']:
                raise ValueError('intake changed active evidence')
            for name,body in artifacts.items():
                path=local(root,name);write_new(path,body);created.append(path)
            manifest.write_bytes(registry_after);manifest_written=True
            if before_commit: before_commit()
            conn.commit();committed=True
        except Exception:
            if not committed:
                conn.rollback()
                if manifest_written: manifest.write_bytes(manifest_before)
                for path in reversed(created): path.unlink()
                if output.exists(): write_new(output/'failed.json',encoded({'status':'rolled_back','created_files_removed':[str(p.relative_to(root)) for p in created]}))
            raise
    local(root,plan['new_raw']).chmod(stat.S_IREAD)
    receipt={'status':'completed','mode':'inactive_candidate_intake','run_id':run,'doc_id':new,
        'plan_sha256':sha(encoded(plan)),'database_before_sha256':plan['database_sha256'],
        'database_after_sha256':sha(database.read_bytes()),'registry_after_sha256':sha(manifest.read_bytes()),
        'created_files':{str(p.relative_to(root)):sha(p.read_bytes()) for p in created},
        'crumbs':plan['new_crumbs'],'chapters':len(chunks),'active_vendor':plan['active_vendor_before'],
        'activation_pending':'Golden score, source-switch decision and evaluation refresh as one controlled continuation.'}
    write_new(receipt_path,encoded(receipt))
    return receipt


def pending_revision_documents(conn):
    """Only a verified inactive replacement may temporarily lack an active run.

    The predecessor must still be active. This is not permission to hide a
    missing active generation in an ordinary document or to activate both.
    """
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='source_revision_intakes' AND type='table'").fetchone():
        return set()
    allowed=set()
    for row in conn.execute('SELECT new_doc_id,old_doc_id,old_run_id,new_run_id,source_sha256 FROM source_revision_intakes'):
        new_doc,old_doc,old_run,new_run,digest=tuple(row)
        old=conn.execute('SELECT doc_id,status,is_active FROM sieve_runs WHERE run_id=?',(old_run,)).fetchone()
        new=conn.execute('SELECT doc_id,status,is_active,completed_at,supersedes_run_id FROM sieve_runs WHERE run_id=?',(new_run,)).fetchone()
        doc=conn.execute('SELECT sha256 FROM documents WHERE doc_id=?',(new_doc,)).fetchone()
        history=conn.execute('SELECT count(*) FROM sieve_runs WHERE doc_id=?',(new_doc,)).fetchone()[0]
        if old and new and doc and tuple(old)==(old_doc,'active',1) and tuple(new[:3])==(new_doc,'candidate',0) and new[3] and new[4]==old_run and doc[0]==digest and history==1:
            allowed.add(new_doc)
    return allowed


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=ROOT)
    parser.add_argument('--review',type=Path)
    parser.add_argument('--run-id');parser.add_argument('--decision-ref')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--apply-plan',type=Path)
    args=parser.parse_args();root=args.project.resolve()
    if args.apply_plan:
        result=apply(root,read_json(local(root,args.apply_plan)),args.output)
    else:
        if not args.review or not args.run_id or not args.decision_ref: parser.error('preview needs review, run-id and decision-ref')
        result=prepare(root,args.review,run_id=args.run_id,decision_ref=args.decision_ref)
        write_new(local(root,args.output),encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k in ('mode','status','run_id','new_doc_id','doc_id','new_crumbs','crumbs','chapters','active_vendor','live_activation') and k!='chapters'}))


if __name__=='__main__': main()
