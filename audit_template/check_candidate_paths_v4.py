"""Read-only static path sweep of a byte-verified development candidate.

Runtime tests are still required. This detects direct legacy path literals,
not every possible dynamically assembled path or arbitrary documentation link.
Only project_layout.py has an explicit legacy-compatibility exemption.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath

import yaml

PREFIXES = ('manifests/', 'derived/', 'benchmarks/', 'handoffs/', 'out/',
            'decisions/', 'backup/', '.bootstrap/', 'outputs/candidates/')
NAMES = {item.rstrip('/') for item in PREFIXES}


def scan(candidate):
    candidate = Path(candidate).resolve(strict=True)
    manifest_bytes = (candidate / 'candidate-manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    findings, config, labels = [], [], []
    code_files = 0
    for row in manifest['files']:
        name = row['path']
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name:
            raise ValueError('unsafe candidate manifest path')
        path = candidate / name
        if not path.resolve().is_relative_to(candidate) or path.is_symlink():
            raise ValueError('redirected candidate payload')
        data = path.read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('candidate payload checksum mismatch: ' + name)
        if path.suffix == '.py':
            code_files += 1
            tree = ast.parse(data.decode('utf-8'))
            if name == 'scripts/project_layout.py':
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.startswith(PREFIXES):
                    findings.append({'file': name, 'line': node.lineno, 'value': node.value})
                elif (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
                      and isinstance(node.right, ast.Constant) and node.right.value in NAMES):
                    findings.append({'file': name, 'line': node.lineno, 'value': node.right.value})
        elif path.suffix in {'.json', '.yml', '.yaml'}:
            payload = yaml.safe_load(data.decode('utf-8'))
            def walk(value, keys=()):
                if isinstance(value, dict):
                    for key, item in value.items():
                        walk(item, (*keys, str(key)))
                elif isinstance(value, list):
                    for number, item in enumerate(value):
                        walk(item, (*keys, str(number)))
                elif isinstance(value, str) and value.startswith(PREFIXES):
                    record = {'file': name, 'field': '.'.join(keys), 'value': value}
                    if name == 'schemas/audit_commands.yml' and 'outputs' in keys:
                        labels.append(record)  # Human descriptions, not runtime options.
                    else:
                        config.append(record)
            walk(payload)
    return {'schema': 'candidate-path-sweep-1', 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
            'verified_files': len(manifest['files']), 'parsed_python_files': code_files,
            'code_findings': findings, 'configuration_findings': config,
            'legacy_descriptive_labels': labels,
            'scope': 'Direct path literals and serialized values; not proof of all dynamic paths',
            'passed': not findings and not config}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    result = scan(args.candidate)
    print(json.dumps(result, ensure_ascii=True))
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
