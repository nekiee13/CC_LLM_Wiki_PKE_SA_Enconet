"""Preview or initialize one clean audit project with explicit company identity.

No sources, approvals, scores, active prompts, or database are copied/created.
Runtime scripts are local copies from the tested, pinned release.
"""
import argparse
import json
from pathlib import Path

import yaml

from bootstrap_sieving import _check_existing_chain, BootstrapError
from framework_release import spec, load_manifest, preview, apply

WORKSPACE = Path(__file__).resolve().parent.parent


def scaffold(supplier):
    if not supplier.strip() or any(ord(c) < 32 for c in supplier):
        raise ValueError('Provide an explicit non-empty supplier identity')
    state = dict(phase='setup',supplier=supplier,deliverable_language=None,benchmarks_locked=False,
        gates={f'G{i}':dict(status='pending',date=None,decision_ref=None) for i in range(1,8)})
    config = dict(supplier=supplier,framework_version='2.0.0',regulatory_editions={},
        source_selection_status='pending-owner',supplier_scope=None,part21_applicability=None,
        deliverable_language=None,reset_backup_waiver=None)
    return {
        'project-state.yml':yaml.safe_dump(state,sort_keys=False,allow_unicode=True).encode('utf-8'),
        'framework-company.json':(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode('utf-8'),
        'AGENTS.md':b'# Company audit guidance\n\nInherit workspace AGENTS.md. Read HANDOFF.md when present, project-state.yml,\ncoordination/BOARD.md when present, docs/FRAMEWORK_METHOD_V2.md and\nsieving/SIEVING_PLAYBOOK.md before audit work. No source edition, applicability,\nactive prompt, golden fixture, generation, or result is approved by copying tools.\nClaude owns CLAUDE.md and .claude; request its setup through coordination.\n',
        'wiki/index.md':b'# Audit index\n\n- [Reusable method](../docs/FRAMEWORK_METHOD_V2.md)\n- [Sieving playbook](../sieving/SIEVING_PLAYBOOK.md)\n- [Current status](current-status.md)\n',
        'wiki/current-status.md':b'# Current status\n\nFramework installed. Fresh intake and owner decisions pending. No audit results.\n',
        'wiki/log.md':b'# Audit log\n\nAppend-only. Framework setup; no source or audit approval implied.\n',
    }


def setup(target, supplier, run_id=None):
    target = Path(target).absolute()
    if '..' in target.parts or target.parent != WORKSPACE or target.name.startswith('.'):
        raise ValueError('Target must be one named company folder directly in this workspace')
    _check_existing_chain(target)
    selected = spec()
    manifest = load_manifest(selected)
    seeds = scaffold(supplier)
    if (target / 'db/nqa_audit.sqlite').exists():
        raise ValueError('This is an audit project, not a clean setup target; use an additive upgrade')
    for name,data in seeds.items():
        path = target / name
        _check_existing_chain(path)
        if path.exists() and (not path.is_file() or path.read_bytes() != data):
            raise BootstrapError('Existing project file differs; preserve it: '+name)
    plan = preview(target,selected) if target.exists() else dict(mode='preview',target=str(target),
        files=[dict(path=e['path'],sha256=e['sha256'],state='create') for e in manifest['files']])
    plan['scaffold'] = list(seeds)
    plan['supplier'] = supplier
    plan['source_selection_status'] = 'pending-owner'
    if run_id is None:
        return plan
    target.mkdir(exist_ok=True)
    result = apply(target,run_id,selected)
    for name,data in seeds.items():
        path = target / name
        path.parent.mkdir(parents=True,exist_ok=True)
        if not path.exists():
            with path.open('xb') as stream:
                stream.write(data)
        elif path.read_bytes() != data:
            raise BootstrapError('Setup changed during apply: '+name)
    return result | dict(supplier=supplier,scaffold=list(seeds),source_selection_status='pending-owner')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target',type=Path,required=True)
    p.add_argument('--supplier',required=True)
    p.add_argument('--apply',action='store_true')
    p.add_argument('--run-id')
    p.add_argument('--plan-output',type=Path,help='Save a fresh preview JSON outside the company target')
    a = p.parse_args()
    if bool(a.run_id) != a.apply:
        p.error('--apply and --run-id must be given together')
    if a.plan_output and (a.apply or a.plan_output.resolve().is_relative_to(a.target.resolve())):
        p.error('Plan output is preview-only and must be outside the target')
    try:
        result = setup(a.target,a.supplier,a.run_id)
        if a.plan_output:
            a.plan_output.parent.mkdir(parents=True,exist_ok=True)
            with a.plan_output.open('x',encoding='utf-8') as stream:
                json.dump(result,stream,ensure_ascii=False,indent=2)
            print(json.dumps(dict(supplier=a.supplier,target=result['target'],files=len(result['files']),
                scaffold=len(result['scaffold']),plan=str(a.plan_output),mode='preview')))
        else:
            print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError) as exc:
        p.exit(1,str(exc)+'\n')


if __name__ == '__main__':
    main()
