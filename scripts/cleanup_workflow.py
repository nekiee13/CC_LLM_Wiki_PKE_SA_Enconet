"""Git-aware wrapper for authorized, reversible cleanup file moves.

Prepare is read-only. Apply/undo require the exact prepared plan and the existing
cleanup authorization. Stage only formerly tracked files, never unrelated edits.
Prune only explicitly listed, empty source directories; never recurse or commit.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess

import cleanup_migration as migration


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if result.returncode:
        raise ValueError('Git check/operation failed: ' + result.stderr.decode('utf-8', errors='replace'))
    return result.stdout


def repository(root):
    if Path(git(root, 'rev-parse', '--show-toplevel').decode('utf-8').strip()).resolve() != root:
        raise ValueError('cleanup root must be the Git workspace root')
    return git(root, 'rev-parse', 'HEAD').decode('ascii').strip()


def index(root):
    result = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        metadata, path = entry.split(b'\t', 1)
        mode, blob, stage = metadata.decode('ascii').split()
        if stage != '0':
            raise ValueError('unmerged index refused')
        result[path.decode('utf-8')] = [mode, blob]
    return result


def directories(root, plan, selected):
    allowed = {parent.relative_to(root).as_posix() for row in plan['files']
               for parent in (root / row['source']).parents
               if parent != root and parent.is_relative_to(root)}
    result = {}
    for name in selected:
        if name not in allowed or name in result:
            raise ValueError('prune list must contain unique source-parent directories')
        path = migration.safe(root, name)
        if not path.is_dir():
            raise ValueError('prune source directory missing')
        result[name] = path.stat().st_mode
    return result


def prepare(root, plan, prune=()):
    root = migration.root_path(root)
    head = repository(root)
    if git(root, 'diff', '--cached', '--name-only', '-z'):
        raise ValueError('existing staged work refused')
    if migration.preview(root, plan)['blocked']:
        raise ValueError('file preview blocked')
    entries = index(root)
    tracked = []
    for row in plan['files']:
        if row['destination'] in entries:
            raise ValueError('destination already tracked')
        if row['source'] in entries:
            if git(root, 'diff', '--name-only', '-z', '--', ':(literal)' + row['source']):
                raise ValueError('dirty tracked source refused')
            tracked.append(row['source'])
    result = dict(plan)
    result['workflow'] = {'schema': 'cleanup-workflow-1', 'root': str(root), 'head': head,
                          'index': entries, 'tracked_sources': tracked,
                          'prune_directories': directories(root, plan, prune)}
    return result


def check(root, plan):
    root = migration.root_path(root)
    record = plan['workflow']
    if (record.get('schema') != 'cleanup-workflow-1' or record.get('root') != str(root)
            or repository(root) != record.get('head')):
        raise ValueError('workflow root/HEAD differs from prepared plan')
    baseline = record['index']
    allowed = {parent.relative_to(root).as_posix() for row in plan['files']
               for parent in (root / row['source']).parents
               if parent != root and parent.is_relative_to(root)}
    for name, mode in record['prune_directories'].items():
        if name not in allowed or type(mode) is not int:
            raise ValueError('prune scope differs from source-parent list')
        path = migration.safe(root, name)
        if path.exists() and not path.is_dir():
            raise ValueError('prune target is not a directory')
    tracked = set(record['tracked_sources'])
    if tracked != {row['source'] for row in plan['files'] if row['source'] in baseline}:
        raise ValueError('tracked-source witness differs from map')
    expected = dict(baseline)
    current = index(root)
    for row in plan['files']:
        source, dest = row['source'], row['destination']
        if source not in tracked:
            continue
        if dest in baseline:
            raise ValueError('tracked destination collision')
        old, new = current.get(source), current.get(dest)
        if old == baseline[source] and new is None:
            continue
        if old is None and new == baseline[source]:
            expected[dest] = expected.pop(source)
            continue
        raise ValueError('planned index entry changed')
    if current != expected:
        raise ValueError('unrelated index edit refused')
    return root, record


def stage(root, plan, restored=False):
    root, record = check(root, plan)
    current = index(root)
    pairs = [row for row in plan['files'] if row['source'] in record['tracked_sources']
             and (row['destination'] if restored else row['source']) in current]
    # Bound native Windows arguments while avoiding one Git process per file.
    batch, size = [], 0
    for row in pairs:
        arguments = [':(literal)' + row['source'], ':(literal)' + row['destination']]
        length = sum(len(value) + 3 for value in arguments)
        if length > 8000:
            raise ValueError('one path pair exceeds bounded Git arguments')
        if batch and size + length > 8000:
            git(root, 'add', '-A', '-f', '--', *batch)
            batch, size = [], 0
        batch.extend(arguments)
        size += length
    if batch:
        git(root, 'add', '-A', '-f', '--', *batch)
    root, record = check(root, plan)
    expected = dict(record['index'])
    if not restored:
        for row in plan['files']:
            if row['source'] in record['tracked_sources']:
                expected[row['destination']] = expected.pop(row['source'])
    if index(root) != expected:
        raise ValueError('Git stage did not reach expected state')


def apply(root, plan, journal, authorization):
    root, record = check(root, plan)
    result = migration.apply(root, plan, journal, authorization)
    retained, removed = [], []
    # The exact prune list is covered by the authorization's full plan hash.
    for name in sorted(record['prune_directories'], key=lambda item: (item.count('/'), item), reverse=True):
        path = migration.safe(root, name)
        if path.exists():
            try:
                path.rmdir()
                removed.append(name)
            except OSError:
                retained.append(name)
    stage(root, plan)
    migration.append(Path(journal), {'kind': 'apply-complete', 'workflow': True, 'removed_empty_directories': removed,
                                    'retained_directories': retained})
    return {**result, 'tracked_moves': len(record['tracked_sources']), 'retained_directories': retained}


def undo(root, plan, journal):
    root, record = check(root, plan)
    # Preflight every file before restoring directories or touching Git.
    first, events = migration.header(root, plan, migration.journal_path(root, journal, plan))
    for row in plan['files']:
        migration.state(root, row, first['identities'][row['source']])
    for name, mode in sorted(record['prune_directories'].items(), key=lambda item: item[0].count('/')):
        path = migration.safe(root, name)
        if not path.exists():
            path.mkdir(parents=True)
            path.chmod(mode)
    result = migration.undo(root, plan, journal)
    stage(root, plan, restored=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--mode', choices=['prepare', 'apply', 'undo'], default='prepare')
    parser.add_argument('--prune', nargs='*', default=[])
    parser.add_argument('--journal', type=Path)
    parser.add_argument('--authorization', type=Path)
    args = parser.parse_args()
    plan = migration.load(args.plan)
    if args.mode == 'prepare':
        result = prepare(args.root, plan, args.prune)
    elif args.mode == 'apply':
        if not args.journal or not args.authorization:
            parser.error('apply requires journal and authorization')
        result = apply(args.root, plan, args.journal, migration.load(args.authorization))
    else:
        if not args.journal:
            parser.error('undo requires journal')
        result = undo(args.root, plan, args.journal)
    print(json.dumps(result, ensure_ascii=True))


if __name__ == '__main__':
    main()
