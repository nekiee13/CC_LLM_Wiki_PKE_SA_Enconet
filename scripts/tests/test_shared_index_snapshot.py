from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import prepare_shared_index_snapshot as tool


def test_profiles_exclude_agents_evidence_history_and_generated_work():
    result = tool.profiles([
        'Enconet/docs/guide.md', 'Enconet/scripts/run.py',
        'Enconet/CLAUDE.md', 'Enconet/.claude/guide.md',
        'Enconet/.agents/guide.md', 'Enconet/work/reviews/CC_review.md',
        'Enconet/work/reviews/CX_review.md', 'Enconet/raw/source.md',
        'Enconet/work/validation/result.md', 'Enconet/work/migrations/original.py',
        'Enconet/docs/context/history.md', 'PKE_SA_NQA1_doc/INDEXING.md',
        'PKE_SA_NQA1_doc/support-transfer/rendered/scratch.md',
    ])
    assert result['PKE_SA_NQA1_Enconet_docs'] == [
        'docs/context/history.md', 'docs/guide.md', 'work/reviews/CX_review.md']
    assert result['PKE_SA_NQA1_Enconet_controlled'] == ['docs/guide.md', 'work/reviews/CX_review.md']
    assert result['Enconet-0a063bd7'] == ['scripts/run.py']
    assert result['PKE_SA_NQA1_global_docs'] == ['INDEXING.md']


def test_snapshot_uses_committed_bytes_and_never_materializes_claude_files(tmp_path):
    def git(*args):
        return subprocess.run(['git', '-C', str(tmp_path), *args], check=True, capture_output=True)
    git('init')
    git('config', 'user.name', 'Synthetic Test')
    git('config', 'user.email', 'test@example.invalid')
    files = {'.gitignore': '.tmp/\n', '.gitattributes': '* text eol=lf\n',
             'Enconet/docs/guide.md': '# committed\n', 'Enconet/scripts/run.py': 'def run(): pass\n',
             'Enconet/CLAUDE.md': '# owned\n', 'Enconet/.claude/settings.json': '{}\n',
             'Enconet/coordination/messages/CC_note.md': '# reviewer\n',
             'PKE_SA_NQA1_doc/INDEXING.md': '# indexing\n'}
    for name, content in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    git('add', '.')
    git('commit', '-m', 'synthetic inputs')
    live = tmp_path / 'Enconet/docs/guide.md'
    live.write_text('# owner edit\n', encoding='utf-8')
    output = tmp_path / 'PKE_SA_NQA1_doc/plans/cleanup-cu4/snapshot.json'
    output.parent.mkdir(parents=True)
    result = tool.prepare(tmp_path, output)
    snapshot = Path(result['snapshot'])
    assert live.read_text(encoding='utf-8') == '# owner edit\n'
    assert (snapshot / 'Enconet/docs/guide.md').read_text(encoding='utf-8') == '# committed\n'
    assert not (snapshot / 'Enconet/CLAUDE.md').exists()
    assert not (snapshot / 'Enconet/.claude').exists()
    assert not (snapshot / 'Enconet/coordination/messages/CC_note.md').exists()
    assert tool.git(snapshot, 'status', '--porcelain', '--untracked-files=no') == b''
    with pytest.raises(ValueError, match='Fresh snapshot'):
        tool.prepare(tmp_path, output.parent / 'retry.json')
