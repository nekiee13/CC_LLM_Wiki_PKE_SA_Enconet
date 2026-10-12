"""Synthetic audit tests: fixtures are not real source or owner decisions."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

TEMPLATE = Path(__file__).parents[1]


def load_builder():
    spec = importlib.util.spec_from_file_location('pipeline_builder', TEMPLATE / 'prepare_framework_candidate_v4.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_runner():
    # Reuse the tested synthetic controls and scoring assertions, not vendor data.
    # Stop before the legacy multi-run catalog/publication portion: not yet v4.
    original = (TEMPLATE / 'tests/synthetic_audit_v3.py').read_text(encoding='utf-8')
    text = original.split("entry = {'run_id':run,'status':'candidate'}", 1)[0]
    replacements = {
        "root/'manifests/approvals.csv'": "root/'work/manifests/approvals.csv'",
        "root/'out/": "root/'work/validation/",
        "root/'outputs/candidates/evidence_access'/run": "root/'outputs'/run",
        "f'{slug}_appendix_b_evaluation_package.json'": "'evaluation_package.json'",
        "f'{slug}_appendix_b_dashboard.html'": "'dashboard_light.html'",
        "f'{slug}_appendix_b_evaluation_report.md'": "'report.md'",
        "f'{slug}_appendix_b_dashboard_data.json'": "'dashboard_data.json'",
        "candidate/'dark/dashboard_dark.html'": "candidate/'dashboard_dark.html'",
    }
    for old, new in replacements.items():
        assert old in text, old
        text = text.replace(old, new)
    # Keep legacy portable review tooling as an internal validation artifact;
    # the supplier-facing dashboards remain standalone under outputs/RUN-ID.
    review = original.split("entry = {'run_id':run,'status':'candidate'}", 1)[1].split("cli_path = root/'out/publication.json'", 1)[0]
    review = "entry = {'run_id':run,'status':'candidate'}" + review
    review = review.replace("root/'outputs/candidates/evidence_access/", "root/'work/reviews/")
    review = review.replace("root/'out/", "root/'work/validation/")
    review = review.replace("candidate/'dark/dashboard_dark.html'", "candidate/'dashboard_dark.html'")
    text += '\n' + review
    return text + '''
import generate_report
unapproved = dict(actual, approvals=[])
try:
    generate_report.require_report_gates(unapproved)
except ValueError:
    pass
else:
    raise AssertionError('Report gate was weakened')
import evidence_access_policy
from project_layout import path_at
try:
    path_at(root.parent/'Other Supplier','manifests')
except ValueError:
    pass
else:
    raise AssertionError('Foreign explicit root accepted')
for unsafe in (root/'outputs/flat.html', root/'outputs/candidates/evidence_access/old.html',
               root/'outputs'/run/'nested/file.html', root.parent/'Other Supplier/outputs'/run/'foreign.html'):
    try:
        evidence_access_policy.require_output_target(unsafe)
    except evidence_access_policy.PolicyError:
        pass
    else:
        raise AssertionError('Unsafe output accepted: '+str(unsafe))
cli('validate_chunks.py','--no-record')
cli('validate_traceability.py','--no-record')
cli('validate_raw_sources.py')
cli('validate_requirements.py','--no-record')
cli('../work/benchmarks/validate_benchmarks.py')
import reset_audit
work_receipts = ['benchmarks', 'reviews', 'decisions', 'migrations', 'archive', 'bootstrap']
for folder in work_receipts:
    path = root/'work'/folder/'retained.txt'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('retain this framework or history', encoding='utf-8')
before = {path.relative_to(root).as_posix():hashlib.sha256(path.read_bytes()).hexdigest()
          for path in root.rglob('*') if path.is_file()}
plan = reset_audit.build_plan(root)
targets = {row['relative_path']:row['action'] for row in plan['candidates']}
assert targets['work/manifests/raw_sources.csv']=='truncate'
assert targets['work/derived/DOC-0001.txt']=='delete'
assert not any(path.startswith('work/'+folder+'/') for path in targets for folder in work_receipts)
assert before == {path.relative_to(root).as_posix():hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in root.rglob('*') if path.is_file()}
cli('make_handoff.py','--status','partial','--objective','Synthetic test only',
    '--next-action','Synthetic check only','--index-state','not configured in test')
records = list((root/'coordination/handoffs').glob('*.md'))
assert len(records)==1
cli('make_handoff.py','--validate',records[0])
staleness = cli('make_handoff.py','--check-staleness')
assert 'does not resolve' not in staleness
import run_validation
assert run_validation._pointer_record() == records[0]
cli('agent_coord.py','status','--write')
board=(root/'coordination/BOARD.md').read_text(encoding='utf-8')
assert '(handoffs/' in board and '(coordination/handoffs/' not in board
cli('agent_coord.py','validate')
status = cli('audit_command.py','audit-status')
assert 'phase:' in status and 'last_validation:' in status
dry = cli('audit_command.py','--dry-run','audit-validate','--','--run-id',run,'--no-record','--allow-pending-claude')
assert 'run_all_validations.py' in dry
if supplier=='Atlas Engineering' and not (root.parent/'Other Supplier').exists():
    cli('browser_harness.py','check',viewer,'--artifacts',root/'work/validation/light-browser','--require-interactive')
    cli('browser_harness.py','check',candidate/'dashboard_dark.html','--artifacts',root/'work/validation/dark-browser','--require-interactive')
for phase in ('registered','chunked','sieved','evidence_reviewed','evaluated','findings_drafted','findings_approved'):
    audit_state.transition(phase)
import publish_audit_release as publisher
contract={'schema_version':1,'run_id':run,'review_status':'deferred',
          'owner_exception':'PUBLICATION-'+run,'gate_approvals':['G5-'+run,'G6-'+run],
          'result_manifest':'work/manifests/synthetic-release.json','artifacts':[]}
for source in (package,report,viewer,data,bundle,candidate/'dashboard_dark.html'):
    relative=source.relative_to(root).as_posix()
    contract['artifacts'].append({'source':relative,'destination':relative,
                                 'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
approval='SYNTHETIC ONLY review deferred contract_sha256='+publisher.fingerprint(contract)
approve(contract['owner_exception'],approval)
plan=root/'work/validation/publication.json'
write_json(plan,contract)
preview=cli('publish_audit_release.py',plan)
assert 'seal-existing-snapshot' in preview
execution=cli('publish_audit_release.py',plan,'--execute','--allow-pending-claude')
assert 'aggregate: PASS' in execution
assert json.loads((root/contract['result_manifest']).read_text())['mode']=='seal-existing-snapshot'
assert not list(root.glob('release-*'))
assert not list((root/'.tmp').glob('release-*'))
for row in contract['artifacts']:
    assert hashlib.sha256((root/row['destination']).read_bytes()).hexdigest()==row['sha256']
cli('publish_audit_release.py',plan,'--execute','--allow-pending-claude',expected=1)
audit_state.transition('report_ready')
audit_state.transition('dashboard_ready')
write_json(root/'work/validation/pipeline-verification.json', {'synthetic_only':True,'score':97.2,'passed':True,'commands':commands})
'''


@pytest.mark.parametrize('name', ['Atlas Engineering', 'Žuti dobavljač'])
@pytest.mark.parametrize('sibling', [False, True])
def test_full_documentary_pipeline_to_standalone_dashboards(tmp_path, name, sibling):
    project = tmp_path / name
    other = tmp_path / 'Other Supplier'
    if sibling:
        other.mkdir()
        (other / 'source.md').write_bytes(b'owner source remains untouched')
    before = (other / 'source.md').stat() if sibling else None
    load_builder().build(project)
    # Use the existing neutral fresh-state scaffold only for isolated test setup.
    sys.path.insert(0, str(TEMPLATE))
    import prepare_vendor
    for path, data in prepare_vendor.scaffold(name, release='v3').items():
        target = project / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    runner = tmp_path / 'synthetic-v4.py'
    runner.write_text(fixture_runner(), encoding='utf-8')
    env = {**os.environ, 'PLAYWRIGHT_BROWSERS_PATH': r'C:\xPY\vEnv\WikiEnconet\pw-browsers', 'PYTHONUTF8': '1'}
    result = subprocess.run([sys.executable, '-B', str(runner), str(project)], cwd=tmp_path, env=env,
                            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads((project / 'work/validation/pipeline-verification.json').read_text(encoding='utf-8'))
    assert evidence['synthetic_only'] and evidence['passed'] and evidence['score'] == 97.2
    output = project / 'outputs/RUN-20261010-03'
    for path in ['dashboard_light.html', 'dashboard_dark.html', 'report.md', 'evaluation_package.json',
                 'dashboard_data.json', 'evidence_bundle.json']:
        assert (output / path).is_file()
    assert '97.2' in (output / 'dashboard_dark.html').read_text(encoding='utf-8')
    assert not (output / 'index.html').exists()
    for old in ['out', 'derived', 'manifests', 'benchmarks', 'handoffs', 'outputs/candidates']:
        assert not (project / old).exists(), old
    if sibling:
        assert (other / 'source.md').read_bytes() == b'owner source remains untouched'
        assert (other / 'source.md').stat().st_mtime_ns == before.st_mtime_ns
    else:
        assert not other.exists()


@pytest.mark.parametrize('backup', [False, True])
def test_v4_reset_apply_retains_framework_and_history(tmp_path, backup):
    project = tmp_path / 'Test-only supplier'
    load_builder().build(project)
    (project / 'incoming').mkdir(exist_ok=True)
    files = {'incoming/owner.md': b'owner input', 'raw/registered.md': b'registered source',
             'work/derived/test.txt': b'derived',
             'work/reviews/record.md': b'review', 'work/decisions/owner.md': b'decision',
             'work/migrations/receipt.json': b'{}', 'work/archive/history.txt': b'history',
             'coordination/handoffs/record.md': b'handoff', 'outputs/RUN-20261010-03/report.md': b'report'}
    for path, data in files.items():
        target = project / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    import stat
    raw = project / 'raw/registered.md'
    raw.chmod(raw.stat().st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
    probe = tmp_path / 'reset-probe.py'
    probe.write_text('''
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'))
import reset_audit
plan=reset_audit.build_plan(root)
before={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob('*') if p.is_file()}
targets={row['relative_path'] for row in plan['candidates']}
assert 'work/derived/test.txt' in targets
assert 'outputs/RUN-20261010-03/report.md' in targets
assert not any(name.startswith(('work/benchmarks/','work/reviews/','work/decisions/',
                              'work/migrations/','work/archive/','coordination/','incoming/','scripts/')) for name in targets)
try:
    reset_audit.build_plan(root.parent)
except ValueError:
    pass
else:
    raise AssertionError('Foreign reset root accepted')
external=root.parent/'plan.json'
reset_audit.write_plan(plan,external)
backup=(root.parent/'backup') if sys.argv[2]=='yes' else None
token=reset_audit.CONFIRMATION if backup else reset_audit.NO_BACKUP_CONFIRMATION
result=reset_audit.apply_plan(external,root,backup,confirmation=token)
for name,digest in before.items():
    path=root/name
    if name not in targets:
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,name
assert not (root/'work/derived/test.txt').exists()
assert not (root/'raw/registered.md').exists()
assert len((root/'work/manifests/approvals.csv').read_text().splitlines())==1
if backup:
    from zipfile import ZipFile
    with ZipFile(result['backup']) as archive:
        for name in targets:
            assert hashlib.sha256(archive.read(name)).hexdigest()==before[name]
print(json.dumps({'synthetic_only':True,'passed':True,'backup':bool(backup)}))
''', encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', str(probe), str(project), 'yes' if backup else 'no'],
                            capture_output=True, text=True, encoding='utf-8', cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)['passed']
