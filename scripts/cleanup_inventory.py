"""Read-only cleanup inventory and audit baseline. No move/delete/reset commands."""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import stat
import subprocess


OLD_PATHS = re.compile(r"(?<![\w])(?:doc|reset-plans|handoffs|manifests|derived|benchmarks|decisions|out|outputs/candidates/evidence_access)[/\\]")
TEXT = {'.py', '.ps1', '.md', '.json', '.yml', '.yaml', '.toml', '.ini', '.sql', '.csv', '.html', '.txt'}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', 'replace'))
    return result.stdout.decode('utf-8', 'replace')


def owner(parts):
    if '.claude' in parts or parts[-1] == 'CLAUDE.md' or parts[-1].startswith('CC_'):
        return 'claude-code'
    if '.agents' in parts or parts[-1] == 'AGENTS.md' or parts[-1].startswith('CX_'):
        return 'codex'
    return 'shared-or-owner'


def proposed(relative, suppliers):
    """Return conservative destination and disposition, never an executable move."""
    parts = PurePosixPath(relative).parts
    own = owner(parts)
    if parts[0] in {'audit_template', 'audit_archives'}:
        return relative, 'retain-versioned-history'
    if any(p in {'.agents', '.claude', '.git'} for p in parts) or parts[-1] in {'AGENTS.md', 'CLAUDE.md'}:
        return relative, 'retain-agent-or-git-home'
    if parts[0] == 'doc':
        destination = PurePosixPath('PKE_SA_NQA1_doc', *parts[1:]).as_posix()
    elif parts[0] == 'reset-plans':
        destination = PurePosixPath('PKE_SA_NQA1_doc', *parts).as_posix()
    elif relative == 'Transition_template_Plan.md':
        destination = 'PKE_SA_NQA1_doc/plans/Transition_template_Plan.md'
    elif parts[0].startswith('pytest'):
        return PurePosixPath('.tmp', 'retained', *parts).as_posix(), 'retain-scratch-review'
    elif parts[0].startswith('ekonerg-reset-'):
        return None, 'hold-classify-reset-scratch-owner'
    elif parts[0] in suppliers and len(parts) > 1:
        company, area = parts[:2]
        tail = parts[2:]
        if area in {'incoming', 'raw', 'db', 'sieving'}:
            return relative, 'retain-evidence-or-runtime'
        if area in {'benchmarks', 'derived', 'manifests', 'backup', 'decisions'}:
            destination = PurePosixPath(company, 'work', area, *tail).as_posix()
        elif area == 'handoffs':
            destination = PurePosixPath(company, 'coordination', 'handoffs', *tail).as_posix()
        elif area == 'docs' and tail and tail[0] == 'reviews':
            destination = PurePosixPath(company, 'work', *tail).as_posix()
        elif area == 'docs' and len(tail) == 1 and re.search(r'(?i)(?:^|_)PLAN(?:_|\.|$)', tail[0]):
            destination = PurePosixPath(company, 'docs', 'plans', *tail).as_posix()
        elif area in {'out', 'outputs'}:
            return None, 'hold-assign-result-run-or-validation-history'
        elif area.startswith(('pytest', '.pytest', '.test-tmp')):
            return PurePosixPath(company, '.tmp', 'retained', area, *tail).as_posix(), 'retain-scratch-review'
        else:
            return relative, 'retain-or-review-purpose'
    else:
        return relative, 'retain-or-review-purpose'
    return destination, 'claude-coordinated-move' if own == 'claude-code' else 'proposed-move-needs-review'


def database_baseline(path):
    if not path.exists():
        return {'status': 'not-configured'}
    before = digest(path)
    with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)) as conn:
        conn.execute('PRAGMA query_only=ON')
        conn.execute('BEGIN')
        integrity = conn.execute('PRAGMA integrity_check').fetchall()
        tables = {}
        for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            escaped = '"' + name.replace('"', '""') + '"'
            rows = conn.execute('SELECT * FROM ' + escaped).fetchall()
            encoded = sorted(json.dumps(row, ensure_ascii=False, default=lambda b: {'blob_hex': b.hex()}, separators=(',', ':')) for row in rows)
            h = hashlib.sha256()
            for row in encoded:
                h.update(row.encode('utf-8') + b'\n')
            tables[name] = {'rows': len(rows), 'row_content_sha256': h.hexdigest()}
        scores = []
        if 'criterion_evaluations' in tables:
            scores = [dict(zip(('run_id', 'criteria', 'score_sum'), r)) for r in conn.execute(
                'SELECT evaluation_run_id,COUNT(*),SUM(score) FROM criterion_evaluations GROUP BY evaluation_run_id ORDER BY evaluation_run_id')]
        active = []
        if conn.execute("SELECT 1 FROM sqlite_master WHERE name='active_crumbs'").fetchone():
            active = conn.execute('SELECT document_side,COUNT(*) FROM active_crumbs GROUP BY document_side ORDER BY document_side').fetchall()
        foreign = conn.execute('PRAGMA foreign_key_check').fetchall()
    after = digest(path)
    return {'status': 'captured' if before == after else 'changed-during-read',
            'sha256_before': before, 'sha256_after': after, 'tables': tables,
            'integrity': integrity, 'foreign_key_errors': foreign,
            'evaluation_scores': scores, 'active_crumbs': active}


def capture(root, suppliers):
    root = Path(root).resolve()
    tracked = set(filter(None, git(root, 'ls-files', '-z').split('\0')))
    dirty = set(filter(None, git(root, 'diff', '--name-only', '-z', 'HEAD').split('\0')))
    entries, failures = [], []

    def walk(folder):
        try:
            children = sorted(os.scandir(folder), key=lambda e: e.name)
        except OSError as error:
            failures.append({'path': Path(folder).relative_to(root).as_posix(), 'error': str(error)})
            return
        for entry in children:
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            if rel.startswith('PKE_SA_NQA1_doc/plans/cleanup-cu1/'):
                continue  # receipts are not their own inputs
            row = {'path': rel, 'owner': owner(PurePosixPath(rel).parts),
                   'git': 'tracked' if rel in tracked else 'untracked-or-ignored', 'dirty': rel in dirty}
            try:
                info = entry.stat(follow_symlinks=False)
                redirected = stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)
                row.update(bytes=info.st_size, mtime_ns=info.st_mtime_ns, mode=info.st_mode,
                           attributes=getattr(info, 'st_file_attributes', 0), hardlinks=info.st_nlink)
                row['type'] = 'redirect' if redirected else ('directory' if entry.is_dir(follow_symlinks=False) else 'file')
                row['new_path'], row['disposition'] = proposed(rel, suppliers)
                row['retention'] = 'keep; no deletion authorized'
                if row['dirty']:
                    row['disposition'] = 'hold-existing-dirty-content'
                if redirected or info.st_nlink > 1 and row['type'] == 'file':
                    row['disposition'] = 'hold-redirect-or-hardlink'
                if row['type'] == 'file' and not redirected:
                    row['sha256'] = digest(path)
                    if path.suffix.lower() in TEXT and not any(p in {'incoming', 'raw', 'DATA', '.git'} for p in path.relative_to(root).parts):
                        with path.open(encoding='utf-8', errors='replace') as stream:
                            row['old_path_references'] = [{'line': n, 'tokens': sorted(set(OLD_PATHS.findall(line)))}
                                                          for n, line in enumerate(stream, 1) if OLD_PATHS.search(line)]
                    if digest(path) != row['sha256'] or path.stat().st_mtime_ns != info.st_mtime_ns:
                        row['disposition'] = 'hold-changed-during-read'
                if row['new_path'] and row['new_path'] != rel:
                    target = root / row['new_path']
                    row['destination_exists'] = target.exists()
                    if target.exists() and row['type'] == 'file':
                        row['disposition'] = 'hold-destination-collision'
                entries.append(row)
                if row['type'] == 'directory' and path.name != '.git':
                    walk(path)
            except OSError as error:
                row['disposition'] = 'hold-access-error'
                entries.append(row)
                failures.append({'path': rel, 'error': str(error)})

    walk(root)
    candidates = [e['path'] for e in entries if e['git'] != 'tracked']
    ignored = subprocess.run(['git', '-C', str(root), 'check-ignore', '-z', '--stdin'],
                             input=('\0'.join(candidates) + '\0').encode('utf-8'), capture_output=True)
    if ignored.returncode not in {0, 1}:
        raise RuntimeError(ignored.stderr.decode('utf-8', 'replace'))
    ignored_paths = set(ignored.stdout.decode('utf-8').split('\0'))
    dependencies = {}
    for entry in entries:
        if entry['git'] != 'tracked':
            entry['git'] = 'ignored' if entry['path'] in ignored_paths else 'untracked'
        for ref in entry.get('old_path_references', []):
            for token in ref['tokens']:
                dependencies.setdefault(token, []).append({'path': entry['path'], 'line': ref['line'],
                                                          'owner': entry['owner']})
        entry['path_users'] = 'See dependency_groups; lexical candidates require semantic review'
    baselines = {}
    for supplier in suppliers:
        project = root / supplier
        if not project.is_dir():
            baselines[supplier] = {'status': 'missing-project'}
            continue
        baselines[supplier] = database_baseline(project / 'db/nqa_audit.sqlite')
        baselines[supplier]['protected_files'] = [
            {k: e[k] for k in ('path', 'sha256', 'bytes', 'mtime_ns')}
            for e in entries if e.get('sha256') and e['path'].startswith(supplier + '/')
            and PurePosixPath(e['path']).parts[1] in {'incoming', 'raw', 'derived', 'db', 'manifests', 'benchmarks', 'decisions', 'sieving', 'outputs', 'out'}]
    unstable = []
    for supplier, baseline in baselines.items():
        for item in baseline.get('protected_files', []):
            try:
                if digest(root / item['path']) != item['sha256']:
                    unstable.append(item['path'])
            except OSError:
                unstable.append(item['path'])
    return {'schema': 'cleanup-inventory-1', 'mode': 'read-only-proposal',
            'git_head': git(root, 'rev-parse', 'HEAD').strip(), 'suppliers': suppliers,
            'entries': entries, 'access_failures': failures, 'baselines': baselines,
            'dependency_groups': dependencies, 'changed_protected_inputs': unstable,
            'summary': {'entries': len(entries), 'access_failures': len(failures),
                        'changed_protected_inputs': len(unstable),
                        'git_categories': dict(sorted(Counter(e['git'] for e in entries).items())),
                        'dispositions': dict(sorted(Counter(e['disposition'] for e in entries).items()))}}


def write_receipts(root, output, record):
    root = Path(root).resolve()
    output = Path(output).absolute()
    output.relative_to(root)
    for parent in [output, *output.parents]:
        if parent.exists() and (parent.is_symlink() or parent.resolve() != parent.absolute()):
            raise ValueError('redirected receipt destination')
        if parent == root:
            break
    if output.exists():
        raise FileExistsError('receipt directory already exists; do not overwrite')
    if any(p in {'incoming', 'raw', 'db', '.claude', '.agents'} for p in output.relative_to(root).parts):
        raise ValueError('protected receipt destination')
    output.mkdir(parents=True)
    for name, data in [('inventory.json', {k: v for k, v in record.items() if k != 'baselines'}),
                       ('audit-baselines.json', record['baselines'])]:
        with (output / name).open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--suppliers', nargs='+', required=True)
    parser.add_argument('--output', type=Path, help='Create fresh receipt folder only; never move input files')
    args = parser.parse_args()
    if any(len(PurePosixPath(s).parts) != 1 or s in {'.', '..'} or '\\' in s for s in args.suppliers):
        parser.error('supplier names must be direct child folder names')
    record = capture(args.workspace, args.suppliers)
    if args.output:
        write_receipts(args.workspace, args.output, record)
    print(json.dumps(record['summary'], ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
