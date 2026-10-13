"""Archive one classified root pytest tree without following its shortcuts.

Only empty real directories and six internal historical symbolic links are
accepted. Rename preserves all metadata; unchanged absolute shortcuts become
historical (not runnable) until undo restores the original root.
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


def witness(root, current):
    nodes, links = {}, {}
    original = root / SOURCE
    def denied(error):
        raise error
    for folder, directories, files in os.walk(current, followlinks=False, onerror=denied):
        folder = Path(folder)
        migration.safe(root, folder.relative_to(root).as_posix())
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
                migration.safe(root, child.relative_to(root).as_posix())
                if not stat.S_ISDIR(info.st_mode):
                    raise ValueError('Regular files or unknown nodes remain')
    if len(links) != 6:
        raise ValueError('Expected six classified pytest shortcuts')
    # Every link names an empty real directory captured in the same original
    # tree. Never resolve a link or accept an uncaptured destination.
    for link in links.values():
        relative = Path(link['target'].removeprefix('\\\\?\\')).relative_to(original).as_posix()
        if relative not in nodes:
            raise ValueError('Shortcut target is not a captured empty directory')
    return dict(directories=nodes, shortcuts=links)


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
    args = parser.parse_args()
    root = migration.root_path(args.root)
    for path in (args.plan, args.authority):
        migration.safe(root, path.absolute().relative_to(root).as_posix())
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
