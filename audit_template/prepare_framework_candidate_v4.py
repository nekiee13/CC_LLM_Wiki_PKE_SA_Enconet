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


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('pinned contract fragment differs: ' + old[:70])
    return source.replace(old, new, 1)


def replace_assignment(source, name, transform):
    """Edit one named literal contract, not arbitrary matching text."""
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    if len(matches) != 1:
        raise ValueError('expected one literal assignment: ' + name)
    node = matches[0].value
    replacement = repr(transform(ast.literal_eval(node)))
    raw = source.encode('utf-8')
    lines = raw.splitlines(keepends=True)
    start = sum(map(len, lines[:node.lineno - 1])) + node.col_offset
    end = sum(map(len, lines[:node.end_lineno - 1])) + node.end_col_offset
    return (raw[:start] + replacement.encode('utf-8') + raw[end:]).decode('utf-8')


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


def route_python(source, explicit_roots=()):
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
    used_explicit = False
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
                and isinstance(node.left, ast.Name) and node.left.id in roots | set(explicit_roots)
                and isinstance(node.right, ast.Constant) and isinstance(node.right.value, str)):
            continue
        parts = PurePosixPath(node.right.value).parts
        if not parts or parts[0] not in KEYS:
            continue
        if node.left.id in explicit_roots:
            expression = 'layout_path_at(' + node.left.id + ', ' + repr(KEYS[parts[0]]) + ')'
            used_explicit = True
        else:
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
        imports = b'from project_layout import path as layout_path\n'
        if used_explicit:
            imports += b'from project_layout import path_at as layout_path_at\n'
        raw = raw[:insertion] + imports + raw[insertion:]
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
            source = data.decode('utf-8')
            if name == 'scripts/reset_audit.py':
                # work now contains framework code and immutable review/decision
                # receipts. Never recursively reset the entire work directory.
                source = replace_assignment(source, 'RESET_DIRS', lambda values:
                    tuple(value for value in values if value not in {'out', 'derived', 'work'})
                    + ('work/derived', 'work/validation'))
                source = replace_assignment(source, 'RESET_TEXT_FILES', lambda values:
                    {'work/' + key: value for key, value in values.items()})
                original = 'incoming = root / "incoming"'
                # The first is the root guard, the second reads its snapshot.
                if source.count(original) != 2:
                    raise ValueError('reset local-root baseline differs')
                source = source.replace(original, 'incoming = layout_path_at(root, "incoming")', 1)
                source = source.replace('from project_paths import configure_standard_streams',
                    'from project_layout import path_at as layout_path_at\nfrom reset_operations import remove_generated\nfrom project_paths import configure_standard_streams', 1)
                if source.count('path.unlink()') != 1:
                    raise ValueError('reset removal baseline differs')
                source = source.replace('path.unlink()', 'remove_generated(path)', 1)
            if name == 'scripts/make_handoff.py':
                old = r'(handoffs/[^)]+\.md)'
                if source.count(old) != 1:
                    raise ValueError('handoff pointer parser baseline differs')
                source = source.replace(old, r'(coordination/handoffs/[^)]+\.md)')
            if name == 'scripts/agent_coord.py':
                old = 'pointer.replace("(handoffs/", "(../handoffs/")'
                if source.count(old) != 1:
                    raise ValueError('coordination pointer baseline differs')
                source = source.replace(old, 'pointer.replace("(coordination/handoffs/", "(handoffs/")')
            if name == 'scripts/run_validation.py':
                source = replace_once(source, r'(handoffs/[^)]+\.md)',
                    r'(coordination/handoffs/[^)]+\.md)')
                source = replace_once(source, 'import argparse',
                    'from project_scratch import temporary_directory\nimport argparse')
                source = replace_once(source, '    try:\n        proc = subprocess.run(',
                    '    try:\n        with temporary_directory(prefix="validation-") as scratch:\n            env.update({key: scratch for key in ("TMP", "TEMP", "TMPDIR")})\n            command = list(step.command)\n            if command[1:3] == ["-m", "pytest"]:\n                command.extend(["--basetemp", str(Path(scratch) / "pytest")])\n            proc = subprocess.run(')
                source = replace_once(source, '            step.command, cwd=step.cwd, capture_output=True, text=True,\n            encoding="utf-8", errors="replace", timeout=STEP_TIMEOUT_S, env=env,\n        )',
                    '                command, cwd=step.cwd, capture_output=True, text=True,\n                encoding="utf-8", errors="replace", timeout=STEP_TIMEOUT_S, env=env,\n            )')
            if name == 'scripts/browser_harness.py':
                source = replace_once(source, 'import argparse',
                    'from project_scratch import browser_environment\nimport argparse')
                source = replace_once(source, 'with sync_playwright() as playwright:',
                    'with browser_environment(), sync_playwright() as playwright:')
            if name == 'scripts/publish_audit_release.py':
                source = replace_once(source, 'import tempfile',
                    'from project_scratch import temporary_directory')
                source = replace_once(source, 'tempfile.TemporaryDirectory(prefix="release-stage-", dir=root)',
                    'temporary_directory(prefix="release-stage-", root=root)')
                source = replace_once(source, 'tempfile.TemporaryDirectory(prefix="release-check-", dir=root)',
                    'temporary_directory(prefix="release-check-", root=root)')
                source = replace_once(source, 'def checked_plan(contract, root):',
                    'def checked_plan(contract, root, *, allow_existing_snapshot=False):')
                source = replace_once(source, 'if destination in destinations or destination.exists():',
                    'if destination in destinations or (destination.exists() and not (allow_existing_snapshot and source == destination)):')
                source = replace_once(source, 'rows, result_path = checked_plan(contract, root)',
                    'if isinstance(contract.get("artifacts"), list) and contract["artifacts"] and all(isinstance(row, dict) and row.get("source") == row.get("destination") for row in contract["artifacts"]):\n        from publication_snapshot import seal\n        return seal(contract_path, root=root, execute=execute, validator=validator, permissions=permissions)\n    rows, result_path = checked_plan(contract, root)')
                source = replace_once(source, 'path = (root / value).resolve()',
                    'path = layout_guard(Path(root) / value).resolve()')
                source = replace_once(source, 'import audit_state',
                    'from project_layout import guard as layout_guard\nimport audit_state')
                source = replace_once(source,
                    'if not (destination.is_relative_to(root / "outputs") or\n                destination.is_relative_to(root / "wiki/dashboards")):',
                    'if destination.parent != layout_path_at(root, "outputs") / run:')
                source = replace_once(source, 'def validate_live(root, *, allow_pending_claude=False):',
                    'def validate_live(root, *, run_id, allow_pending_claude=False):')
                for suffix, filename in [('evaluation_package.json', 'evaluation_package.json'),
                                         ('evaluation_report.md', 'report.md'),
                                         ('dashboard.html', 'dashboard_light.html')]:
                    source = replace_once(source, 'root / f"outputs/{supplier}_appendix_b_' + suffix + '"',
                        'layout_path_at(root, "outputs") / run_id / "' + filename + '"')
                source = replace_once(source, '"--state", str(projected), "--benchmarks", "--no-record"',
                    '"--state", str(projected), "--run-id", run_id, "--benchmarks", "--no-record"')
                source = replace_once(source, 'validate_live(ROOT, allow_pending_claude=args.allow_pending_claude)',
                    'validate_live(ROOT, run_id=json.loads(args.contract.read_text(encoding="utf-8"))["run_id"], allow_pending_claude=args.allow_pending_claude)')
            if name in {'scripts/generate_review_catalog.py', 'scripts/generate_review_workspace.py',
                        'scripts/build_review_package.py'}:
                source = replace_once(source, 'import argparse',
                    'from project_layout import path as layout_path\nimport argparse')
                source = replace_once(source,
                    'PROJECT / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"',
                    'layout_path("reviews", "review_catalog.json")')
                if name == 'scripts/build_review_package.py':
                    source = replace_once(source,
                        'PROJECT / "outputs" / "candidates" / "evidence_access" / "portable_package"',
                        'layout_path("reviews", "portable_package")')
            if name == 'scripts/run_all_validations.py':
                source = replace_once(source,
                    'package = outputs / f"{supplier}_appendix_b_evaluation_package.json"',
                    'run_root = outputs / run_id if run_id else outputs\n    package = run_root / "evaluation_package.json"')
                for stem, filename in [('evaluation_report.md', 'report.md'),
                                       ('dashboard_data.json', 'dashboard_data.json'),
                                       ('dashboard.html', 'dashboard_light.html')]:
                    source = replace_once(source, 'outputs / f"{supplier}_appendix_b_' + stem + '"',
                        'run_root / "' + filename + '"')
                source = replace_once(source, 'evidence_root = outputs / "candidates" / "evidence_access"',
                    'evidence_root = layout_path("reviews")')
                source = replace_once(source, 'evidence_run = evidence_root / run_id if run_id else None',
                    'evidence_run = run_root if run_id else None')
                source = replace_once(source, 'evidence_run / f"{supplier}_appendix_b_evaluation_report.md"',
                    'evidence_run / "report.md"')
                source = replace_once(source, 'evidence_run / f"{supplier}_appendix_b_dashboard.html"',
                    'evidence_run / "dashboard_light.html"')
                source = replace_once(source, 'evidence_root / "validation_artifacts" / "browser_evidence"',
                    'layout_path("validation", run_id or "setup", "browser_evidence")')
            explicit = {'scripts/full_keyword_sweep.py': ('root',),
                        'scripts/make_handoff.py': ('project',),
                        'scripts/publish_audit_release.py': ('root',)}.get(name, ())
            converted, count = route_python(source, explicit)
            if converted != data.decode('utf-8'):
                data = converted.encode('utf-8')
            if count:
                routes[name] = count
        if name == 'benchmarks/validate_benchmarks.py':
            source = data.decode('utf-8')
            old = 'ROOT = Path(__file__).resolve().parents[1]'
            if source.count(old) != 1:
                raise ValueError('benchmark root baseline differs')
            data = source.replace(old, 'ROOT = Path(__file__).resolve().parents[2]').encode('utf-8')
        if target.casefold() in {key.casefold() for key in payload}:
            raise ValueError('candidate destination collision')
        payload[target] = data
    commands = payload['schemas/audit_commands.yml'].decode('utf-8')
    for old, new in [('manifests/raw_sources.csv row', 'work/manifests/raw_sources.csv row'),
                     ('derived/chunks artifact', 'work/derived/chunks artifact'),
                     ('manifests/validation_runs.csv unless --no-record',
                      'work/manifests/validation_runs.csv unless --no-record')]:
        commands = replace_once(commands, old, new)
    payload['schemas/audit_commands.yml'] = commands.encode('utf-8')
    payload['scripts/project_layout.py'] = (RUNTIME / 'project_layout.py').read_bytes()
    payload['scripts/evidence_access_policy.py'] = (RUNTIME / 'evidence_access_policy.py').read_bytes()
    payload['scripts/reset_operations.py'] = (RUNTIME / 'reset_operations.py').read_bytes()
    payload['scripts/publication_snapshot.py'] = (RUNTIME / 'publication_snapshot.py').read_bytes()
    payload['scripts/project_scratch.py'] = (RUNTIME / 'project_scratch.py').read_bytes()
    payload['project-layout.json'] = (RUNTIME / 'project-layout.example.json').read_bytes()
    record = {'schema_version': 1, 'status': 'development-only-not-installable',
              'baseline_manifest_sha256': PIN, 'routed_expressions': routes,
              'contract_adaptations': ['reset: working data only, local root guard, manifest headers and read-only targets',
                                      'handoff: coordination/handoffs and pointer parser',
                                      'coordination: board-relative handoff pointer',
                                      'benchmark: parent depth after relocation',
                                      'evidence policy: direct run-root candidate outputs',
                                      'publication: run-root copy or seal, unchanged artifacts, marker last',
                                      'aggregate: direct run artifacts and internal review packages',
                                      'catalog/package: internal work/reviews defaults',
                                      'scratch: local publication, browser and layered pytest folders',
                                      'layered validation: current handoff pointer',
                                      'dispatcher: current output labels'],
              'remaining': ['final acceptance review including latest scratch adaptations',
                            'current guidance and exact live-batch review before installation'],
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
