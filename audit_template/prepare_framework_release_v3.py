"""Build one new, immutable clean release from pinned v2 and current tested tools.

No source documents, live database, output, owner decision, edition selection,
company calibration or Claude infrastructure enters the release. Build-time
source reads are explicit; installed code never reads those source projects.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import re
import subprocess

import yaml
from framework_release import spec, load_manifest

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
LATEST = WORKSPACE/'Enconet'
RUNTIME = ROOT/'runtime_v3'
VERSION = '3.0.0'
TOOLS = (
    'build_evaluation_package.py','build_dashboard_data.py','generate_report.py',
    'generate_dashboard.py','validate_report.py','validate_dashboard.py',
    'finding_workflow.py','validate_findings.py','citation_renderer.py',
    'evidence_navigation.py','evidence_resolver.py','generate_evidence_bundle.py',
    'validate_evidence_bundle.py','validate_report_links.py','generate_review_catalog.py',
    'generate_review_workspace.py','validate_review_catalog.py','validate_review_workspace.py',
    'build_review_package.py','validate_review_package.py','browser_harness.py',
    'validate_evidence_access_budgets.py','publish_audit_release.py','repair_release_permissions.ps1',
    'build_dark_dashboard.py','dashboard_dark.css','dashboard_reference_groups.js','dashboard_spotlight.js',
    'seed_requirements.py','approve.py','sieve_generation.py',
)
CONTRACTS = (
    'evaluation_package_schema.yml','dashboard_schema.yml','evidence_bundle.schema.json',
    'evidence_navigation.yml','review_catalog.schema.json','review_package_manifest.schema.json',
    'vocabularies.yml','page_types.yml','required_fields.yml',
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def neutral(text):
    return text.replace('ENCONET','PROJECT').replace('Enconet','project').replace('enconet','project')


def collect():
    baseline = spec()
    old = load_manifest(baseline)
    files = {row['path']:(baseline.bundle/row['path']).read_bytes() for row in old['files']}
    provenance = [{'source':'audit_template/framework/v2/manifest.json',
                   'sha256':digest((baseline.bundle/'manifest.json').read_bytes())}]
    def copy(relative):
        data = (LATEST/relative).read_bytes()
        provenance.append({'source':'Enconet/'+relative,'sha256':digest(data)})
        return neutral(data.decode('utf-8')).replace('\r\n','\n').encode('utf-8')
    for name in TOOLS:
        files['scripts/'+name] = copy('scripts/'+name)
    for name in CONTRACTS:
        files['schemas/'+name] = copy('schemas/'+name)
    for name in ('evaluation-report-template.md','finding-template.md','action-template.md',
                 'review-workspace-template.html'):
        files['templates/'+name] = copy('templates/'+name)
    files['templates/dashboard-template.html'] = copy('templates/dashboard-template.html')
    files['scripts/evidence_access_policy.py'] = (RUNTIME/'evidence_access_policy.py').read_bytes()
    files['scripts/supplier_identity.py'] = (RUNTIME/'supplier_identity.py').read_bytes()
    text = files['scripts/validate_evidence_bundle.py'].decode('utf-8')
    text = text.replace('for field in ("supplier", "framework"):', 'for field in ("framework",):')
    marker = '        patterns = _patterns()'
    insert = '''        supplier = metadata.get("supplier")
        if not isinstance(supplier, str) or not supplier.strip() or len(supplier) > 256 or any(ord(c) < 32 or 127 <= ord(c) < 160 for c in supplier):
            errors.append("invalid metadata.supplier")
'''
    text = text.replace(marker,insert+marker,1)
    files['scripts/validate_evidence_bundle.py'] = text.encode('utf-8')
    schema = json.loads(files['schemas/evidence_bundle.schema.json'])
    schema['$defs']['metadata']['properties']['supplier'] = {
        'type':'string','minLength':1,'maxLength':256,
        'description':'Explicit local supplier display name; Unicode and spaces allowed, never a path.'}
    files['schemas/evidence_bundle.schema.json'] = (json.dumps(schema,indent=2)+'\n').encode('utf-8')
    text = files['scripts/validate_review_catalog.py'].decode('utf-8')
    text = text.replace('import yaml','import yaml\nfrom supplier_identity import supplier_label') if 'import yaml' in text else text.replace('import re','import re\nfrom supplier_identity import supplier_label')
    text = text.replace('for field in ("supplier", "framework"):', 'for field in ("framework",):')
    text = text.replace('        artifacts = row.get("artifacts")',
        '''        try:
            supplier_label(row.get("supplier"))
        except ValueError:
            errors.append(f"invalid catalog supplier: {prefix}")
        artifacts = row.get("artifacts")''')
    files['scripts/validate_review_catalog.py'] = text.encode('utf-8')
    schema = json.loads(files['schemas/review_catalog.schema.json'])
    # Supplier is a display name, not a path or an identifier grammar.
    def labels(node):
        if isinstance(node,dict):
            if isinstance(node.get('properties'),dict) and 'supplier' in node['properties']:
                node['properties']['supplier']={'type':'string','minLength':1,'maxLength':256}
            for child in node.values(): labels(child)
        elif isinstance(node,list):
            for child in node: labels(child)
    labels(schema)
    files['schemas/review_catalog.schema.json'] = (json.dumps(schema,indent=2)+'\n').encode('utf-8')
    # Keep the safer preserving intake, initializer, state and evaluation writer.
    # The updated package reader needs the same metrics API with an optional model.
    text = files['scripts/evaluation_engine.py'].decode('utf-8')
    text = text.replace('human judge_ruling and rationale are required','documentary judge_ruling and rationale are required')
    text = text.replace('def metrics(rows: list[dict], *, scoring_model: dict) -> dict:',
                        'def metrics(rows: list[dict], *, scoring_model: dict | None = None) -> dict:\n    scoring_model = scoring_model or model()')
    files['scripts/evaluation_engine.py'] = text.encode('utf-8')
    # Use the coherent current DDL, with the portable source-approval registry.
    current = copy('db/schema.sql').decode('utf-8')
    old_schema = files['db/schema.sql'].decode('utf-8')
    registry = re.search(r'CREATE TABLE IF NOT EXISTS approved_sources \(.*?\) STRICT;',old_schema,re.S).group(0)
    files['db/schema.sql'] = (current+'\n'+registry+'\nPRAGMA user_version = 1;\n').encode('utf-8')
    # No inherited package registration or capacity approval.
    files['schemas/review_packages.yml'] = b'schema_version: "1.0"\npackages: []\n'
    for name in ('evidence_access_budgets.yml','evidence_access_budgets_v2.yml'):
        data = yaml.safe_load((LATEST/'schemas'/name).read_text(encoding='utf-8'))
        provenance.append({'source':'Enconet/schemas/'+name,'sha256':digest((LATEST/'schemas'/name).read_bytes())})
        data['approval'] = {'authority':'project_owner','decision':'pending-local-owner',
                            'evidence':'Clean capacity candidate; no inherited approval.'}
        if name.endswith('_v2.yml'):
            data['approval']['approval_ref'] = 'EVIDENCE-SIZE-LOCAL'
        files['schemas/'+name] = yaml.safe_dump(data,sort_keys=False).encode('utf-8')
    browser = yaml.safe_load((LATEST/'schemas/browser_harness.yml').read_text(encoding='utf-8'))
    browser['browser']['root'] = 'browser-runtime'
    files['schemas/browser_harness.yml'] = yaml.safe_dump(browser,sort_keys=False).encode('utf-8')
    text = files['scripts/browser_harness.py'].decode('utf-8')
    text = text.replace('    return config\n',
                        '    value = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or config["browser"]["root"])\n    config["browser"]["root"] = str((value if value.is_absolute() else PROJECT / value).resolve())\n    return config\n',1)
    text = text.replace('return Path(override if override else config["browser"]["root"]).resolve()',
                        'value = Path(override if override else config["browser"]["root"])\n    return (value if value.is_absolute() else PROJECT / value).resolve()')
    files['scripts/browser_harness.py'] = text.encode('utf-8')
    files['benchmarks/validate_benchmarks.py'] = (RUNTIME/'validate_benchmarks.py').read_bytes()
    # Missing Claude files remain visibly pending, never synthesized or reported
    # synchronized. Only that infrastructure absence may be explicitly tolerated.
    # Bring config-selected size guards into the preserving local aggregate.
    text = files['scripts/run_all_validations.py'].decode('utf-8')
    text = text.replace('supplier = _safe_supplier(state["supplier"])',
                        'supplier = re.sub(r"[^a-z0-9_-]+", "-", _safe_supplier(state["supplier"]).casefold()).strip("-")')
    text = text.replace('        checks = run(phase, check_commands)',
        '''        if state.get("evidence_budget_profile"):
            import generate_dashboard
            profile = local_path(args.state.parent / state["evidence_budget_profile"])
            generate_dashboard.load_budget_profile(profile)
            command = check_commands["evidence_budgets"]
            command[command.index("--budgets") + 1] = str(profile)
        checks = run(phase, check_commands)''')
    text = text.replace('        checks = run(phase, check_commands)',
        '''        if args.allow_pending_claude:
            check_commands["sieving_harness"].append("--allow-pending-claude")
        checks = run(phase, check_commands)''')
    text = text.replace('    parser.add_argument("--no-record", action="store_true")',
                        '    parser.add_argument("--allow-pending-claude", action="store_true", help="explicit pending agent infrastructure only; no audit approval")\n    parser.add_argument("--no-record", action="store_true")')
    files['scripts/run_all_validations.py'] = text.encode('utf-8')
    # Candidate generation must never silently write a controlled published path.
    text = files['scripts/generate_report.py'].decode('utf-8')
    text = text.replace('            content = render(package, documentary=args.documentary)',
                        '            evidence_access_policy.require_output_target(output)\n            content = render(package, documentary=args.documentary)')
    files['scripts/generate_report.py'] = text.encode('utf-8')
    text = files['scripts/generate_dashboard.py'].decode('utf-8')
    text = text.replace('            for path in (output, wiki_output):\n',
                        '            for path in (output, wiki_output):\n                evidence_access_policy.require_output_target(path)\n')
    files['scripts/generate_dashboard.py'] = text.encode('utf-8')
    text = files['scripts/publish_audit_release.py'].decode('utf-8')
    text = text.replace('def validate_live(root):','def validate_live(root, *, allow_pending_claude=False):')
    text = text.replace('        completed = subprocess.run([sys.executable, str(root / "scripts/run_all_validations.py"),',
                        '        command = [sys.executable, str(root / "scripts/run_all_validations.py"),')
    text = text.replace('"--state", str(projected), "--benchmarks", "--no-record"],\n                                   cwd=root, check=False)',
                        '"--state", str(projected), "--benchmarks", "--no-record"]\n        if allow_pending_claude:\n            command.append("--allow-pending-claude")\n        completed = subprocess.run(command, cwd=root, check=False)')
    text = text.replace('    parser.add_argument("--execute", action="store_true")',
                        '    parser.add_argument("--execute", action="store_true")\n    parser.add_argument("--allow-pending-claude", action="store_true", help="explicit pending agent infrastructure, not review acceptance")')
    text = text.replace('validator=lambda: validate_live(ROOT)',
                        'validator=lambda: validate_live(ROOT, allow_pending_claude=args.allow_pending_claude)')
    files['scripts/publish_audit_release.py'] = text.encode('utf-8')
    text = files['scripts/publish_audit_release.py'].decode('utf-8')
    # Complete the atomic no-clobber install, then remove only its temporary
    # alias before local validators inspect nlink. Existing hard-link rejection
    # remains intact; no exception is added to evidence/path validators.
    text = text.replace('                installed.append((destination, digest))\n',
                        '                installed.append((destination, digest))\n                path.unlink()  # temporary alias only; public file now has one link\n')
    text = text.replace('            installed.append((result_path, hashlib.sha256(marker.read_bytes()).hexdigest()))',
                        '            installed.append((result_path, hashlib.sha256(marker.read_bytes()).hexdigest()))\n            marker.unlink()')
    files['scripts/publish_audit_release.py'] = text.encode('utf-8')
    text = files['scripts/validate_evaluation.py'].decode('utf-8')
    text = text.replace('    args = parser.parse_args()',
                        '    parser.add_argument("--no-record", action="store_true", help="compatibility: this validator is always read-only")\n    args = parser.parse_args()')
    files['scripts/validate_evaluation.py'] = text.encode('utf-8')
    # Current schema stores optional source anchors; keep v2 safe importer API.
    text = files['scripts/import_crumbs.py'].decode('utf-8')
    marker = '        conn.execute("UPDATE sieve_runs SET completed_at=CURRENT_TIMESTAMP WHERE run_id=?", (run_id,))'
    text = text.replace(marker, '''            if 'context' in item or 'evidence_type' in item:
                context = item.get('context', {})
                db_util.insert(conn, 'crumb_context', {'item_id': crumb_id,
                    'evidence_type': item.get('evidence_type'),
                    **{field: context.get(field) for field in ('project_ref','contract_ref','supplier_ref','source_revision','evidence_date')}})
'''+marker)
    files['scripts/import_crumbs.py'] = text.encode('utf-8')
    files['sieving/src/json_extractor/evidence_context.py'] = copy('sieving/src/json_extractor/evidence_context.py')
    text = files['sieving/src/json_extractor/crumb_validation.py'].decode('utf-8')
    text = text.replace('from .contract import canonical_codes, load_contract',
                        'from .contract import canonical_codes, load_contract\nfrom .evidence_context import validate_context')
    text = text.replace('        for optional in ("item_type", "entities"):',
                        '        result.errors.extend(f"{where}: {error}" for error in validate_context(item))\n        for optional in ("item_type", "entities"):')
    files['sieving/src/json_extractor/crumb_validation.py'] = text.encode('utf-8')
    schema = yaml.safe_load(files['schemas/app_b_json_schema.yml'])
    schema['targets_prompt_versions'].append('appb_document_v3_context_anchors')
    schema['item_block']['optional_fields']['evidence_type'] = {'tier':'strict_when_present','enum_from':'evidence_context.evidence_types'}
    schema['item_block']['optional_fields']['context'] = {'tier':'strict_when_present','fields_from':'evidence_context.context_fields'}
    files['schemas/app_b_json_schema.yml'] = yaml.safe_dump(schema,sort_keys=False).encode('utf-8')
    text = files['scripts/init_db.py'].decode('utf-8').replace('    "approved_sources",','    "approved_sources", "crumb_context",')
    files['scripts/init_db.py'] = text.encode('utf-8')
    files['docs/FRAMEWORK_METHOD_V3.md'] = (RUNTIME/'FRAMEWORK_METHOD_V3.md').read_bytes()
    files['.gitattributes'] += b'\n# v3 immutable portable payload and generated evidence\noutputs/** -text\nwiki/dashboards/*.html -text\nscripts/*.ps1 text eol=lf\n'
    for name, data in list(files.items()):
        if name.endswith('.py'):
            if name.startswith('scripts/') and 'if __name__ ==' in data.decode('utf-8'):
                text = data.decode('utf-8')
                text = re.sub(r'(if __name__ == [\'\"]__main__[\'\"]:\n)',
                              r'\1    from project_paths import configure_standard_streams\n    configure_standard_streams()\n',text)
                data = files[name] = text.encode('utf-8')
            ast.parse(data.decode('utf-8'),filename=name)
        if name.startswith(('raw/','out/','outputs/','coordination/','.claude/')) or 'CLAUDE.md' in name:
            raise ValueError('Company or reviewer payload is forbidden: '+name)
    return files, provenance


def build(destination=None, *, refresh_candidate=False):
    folder = Path(destination) if destination is not None else ROOT/'framework/v3'
    if folder.exists() and not refresh_candidate:
        raise FileExistsError('Versioned release exists; never rebuild it in place')
    files, provenance = collect()
    if refresh_candidate:
        if folder.resolve() != (ROOT/'framework/v3').resolve():
            raise ValueError('Only this uncommitted v3 candidate may be refreshed')
        tracked = subprocess.check_output(['git','ls-files','--','audit_template/framework/v3'],cwd=WORKSPACE,text=True)
        if tracked.strip():
            raise ValueError('Committed or staged release is immutable')
        previous = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        if previous['status'] != 'candidate-not-company-approved':
            raise ValueError('Only an unpublished candidate may be refreshed')
        existing = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}-{'manifest.json'}
        if not existing <= set(files):
            raise ValueError('Candidate refresh may not delete paths')
    # Validate all content before the first output write.
    folder.mkdir(parents=True,exist_ok=refresh_candidate)
    for name, data in sorted(files.items()):
        path = folder/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    manifest = {'template_version':VERSION,'scope':'clean-audit-framework',
                'status':'candidate-not-company-approved','source_head':subprocess.check_output(
                    ['git','rev-parse','HEAD'],cwd=WORKSPACE,text=True).strip(),
                'provenance':provenance,
                'files':[{'path':name,'sha256':digest(data),'bytes':len(data)} for name,data in sorted(files.items())]}
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-candidate',action='store_true')
    result = build(refresh_candidate=parser.parse_args().refresh_candidate)
    print(f"v3: {len(result['files'])} files; no company evidence or approvals")
