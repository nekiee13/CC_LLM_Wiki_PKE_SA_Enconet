"""Resolve retained logical file references without editing audit records."""
import json
from pathlib import Path

from project_layout import ROOT, configuration, guard, path

ALIASES = {name: name for name in ('manifests', 'derived', 'benchmarks', 'backup', 'handoffs', 'decisions')}
ALIASES.update({'out': 'validation', '.bootstrap': 'bootstrap'})


def recorded_path(value):
    requested = Path(value)
    requested = guard(requested if requested.is_absolute() else ROOT / requested)
    relative = requested.relative_to(ROOT).as_posix()
    if ':' in relative:
        raise ValueError('alternate-stream reference refused')
    if configuration() == 'legacy':
        return requested
    file = guard(ROOT / 'project-file-relocations.json')
    data = json.loads(file.read_text(encoding='utf-8'))
    if (not isinstance(data, dict) or set(data) != {'schema_version', 'paths'}
            or type(data['schema_version']) is not int or data['schema_version'] != 1
            or not isinstance(data['paths'], dict)):
        raise ValueError('invalid project-file-relocations.json')
    if relative in data['paths']:
        target = data['paths'][relative]
        if (not isinstance(target, str) or not target or Path(target).is_absolute()
                or ':' in target or '..' in Path(target).parts or '\\' in target):
            raise ValueError('unsafe recorded relocation')
        return guard(ROOT / target)
    parts = Path(relative).parts
    if parts and parts[0] in ALIASES:
        return path(ALIASES[parts[0]], *parts[1:])
    if parts[:2] == ('docs', 'reviews'):
        return path('reviews', *parts[2:])
    return requested


def recorded_path_at(root, value):
    if guard(Path(root).absolute()) != ROOT:
        raise ValueError('recorded path root differs from local supplier')
    return recorded_path(value)
