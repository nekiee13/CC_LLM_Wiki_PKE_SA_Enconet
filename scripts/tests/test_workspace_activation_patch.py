"""Rehearse the reviewed reference patch in a disposable copy only."""
import json
import base64
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).parents[2]


def test_activation_patch_matches_current_files_and_retains_guidance_check(tmp_path):
    snapshot = ROOT / 'PKE_SA_NQA1_doc/plans/cleanup-cu3/live-workspace-20261012/patch-before.json.zip'
    before = None
    if snapshot.exists():
        with zipfile.ZipFile(snapshot) as archive:
            before = json.loads(archive.read('patch-before.json'))
    pairs = {'workspace-layout.json': 'workspace-layout.json', 'README.md': 'README.md',
             'AGENTS.md': 'AGENTS.md', '.gitignore': '.gitignore',
             'PKE_SA_NQA1_doc/GUIDANCE_PAIRS.json': 'doc/GUIDANCE_PAIRS.json',
             'PKE_SA_NQA1_doc/README.md': 'doc/README.md',
             'PKE_SA_NQA1_doc/INDEXING.md': 'doc/INDEXING.md'}
    for destination, source in pairs.items():
        path = tmp_path / destination
        path.parent.mkdir(parents=True, exist_ok=True)
        data = base64.b64decode(before[destination]['bytes_base64']) if before else (ROOT / source).read_bytes()
        if before:
            assert hashlib.sha256(data).hexdigest() == before[destination]['sha256']
        path.write_bytes(data)
    executable = Path.home() / 'AppData/Local/Programs/OpenAI/Codex/bin/codex.exe'
    patch = (ROOT / 'PKE_SA_NQA1_doc/plans/cleanup-cu3/workspace-activation.patch').read_text(encoding='utf-8')
    applied = subprocess.run([str(executable), '--codex-run-as-apply-patch', patch],
                             cwd=tmp_path, capture_output=True, text=True, encoding='utf-8')
    assert applied.returncode == 0, applied.stdout + applied.stderr
    assert json.loads((tmp_path / 'workspace-layout.json').read_text())['documentation_root'] == 'PKE_SA_NQA1_doc'
    manifest = json.loads((tmp_path / 'PKE_SA_NQA1_doc/GUIDANCE_PAIRS.json').read_text())
    pair = next(item for item in manifest['pairs'] if item['id'] == 'workspace-guidance')
    rule = next(item for item in pair['rules'] if item['id'] == 'workspace-doc-dir')
    # This is a historical patch rehearsal, not the live paired-guidance check.
    # Claude has since synchronized its own path. Read its original Git blob
    # at the exact recorded preparation HEAD without writing a Claude file.
    if before:
        workflow_zip = snapshot.parent / 'workflow-plan.json.zip'
        with zipfile.ZipFile(workflow_zip) as archive:
            assert len(archive.namelist()) == 1
            source_head = json.loads(archive.read(archive.namelist()[0]))['workflow']['head']
        historical = subprocess.run(['git', '-C', str(ROOT), 'show', source_head + ':CLAUDE.md'],
                                    capture_output=True, check=True)
        claude_text = historical.stdout.decode('utf-8')
    else:
        claude_text = (ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
    for side, content in [('codex', (tmp_path / 'AGENTS.md').read_text(encoding='utf-8')),
                          ('claude', claude_text)]:
        text = re.sub(r'\s+', ' ', content)
        assert re.search(rule[side + '_pattern'], text, re.IGNORECASE | re.DOTALL)
    assert 'PKE_SA_NQA1_doc/README.md' in (tmp_path / 'README.md').read_text()
    assert 'plans/SUPPORT_SYSTEM_TRANSFER_MASTER_PLAN.md' in (tmp_path / 'PKE_SA_NQA1_doc/README.md').read_text()
    assert not (tmp_path / 'CLAUDE.md').exists()
