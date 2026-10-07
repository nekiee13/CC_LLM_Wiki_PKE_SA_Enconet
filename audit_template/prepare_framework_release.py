"""Assemble the pinned clean framework and additive upgrade, once per version.

Build-time reads may use the source project. Installed runtime files never do.
Regulatory texts, databases, owner approvals and active prompt history are excluded.
"""
from __future__ import annotations

import hashlib
import argparse
import json
from pathlib import Path
import re
import subprocess

from bootstrap_sieving import BundleSpec, load_manifest

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
LIGHT = WORKSPACE / 'Ekonerg/out/2026-10-07/all18-review/EKONERG_DASHBOARD.html'
LIGHT_SHA = '99197f65e2ed2fa9e4e68d5da3fd517d9f0c995fad6e9c51338c2ac6465b194d'
VERSION = '2.0.0'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def template():
    raw = LIGHT.read_bytes()
    if sha(raw) != LIGHT_SHA:
        raise ValueError('Approved presentation source changed')
    text = raw.decode('utf-8')
    css = re.search(r'<style>(.*?)</style>',text,re.S).group(1)
    js = re.search(r'<script>(.*?)</script>',text,re.S).group(1)
    js, count = re.subn(r'const data = .*?;\nconst labels=', 'const data = __DATA__;\nconst labels=', js, flags=re.S)
    if count != 1:
        raise ValueError('Cannot isolate presentation from audit data')
    js = js.replace("unmet:'Unmet'}", "unmet:'Unmet',na:'Not applicable'}")
    js = js.replace("unmet:'var(--unmet)'}", "unmet:'var(--unmet)',na:'var(--und)'}")
    js = js.replace('fully:1};','fully:1,na:0};')
    # Existing evidence-sort was effectively a no-op (empty evidenceRank).
    js = js.replace('(evidenceRank[b.crumbs]||0)-(evidenceRank[a.crumbs]||0)',
                    '(b.score_crumb_count||0)-(a.score_crumb_count||0)')
    js = js.replace("if(k==='crumbs') return clean(a.crumbs).localeCompare(clean(b.crumbs))*asc;",
                    "if(k==='crumbs') return (a.score_crumb_count-b.score_crumb_count)*asc;")
    js = js.replace('${d.score}% · ${d.scale_points}/5',
                    "${d.applicable ? d.score+'% · '+d.scale_points+'/5' : 'Not applicable'}")
    js = js.replace('No linked vendor crumb; score is unmet because vendor evidence is absent.',
                    'No linked vendor crumb in this recorded evaluation.')
    body = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title>
<style>__CSS__</style></head><body>
<header class="header"><h1>__TITLE__</h1><p class="sub">Recorded documentation audit of __SUPPLIER__. Read each rating with its source evidence and written gaps. Objective implementation checks belong to the real audit.</p><div class="pillRow"><span class="pill">Local vendor evidence</span><span class="pill">Overall: __SCORE__</span><span class="pill">18 criteria visible</span></div></header>
<section class="topbar">__METRICS__</section><main class="wrap">
<section class="section summaryGrid"><div><h2>Executive Summary</h2><p>The recorded result is <strong>__SCORE__</strong>. Ratings come from this vendor's selected run, not from crumb counts. The five levels are fully (5/5, 100), substantially (4/5, 75), partially (3/5, 50), minimally (2/5, 25), and unmet (1/5, 0). Approved not-applicable criteria stay visible and are excluded from the score.</p><div class="note">Written controls and operational proof are different. A full documentation rating does not prove implementation. This ordinal score is not a percentage of every regulatory clause.</div><div class="note">__NOTE__</div></div><div><h2>Classification Distribution</h2><div class="legend">__DISTRIBUTION__</div></div></section>
<section class="section"><h2>Criterion Cards — Evidence Review</h2><div class="controls">
<button class="btn active" data-filter="all">All <span class="count">18</span></button>__FILTERS__
<input class="search" id="search" aria-label="Search criteria" placeholder="Search criteria or evidence (/)">
<select class="select" id="sort" aria-label="Sort criteria"><option value="order">Criterion order</option><option value="risk">Lowest rating first</option><option value="score">Highest score first</option><option value="evidence">Most linked evidence first</option></select>
<button class="btn utility" id="expandAll">Expand all</button><button class="btn utility" id="collapseAll">Collapse all</button><button class="btn utility" id="printBtn">Print / PDF</button></div><div class="grid" id="cards"></div></section>
<section class="section"><h2>__SUPPLIER__ Evidence Matrix</h2><p>Click a column heading to sort.</p><div class="matrixWrap"><table class="matrix" id="matrix"></table></div></section>
<section class="section"><h2>Top Gaps Requiring Follow-up</h2><ul class="riskList">__GAPS__</ul></section>
<section class="section"><h2>Priority Auditor Verification Actions</h2><ol class="riskList">__ACTIONS__</ol></section>
<footer class="footer">Snapshot __DATE__; run __RUN__; model __MODEL__. Separate presentation candidate; no audit data changed.</footer></main>
<script>__JS__</script></body></html>
'''
    result = body.replace('__CSS__',css).replace('__JS__',js)
    if any(name in result.casefold() for name in ('ekonerg','enconet','tekol')):
        raise ValueError('Company data leaked into presentation template')
    return result.encode('utf-8')


def collect():
    files, provenance = {}, []
    for path in sorted(ROOT.glob('*/v1/manifest.json')):
        m = json.loads(path.read_text(encoding='utf-8'))
        names = frozenset(e['path'] for e in m['files'])
        spec = BundleSpec(path.parent,m['template_version'],m['scope'],
            frozenset(n.split('/')[0] for n in names),'unused','unused',names)
        load_manifest(spec)
        for name in names:
            data = (path.parent / name).read_bytes()
            if name in files and files[name] != data:
                raise ValueError('Conflicting component bytes: ' + name)
            files[name] = data
        provenance.append(dict(component=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes())))
    additions = {}
    for name in ('full_keyword_sweep.py','build_dark_dashboard.py','dashboard_dark.css',
                 'dashboard_reference_groups.js','dashboard_spotlight.js','reset_audit.py','project_paths.py'):
        data = (WORKSPACE / 'Ekonerg/scripts' / name).read_bytes()
        provenance.append(dict(source='Ekonerg/scripts/'+name,sha256=sha(data)))
        text = data.decode('utf-8').replace('ekonerg-', 'audit-').replace('RESET-EKONERG','RESET-AUDIT')
        if name == 'reset_audit.py':
            text = text.replace("Ekonerg's", "this project's").replace('PLAN_VERSION = 1','PLAN_VERSION = 2')
            text = text.replace('    "raw",','    "raw",\n    "out",\n    "sieving/candidates",')
            text = text.replace('RESET_TEXT_FILES = {','RESET_TEXT_FILES = {\n    "manifests/raw_sources.csv": "doc_id,filename,title,supplier,doc_date,language,side_hint,sha256,promoted_utc,source_url,notes",')
        if name == 'full_keyword_sweep.py':
            text = text.replace('if p.is_file())\n    actual =', 'if p.is_file() and p.name != ".gitkeep")\n    actual =')
        additions['scripts/'+name] = text.encode('utf-8')
    additions['scripts/build_vendor_dashboard.py'] = (ROOT / 'runtime_v2/build_vendor_dashboard.py').read_bytes()
    additions['templates/vendor-dashboard.html'] = template()
    for path in ('sieving/prompts/full_keyword_sweep_v1.json','sieving/prompts/appb_concepts.yml',
                 'sieving/prompts/appb_document_v3_context_anchors.md','schemas/evidence_context.yml'):
        data = (WORKSPACE / 'Ekonerg' / path).read_bytes()
        provenance.append(dict(source='Ekonerg/'+path,sha256=sha(data)))
        additions[path] = data
    # Methods are reusable; activation and golden approvals are company-local.
    additions['docs/FRAMEWORK_METHOD_V2.md'] = (ROOT / 'runtime_v2/FRAMEWORK_METHOD_V2.md').read_bytes()
    additions['scripts/project_paths.py'] = files['scripts/project_paths.py']
    # Close two dependency gaps in the older component union. These are clean
    # bootstrap files only, not replacements for Enconet's approved implementations.
    files['scripts/promote_source.py'] = (ROOT / 'runtime_v2/promote_source.py').read_bytes()
    files['scripts/gate_packet.py'] = (WORKSPACE / 'Enconet/scripts/gate_packet.py').read_bytes()
    files['templates/gate-packet-template.md'] = (WORKSPACE / 'Enconet/templates/gate-packet-template.md').read_bytes()
    files['manifests/raw_sources.csv'] = b'doc_id,filename,title,supplier,doc_date,language,side_hint,sha256,promoted_utc,source_url,notes\n'
    files['Sieving_method_specification_Guide.md'] = additions['docs/FRAMEWORK_METHOD_V2.md']
    initializer = files['scripts/init_db.py'].decode('utf-8')
    initializer = initializer.replace('import sqlite3','import sqlite3\nimport yaml',1)
    initializer = initializer.replace('    return "initialized empty database; no source or criterion approved"',
        '''    taxonomy = yaml.safe_load((ROOT / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))["criteria"]
    with closing(sqlite3.connect(db_path)) as conn:
        conn.executemany("INSERT INTO criteria(criterion_id,criterion_name,description) VALUES (?,?,?)",
                         [(c["criterion_id"],c["criterion_name"],c["description"]) for c in taxonomy])
        conn.commit()
    return "initialized database with 18 taxonomy names; no source, applicability or audit approved"''')
    files['scripts/init_db.py'] = initializer.encode('utf-8')
    files['.gitattributes'] += b'\n# Version-2 portable presentation and method assets\nscripts/*.css text eol=lf\nscripts/*.js text eol=lf\ntemplates/** text eol=lf\ndocs/FRAMEWORK_METHOD_V2.md text eol=lf\nSieving_method_specification_Guide.md text eol=lf\ndb/schema.sql text eol=lf\nsieving/SIEVING_PLAYBOOK.md text eol=lf\nbenchmarks/sieving_golden/manifest.yml text eol=lf\nhandoff_schema.yml text eol=lf\n'
    files['.gitattributes'] += b'\n# Preserve evidence exactly across Git checkouts\nincoming/** -text\nraw/** -text\nderived/** -text\nsieving/DATA/** -text\ndb/*.sqlite binary\n'
    return files | additions, additions, provenance


def build(refresh_draft=False):
    files, additions, provenance = collect()
    destination = ROOT / 'framework'
    if destination.exists() and not refresh_draft:
        raise FileExistsError('Versioned release already exists; verify instead of rebuilding in place')
    if refresh_draft:
        tracked = subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD','--','audit_template/framework'],cwd=WORKSPACE,text=True)
        if tracked.strip():
            raise ValueError('Committed release is immutable; prepare a new version instead')
    for label, content, scope in (('v2',files,'clean-audit-framework'),('upgrade-v2',additions,'framework-upgrade')):
        folder = destination / label
        if refresh_draft and folder.exists():
            manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
            if manifest['status'] != 'candidate-tested-not-company-approved':
                raise ValueError('Only an unpublished candidate can be refreshed')
            existing = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()} - {'manifest.json'}
            if not existing <= set(content):
                raise ValueError('Draft refresh may not remove paths; create a new version')
        folder.mkdir(parents=True,exist_ok=refresh_draft)
        for name,data in sorted(content.items()):
            if name.startswith(('raw/','out/','outputs/','.claude/','coordination/')) or 'CLAUDE.md' in name:
                raise ValueError('Forbidden company/infrastructure payload: '+name)
            path = folder / name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
        manifest = dict(template_version=VERSION,scope=scope,status='candidate-tested-not-company-approved',
            source_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=WORKSPACE,text=True).strip(),
            presentation_source_sha256=LIGHT_SHA,provenance=provenance,
            files=[dict(path=name,sha256=sha(data),bytes=len(data)) for name,data in sorted(content.items())])
        (folder / 'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
        print(label, len(content), 'files')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-draft',action='store_true',help='During development only; same path list, unpublished candidate')
    build(parser.parse_args().refresh_draft)
