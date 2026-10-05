"""Contract checks for per-criterion summaries and score traceability."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_umbra_conformance_dashboard import DEFAULT_DB, DEFAULT_MATRIX, render


def _data(page: str) -> list[dict]:
    payload = re.search(r"const data = (\[.*?\]);\nconst labels=", page, re.S)
    assert payload is not None
    return json.loads(payload.group(1))


def test_cards_show_summary_and_crumbs_that_feed_score() -> None:
    page = render(DEFAULT_MATRIX, DEFAULT_DB, "2026-10-05", "RUN-20261003-32")
    data = _data(page)
    assert len(data) == 18
    assert "Criterion summary" in page
    assert "Crumbs linked to this score" in page
    assert "Source chapter:" in page
    assert "chapterText" in page
    assert "score_trace" in page
    assert sum(row["score"] for row in data) == 950
    organization = next(row for row in data if row["n"] == "I")
    assert organization["score_crumb_count"] == 31
    assert organization["score_trace"] == "31 linked vendor crumb(s) -> substantially (4/5, 75 points)"
    assert organization["score_crumbs"]
    assert organization["score_crumbs"][0]["filename"]
    assert organization["score_crumbs"][0]["chapters"][0]["heading_path"]
    assert organization["score_crumbs"][0]["chapters"][0]["text"]
    missing = next(row for row in data if row["n"] == "VIII")
    assert missing["score_crumb_count"] == 0
    assert missing["score"] == 0
