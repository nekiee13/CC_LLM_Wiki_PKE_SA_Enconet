"""Company-isolation and preservation tests for the coherent reuse release."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys

import pytest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))


def release():
    import framework_release
    return framework_release


@pytest.mark.parametrize('name', ['Acme Engineering', 'Žuti dobavljač'])
@pytest.mark.parametrize('sibling', [False, True])
def test_local_install_and_retry(tmp_path, name, sibling):
    r = release()
    target = tmp_path / name
    target.mkdir()
    other = tmp_path / 'Other company'
    if sibling:
        other.mkdir()
        (other / 'keep.txt').write_text('other evidence')
    spec = r.spec()
    before = list(target.iterdir())
    r.preview(target, spec)
    assert list(target.iterdir()) == before
    result = r.apply(target, 'install-1', spec)
    assert result['created']
    assert r.apply(target, 'install-2', spec)['created'] == []
    with pytest.raises(r.BootstrapError):
        r.apply(target, 'install-2', spec)
    assert not (target / 'db/nqa_audit.sqlite').exists()
    assert (target / 'manifests/approvals.csv').read_text().count('\n') == 1
    assert 'active: {}' in (target / 'sieving/prompts/active.yml').read_text()
    # Normal runtime needs no sibling code and works from an unrelated CWD.
    for script in ('full_keyword_sweep.py', 'build_vendor_dashboard.py', 'build_dark_dashboard.py', 'reset_audit.py'):
        run = subprocess.run([sys.executable, str(target / 'scripts' / script), '--help'],
                             cwd=tmp_path, capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
    if sibling:
        assert (other / 'keep.txt').read_text() == 'other evidence'


def test_conflict_blocks_entire_apply(tmp_path):
    r = release()
    (tmp_path / 'scripts').mkdir()
    original = tmp_path / 'scripts/full_keyword_sweep.py'
    original.write_text('owner work')
    with pytest.raises(r.BootstrapError):
        r.apply(tmp_path, 'conflict', r.spec())
    assert original.read_text() == 'owner work'
    assert not (tmp_path / '.bootstrap').exists()


def test_release_has_no_company_evidence_or_approvals():
    r = release()
    manifest = r.load_manifest(r.spec())
    paths = {e['path'] for e in manifest['files']}
    assert not any(p.startswith(('raw/', 'out/', 'outputs/', 'coordination/', '.claude/')) for p in paths)
    assert 'CLAUDE.md' not in paths
    assert 'scripts/build_vendor_dashboard.py' in paths
    assert 'scripts/reset_audit.py' in paths
    assert 'templates/vendor-dashboard.html' in paths
    import yaml
    registry = yaml.safe_load((r.spec().bundle / 'schemas/audit_commands.yml').read_text())
    assert all(p in paths for command in registry['commands'].values() for p in command['scripts'])


def test_reset_covers_latest_outputs_but_preserves_framework(tmp_path):
    r = release()
    r.apply(tmp_path, 'reset-test', r.spec())
    script = tmp_path / 'scripts/reset_audit.py'
    sys.path.insert(0, str(script.parent))
    spec = importlib.util.spec_from_file_location('portable_reset', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ('incoming/source.md', 'raw/old.md', 'out/2026-01-01/dashboard.html',
                 'sieving/candidates/old.json', 'docs/reviews/keep.md', 'coordination/archive/keep.md'):
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('fixture')
    registry = tmp_path / 'manifests/raw_sources.csv'
    registry.write_text(module.RESET_TEXT_FILES['manifests/raw_sources.csv'] + '\nDOC-0001,old\n')
    plan = module.build_plan(tmp_path)
    names = {p['relative_path'] for p in plan['candidates']}
    assert 'out/2026-01-01/dashboard.html' in names
    assert 'sieving/candidates/old.json' in names
    assert not any(p.startswith(('incoming/', 'scripts/', 'docs/', 'coordination/')) for p in names)
    external = tmp_path.parent / (tmp_path.name + '-plan.json')
    module.write_plan(plan, external)
    with pytest.raises(module.ResetError):
        module.apply_plan(external, tmp_path, None, confirmation='RESET-EKONERG-NO-BACKUP')
    backups = tmp_path.parent / (tmp_path.name + '-backups')
    result = module.apply_plan(external, tmp_path, backups, confirmation=module.CONFIRMATION)
    assert Path(result['backup']).is_file()
    assert (tmp_path / 'incoming/source.md').read_text() == 'fixture'
    assert (tmp_path / 'docs/reviews/keep.md').exists()
    assert (tmp_path / 'coordination/archive/keep.md').exists()
    assert not (tmp_path / 'out/2026-01-01/dashboard.html').exists()
    assert registry.read_text() == module.RESET_TEXT_FILES['manifests/raw_sources.csv'] + '\n'


def test_template_neutral_and_preserves_interactions():
    source = (release().spec().bundle / 'templates/vendor-dashboard.html').read_text(encoding='utf-8')
    assert all(name not in source.casefold() for name in ('ekonerg', 'enconet', 'tekol', '1499', '83.3%'))
    for hook in ('renderCards', 'renderMatrix', 'expandAll', 'collapseAll', 'printBtn', 'chapterText'):
        assert hook in source


@pytest.mark.parametrize('company,run_id,count,score', [
    ('Enconet','RUN-20260728-01',234,87.5),
    ('Ekonerg','RUN-20261003-32',475,77.8)])
def test_existing_audits_read_only(company, run_id, count, score, tmp_path):
    # Regression against existing evidence, opened with SQLite mode=ro.
    script = TEMPLATE / 'runtime_v2/build_vendor_dashboard.py'
    spec = importlib.util.spec_from_file_location('portable_dashboard', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    project = TEMPLATE.parent / company
    if company == 'Enconet':
        # This is a fixed historical characterization, not a query against the
        # new audit created after the owner-approved reset. Preserve every
        # expected assertion and use the genuine checksum-verified old DB.
        history_path = TEMPLATE.parent/'Enconet/scripts/regression_fixture.py'
        history_spec = importlib.util.spec_from_file_location('v2_history_fixture',history_path)
        history = importlib.util.module_from_spec(history_spec)
        history_spec.loader.exec_module(history)
        history.validate_archive()
        from zipfile import ZipFile
        project = tmp_path/'Enconet-history'
        (project/'db').mkdir(parents=True)
        with ZipFile(history.ARCHIVE) as archive:
            (project/'db/nqa_audit.sqlite').write_bytes(archive.read('db/nqa_audit.sqlite'))
            for relative in archive.namelist():
                if relative.startswith('raw/'):
                    target = (project/relative).resolve()
                    assert target.is_relative_to(project.resolve())
                    target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(archive.read(relative))
            (project/'schemas').mkdir()
            # Reset archives data, not preserved framework files. Retrieve the
            # genuine matching model from the v2 build's pinned pre-reset Git tip.
            model = subprocess.check_output(['git','show',
                'c3baa9e2d7c82e2c39ebfad822776266c8ebf183:Enconet/schemas/scoring_model.yml'],
                cwd=TEMPLATE.parent)
            (project/'schemas/scoring_model.yml').write_bytes(model)
    data = module.dataset(project, run_id)
    assert data['vendor_total'] == count
    assert data['score'] == score
    assert len(data['data']) == 18
    assert all(d['score_crumbs'] for d in data['data'] if d['rating'] in ('fully','substantially'))


def test_clean_intake_fixture(tmp_path):
    import sqlite3
    r = release()
    r.apply(tmp_path,'intake-test',r.spec())
    def cli(name,*args):
        result = subprocess.run([sys.executable,str(tmp_path/'scripts'/name),*args],cwd=tmp_path,
                                capture_output=True,text=True,encoding='utf-8')
        assert result.returncode == 0,result.stdout+result.stderr
        return result.stdout
    cli('init_db.py')
    with sqlite3.connect(tmp_path/'db/nqa_audit.sqlite') as conn:
        assert conn.execute('SELECT count(*) FROM criteria').fetchone()[0] == 18
        assert conn.execute('SELECT count(*) FROM approved_sources').fetchone()[0] == 0
    source = tmp_path/'incoming/source.md'
    source.write_text('# Quality procedure\n\nApproved work is checked and records retained.\n',encoding='utf-8')
    opts = ('source.md','--title','Fixture','--supplier','Synthetic','--language','en','--side','DOCUMENT')
    cli('promote_source.py',*opts)
    assert not (tmp_path/'raw/source.md').exists()
    cli('promote_source.py',*opts,'--apply')
    assert source.is_file() and (tmp_path/'raw/source.md').read_bytes() == source.read_bytes()
    cli('extract_text.py','DOC-0001','--apply')
    cli('chunk_document.py','DOC-0001','--apply')
    cli('full_keyword_sweep.py','--output',str(tmp_path/'out/sweep'))
    result = json.loads((tmp_path/'out/sweep/manifest.json').read_text())
    assert result['totals']['DOCUMENT']['documents'] == 1
    assert result['database_imported'] is False
    assert result['semantic_review_complete'] is False


@pytest.mark.parametrize('name', ['Acme Engineering','Žuti dobavljač'])
def test_company_scaffold_is_pending_and_preview_is_read_only(tmp_path, monkeypatch, name):
    import prepare_vendor
    import yaml
    monkeypatch.setattr(prepare_vendor,'WORKSPACE',tmp_path)
    target = tmp_path/name
    plan = prepare_vendor.setup(target,name)
    assert not target.exists()
    assert plan['source_selection_status'] == 'pending-owner'
    prepare_vendor.setup(target,name,'fixture-setup')
    state = yaml.safe_load((target/'project-state.yml').read_text(encoding='utf-8'))
    assert state['supplier'] == name
    assert state['phase'] == 'setup'
    assert all(g['status']=='pending' for g in state['gates'].values())
    assert not (target/'CLAUDE.md').exists()
    assert not (target/'db/nqa_audit.sqlite').exists()
    assert json.loads((target/'framework-company.json').read_text(encoding='utf-8'))['regulatory_editions'] == {}
