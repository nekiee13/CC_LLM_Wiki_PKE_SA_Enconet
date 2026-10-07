"""Execute a reviewed hash-pinned intake plan through local phase routing.

Each batch is validated before the next starts. No gate, prompt, applicability,
chaptering, extraction or approval is written. Preview is the default.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def run(project, plan_file, receipt, apply=False):
    root = Path(project).resolve()
    plan = json.loads(Path(plan_file).read_text(encoding='utf-8'))
    if Path(plan['project']).resolve() != root:
        raise ValueError('Plan belongs to a different project')
    output = Path(receipt).resolve()
    if output.exists() or not output.is_relative_to(root / 'out'):
        raise ValueError('Use a fresh receipt under selected project out/')
    rows = [row for batch in plan['batches'] for row in batch['documents']]
    if not rows or len({r['filename'] for r in rows}) != len(rows):
        raise ValueError('Plan must contain unique documents')
    for batch in plan['batches']:
        n = len(batch['documents'])
        if not (n == 1 if batch['size_class']=='large' else n in (2,3)):
            raise ValueError('Unsafe source batch size')
        for row in batch['documents']:
            source = root / 'incoming' / row['filename']
            if source.name != row['filename'] or source.is_symlink() or source.resolve().parent != root / 'incoming':
                raise ValueError('Unsafe source filename')
            if hashlib.sha256(source.read_bytes()).hexdigest() != row['sha256']:
                raise ValueError('Source changed since review: '+source.name)
            if (root / 'raw' / source.name).exists():
                raise ValueError('Existing raw source refused: '+source.name)
    if not apply:
        return dict(mode='preview',batches=len(plan['batches']),documents=len(rows),writes=0)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as journal:
        def record(entry):
            journal.write(json.dumps(entry,ensure_ascii=False)+'\n')
            journal.flush()
        for batch in plan['batches']:
            for row in batch['documents']:
                source = root / 'incoming' / row['filename']
                if hashlib.sha256(source.read_bytes()).hexdigest()!=row['sha256']:
                    raise ValueError('Source changed during intake')
                notes = 'batch_id='+batch['batch_id']+'; change_type=new; incoming_preserved=true; registration_not_source_approval'
                command = [sys.executable,str(root/'scripts/audit_command.py'),'audit-register','--',row['filename'],
                    '--title',row['title'],'--supplier',row['supplier'],'--doc-date',row['doc_date'],
                    '--language',row['language'],'--side',row['side'],'--notes',notes,'--preserve-incoming']
                result = subprocess.run(command,cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace',
                                        env={**os.environ,'PYTHONUTF8':'1'})
                record(dict(utc=datetime.now(timezone.utc).isoformat(),batch_id=batch['batch_id'],filename=row['filename'],
                            command=command,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
                if result.returncode:
                    raise RuntimeError('Registration failed; inspect receipt before continuing')
                if hashlib.sha256(source.read_bytes()).hexdigest()!=row['sha256']:
                    raise RuntimeError('Incoming changed during registration')
            command = [sys.executable,str(root/'scripts/validate_raw_sources.py')]
            result = subprocess.run(command,cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace',
                                    env={**os.environ,'PYTHONUTF8':'1'})
            record(dict(batch_id=batch['batch_id'],stage='validate_raw_sources',command=command,
                        exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
            if result.returncode:
                raise RuntimeError('Batch validation failed; next batch blocked')
            print(batch['batch_id']+': registered '+str(len(batch['documents']))+'; validation passed',flush=True)
    return dict(mode='apply',batches=len(plan['batches']),documents=len(rows),receipt=str(output))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--receipt',type=Path,required=True)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    try:
        print(json.dumps(run(args.project,args.plan,args.receipt,args.apply)))
    except (OSError,ValueError,RuntimeError) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__=='__main__':
    main()
