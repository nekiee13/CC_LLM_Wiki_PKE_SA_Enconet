import copy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import cleanup_runtime_install as install


def fixture(root, supplier='Test vendor Ž'):
    (root / supplier / 'scripts').mkdir(parents=True)
    (root / '.tmp/payload').mkdir(parents=True)
    (root / supplier / 'scripts/runtime.py').write_bytes(b'old runtime\n')
    (root / '.tmp/payload/runtime.py').write_bytes(b'new runtime\n')
    (root / '.tmp/payload/helper.py').write_bytes(b'new helper\n')
    plan = install.prepare(root, supplier, [
        ('scripts/runtime.py', '.tmp/payload/runtime.py'),
        ('scripts/helper.py', '.tmp/payload/helper.py')], 'work/migrations/test/original')
    approval = {'schema': 'cleanup-authorization-1', 'root': str(root),
                'plan_sha256': install.migration.plan_hash(plan), 'allow_apply': True,
                'owner_decision': 'test owner approval', 'review_decision': 'test review'}
    journal = root / supplier / 'work/migrations/test/install.jsonl'
    return plan, approval, journal


@pytest.mark.parametrize('supplier', ['Test vendor Ž', 'Another company'])
def test_preview_apply_retry_undo_preserve_original_identity(tmp_path, supplier):
    plan, approval, journal = fixture(tmp_path, supplier)
    original = tmp_path / supplier / 'scripts/runtime.py'
    witness = install.migration.identity(original)
    sibling = tmp_path / 'Other/vendor.txt'
    sibling.parent.mkdir()
    sibling.write_bytes(b'not changed')
    assert install.preview(tmp_path, plan)['files'] == 2
    assert not journal.exists()
    assert install.run(tmp_path, plan, journal, approval)['state'] == 'installed'
    assert original.read_bytes() == b'new runtime\n'
    install.run(tmp_path, plan, journal, approval)
    install.run(tmp_path, plan, journal, undo=True)
    install.run(tmp_path, plan, journal, undo=True)
    assert original.read_bytes() == b'old runtime\n'
    assert install.migration.identity(original) == witness
    assert sibling.read_bytes() == b'not changed'
    assert not (tmp_path / supplier / 'scripts/helper.py').exists()


def test_retry_after_backup_before_payload_move(tmp_path, monkeypatch):
    plan, approval, journal = fixture(tmp_path)
    move = install.migration.move_no_replace
    def fail(source, destination):
        if source.name == 'runtime.py' and source.parent.name == 'payload':
            raise OSError('simulated interruption')
        move(source, destination)
    monkeypatch.setattr(install.migration, 'move_no_replace', fail)
    with pytest.raises(OSError):
        install.run(tmp_path, plan, journal, approval)
    monkeypatch.setattr(install.migration, 'move_no_replace', move)
    assert install.run(tmp_path, plan, journal, approval)['state'] == 'installed'
    install.run(tmp_path, plan, journal, undo=True)


def test_undo_preflights_all_files_before_mutation(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    install.run(tmp_path, plan, journal, approval)
    (tmp_path / plan['files'][0]['target']).write_bytes(b'owner edited')
    other = tmp_path / plan['files'][1]['target']
    before = other.read_bytes()
    with pytest.raises(ValueError, match='changed'):
        install.run(tmp_path, plan, journal, undo=True)
    assert other.read_bytes() == before


@pytest.mark.parametrize('bad', ['Other/scripts/runtime.py', 'Test vendor Ž/db/database.py',
                                'Test vendor Ž/scripts/CC_test.py', 'Test vendor Ž/../scripts/runtime.py'])
def test_unsafe_or_foreign_targets_refused(tmp_path, bad):
    plan, approval, journal = fixture(tmp_path)
    plan['files'][0]['target'] = bad
    with pytest.raises(ValueError):
        install.preview(tmp_path, plan)
    assert not journal.exists()


def test_wrong_authorization_or_backup_collision_writes_nothing(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    bad = copy.deepcopy(approval)
    bad['plan_sha256'] = 'wrong'
    with pytest.raises(ValueError, match='authorization'):
        install.run(tmp_path, plan, journal, bad)
    assert not journal.exists()
    backup = tmp_path / plan['files'][0]['backup']
    backup.parent.mkdir(parents=True)
    backup.write_bytes(b'collision')
    with pytest.raises(ValueError, match='collided'):
        install.run(tmp_path, plan, journal, approval)
    assert not journal.exists()


def test_layout_must_be_last(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    (tmp_path / '.tmp/payload/project-layout.json').write_bytes(b'{"layout":"v4"}')
    row = {'target': 'Test vendor Ž/project-layout.json', 'payload': '.tmp/payload/project-layout.json',
           'backup': 'Test vendor Ž/work/migrations/test/original/project-layout.json',
           'before_sha256': None, 'after_sha256': install.migration.digest(tmp_path / '.tmp/payload/project-layout.json')}
    plan['files'].insert(0, row)
    with pytest.raises(ValueError, match='last'):
        install.preview(tmp_path, plan)


def test_activation_refuses_legacy_homes_before_any_writes(tmp_path):
    plan, approval, journal = fixture(tmp_path)
    payload = tmp_path / '.tmp/payload/layout.json'
    payload.write_bytes(b'{"schema_version":1,"layout":"v4"}')
    plan['files'].append({'target': 'Test vendor Ž/project-layout.json',
                         'payload': '.tmp/payload/layout.json',
                         'backup': 'Test vendor Ž/work/migrations/test/original/project-layout.json',
                         'before_sha256': None, 'after_sha256': install.migration.digest(payload)})
    approval['plan_sha256'] = install.migration.plan_hash(plan)
    (tmp_path / 'Test vendor Ž/derived').mkdir()
    with pytest.raises(ValueError, match='not ready'):
        install.run(tmp_path, plan, journal, approval)
    assert not journal.exists()
    assert (tmp_path / 'Test vendor Ž/scripts/runtime.py').read_bytes() == b'old runtime\n'
