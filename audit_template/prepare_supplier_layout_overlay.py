"""Read-only preparation of a path overlay from a supplier's own runtime.

Never replace company audit logic with another project's implementation.
Emit a complete script snapshot and mark only changed code for later installation.
Direct-path findings and unadapted integrations keep the overlay un-installable.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import stat

from prepare_framework_candidate_v4 import route_python, replace_assignment, replace_once
from check_candidate_paths_v4 import scan

WORKSPACE = Path(__file__).resolve().parents[1]


def regular(path):
    for item in (path, *path.parents):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('redirected supplier path')
    if path.stat().st_nlink != 1:
        raise ValueError('hard-linked supplier source')
    return path.read_bytes()


def build(supplier, destination, *, workspace=WORKSPACE):
    workspace = Path(workspace).resolve(strict=True)
    source_root = workspace / supplier
    if Path(supplier).name != supplier or not source_root.is_dir():
        raise ValueError('one existing supplier folder name required')
    destination = Path(destination).absolute()
    if destination.exists() or not destination.resolve().is_relative_to(workspace / '.tmp'):
        raise ValueError('fresh workspace .tmp destination required')
    for item in (destination.parent, *destination.parent.parents):
        if item.exists() and (item.is_symlink() or getattr(item.stat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('redirected overlay parent')
    payload, changes, holds = {}, [], []
    for path in sorted((source_root / 'scripts').glob('*.py')):
        if path.name.startswith('CC_'):
            holds.append({'file': path.name, 'reason': 'Claude-owned filename'})
            continue
        before = regular(path)
        text = before.decode('utf-8-sig')
        if path.name == 'reset_audit.py':
            text = replace_assignment(text, 'RESET_DIRS', lambda values:
                tuple(value for value in values if value not in {'out', 'derived', 'work'})
                + ('work/derived', 'work/validation'))
            text = replace_assignment(text, 'RESET_TEXT_FILES', lambda values:
                {'work/' + key if key.startswith('manifests/') else key: value for key, value in values.items()})
        if path.name in {'make_handoff.py', 'run_validation.py'}:
            fragment = r'(handoffs/[^)]+\.md)'
            if fragment in text:
                text = replace_once(text, fragment, r'(coordination/handoffs/[^)]+\.md)')
        if path.name == 'agent_coord.py':
            fragment = 'pointer.replace("(handoffs/", "(../handoffs/")'
            if fragment in text:
                text = replace_once(text, fragment, 'pointer.replace("(coordination/handoffs/", "(handoffs/")')
        explicit = ('project',) if path.name == 'make_handoff.py' else ()
        converted, count = route_python(text, explicit)
        name = 'scripts/' + path.name
        payload[name] = converted.encode('utf-8')
        if converted.encode('utf-8') != before:
            data = converted.encode('utf-8')
            changes.append({'path': name, 'before_sha256': hashlib.sha256(before).hexdigest(),
                            'after_sha256': hashlib.sha256(data).hexdigest(), 'routed_paths': count})
    for name in ('project_layout.py', 'project_scratch.py', 'reset_operations.py'):
        target = source_root / 'scripts' / name
        if target.exists():
            holds.append({'file': str(target.relative_to(source_root)), 'reason': 'new helper destination already exists'})
            continue
        payload['scripts/' + name] = (WORKSPACE / 'audit_template/runtime_v4' / name).read_bytes()
    payload['project-layout.json'] = b'{"schema_version":1,"layout":"v4"}\n'
    if (source_root / 'project-layout.json').exists():
        holds.append({'file': 'project-layout.json', 'reason': 'existing layout configuration requires review'})
    manifest = {'schema_version': 1, 'status': 'development-overlay-not-installable',
        'source_supplier': supplier, 'changes': changes, 'holds': holds,
        'install_paths': [row['path'] for row in changes] + [
            'scripts/project_layout.py', 'scripts/project_scratch.py',
            'scripts/reset_operations.py', 'project-layout.json'],
        'remaining': ['direct-path findings', 'output defaults and stored-path users',
                      'scratch integration', 'isolated current-runtime validation and review',
                      'dirty and owned-file move dispositions'],
        'files': [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(payload.items())]}
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in payload.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
    with (destination / 'candidate-manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
    report = scan(destination)
    with (destination / 'path-sweep.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
    return {'changed_scripts': len(changes), 'routed_paths': sum(row['routed_paths'] for row in changes),
            'holds': holds, 'direct_code_findings': len(report['code_findings']),
            'snapshotted_scripts': sum(name.startswith('scripts/') for name in payload),
            'status': manifest['status']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--supplier', required=True)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.supplier, args.destination), ensure_ascii=False))


if __name__ == '__main__':
    main()
