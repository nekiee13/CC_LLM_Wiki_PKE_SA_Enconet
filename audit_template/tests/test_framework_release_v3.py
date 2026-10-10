"""The updated clean release must be local, versioned and evidence-free."""
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import framework_release
import prepare_vendor


def selected():
    return framework_release.spec(release='v3')


def test_v3_manifest_contains_complete_modern_delivery_stack():
    spec = selected()
    manifest = framework_release.load_manifest(spec)
    paths = {row['path'] for row in manifest['files']}
    assert manifest['template_version'] == '3.0.0'
    for name in ('build_review_package.py','generate_evidence_bundle.py','publish_audit_release.py',
                 'repair_release_permissions.ps1','generate_report.py','generate_dashboard.py',
                 'browser_harness.py','dashboard_dark.css'):
        assert 'scripts/'+name in paths
    assert 'schemas/evidence_access_budgets_v2.yml' in paths
    assert 'templates/dashboard-template.html' in paths
    assert not any(p.startswith(('raw/','out/','outputs/','coordination/','.claude/')) for p in paths)
    assert all('CLAUDE.md' not in p and '.sqlite' not in p and 'RUN-20' not in p for p in paths)
    assert 'scripts/sieve_generation.py' in paths and 'scripts/approve.py' in paths
    assert 'active: {}' in (spec.bundle/'sieving/prompts/active.yml').read_text()
    assert (spec.bundle/'manifests/approvals.csv').read_text().count('\n') == 1


@pytest.mark.parametrize('name',['Atlas Engineering','Žuti dobavljač'])
@pytest.mark.parametrize('sibling',[False,True])
def test_v3_setup_runtime_and_isolation(tmp_path, monkeypatch, name, sibling):
    monkeypatch.setattr(prepare_vendor,'WORKSPACE',tmp_path)
    target = tmp_path/name
    other = tmp_path/'Other Company'
    if sibling:
        other.mkdir()
        (other/'evidence.md').write_bytes(b'owner evidence')
    before_other = {p.relative_to(other).as_posix():(p.read_bytes(),p.stat().st_mtime_ns)
                    for p in other.rglob('*') if p.is_file()} if sibling else None
    prepare_vendor.setup(target,name,release='v3')
    assert not target.exists()
    prepare_vendor.setup(target,name,'v3-test',release='v3')
    assert prepare_vendor.setup(target,name,'v3-retry',release='v3')['created'] == []
    state = yaml.safe_load((target/'project-state.yml').read_text(encoding='utf-8'))
    assert state['supplier'] == name and state['phase'] == 'setup'
    assert all(g['status']=='pending' for g in state['gates'].values())
    assert json.loads((target/'framework-company.json').read_text(encoding='utf-8'))['framework_version']=='3.0.0'
    assert not (target/'db/nqa_audit.sqlite').exists()
    for tool in ('publish_audit_release.py','generate_evidence_bundle.py','build_review_package.py',
                 'generate_report.py','generate_dashboard.py','build_dark_dashboard.py','reset_audit.py'):
        result = subprocess.run([sys.executable,str(target/'scripts'/tool),'--help'],cwd=tmp_path,
                                capture_output=True,text=True,encoding='utf-8',errors='replace')
        assert result.returncode == 0, result.stdout+result.stderr
    result = subprocess.run([sys.executable,str(target/'scripts/init_db.py')],cwd=tmp_path,
                            capture_output=True,text=True,encoding='utf-8',errors='replace')
    assert result.returncode == 0, result.stdout+result.stderr
    result = subprocess.run([sys.executable,str(target/'scripts/audit_command.py'),'audit-status'],
                            cwd=tmp_path,capture_output=True,text=True,encoding='utf-8',errors='replace')
    assert result.returncode == 0,result.stdout+result.stderr
    if sibling:
        assert {p.relative_to(other).as_posix():(p.read_bytes(),p.stat().st_mtime_ns)
                for p in other.rglob('*') if p.is_file()} == before_other
    else:
        assert not other.exists()


def test_candidate_refresh_refuses_committed_payload_and_legacy_release(tmp_path):
    import prepare_framework_release_v3 as builder
    with pytest.raises(ValueError,match='uncommitted v3'):
        builder.build(TEMPLATE/'framework/v2',refresh_candidate=True)
    assert framework_release.load_manifest(framework_release.spec())['template_version']=='2.0.0'


def test_dependency_graph_is_complete_without_source_projects():
    import ast
    paths = {row['path'] for row in framework_release.load_manifest(selected())['files']}
    local = {Path(p).stem for p in paths if p.startswith('scripts/') and p.endswith('.py')}
    source_names = {p.stem for p in (TEMPLATE.parent/'Enconet/scripts').glob('*.py')}
    for path in paths:
        if path.startswith('scripts/') and path.endswith('.py'):
            tree = ast.parse((selected().bundle/path).read_text(encoding='utf-8'))
            imports = {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module}
            imports |= {a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
            assert not ((imports&source_names)-local),(path,(imports&source_names)-local)


def test_v3_conflict_preserves_existing_files(tmp_path):
    target = tmp_path/'Project'
    (target/'scripts').mkdir(parents=True)
    owner = target/'scripts/generate_report.py'
    owner.write_bytes(b'owner edits')
    with pytest.raises(ValueError):
        framework_release.apply(target,'conflict',selected())
    assert owner.read_bytes()==b'owner edits'
    assert not (target/'scripts/generate_dashboard.py').exists()


def test_v3_has_no_foreign_runtime_identity_or_approvals():
    spec = selected()
    for row in framework_release.load_manifest(spec)['files']:
        if row['path'].endswith(('.py','.yml','.json','.html','.css','.js','.ps1')):
            text = (spec.bundle/row['path']).read_text(encoding='utf-8').casefold()
            assert 'c:\\xpy' not in text and 'wikienconet' not in text,row['path']
            if row['path'].startswith('scripts/'):
                assert 'enconet' not in text and 'ekonerg' not in text,row['path']
    budgets = yaml.safe_load((spec.bundle/'schemas/evidence_access_budgets_v2.yml').read_text())
    assert budgets['size_bytes']['viewer']==1048576
    assert budgets['approval']['decision'] != 'approved'
    assert 'EVIDENCE-SIZE-LIMITS-20261009' not in str(budgets)


def test_v3_defaults_to_preview_and_does_not_replace_v2():
    before = framework_release.load_manifest(framework_release.spec())
    assert before['template_version']=='2.0.0'
    assert selected().journal_name == 'framework-v3'


@pytest.mark.parametrize('name',['Atlas Engineering','Žuti dobavljač'])
@pytest.mark.parametrize('sibling',[False,True])
def test_full_local_document_to_report_pipeline(tmp_path,monkeypatch,name,sibling):
    monkeypatch.setattr(prepare_vendor,'WORKSPACE',tmp_path)
    target = tmp_path/name
    other = tmp_path/'Other company'
    if sibling:
        other.mkdir()
        (other/'keep.md').write_bytes(b'owner original')
    before_other = {p.relative_to(other).as_posix():(p.read_bytes(),p.stat().st_mtime_ns)
                    for p in other.rglob('*') if p.is_file()} if sibling else None
    prepare_vendor.setup(target,name,'pipeline',release='v3')
    import os
    env = dict(os.environ,PLAYWRIGHT_BROWSERS_PATH=r'C:\xPY\vEnv\WikiEnconet\pw-browsers',PYTHONUTF8='1')
    result = subprocess.run([sys.executable,str(TEMPLATE/'tests/synthetic_audit_v3.py'),str(target)],
                            cwd=tmp_path,capture_output=True,text=True,encoding='utf-8',errors='replace',env=env)
    assert result.returncode==0,result.stdout+result.stderr
    evidence = json.loads((target/'out/synthetic-verification.json').read_text(encoding='utf-8'))
    assert evidence['passed'] and evidence['synthetic_only'] and evidence['score']==97.2
    if sibling:
        assert {p.relative_to(other).as_posix():(p.read_bytes(),p.stat().st_mtime_ns)
                for p in other.rglob('*') if p.is_file()} == before_other
    else:
        assert not other.exists()
