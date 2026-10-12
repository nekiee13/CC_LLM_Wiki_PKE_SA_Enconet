"""Windows-only, reversible native renames of emptied legacy directory trees.

Keep directory identities, owners and ACLs instead of pruning/recreating them.
No recursive deletion, source/DB changes, Git staging or approval factory.
Preparation may pin pending file moves; apply refuses any remaining file.
"""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re

import cleanup_migration as migration

HOMES = ('benchmarks', 'derived', 'manifests', 'decisions', 'backup', 'handoffs',
         'out', '.bootstrap', 'docs/reviews', '.pytest_cache', 'outputs/candidates')


def acl_hash(path):
    if os.name != 'nt':
        raise ValueError('native directory recovery is Windows-only')
    from ctypes import wintypes
    api = ctypes.WinDLL('advapi32', use_last_error=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    api.GetNamedSecurityInfoW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD,
                                        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                                        ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]
    api.GetNamedSecurityInfoW.restype = wintypes.DWORD
    api.ConvertSecurityDescriptorToStringSecurityDescriptorW.argtypes = [
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p]
    api.ConvertSecurityDescriptorToStringSecurityDescriptorW.restype = wintypes.BOOL
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    descriptor, text = ctypes.c_void_p(), ctypes.c_void_p()
    result = api.GetNamedSecurityInfoW(str(path), 1, 7, None, None, None, None, ctypes.byref(descriptor))
    if result:
        raise ctypes.WinError(result)
    try:
        if not api.ConvertSecurityDescriptorToStringSecurityDescriptorW(descriptor, 1, 7, ctypes.byref(text), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return hashlib.sha256(ctypes.wstring_at(text).encode('utf-8')).hexdigest()
    finally:
        if text.value:
            kernel.LocalFree(text)
        kernel.LocalFree(descriptor)


def scan(root, name):
    folder = migration.safe(root, name)
    if not folder.is_dir():
        raise ValueError('legacy tree missing or not a directory')
    nodes, files = {}, []
    def denied(error):
        raise error
    for current, directories, filenames in os.walk(folder, followlinks=False, onerror=denied):
        current = Path(current)
        migration.safe(root, current.relative_to(root).as_posix())
        witness = migration.identity(current)
        # Removing approved files changes parent mtime, not directory identity.
        witness.pop('mtime_ns')
        witness['sddl_sha256'] = acl_hash(current)
        nodes[current.relative_to(folder).as_posix()] = witness
        for child in directories:
            migration.safe(root, (current / child).relative_to(root).as_posix())
        for child in filenames:
            path = current / child
            migration.safe(root, path.relative_to(root).as_posix())
            files.append(path.relative_to(root).as_posix())
    return nodes, files


def tree(root, name):
    nodes, files = scan(root, name)
    if files:
        raise ValueError('files remain in legacy tree')
    return nodes


def destination(supplier, run, home):
    return supplier + ('/work/backup' if home == 'backup'
                       else '/work/migrations/' + run + '/empty-original-homes/' + home)


def shape(root, plan):
    root = migration.root_path(root)
    supplier, run = plan.get('supplier'), plan.get('run')
    if (plan.get('schema') != 'cleanup-empty-homes-1' or not isinstance(supplier, str)
            or supplier in {'', '.', '..'} or Path(supplier).name != supplier
            or not isinstance(run, str) or not re.fullmatch('[A-Za-z0-9_-]+', run)
            or not isinstance(plan.get('directories'), list) or not plan['directories']):
        raise ValueError('bound local empty-home plan required')
    migration.safe(root, supplier)
    seen = set()
    for row in plan['directories']:
        if row['home'] not in HOMES or row['source'] != supplier + '/' + row['home']:
            raise ValueError('unknown legacy home')
        if row['destination'] != destination(supplier, run, row['home']):
            raise ValueError('foreign or unexpected directory destination')
        for name in (row['source'], row['destination']):
            migration.safe(root, name)
            if name.casefold() in seen:
                raise ValueError('directory collision')
            seen.add(name.casefold())
    return root


def prepare(root, supplier, run, file_map=None):
    root = migration.root_path(root)
    file_map = file_map or {'schema': 'cleanup-file-map-1', 'files': []}
    if file_map.get('schema') != 'cleanup-file-map-1':
        raise ValueError('pending file map schema differs')
    pending = {}
    for row in file_map['files']:
        if not row['source'].startswith(supplier + '/') or not row['destination'].startswith(supplier + '/'):
            raise ValueError('foreign pending file move')
        if row['source'] in pending:
            raise ValueError('duplicate pending file')
        pending[row['source']] = row['sha256']
    rows = []
    # Check supplier/run shape before visiting a filesystem path.
    shape(root, {'schema': 'cleanup-empty-homes-1', 'supplier': supplier, 'run': run,
                 'directories': [{'home': 'backup', 'source': supplier + '/backup',
                                  'destination': destination(supplier, run, 'backup')}]})
    for home in HOMES:
        source = supplier + '/' + home
        if not migration.safe(root, source).exists():
            continue
        nodes, files = scan(root, source)
        for name in files:
            if name not in pending or migration.digest(root / name) != pending[name]:
                raise ValueError('unmapped or changed file in legacy home: ' + name)
        target = destination(supplier, run, home)
        if migration.safe(root, target).exists():
            raise ValueError('directory destination collision')
        rows.append({'home': home, 'source': source, 'destination': target,
                     'tree': nodes, 'pending_files': files})
    plan = {'schema': 'cleanup-empty-homes-1', 'supplier': supplier, 'run': run,
            'file_plan_sha256': migration.plan_hash(file_map), 'directories': rows}
    shape(root, plan)
    return plan


def state(root, row):
    source, target = [migration.safe(root, row[key]) for key in ('source', 'destination')]
    if source.exists() == target.exists():
        raise ValueError('directory collision or both homes missing')
    name = row['source'] if source.exists() else row['destination']
    if tree(root, name) != row['tree']:
        raise ValueError('directory identity, shape, owner or ACL changed')
    return 'original' if source.exists() else 'moved'


def preview(root, plan):
    root = shape(root, plan)
    blocked = []
    for row in plan['directories']:
        try:
            if state(root, row) != 'original':
                raise ValueError('preview requires original tree')
        except (ValueError, OSError) as error:
            blocked.append({'source': row['source'], 'reason': str(error)})
    return {'mode': 'read-only-preview', 'ready': not blocked, 'blocked': blocked,
            'directories': len(plan['directories']), 'plan_sha256': migration.plan_hash(plan)}


def native_move(source, target):
    if os.name != 'nt':
        raise ValueError('native directory move is Windows-only')
    os.rename(source, target)  # Same-volume Windows rename refuses existing target.


def run(root, plan, journal, approval=None, undo=False):
    root = shape(root, plan)
    journal = Path(journal).absolute()
    relative = journal.relative_to(root).as_posix()
    migration.safe(root, relative)
    if not relative.startswith(plan['supplier'] + '/work/migrations/' + plan['run'] + '/'):
        raise ValueError('journal must be in this local migration run')
    if any(relative == name or relative.startswith(name + '/') for row in plan['directories']
           for name in (row['source'], row['destination'])):
        raise ValueError('journal overlaps directory tree')
    if not undo:
        migration.authorize(root, plan, approval)
    if journal.exists():
        lines = journal.read_bytes().splitlines()
        first = json.loads(lines[0])
        if (first.get('root') != str(root) or first.get('plan_sha256') != migration.plan_hash(plan)
                or first.get('seal') != migration.plan_hash({key: value for key, value in first.items() if key != 'seal'})):
            raise ValueError('directory journal root/plan/checksum changed')
        migration.authorize(root, plan, first['authorization'])
        if not undo and first['authorization'] != approval:
            raise ValueError('journal authorization changed')
        for line in lines[1:]:
            json.loads(line)  # Refuse damaged records; never silently truncate.
    else:
        if undo:
            raise ValueError('undo requires existing journal')
        if any(state(root, row) != 'original' for row in plan['directories']):
            raise ValueError('new run requires original trees')
        first = {'kind': 'begin', 'root': str(root), 'plan_sha256': migration.plan_hash(plan),
                 'authorization': approval}
        first['seal'] = migration.plan_hash(first)
        journal.parent.mkdir(parents=True, exist_ok=True)
        with journal.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(json.dumps(first) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
    # Whole-batch checks before the first move, including retry and undo.
    for row in plan['directories']:
        state(root, row)
    expected = 'original' if undo else 'moved'
    for row in reversed(plan['directories']) if undo else plan['directories']:
        if state(root, row) == expected:
            continue
        source, target = ((root / row['destination'], root / row['source']) if undo
                          else (root / row['source'], root / row['destination']))
        target.parent.mkdir(parents=True, exist_ok=True)
        native_move(source, target)
        if state(root, row) != expected:
            raise ValueError('native move changed directory metadata')
        migration.append(journal, {'kind': expected, 'source': row['source'], 'destination': row['destination']})
    migration.append(journal, {'kind': 'undo-complete' if undo else 'apply-complete'})
    return {'mode': 'undo' if undo else 'apply', 'directories': len(plan['directories']), 'state': expected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--mode', choices=['prepare', 'preview', 'apply', 'undo'], default='preview')
    parser.add_argument('--supplier')
    parser.add_argument('--run')
    parser.add_argument('--file-map', type=Path)
    parser.add_argument('--journal', type=Path)
    parser.add_argument('--authorization', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.mode == 'prepare':
        if not args.supplier or not args.run:
            parser.error('prepare requires supplier and run')
        result = prepare(args.root, args.supplier, args.run, migration.load(args.file_map) if args.file_map else None)
    else:
        if not args.plan:
            parser.error('plan required')
        plan = migration.load(args.plan)
        if args.mode == 'preview':
            result = preview(args.root, plan)
        else:
            if not args.journal or args.mode == 'apply' and not args.authorization:
                parser.error('journal and apply authorization required')
            result = run(args.root, plan, args.journal,
                         migration.load(args.authorization) if args.authorization else None, args.mode == 'undo')
    if args.output:
        root = migration.root_path(args.root)
        name = args.output.absolute().relative_to(root).as_posix()
        target = migration.safe(root, name)
        if not name.startswith('PKE_SA_NQA1_doc/plans/cleanup-cu3/'):
            parser.error('output must be a fresh cleanup review artifact')
        with target.open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'mode': args.mode, 'directories': len(result['directories']),
                      'plan_sha256': migration.plan_hash(result)} if args.mode == 'prepare' else result))
    return int(args.mode == 'preview' and not result['ready'])


if __name__ == '__main__':
    raise SystemExit(main())
