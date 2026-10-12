"""Explicit workspace documentation home for engineering tools.

This is workspace tooling, not supplier runtime. Read configuration without
creating folders or guessing a home from which files happen to exist.
"""
import json
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[1]


def checked(root, path):
    root, path = Path(root).absolute(), Path(path).absolute()
    if not path.is_relative_to(root):
        raise ValueError('documentation path outside workspace')
    for entry in (path, *path.parents):
        if not entry.is_relative_to(root):
            break
        try:
            info = entry.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('redirected documentation path')
        if stat.S_ISREG(info.st_mode) and info.st_nlink > 1:
            raise ValueError('hard-linked documentation file')
    return path


def documentation(*tail, root=ROOT):
    root = Path(root).absolute()
    config = json.loads(checked(root, root / 'workspace-layout.json').read_text(encoding='utf-8'))
    if (not isinstance(config, dict) or set(config) != {'schema_version', 'documentation_root'}
            or type(config['schema_version']) is not int or config['schema_version'] != 1
            or config['documentation_root'] not in {'doc', 'PKE_SA_NQA1_doc'}):
        raise ValueError('unsupported workspace-layout.json')
    result = root / config['documentation_root']
    for value in tail:
        part = Path(value)
        if not str(value) or part.is_absolute() or ':' in str(value) or '..' in part.parts:
            raise ValueError('unsafe documentation suffix')
        result /= part
    return checked(root, result)
