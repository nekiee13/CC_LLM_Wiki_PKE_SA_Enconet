"""Build a fresh development-only v4 tree from the hash-pinned v3 payload.

This is not a release installer or a migration tool. It never overwrites a
destination, and refuses live workspace locations. Remaining string/config
paths, report publication, reset and handoff integration still need review.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
BASELINE = ROOT / 'framework/v3'
PIN = '16f4015b64cc228d7a9e0537a0ae417dcb7f52c6153f17ba3746a979b698cf1c'
RUNTIME = ROOT / 'runtime_v4'
MOVED = {key: 'work/' + key for key in ('benchmarks', 'derived', 'manifests', 'decisions', 'backup')}
MOVED.update({'handoffs': 'coordination/handoffs', 'out': 'work/validation', '.bootstrap': 'work/bootstrap'})
KEYS = {**{key: key for key in MOVED}, 'out': 'validation', '.bootstrap': 'bootstrap'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_payload(manifest, source):
    """Verify every byte before creating a destination; refuse unsafe paths."""
    files = {}
    for row in manifest['files']:
        name = row['path']
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
            raise ValueError('unsafe baseline path')
        path = source / name
        if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()):
            raise ValueError('redirected baseline path')
        data = path.read_bytes()
        if sha(data) != row['sha256'] or len(data) != row['bytes']:
            raise ValueError('baseline checksum mismatch: ' + name)
        if name.casefold() in {key.casefold() for key in files}:
            raise ValueError('duplicate baseline path')
        files[name] = data
    return files


def route_python(source):
    """Change only recognized local-root path expressions, preserving comments.

    AST positions are byte offsets, so editing uses UTF-8 bytes. Do not rewrite
    arbitrary strings: a reference in a quote is evidence, not a filesystem path.
    Parameter roots and roots derived in other ways remain explicit integration
    work rather than being guessed here.
    """
    tree = ast.parse(source)
    roots = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            expression = ast.unparse(node.value).replace(' ', '')
            if expression in {"Path(__file__).resolve().parents[1]", "Path(__file__).resolve().parent.parent"}:
                roots.update(t.id for t in node.targets if isinstance(t, ast.Name))
    raw = source.encode('utf-8')
    lines = raw.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits = []
    # A local binding can shadow a module root. Keep that whole scope untouched.
    shadowed = set()
    for scope in ast.walk(tree):
        if not isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        bindings = {node.id for node in ast.walk(scope)
                    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)}
        if hasattr(scope, 'args'):
            bindings.update(arg.arg for arg in ast.walk(scope.args) if isinstance(arg, ast.arg))
        if roots & bindings:
            shadowed.update(id(node) for node in ast.walk(scope))
    for node in ast.walk(tree):
        if id(node) in shadowed:
            continue
        if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
                and isinstance(node.left, ast.Name) and node.left.id in roots
                and isinstance(node.right, ast.Constant) and isinstance(node.right.value, str)):
            continue
        parts = PurePosixPath(node.right.value).parts
        if not parts or parts[0] not in KEYS:
            continue
        expression = 'layout_path(' + repr(KEYS[parts[0]]) + ')'
        for part in parts[1:]:
            expression += ' / ' + repr(part)
        edits.append((offsets[node.lineno - 1] + node.col_offset,
                      offsets[node.end_lineno - 1] + node.end_col_offset, expression.encode('utf-8')))
    for start, end, replacement in sorted(edits, reverse=True):
        raw = raw[:start] + replacement + raw[end:]
    if edits:
        # After docstring and future imports, before imports that can load defaults.
        insertion = 0
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                insertion = offsets[node.end_lineno]
            elif isinstance(node, ast.ImportFrom) and node.module == '__future__':
                insertion = offsets[node.end_lineno]
            else:
                break
        raw = raw[:insertion] + b'from project_layout import path as layout_path\n' + raw[insertion:]
    result = raw.decode('utf-8')
    ast.parse(result)
    return result, len(edits)


def build(destination):
    destination = Path(destination).absolute()
    if destination.exists():
        raise FileExistsError('candidate destination must be fresh')
    if destination.resolve().is_relative_to(WORKSPACE) and not destination.resolve().is_relative_to(WORKSPACE / '.tmp'):
        raise ValueError('workspace candidates must be under .tmp, never in live suppliers or releases')
    for parent in destination.parents:
        if parent.is_symlink() or (parent.exists() and getattr(parent.stat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('redirected candidate parent')
    manifest_bytes = (BASELINE / 'manifest.json').read_bytes()
    if sha(manifest_bytes) != PIN:
        raise ValueError('baseline manifest checksum mismatch')
    files = verify_payload(json.loads(manifest_bytes), BASELINE)
    payload, routes = {}, {}
    for name, data in files.items():
        parts = PurePosixPath(name).parts
        target = '/'.join((MOVED.get(parts[0], parts[0]), *parts[1:]))
        if name.startswith('scripts/') and name.endswith('.py'):
            converted, count = route_python(data.decode('utf-8'))
            if count:
                data = converted.encode('utf-8')
                routes[name] = count
        if target.casefold() in {key.casefold() for key in payload}:
            raise ValueError('candidate destination collision')
        payload[target] = data
    payload['scripts/project_layout.py'] = (RUNTIME / 'project_layout.py').read_bytes()
    payload['project-layout.json'] = (RUNTIME / 'project-layout.example.json').read_bytes()
    record = {'schema_version': 1, 'status': 'development-only-not-installable',
              'baseline_manifest_sha256': PIN, 'routed_expressions': routes,
              'remaining': ['config/string paths', 'full sieving/audit/report pipeline',
                            'reset/handoff', 'run-root output policy', 'Git/history orchestration'],
              'files': [{'path': name, 'sha256': sha(data), 'bytes': len(data)}
                        for name, data in sorted(payload.items())]}
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in payload.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
    with (destination / 'candidate-manifest.json').open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    record = build(args.destination)
    print(json.dumps({'status': record['status'], 'files': len(record['files']),
                      'routed_scripts': len(record['routed_expressions'])}))


if __name__ == '__main__':
    main()
