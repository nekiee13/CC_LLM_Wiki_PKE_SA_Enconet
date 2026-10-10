"""Synthetic-only end-to-end exercise of installed local v3 runtime.

Every document, approval and judgment below is generated for an isolated unit
test. None is a real regulatory source, vendor record, or owner authorization.
The script is NOT part of the release payload.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import yaml

root = Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'scripts'))
import evaluation_engine
import audit_state
import gap_register
import finding_workflow

commands = []
def cli(name,*args,expected=0):
    command = [sys.executable,'-B',str(root/'scripts'/name),*map(str,args)]
    result = subprocess.run(command,cwd=root.parent,capture_output=True,text=True,encoding='utf-8',errors='replace')
    commands.append({'command':command,'exit_code':result.returncode})
    assert result.returncode==expected,(name,result.stdout,result.stderr)
    return result.stdout

def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def approve(ref,notes='SYNTHETIC TEST ONLY'):
    with (root/'manifests/approvals.csv').open('a',encoding='utf-8',newline='') as stream:
        csv.writer(stream).writerow([ref,'approved','2026-10-10','project-owner',notes])

cli('init_db.py')
taxa = yaml.safe_load((root/'schemas/app_b_taxonomy.yml').read_text(encoding='utf-8'))['criteria']
state = yaml.safe_load((root/'project-state.yml').read_text(encoding='utf-8'))
supplier = state['supplier']
db = root/'db/nqa_audit.sqlite'
run = 'RUN-20261010-03'
for gate in range(1,7):
    approve(f'G{gate}-{run}','SYNTHETIC TEST ONLY; fixture-3')
    audit_state.record_gate_decision(f'G{gate}',f'G{gate}-{run}')
model = yaml.safe_load((root/'schemas/scoring_model.yml').read_text(encoding='utf-8'))
model.update(model_version='fixture-3',calibration_status='approved',approval_ref=f'G3-{run}')
(root/'schemas/scoring_model.yml').write_text(yaml.safe_dump(model,sort_keys=False),encoding='utf-8',newline='\n')
active = {'schema_version':'1.0','active':{'DOCUMENT':'appb_document_v3_context_anchors','RULE':'appb_rule_v1'}}
(root/'sieving/prompts/active.yml').write_text(yaml.safe_dump(active),encoding='utf-8',newline='\n')
with (root/'sieving/prompts/CHANGELOG.md').open('a',encoding='utf-8') as stream:
    stream.write('\nSynthetic local test activation: appb_document_v3_context_anchors; appb_rule_v1.\n')

for ordinal,side in enumerate(('DOCUMENT','RULE'),1):
    doc = f'DOC-{ordinal:04d}'
    sieve = f'RUN-20261010-{ordinal:02d}'
    filename = f'synthetic-{side}.md'
    sentences = [f'Synthetic {side.lower()} control {t["criterion_id"]}: work is checked and records kept for SYNTHETIC-PROJECT.' for t in taxa]
    content = '# Synthetic test-only document\n\n' + ''.join(f'## {t["criterion_id"]} {t["criterion_name"]}\n\n{s}\n\n' for t,s in zip(taxa,sentences))
    (root/'incoming'/filename).write_text(content,encoding='utf-8',newline='\n')
    original = (root/'incoming'/filename).read_bytes()
    cli('promote_source.py',filename,'--title','Synthetic fixture','--supplier',supplier,
        '--language','en','--side',side,'--apply')
    assert (root/'incoming'/filename).read_bytes()==original
    cli('extract_text.py',doc,'--apply')
    cli('chunk_document.py',doc,'--apply')
    authorities = [] if side=='DOCUMENT' else [{'authority_role':'GOVERNING','source_code':'10CFR50_APPB',
                  'source_locator':t['criterion_id']} for t in taxa]
    if side=='RULE':
        with sqlite3.connect(db) as conn:
            conn.execute('INSERT INTO approved_sources VALUES (?,?,?,?,?,?,?)',
                         ('10CFR50_APPB','GOVERNING','SYNTHETIC-ONLY',hashlib.sha256(original).hexdigest(),
                          f'G1-{run}','project-owner','2026-10-10'))
        contract_path = root/'schemas/sieving_contract.yml'
        contract = json.loads(contract_path.read_text(encoding='utf-8'))
        contract['canonical_codes'] = [{'ref_code':'10CFR50_APPB','authority_role':'GOVERNING',
                                       'allowed_locators':'criteria'}]
        contract_path.write_text(json.dumps(contract,indent=2)+'\n',encoding='utf-8',newline='\n')
    args = ['--run-id',sieve,'--doc-id',doc,'--document-side',side,'--prompt-version',active['active'][side]]
    for authority in authorities:
        args += ['--authority-json',json.dumps(authority)]
    cli('sieve_run.py',*args)
    items = []
    for index,(taxon,sentence) in enumerate(zip(taxa,sentences),1):
        item = {'item_id':f'I-{index}','criterion_id':taxon['criterion_id'],'criterion_name':taxon['criterion_name'],
                'statement':sentence,'item_type':'control' if side=='DOCUMENT' else 'requirement',
                'entities':{},'sources':[{'source_locator':taxon['criterion_id']}],
                'evidence_quotes':[{'quote_original':sentence,'quote_language':'en'}]}
        if side=='DOCUMENT':
            item.update(evidence_type='objective_record',context={'project_ref':'SYNTHETIC-PROJECT'})
        else:
            item['authority_references'] = [authorities[index-1]]
        items.append(item)
    payload = {'document':{'doc_id':doc,'name':'Synthetic fixture','date':'2026-10-10',
               'document_side':side,'authority_references':authorities},'items':items}
    target = root/'sieving/runs'/sieve/'generated.json'
    write_json(target,payload)
    cli('import_crumbs.py',target,'--run-id',sieve)
    cli('link_crumbs.py','--run-id',sieve,'--apply')
    cli('sieve_metrics.py','--run-id',sieve)

cli('full_keyword_sweep.py','--output',root/'out/synthetic-sweep')
cli('seed_requirements.py','--run-id','RUN-20261010-02','--apply')
with sqlite3.connect(db) as conn:
    assert conn.execute('SELECT count(*) FROM crumb_context').fetchone()[0]==18
    assert conn.execute('SELECT count(*) FROM crumb_chunk_links').fetchone()[0]==36
rulings = [{'criterion_id':t['criterion_id'],'applicable':True,'justification':'Synthetic test only',
             'scope_source_doc_id':'DOC-0002'} for t in taxa]
evaluation_engine.write_rulings(db,run_id=run,supplier=supplier,language='en',rulings=rulings,apply=True)
for index,taxon in enumerate(taxa):
    cid = taxon['criterion_id']
    row = {'criterion_id':cid,'classification':'fully' if index<17 else 'partially',
           'affirmative_summary':'Synthetic documented control','contrary_summary':'Synthetic real-audit check remains',
           'judge_ruling':'Synthetic documentary rating','rationale':'Synthetic only'}
    evaluation_engine.write_evaluation(db,run_id=run,record=row,
        evidence_ids=[f'CRUMB-DOC-0001-{cid}-0001'],apply=True)
cli('validate_evaluation.py','--run-id',run)
cid = 'APP_B_XVIII'
gap = {'gap_id':f'GAP-{cid}-01','evaluation_id':f'EVAL-{cid}','status':'partially-covered',
       'description':'Synthetic verification lead','evidence_item_id':f'CRUMB-DOC-0001-{cid}-0001',
       'missing_evidence_ref':None}
write_json(root/'out/gap.json',gap)
cli('gap_register.py',root/'out/gap.json','--apply')
voc = yaml.safe_load((root/'schemas/vocabularies.yml').read_text(encoding='utf-8'))['vocabularies']
finding = finding_workflow.write_finding(db,{'evaluation_run_id':run,'criterion_id':cid,
    'gap_id':gap['gap_id'],'title':'Synthetic test finding','body':'Synthetic evidence needs a sample.',
    'severity':voc['finding_severities']['values'][0],'confidence':voc['finding_confidences']['values'][0],
    'basis':'Synthetic control only','verification_status':'pending'})
approve(finding)
cli('approve.py',finding)
action = finding_workflow.write_action(db,{'evaluation_run_id':run,'finding_id':finding,
    'action_type':'verification','description':'Synthetic sample request; do not close automatically',
    'state':'open','priority':True})
approve(action)
cli('approve.py',action)
cli('validate_findings.py','--no-record')

slug = re.sub(r'[^a-z0-9_-]+','-',supplier.casefold()).strip('-')
candidate = root/'outputs/candidates/evidence_access'/run
candidate.mkdir(parents=True)
package = candidate/f'{slug}_appendix_b_evaluation_package.json'
viewer = candidate/f'{slug}_appendix_b_dashboard.html'
report = candidate/f'{slug}_appendix_b_evaluation_report.md'
data = candidate/f'{slug}_appendix_b_dashboard_data.json'
bundle = candidate/'evidence_bundle.json'
cli('build_evaluation_package.py','--run-id',run,'--output',package)
cli('generate_evidence_bundle.py','--package',package,'--db',db,'--run-id',run,
    '--generated-at-utc','2026-10-10T00:00:00Z','--output',bundle)
cli('generate_report.py',package,'--output',report,'--viewer-output',viewer,'--documentary')
cli('build_dashboard_data.py',package,'--output',data)
cli('generate_dashboard.py',package,data,'--output',viewer,'--evidence-bundle',bundle)
cli('validate_report_links.py',report,viewer,package)
cli('validate_dashboard.py',package,data,viewer,'--db',db,'--no-record')
cli('build_dark_dashboard.py','--source',viewer,'--output',candidate/'dark/dashboard_dark.html')
actual = json.loads(package.read_text(encoding='utf-8'))
assert actual['metrics']['consolidated_score']==97.2 and actual['run']['supplier']==supplier
assert '97.2' in viewer.read_text(encoding='utf-8') and '97.2' in report.read_text(encoding='utf-8')

entry = {'run_id':run,'status':'candidate'}
for kind,path in [('bundle',bundle),('package',package),('report',report),('viewer',viewer)]:
    entry[kind]=path.relative_to(root).as_posix()
    entry[kind+'_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
registry = root/'schemas/review_packages.yml'
registry.write_text(yaml.safe_dump({'schema_version':'1.0','packages':[entry]}),encoding='utf-8',newline='\n')
catalog = root/'outputs/candidates/evidence_access/review_catalog.json'
cli('generate_review_catalog.py','--output',catalog)
cli('build_review_package.py','--catalog',catalog)
cli('validate_review_package.py',root/'outputs/candidates/evidence_access/portable_package')
cli('browser_harness.py','check',viewer,'--artifacts',root/'out/browser','--require-interactive')
cli('browser_harness.py','check',candidate/'dark/dashboard_dark.html','--artifacts',root/'out/dark-browser','--require-interactive')
cli('validate_evidence_access_budgets.py',root/'outputs/candidates/evidence_access/portable_package',
    '--budgets',root/'schemas/evidence_access_budgets.yml')
cli_path = root/'out/publication.json'
import publish_audit_release
contract = {'schema_version':1,'run_id':run,'review_status':'deferred',
            'owner_exception':f'PUBLICATION-{run}','gate_approvals':[f'G5-{run}',f'G6-{run}'],
            'artifacts':[],'result_manifest':'manifests/synthetic-release.json'}
for source,destination in [(package,f'outputs/{package.name}'),(report,f'outputs/{report.name}'),
                           (data,f'outputs/{data.name}'),(viewer,f'outputs/{viewer.name}'),
                           (viewer,f'wiki/dashboards/{viewer.name}')]:
    contract['artifacts'].append({'source':source.relative_to(root).as_posix(),'destination':destination,
                                  'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
write_json(cli_path,contract)
approve(contract['owner_exception'],f'SYNTHETIC ONLY review deferred contract_sha256={publish_audit_release.fingerprint(contract)}')
for phase in ('registered','chunked','sieved','evidence_reviewed','evaluated','findings_drafted','findings_approved'):
    audit_state.transition(phase)
cli('publish_audit_release.py',cli_path)
cli('publish_audit_release.py',cli_path,'--execute','--allow-pending-claude')
for row in contract['artifacts']:
    assert hashlib.sha256((root/row['destination']).read_bytes()).hexdigest()==row['sha256']
cli('publish_audit_release.py',cli_path,'--execute','--allow-pending-claude',expected=1)
audit_state.transition('report_ready')
audit_state.transition('dashboard_ready')
cli('run_all_validations.py','--benchmarks','--no-record','--allow-pending-claude')
write_json(root/'out/synthetic-verification.json',{'synthetic_only':True,'supplier':supplier,
           'score':97.2,'vendor_crumbs':18,'quotes':36,'commands':commands,'passed':True})
print(json.dumps({'synthetic_only':True,'supplier':supplier,'score':97.2,'commands':len(commands),'passed':True}))
