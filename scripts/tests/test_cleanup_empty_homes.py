import hashlib
import json
from pathlib import Path
import sys
import subprocess

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import cleanup_empty_homes as tool


def fixture(root, supplier='Vendor Ž'):
    folder = root / supplier / 'out/date/empty'
    folder.mkdir(parents=True)
    (root / supplier / 'backup').mkdir()
    plan = tool.prepare(root, supplier, 'fixture-1')
    approval = {'schema': 'cleanup-authorization-1', 'root': str(root),
                'plan_sha256': tool.migration.plan_hash(plan), 'allow_apply': True,
                'owner_decision': 'FIXTURE-OWNER', 'review_decision': 'FIXTURE-REVIEW'}
    journal = root / supplier / 'work/migrations/fixture-1/directories.jsonl'
    return plan, approval, journal


@pytest.mark.parametrize('supplier', ['Vendor Ž', 'Company With Spaces'])
def test_native_apply_retry_undo_preserves_directory_tree_permissions(tmp_path, supplier):
    plan, approval, journal = fixture(tmp_path, supplier)
    before = tool.tree(tmp_path, supplier + '/out')
    assert tool.preview(tmp_path, plan)['ready']
    assert not journal.exists()
    tool.run(tmp_path, plan, journal, approval)
    tool.run(tmp_path, plan, journal, approval)
    assert not (tmp_path / supplier / 'out').exists()
    assert (tmp_path / supplier / 'work/backup').is_dir()
    assert tool.tree(tmp_path, supplier + '/work/migrations/fixture-1/empty-original-homes/out') == before
    tool.run(tmp_path, plan, journal, undo=True)
    tool.run(tmp_path, plan, journal, undo=True)
    assert tool.tree(tmp_path, supplier + '/out') == before


def test_pending_files_allow_preparation_not_application(tmp_path):
    source = tmp_path / 'Vendor/out/date/record.txt'
    source.parent.mkdir(parents=True)
    source.write_bytes(b'owner record')
    file_map = {'schema': 'cleanup-file-map-1', 'files': [
        {'source': 'Vendor/out/date/record.txt', 'destination': 'Vendor/work/validation/date/record.txt',
         'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}]}
    plan = tool.prepare(tmp_path, 'Vendor', 'fixture-1', file_map)
    assert not tool.preview(tmp_path, plan)['ready']
    approval = {'schema': 'cleanup-authorization-1', 'root': str(tmp_path),
                'plan_sha256': tool.migration.plan_hash(plan), 'allow_apply': True,
                'owner_decision': 'FIXTURE-OWNER', 'review_decision': 'FIXTURE-REVIEW'}
    journal = tmp_path / 'Vendor/work/migrations/fixture-1/directories.jsonl'
    with pytest.raises(ValueError, match='files remain'):
        tool.run(tmp_path, plan, journal, approval)
    assert not journal.exists()
    moved = tmp_path / file_map['files'][0]['destination']
    moved.parent.mkdir(parents=True)
    source.rename(moved)
    tool.run(tmp_path, plan, journal, approval)
    assert not (tmp_path / 'Vendor/out').exists()


def test_whole_batch_preflight_refuses_new_file_before_any_move(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    (tmp_path / 'Vendor Ž/out/owner.txt').write_bytes(b'keep')
    with pytest.raises(ValueError, match='files remain'):
        tool.run(tmp_path, plan, journal, approval)
    assert (tmp_path / 'Vendor Ž/backup').exists()
    assert not journal.exists()


def test_undo_refuses_new_owner_folder_without_overwrite(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    tool.run(tmp_path, plan, journal, approval)
    (tmp_path / 'Vendor Ž/out').mkdir()
    with pytest.raises(ValueError, match='collision'):
        tool.run(tmp_path, plan, journal, undo=True)
    assert (tmp_path / 'Vendor Ž/work/backup').exists()


def test_interrupted_native_rename_can_retry(tmp_path, monkeypatch):
    plan, approval, journal = fixture(tmp_path)
    original = tool.native_move
    calls = []
    def interrupted(source, target):
        if calls:
            raise OSError('interrupted')
        calls.append(source)
        original(source, target)
    monkeypatch.setattr(tool, 'native_move', interrupted)
    with pytest.raises(OSError):
        tool.run(tmp_path, plan, journal, approval)
    monkeypatch.setattr(tool, 'native_move', original)
    tool.run(tmp_path, plan, journal, approval)
    tool.run(tmp_path, plan, journal, undo=True)


def test_foreign_target_and_wrong_approval_refused(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    approval['plan_sha256'] = 'wrong'
    with pytest.raises(ValueError, match='authorization'):
        tool.run(tmp_path, plan, journal, approval)
    assert not journal.exists()
    plan['directories'][0]['destination'] = 'Other/work/backup'
    with pytest.raises(ValueError, match='destination'):
        tool.preview(tmp_path, plan)


def test_acl_or_empty_tree_shape_drift_refused_before_any_move(tmp_path, monkeypatch):
    plan, approval, journal = fixture(tmp_path)
    original = tool.acl_hash
    monkeypatch.setattr(tool, 'acl_hash', lambda path: 'changed descriptor')
    with pytest.raises(ValueError, match='ACL changed'):
        tool.run(tmp_path, plan, journal, approval)
    assert not journal.exists()
    monkeypatch.setattr(tool, 'acl_hash', original)
    (tmp_path / 'Vendor Ž/out/new-owner-folder').mkdir()
    with pytest.raises(ValueError, match='shape'):
        tool.run(tmp_path, plan, journal, approval)
    assert not journal.exists()


def test_cli_blocked_preview_returns_nonzero(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    (tmp_path / 'Vendor Ž/out/file.txt').write_bytes(b'keep')
    filename = tmp_path / 'plan.json'
    filename.write_text(json.dumps(plan), encoding='utf-8')
    result = subprocess.run([sys.executable, str(Path(tool.__file__)), '--root', str(tmp_path),
                             '--mode', 'preview', '--plan', str(filename)], capture_output=True, text=True)
    assert result.returncode == 1
    assert json.loads(result.stdout)['ready'] is False
