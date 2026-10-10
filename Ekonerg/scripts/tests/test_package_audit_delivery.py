"""Portable delivery is a read-only projection, not a new audit approval."""
import importlib.util
import json
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'package_audit_delivery.py'
spec = importlib.util.spec_from_file_location('package_audit_delivery', SCRIPT)
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)


def test_data_parser_refuses_stale_scores_and_changed_reason():
    row = dict(n='I', rating='fully', score=100, aff='a', con='c', judge='j', rationale='r', score_crumbs=[])
    evaluation = dict(criterion_id='APP_B_I', classification='fully', score=100,
                      affirmative_summary='a', contrary_summary='c', judge_ruling='j', rationale='r', evidence_ids=[])
    delivery.check_projection([row], [evaluation])
    with pytest.raises(ValueError, match='projection'):
        delivery.check_projection([{**row, 'score':75}], [evaluation])
    with pytest.raises(ValueError, match='projection'):
        delivery.check_projection([{**row, 'judge':'new judgment'}], [evaluation])


def test_output_cannot_be_canonical_foreign_or_redirected(tmp_path):
    root = tmp_path / 'Žuti Vendor'
    root.mkdir()
    with pytest.raises(ValueError):
        delivery.candidate_path(root, root / 'outputs/dashboard.html', 'RUN-1')
    with pytest.raises(ValueError):
        delivery.candidate_path(root, tmp_path / 'Other Vendor', 'RUN-1')
    assert delivery.candidate_path(root, root / 'outputs/candidates/evidence_access/RUN-1/review', 'RUN-1')


def test_no_clobber_write_rolls_back_only_own_created_files(tmp_path):
    output = tmp_path / 'delivery'
    manifest = delivery.write_new(output, {'one.txt':b'1', 'two.txt':b'2'}, {'state':'prepared'})
    assert manifest['state'] == 'prepared'
    assert delivery.verify(output)['files'] == 2
    with pytest.raises(FileExistsError):
        delivery.write_new(output, {'one.txt':b'changed'}, {})
    assert (output / 'one.txt').read_bytes() == b'1'
    (output / 'two.txt').write_bytes(b'tampered')
    with pytest.raises(ValueError, match='hash'):
        delivery.verify(output)


def test_mid_write_failure_preserves_racing_owner_file(tmp_path, monkeypatch):
    output = tmp_path / 'delivery'
    def inject(path, content):
        if path.name == 'two.txt':
            path.write_bytes(b'owner raced here')
        with path.open('xb') as stream:
            stream.write(content)
    monkeypatch.setattr(delivery, 'write_exclusive', inject)
    with pytest.raises(FileExistsError):
        delivery.write_new(output, {'one.txt':b'1', 'two.txt':b'2'}, {})
    assert not (output / 'one.txt').exists()
    assert (output / 'two.txt').read_bytes() == b'owner raced here'
    assert not (output / 'release_manifest.json').exists()


def test_report_keeps_score_reasons_and_clickable_crumbs():
    package = dict(run={'supplier':'Žuti Vendor','run_id':'RUN-1'},
                   metrics={'consolidated_score':75,'classification':'substantially',
                            'classification_counts':{'substantially':1}},
                   findings=[], actions=[], applicability=[])
    row = dict(n='I', title='Organization', rating='substantially', score=75,
               scale_points=4, summary='Reason', aff='Control', con='Open point',
               judge='Judgment', verify='Check record', score_crumb_ids=['CRUMB-1'],
               score_crumbs=[{'id':'CRUMB-1'}])
    text = delivery.render_documentary_export(package, [row], 'viewer.html')
    assert '75%' in text and 'Judgment' in text and 'Reason' in text
    assert 'viewer.html#crumb:CRUMB-1' in text
    assert 'not an issued G5/G6' in text
    assert 'No formal finding rows are recorded' in text


def test_real_projection_and_preview_preserve_all_input_bytes():
    root = Path(__file__).resolve().parents[2]
    paths = [root/'db/nqa_audit.sqlite', root/'project-state.yml', root/'manifests/approvals.csv',
             root/'out/2026-10-07/all18-review/EKONERG_DASHBOARD.html',
             root/'out/2026-10-07/dark-dashboard/grid/EKONERG_DASHBOARD_DARK.html']
    before = {str(p):delivery.sha(p.read_bytes()) for p in paths}
    result, files = delivery.prepare(root, 'RUN-20261003-32', paths[3], paths[4])
    assert result['score'] == 77.8 and result['score_points'] == 1400
    assert result['score_crumbs'] == 379
    assert result['formal_gate_status']['G5'] == 'pending'
    assert not (root/'outputs/candidates/evidence_access/RUN-20261003-32/delivery').exists()
    assert {str(p):delivery.sha(p.read_bytes()) for p in paths} == before
    assert json.loads(files['evidence_bundle.json'])['counts']['crumbs'] == 379


@pytest.mark.parametrize('name',['TEKOL Engineering','Žuti dobavljač'])
@pytest.mark.parametrize('sibling',[False,True])
def test_local_cli_synthetic_names_no_sibling_dependency(tmp_path, name, sibling):
    import yaml
    project = tmp_path/name
    for folder in ['scripts','db','raw','schemas','manifests','out']:
        (project/folder).mkdir(parents=True,exist_ok=True)
    for script in ['package_audit_delivery.py','report_stack_core.py']:
        shutil.copyfile(SCRIPT.parent/script,project/'scripts'/script)
    raw = ''.join(f'Synthetic control {i}.\n' for i in range(18))
    (project/'raw/source.md').write_text(raw,encoding='utf-8',newline='\n')
    source_hash = delivery.sha(raw.encode())
    model = dict(rating_weights=dict(fully=1,substantially=.75,partially=.5,minimally=.25,
                                    unmet=0,undetermined=0,na=None),
                 classification_thresholds=[dict(min_score=90,**{'class':'fully'}),dict(min_score=0,**{'class':'unmet'})])
    (project/'schemas/scoring_model.yml').write_text(yaml.safe_dump(model),encoding='utf-8')
    (project/'project-state.yml').write_text(yaml.safe_dump(dict(supplier=name,
        gates={f'G{i}':dict(status='approved' if i<4 else 'pending') for i in range(1,8)})),encoding='utf-8')
    (project/'manifests/approvals.csv').write_text(
        'object_id,decision,date,reviewer,notes\nG2-RUN-TEST,approved,2026-10-10,synthetic,fixture only\n'
        'G3-RUN-TEST,approved,2026-10-10,synthetic,fixture only\n',encoding='utf-8')
    data = []
    conn = sqlite3.connect(project/'db/nqa_audit.sqlite')
    conn.executescript((SCRIPT.parents[1]/'db/schema.sql').read_text(encoding='utf-8'))
    conn.execute('INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) VALUES(?,?,?,?,?,?,?)',
                 ('DOC-TEST','source.md','Synthetic source',name,'en','DOCUMENT',source_hash))
    conn.execute('INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side) VALUES(?,?,?,?)',
                 ('SIEVE-TEST','DOC-TEST','synthetic','DOCUMENT'))
    conn.execute('INSERT INTO evaluation_runs(run_id,supplier,deliverable_language,scoring_model_version) VALUES(?,?,?,?)',
                 ('RUN-TEST',name,'en','synthetic'))
    pos = 0
    for i,n in enumerate('I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII'.split()):
        text=f'Synthetic control {i}.\n'; cid='APP_B_'+n; item='CRUMB-'+n; chunk='CHUNK-'+n; qid='QUOTE-'+n
        conn.execute('INSERT INTO criteria VALUES(?,?,?)',(cid,'Criterion '+n,'synthetic only'))
        conn.execute('INSERT INTO document_chunks VALUES(?,?,?,?,?,?,?)',(chunk,'DOC-TEST',n,text,pos,pos+len(text),source_hash))
        pos+=len(text)
        conn.execute('INSERT INTO crumbs(item_id,doc_id,sieve_run_id,criterion_id,document_side,statement) VALUES(?,?,?,?,?,?)',
                     (item,'DOC-TEST','SIEVE-TEST',cid,'DOCUMENT',text))
        conn.execute('INSERT INTO crumb_quotes VALUES(?,?,?,?,?)',(qid,item,text,'en',n))
        conn.execute('INSERT INTO crumb_chunk_links VALUES(?,?,?,?,?)',(item,qid,chunk,'EXACT',1))
        conn.execute('INSERT INTO criterion_evaluations VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                     ('EVAL-'+n,'RUN-TEST',cid,'fully',100,1,1,1,1,1,1,'a','c','j','r'))
        conn.execute('INSERT INTO evaluation_evidence VALUES(?,?)',('EVAL-'+n,item))
        data.append(dict(n=n,title='Criterion '+n,rating='fully',score=100,scale_points=5,
                         aff='a',con='c',judge='j',rationale='r',summary='r',verify='v',score_crumb_ids=[item],
                         score_crumbs=[dict(id=item,quotes=[dict(quote_id=qid,text=text)],
                                           chapters=[dict(chunk_id=chunk,text=text)])]))
    conn.commit();conn.close()
    page='<html><head><title>'+name+'</title></head><body><script>const data = '+json.dumps(data)+';\nconst labels={};</script></body></html>'
    for theme in ['light','dark']:
        (project/'out'/f'{theme}.html').write_text(page,encoding='utf-8')
    other=tmp_path/'Other Company'
    if sibling:
        other.mkdir();(other/'owner.txt').write_bytes(b'untouched')
    before={p.relative_to(project).as_posix():(p.read_bytes(),p.stat().st_mtime_ns)
            for p in project.rglob('*') if p.is_file()}
    output=project/'outputs/candidates/evidence_access/RUN-TEST/delivery'
    result=subprocess.run([sys.executable,'-B',str(project/'scripts/package_audit_delivery.py'),
        '--run-id','RUN-TEST','--light',str(project/'out/light.html'),'--dark',str(project/'out/dark.html'),
        '--output',str(output),'--apply'],cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    assert delivery.verify(output)['score']==100
    assert all((project/p).read_bytes()==b and (project/p).stat().st_mtime_ns==t for p,(b,t) in before.items())
    assert (other/'owner.txt').read_bytes()==b'untouched' if sibling else not other.exists()
