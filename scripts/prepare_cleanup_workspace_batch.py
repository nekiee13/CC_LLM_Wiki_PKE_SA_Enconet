"""Prepare a fresh review-only workspace batch; no moves or authorization.

Select only workspace rows from the prior reviewed inventory. Recheck current
hashes, dirty state, ownership, redirects and destinations. Preserve every hold.
New files absent from the inventory remain held. Emit fresh review artifacts.
"""
import argparse
import json
from pathlib import Path
import zipfile

import cleanup_migration as migration
import cleanup_workflow as workflow


def in_scope(name):
    first = name.split('/')[0]
    return (first in {'doc', 'reset-plans', '.pytest_cache', '.reset-test-work'}
            or first.startswith('pytest') or name == 'Transition_template_Plan.md')


def build(root, inventory_plan):
    root = migration.root_path(root)
    dirty = set(workflow.git(root, 'diff', '--name-only', '-z').decode('utf-8').split('\0'))
    dirty.update(workflow.git(root, 'diff', '--cached', '--name-only', '-z').decode('utf-8').split('\0'))
    selected, held = [], []
    for original in inventory_plan['files']:
        if not in_scope(original['source']):
            continue
        row = dict(original)
        reason = row.get('hold')
        if row['source'] in dirty:
            reason = 'hold-existing-dirty-content'
        if not reason:
            try:
                migration.check_row(root, row)
            except (ValueError, OSError) as error:
                reason = str(error)
        if reason:
            held.append({'source': row['source'], 'destination': row['destination'], 'reason': reason})
        else:
            row['approval'] = 'pending-exact-batch-review'
            selected.append(row)
    known = {row['source'] for row in inventory_plan['files']}
    special = [row for row in inventory_plan.get('special_holds', []) if in_scope(row['source'])]
    held.extend({'source': row['source'], 'reason': row.get('hold', 'inventory special hold')}
                for row in special)
    # Inspect only explicitly scoped top-level areas; never follow redirects.
    import os
    for top in root.iterdir():
        if not in_scope(top.name) or not top.is_dir():
            continue
        try:
            migration.safe(root, top.name)
        except (ValueError, OSError):
            continue  # Recorded by the original special-hold list.
        def failed(error):
            held.append({'source': str(Path(error.filename).relative_to(root)),
                         'reason': 'live enumeration access failure'})
        for folder, directories, filenames in os.walk(top, followlinks=False, onerror=failed):
            for name in list(directories):
                path = Path(folder) / name
                try:
                    migration.safe(root, path.relative_to(root).as_posix())
                except (ValueError, OSError):
                    directories.remove(name)
            for name in filenames:
                source = (Path(folder) / name).relative_to(root).as_posix()
                if source not in known and not any(row['source'] == source for row in special):
                    held.append({'source': source, 'reason': 'not-in-reviewed-inventory'})
    plan = {'schema': 'cleanup-file-map-1', 'status': 'preview-only-not-authorized',
            'capture_head': workflow.repository(root), 'files': selected, 'collisions': []}
    preview = migration.preview(root, plan)
    return plan, {'schema': 'cleanup-workspace-preview-1', 'plan_sha256': migration.plan_hash(plan),
                  'capture_head': plan['capture_head'], 'preview': preview, 'held': held,
                  'limits': ['No live authority; exact-batch review required.',
                             'Workflow plan must be prepared again at application HEAD.',
                             'No directory pruning selected; custom directory ACLs remain untouched.',
                             'Current reference updates must accompany workspace migration.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--map', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = migration.root_path(args.root)
    output = migration.safe(root, args.output.absolute().relative_to(root).as_posix())
    if not output.is_relative_to(root / 'PKE_SA_NQA1_doc/plans/cleanup-cu3') or output.exists():
        raise ValueError('fresh cleanup-cu3 packet directory required')
    plan, receipt = build(root, migration.load(args.map))
    output.mkdir(parents=True, exist_ok=False)
    for filename, value in [('workspace-map.json', plan), ('workspace-preview.json', receipt)]:
        with zipfile.ZipFile(output / (filename + '.zip'), 'x', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(filename, json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'eligible': receipt['preview']['eligible'], 'blocked': receipt['preview']['blocked'],
                      'held': len(receipt['held']), 'plan_sha256': receipt['plan_sha256']}))


if __name__ == '__main__':
    main()
