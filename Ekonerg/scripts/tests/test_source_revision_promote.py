"""Atomic source replacement must preserve the previous audit and fail closed."""
import json
import sqlite3
from pathlib import Path

import pytest
import yaml

from test_source_revision_intake import sample, plan, intake, inventory, SCRIPTS
import source_revision_promote as promote


@pytest.fixture
def ready(sample):
    root, _ = sample
    intake.apply(root, plan(sample), root/'out/intake')
    model = yaml.safe_load((SCRIPTS.parent/'schemas/scoring_model.yml').read_text())
    model['approval_ref']='G3-RUN-20260101-02'
    (root/'schemas').mkdir()
    (root/'schemas/scoring_model.yml').write_text(yaml.safe_dump(model))
    with (root/'manifests/approvals.csv').open('a') as f:
        for ref in ['PROMOTE','GOLDEN','G2-RUN-20260101-02','G3-RUN-20260101-02']:
            f.write(f'{ref},approved,2026-10-06,Owner,{model["model_version"]}\n')
    (root/'sieving/prompts/CHANGELOG.md').write_text('| p1 | a | b | c | d | e | f | sieving-tuning |\n')
    candidate=json.loads((root/'sieving/runs/RUN-20261006-99/candidate.json').read_text())
    fixture={'status':'approved','approval_ref':'GOLDEN','document':candidate['document'],'expected_crumbs':candidate['items']}
    (root/'golden.yml').write_text(yaml.safe_dump(fixture))
    taxonomy=yaml.safe_load((SCRIPTS.parent/'schemas/app_b_taxonomy.yml').read_text())
    entries=[]
    with sqlite3.connect(root/'db/nqa_audit.sqlite') as c:
        c.execute("INSERT INTO evaluation_runs VALUES ('RUN-20260101-02','Example','en',?,'2026-01-01',NULL)",(model['model_version'],))
        for t in taxonomy['criteria']:
            cid=t['criterion_id']
            c.execute('INSERT OR IGNORE INTO criteria VALUES (?,?,?)',(cid,cid,cid))
            c.execute("INSERT INTO criterion_applicability(evaluation_run_id,criterion_id,applicable,justification,scope_source_doc_id,approved_by,approved_date,decision_ref) VALUES ('RUN-20260101-02',?,1,'scope','DOC-0001','Owner','2026-01-01','G2-RUN-20260101-02')",(cid,))
            c.execute("INSERT INTO criterion_evaluations VALUES (?, 'RUN-20260101-02',?,'unmet',0,0,0,0,0,0,0,'old','old','old','old')",('EVAL-'+cid,cid))
            entries.append({'criterion_id':cid,'rating':'partially' if cid=='APP_B_XVII' else 'unmet','affirmative_summary':'Records are retained.','contrary_summary':'Some details absent.','rationale':'Document screen.','judge_ruling':'Document-based rating.'})
    c.close()
    config={'run_id':'RUN-20260101-02','new_run_id':'RUN-20261006-99','decision_ref':'PROMOTE','golden':'golden.yml','evaluations':entries}
    (root/'assessment.json').write_text(json.dumps(config))
    return root


def test_preview_apply_retry_and_history(ready):
    root=ready; before=inventory(root)
    p=promote.prepare(root,'assessment.json')
    assert inventory(root)==before
    result=promote.apply(root,p,'out/promotion')
    assert result['active_vendor']==1
    with sqlite3.connect(root/'db/nqa_audit.sqlite') as c:
        assert c.execute('select count(*) from evaluation_revisions').fetchone()[0]==1
        assert c.execute("select rating from criterion_evaluations where criterion_id='APP_B_XVII'").fetchone()[0]=='partially'
        assert c.execute('PRAGMA foreign_key_check').fetchall()==[]
        assert promote.retired_documents(c)=={'DOC-0001'}
        with pytest.raises(sqlite3.IntegrityError,match='retired source'):
            c.execute("UPDATE sieve_runs SET is_active=1,status='active' WHERE run_id='RUN-20260101-01'")
    assert promote.apply(root,p,'out/promotion')['status']=='already_applied'
    assert (root/'raw/old.md').read_bytes()==before['raw/old.md']
    history=json.loads((root/'out/promotion/before.json').read_text())
    assert all(r['rating']=='unmet' for r in history['evaluations'])


@pytest.mark.parametrize('defect',['approval','golden','raw','quote','scope','model','missing','stale','escape','downstream'])
def test_fail_closed(ready,defect):
    root=ready;p=promote.prepare(root,'assessment.json')
    if defect=='approval': (root/'manifests/approvals.csv').write_text('object_id,decision,date,reviewer,notes\n')
    if defect=='golden': (root/'golden.yml').write_text('status: pending\n')
    if defect=='raw': (root/'raw/old.md').write_bytes(b'changed')
    if defect in ('quote','scope','stale','downstream'):
        with sqlite3.connect(root/'db/nqa_audit.sqlite') as c:
            if defect=='quote': c.execute("UPDATE crumb_quotes SET quote_original='invented'")
            if defect=='scope':
                # Emulate an invalid legacy database, bypassing its normal guard.
                for (name,) in c.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND tbl_name='criterion_applicability'").fetchall():
                    c.execute('DROP TRIGGER '+name)
                c.execute("UPDATE criterion_applicability SET applicability_state='conditional',conditional_confirmation_ref=NULL")
            if defect=='stale': c.execute("UPDATE documents SET title='changed'")
            if defect=='downstream': c.execute("INSERT INTO gaps VALUES ('GAP-1','EVAL-APP_B_XVII','missing-evidence','gap',NULL,'ref')")
    if defect=='model': (root/'schemas/scoring_model.yml').write_text('calibration_status: pending\n')
    if defect=='missing':
        config=json.loads((root/'assessment.json').read_text());config['evaluations'].pop();(root/'assessment.json').write_text(json.dumps(config))
    if defect=='escape': p['assessment']='../outside.json'
    before=inventory(root)
    with pytest.raises((ValueError,KeyError)):
        promote.apply(root,p,'out/promotion')
    assert inventory(root)==before


def test_transaction_rollback(ready):
    root=ready;p=promote.prepare(root,'assessment.json')
    def fail(): raise RuntimeError('injected')
    with pytest.raises(RuntimeError,match='injected'):
        promote.apply(root,p,'out/promotion',before_commit=fail)
    with sqlite3.connect(root/'db/nqa_audit.sqlite') as c:
        assert c.execute("select is_active from sieve_runs where run_id='RUN-20260101-01'").fetchone()[0]==1
        assert c.execute("select rating from criterion_evaluations where criterion_id='APP_B_XVII'").fetchone()[0]=='unmet'
    with pytest.raises(ValueError,match='journal'):
        promote.apply(root,p,'out/promotion')


@pytest.mark.parametrize('name',['New Company','Čista tvrtka'])
@pytest.mark.parametrize('sibling',[True,False])
def test_neutral_root(ready,name,sibling):
    root=ready;new=root.with_name(name);root.rename(new)
    other=new.with_name('Sibling')
    if sibling: other.mkdir();(other/'keep').write_text('unchanged')
    p=promote.prepare(new,'assessment.json');promote.apply(new,p,'out/promotion')
    if sibling: assert (other/'keep').read_text()=='unchanged'
