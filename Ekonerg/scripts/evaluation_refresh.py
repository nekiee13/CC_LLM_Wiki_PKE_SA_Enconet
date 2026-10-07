"""Preview/apply an evidence-preserving documentation reassessment.

No source, crumb, evidence link, applicability or scoring-model value changes.
The previous results are retained in immutable history and a hash-bound journal.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3

import yaml
from evaluation_engine import DIMENSIONS, RATINGS, SUMMARIES, metrics, score_rating
from source_revision_intake import approval, encoded, insert, local, read_json, sha, write_new
from source_revision_promote import FIVE, SCHEMA, rows

ROOT = Path(__file__).resolve().parents[1]


def snapshot(c, run):
    meta = c.execute('SELECT * FROM evaluation_runs WHERE run_id=?', (run,)).fetchone()
    if not meta:
        raise ValueError('evaluation run missing')
    return {
        'run': dict(meta),
        'evaluations': rows(c, 'SELECT * FROM criterion_evaluations WHERE evaluation_run_id=? ORDER BY criterion_id', (run,)),
        'evidence': rows(c, 'SELECT e.* FROM evaluation_evidence e JOIN criterion_evaluations v USING(evaluation_id) WHERE v.evaluation_run_id=? ORDER BY evaluation_id,item_id', (run,)),
    }


def prepare(root, assessment):
    root = Path(root).resolve()
    db = local(root, 'db/nqa_audit.sqlite')
    digest = sha(db.read_bytes())
    inputs = {}

    def bind(path):
        p = local(root, path)
        inputs[p.relative_to(root).as_posix()] = sha(p.read_bytes())
        return p

    config_path = bind(assessment)
    cfg = read_json(config_path)
    run, revision, decision = cfg['run_id'], cfg['revision_id'], cfg['decision_ref']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}', revision):
        raise ValueError('invalid revision ID')
    bind('manifests/approvals.csv')
    for ref in (decision, 'G2-' + run, 'G3-' + run):
        approval(root, ref)
    rubric_path = bind(cfg['methodology'])
    if not rubric_path.read_text(encoding='utf-8').strip():
        raise ValueError('documentation methodology missing')
    model = yaml.safe_load(bind('schemas/scoring_model.yml').read_text(encoding='utf-8'))
    with local(root, 'manifests/approvals.csv').open(encoding='utf-8-sig', newline='') as f:
        g3 = next(r for r in csv.DictReader(f) if r['object_id'] == 'G3-' + run)
    if (model.get('calibration_status') != 'approved' or model.get('approval_ref') != 'G3-' + run
            or not model.get('model_version') or 'placeholder' in model['model_version'].lower()
            or model['model_version'] not in g3['notes']):
        raise ValueError('approved model version required')
    weights = model['rating_weights']
    if set(weights) != RATINGS or weights['na'] is not None or any(
            type(weights[r]) not in (int, float) or not 0 <= weights[r] <= 1 for r in RATINGS - {'na'}):
        raise ValueError('invalid model weights')
    baseline = read_json(bind(cfg['baseline']))
    if baseline['run_id'] != run:
        raise ValueError('baseline run mismatch')
    changes = cfg['changes']
    if not changes or len({r['criterion_id'] for r in changes}) != len(changes):
        raise ValueError('unique non-empty changes required')

    with closing(sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)) as c:
        c.row_factory = sqlite3.Row
        before = snapshot(c, run)
        if before['run']['scoring_model_version'] != model['model_version']:
            raise ValueError('run model mismatch')
        criteria = {r[0] for r in c.execute('SELECT criterion_id FROM criteria')}
        previous = {r['criterion_id']: r for r in before['evaluations']}
        base = {r['criterion_id']: r for r in baseline['evaluations']}
        if len(criteria) != 18 or set(previous) != criteria or len(before['evaluations']) != 18 or set(base) != criteria or len(baseline['evaluations']) != 18:
            raise ValueError('exactly 18 baseline/current assessments required')
        for cid, prior in previous.items():
            if any(prior[k] != base[cid][k] for k in ('rating', *SUMMARIES)):
                raise ValueError('baseline differs from live assessment')
            if prior['score'] != score_rating(prior['rating'], scoring_model=model):
                raise ValueError('existing score differs from approved model')
            ruling = c.execute('SELECT * FROM criterion_applicability WHERE evaluation_run_id=? AND criterion_id=?', (run, cid)).fetchone()
            if not ruling or not ruling['applicable'] or (ruling['applicability_state'] == 'conditional' and not ruling['conditional_confirmation_ref']):
                raise ValueError('applicability not confirmed')
            if ruling['conditional_confirmation_ref']:
                approval(root, ruling['conditional_confirmation_ref'])
        for table in ('gaps', 'findings', 'auditor_actions'):
            if c.execute('SELECT count(*) FROM ' + table).fetchone()[0]:
                raise ValueError('downstream records need reconciliation')
        if c.execute("SELECT 1 FROM sqlite_master WHERE name='evaluation_revisions'").fetchone() and c.execute('SELECT 1 FROM evaluation_revisions WHERE revision_id=?', (revision,)).fetchone():
            raise ValueError('revision already exists; use original apply plan for retry')
        raw_text = {}
        for doc in rows(c, 'SELECT * FROM documents'):
            raw = bind('raw/' + doc['filename']).read_bytes()
            if sha(raw) != doc['sha256']:
                raise ValueError('registered source hash changed')
            raw_text[doc['doc_id']] = raw.decode('utf-8-sig')
        for link in before['evidence']:
            crumb = c.execute('SELECT a.*,x.evidence_type FROM active_crumbs a LEFT JOIN crumb_context x USING(item_id) WHERE a.item_id=?', (link['item_id'],)).fetchone()
            cid = next(r['criterion_id'] for r in previous.values() if r['evaluation_id'] == link['evaluation_id'])
            if not crumb or crumb['document_side'] != 'DOCUMENT' or crumb['criterion_id'] != cid or crumb['evidence_type'] == 'candidate_lead' or crumb['statement'].startswith('candidate_lead:'):
                raise ValueError('score evidence must be active same-criterion vendor control')
            quotes = rows(c, 'SELECT * FROM crumb_quotes WHERE item_id=?', (link['item_id'],))
            if not quotes:
                raise ValueError('linked crumb lacks quotes')
            for q in quotes:
                chapters = rows(c, 'SELECT ch.* FROM crumb_chunk_links l JOIN document_chunks ch USING(chunk_id) WHERE l.item_id=? AND l.quote_id=?', (link['item_id'], q['quote_id']))
                if not chapters or not q['quote_original']:
                    raise ValueError('linked quote lacks chapter')
                for ch in chapters:
                    if ch['doc_id'] != crumb['doc_id'] or q['quote_original'] not in ch['chunk_text'] or ch['chunk_text'] != raw_text[ch['doc_id']][ch['char_start']:ch['char_end']] or ch['source_sha256'] != sha(bind('raw/' + c.execute('SELECT filename FROM documents WHERE doc_id=?', (ch['doc_id'],)).fetchone()[0]).read_bytes()):
                        raise ValueError('quote/chapter/source mismatch')
        after = json.loads(json.dumps(before))
        targets = {r['criterion_id']: r for r in after['evaluations']}
        for change in changes:
            cid = change['criterion_id']
            if cid not in targets or change['rating'] not in FIVE:
                raise ValueError('change must name valid criterion and five-level rating')
            selected = {r['item_id'] for r in before['evidence'] if r['evaluation_id'] == targets[cid]['evaluation_id']}
            basis = change['basis_crumb_ids']
            if not basis or len(basis) != len(set(basis)) or not set(basis) <= selected:
                raise ValueError('change basis must cite linked active vendor controls')
            for field in SUMMARIES:
                if not isinstance(change.get(field), str) or not change[field].strip():
                    raise ValueError('change explanations required')
            score = score_rating(change['rating'], scoring_model=model)
            targets[cid].update(rating=change['rating'], score=score,
                                **{k: change[k].strip() for k in SUMMARIES},
                                **{k: score / 100 for k in DIMENSIONS})
        active = rows(c, 'SELECT run_id,doc_id,status,is_active FROM sieve_runs WHERE is_active=1 ORDER BY run_id')
        vendor_count = c.execute("SELECT count(*) FROM active_crumbs WHERE document_side='DOCUMENT'").fetchone()[0]
    if sha(db.read_bytes()) != digest:
        raise ValueError('database changed during preview')
    return {'schema': 'evaluation_refresh/1', 'root': str(root), 'assessment': config_path.relative_to(root).as_posix(),
            'database_sha256': digest, 'inputs': inputs, 'run_id': run, 'revision_id': revision,
            'decision_ref': decision, 'before': before, 'after': after,
            'active_generations': active, 'active_vendor': vendor_count,
            'metrics': metrics(after['evaluations'], scoring_model=model)}


def apply(root, plan, output, *, before_commit=None):
    root = Path(root).resolve()
    output = local(root, output)
    db = local(root, 'db/nqa_audit.sqlite')
    if output == root / 'out' or not output.is_relative_to(root / 'out'):
        raise ValueError('journal must be beneath project out')
    digest = sha(encoded(plan))
    if (output / 'completed.json').exists():
        receipt = read_json(output / 'completed.json')
        if (receipt['plan_sha256'] != digest or receipt['revision_id'] != plan['revision_id']
                or receipt['metrics'] != plan['metrics'] or receipt['active_vendor'] != plan['active_vendor']):
            raise ValueError('retry plan changed')
        with closing(sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)) as c:
            c.row_factory = sqlite3.Row
            event = c.execute('SELECT * FROM evaluation_revisions WHERE revision_id=?', (plan['revision_id'],)).fetchone()
            if not event or event['decision_ref'] != plan['decision_ref'] or json.loads(event['before_json']) != plan['before'] or json.loads(event['after_json']) != plan['after'] or snapshot(c, plan['run_id']) != plan['after']:
                raise ValueError('retry history/current assessment mismatch')
            if rows(c, 'SELECT run_id,doc_id,status,is_active FROM sieve_runs WHERE is_active=1 ORDER BY run_id') != plan['active_generations']:
                raise ValueError('retry active evidence state mismatch')
        for name, value in receipt['journal_hashes'].items():
            if sha(local(root, output / name).read_bytes()) != value:
                raise ValueError('journal changed')
        return {**receipt, 'status': 'already_applied'}
    if output.exists():
        raise ValueError('incomplete journal; inspect history before recovery')
    if prepare(root, plan['assessment']) != plan:
        raise ValueError('preview is stale or altered')
    with closing(sqlite3.connect(db.as_uri() + '?mode=rw', uri=True)) as c:
        c.row_factory = sqlite3.Row
        c.execute('PRAGMA foreign_keys=ON')
        c.execute('BEGIN IMMEDIATE')
        if sha(db.read_bytes()) != plan['database_sha256'] or any(sha(local(root, p).read_bytes()) != h for p, h in plan['inputs'].items()):
            raise ValueError('database or input changed before transaction')
        output.mkdir(parents=True, exist_ok=False)
        write_new(output / 'intent.json', encoded(plan))
        write_new(output / 'before.json', encoded(plan['before']))
        try:
            for sql in SCHEMA:
                if 'evaluation_revisions' in sql:
                    c.execute(sql)
            insert(c, 'evaluation_revisions', {'revision_id': plan['revision_id'], 'evaluation_run_id': plan['run_id'],
                   'decision_ref': plan['decision_ref'], 'before_json': encoded(plan['before']).decode(),
                   'after_json': encoded(plan['after']).decode(), 'recorded_at': datetime.now(timezone.utc).isoformat()})
            for row in plan['after']['evaluations']:
                keys = ['rating', 'score', *SUMMARIES, *DIMENSIONS]
                c.execute('UPDATE criterion_evaluations SET ' + ','.join(k + '=?' for k in keys) + ' WHERE evaluation_id=? AND evaluation_run_id=?', [row[k] for k in keys] + [row['evaluation_id'], plan['run_id']])
            if snapshot(c, plan['run_id']) != plan['after'] or rows(c, 'SELECT run_id,doc_id,status,is_active FROM sieve_runs WHERE is_active=1 ORDER BY run_id') != plan['active_generations'] or c.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('assessment or evidence state mismatch')
            if before_commit:
                before_commit()
            c.commit()
        except Exception:
            c.rollback()
            write_new(output / 'failed.json', encoded({'status': 'rolled_back'}))
            raise
    receipt = {'status': 'completed', 'revision_id': plan['revision_id'], 'active_vendor': plan['active_vendor'],
               'plan_sha256': digest, 'database_before_sha256': plan['database_sha256'],
               'database_after_sha256': sha(db.read_bytes()), 'metrics': plan['metrics'],
               'journal_hashes': {n: sha((output / n).read_bytes()) for n in ('intent.json', 'before.json')}}
    write_new(output / 'completed.json', encoded(receipt))
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, default=ROOT)
    p.add_argument('--assessment')
    p.add_argument('--apply-plan')
    p.add_argument('--output', required=True)
    a = p.parse_args()
    root = a.project.resolve()
    if a.apply_plan:
        result = apply(root, read_json(local(root, a.apply_plan)), a.output)
    else:
        result = prepare(root, a.assessment)
        write_new(local(root, a.output), encoded(result))
    print(json.dumps({k: result[k] for k in ('metrics', 'active_vendor', 'revision_id')} | {'status': result.get('status', 'preview')}))


if __name__ == '__main__':
    main()
