"""Hash-bound first-publication fixtures, not actual owner authorizations."""
import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest


def candidate(tmp_path):
    spec = importlib.util.spec_from_file_location('publication_builder', Path(__file__).parents[1] / 'prepare_framework_candidate_v4.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    project = tmp_path / 'Žuti publication test'
    module.build(project)
    return project


@pytest.mark.parametrize('failure', [False, True])
def test_first_publication_preview_apply_or_rollback(tmp_path, failure):
    project = candidate(tmp_path)
    probe = tmp_path / 'publication.py'
    probe.write_text('''
import csv,hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'))
import publish_audit_release as publisher
run='RUN-20261010-03'
source=root/'work/validation/source.html';source.parent.mkdir(parents=True)
source.write_bytes(b'synthetic publication fixture, not an audit result')
contract={'schema_version':1,'run_id':run,'review_status':'deferred',
          'owner_exception':'PUBLICATION-'+run,'gate_approvals':['G5-'+run,'G6-'+run],
          'result_manifest':'work/manifests/synthetic-release.json',
          'artifacts':[{'source':source.relative_to(root).as_posix(),
                        'destination':'outputs/'+run+'/dashboard_light.html',
                        'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]}
plan=root/'work/validation/plan.json';plan.write_text(json.dumps(contract),encoding='utf-8')
try:
    publisher.publish(plan)
except ValueError:
    pass
else:
    raise AssertionError('Missing approvals accepted')
assert not (root/'outputs').exists()
with (root/'work/manifests/approvals.csv').open('a',encoding='utf-8',newline='') as stream:
    writer=csv.writer(stream)
    for ref in contract['gate_approvals']+[contract['owner_exception']]:
        writer.writerow([ref,'approved','2000-01-01','project-owner',
                         'SYNTHETIC ONLY review deferred contract_sha256='+publisher.fingerprint(contract)])
preview=publisher.publish(plan)
assert preview['preview'] and not (root/'outputs').exists()
def validator():
    if sys.argv[2]=='fail':
        raise ValueError('synthetic validation failure')
try:
    result=publisher.publish(plan,execute=True,validator=validator)
except ValueError:
    assert sys.argv[2]=='fail'
    assert not (root/contract['artifacts'][0]['destination']).exists()
    assert not (root/contract['result_manifest']).exists()
else:
    assert sys.argv[2]=='pass'
    assert (root/contract['artifacts'][0]['destination']).read_bytes()==source.read_bytes()
    assert (root/contract['result_manifest']).is_file()
    try:
        publisher.publish(plan,execute=True,validator=validator)
    except ValueError:
        pass
    else:
        raise AssertionError('Repeat publication accepted')
assert not (root/'manifests').exists()
print('passed')
''', encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', str(probe), str(project), 'fail' if failure else 'pass'],
                            cwd=tmp_path, capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == 'passed'


@pytest.mark.parametrize('mode', ['success', 'validator-fails', 'artifact-changes', 'marker-permission-fails'])
def test_snapshot_seal_never_deletes_existing_artifact(tmp_path, mode):
    project = candidate(tmp_path)
    probe = tmp_path / 'snapshot.py'
    probe.write_text('''
import csv,hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'))
import publish_audit_release as publisher
run='RUN-20261010-03'
relative='outputs/'+run+'/dashboard_light.html'
artifact=root/relative;artifact.parent.mkdir(parents=True)
artifact.write_bytes(b'synthetic snapshot')
contract={'schema_version':1,'run_id':run,'review_status':'deferred',
          'owner_exception':'PUBLICATION-'+run,'gate_approvals':['G5-'+run,'G6-'+run],
          'result_manifest':'work/manifests/synthetic-release.json',
          'artifacts':[{'source':relative,'destination':relative,
                        'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}]}
with (root/'work/manifests/approvals.csv').open('a',encoding='utf-8',newline='') as stream:
    writer=csv.writer(stream)
    for ref in contract['gate_approvals']+[contract['owner_exception']]:
        writer.writerow([ref,'approved','2000-01-01','project-owner',
                         'SYNTHETIC ONLY review deferred contract_sha256='+publisher.fingerprint(contract)])
plan=root/'work/manifests/plan.json';plan.write_text(json.dumps(contract),encoding='utf-8')
assert publisher.publish(plan)['mode']=='seal-existing-snapshot'
assert not (root/contract['result_manifest']).exists()
def validator():
    if sys.argv[2]=='validator-fails':
        raise ValueError('test validation failure')
    if sys.argv[2]=='artifact-changes':
        artifact.write_bytes(b'owner edit simulated by test')
def permissions(path):
    if sys.argv[2]=='marker-permission-fails':
        raise OSError('test marker permissions failure')
try:
    publisher.publish(plan,execute=True,validator=validator,permissions=permissions)
except (ValueError,OSError):
    assert sys.argv[2]!='success'
    assert artifact.is_file()
    assert not (root/contract['result_manifest']).exists()
else:
    assert sys.argv[2]=='success'
    assert (root/contract['result_manifest']).is_file()
expected=b'owner edit simulated by test' if sys.argv[2]=='artifact-changes' else b'synthetic snapshot'
assert artifact.read_bytes()==expected
print('passed')
''', encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', str(probe), str(project), mode], cwd=tmp_path,
                            capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == 'passed'
