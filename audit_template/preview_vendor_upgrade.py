"""Read-only v2-to-v3 plan for an unstarted company scaffold. No apply mode."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path

from bootstrap_sieving import _check_existing_chain, load_manifest
from framework_release import spec
from prepare_vendor import scaffold

ROOT = Path(__file__).resolve().parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def match(actual, baseline):
    if actual == baseline:
        return 'exact'
    if b'\x00' not in actual + baseline and actual.replace(b'\r\n', b'\n') == baseline.replace(b'\r\n', b'\n'):
        return 'crlf-lf-equivalent'
    return None


def preview(target):
    target = Path(target).absolute()
    _check_existing_chain(target)
    if not target.is_dir():
        raise ValueError('Existing company scaffold required')
    config = json.loads((target / 'framework-company.json').read_text(encoding='utf-8'))
    supplier = config['supplier']
    old_spec, new_spec = spec(release='v2'), spec(release='v3')
    old, new = load_manifest(old_spec), load_manifest(new_spec)
    old_data = {e['path']: (old_spec.bundle / e['path']).read_bytes() for e in old['files']}
    new_data = {e['path']: (new_spec.bundle / e['path']).read_bytes() for e in new['files']}
    old_data.update(scaffold(supplier, release='v2'))
    new_data.update(scaffold(supplier, release='v3'))
    blockers, rows = [], []
    # An unstarted scaffold has no documents, evidence, database or audit output.
    # Inspect links before traversal and refuse hard links too.
    for folder, directories, files in os.walk(target, followlinks=False):
        for name in directories + files:
            path = Path(folder) / name
            _check_existing_chain(path)
            if path.is_file() and path.stat().st_nlink != 1:
                raise ValueError('Hard-linked file: ' + str(path))
        for name in files:
            path = Path(folder) / name
            rel = path.relative_to(target).as_posix()
            if rel not in old_data and not rel.startswith('.bootstrap/'):
                blockers.append('Unplanned file must be preserved/reviewed: ' + rel)
    for name, data in sorted(new_data.items()):
        path = target / name
        _check_existing_chain(path)
        if path.exists() and not path.is_file():
            raise ValueError('Expected file, found directory: ' + name)
        actual = path.read_bytes() if path.is_file() else None
        baseline = old_data.get(name)
        baseline_match = match(actual, baseline) if actual is not None and baseline is not None else None
        if actual is None:
            action = 'add'
            if baseline is not None:
                blockers.append('Missing installed v2 file: ' + name)
        elif match(actual, data):
            action = 'keep'
        elif baseline_match:
            action = 'replace'
        else:
            action = 'conflict'
            blockers.append('Local change or differing new-path file: ' + name)
        rows.append(dict(path=name, action=action, baseline_match=baseline_match,
                         before_sha256=digest(actual) if actual is not None else None,
                         v2_sha256=digest(baseline) if baseline is not None else None,
                         v3_sha256=digest(data)))
    retained = []
    for name in sorted(old_data.keys() - new_data.keys()):
        path = target / name
        _check_existing_chain(path)
        actual = path.read_bytes() if path.is_file() else None
        if actual is None or not match(actual, old_data[name]):
            blockers.append('Missing/changed retained v2 file: ' + name)
        retained.append(dict(path=name, action='retain-legacy-no-delete',
                             before_sha256=digest(actual) if actual is not None else None))
    return dict(mode='preview-only', apply_supported=False, target=str(target), supplier=supplier,
                from_version='2.0.0', to_version='3.0.0',
                manifest_hashes={v: digest((s.bundle / 'manifest.json').read_bytes())
                                 for v, s in [('v2', old_spec), ('v3', new_spec)]},
                counts=dict(Counter(row['action'] for row in rows)), files=rows,
                retained=retained, blockers=blockers,
                approval='not-authorized-to-apply',
                hash_representation='SHA-256 of exact file bytes; CRLF/LF equivalence separately labelled')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--targets', nargs='+', required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    targets = [ROOT / name for name in args.targets]
    if any(t.parent != ROOT or t.name.startswith('.') for t in targets):
        p.error('Each target must be a direct company folder in the workspace')
    output = args.output.absolute()
    _check_existing_chain(output)
    if any(output.is_relative_to(t) for t in targets):
        p.error('Output must be outside every company target')
    plans = [preview(t) for t in targets]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(plans, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    for plan in plans:
        print(json.dumps({k: plan[k] for k in ('supplier', 'counts', 'blockers')}, ensure_ascii=True))
    return int(any(plan['blockers'] for plan in plans))


if __name__ == '__main__':
    raise SystemExit(main())
