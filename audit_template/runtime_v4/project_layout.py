"""Candidate v4 local layout contract. Copy into <supplier>/scripts before use.

This helper does not install, migrate, create directories or approve an audit.
Both legacy and v4 modes require explicit project-local configuration.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import stat
import sys

ROOT=Path(__file__).resolve().parents[1]
COMMON={'incoming':'incoming','raw':'raw','db':'db','database':'db/nqa_audit.sqlite',
        'scripts':'scripts','schemas':'schemas','sieving':'sieving','wiki':'wiki',
        'outputs':'outputs','docs':'docs','temp':'.tmp'}
LEGACY={**COMMON,**{name:name for name in ('benchmarks','derived','manifests','decisions','backup','handoffs')},
        'plans':'docs','reviews':'docs/reviews','validation':'out','migrations':'work/migrations','bootstrap':'.bootstrap'}
V4={**COMMON,**{name:'work/'+name for name in ('benchmarks','derived','manifests','decisions','backup')},
    'plans':'docs/plans','reviews':'work/reviews','handoffs':'coordination/handoffs',
    'validation':'work/validation','migrations':'work/migrations','bootstrap':'work/bootstrap'}


def guard(value):
    path=Path(value).absolute()
    if not path.is_relative_to(ROOT):
        raise ValueError('foreign project path')
    for candidate in (path,*path.parents):
        if not candidate.is_relative_to(ROOT):
            break
        try:
            info=candidate.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)&0x400:
            raise ValueError('redirected project path')
        if stat.S_ISREG(info.st_mode) and info.st_nlink>1:
            raise ValueError('hard-linked project path')
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError('foreign resolved project path')
    return path


def configuration():
    config=guard(ROOT/'project-layout.json')
    if not config.is_file():
        raise ValueError('explicit project-layout.json configuration required')
    data=json.loads(config.read_text(encoding='utf-8'))
    if not isinstance(data,dict) or set(data)!={'schema_version','layout'} or type(data['schema_version']) is not int or data['schema_version']!=1 or not isinstance(data['layout'],str) or data['layout'] not in {'legacy','v4'}:
        raise ValueError('unsupported layout configuration')
    return data['layout']


def path(key,*tail):
    mode=configuration()
    if key not in V4:
        raise ValueError('unknown layout key')
    old,new=guard(ROOT/LEGACY[key]),guard(ROOT/V4[key])
    if key!='plans' and old!=new and old.exists() and new.exists():
        raise ValueError('mixed legacy/v4 locations')
    if key!='plans' and mode=='v4' and old!=new and old.exists():
        raise ValueError('legacy location remains under v4 configuration')
    if key!='plans' and mode=='legacy' and old!=new and new.exists() and not old.exists():
        raise ValueError('v4 location remains under legacy configuration')
    chosen=new if mode=='v4' else old
    for part in tail:
        item=Path(part)
        if not str(part) or item.is_absolute() or ':' in str(part) or any(p=='..' for p in item.parts):
            raise ValueError('unsafe path tail')
        chosen=chosen/item
    return guard(chosen)


def run_output(run_id):
    if not re.fullmatch(r'RUN-\d{8}-\d+',run_id):
        raise ValueError('invalid run ID')
    return path('outputs',run_id)


def describe():
    return {key:str(path(key)) for key in sorted(V4)}


def main():
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--describe',action='store_true',required=True)
    parser.parse_args()
    print(json.dumps(describe(),ensure_ascii=False))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
