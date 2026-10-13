import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import cleanup_residual_empty as tool


def fixture(tmp_path, monkeypatch):
    for name in tool.MOVES:
        (tmp_path / name).mkdir(parents=True)
    authority = tmp_path / 'authority.md'
    authority.write_text('synthetic owner cleanup authorization', encoding='utf-8')
    base = ['tool', '--root', str(tmp_path), '--plan', str(tmp_path / 'plan.json'),
            '--journal', str(tmp_path / 'journal.jsonl'), '--authority', str(authority)]
    def run(mode):
        monkeypatch.setattr(sys, 'argv', base + ['--mode', mode])
        return tool.main()
    run('preview')
    return run


def test_apply_retry_verify_and_undo_preserve_identity_and_acl(tmp_path, monkeypatch):
    run = fixture(tmp_path, monkeypatch)
    before = {name: tool.homes.tree(tmp_path, name) for name in tool.MOVES}
    assert run('apply') == run('apply') == run('verify') == 0
    for name, destination in tool.MOVES.items():
        assert not (tmp_path / name).exists()
        assert tool.homes.tree(tmp_path, destination) == before[name]
    assert run('undo') == run('undo') == 0
    for name in tool.MOVES:
        assert tool.homes.tree(tmp_path, name) == before[name]


def test_new_file_blocks_entire_batch(tmp_path, monkeypatch):
    run = fixture(tmp_path, monkeypatch)
    (tmp_path / 'reset-plans/owner.txt').write_bytes(b'keep')
    with pytest.raises(ValueError, match='files remain'):
        run('apply')
    assert all((tmp_path / name).exists() for name in tool.MOVES)
    assert not (tmp_path / 'journal.jsonl').exists()


def test_foreign_destination_refused(tmp_path, monkeypatch):
    run = fixture(tmp_path, monkeypatch)
    path = tmp_path / 'plan.json'
    plan = json.loads(path.read_text(encoding='utf-8'))
    plan['rows'][0]['destination'] = 'Other/foreign'
    path.write_text(json.dumps(plan), encoding='utf-8')
    with pytest.raises(ValueError, match='Plan or authority differs'):
        run('apply')
    assert all((tmp_path / name).exists() for name in tool.MOVES)


def test_root_cache_bundle_is_separate_and_reversible(tmp_path, monkeypatch):
    for name in tool.ROOT_CACHES:
        (tmp_path / name).mkdir()
    authority = tmp_path / 'authority.md'
    authority.write_bytes(b'synthetic authority')
    base = ['tool', '--root', str(tmp_path), '--plan', str(tmp_path / 'cache-plan.json'),
            '--authority', str(authority), '--journal', str(tmp_path / 'cache-journal.jsonl'),
            '--bundle', 'root-caches']
    for mode in ('preview', 'apply', 'apply', 'verify', 'undo'):
        monkeypatch.setattr(sys, 'argv', base + ['--mode', mode])
        assert tool.main() == 0
    assert all((tmp_path / name).is_dir() for name in tool.ROOT_CACHES)
    assert not any((tmp_path / name).exists() for name in tool.MOVES)
