"""Preserve bounded bundles of empty cleanup leftovers by native rename.

This bounded CU-4.2 operation never deletes content or changes permissions.
Preview captures directory identity and ACL; apply checks the whole batch first.
"""
import argparse
import json
from pathlib import Path

import cleanup_empty_homes as homes
import cleanup_migration as migration

MOVES = {
    'pytest-min11-one': '.tmp/cleanup-retained-20261013/pytest-min11-one',
    'pytest-min11-temp': '.tmp/cleanup-retained-20261013/pytest-min11-temp',
    'pytest-min11-temp2': '.tmp/cleanup-retained-20261013/pytest-min11-temp2',
    'ekonerg-reset-rk6wsybf': 'Ekonerg/.tmp/cleanup-retained-20261013/ekonerg-reset-rk6wsybf',
    'reset-plans': 'PKE_SA_NQA1_doc/reset-plans/retained-original-directory-20261013',
}
ROOT_CACHES = {
    '.pytest_cache': '.tmp/cleanup-retained-20261013/.pytest_cache',
    '.reset-test-work': '.tmp/cleanup-retained-20261013/.reset-test-work',
}
OLD_DOC = {'doc': '.tmp/cleanup-retained-20261014/old-doc-empty-shells'}


def witness(root, source, destination):
    old = migration.safe(root, source)
    new = migration.safe(root, destination)
    if old.exists() == new.exists():
        raise ValueError('Both homes present or both missing: ' + source)
    current = source if old.exists() else destination
    return homes.tree(root, current), 'original' if old.exists() else 'moved'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--mode', choices=['preview', 'apply', 'verify', 'undo'], required=True)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--journal', type=Path, required=True)
    parser.add_argument('--bundle', choices=['original-five', 'root-caches', 'old-doc'], default='original-five')
    args = parser.parse_args()
    root = migration.root_path(args.root)
    moves = {'original-five': MOVES, 'root-caches': ROOT_CACHES, 'old-doc': OLD_DOC}[args.bundle]
    for path in (args.plan, args.authority, args.journal):
        migration.safe(root, path.absolute().relative_to(root).as_posix())
    if args.mode == 'preview':
        rows = []
        for source, destination in moves.items():
            tree, state = witness(root, source, destination)
            if state != 'original':
                raise ValueError('Preview requires original directory')
            rows.append(dict(source=source, destination=destination, tree=tree))
        plan = dict(schema='cleanup-residual-empty-1', root=str(root), rows=rows,
                    authority_sha256=migration.digest(args.authority))
        with args.plan.open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(plan, stream, indent=2)
    else:
        plan = migration.load(args.plan)
        if (plan.get('schema') != 'cleanup-residual-empty-1'
                or plan.get('root') != str(root)
                or plan.get('authority_sha256') != migration.digest(args.authority)
                or [(r['source'], r['destination']) for r in plan['rows']] != list(moves.items())):
            raise ValueError('Plan or authority differs')
        for row in plan['rows']:
            tree, state = witness(root, row['source'], row['destination'])
            if tree != row['tree'] or args.mode == 'verify' and state != 'moved':
                raise ValueError('Directory content, identity or ACL differs')
        if args.mode in ('apply', 'undo'):
            if args.journal.exists():
                first = json.loads(args.journal.read_text(encoding='utf-8').splitlines()[0])
                if first != dict(kind='begin', plan_sha256=migration.plan_hash(plan)):
                    raise ValueError('Journal differs')
            else:
                if args.mode == 'undo':
                    raise ValueError('Undo requires an existing journal')
                with args.journal.open('x', encoding='utf-8', newline='\n') as stream:
                    stream.write(json.dumps(dict(kind='begin', plan_sha256=migration.plan_hash(plan))) + '\n')
            expected = 'original' if args.mode == 'undo' else 'moved'
            for row in reversed(plan['rows']) if args.mode == 'undo' else plan['rows']:
                _, state = witness(root, row['source'], row['destination'])
                if state == expected:
                    continue
                source_name, target_name = ((row['destination'], row['source']) if args.mode == 'undo'
                                            else (row['source'], row['destination']))
                destination = migration.safe(root, target_name)
                destination.parent.mkdir(parents=True, exist_ok=True)
                homes.native_move(root / source_name, destination)
                tree, state = witness(root, row['source'], row['destination'])
                if tree != row['tree'] or state != expected:
                    raise ValueError('Post-move identity or ACL differs')
                migration.append(args.journal, dict(kind=expected, source=source_name, destination=target_name))
            migration.append(args.journal, dict(kind=args.mode + '-complete'))
    print(json.dumps(dict(mode=args.mode, directories=len(plan['rows']), plan_sha256=migration.plan_hash(plan))))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
