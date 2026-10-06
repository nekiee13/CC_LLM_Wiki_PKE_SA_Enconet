"""Source changes create new identities; never mutate old evidence."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('source_revision_intake', SCRIPTS / 'source_revision_intake.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


@pytest.fixture
def sample(tmp_path):
    root = tmp_path / 'Company with spaces'
    for directory in ('db', 'raw', 'derived/chunks', 'manifests', 'sieving/candidates/review/reviewed', 'sieving/prompts', 'out'):
        (root / directory).mkdir(parents=True, exist_ok=True)
    old = b'# old\nOld text.\n'
    raw = b'# New chapter\nKeep records.\n'
    (root / 'raw/old.md').write_bytes(old)
    (root / 'out/new.md').write_bytes(raw)
    db = root / 'db/nqa_audit.sqlite'
    with sqlite3.connect(db) as conn:
        conn.executescript((SCRIPTS.parent / 'db/schema.sql').read_text(encoding='utf-8'))
        conn.execute("INSERT INTO criteria VALUES ('APP_B_XVII','Records','Records')")
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256,promoted_utc) VALUES ('DOC-0001','old.md','Manual','Example','en','DOCUMENT',?,'2026-01-01')", (intake.sha(old),))
        conn.execute("INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side,completed_at) VALUES ('RUN-20260101-01','DOC-0001','p1','DOCUMENT','2026-01-01')")
    conn.close()
    header = intake.HEADER
    (root / 'manifests/raw_sources.csv').write_text(','.join(header)+'\nDOC-0001,old.md,Manual,Example,n-a,en,DOCUMENT,'+intake.sha(old)+',2026-01-01,n-a,\n', encoding='utf-8')
    (root / 'manifests/approvals.csv').write_text('object_id,decision,date,reviewer,notes\nSOURCE,approved,2026-10-06,Owner,Replacement intake\n', encoding='utf-8')
    (root / 'sieving/prompts/p1.md').write_text('prompt', encoding='utf-8')
    (root / 'sieving/prompts/active.yml').write_text('active:\n  DOCUMENT: p1\n', encoding='utf-8')
    review = root / 'sieving/candidates/review'
    config = {'doc_id':'DOC-0001', 'source':'out/new.md', 'source_sha256':intake.sha(raw),
        'registered_sha256':intake.sha(old), 'sections':[{'start':1,'end':2,'chapter':'1. Records','pass1':'Retention','pass2':'Traceability'}]}
    payload = {'prompt_version':'p1','source_sha256':intake.sha(raw),'document':{'doc_id':'DOC-0001','name':'Manual','date':'n-a','document_side':'DOCUMENT','authority_references':[]},
        'items':[{'item_id':'FULL-0001','criterion_id':'APP_B_XVII','criterion_name':'Quality Assurance Records','statement':'Retain records.', 'item_type':'control','entities':{},'sources':[{'source_locator':'1. Records'}], 'evidence_quotes':[{'quote_original':'Keep records.','quote_language':'en','source_locator':'1. Records'}]}]}
    (review/'review.json').write_text(json.dumps(config),encoding='utf-8')
    (review/'reviewed/candidate.json').write_text(json.dumps(payload),encoding='utf-8')
    (review/'reviewed/provenance.json').write_text(json.dumps({'source_sha256':intake.sha(raw)}),encoding='utf-8')
    manifest={'source_sha256':intake.sha(raw),'artifacts':{p.name:intake.sha(p.read_bytes()) for p in (review/'reviewed').iterdir()}}
    (review/'reviewed/manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
    return root, review


def plan(sample):
    root, review = sample
    return intake.prepare(root, review, run_id='RUN-20261006-99', decision_ref='SOURCE')


def inventory(root):
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}


def test_preview_is_read_only_and_apply_preserves_active(sample):
    root, _ = sample
    before=inventory(root)
    data=plan(sample)
    assert inventory(root)==before
    assert data['new_doc_id']=='DOC-0002'
    receipt=intake.apply(root,data,root/'out/intake')
    assert receipt['status']=='completed'
    with sqlite3.connect(root/'db/nqa_audit.sqlite') as c:
        assert c.execute("SELECT count(*) FROM active_crumbs").fetchone()[0]==0
        assert c.execute("SELECT status,is_active FROM sieve_runs WHERE run_id='RUN-20261006-99'").fetchone()==('candidate',0)
        assert c.execute('SELECT count(*) FROM crumb_chunk_links').fetchone()[0]==1
        assert c.execute('SELECT quote_original FROM crumb_quotes').fetchone()[0]=='Keep records.'
        assert c.execute('PRAGMA foreign_key_check').fetchall()==[]
        assert intake.pending_revision_documents(c)=={'DOC-0002'}
        c.execute("UPDATE sieve_runs SET status='superseded',is_active=0 WHERE run_id='RUN-20260101-01'")
        assert intake.pending_revision_documents(c)==set()
        c.rollback()
    for name,raw in before.items():
        if name not in ('db/nqa_audit.sqlite','manifests/raw_sources.csv'):
            assert (root/name).read_bytes()==raw
    assert (root/'manifests/raw_sources.csv').read_bytes().startswith(before['manifests/raw_sources.csv'])
    assert intake.apply(root,data,root/'out/intake')['status']=='already_applied'


@pytest.mark.parametrize('defect',['source','candidate','approval','database','outside'])
def test_refuse_stale_or_escaped_plan(sample,defect,tmp_path):
    root,review=sample
    data=plan(sample)
    if defect=='source': (root/'out/new.md').write_bytes(b'changed')
    if defect=='candidate': (review/'reviewed/candidate.json').write_text('{}',encoding='utf-8')
    if defect=='approval': (root/'manifests/approvals.csv').write_text('object_id,decision,date,reviewer,notes\n',encoding='utf-8')
    if defect=='database':
        with sqlite3.connect(root/'db/nqa_audit.sqlite') as c: c.execute("UPDATE documents SET title='Changed'")
    if defect=='outside': data['new_raw']='../escape.md'
    before=inventory(root)
    with pytest.raises((ValueError,KeyError)):
        intake.apply(root,data,root/'out/intake')
    assert inventory(root)==before


def test_rollback_removes_only_new_files(sample):
    root,_=sample
    data=plan(sample)
    before=inventory(root)
    def fail(): raise RuntimeError('injected before commit')
    with pytest.raises(RuntimeError,match='injected'):
        intake.apply(root,data,root/'out/intake',before_commit=fail)
    assert (root/'manifests/raw_sources.csv').read_bytes()==before['manifests/raw_sources.csv']
    assert not (root/data['new_raw']).exists()
    with sqlite3.connect(root/'db/nqa_audit.sqlite') as c:
        assert c.execute('SELECT count(*) FROM documents').fetchone()[0]==1
        assert c.execute('SELECT count(*) FROM crumbs').fetchone()[0]==0
    assert json.loads((root/'out/intake/failed.json').read_text())['status']=='rolled_back'


@pytest.mark.parametrize('name',['Second Company','Čista tvrtka'])
@pytest.mark.parametrize('sibling',[False,True])
def test_company_neutral(sample,tmp_path,name,sibling):
    root,review=sample
    moved=root.with_name(name)
    root.rename(moved)
    if sibling:
        other=tmp_path/'Sibling';other.mkdir();(other/'sentinel').write_bytes(b'untouched')
    data=intake.prepare(moved,moved/'sieving/candidates/review',run_id='RUN-20261006-99',decision_ref='SOURCE')
    intake.apply(moved,data,moved/'out/intake')
    if sibling: assert (other/'sentinel').read_bytes()==b'untouched'


def test_bad_quote_refused_before_any_write(sample):
    root,review=sample
    payload=json.loads((review/'reviewed/candidate.json').read_text())
    payload['items'][0]['evidence_quotes'][0]['quote_original']='Invented quote'
    (review/'reviewed/candidate.json').write_text(json.dumps(payload),encoding='utf-8')
    manifest=json.loads((review/'reviewed/manifest.json').read_text())
    manifest['artifacts']['candidate.json']=intake.sha((review/'reviewed/candidate.json').read_bytes())
    (review/'reviewed/manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
    before=inventory(root)
    with pytest.raises(ValueError,match='not exact'):
        plan(sample)
    assert inventory(root)==before


def test_future_sweep_uses_replacement_once(sample):
    import full_keyword_sweep as sweep
    root,review=sample
    data=plan(sample)
    intake.apply(root,data,root/'out/intake')
    (root/'incoming').mkdir()
    (root/'incoming/old.md').write_bytes((root/'out/new.md').read_bytes())
    before=inventory(root)
    result=sweep.prepare(root,sweep.load_rules(SCRIPTS.parent/'sieving/prompts/full_keyword_sweep_v1.json'))
    assert len(result)==1
    assert result[0][1]['doc_id']=='DOC-0002'
    assert result[0][1]['filename']=='old.md'
    assert result[0][1]['source_changed'] is False
    assert inventory(root)==before


def test_diff_requires_explicit_source_relation(sample,monkeypatch):
    import sieve_diff
    root,_=sample
    data=plan(sample)
    intake.apply(root,data,root/'out/intake')
    monkeypatch.setattr(sieve_diff,'local_path',lambda p: Path(p))
    db=root/'db/nqa_audit.sqlite'
    diff=sieve_diff.compare(db,'RUN-20260101-01','RUN-20261006-99')
    assert diff['source_revision']['new_doc_id']=='DOC-0002'
    assert len(diff['criteria']['APP_B_XVII']['added'])==1
    with sqlite3.connect(db) as c: c.execute('DELETE FROM source_revision_intakes')
    with pytest.raises(ValueError,match='verified source-revision'):
        sieve_diff.compare(db,'RUN-20260101-01','RUN-20261006-99')
