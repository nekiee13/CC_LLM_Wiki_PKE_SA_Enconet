from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import archive_pytest_scratch as tool


def fixture(root):
    source = root / tool.SOURCE
    source.mkdir()
    for index in range(6):
        target = source / ('test_' + str(index))
        target.mkdir()
        (source / ('test_current_' + str(index))).symlink_to(target, target_is_directory=True)
    authority = root / 'authority.md'
    authority.write_bytes(b'synthetic owner authority')
    plan = dict(root=str(root), source=tool.SOURCE, destination=tool.DESTINATION,
                authority_sha256=tool.migration.digest(authority), witness=tool.witness(root, source))
    return plan, authority


def test_native_archive_retry_verify_undo_preserves_shortcuts_and_acls(tmp_path):
    plan, authority = fixture(tmp_path)
    for mode in ('apply', 'apply', 'verify', 'undo', 'undo'):
        result = tool.run(tmp_path, plan, authority, mode)
        assert result['preserved']
    assert tool.witness(tmp_path, tmp_path / tool.SOURCE) == plan['witness']


def test_added_regular_file_blocks_before_move(tmp_path):
    plan, authority = fixture(tmp_path)
    (tmp_path / tool.SOURCE / 'owner.md').write_bytes(b'keep')
    with pytest.raises(ValueError, match='Regular files'):
        tool.run(tmp_path, plan, authority, 'apply')
    assert (tmp_path / tool.SOURCE).exists()
    assert not (tmp_path / tool.DESTINATION).exists()


def test_foreign_shortcut_refused_without_following_it(tmp_path):
    plan, authority = fixture(tmp_path)
    outside = tmp_path / 'outside'
    outside.mkdir()
    # An additional redirect is refused even though its target is accessible.
    (tmp_path / tool.SOURCE / 'foreign').symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match='External shortcut'):
        tool.run(tmp_path, plan, authority, 'apply')
    assert (tmp_path / tool.SOURCE).exists()


def legacy_fixture(tmp_path):
    source = tmp_path / tool.LEGACY_TOP[0]
    source.mkdir(parents=True)
    target = source / 'test_0'
    target.mkdir()
    (source / 'test_current').symlink_to(target, target_is_directory=True)
    template = tmp_path / 'audit_template/tests/old-synthetic'
    template.mkdir(parents=True)
    authority = tmp_path / 'authority.md'
    authority.write_bytes(b'synthetic cleanup retry')
    return source, template, authority, tool.prepare_legacy(tmp_path, authority)


def test_legacy_batch_retry_verify_undo_and_original_pilot_contract(tmp_path):
    source, template, authority, plan = legacy_fixture(tmp_path)
    assert len(plan['rows']) == 2
    for mode in ('apply', 'apply', 'verify', 'undo', 'undo'):
        result = tool.run_legacy(tmp_path, plan, authority, mode)
        assert result['preserved'] and result['shortcuts'] == 1
    assert source.exists() and template.exists()
    assert tool.SOURCE == 'pytest-pilot-temp'


def test_legacy_added_file_blocks_all_moves(tmp_path):
    source, template, authority, plan = legacy_fixture(tmp_path)
    (template / 'owner.txt').write_bytes(b'keep')
    with pytest.raises(ValueError, match='Regular files'):
        tool.run_legacy(tmp_path, plan, authority, 'apply')
    assert source.exists() and template.exists()


def test_legacy_foreign_target_and_owner_authority_fail_before_move(tmp_path):
    source, template, authority, plan = legacy_fixture(tmp_path)
    plan['rows'][-1]['destination'] = 'AnotherSupplier/.tmp/foreign'
    with pytest.raises(ValueError, match='Foreign legacy'):
        tool.run_legacy(tmp_path, plan, authority, 'apply')
    assert source.exists() and template.exists()
    authority.write_bytes(b'changed')
    with pytest.raises(ValueError, match='authority'):
        tool.run_legacy(tmp_path, plan, authority, 'apply')


def test_legacy_protected_files_and_real_fixture_files_remain_held(tmp_path):
    source, template, authority, _ = legacy_fixture(tmp_path)
    protected = tmp_path / 'Enconet/.test-tmp/regression-held/.claude'
    protected.mkdir(parents=True)
    (protected / 'note.md').write_bytes(b'Claude owned')
    (template / 'fixture.db').write_bytes(b'synthetic test data')
    plan = tool.prepare_legacy(tmp_path, authority)
    assert len(plan['rows']) == 1
    assert len(plan['held']) == 2
    tool.run_legacy(tmp_path, plan, authority, 'apply')
    assert (protected / 'note.md').read_bytes() == b'Claude owned'
    assert (template / 'fixture.db').read_bytes() == b'synthetic test data'


def test_legacy_external_shortcut_is_held_and_never_followed(tmp_path):
    source, template, authority, _ = legacy_fixture(tmp_path)
    external = tmp_path / 'owner'
    external.mkdir()
    (external / 'keep.md').write_bytes(b'keep')
    (source / 'external').symlink_to(external, target_is_directory=True)
    plan = tool.prepare_legacy(tmp_path, authority)
    assert len(plan['held']) == 1
    tool.run_legacy(tmp_path, plan, authority, 'apply')
    assert source.exists() and (external / 'keep.md').read_bytes() == b'keep'
