"""One owner-approved, move-only retention of Enconet's generated test fixtures.

The normal ownership guard is unchanged. Only the two exact parent homes here
permit reading witnesses inside generated .claude copies; no file is edited.
Native rename preserves the tree, and no shortcut target is followed or rewritten.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

import archive_pytest_scratch as scratch
import cleanup_migration as migration

SOURCE = 'Enconet/.test-tmp'
DESTINATION = 'Enconet/.tmp/cleanup-retained-20261014/protected-test-fixtures'
BASELINE = 'PKE_SA_NQA1_doc/plans/cleanup-cu4/legacy-empty-archive-plan.json'


def fixture_path(root, name):
    parts = PurePosixPath(name).parts
    if (not parts or PurePosixPath(name).is_absolute() or '\\' in name
            or any(p in {'.', '..'} or ':' in p or p.rstrip(' .') != p for p in parts)
            or any(p.casefold() in {'.git', '.agents'} for p in parts)):
        raise ValueError('Unsafe fixture path')
    path = root.joinpath(*parts)
    homes = [migration.safe(root, home) for home in (SOURCE, DESTINATION)]
    base = next((p for p in homes if path.is_relative_to(p)), None)
    if base is None:
        raise ValueError('Outside exact owner-approved fixture homes')
    # lstat only: neither an ancestor redirect nor a hard link is accepted.
    for candidate in (path, *path.parents):
        if not candidate.is_relative_to(base):
            break
        try:
            info = candidate.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('Redirected fixture path')
        if candidate != path and not stat.S_ISDIR(info.st_mode):
            raise ValueError('Fixture parent is not a directory')
        if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
            raise ValueError('Hard-linked fixture path')
    return path


def expected_names(root):
    baseline = migration.load(root / BASELINE)
    names = sorted(Path(row['source']).name for row in baseline['held']
                   if row['source'].startswith(SOURCE + '/'))
    if len(names) != 15 or len(set(names)) != 15:
        raise ValueError('Expected exact fifteen recorded fixture trees')
    return names


def witness(root, current):
    if not current.is_dir():
        raise ValueError('Fixture home missing')
    names = sorted(p.name for p in current.iterdir())
    if names != expected_names(root):
        raise ValueError('Fixture membership differs from reviewed holds')
    for name in names:
        child = fixture_path(root, (current / name).relative_to(root).as_posix())
        if not child.is_dir():
            raise ValueError('Fixture child is not a real directory')
    return scratch.witness(root, current, SOURCE, None, allow_files=True,
                           path_guard=fixture_path)


def prepare(root, authority):
    root = migration.root_path(root)
    old = fixture_path(root, SOURCE)
    if fixture_path(root, DESTINATION).exists():
        raise ValueError('Fixture destination collision')
    return dict(schema='protected-fixture-retention-1', root=str(root), source=SOURCE,
                destination=DESTINATION, authority_sha256=migration.digest(authority),
                baseline_sha256=migration.digest(root / BASELINE), witness=witness(root, old))


def run(root, plan, authority, mode):
    root = migration.root_path(root)
    if (plan.get('schema') != 'protected-fixture-retention-1' or plan.get('root') != str(root)
            or plan.get('source') != SOURCE or plan.get('destination') != DESTINATION
            or plan.get('authority_sha256') != migration.digest(authority)
            or plan.get('baseline_sha256') != migration.digest(root / BASELINE)):
        raise ValueError('Exact fixture plan/root/authority differs')
    old, new = fixture_path(root, SOURCE), fixture_path(root, DESTINATION)
    if old.exists() == new.exists():
        raise ValueError('Fixture collision or both homes missing')
    current = old if old.exists() else new
    actual = witness(root, current)
    if actual != plan['witness']:
        raise ValueError('Fixture content/identity/ACL changed')
    moved = new.exists()
    if mode == 'verify':
        if not moved:
            raise ValueError('Fixture move incomplete')
    elif mode in {'apply', 'undo'}:
        if moved != (mode == 'apply'):
            target = new if mode == 'apply' else old
            target.parent.mkdir(parents=True, exist_ok=True)
            scratch.homes.native_move(current, target)
            if witness(root, target) != actual:
                raise ValueError('Post-rename fixture witness differs')
    else:
        raise ValueError('Unknown fixture mode')
    return dict(mode=mode, fixtures=15, directories=len(actual['directories']),
                files=len(actual['files']), shortcuts=len(actual['shortcuts']),
                preserved=True, plan_sha256=migration.plan_hash(plan))


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
        plan = prepare(root, args.authority)
        if args.plan.suffix != '.zip':
            parser.error('Use a fresh ZIP for the full native witness')
        with zipfile.ZipFile(args.plan, 'x', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('fixture-plan.json', json.dumps(plan, indent=2) + '\n')
        print(json.dumps(dict(mode='preview', fixtures=15, plan_sha256=migration.plan_hash(plan))))
    else:
        print(json.dumps(run(root, migration.load(args.plan), args.authority, args.mode)))


if __name__ == '__main__':
    main()
