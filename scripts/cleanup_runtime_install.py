"""Bound runtime installation with byte-exact backups, preview, retry and undo.

No Git staging, source/DB changes, approval factory or recursive deletion.
Payload files must already exist in workspace .tmp. Review before live use.
"""
import argparse
import json
from pathlib import Path, PurePosixPath

import cleanup_migration as migration


def structure(root, plan):
    root = migration.root_path(root)
    supplier = plan.get('supplier')
    if (plan.get('schema') != 'cleanup-runtime-install-1' or not isinstance(supplier, str)
            or len(PurePosixPath(supplier).parts) != 1 or supplier in {'.', '..'}):
        raise ValueError('explicit supplier installation plan required')
    migration.safe(root, supplier)
    if not (root / supplier).is_dir():
        raise ValueError('supplier root missing')
    seen = set()
    if not isinstance(plan.get('files'), list) or not plan['files']:
        raise ValueError('nonempty installation required')
    for row in plan['files']:
        name = row['target']
        parts = PurePosixPath(name).parts
        if parts[0] != supplier or not (
                len(parts) == 3 and parts[1] == 'scripts' and parts[2].endswith('.py')
                or len(parts) == 2 and parts[1] in {
                    'project-layout.json', 'project-file-relocations.json'}):
            raise ValueError('runtime/configuration targets only')
        for key in ('target', 'payload', 'backup'):
            value = row[key]
            migration.safe(root, value)
            if value.casefold() in seen:
                raise ValueError('installation path collision')
            seen.add(value.casefold())
        if not row['payload'].startswith('.tmp/'):
            raise ValueError('payload must be workspace scratch')
        if not row['backup'].startswith(supplier + '/work/migrations/'):
            raise ValueError('backup must be local migration history')
    # Layout activation is the final file, never the first operation.
    layouts = [row['target'] for row in plan['files'] if row['target'].endswith('/project-layout.json')]
    if layouts and plan['files'][-1]['target'] != layouts[0]:
        raise ValueError('layout activation must be last')
    return root


def prepare(root, supplier, entries, backup_home):
    """Read-only plan. Each entry is (supplier-relative target, staged payload)."""
    root = migration.root_path(root)
    rows = []
    for name, payload in entries:
        target_name = supplier + '/' + name
        target = migration.safe(root, target_name)
        staged = migration.safe(root, payload)
        if not staged.is_file():
            raise ValueError('staged payload missing')
        if target.exists() and not target.is_file():
            raise ValueError('runtime target not a file')
        rows.append({'target': target_name, 'payload': payload,
                     'backup': supplier + '/' + backup_home + '/' + name,
                     'before_sha256': migration.digest(target) if target.exists() else None,
                     'after_sha256': migration.digest(staged)})
    rows.sort(key=lambda row: (row['target'].endswith('/project-layout.json'), row['target']))
    plan = {'schema': 'cleanup-runtime-install-1', 'supplier': supplier, 'files': rows}
    structure(root, plan)
    for row in rows:
        if (root / row['backup']).exists():
            raise ValueError('backup already exists')
    return plan


def matches(path, digest, witness=None):
    return (path.is_file() and migration.digest(path) == digest
            and (witness is None or migration.identity(path) == witness))


def state(root, row, witness=None):
    target, staged, backup = [migration.safe(root, row[key]) for key in ('target', 'payload', 'backup')]
    old = row['before_sha256']
    before = witness['before'] if witness else None
    after = witness['after'] if witness else None
    if (matches(staged, row['after_sha256'], after) and not backup.exists()
            and (matches(target, old, before) if old else not target.exists())):
        return 'original'
    saved = matches(backup, old, before) if old else not backup.exists()
    if saved and matches(staged, row['after_sha256'], after) and not target.exists():
        return 'backed-up'
    if saved and matches(target, row['after_sha256'], after) and not staged.exists():
        return 'installed'
    raise ValueError('installation file changed, missing or collided: ' + row['target'])


def journal_file(root, plan, journal):
    journal = Path(journal).absolute()
    name = journal.relative_to(root).as_posix()
    migration.safe(root, name)
    if not name.startswith(plan['supplier'] + '/work/migrations/'):
        raise ValueError('journal must be local migration history')
    if any(name in {row[key] for key in ('target', 'payload', 'backup')} for row in plan['files']):
        raise ValueError('journal overlaps installation')
    return journal


def header(root, plan, journal):
    lines = journal.read_bytes().splitlines()
    if not lines:
        raise ValueError('empty installation journal')
    first = json.loads(lines[0])
    if (first.get('kind') != 'begin' or first.get('root') != str(root)
            or first.get('plan_sha256') != migration.plan_hash(plan)
            or first.get('seal') != migration.plan_hash({key: value for key, value in first.items() if key != 'seal'})
            or set(first.get('identities', {})) != {row['target'] for row in plan['files']}
            or first.get('new_directories') != []):
        raise ValueError('installation journal differs from bound plan')
    migration.authorize(root, plan, first['authorization'])
    events = [first]
    for index, line in enumerate(lines[1:], 1):
        try:
            events.append(json.loads(line))
        except (ValueError, UnicodeError):
            # No moves rely on event counts. Refuse damaged committed records;
            # an incomplete final append is safe to ignore after full state check.
            if index != len(lines) - 1:
                raise ValueError('damaged committed installation journal')
            events.append({'kind': 'incomplete-final-record'})
    return first, events


def preview(root, plan):
    root = structure(root, plan)
    states = [state(root, row) for row in plan['files']]
    if any(value != 'original' for value in states):
        raise ValueError('fresh preview requires original state')
    return {'mode': 'read-only-preview', 'files': len(states), 'plan_sha256': migration.plan_hash(plan)}


def run(root, plan, journal, approval=None, undo=False):
    root = structure(root, plan)
    journal = journal_file(root, plan, journal)
    if not undo:
        migration.authorize(root, plan, approval)
        if any(row['target'].endswith('/project-layout.json') for row in plan['files']):
            for name in ('benchmarks', 'derived', 'manifests', 'decisions', 'backup',
                         'handoffs', 'out', '.bootstrap', 'docs/reviews'):
                if migration.safe(root, plan['supplier'] + '/' + name).exists():
                    raise ValueError('legacy working home remains; layout not ready: ' + name)
    if journal.exists():
        first, events = header(root, plan, journal)
        if not undo and first['authorization'] != approval:
            raise ValueError('authorization differs from journal')
    else:
        if undo:
            raise ValueError('undo requires existing journal')
        preview(root, plan)
        first = {'kind': 'begin', 'root': str(root), 'plan_sha256': migration.plan_hash(plan),
                 'authorization': approval, 'new_directories': [], 'identities': {}}
        for row in plan['files']:
            target, staged = root / row['target'], root / row['payload']
            first['identities'][row['target']] = {
                'before': migration.identity(target) if target.exists() else None,
                'after': migration.identity(staged)}
        first['seal'] = migration.plan_hash(first)
        # Validate every state before any writes, including journal creation.
        for row in plan['files']:
            state(root, row, first['identities'][row['target']])
        journal.parent.mkdir(parents=True, exist_ok=True)
        with journal.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(json.dumps(first, ensure_ascii=False) + '\n')
            stream.flush()
            import os
            os.fsync(stream.fileno())
        events = [first]
    for row in plan['files']:
        state(root, row, first['identities'][row['target']])
    if events[-1].get('kind') == 'incomplete-final-record':
        raise ValueError('incomplete journal append; preserve and review before retry')
    for row in reversed(plan['files']) if undo else plan['files']:
        current = state(root, row, first['identities'][row['target']])
        target, staged, backup = [root / row[key] for key in ('target', 'payload', 'backup')]
        if undo:
            if current == 'installed':
                migration.move_no_replace(target, staged)
                migration.append(journal, {'kind': 'uninstalled', 'target': row['target']})
                current = 'backed-up'
            if current == 'backed-up' and row['before_sha256']:
                migration.move_no_replace(backup, target)
                migration.append(journal, {'kind': 'restored', 'target': row['target']})
        else:
            if current == 'original' and row['before_sha256']:
                backup.parent.mkdir(parents=True, exist_ok=True)
                migration.move_no_replace(target, backup)
                migration.append(journal, {'kind': 'backed-up', 'target': row['target']})
                current = 'backed-up'
            if current != 'installed':
                target.parent.mkdir(parents=True, exist_ok=True)
                migration.move_no_replace(staged, target)
                migration.append(journal, {'kind': 'installed', 'target': row['target']})
    expected = 'original' if undo else 'installed'
    if any(state(root, row, first['identities'][row['target']]) != expected for row in plan['files']):
        raise ValueError('installation did not reach expected state')
    migration.append(journal, {'kind': 'undo-complete' if undo else 'apply-complete'})
    return {'mode': 'undo' if undo else 'apply', 'files': len(plan['files']), 'state': expected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--mode', choices=['preview', 'apply', 'undo'], default='preview')
    parser.add_argument('--journal', type=Path)
    parser.add_argument('--authorization', type=Path)
    args = parser.parse_args()
    plan = migration.load(args.plan)
    if args.mode == 'preview':
        result = preview(args.root, plan)
    else:
        if not args.journal or args.mode == 'apply' and not args.authorization:
            parser.error('apply requires journal/authorization; undo requires journal')
        result = run(args.root, plan, args.journal,
                     migration.load(args.authorization) if args.authorization else None,
                     undo=args.mode == 'undo')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
