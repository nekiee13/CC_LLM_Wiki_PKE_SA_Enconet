"""Capture or verify existing company bytes before an additive framework upgrade."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def capture(project):
    root = project.resolve(strict=True)
    git_root = Path(subprocess.check_output(['git','-C',str(root),'rev-parse','--show-toplevel'],text=True).strip())
    relative = root.relative_to(git_root).as_posix()
    tracked = subprocess.check_output(['git','-C',str(git_root),'ls-files','-z','--',relative]).decode('utf-8').split('\0')
    files = {git_root / name for name in tracked if name and (git_root / name).is_file()}
    for folder in ('raw','db'):
        files.update(p for p in (root / folder).rglob('*') if p.is_file())
    return dict(project=str(root),head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),
        files={p.relative_to(root).as_posix():digest(p) for p in sorted(files)})


def verify(record):
    root = Path(record['project'])
    changed = [name for name,sha in record['files'].items() if not (root/name).is_file() or digest(root/name) != sha]
    return dict(project=str(root),verified=len(record['files']),changed=changed)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',type=Path)
    p.add_argument('--output',type=Path)
    p.add_argument('--verify',type=Path)
    args = p.parse_args()
    if args.verify:
        result = verify(json.loads(args.verify.read_text(encoding='utf-8')))
        print(json.dumps(result,indent=2))
        return bool(result['changed'])
    if not args.project or not args.output:
        p.error('Use --project and --output, or --verify')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    result = capture(args.project)
    with args.output.open('x',encoding='utf-8') as stream:
        json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps(dict(project=result['project'],files=len(result['files']),output=str(args.output))))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
