"""One release command for a clean vendor, or an additive Enconet upgrade.

Preview never writes. Apply is exclusive-create with a run journal; conflicts
fail before any copy. No source intake, reset, approval or evaluation is run.
"""
from pathlib import Path
import argparse
import json
from bootstrap_sieving import (BundleSpec, BootstrapError, apply, preview, load_manifest)

ROOT = Path(__file__).resolve().parent
VERSION = '2.0.0'


def spec(upgrade=False, *, release='v2'):
    if release not in {'v2','v3'}:
        raise ValueError('Choose v2 or v3')
    if upgrade and release == 'v3':
        raise ValueError('v3 is a clean release; do not overlay an existing audit')
    bundle = ROOT / 'framework' / ('upgrade-v2' if upgrade else release)
    manifest = json.loads((bundle / 'manifest.json').read_text(encoding='utf-8'))
    paths = frozenset(e['path'] for e in manifest['files'])
    return BundleSpec(bundle, '3.0.0' if release == 'v3' else VERSION,
        'framework-upgrade' if upgrade else 'clean-audit-framework',
        frozenset(p.split('/')[0] for p in paths), 'framework-'+release, '.framework-bootstrap.lock', paths)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target',type=Path,required=True)
    p.add_argument('--upgrade',action='store_true',help='Only additive current-method tools; keep existing framework')
    p.add_argument('--release',choices=['v2','v3'],default='v3')
    p.add_argument('--apply',action='store_true')
    p.add_argument('--run-id')
    args = p.parse_args()
    if bool(args.run_id) != args.apply:
        p.error('--apply and --run-id must be given together')
    try:
        selected = spec(args.upgrade,release=args.release)
        result = apply(args.target,args.run_id,selected) if args.apply else preview(args.target,selected)
    except (BootstrapError,OSError,ValueError) as exc:
        p.exit(1,str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
