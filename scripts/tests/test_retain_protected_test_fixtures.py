import json
import os
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import retain_protected_test_fixtures as tool


def fixture(root):
    rows = []
    for number in range(15):
        source = tool.SOURCE + '/regression-fixture-' + str(number)
        folder = root / source
        folder.mkdir(parents=True)
        (folder / 'data.txt').write_bytes(('synthetic ' + str(number)).encode())
        rows.append(dict(source=source))
    target = root / rows[0]['source'] / 'empty'
    target.mkdir()
    (target.parent / 'current').symlink_to(target, target_is_directory=True)
    baseline = root / tool.BASELINE
    baseline.parent.mkdir(parents=True)
    baseline.write_text(json.dumps(dict(held=rows)), encoding='utf-8')
    authority = root / 'authority.md'
    authority.write_bytes(b'synthetic specific parent-move permission')
    return authority, tool.prepare(root, authority)


def test_native_fixture_move_retry_verify_undo_preserves_files_links_acls(tmp_path):
    authority, plan = fixture(tmp_path)
    for mode in ('apply', 'apply', 'verify', 'undo', 'undo'):
        result = tool.run(tmp_path, plan, authority, mode)
        assert result['files'] == 15 and result['shortcuts'] == 1 and result['preserved']
    assert tool.prepare(tmp_path, authority) == plan


def test_fixture_exception_is_limited_to_exact_parent_homes(tmp_path):
    fixture(tmp_path)
    # Check an absent generated path without creating Claude-owned files.
    allowed = tool.SOURCE + '/regression-fixture-0/.claude/commands/check.md'
    assert tool.fixture_path(tmp_path, allowed).is_relative_to(tmp_path / tool.SOURCE)
    for path in ('Enconet/.claude/config.yml', 'Enconet/.test-tmp-foreign/x',
                 tool.SOURCE + '/../.claude/config.yml', tool.SOURCE + '/.git/config'):
        with pytest.raises(ValueError):
            tool.fixture_path(tmp_path, path)


@pytest.mark.parametrize('change', ['file', 'membership', 'authority', 'baseline', 'destination'])
def test_changed_fixture_or_authority_blocks_before_any_rename(tmp_path, change):
    authority, plan = fixture(tmp_path)
    if change == 'file':
        next((tmp_path / tool.SOURCE).glob('*/data.txt')).write_bytes(b'changed')
    elif change == 'membership':
        (tmp_path / tool.SOURCE / 'unexpected').mkdir()
    elif change == 'authority':
        authority.write_bytes(b'changed authority')
    elif change == 'baseline':
        (tmp_path / tool.BASELINE).write_text('{}')
    else:
        plan['destination'] = 'AnotherSupplier/.tmp/foreign'
    with pytest.raises(ValueError):
        tool.run(tmp_path, plan, authority, 'apply')
    assert (tmp_path / tool.SOURCE).exists()
    assert not (tmp_path / tool.DESTINATION).exists()


def test_external_shortcut_hardlink_and_destination_collision_are_refused(tmp_path):
    authority, _ = fixture(tmp_path)
    root = tmp_path / tool.SOURCE
    folder = root / 'regression-fixture-0'
    outside = tmp_path / 'owner'
    outside.mkdir()
    shortcut = folder / 'external'
    shortcut.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match='External shortcut'):
        tool.prepare(tmp_path, authority)
    shortcut.unlink()  # Disposable synthetic shortcut only.
    os.link(folder / 'data.txt', folder / 'alias.txt')
    with pytest.raises(ValueError, match='Hard-linked'):
        tool.prepare(tmp_path, authority)
    (folder / 'alias.txt').unlink()
    (tmp_path / tool.DESTINATION).mkdir(parents=True)
    with pytest.raises(ValueError, match='collision'):
        tool.prepare(tmp_path, authority)


def test_failed_native_rename_is_retryable_without_partial_file_changes(tmp_path, monkeypatch):
    authority, plan = fixture(tmp_path)
    original = tool.scratch.homes.native_move
    def denied(*args):
        raise PermissionError('synthetic native denial')
    monkeypatch.setattr(tool.scratch.homes, 'native_move', denied)
    with pytest.raises(PermissionError):
        tool.run(tmp_path, plan, authority, 'apply')
    assert (tmp_path / tool.SOURCE).exists()
    monkeypatch.setattr(tool.scratch.homes, 'native_move', original)
    assert tool.run(tmp_path, plan, authority, 'apply')['preserved']
