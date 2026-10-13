"""Copy a reviewed incoming source to exclusive raw storage and register it.

Keeps incoming intact for recall sweeps. The command does not approve an edition,
advance a gate, or change an existing raw source. Preview is the default.
"""
import argparse
from pathlib import Path
import sys

import db_util
from project_paths import local_path, configure_standard_streams
from source_registry import ROOT, RAW, register, write_lock


def promote(filename, *, apply=False, **metadata):
    source = local_path(ROOT / 'incoming' / filename)
    if source.parent != (ROOT / 'incoming').resolve() or not source.is_file() or source.name == '.gitkeep':
        raise ValueError('Use one regular file directly under local incoming')
    destination = local_path(RAW / source.name)
    if destination.exists():
        raise FileExistsError('Registered raw files are never overwritten')
    data = source.read_bytes()
    if not apply:
        return 'preview: copy ' + source.name + '; explicit --apply required'
    # Fail before copying if the local registry or database is missing.
    from source_registry import read_manifest
    read_manifest()
    if not local_path(metadata['db_path']).is_file():
        raise FileNotFoundError('Initialize the local database first')
    RAW.mkdir(parents=True,exist_ok=True)
    with destination.open('xb') as stream:
        stream.write(data)
    try:
        write_lock(destination)
        return register(destination,**metadata)
    except Exception:
        # Preserve the new file for diagnosis. No registered source is removed.
        raise RuntimeError('Intake failed; retain the new raw file and inspect registry/DB before retry')


def main():
    configure_standard_streams()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('filename')
    p.add_argument('--apply',action='store_true')
    p.add_argument('--db',type=Path,default=db_util.DEFAULT_DB)
    p.add_argument('--title',required=True)
    p.add_argument('--supplier',required=True)
    p.add_argument('--language',choices=['sl','en','hr'],required=True)
    p.add_argument('--side',choices=['RULE','DOCUMENT'],required=True)
    p.add_argument('--doc-date',default='n-a')
    p.add_argument('--source-url',default='n-a')
    p.add_argument('--notes',default='')
    a = p.parse_args()
    try:
        print(promote(a.filename,apply=a.apply,db_path=a.db,title=a.title,supplier=a.supplier,
            language=a.language,side_hint=a.side,doc_date=a.doc_date,source_url=a.source_url,notes=a.notes))
        return 0
    except (OSError,ValueError,RuntimeError) as exc:
        print(str(exc),file=sys.stderr)
        return 1


if __name__ == '__main__':
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
