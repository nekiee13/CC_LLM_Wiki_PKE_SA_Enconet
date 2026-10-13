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
