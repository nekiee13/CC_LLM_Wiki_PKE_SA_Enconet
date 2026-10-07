"""Contract checks for per-criterion summaries and score traceability."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_umbra_conformance_dashboard import DEFAULT_DB, DEFAULT_MATRIX, render


def test_radar_removal_keeps_page_startup():
    page = render(DEFAULT_MATRIX, DEFAULT_DB, "2026-10-06", "RUN-20261003-32")
    assert re.search(r"renderCards\(\);\s*renderMatrix\(\);\s*</script>", page)
    assert 'renderRadar();' not in page


def test_part21_boundary_is_visible_without_a_second_score():
    page = render(DEFAULT_MATRIX, DEFAULT_DB, "2026-10-07", "RUN-20261003-32")
    assert "Part 21 remains applicable" in page
    assert "not included in Criterion XVI or the overall Appendix B score" in page
    assert "reporting path remains unresolved" in page
    assert len(_data(page)) == 18


def test_published_all18_snapshot_matches_its_assessment():
    root = Path(__file__).resolve().parents[2]
    cfg = json.loads((root / 'docs/reviews/ALL18_ASSESSMENT_20261007.json').read_text(encoding='utf-8'))
    page = (root / 'out/2026-10-07/all18-review/EKONERG_DASHBOARD.html').read_text(encoding='utf-8')
    data = _data(page)
    assert len(data) == 18
    assert '77.8% — Substantially Matched' in page
    assert 'TEKOL' not in page
    assert 'Part 21 remains applicable' in page
    weights = {'fully': 100, 'substantially': 75, 'partially': 50, 'minimally': 25, 'unmet': 0}
    for row in cfg['changes']:
        card = next(d for d in data if 'APP_B_' + d['n'] == row['criterion_id'])
        assert card['rating'] == row['rating']
        assert card['score'] == weights[row['rating']]
        assert card['rationale'] == card['summary'] == row['rationale']
        assert card['aff'] == row['affirmative_summary']
        assert card['con'] == row['contrary_summary']
        assert card['judge'] == row['judge_ruling']
        assert set(row['basis_crumb_ids']) <= set(card['score_crumb_ids'])
        assert all(c['quotes'] and c['chapters'] for c in card['score_crumbs'])
    assert sum(d['score'] for d in data) == 1400
    assert sum(d['score_crumb_count'] for d in data) == 379


def _data(page: str) -> list[dict]:
    payload = re.search(r"const data = (\[.*?\]);\nconst labels=", page, re.S)
    assert payload is not None
    return json.loads(payload.group(1))


def test_collapsed_card_keeps_summary_but_hides_crumb_references() -> None:
    page = render(DEFAULT_MATRIX, DEFAULT_DB, "2026-10-07", "RUN-20261003-32")
    # The last definition is the one used by renderCards at page startup.
    card = page.rsplit('function cardHtml(d){', 1)[1].split('renderCards();', 1)[0]
    compact, expanded = card.split('<div class="cardBody">', 1)
    visible = compact.split('return `<article', 1)[1]
    assert '${d.summary}' in visible
    assert '${d.score_trace}' in visible
    assert '${d.refs}' not in visible
    assert '${esc(d.refs)}' not in visible
    assert '<div class="block criterionRefs">' in expanded
    assert '${esc(d.refs)}' in expanded
    assert '<details class="crumbTrace">' in expanded
    assert '${crumbs}' in expanded
    assert all(token in expanded for token in ('${d.aff}', '${d.con}', '${d.judge}', '${d.verify}', '${d.quote}'))
    assert '.cardBody{display:none' in page
    assert '.card.open .cardBody{display:block}' in page
    assert '.scoreTrace{flex-basis:100%}' in page
    assert '.cardBody{display:block!important}' in page  # Print still shows all details.


def test_cards_show_summary_and_crumbs_that_feed_score() -> None:
    page = render(DEFAULT_MATRIX, DEFAULT_DB, "2026-10-05", "RUN-20261003-32")
    data = _data(page)
    assert len(data) == 18
    assert "Criterion summary" in page
    assert "What full means:" in page
    assert "Missing work samples alone do not lower a documentation rating" in page
    assert "Crumbs linked to this score" in page
    assert "Source chapter:" in page
    assert "chapterText" in page
    assert "score_trace" in page
    with sqlite3.connect(DEFAULT_DB) as conn:
        expected = {row[0]: row[1] for row in conn.execute(
            "SELECT criterion_id,score FROM criterion_evaluations WHERE evaluation_run_id='RUN-20261003-32'")}
        links = conn.execute("SELECT count(*) FROM evaluation_evidence e JOIN crumbs c USING(item_id) WHERE evaluation_id='EVAL-APP_B_I' AND c.document_side='DOCUMENT'").fetchone()[0]
    assert {"APP_B_"+row['n']: row['score'] for row in data} == expected
    organization = next(row for row in data if row["n"] == "I")
    assert organization["score_crumb_count"] == links
    assert organization["score_trace"] == f"{links} linked controls; content-based judgment: substantially (4/5, 75 points)"
    assert organization["score_crumbs"]
    assert organization["score_crumbs"][0]["filename"]
    assert organization["score_crumbs"][0]["chapters"][0]["heading_path"]
    assert organization["score_crumbs"][0]["chapters"][0]["text"]
    assert all(row['aff'] and row['con'] and row['rationale'] for row in data)
