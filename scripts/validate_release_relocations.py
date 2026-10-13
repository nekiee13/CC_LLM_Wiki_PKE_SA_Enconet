"""Read-only verification of frozen release manifests using external relocations.

Original/planned modes read original files; relocated mode reads mapped retained
files. Manifest bytes are never rewritten. No approval or audit result changes.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import shutil

import cleanup_migration as migration


def logical(value):
    if (not isinstance(value, str) or not value or PurePosixPath(value).is_absolute()
            or '\\' in value or ':' in value or '..' in PurePosixPath(value).parts):
        raise ValueError('unsafe manifest-relative path')
    return PurePosixPath(value)


def verify(root, supplier, manifest_name, plan, mode='planned'):
    root = migration.root_path(root)
    if len(logical(supplier).parts) != 1 or supplier == '.':
        raise ValueError('one supplier required')
    if mode not in {'original', 'planned', 'relocated'}:
        raise ValueError('unsupported verification mode')
    if plan.get('schema') != 'cleanup-file-map-1' or not isinstance(plan.get('files'), list):
        raise ValueError('unsupported relocation file map')
    prefix = supplier + '/'
    mapped = {}
    for row in plan['files']:
        if not row['source'].startswith(prefix) or not row['destination'].startswith(prefix):
            raise ValueError('foreign supplier relocation')
        migration.safe(root, row['source'])
        migration.safe(root, row['destination'])
        if row['source'] in mapped:
            raise ValueError('duplicate relocation source')
        mapped[row['source']] = row
    old_manifest = prefix + str(logical(manifest_name))
    manifest_row = mapped.get(old_manifest)
    actual_manifest = manifest_row['destination'] if mode == 'relocated' and manifest_row else old_manifest
    manifest_file = migration.safe(root, actual_manifest)
    raw_hash = migration.digest(manifest_file)
    if mode != 'original' and manifest_row and raw_hash != manifest_row['sha256']:
        return {'passed': False, 'verified': 0, 'failures': [{'source': old_manifest, 'reason': 'manifest hash changed'}]}
    data = json.loads(manifest_file.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or ('files' in data and 'artifacts' in data):
        raise ValueError('ambiguous or invalid release manifest')
    publication = 'artifacts' in data
    members = data.get('artifacts' if publication else 'files')
    if not isinstance(members, list) or not members:
        raise ValueError('nonempty release manifest required')
    if publication and (type(data.get('schema_version')) is not int
            or data['schema_version'] != 1 or not isinstance(data.get('run_id'), str)
            or not re.fullmatch(r'RUN-\d{8}-\d+', data['run_id'])):
        raise ValueError('unsupported publication manifest version or run ID')
    records, seen = [], set()
    for item in members:
        if not isinstance(item, dict):
            raise ValueError('invalid manifest member')
        if publication:
            if set(item) != {'source', 'destination', 'sha256'}:
                raise ValueError('invalid publication manifest artifact fields')
            logical(item['source'])
        member = logical(item['destination' if publication else 'path'])
        base = PurePosixPath(supplier) if publication else PurePosixPath(old_manifest).parent
        old = str(base / member)
        if old.casefold() in seen:
            raise ValueError('duplicate manifest member')
        seen.add(old.casefold())
        if (not isinstance(item.get('sha256'), str) or not re.fullmatch('[0-9a-f]{64}', item['sha256'])
                or not publication and (type(item.get('bytes')) is not int or item['bytes'] < 0)):
            raise ValueError('invalid member hash or byte count')
        row = mapped.get(old)
        target = row['destination'] if mode == 'relocated' and row else old
        path = migration.safe(root, target)
        reason = None
        if mode != 'original' and row and row['sha256'] != item['sha256']:
            reason = 'manifest/member relocation hash differs'
        elif not path.is_file():
            reason = 'member missing'
        elif (not publication and path.stat().st_size != item['bytes']
              or migration.digest(path) != item['sha256']):
            reason = 'member bytes or hash changed'
        records.append({'source': old, 'resolved': target, 'passed': reason is None, 'reason': reason})
    if migration.digest(manifest_file) != raw_hash:
        raise ValueError('manifest changed during read-only verification')
    return {'schema': 'release-relocation-verification-1', 'mode': mode, 'supplier': supplier,
            'manifest': old_manifest, 'resolved_manifest': actual_manifest,
            'manifest_sha256': raw_hash, 'plan_sha256': migration.plan_hash(plan),
            'passed': all(item['passed'] for item in records),
            'verified': sum(item['passed'] for item in records),
            'failures': [item for item in records if not item['passed']], 'files': records}


def rehearse(root, supplier, manifest_name, plan, destination):
    """Verify copied release bytes at proposed homes, without moving live files."""
    root = migration.root_path(root)
    destination = Path(destination).absolute()
    name = destination.relative_to(root).as_posix()
    migration.safe(root, name)
    if not name.startswith('.tmp/') or destination.exists():
        raise ValueError('fresh workspace scratch rehearsal required')
    before = verify(root, supplier, manifest_name, plan, 'planned')
    if not before['passed']:
        raise ValueError('original release verification failed')
    mapped = {row['source']: row['destination'] for row in plan['files']}
    selected = {item['source']: item['source'] for item in before['files']}
    selected[before['manifest']] = before['resolved_manifest']
    destinations = set()
    for old in selected:
        target = mapped.get(old, old)
        if target.casefold() in destinations:
            raise ValueError('rehearsal destination collision')
        destinations.add(target.casefold())
    destination.mkdir(parents=True, exist_ok=False)
    observed = {}
    for old, actual in selected.items():
        source = migration.safe(root, actual)
        target = migration.safe(destination, mapped.get(old, old))
        observed[actual] = migration.digest(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    after = verify(destination, supplier, manifest_name, plan, 'relocated')
    if any(migration.digest(migration.safe(root, name)) != digest for name, digest in observed.items()):
        raise ValueError('original release changed during rehearsal')
    return {**after, 'mode': 'isolated-relocation-rehearsal',
            'live_files_unchanged': True, 'copied_files': len(observed)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--supplier', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--mode', choices=['original', 'planned', 'relocated'], default='planned')
    parser.add_argument('--receipt', type=Path)
    parser.add_argument('--rehearsal', type=Path, help='fresh workspace .tmp copy; no live moves')
    args = parser.parse_args()
    if args.rehearsal and args.mode != 'planned':
        parser.error('rehearsal requires planned mode')
    result = (rehearse(args.root, args.supplier, args.manifest, migration.load(args.plan), args.rehearsal)
              if args.rehearsal else verify(args.root, args.supplier, args.manifest, migration.load(args.plan), args.mode))
    if args.receipt:
        target = migration.safe(migration.root_path(args.root), args.receipt.absolute().relative_to(args.root.absolute()).as_posix())
        if not target.relative_to(args.root.absolute()).as_posix().startswith('PKE_SA_NQA1_doc/plans/cleanup-cu3/'):
            parser.error('receipt must be a fresh cleanup review artifact')
        with target.open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: value for key, value in result.items() if key != 'files'}))
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
