"""Prepare explicit neutral corpora in a clean, retained committed worktree.

Never stash owner edits, copy agent infrastructure, or walk untracked evidence.
The snapshot stays under .tmp so byte-offset indexes keep their source files.
"""
import argparse
import fnmatch
import hashlib
import json
from pathlib import Path
import subprocess

EXCLUDED = [
    'raw/**', 'incoming/**', 'derived/**', 'db/**', 'sieving/DATA/**',
    'coordination/archive/**', 'coordination/claims/**', 'coordination/BOARD.md',
    'work/derived/**', 'work/manifests/**', 'work/backup/**',
    'work/bootstrap/**', 'work/migrations/**', 'work/validation/**',
    'outputs/**', 'sieving/runs/**', 'tests/fixtures/**',
    '.tmp/**', '.test-tmp/**', '.pytest*/**',
]
CODE_EXCLUDED = EXCLUDED + ['coordination/**', 'wiki/**', 'docs/**']
CONTROLLED_EXCLUDED = ['docs/context/**', 'docs/_archive/**']
GLOBAL_EXCLUDED = ['support-transfer/rendered/**', 'plans/**/rendered/**']
DOC_SUFFIXES = {'.md', '.txt', '.rst'}
CODE_SUFFIXES = {'.py', '.json', '.yaml', '.yml', '.toml', '.ps1', '.sh', '.js', '.css', '.html'}


def neutral(name):
    parts = Path(name).parts
    return not any(p.casefold() in {'.agents', '.claude', '.codex'}
                   or p.casefold() in {'agents.md', 'claude.md', 'settings.local.json'}
                   or p.casefold().startswith('cc_') for p in parts)


def selected(name, patterns):
    return neutral(name) and not any(fnmatch.fnmatchcase(name, p) for p in patterns)


def profiles(tracked):
    docs, code, global_docs = [], [], []
    for name in tracked:
        if name.startswith('Enconet/'):
            relative = name[len('Enconet/'):]
            if selected(relative, EXCLUDED) and Path(relative).suffix.lower() in DOC_SUFFIXES:
                docs.append(relative)
            if selected(relative, CODE_EXCLUDED) and Path(relative).suffix.lower() in CODE_SUFFIXES:
                code.append(relative)
        elif name.startswith('PKE_SA_NQA1_doc/'):
            relative = name[len('PKE_SA_NQA1_doc/'):]
            if selected(relative, GLOBAL_EXCLUDED) and Path(relative).suffix.lower() in DOC_SUFFIXES:
                global_docs.append(relative)
    return {
        'PKE_SA_NQA1_Enconet_docs': sorted(docs),
        'PKE_SA_NQA1_Enconet_controlled': sorted(p for p in docs if selected(p, CONTROLLED_EXCLUDED)),
        'PKE_SA_NQA1_global_docs': sorted(global_docs),
        'Enconet-0a063bd7': sorted(code),
    }


def git(root, *args, input=None):
    result = subprocess.run(['git', '-C', str(root), *args], input=input,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return result.stdout


def prepare(root, output):
    root = root.resolve(strict=True)
    if Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != root:
        raise ValueError('Explicit workspace Git root required')
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    tracked = git(root, 'ls-tree', '-rz', '--name-only', head).decode('utf-8').split('\0')
    corpora = profiles(p for p in tracked if p)
    if not all(corpora.values()):
        raise ValueError('Empty corpus refused')
    snapshot = root / '.tmp' / ('index-source-' + head[:12])
    if snapshot.exists():
        raise ValueError('Fresh snapshot required; existing source is never overwritten')
    output = output.absolute()
    if not output.is_relative_to(root / 'PKE_SA_NQA1_doc/plans/cleanup-cu4') or output.exists():
        raise ValueError('Fresh CU-4 receipt required')
    paths = {'.gitignore', '.gitattributes'}
    for name, entries in corpora.items():
        prefix = 'PKE_SA_NQA1_doc/' if name == 'PKE_SA_NQA1_global_docs' else 'Enconet/'
        paths.update(prefix + p for p in entries)
    # Explicit file-only sparse patterns. Never materialize excluded agent trees.
    patterns = []
    for path in sorted(paths):
        if not neutral(path) or '\n' in path or '\r' in path:
            raise ValueError('Unsafe or owned snapshot path')
        patterns.append('/' + ''.join('\\' + c if c in '*?[]!#\\' else c for c in path))
    git(root, 'worktree', 'add', '--detach', '--no-checkout', str(snapshot), head)
    git(snapshot, 'sparse-checkout', 'init', '--no-cone')
    git(snapshot, '-c', 'core.autocrlf=false', '-c', 'core.eol=lf',
        'sparse-checkout', 'set', '--no-cone', '--stdin', input=('\n'.join(patterns) + '\n').encode('utf-8'))
    # --no-checkout starts with an empty index. Populate it only after the
    # explicit sparse rules exist, so excluded agent files are never created.
    git(snapshot, '-c', 'core.autocrlf=false', '-c', 'core.eol=lf', 'read-tree', '-m', '-u', head)
    if git(snapshot, 'status', '--porcelain', '--untracked-files=no').strip():
        raise ValueError('Snapshot is not clean')
    hashes = {p: hashlib.sha256((snapshot / p).read_bytes()).hexdigest() for p in sorted(paths)}
    result = dict(schema='shared-index-snapshot-1', head=head, snapshot=str(snapshot),
                  profiles=corpora, files_sha256=hashes, excludes=EXCLUDED,
                  code_excludes=CODE_EXCLUDED, controlled_excludes=CONTROLLED_EXCLUDED,
                  global_excludes=GLOBAL_EXCLUDED)
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = prepare(args.root, args.output)
    print(json.dumps(dict(head=result['head'], snapshot=result['snapshot'],
                          counts={k: len(v) for k, v in result['profiles'].items()})))


if __name__ == '__main__':
    main()
