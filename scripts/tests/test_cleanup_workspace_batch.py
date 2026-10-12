import hashlib
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from prepare_cleanup_workspace_batch import build


def test_workspace_preview_holds_dirty_changed_foreign_and_new_files(tmp_path):
    def git(*args):
        subprocess.run(['git', '-C', str(tmp_path), *args], check=True, capture_output=True)
    git('init', '-q')
    git('config', 'user.name', 'Synthetic')
    git('config', 'user.email', 'fixture@example.invalid')
    (tmp_path / 'doc').mkdir()
    rows = []
    for name in ('clean.md', 'dirty.md', 'changed.md', 'CC_review.md'):
        path = tmp_path / 'doc' / name
        path.write_bytes(b'original')
        rows.append({'source': 'doc/' + name, 'destination': 'PKE_SA_NQA1_doc/' + name,
                     'sha256': hashlib.sha256(b'original').hexdigest(), 'hold': None,
                     'owner': 'claude-code' if name.startswith('CC_') else 'shared-or-owner'})
    git('add', 'doc/clean.md', 'doc/dirty.md')
    git('commit', '-qm', 'Synthetic baseline')
    (tmp_path / 'doc/dirty.md').write_bytes(b'owner edit')
    (tmp_path / 'doc/changed.md').write_bytes(b'changed since inventory')
    (tmp_path / 'doc/new.md').write_bytes(b'new owner file')
    before = {path.name: path.read_bytes() for path in (tmp_path / 'doc').iterdir()}
    plan, receipt = build(tmp_path, {'files': rows})
    assert [row['source'] for row in plan['files']] == ['doc/clean.md']
    assert receipt['preview']['eligible'] == 1 and receipt['preview']['blocked'] == 0
    assert {row['source'] for row in receipt['held']} == {
        'doc/dirty.md', 'doc/changed.md', 'doc/CC_review.md', 'doc/new.md'}
    assert before == {path.name: path.read_bytes() for path in (tmp_path / 'doc').iterdir()}
    assert not (tmp_path / 'PKE_SA_NQA1_doc').exists()
