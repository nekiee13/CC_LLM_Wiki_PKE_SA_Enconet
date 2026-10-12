"""Rehearse the reviewed reference patch in a disposable copy only."""
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).parents[2]


def test_activation_patch_matches_current_files_and_retains_guidance_check(tmp_path):
    pairs = {'workspace-layout.json': 'workspace-layout.json', 'README.md': 'README.md',
             'AGENTS.md': 'AGENTS.md', '.gitignore': '.gitignore',
             'PKE_SA_NQA1_doc/GUIDANCE_PAIRS.json': 'doc/GUIDANCE_PAIRS.json',
             'PKE_SA_NQA1_doc/README.md': 'doc/README.md',
             'PKE_SA_NQA1_doc/INDEXING.md': 'doc/INDEXING.md'}
    for destination, source in pairs.items():
        path = tmp_path / destination
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / source).read_bytes())
    executable = Path.home() / 'AppData/Local/Programs/OpenAI/Codex/bin/codex.exe'
    patch = (ROOT / 'PKE_SA_NQA1_doc/plans/cleanup-cu3/workspace-activation.patch').read_text(encoding='utf-8')
    applied = subprocess.run([str(executable), '--codex-run-as-apply-patch', patch],
                             cwd=tmp_path, capture_output=True, text=True, encoding='utf-8')
    assert applied.returncode == 0, applied.stdout + applied.stderr
    assert json.loads((tmp_path / 'workspace-layout.json').read_text())['documentation_root'] == 'PKE_SA_NQA1_doc'
    manifest = json.loads((tmp_path / 'PKE_SA_NQA1_doc/GUIDANCE_PAIRS.json').read_text())
    pair = next(item for item in manifest['pairs'] if item['id'] == 'workspace-guidance')
    rule = next(item for item in pair['rules'] if item['id'] == 'workspace-doc-dir')
    for side, path in [('codex', tmp_path / 'AGENTS.md'), ('claude', ROOT / 'CLAUDE.md')]:
        text = re.sub(r'\s+', ' ', path.read_text(encoding='utf-8'))
        assert re.search(rule[side + '_pattern'], text, re.IGNORECASE | re.DOTALL)
    assert 'PKE_SA_NQA1_doc/README.md' in (tmp_path / 'README.md').read_text()
    assert 'plans/SUPPORT_SYSTEM_TRANSFER_MASTER_PLAN.md' in (tmp_path / 'PKE_SA_NQA1_doc/README.md').read_text()
    assert not (tmp_path / 'CLAUDE.md').exists()
