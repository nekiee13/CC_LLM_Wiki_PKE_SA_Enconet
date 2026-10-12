import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import cleanup_workflow as workflow


def fixture(tmp_path):
    def git(*args):
        result = subprocess.run(['git', '-C', str(tmp_path), *args], capture_output=True)
        assert result.returncode == 0, result.stderr
        return result.stdout
    git('init', '-q')
    git('config', 'user.name', 'Synthetic fixture')
    git('config', 'user.email', 'fixture@example.invalid')
    source = tmp_path / 'Supplier/manifests/a.csv'
    source.parent.mkdir(parents=True)
    source.write_bytes(b'exact\r\n')
    (tmp_path / 'owner.txt').write_bytes(b'owner baseline')
    git('add', '--', 'Supplier/manifests/a.csv', 'owner.txt')
    git('commit', '-qm', 'Synthetic baseline')
    (tmp_path / 'owner.txt').write_bytes(b'owner dirty edit')
    untracked = tmp_path / 'Supplier/manifests/untracked.csv'
    untracked.write_bytes(b'not tracked')
    rows = [{'source': path.relative_to(tmp_path).as_posix(),
             'destination': 'Supplier/work/manifests/' + path.name,
             'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
             'owner': 'shared-or-owner', 'hold': None} for path in [source, untracked]]
    plan = workflow.prepare(tmp_path, {'schema': 'cleanup-file-map-1', 'files': rows, 'collisions': []},
                            ['Supplier/manifests'])
    approval = {'schema': 'cleanup-authorization-1', 'root': str(tmp_path),
                'plan_sha256': workflow.migration.plan_hash(plan), 'allow_apply': True,
                'owner_decision': 'SYNTHETIC', 'review_decision': 'SYNTHETIC'}
    return git, source, plan, approval


def test_stage_retry_undo_preserves_unrelated_dirty_and_untracked(tmp_path):
    git, source, plan, approval = fixture(tmp_path)
    journal = tmp_path / 'journal.jsonl'
    workflow.apply(tmp_path, plan, journal, approval)
    assert workflow.migration.verify(tmp_path, plan, journal)['complete']
    assert not source.parent.exists()
    assert 'Supplier/work/manifests/a.csv' in workflow.index(tmp_path)
    assert 'Supplier/work/manifests/untracked.csv' not in workflow.index(tmp_path)
    workflow.apply(tmp_path, plan, journal, approval)
    workflow.undo(tmp_path, plan, journal)
    assert source.read_bytes() == b'exact\r\n'
    assert (tmp_path / 'Supplier/manifests/untracked.csv').read_bytes() == b'not tracked'
    assert (tmp_path / 'owner.txt').read_bytes() == b'owner dirty edit'
    assert not git('diff', '--cached', '--name-only')


def test_git_history_follows_identical_rename(tmp_path):
    git, source, plan, approval = fixture(tmp_path)
    workflow.apply(tmp_path, plan, tmp_path / 'journal.jsonl', approval)
    git('commit', '-qm', 'Synthetic move')
    log = git('log', '--follow', '--format=%s', '--', 'Supplier/work/manifests/a.csv')
    assert b'Synthetic baseline' in log and b'Synthetic move' in log


def test_refuse_unrelated_staged_work_before_apply(tmp_path):
    git, source, plan, approval = fixture(tmp_path)
    git('add', '--', 'owner.txt')
    with pytest.raises(ValueError, match='index edit'):
        workflow.apply(tmp_path, plan, tmp_path / 'journal.jsonl', approval)
    assert source.exists()


def test_nonempty_source_directory_is_retained(tmp_path):
    git, source, plan, approval = fixture(tmp_path)
    (source.parent / 'CC_retained.md').write_bytes(b'Claude-owned record')
    result = workflow.apply(tmp_path, plan, tmp_path / 'journal.jsonl', approval)
    assert result['retained_directories'] == ['Supplier/manifests']
    assert (source.parent / 'CC_retained.md').read_bytes() == b'Claude-owned record'


def test_interrupted_git_batches_resume_without_staging_owner_edit(tmp_path, monkeypatch):
    git, source, plan, approval = fixture(tmp_path)
    rows = list(plan['files'])
    paths = []
    for number in range(80):
        name = f'{number:03d}-' + 'long-name-' * 7 + '.txt'
        path = source.parent / name
        path.write_bytes(str(number).encode())
        paths.append(path.relative_to(tmp_path).as_posix())
        rows.append({'source': paths[-1], 'destination': 'Supplier/work/manifests/' + name,
                     'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'owner': 'shared-or-owner', 'hold': None})
    git('add', '--', *paths)
    git('commit', '-qm', 'Synthetic many-file baseline')
    plan = workflow.prepare(tmp_path, {'schema': 'cleanup-file-map-1', 'files': rows, 'collisions': []})
    approval['plan_sha256'] = workflow.migration.plan_hash(plan)
    actual = workflow.git
    calls = 0
    def interrupted(root, *args):
        nonlocal calls
        if args[0] == 'add':
            calls += 1
            if calls == 2:
                raise ValueError('synthetic Git interruption')
        return actual(root, *args)
    monkeypatch.setattr(workflow, 'git', interrupted)
    journal = tmp_path / 'journal.jsonl'
    with pytest.raises(ValueError, match='interruption'):
        workflow.apply(tmp_path, plan, journal, approval)
    monkeypatch.setattr(workflow, 'git', actual)
    workflow.apply(tmp_path, plan, journal, approval)
    assert (tmp_path / 'owner.txt').read_bytes() == b'owner dirty edit'
    assert workflow.index(tmp_path)['owner.txt'] == plan['workflow']['index']['owner.txt']
    workflow.undo(tmp_path, plan, journal)
    assert not git('diff', '--cached', '--name-only')


def test_invalid_prune_scope_fails_before_any_move(tmp_path):
    git, source, plan, approval = fixture(tmp_path)
    plan['workflow']['prune_directories']['outside-scope'] = source.parent.stat().st_mode
    approval['plan_sha256'] = workflow.migration.plan_hash(plan)
    with pytest.raises(ValueError, match='prune scope'):
        workflow.apply(tmp_path, plan, tmp_path / 'journal.jsonl', approval)
    assert source.exists()
