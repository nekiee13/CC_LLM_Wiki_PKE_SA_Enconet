"""Prepare a relocatable documentary delivery; never issue or replace a gated release.

Preview is read-only. Apply creates a fresh directory under the local candidate
root, writes a hash manifest last, and refuses every existing destination.
Runtime uses this project's copies only. No audit database or approval is written.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sqlite3
import stat
import sys
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_stack_core import approved_ids, build_package, validate_package

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n').encode('utf-8')


def safe(root, path):
    root = Path(root).absolute()
    path = Path(path).absolute()
    if '..' in path.parts or not path.is_relative_to(root):
        raise ValueError('Foreign or escaping path: '+str(path))
    for part in (path, *path.parents):
        if part.exists() or part.is_symlink():
            info = part.lstat()
            if (stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)
                    & getattr(stat,'FILE_ATTRIBUTE_REPARSE_POINT',0)):
                raise ValueError('Redirected path: '+str(part))
            if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
                raise ValueError('Hard-linked file: '+str(part))
    return path


def candidate_path(root, output, run_id):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', run_id):
        raise ValueError('Unsafe run ID')
    output = safe(root, output)
    base = Path(root).absolute()/'outputs/candidates/evidence_access'/run_id
    if output == base or not output.is_relative_to(base):
        raise ValueError('Output must be a fresh subdirectory of the run candidate root')
    return output


def dashboard_data(page):
    match = re.search(r'const data = (\[.*?\]);\s*const labels=', page, re.S)
    if not match:
        raise ValueError('Expected existing standalone dashboard data')
    return json.loads(match.group(1))


def check_projection(data, evaluations):
    rows = {e['criterion_id']: e for e in evaluations}
    if len(data) != len(rows) or len({d['n'] for d in data}) != len(rows):
        raise ValueError('Dashboard/database projection has different criteria')
    for d in data:
        e = rows.get('APP_B_'+d['n'])
        fields = [('rating','classification'),('score','score'),('aff','affirmative_summary'),
                  ('con','contrary_summary'),('judge','judge_ruling'),('rationale','rationale')]
        if not e or any(d[a] != e[b] for a,b in fields):
            raise ValueError('Stale dashboard/database projection: '+d['n'])
        if {c['id'] for c in d['score_crumbs']} != set(e['evidence_ids']):
            raise ValueError('Score-support projection mismatch: '+d['n'])


def render_documentary_export(package, data, viewer):
    """Candidate export of existing official tool judgments, not a formal G4 report."""
    run, metric = package['run'], package['metrics']
    lines = [f"# Appendix B documentary report — {run['supplier']}", '',
             f"Run: `{run['run_id']}`. **{metric['consolidated_score']:g}%** — {metric['classification']}.\n",
             'Prepared documentary delivery of the stored owner-operated tool result; '
             'not an issued G5/G6 release or proof of field implementation.', '',
             '## Scope and method', '',
             '10 CFR 50 Appendix B, interpreted under this project\'s approved ASME NQA-1 scope. '
             'Existing five-level scores, applicability decisions and explanations are preserved. '
             'Part 21 is separate from the 18-criterion score. No source edition or approval is inherited.', '',
             'Report labels retain the current English dashboard presentation; quotations retain their source language.', '',
             '## Executive summary', '',
             '| Rating | Criteria |', '|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in metric['classification_counts'].items() if v]
    lines += ['', '## Criterion-by-criterion evaluation', '']
    scope = {r['criterion_id']:r for r in package.get('applicability',[])}
    for d in data:
        ruling = scope.get('APP_B_'+d['n'], {})
        links = ' '.join(f'[{id}]({viewer}#crumb:{quote(id, safe="")})' for id in d['score_crumb_ids'])
        lines += [f"### {d['n']} — {d['title']}", '',
                  f"**{d['rating']} — {d['score']:g}/100; {d['scale_points']}/5**", '',
                  f"Applicability: {ruling.get('applicability_state', ruling.get('applicable','not recorded'))}.",
                  str(ruling.get('justification','')), '',
                  '**Summary:** '+d['summary'], '', '**Affirmative:** '+d['aff'], '',
                  '**Contrary / limitation:** '+d['con'], '', '**Judgment:** '+d['judge'], '',
                  '**Real-audit verification:** '+d['verify'], '', '**Score-support evidence:** '+links, '']
    lines += ['## Evidence matrix', '', '| Criterion | Score | Linked controls |', '|---|---:|---:|']
    lines += [f"| [{d['n']}]({viewer}#criterion:{d['n']}) | {d['score']:g} | {len(d['score_crumbs'])} |" for d in data]
    lines += ['', '## Findings and follow-up', '',
              'No formal finding rows are recorded.' if not package['findings'] else
              'Formal findings remain in the evaluation package with their recorded status.',
              'The criterion limitations and verification text above are existing documentary '
              'follow-up guidance, not newly approved finding/action database rows.', '',
              '## Limitations and release status', '',
              'Formal G4–G6 records remain as recorded in project-state.yml. This candidate '
              'does not advance a phase, certify implementation, or close real-audit actions. '
              'Every linked crumb opens its verbatim quotations and full linked source chapters.', '']
    return '\n'.join(lines)


HASH_SCRIPT = '''<script id="delivery-evidence-links">
function openDeliveryReference(){
  const raw=decodeURIComponent(location.hash.slice(1));
  const split=raw.indexOf(':'); if(split<0)return;
  const type=raw.slice(0,split),id=raw.slice(split+1);
  const criterion=data.find(d=>type==='criterion'?d.n===id:(d.score_crumb_ids||[]).includes(id));
  if(!criterion)return;
  document.getElementById('search').value='';
  document.querySelector('[data-filter="all"]').click();
  const card=[...document.querySelectorAll('.card')].find(c=>c.querySelector('.id').textContent===criterion.n);
  if(!card)return; card.classList.add('open');
  if(type==='crumb'){
    const details=[...card.querySelectorAll('.crumbItem')].find(c=>c.querySelector('.crumbLink').textContent===id);
    if(details){details.closest('.crumbTrace').open=true;details.open=true;details.scrollIntoView({block:'center'});}
  }else card.scrollIntoView({block:'start'});
}
window.addEventListener('hashchange',openDeliveryReference);openDeliveryReference();
</script>'''


def prepare(root, run_id, light, dark):
    root = Path(root).absolute()
    paths = [safe(root,p) for p in [root/'db/nqa_audit.sqlite', root/'manifests/approvals.csv',
                                   root/'schemas/scoring_model.yml', root/'project-state.yml', light,dark]]
    before = {p:sha(p.read_bytes()) for p in paths}
    import yaml
    state = yaml.safe_load(paths[3].read_text(encoding='utf-8'))
    package = build_package(paths[0], run_id, paths[1])
    if validate_package(package):
        raise ValueError('Invalid canonical evaluation package')
    if any(f'{g}-{run_id}' not in approved_ids(package) for g in ('G2','G3')):
        raise ValueError('Local G2/G3 approval required for a scored documentary export')
    light_text, dark_text = paths[4].read_text(encoding='utf-8'), paths[5].read_text(encoding='utf-8')
    data = dashboard_data(light_text)
    if dashboard_data(dark_text) != data:
        raise ValueError('Dark and light audit data differ')
    check_projection(data, package['evaluations'])
    supplier = package['run']['supplier']
    if state['supplier'].casefold() != supplier.casefold():
        raise ValueError('State and evaluation supplier mismatch')
    if not re.fullmatch(r'[\w -]{1,80}', supplier):
        raise ValueError('Unsafe supplier file stem')
    for text in [light_text,dark_text]:
        title = re.search(r'<title>(.*?)</title>',text,re.S|re.I)
        if title and supplier.casefold() not in html.unescape(title.group(1)).casefold():
            raise ValueError('Dashboard title and local supplier differ')
    with sqlite3.connect(paths[0].as_uri()+'?mode=ro',uri=True) as conn:
        conn.row_factory = sqlite3.Row
        active_counts = dict(conn.execute('SELECT document_side,count(*) FROM active_crumbs GROUP BY document_side'))
        crumbs, quotes, chapters, documents, links = {}, {}, {}, {}, []
        for d in data:
            for display in d['score_crumbs']:
                id = display['id']
                c = conn.execute("SELECT * FROM active_crumbs WHERE item_id=? AND document_side='DOCUMENT'",(id,)).fetchone()
                if not c or c['criterion_id'] != 'APP_B_'+d['n']:
                    raise ValueError('Inactive/foreign score crumb: '+id)
                crumbs[id] = dict(c)
                expected_quotes = [dict(q) for q in conn.execute('SELECT * FROM crumb_quotes WHERE item_id=?',(id,))]
                if {q['quote_id']:q['quote_original'] for q in expected_quotes} != {q['quote_id']:q['text'] for q in display['quotes']}:
                    raise ValueError('Quote projection mismatch: '+id)
                expected_chapters = set()
                for q in expected_quotes:
                    quotes[q['quote_id']] = q
                    found = conn.execute('SELECT * FROM crumb_chunk_links WHERE item_id=? AND quote_id=?',(id,q['quote_id'])).fetchall()
                    if not found:
                        raise ValueError('Unlinked score quote: '+q['quote_id'])
                    for l in found:
                        ch = dict(conn.execute('SELECT * FROM document_chunks WHERE chunk_id=?',(l['chunk_id'],)).fetchone())
                        doc = dict(conn.execute('SELECT * FROM documents WHERE doc_id=?',(ch['doc_id'],)).fetchone())
                        if ch['doc_id'] != c['doc_id'] or q['quote_original'] not in ch['chunk_text']:
                            raise ValueError('Non-exact/cross-document quote: '+q['quote_id'])
                        if ch['source_sha256'] != doc['sha256']:
                            raise ValueError('Broken chapter hash chain: '+ch['chunk_id'])
                        raw = safe(root, root/'raw'/doc['filename'])
                        if raw not in before:
                            before[raw] = sha(raw.read_bytes())
                        if before[raw] != doc['sha256'] or raw.read_text(encoding='utf-8')[ch['char_start']:ch['char_end']] != ch['chunk_text']:
                            raise ValueError('Raw source/chapter range mismatch: '+ch['chunk_id'])
                        expected_chapters.add(ch['chunk_id'])
                        chapters[ch['chunk_id']], documents[doc['doc_id']] = ch,doc
                        links.append(dict(l))
                displayed = {ch['chunk_id']:ch['text'] for ch in display['chapters']}
                if set(displayed) != expected_chapters or any(displayed[k] != chapters[k]['chunk_text'] for k in displayed):
                    raise ValueError('Chapter projection mismatch: '+id)
    counts = dict(crumbs=len(crumbs), quotes=len(quotes), chapters=len(chapters), documents=len(documents))
    bundle = dict(schema_version='documentary-delivery-1', run_id=run_id, counts=counts,
                  documents=list(documents.values()), chapters=list(chapters.values()),
                  crumbs=list(crumbs.values()), quotes=list(quotes.values()),
                  links={json.dumps(l,sort_keys=True):l for l in links})
    bundle['links'] = list(bundle['links'].values())
    stem = supplier.casefold().replace(' ','_')+'_appendix_b'
    name = {k:stem+'_'+suffix for k,suffix in dict(package='evaluation_package.json',
            report='evaluation_report.md', data='dashboard_data.json', light='dashboard.html',
            dark='dashboard_dark.html').items()}
    def linked(text):
        if text.count('</body>') != 1:
            raise ValueError('Expected one dashboard body')
        return text.replace('</body>', HASH_SCRIPT+'\n</body>').encode('utf-8')
    files = {name['package']:encoded(package),name['data']:encoded(data),name['light']:linked(light_text),
             name['dark']:linked(dark_text),'evidence_bundle.json':encoded(bundle),
             name['report']:render_documentary_export(package,data,name['light']).encode('utf-8')}
    portable = 'portable_package/'+run_id+'/'
    for key,target in [('package','evaluation_package.json'),('data','dashboard_data.json'),
                       ('light','evidence_explorer.html'),('dark','evidence_explorer_dark.html')]:
        files[portable+target] = files[name[key]]
    files[portable+'evidence_bundle.json'] = files['evidence_bundle.json']
    files[portable+'evaluation_report.md'] = render_documentary_export(package,data,'evidence_explorer.html').encode('utf-8')
    catalog = dict(schema_version='documentary-delivery-1',run_id=run_id,supplier=supplier,
                   score=package['metrics']['consolidated_score'],artifacts={
                       'light':run_id+'/evidence_explorer.html','dark':run_id+'/evidence_explorer_dark.html',
                       'report':run_id+'/evaluation_report.md','package':run_id+'/evaluation_package.json',
                       'bundle':run_id+'/evidence_bundle.json'})
    files['portable_package/review_catalog.json'] = encoded(catalog)
    files['portable_package/review_workspace.html'] = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>'+html.escape(supplier)+' review workspace</title><style>body{font:18px/1.5 system-ui;max-width:800px;margin:3rem auto;padding:1rem}li{margin:1rem 0}</style>'
        '<h1>'+html.escape(supplier)+' — documentary review</h1><p>Score: '+str(catalog['score'])+'%. Prepared delivery; formal release gates unchanged.</p><ul>'+
        ''.join('<li><a href="'+html.escape(path)+'">'+html.escape(label)+'</a></li>' for label,path in catalog['artifacts'].items())+'</ul></html>').encode('utf-8')
    files['portable_package/package_manifest.json'] = encoded(dict(files=[
        dict(path=p.removeprefix('portable_package/'),sha256=sha(b),bytes=len(b))
        for p,b in sorted(files.items()) if p.startswith('portable_package/')]))
    files['README.md'] = (f'# {supplier} documentary delivery\n\nOpen portable_package/review_workspace.html.\n\n'
        'All evidence is embedded; no database or web service is needed. Copy the entire folder.\n'
        'Stored scores and quotations are preserved. This is a prepared candidate, not formal G5/G6 publication.\n'
        'The existing English presentation is retained. Raw source and database files are not distributed.\n').encode('utf-8')
    if any(sha(p.read_bytes()) != h for p,h in before.items()):
        raise ValueError('Input changed during preparation; no delivery allowed')
    proof = dict(schema_version=1,state='prepared',run_id=run_id,supplier=supplier,
                 score=package['metrics']['consolidated_score'],score_points=sum(d['score'] for d in data),
                 score_crumbs=len(crumbs),evidence_counts=counts,active_crumb_counts=active_counts,
                 formal_gate_status={k:v['status'] for k,v in state['gates'].items()},
                 review_status='pending',input_hashes={str(p.relative_to(root)).replace('\\','/'):h for p,h in before.items()},
                 generator_sha256=sha(Path(__file__).read_bytes()),
                 scope='Read-only documentary candidate export; no source, DB, approval or gate writes')
    return proof, files


def write_exclusive(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def write_new(output, files, proof):
    output = Path(output)
    output.mkdir(parents=True,exist_ok=False)
    created = []
    manifest = dict(proof,files=[dict(path=p,sha256=sha(b),bytes=len(b)) for p,b in sorted(files.items())])
    try:
        for name,data in [*sorted(files.items()),('release_manifest.json',encoded(manifest))]:
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts or '\\' in name:
                raise ValueError('Unsafe artifact path')
            path = output/relative
            safe(output,path)
            path.parent.mkdir(parents=True,exist_ok=True)
            safe(output,path)
            write_exclusive(path,data)
            created.append((path,sha(data)))
        verify(output)
    except Exception:
        # Only unchanged files created by this run; never recursive deletion.
        for path,digest in reversed(created):
            if path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == digest:
                path.unlink()
        raise
    return manifest


def verify(output):
    output = Path(output).absolute()
    safe(output,output)
    manifest = json.loads((output/'release_manifest.json').read_text(encoding='utf-8'))
    expected = {'release_manifest.json'}
    for row in manifest['files']:
        path = safe(output,output/row['path'])
        if row['path'] in expected or path.stat().st_size != row['bytes'] or sha(path.read_bytes()) != row['sha256']:
            raise ValueError('Delivery file hash/size mismatch: '+row['path'])
        expected.add(row['path'])
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError('Delivery file inventory mismatch')
    return dict(passed=True,files=len(manifest['files']),state=manifest.get('state'),score=manifest.get('score'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id')
    parser.add_argument('--light',type=Path)
    parser.add_argument('--dark',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--verify',type=Path)
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(safe(ROOT,args.verify))))
        return 0
    if not all([args.run_id,args.light,args.dark,args.output]):
        parser.error('--run-id, --light, --dark and --output required')
    output = candidate_path(ROOT,args.output,args.run_id)
    proof,files = prepare(ROOT,args.run_id,args.light,args.dark)
    if args.apply:
        manifest = write_new(output,files,proof)
        print(json.dumps(dict(mode='prepared',output=str(output),files=len(manifest['files']),score=proof['score'])))
    else:
        print(json.dumps(dict(mode='preview',output=str(output),files=len(files),bytes=sum(map(len,files.values())),**proof),ensure_ascii=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
