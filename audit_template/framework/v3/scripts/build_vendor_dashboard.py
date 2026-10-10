"""Render a separate light dashboard from this company's recorded audit.

Read-only: never writes scores, sources, approvals, or published dashboards.
The run ID is required. No other company's project is read at runtime.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import html
import json
from pathlib import Path
import sqlite3

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROMANS = 'I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII'.split()
POINTS = dict(fully=5, substantially=4, partially=3, minimally=2, unmet=1)


def dataset(root: Path, run_id: str) -> dict:
    root = root.resolve(strict=True)
    db = root / 'db/nqa_audit.sqlite'
    # mode=ro also prevents SQLite from creating a missing database.
    with sqlite3.connect(db.resolve(strict=True).as_uri() + '?mode=ro', uri=True) as conn:
        conn.row_factory = sqlite3.Row
        run = conn.execute('SELECT * FROM evaluation_runs WHERE run_id=?', (run_id,)).fetchone()
        if run is None:
            raise ValueError('Requested evaluation run does not exist')
        evaluations = {r['criterion_id']: r for r in conn.execute(
            'SELECT e.*, c.criterion_name FROM criterion_evaluations e JOIN criteria c '
            'ON c.criterion_id=e.criterion_id WHERE evaluation_run_id=?', (run_id,))}
        if set(evaluations) != {'APP_B_' + n for n in ROMANS}:
            raise ValueError('The run must contain all 18 criterion records')
        applicability = {r['criterion_id']: r for r in conn.execute(
            'SELECT * FROM criterion_applicability WHERE evaluation_run_id=?', (run_id,))}
        if set(applicability) != set(evaluations) or any(not r['decision_ref'] for r in applicability.values()):
            raise ValueError('All applicability decisions must be recorded')
        model = yaml.safe_load((root / 'schemas/scoring_model.yml').read_text(encoding='utf-8'))
        data = []
        for order, roman in enumerate(ROMANS, 1):
            cid = 'APP_B_' + roman
            e = evaluations[cid]
            applicable = bool(applicability[cid]['applicable'])
            rating = e['rating']
            if (applicable and rating not in POINTS) or (not applicable and rating != 'na'):
                raise ValueError('Unruled or undetermined ratings cannot be presented as completed results')
            expected = 100 * model['rating_weights'][rating] if applicable else None
            if applicable and float(e['score']) != expected:
                raise ValueError('Stored score does not match the local scoring model: ' + cid)
            linked = conn.execute(
                'SELECT c.item_id,c.doc_id,d.filename,q.quote_id,q.quote_original,q.source_locator,'
                'ch.chunk_id,ch.heading_path,ch.chunk_text,ch.doc_id AS chapter_doc_id '
                'FROM evaluation_evidence x JOIN active_crumbs c ON c.item_id=x.item_id '
                'JOIN documents d ON d.doc_id=c.doc_id '
                'LEFT JOIN crumb_quotes q ON q.item_id=c.item_id '
                'LEFT JOIN crumb_chunk_links l ON l.item_id=q.item_id AND l.quote_id=q.quote_id '
                'LEFT JOIN document_chunks ch ON ch.chunk_id=l.chunk_id '
                'WHERE x.evaluation_id=? AND c.document_side=\'DOCUMENT\' '
                'ORDER BY c.item_id,q.quote_id,ch.chunk_id', (e['evaluation_id'],)).fetchall()
            total_support = conn.execute(
                'SELECT count(*) FROM evaluation_evidence WHERE evaluation_id=?', (e['evaluation_id'],)).fetchone()[0]
            crumbs = {}
            for row in linked:
                if (not row['chunk_id'] or not row['quote_original'] or
                        row['doc_id'] != row['chapter_doc_id'] or
                        row['quote_original'] not in row['chunk_text']):
                    raise ValueError('Score evidence requires an exact same-document chapter link: ' + row['item_id'])
                crumb = crumbs.setdefault(row['item_id'], dict(id=row['item_id'], doc_id=row['doc_id'],
                    filename=row['filename'], quotes=[], chapters=[]))
                if row['quote_id'] not in {q['quote_id'] for q in crumb['quotes']}:
                    crumb['quotes'].append(dict(quote_id=row['quote_id'], text=row['quote_original'], locator=row['source_locator']))
                if row['chunk_id'] not in {c['chunk_id'] for c in crumb['chapters']}:
                    crumb['chapters'].append(dict(chunk_id=row['chunk_id'], heading_path=row['heading_path'], text=row['chunk_text']))
            if len(crumbs) != total_support:
                raise ValueError('Support links include inactive or non-vendor evidence: ' + cid)
            if rating in ('fully', 'substantially') and not crumbs:
                raise ValueError('Positive rating lacks linked vendor evidence: ' + cid)
            count = conn.execute('SELECT count(*) FROM active_crumbs WHERE document_side=\'DOCUMENT\' AND criterion_id=?', (cid,)).fetchone()[0]
            actions = conn.execute(
                'SELECT DISTINCT a.action_id,a.description FROM auditor_actions a '
                'LEFT JOIN findings f ON f.finding_id=a.finding_id '
                'LEFT JOIN gaps g ON g.gap_id=a.gap_id '
                'LEFT JOIN criterion_evaluations ge ON ge.evaluation_id=g.evaluation_id '
                'WHERE a.evaluation_run_id=? AND (f.criterion_id=? OR ge.criterion_id=?) '
                'AND a.approval_status=\'approved\' ORDER BY a.action_id', (run_id,cid,cid)).fetchall()
            # Text inserted into existing innerHTML slots is escaped; quote/chapter
            # strings stay raw because their own renderer uses text escaping.
            esc = lambda value: html.escape(str(value or ''), quote=True)
            data.append(dict(n=roman, order=order, title=esc(e['criterion_name']), rating=rating,
                score=float(e['score']) if applicable else 0, scale_points=POINTS.get(rating, 'N/A'),
                applicable=applicable, summary=esc(e['rationale']), aff=esc(e['affirmative_summary']),
                con=esc(e['contrary_summary']), judge=esc(e['judge_ruling']),
                verify=esc('; '.join(r['description'] for r in actions) or e['contrary_summary']),
                vendor_count=count, crumbs=str(count) + ' vendor', score_crumb_count=len(crumbs),
                score_crumbs=list(crumbs.values()),
                score_trace=esc(f'{len(crumbs)} linked controls; recorded judgment: {rating}'),
                refs='Vendor crumbs: ' + ', '.join(crumbs) + '; source documents: ' + ', '.join(sorted({c['filename'] for c in crumbs.values()})),
                quote=esc(next((q['text'] for c in crumbs.values() for q in c['quotes']), 'No linked vendor quote'))))
        vendor_total = conn.execute('SELECT count(*) FROM active_crumbs WHERE document_side=\'DOCUMENT\'').fetchone()[0]
        docs = conn.execute('SELECT filename,sha256 FROM documents').fetchall()
    # Re-prove registered bytes before embedding their chapters in a new output.
    for doc in docs:
        raw = root / 'raw' / doc['filename']
        if not raw.resolve(strict=True).is_relative_to(root / 'raw'):
            raise ValueError('Registered source escapes local raw folder')
        if hashlib.sha256(raw.read_bytes()).hexdigest() != doc['sha256']:
            raise ValueError('Registered source hash mismatch: ' + doc['filename'])
    applicable_data = [d for d in data if d['applicable']]
    if not applicable_data:
        raise ValueError('No applicable criteria')
    total = sum(Decimal(str(d['score'])) for d in applicable_data)
    score = float((total / len(applicable_data)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
    return dict(supplier=run['supplier'], run_id=run_id, data=data, vendor_total=vendor_total,
        score=score, total_points=float(total), possible_points=100 * len(applicable_data),
        model_version=model['model_version'], language=run['deliverable_language'])


def render(payload: dict, template: Path, date: str, scope_note: str = '') -> str:
    data = payload['data']
    esc = html.escape
    supplier = esc(payload['supplier'])
    score = payload['score']
    counts = {r: sum(d['rating'] == r for d in data) for r in (*POINTS, 'na')}
    badges = ''.join(f'<button class="btn" data-filter="{r}">{r.title()} <span class="count">{counts[r]}</span></button>' for r in counts)
    segments = ''.join(f'<span>{r.title()}: {counts[r]}</span>' for r in counts)
    metrics = [(f'{score:.1f}%', 'Overall conformance', f"{payload['total_points']:g} / {payload['possible_points']} evidence points"),
        ('18', 'Appendix B criteria', 'All criteria visible'), (str(payload['vendor_total']), 'Vendor crumbs', 'Active local evidence'),
        (str(counts['fully']), 'Fully matched', '5 / 5'), (str(counts['substantially']), 'Substantially matched', '4 / 5'),
        (str(counts['unmet']), 'Unmet', '1 / 5')]
    topbar = ''.join(f'<div class="metric{ " main" if i == 0 else "" }"><div class="num">{a}</div><div class="label">{b}</div><div class="small">{c}</div></div>' for i, (a,b,c) in enumerate(metrics))
    gaps = ''.join(f'<li><strong>{d["n"]} — {d["title"]}:</strong> {d["con"]}</li>' for d in sorted(data,key=lambda d:d['score']) if d['applicable'] and d['score'] < 100)
    actions = ''.join(f'<li><strong>{d["n"]}:</strong> {d["verify"]}</li>' for d in sorted(data,key=lambda d:d['score']) if d['applicable'])
    values = dict(TITLE=f'{supplier} — 10 CFR 50 Appendix B Conformance Dashboard', SUPPLIER=supplier,
        METRICS=topbar, SCORE=f'{score:.1f}%', FILTERS=badges, DISTRIBUTION=segments,
        GAPS=gaps or '<li>No written gap is recorded.</li>', ACTIONS=actions,
        NOTE=esc(scope_note), DATE=esc(date), RUN=esc(payload['run_id']), MODEL=esc(payload['model_version']),
        DATA=json.dumps(data,ensure_ascii=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e'))
    text = template.read_text(encoding='utf-8')
    for key,value in values.items():
        text = text.replace('__' + key + '__', value)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--date', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--scope-note', default='', help='Explicit company-specific regulatory or audit limitation')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'out') or output.exists():
        parser.error('Use a NEW HTML file below this project out folder')
    before = hashlib.sha256((ROOT / 'db/nqa_audit.sqlite').read_bytes()).hexdigest()
    payload = dataset(ROOT, args.run_id)
    text = render(payload, ROOT / 'templates/vendor-dashboard.html', args.date, args.scope_note)
    if hashlib.sha256((ROOT / 'db/nqa_audit.sqlite').read_bytes()).hexdigest() != before:
        raise ValueError('Database changed while generating the snapshot')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(text)
    receipt = dict(supplier=payload['supplier'], run_id=args.run_id, score=payload['score'],
        criteria=len(payload['data']), vendor_crumbs=payload['vendor_total'], database_sha256=before,
        html_sha256=hashlib.sha256(output.read_bytes()).hexdigest(), output=str(output),
        publication_status='candidate; existing controlled results unchanged')
    with output.with_suffix('.provenance.json').open('x',encoding='utf-8') as stream:
        json.dump(receipt,stream,ensure_ascii=False,indent=2)
    print(json.dumps(receipt,ensure_ascii=False))


if __name__ == '__main__':
    from project_paths import configure_standard_streams
    configure_standard_streams()
    main()
