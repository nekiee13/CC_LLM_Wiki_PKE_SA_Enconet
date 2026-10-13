"""Retain classified pytest scratch without deletion or shortcut traversal.

Empty-tree profiles preserve captured internal historical symbolic links.
The separate populated profile is limited to five classified synthetic-test
and cache trees, with per-file content/identity/ACL witnesses and no shortcuts.
Rename preserves metadata; unchanged absolute shortcuts become historical
(not runnable) until undo restores the original root.
"""
import argparse
import json
import os
from pathlib import Path
import stat

import cleanup_empty_homes as homes
import cleanup_migration as migration

SOURCE = 'pytest-pilot-temp'
DESTINATION = '.tmp/cleanup-retained-20261013/pytest-pilot-temp'


def scratch_path(root, name):
    # The shared migration guard excludes the release tree. This narrower
    # doorway permits only test scratch beneath audit_template/tests/.
    if name.startswith('audit_template/tests/'):
        return migration.safe(root / 'audit_template', name[len('audit_template/'):])
    return migration.safe(root, name)


def witness(root, current, source=SOURCE, expected_links=6, allow_files=False):
    nodes, links = {}, {}
    regular = {}
    original = root / source
    def denied(error):
        raise error
    for folder, directories, files in os.walk(current, followlinks=False, onerror=denied):
        folder = Path(folder)
        scratch_path(root, folder.relative_to(root).as_posix())
        node = migration.identity(folder)
        node.pop('mtime_ns')
        node['acl_sha256'] = homes.acl_hash(folder)
        nodes[folder.relative_to(current).as_posix()] = node
        for name in directories + files:
            child = folder / name
            info = child.lstat()
            if getattr(info, 'st_file_attributes', 0) & 0x400:
                if not stat.S_ISLNK(info.st_mode):
                    raise ValueError('Unknown reparse type')
                raw = os.readlink(child)
                target = Path(raw.removeprefix('\\\\?\\'))
                if not target.is_absolute() or not target.is_relative_to(original):
                    raise ValueError('External shortcut refused')
                links[child.relative_to(current).as_posix()] = dict(
                    ino=info.st_ino, device=info.st_dev, attributes=info.st_file_attributes, target=raw)
            else:
                scratch_path(root, child.relative_to(root).as_posix())
                if allow_files and stat.S_ISREG(info.st_mode):
                    if info.st_nlink != 1:
                        raise ValueError('Hard-linked fixture refused')
                    entry = migration.identity(child)
                    entry['acl_sha256'] = homes.acl_hash(child)
                    entry['sha256'] = migration.digest(child)
                    if migration.identity(child) != {k: v for k, v in entry.items()
                                                     if k not in {'acl_sha256', 'sha256'}}:
                        raise ValueError('Fixture changed while reading')
                    regular[child.relative_to(current).as_posix()] = entry
                elif not stat.S_ISDIR(info.st_mode):
                    raise ValueError('Regular files or unknown nodes remain')
    if expected_links is not None and len(links) != expected_links:
        raise ValueError('Expected six classified pytest shortcuts')
    # Every link names an empty real directory captured in the same original
    # tree. Never resolve a link or accept an uncaptured destination.
    for link in links.values():
        relative = Path(link['target'].removeprefix('\\\\?\\')).relative_to(original).as_posix()
        if relative not in nodes:
            raise ValueError('Shortcut target is not a captured empty directory')
    result = dict(directories=nodes, shortcuts=links)
    if allow_files:
        result['files'] = regular
    return result


LEGACY_TOP = (
    'Enconet/.pytest-ea22-red', 'Enconet/.pytest-tmp-epic-review',
    'Enconet/.pytest-tmp-g4-20260728', 'Enconet/.pytest_tmp',
    'Enconet/pytest-cache-files-fgtlfzwi', 'Enconet/pytest-cache-files-sglcfhjt',
    'doc/support-transfer/staged',
)
LEGACY_PARENTS = ('Enconet/.test-tmp', 'audit_template/tests')
POPULATED_TEST_HISTORY = (
    'audit_template/tests/analysis-bundle-yupz4b7d',
    'audit_template/tests/phase-criteria-382h_mz1',
    'audit_template/tests/source-validators-0ex7vaq2',
    'audit_template/tests/source-validators-94s0r7sf',
    'audit_template/tests/__pycache__',
)


def legacy_destination(source):
    if source not in LEGACY_TOP and Path(source).parent.as_posix() not in LEGACY_PARENTS:
        raise ValueError('Unknown legacy scratch source')
    if source.startswith('Enconet/'):
        return 'Enconet/.tmp/cleanup-retained-20261014/' + source[len('Enconet/'):]
    return '.tmp/cleanup-retained-20261014/' + source


def prepare_legacy(root, authority):
    sources = list(LEGACY_TOP)
    for parent in LEGACY_PARENTS:
        base = root / parent
        if base.exists():
            sources.extend(p.relative_to(root).as_posix() for p in base.iterdir()
                           if stat.S_ISDIR(p.lstat().st_mode)
                           and not getattr(p.lstat(), 'st_file_attributes', 0) & 0x400)
    rows, held = [], []
    for source in sorted(sources):
        try:
            current = scratch_path(root, source)
            if not current.exists():
                continue
            destination = legacy_destination(source)
            if migration.safe(root, destination).exists():
                raise ValueError('Destination already exists')
            actual = witness(root, current, source, None)
            rows.append(dict(source=source, destination=destination, witness=actual))
        except (ValueError, OSError) as error:
            held.append(dict(source=source, reason=str(error)))
    if not rows:
        raise ValueError('No eligible legacy empty scratch')
    return dict(schema='legacy-empty-scratch-1', root=str(root), rows=rows, held=held,
                authority_sha256=migration.digest(authority))


def prepare_populated(root, authority):
    rows = []
    for source in POPULATED_TEST_HISTORY:
        current = scratch_path(root, source)
        if not current.is_dir():
            raise ValueError('Populated history source missing or not a directory')
        destination = legacy_destination(source)
        if migration.safe(root, destination).exists():
            raise ValueError('Populated history destination collision')
        rows.append(dict(source=source, destination=destination,
                         witness=witness(root, current, source, 0, allow_files=True)))
    return dict(schema='legacy-populated-test-history-1', root=str(root), rows=rows,
                held=[], authority_sha256=migration.digest(authority))


def run_legacy(root, plan, authority, mode, populated=False):
    root = migration.root_path(root)
    schema = 'legacy-populated-test-history-1' if populated else 'legacy-empty-scratch-1'
    if (plan.get('schema') != schema or plan.get('root') != str(root)
            or plan.get('authority_sha256') != migration.digest(authority)):
        raise ValueError('Legacy plan root or authority differs')
    rows = plan['rows']
    if populated and [r['source'] for r in rows] != list(POPULATED_TEST_HISTORY):
        raise ValueError('Populated test-history scope differs')
    if not rows or len({r['source'].casefold() for r in rows}) != len(rows):
        raise ValueError('Empty or duplicate legacy batch')

    def state(row):
        if row['destination'] != legacy_destination(row['source']):
            raise ValueError('Foreign legacy destination')
        old = scratch_path(root, row['source'])
        new = migration.safe(root, row['destination'])
        if old.exists() == new.exists():
            raise ValueError('Collision or both homes missing')
        current = old if old.exists() else new
        if witness(root, current, row['source'], 0 if populated else None,
                   allow_files=populated) != row['witness']:
            raise ValueError('Legacy identity, ACL or contents changed')
        return 'original' if old.exists() else 'moved'

    # Complete no-follow preflight before the first rename, also on retry/undo.
    states = [state(row) for row in rows]
    expected = 'original' if mode == 'undo' else 'moved'
    if mode == 'verify':
        if any(s != expected for s in states):
            raise ValueError('Legacy batch incomplete')
    elif mode in {'apply', 'undo'}:
        for row in reversed(rows) if mode == 'undo' else rows:
            if state(row) == expected:
                continue
            old, new = ((row['destination'], row['source']) if mode == 'undo'
                        else (row['source'], row['destination']))
            target = scratch_path(root, new)
            target.parent.mkdir(parents=True, exist_ok=True)
            homes.native_move(scratch_path(root, old), target)
            if state(row) != expected:
                raise ValueError('Legacy post-rename mismatch')
    else:
        raise ValueError('Unknown legacy action')
    return dict(mode=mode, directories=len(rows),
                directory_nodes=sum(len(r['witness']['directories']) for r in rows),
                shortcuts=sum(len(r['witness']['shortcuts']) for r in rows),
                files=sum(len(r['witness'].get('files', {})) for r in rows),
                held=len(plan['held']), preserved=True, plan_sha256=migration.plan_hash(plan))


def run(root, plan, authority, mode):
    root = migration.root_path(root)
    source = migration.safe(root, SOURCE)
    destination = migration.safe(root, DESTINATION)
    if source.exists() == destination.exists():
        raise ValueError('Collision or both homes missing')
    state = 'original' if source.exists() else 'moved'
    current = source if source.exists() else destination
    actual = witness(root, current)
    if (plan['root'] != str(root) or plan['source'] != SOURCE or plan['destination'] != DESTINATION
            or migration.digest(authority) != plan['authority_sha256'] or actual != plan['witness']):
        raise ValueError('Bound plan, authority or identity/ACL changed')
    if mode == 'verify':
        if state != 'moved':
            raise ValueError('Not archived')
    else:
        expected = 'original' if mode == 'undo' else 'moved'
        if state != expected:
            target = source if mode == 'undo' else destination
            target.parent.mkdir(parents=True, exist_ok=True)
            homes.native_move(current, target)
            if witness(root, target) != actual:
                raise ValueError('Post-rename metadata differs')
    return dict(mode=mode, directory_count=len(actual['directories']), shortcut_count=len(actual['shortcuts']),
                plan_sha256=migration.plan_hash(plan), preserved=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--mode', choices=['preview', 'apply', 'verify', 'undo'], required=True)
    parser.add_argument('--bundle', choices=['root-pilot', 'legacy-empty', 'populated-test-history'], default='root-pilot')
    args = parser.parse_args()
    root = migration.root_path(args.root)
    for path in (args.plan, args.authority):
        migration.safe(root, path.absolute().relative_to(root).as_posix())
    if args.bundle in {'legacy-empty', 'populated-test-history'}:
        populated = args.bundle == 'populated-test-history'
        if args.mode == 'preview':
            plan = prepare_populated(root, args.authority) if populated else prepare_legacy(root, args.authority)
            with args.plan.open('x', encoding='utf-8', newline='\n') as stream:
                json.dump(plan, stream, indent=2)
            result = dict(mode='preview', directories=len(plan['rows']), held=len(plan['held']),
                          plan_sha256=migration.plan_hash(plan))
        else:
            result = run_legacy(root, migration.load(args.plan), args.authority, args.mode, populated=populated)
        print(json.dumps(result))
        return
    if args.mode == 'preview':
        if (root / DESTINATION).exists():
            raise ValueError('Destination already exists')
        actual = witness(root, migration.safe(root, SOURCE))
        plan = dict(root=str(root), source=SOURCE, destination=DESTINATION,
                    authority_sha256=migration.digest(args.authority), witness=actual)
        with args.plan.open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(plan, stream, indent=2)
        result = dict(mode='preview', directory_count=len(actual['directories']),
                      shortcut_count=len(actual['shortcuts']), plan_sha256=migration.plan_hash(plan))
    else:
        result = run(root, migration.load(args.plan), args.authority, args.mode)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
