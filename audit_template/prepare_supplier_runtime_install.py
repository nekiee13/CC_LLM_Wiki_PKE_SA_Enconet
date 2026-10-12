"""Prepare exact runtime installation payload/plan in fresh workspace scratch.

No installation, authorization or live file writes. The emitted plan must be
reviewed before cleanup_runtime_install.py can apply it.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from prepare_supplier_layout_overlay import regular
from prepare_supplier_cleanup_batch import relocation_aliases

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / 'scripts'))
import cleanup_migration as migration
import cleanup_runtime_install as installer


def prepare(supplier, overlay, file_map, destination, backup_home):
    source = migration.safe(WORKSPACE, supplier)
    if (supplier in {'', '.', '..'} or Path(supplier).name != supplier
            or source.parent != WORKSPACE or not source.is_dir()):
        raise ValueError('one local supplier required')
    destination = Path(destination).absolute()
    relative = destination.relative_to(WORKSPACE).as_posix()
    migration.safe(WORKSPACE, relative)
    if not relative.startswith('.tmp/') or destination.exists():
        raise ValueError('fresh workspace scratch required')
    overlay = Path(overlay).absolute()
    migration.safe(WORKSPACE, overlay.relative_to(WORKSPACE).as_posix())
    manifest = json.loads(regular(overlay / 'candidate-manifest.json'))
    if manifest['source_supplier'] != supplier or manifest['holds']:
        raise ValueError('foreign or held overlay')
    files = {row['path']: row['sha256'] for row in manifest['files']}
    changes = {row['path']: row for row in manifest['changes']}
    chosen = manifest['install_paths']
    if len(set(chosen)) != len(chosen):
        raise ValueError('duplicate installation path')
    bodies = {}
    for name in chosen:
        migration.safe(source, name)
        body = regular(overlay / name)
        if hashlib.sha256(body).hexdigest() != files[name]:
            raise ValueError('overlay payload hash changed')
        target = source / name
        if name in changes:
            if hashlib.sha256(regular(target)).hexdigest() != changes[name]['before_sha256']:
                raise ValueError('current runtime differs from overlay')
        elif target.exists():
            raise ValueError('new runtime file already exists')
        bodies[name] = body
    plan = migration.load(file_map)
    if plan['schema'] != 'cleanup-file-map-1':
        raise ValueError('unsupported relocation plan')
    if migration.preview(WORKSPACE, plan)['blocked']:
        raise ValueError('relocation preview blocked')
    mapping = relocation_aliases(plan['files'], supplier)
    bodies['project-file-relocations.json'] = (json.dumps(mapping, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if 'project-layout.json' not in bodies:
        raise ValueError('layout config missing')
    # Validate the complete installation shape before creating any scratch files.
    shape = {'schema': 'cleanup-runtime-install-1', 'supplier': supplier, 'files': [
        {'target': supplier + '/' + name, 'payload': relative + '/payload/' + name,
         'backup': supplier + '/' + backup_home + '/' + name}
        for name in sorted(bodies, key=lambda name: (name == 'project-layout.json', name))]}
    installer.structure(WORKSPACE, shape)
    destination.mkdir(parents=True, exist_ok=False)
    for name, body in bodies.items():
        target = destination / 'payload' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(body)
    result = installer.prepare(WORKSPACE, supplier,
                               [(name, relative + '/payload/' + name) for name in bodies], backup_home)
    with (destination / 'installation-plan.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    return {'mode': 'prepared-not-applied', 'files': len(result['files']),
            'plan_sha256': migration.plan_hash(result), 'logical_aliases': len(mapping['paths'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--supplier', required=True)
    parser.add_argument('--overlay', required=True, type=Path)
    parser.add_argument('--file-map', required=True, type=Path)
    parser.add_argument('--destination', required=True, type=Path)
    parser.add_argument('--backup-home', required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.supplier, args.overlay, args.file_map, args.destination, args.backup_home)))


if __name__ == '__main__':
    main()
