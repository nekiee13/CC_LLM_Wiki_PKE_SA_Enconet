"""Copy boundaries for the portable requirement seed add-on."""
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bootstrap_requirement_seed as wrapper


@pytest.mark.parametrize('name', ['Company With Spaces', 'Županija audit'])
@pytest.mark.parametrize('with_sibling', [False, True])
def test_preview_apply_retry_are_local(tmp_path, name, with_sibling):
    target = tmp_path / name
    target.mkdir()
    marker = target / 'owner.txt'
    marker.write_bytes(b'preserve owner data')
    sibling = tmp_path / 'other supplier'
    if with_sibling:
        sibling.mkdir()
        (sibling / 'evidence.txt').write_bytes(b'other company evidence')
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in tmp_path.rglob('*') if p.is_file()}
    spec = wrapper.REQUIREMENT_SEED
    preview = wrapper.core.preview(target, spec)
    assert len(preview['files']) == 2
    assert not (target / 'scripts').exists()
    first = wrapper.core.apply(target, 'first-run', spec)
    assert len(first['created']) == 2
    retry = wrapper.core.apply(target, 'retry-run', spec)
    assert retry['created'] == [] and len(retry['preserved']) == 2
    for path, digest in before.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
    assert set(p.relative_to(target).as_posix() for p in (target / 'scripts').rglob('*.py')) == {
        'scripts/seed_requirements.py', 'scripts/tests/test_seed_requirements.py'}
    # A normal initialized audit already has these neutral foundation files.
    foundation = Path(__file__).resolve().parents[1] / 'framework' / 'v2'
    for relative in ['scripts/db_util.py', 'scripts/project_paths.py', 'schemas/id_patterns.yml']:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(foundation / relative, destination)
    (target / 'db').mkdir()
    database = target / 'db' / 'nqa_audit.sqlite'
    with sqlite3.connect(database) as conn:
        conn.executescript('''
            CREATE TABLE criteria (criterion_id TEXT PRIMARY KEY);
            CREATE TABLE sieve_runs (run_id TEXT PRIMARY KEY,is_active INTEGER);
            CREATE TABLE crumbs (item_id TEXT PRIMARY KEY,criterion_id TEXT,
                sieve_run_id TEXT,document_side TEXT,statement TEXT);
            CREATE TABLE requirements (requirement_id TEXT PRIMARY KEY,criterion_id TEXT,
                requirement_text TEXT,source_item_id TEXT,parent_requirement_id TEXT,
                is_subrequirement INTEGER);
            INSERT INTO criteria VALUES ('APP_B_I');
            INSERT INTO sieve_runs VALUES ('RUN-1',1);
            INSERT INTO crumbs VALUES ('CRUMB-DOC-0001-APP_B_I-0001','APP_B_I','RUN-1','RULE','Test rule');
        ''')
    command = [sys.executable, str(target / 'scripts' / 'seed_requirements.py'), '--run-id', 'RUN-1']
    def run(*arguments):
        result = subprocess.run(command + list(arguments), cwd=tmp_path,
                                capture_output=True, text=True, encoding='utf-8')
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)
    assert run()['mode'] == 'preview'
    with sqlite3.connect(database) as conn:
        assert conn.execute('SELECT COUNT(*) FROM requirements').fetchone()[0] == 0
    assert run('--apply')['inserted'] == 1
    assert run('--apply')['inserted'] == 0
    for path, digest in before.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
