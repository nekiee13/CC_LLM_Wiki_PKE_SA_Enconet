"""Validate a supplier's preserved runtime/data in an isolated v4 snapshot.

Copy only into a fresh workspace scratch location. Never copy agent-owned trees
or CC/CLAUDE files. No live source, ledger, database or gate is written.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from prepare_supplier_layout_overlay import regular
from prepare_framework_candidate_v4 import MOVED

WORKSPACE = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(supplier, overlay, destination):
    source = WORKSPACE / supplier
    if (supplier in {'', '.', '..'} or Path(supplier).name != supplier
            or not source.is_dir() or source.resolve().parent != WORKSPACE):
        raise ValueError('explicit local supplier required')
    overlay = Path(overlay).resolve(strict=True)
    destination = Path(destination).absolute()
    if destination.exists() or not destination.resolve().is_relative_to(WORKSPACE / '.tmp'):
        raise ValueError('fresh workspace scratch destination required')
    manifest = json.loads((overlay / 'candidate-manifest.json').read_text(encoding='utf-8'))
    if manifest['source_supplier'] != supplier or manifest['holds']:
        raise ValueError('foreign or held overlay')
    for row in manifest['files']:
        name = row['path']
        if Path(name).is_absolute() or '..' in Path(name).parts or ':' in name or '\\' in name:
            raise ValueError('unsafe overlay payload path')
        if '.claude' in Path(name).parts or Path(name).name == 'CLAUDE.md' or Path(name).name.startswith('CC_'):
            raise ValueError('Claude-owned overlay payload refused')
        if sha(overlay / row['path']) != row['sha256']:
            raise ValueError('overlay hash differs')
    for row in manifest['changes']:
        if sha(source / row['path']) != row['before_sha256']:
            raise ValueError('live runtime changed since overlay preparation')
    with zipfile.ZipFile(WORKSPACE / 'PKE_SA_NQA1_doc/plans/cleanup-cu1/compiled-map/file-moves-final.zip') as archive:
        old_map = json.loads(archive.read(archive.namelist()[0]))
    mapping = {row['source'].removeprefix(supplier + '/'): row['destination'].removeprefix(supplier + '/')
               for row in old_map['files'] if row['source'].startswith(supplier + '/')}
    observed, skipped = {}, []
    destination.mkdir(parents=True, exist_ok=False)
    areas = {'scripts', 'schemas', 'raw', 'db', 'sieving', 'wiki', 'docs',
             'derived', 'manifests', 'benchmarks', 'outputs', 'out', 'handoffs', '.agents'}
    for top in sorted(source.iterdir()):
        if top.is_dir() and top.name not in areas:
            continue
        if top.is_file() and top.name not in {'project-state.yml', 'HANDOFF.md', 'handoff_schema.yml'}:
            continue
        candidates = []
        if top.is_file():
            candidates = [top]
        else:
            for folder, directories, filenames in os.walk(top, followlinks=False):
                directories[:] = [name for name in directories if name not in {
                    '.claude', '.git', '__pycache__', '.tmp', 'backups', 'tests'}
                    and not (Path(folder) / name).is_symlink()]
                candidates.extend(Path(folder) / name for name in filenames)
        for path in candidates:
            name = path.relative_to(source).as_posix()
            if path.name == 'CLAUDE.md' or path.name.startswith('CC_') or path.suffix == '.pyc':
                skipped.append(name)
                continue
            data = regular(path)
            observed[name] = hashlib.sha256(data).hexdigest()
            target_name = mapping.get(name, name)
            if target_name == name:
                parts = name.split('/')
                if parts[0] in MOVED:
                    target_name = '/'.join((MOVED[parts[0]], *parts[1:]))
            target = destination / target_name
            if not target.resolve().is_relative_to(destination):
                raise ValueError('snapshot target escapes scratch root')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    for row in manifest['files']:
        target = destination / row['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((overlay / row['path']).read_bytes())
    aliases = dict(mapping)
    for old, new in mapping.items():
        parts = old.split('/')
        if parts[0] in MOVED:
            generic = '/'.join((MOVED[parts[0]], *parts[1:]))
            if generic != new:
                if generic in aliases and aliases[generic] != new:
                    raise ValueError('ambiguous relocated logical path')
                aliases[generic] = new
    (destination / 'project-file-relocations.json').write_text(json.dumps(
        {'schema_version': 1, 'paths': aliases}, ensure_ascii=False, indent=2), encoding='utf-8')
    pointer = destination / 'HANDOFF.md'
    if pointer.exists():
        pointer.write_text(pointer.read_text(encoding='utf-8').replace('(handoffs/', '(coordination/handoffs/'), encoding='utf-8')
    # An empty incoming directory is sufficient for reset preview root checks.
    (destination / 'incoming').mkdir(exist_ok=True)
    commands = [
        ['validate_raw_sources.py'], ['validate_chunks.py', '--no-record'],
        ['validate_traceability.py', '--active-only', '--no-record'],
        ['validate_requirements.py', '--no-record'], ['audit_command.py', 'audit-status'],
        ['reset_audit.py'], ['run_all_validations.py', '--no-record', '--allow-pending-claude'],
    ]
    packages = list((destination / 'outputs').glob('RUN-*/evaluation_package.json'))
    if len(packages) == 1:
        package = json.loads(packages[0].read_text(encoding='utf-8'))
        run = package['run']['run_id']
        run_root = packages[0].parent
        commands.extend([
            ['validate_evaluation.py', '--run-id', run],
            ['package_audit_delivery.py', '--run-id', run,
             '--light', str(run_root / 'dashboard_light.html'),
             '--dark', str(run_root / 'dashboard_dark.html'), '--output', str(run_root)],
        ])
    records = []
    db_before = sha(destination / 'db/nqa_audit.sqlite')
    for command in commands:
        result = subprocess.run([sys.executable, '-B', str(destination / 'scripts' / command[0]), *command[1:]],
                                cwd=destination, capture_output=True, text=True, encoding='utf-8', timeout=180)
        records.append({'command': command, 'exit_code': result.returncode,
                        'stdout': result.stdout, 'stderr': result.stderr})
    changed = [name for name, digest in observed.items() if sha(source / name) != digest]
    if changed or sha(destination / 'db/nqa_audit.sqlite') != db_before:
        raise ValueError('source files or snapshot database changed during checks')
    receipt = {'schema': 'supplier-layout-snapshot-1', 'supplier': supplier,
               'copied_files': len(observed), 'skipped_owned_files': skipped,
               'source_files_unchanged': not changed, 'snapshot_database_unchanged': True,
               'claude_infrastructure': 'deferred in isolated copy; no Claude infrastructure copied or edited',
               'commands': records, 'passed': all(row['exit_code'] == 0 for row in records)}
    with (destination / 'snapshot-verification.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--supplier', required=True)
    parser.add_argument('--overlay', required=True, type=Path)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    receipt = verify(args.supplier, args.overlay, args.destination)
    print(json.dumps({'passed': receipt['passed'], 'copied_files': receipt['copied_files'],
                      'commands': [{key: row[key] for key in ('command', 'exit_code')} for row in receipt['commands']]}))
    return int(not receipt['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
