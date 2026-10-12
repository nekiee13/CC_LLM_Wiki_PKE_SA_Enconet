"""Read-only preparation of a path overlay from a supplier's own runtime.

Never replace company audit logic with another project's implementation.
Emit a complete script snapshot and mark only changed code for later installation.
Direct-path findings and unadapted integrations keep the overlay un-installable.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import stat

from prepare_framework_candidate_v4 import (route_python, replace_assignment, replace_once,
                                          MOVED, BASELINE, PIN, sha, verify_payload)
from check_candidate_paths_v4 import scan

WORKSPACE = Path(__file__).resolve().parents[1]


def local_literals(source):
    """Route path arguments/defaults, never arbitrary quoted evidence or IDs."""
    tree = ast.parse(source)
    raw = source.encode('utf-8')
    lines = raw.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits = {}
    def route(node):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            return
        parts = node.value.split('/')
        if parts[0] not in MOVED:
            return
        value = '/'.join((MOVED[parts[0]], *parts[1:]))
        start = offsets[node.lineno - 1] + node.col_offset
        end = offsets[node.end_lineno - 1] + node.end_col_offset
        edits[(start, end)] = repr(value).encode('utf-8')
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == 'local' and len(node.args) >= 2:
                route(node.args[1])
            elif node.func.id == 'bind' and node.args:
                route(node.args[0])
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == 'add_argument'):
            for keyword in node.keywords:
                if (keyword.arg == 'default' and isinstance(keyword.value, ast.Call)
                        and isinstance(keyword.value.func, ast.Name) and keyword.value.func.id == 'Path'
                        and len(keyword.value.args) == 1):
                    route(keyword.value.args[0])
    for (start, end), value in sorted(edits.items(), reverse=True):
        raw = raw[:start] + value + raw[end:]
    return raw.decode('utf-8'), len(edits)


def regular(path):
    for item in (path, *path.parents):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('redirected supplier path')
    if path.stat().st_nlink != 1:
        raise ValueError('hard-linked supplier source')
    return path.read_bytes()


def build(supplier, destination, *, workspace=WORKSPACE):
    workspace = Path(workspace).resolve(strict=True)
    source_root = workspace / supplier
    if (supplier in {'', '.', '..'} or Path(supplier).name != supplier
            or not source_root.is_dir() or source_root.resolve().parent != workspace):
        raise ValueError('one existing supplier folder name required')
    destination = Path(destination).absolute()
    if destination.exists() or not destination.resolve().is_relative_to(workspace / '.tmp'):
        raise ValueError('fresh workspace .tmp destination required')
    for item in (destination.parent, *destination.parent.parents):
        if item.exists() and (item.is_symlink() or getattr(item.stat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('redirected overlay parent')
    payload, changes, holds = {}, [], []
    for path in sorted((source_root / 'scripts').glob('*.py')):
        if path.name.startswith('CC_'):
            holds.append({'file': path.name, 'reason': 'Claude-owned filename'})
            continue
        before = regular(path)
        text = before.decode('utf-8-sig')
        if path.name == 'reset_audit.py':
            text = replace_assignment(text, 'RESET_DIRS', lambda values:
                tuple(value for value in values if value not in {'out', 'derived', 'work'})
                + ('work/derived', 'work/validation'))
            text = replace_assignment(text, 'RESET_TEXT_FILES', lambda values:
                {'work/' + key if key.startswith('manifests/') else key: value for key, value in values.items()})
        if path.name in {'make_handoff.py', 'run_validation.py'}:
            fragment = r'(handoffs/[^)]+\.md)'
            if fragment in text:
                text = replace_once(text, fragment, r'(coordination/handoffs/[^)]+\.md)')
        if path.name == 'agent_coord.py':
            fragment = 'pointer.replace("(handoffs/", "(../handoffs/")'
            if fragment in text:
                text = replace_once(text, fragment, 'pointer.replace("(coordination/handoffs/", "(handoffs/")')
        if path.name == 'project_paths.py':
            text = replace_once(text, 'import stat', 'from project_records import recorded_path\nimport stat')
            text = replace_once(text, '    path = Path(value)\n    if not path.is_absolute():\n        path = ROOT / path',
                                '    path = recorded_path(value)')
        if path.name == 'source_revision_intake.py':
            text = replace_once(text, 'import argparse',
                                'from project_records import recorded_path_at\nimport argparse')
            text = replace_once(text, '    value = path if path.is_absolute() else root / path',
                                '    value = recorded_path_at(root, path)')
            text = replace_once(text, "derived=f'derived/{new_id}.txt'; artifact=f'derived/chunks/{new_id}.json'",
                                "derived=f'work/derived/{new_id}.txt'; artifact=f'work/derived/chunks/{new_id}.json'")
        if path.name == 'validate_report_links.py':
            text = replace_once(text, 'import argparse',
                                'from project_records import recorded_path_at\nimport argparse')
            text = replace_once(text, 'artifact = (root / Path(relative)).resolve()',
                'artifact = (recorded_path_at(root, relative) if root == ENCONET.resolve() '
                'else root / Path(relative)).resolve()')
        if path.name == 'build_evidence_dashboard.py':
            text = replace_once(text, 'import argparse', 'from project_records import recorded_path\nimport argparse')
            text = replace_once(text, '"matrix": "out/2026-10-05/MIN-3.1-evidence-matrix-v4.json"',
                                '"matrix": recorded_path(matrix_path).relative_to(ROOT).as_posix()')
            text = replace_once(text, 'counts, criteria = _query_snapshot(db, matrix_path, run_id)',
                                'counts, criteria = _query_snapshot(db, recorded_path(matrix_path), run_id)')
        if path.name == 'reset_audit.py':
            text = replace_once(text, 'from project_paths import configure_standard_streams',
                                'from reset_operations import remove_generated\nfrom project_paths import configure_standard_streams')
            text = replace_once(text, '            path.unlink()', '            remove_generated(path)')
        if path.name == 'run_all_validations.py':
            text = replace_once(text, 'import argparse', 'from project_records import recorded_path\nimport argparse')
            if 'BENCHMARKS = ENCONET / "benchmarks" / "validate_benchmarks.py"' in text:
                text = replace_once(text, 'BENCHMARKS = ENCONET / "benchmarks" / "validate_benchmarks.py"',
                                    'BENCHMARKS = SCRIPTS / "validate_benchmarks.py"')
            if '"--allow-pending-claude"' not in text:
                text = replace_once(text, '    parser.add_argument("--no-record", action="store_true")',
                    '    parser.add_argument("--no-record", action="store_true")\n    parser.add_argument("--allow-pending-claude", action="store_true", help="explicit deferred agent infrastructure; never source or evidence approval")')
                text = replace_once(text, '        checks = run(phase, check_commands)',
                    '        if args.allow_pending_claude:\n            check_commands["sieving_harness"].append("--allow-pending-claude")\n        checks = run(phase, check_commands)')
            text = replace_once(text, 'package = outputs / f"{supplier}_appendix_b_evaluation_package.json"',
                                'run_root = outputs / run_id if run_id else outputs\n    package = run_root / "evaluation_package.json"')
            for old, new in [('evaluation_report.md', 'report.md'), ('dashboard_data.json', 'dashboard_data.json'),
                             ('dashboard.html', 'dashboard_light.html')]:
                text = replace_once(text, 'outputs / f"{supplier}_appendix_b_' + old + '"',
                                    'run_root / "' + new + '"')
            text = replace_once(text, 'evidence_root = outputs / "candidates" / "evidence_access"',
                                'evidence_root = layout_path("reviews")')
            text = replace_once(text, 'evidence_run = evidence_root / run_id if run_id else None',
                                'evidence_run = run_root if run_id else None')
            text = replace_once(text, 'evidence_run / f"{supplier}_appendix_b_evaluation_report.md"',
                                'evidence_run / "report.md"')
            text = replace_once(text, 'evidence_run / f"{supplier}_appendix_b_dashboard.html"',
                                'evidence_run / "dashboard_light.html"')
            text = replace_once(text, 'evidence_run / "evidence_bundle.json"',
                'recorded_path("outputs/candidates/evidence_access/" + run_id + "/evidence_bundle.json")')
            package_reference = 'evidence_root / "portable_package"'
            if text.count(package_reference) != 2:
                raise ValueError('portable package validator bindings differ')
            text = text.replace(package_reference,
                'recorded_path("outputs/archive/legacy-outputs/candidates/evidence_access/portable_package")')
            text = replace_once(text, 'evidence_root / "validation_artifacts" / "browser_evidence"',
                                'layout_path("validation", run_id or "setup", "browser_evidence")')
        if path.name == 'run_validation.py':
            text = replace_once(text, 'import argparse', 'from project_scratch import temporary_directory\nimport argparse')
            text = replace_once(text, '    try:\n        proc = subprocess.run(',
                '    try:\n        with temporary_directory(prefix="validation-") as scratch:\n            env.update({key: scratch for key in ("TMP", "TEMP", "TMPDIR")})\n            command = list(step.command)\n            if command[1:3] == ["-m", "pytest"]:\n                command.extend(["--basetemp", str(Path(scratch) / "pytest")])\n            proc = subprocess.run(')
            text = replace_once(text, '            step.command, cwd=step.cwd, capture_output=True, text=True,\n            encoding="utf-8", errors="replace", timeout=STEP_TIMEOUT_S, env=env,\n        )',
                '                command, cwd=step.cwd, capture_output=True, text=True,\n                encoding="utf-8", errors="replace", timeout=STEP_TIMEOUT_S, env=env,\n            )')
        if path.name == 'package_audit_delivery.py':
            text = replace_once(text, "base = Path(root).absolute()/'outputs/candidates/evidence_access'/run_id",
                                "base = layout_path_at(root, 'outputs') / run_id")
            text = replace_once(text, 'if output == base or not output.is_relative_to(base):',
                                'if output != base:')
            text = replace_once(text, "raise ValueError('Output must be a fresh subdirectory of the run candidate root')",
                                "raise ValueError('Output must be the exact run output folder')")
            text = replace_once(text, "    stem = supplier.casefold().replace(' ','_')+'_appendix_b'\n    name = {k:stem+'_'+suffix for k,suffix in dict(package='evaluation_package.json',\n            report='evaluation_report.md', data='dashboard_data.json', light='dashboard.html',\n            dark='dashboard_dark.html').items()}",
                                "    name = dict(package='evaluation_package.json', report='report.md',\n                data='dashboard_data.json', light='dashboard_light.html', dark='dashboard_dark.html')")
            start = text.index("    portable = 'portable_package/'+run_id+'/'")
            stop = text.index('    if any(sha(p.read_bytes()) != h for p,h in before.items()):', start)
            text = text[:start] + "    files['README.md'] = (f'# {supplier} documentary delivery\\n\\n'\n        'Open dashboard_light.html or dashboard_dark.html. Each HTML is self-contained.\\n'\n        'Stored scores, quotes and release-gate status are preserved.\\n').encode('utf-8')\n" + text[stop:]
            text = replace_once(text, 'import argparse',
                                'from project_layout import path_at as layout_path_at\nimport argparse')
        text, literals = local_literals(text)
        explicit = ('root', 'project')
        converted, count = route_python(text, explicit)
        name = 'scripts/' + path.name
        payload[name] = converted.encode('utf-8')
        if converted.encode('utf-8') != before:
            data = converted.encode('utf-8')
            changes.append({'path': name, 'before_sha256': hashlib.sha256(before).hexdigest(),
                            'after_sha256': hashlib.sha256(data).hexdigest(), 'routed_paths': count + literals})
    added = []
    if not (source_root / 'scripts/agent_coord.py').exists():
        baseline_bytes = (BASELINE / 'manifest.json').read_bytes()
        if sha(baseline_bytes) != PIN:
            raise ValueError('neutral coordinator baseline checksum mismatch')
        neutral = verify_payload(json.loads(baseline_bytes), BASELINE)['scripts/agent_coord.py']
        text = neutral.decode('utf-8')
        text = replace_once(text, 'pointer.replace("(handoffs/", "(../handoffs/")',
                            'pointer.replace("(coordination/handoffs/", "(handoffs/")')
        payload['scripts/agent_coord.py'] = text.encode('utf-8')
        added.append('scripts/agent_coord.py')
    benchmark = source_root / 'benchmarks/validate_benchmarks.py'
    if benchmark.is_file() and not (source_root / 'scripts/validate_benchmarks.py').exists():
        text = regular(benchmark).decode('utf-8-sig')
        text = replace_once(text, 'ROOT = Path(__file__).resolve().parent',
                            'from project_layout import path as layout_path\nROOT = layout_path("benchmarks")')
        payload['scripts/validate_benchmarks.py'] = text.encode('utf-8')
        added.append('scripts/validate_benchmarks.py')
    for name in ('project_layout.py', 'project_scratch.py', 'reset_operations.py', 'project_records.py'):
        target = source_root / 'scripts' / name
        if target.exists():
            holds.append({'file': str(target.relative_to(source_root)), 'reason': 'new helper destination already exists'})
            continue
        payload['scripts/' + name] = (WORKSPACE / 'audit_template/runtime_v4' / name).read_bytes()
    payload['project-layout.json'] = b'{"schema_version":1,"layout":"v4"}\n'
    payload['project-file-relocations.json'] = b'{"schema_version":1,"paths":{}}\n'
    if (source_root / 'project-layout.json').exists():
        holds.append({'file': 'project-layout.json', 'reason': 'existing layout configuration requires review'})
    manifest = {'schema_version': 1, 'status': 'development-overlay-not-installable',
        'source_supplier': supplier, 'changes': changes, 'holds': holds,
        'install_paths': [row['path'] for row in changes] + added + [
            'scripts/project_layout.py', 'scripts/project_scratch.py',
            'scripts/reset_operations.py', 'scripts/project_records.py',
            'project-layout.json', 'project-file-relocations.json'],
        'remaining': ['direct-path findings', 'output defaults and stored-path users',
                      'scratch integration', 'isolated current-runtime validation and review',
                      'dirty and owned-file move dispositions'],
        'files': [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(payload.items())]}
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in payload.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
    with (destination / 'candidate-manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
    report = scan(destination)
    with (destination / 'path-sweep.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
    return {'changed_scripts': len(changes), 'routed_paths': sum(row['routed_paths'] for row in changes),
            'holds': holds, 'direct_code_findings': len(report['code_findings']),
            'snapshotted_scripts': sum(name.startswith('scripts/') for name in payload),
            'status': manifest['status']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--supplier', required=True)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.supplier, args.destination), ensure_ascii=False))


if __name__ == '__main__':
    main()
