"""A rating correction must not mutate the evidence or lose the old result."""
import json
import sqlite3

import pytest

from test_source_revision_promote import ready
from test_source_revision_intake import inventory, sample
import source_revision_promote as promote
import evaluation_refresh as refresh


@pytest.fixture
def current(ready):
    root = ready
    promote.apply(root, promote.prepare(root, 'assessment.json'), 'out/promotion')
    with (root / 'manifests/approvals.csv').open('a') as f:
        f.write('REASSESS,approved,2026-10-07,Owner,Fair document review\n')
    (root / 'rubric.md').write_text('Score the written controls, not absent field samples.')
    baseline = json.loads((root / 'assessment.json').read_text())
    change = next(r.copy() for r in baseline['evaluations'] if r['criterion_id'] == 'APP_B_XVII')
    with sqlite3.connect(root / 'db/nqa_audit.sqlite') as c:
        basis = [r[0] for r in c.execute("SELECT item_id FROM evaluation_evidence WHERE evaluation_id='EVAL-APP_B_XVII'")]
    c.close()
    change.update(rating='fully', basis_crumb_ids=basis, rationale='Written record control covers the applicable duty.')
    cfg = {'run_id': baseline['run_id'], 'revision_id': 'REVIEW-1', 'decision_ref': 'REASSESS',
           'baseline': 'assessment.json', 'methodology': 'rubric.md', 'changes': [change]}
    (root / 'refresh.json').write_text(json.dumps(cfg))
    return root


def test_preview_apply_retry_history_and_no_evidence_mutation(current):
    root = current
    before = inventory(root)
    plan = refresh.prepare(root, 'refresh.json')
    assert inventory(root) == before
    assert plan['after']['evidence'] == plan['before']['evidence']
    result = refresh.apply(root, plan, 'out/review')
    assert result['metrics']['classification_counts']['fully'] == 1
    assert refresh.apply(root, plan, 'out/review')['status'] == 'already_applied'
    assert (root / 'raw/old.md').read_bytes() == before['raw/old.md']
    with sqlite3.connect(root / 'db/nqa_audit.sqlite') as c:
        old, new = c.execute("SELECT before_json,after_json FROM evaluation_revisions WHERE revision_id='REVIEW-1'").fetchone()
        assert next(r for r in json.loads(old)['evaluations'] if r['criterion_id'] == 'APP_B_XVII')['rating'] == 'partially'
        assert next(r for r in json.loads(new)['evaluations'] if r['criterion_id'] == 'APP_B_XVII')['rating'] == 'fully'
        assert c.execute("SELECT is_active FROM sieve_runs WHERE run_id='RUN-20261006-99'").fetchone()[0] == 1
        with pytest.raises(sqlite3.IntegrityError, match='immutable'):
            c.execute("DELETE FROM evaluation_revisions WHERE revision_id='REVIEW-1'")


@pytest.mark.parametrize('defect', ['approval', 'raw', 'quote', 'stale', 'baseline', 'basis', 'rating', 'model', 'escape', 'summary', 'incomplete', 'duplicate'])
def test_fail_closed(current, defect):
    root = current
    plan = refresh.prepare(root, 'refresh.json')
    cfg = json.loads((root / 'refresh.json').read_text())
    if defect == 'approval':
        (root / 'manifests/approvals.csv').write_text('object_id,decision,date,reviewer,notes\n')
    if defect == 'raw':
        (root / 'raw/old.md').write_bytes(b'altered')
    if defect in ('quote', 'stale'):
        with sqlite3.connect(root / 'db/nqa_audit.sqlite') as c:
            if defect == 'quote': c.execute("UPDATE crumb_quotes SET quote_original='invented'")
            else: c.execute("UPDATE documents SET title='changed'")
    if defect == 'baseline':
        baseline = json.loads((root / 'assessment.json').read_text())
        baseline['evaluations'][0]['rating'] = 'fully'
        (root / 'assessment.json').write_text(json.dumps(baseline))
    if defect == 'basis': cfg['changes'][0]['basis_crumb_ids'] = ['invented']
    if defect == 'rating': cfg['changes'][0]['rating'] = 'undetermined'
    if defect == 'summary': cfg['changes'][0]['judge_ruling'] = ''
    if defect == 'duplicate': cfg['changes'] *= 2
    if defect == 'model': (root / 'schemas/scoring_model.yml').write_text('calibration_status: pending\n')
    if defect == 'escape': plan['assessment'] = '../outside.json'
    if defect == 'incomplete': (root / 'out/review').mkdir()
    (root / 'refresh.json').write_text(json.dumps(cfg))
    before = inventory(root)
    with pytest.raises((ValueError, KeyError, StopIteration)):
        refresh.apply(root, plan, 'out/review')
    assert inventory(root) == before


def test_rollback_and_block_uninspected_retry(current):
    root = current
    plan = refresh.prepare(root, 'refresh.json')
    def fail(): raise RuntimeError('injected')
    with pytest.raises(RuntimeError, match='injected'):
        refresh.apply(root, plan, 'out/review', before_commit=fail)
    with sqlite3.connect(root / 'db/nqa_audit.sqlite') as c:
        c.row_factory = sqlite3.Row
        assert refresh.snapshot(c, plan['run_id']) == plan['before']
        assert not c.execute("SELECT 1 FROM evaluation_revisions WHERE revision_id='REVIEW-1'").fetchone()
    with pytest.raises(ValueError, match='journal'):
        refresh.apply(root, plan, 'out/review')


def test_all18_present_tense_reassessment_preserves_evidence(current):
    root = current
    cfg = json.loads((root / 'refresh.json').read_text())
    baseline = json.loads((root / 'assessment.json').read_text())
    with sqlite3.connect(root / 'db/nqa_audit.sqlite') as c:
        c.row_factory = sqlite3.Row
        template = dict(c.execute('SELECT * FROM active_crumbs').fetchone())
        quote = dict(c.execute('SELECT * FROM crumb_quotes WHERE item_id=?', (template['item_id'],)).fetchone())
        link = dict(c.execute('SELECT * FROM crumb_chunk_links WHERE item_id=?', (template['item_id'],)).fetchone())
        cfg['changes'] = []
        for row in baseline['evaluations']:
            change = {k: row[k] for k in ('criterion_id', 'rating', *refresh.SUMMARIES)}
            change['rationale'] = 'The written controls cover the stated duty, with the described limits.'
            change['basis_crumb_ids'] = [r[0] for r in c.execute(
                'SELECT item_id FROM evaluation_evidence WHERE evaluation_id=?',
                ('EVAL-' + row['criterion_id'],))]
            if not change['basis_crumb_ids']:
                # Synthetic controls give every fixture criterion an exact linked quote.
                item = 'TEST-' + row['criterion_id']
                crumb = {k: template[k] for k in ('doc_id', 'sieve_run_id', 'document_side', 'statement', 'item_type', 'quote_language')}
                refresh.insert(c, 'crumbs', {**crumb, 'item_id': item, 'criterion_id': row['criterion_id']})
                refresh.insert(c, 'crumb_quotes', {**quote, 'quote_id': item + '-Q', 'item_id': item})
                refresh.insert(c, 'crumb_chunk_links', {**link, 'quote_id': item + '-Q', 'item_id': item})
                refresh.insert(c, 'evaluation_evidence', {'evaluation_id': 'EVAL-' + row['criterion_id'], 'item_id': item})
                change['basis_crumb_ids'] = [item]
            cfg['changes'].append(change)
    (root / 'refresh.json').write_text(json.dumps(cfg))
    plan = refresh.prepare(root, 'refresh.json')
    assert len(plan['after']['evaluations']) == 18
    assert plan['after']['evidence'] == plan['before']['evidence']
    result = refresh.apply(root, plan, 'out/all18')
    assert result['metrics'] == plan['metrics']
    assert refresh.apply(root, plan, 'out/all18')['status'] == 'already_applied'


def test_published_all18_review_explains_current_controls_not_change_history():
    from pathlib import Path
    path = Path(__file__).resolve().parents[2] / 'docs/reviews/ALL18_ASSESSMENT_20261007.json'
    cfg = json.loads(path.read_text(encoding='utf-8'))
    assert len(cfg['changes']) == 18
    assert len({r['criterion_id'] for r in cfg['changes']}) == 18
    for row in cfg['changes']:
        assert row['basis_crumb_ids']
        for field in refresh.SUMMARIES:
            value = row[field].lower()
            assert value.strip()
            assert not any(word in value for word in ('raise ', 'retain ', 'previous deduction', 'earlier score', 'lower ', 'old score'))


@pytest.mark.parametrize('name', ['New Company', 'Čista tvrtka'])
@pytest.mark.parametrize('sibling', [True, False])
def test_neutral_root(current, name, sibling):
    root = current
    new = root.with_name(name)
    root.rename(new)
    other = new.with_name('Other Company')
    if sibling:
        other.mkdir()
        (other / 'keep').write_text('unchanged')
    refresh.apply(new, refresh.prepare(new, 'refresh.json'), 'out/review')
    if sibling:
        assert (other / 'keep').read_text() == 'unchanged'
