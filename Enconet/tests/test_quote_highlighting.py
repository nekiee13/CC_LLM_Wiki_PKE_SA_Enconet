"""EA2.3 browser tests for safe quote highlighting and bounded chunk navigation."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import browser_harness  # noqa: E402


CONFIG = ENCONET / "schemas" / "browser_harness.yml"
CANDIDATE = (
    ENCONET / "outputs" / "candidates" / "evidence_access" /
    "RUN-20260728-01" / "enconet_appendix_b_dashboard.html"
)
SAMPLE_CRUMB = "CRUMB-DOC-0021-APP_B_I-0003"


@pytest.fixture
def page():
    assert browser_harness.preflight(CONFIG) == []
    config = browser_harness.load_config(CONFIG)
    previous = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = config["browser"]["root"]
    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                browser_page = browser.new_page()
                browser_page.goto(CANDIDATE.resolve().as_uri(), wait_until="load")
                yield browser_page
            finally:
                browser.close()
    finally:
        if previous is None:
            os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
        else:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous


def _open_sample(page):
    page.locator(f'[data-evidence-id="{SAMPLE_CRUMB}"]').first.click()


def _synthetic_highlight(page, source: str, quotes: list[dict]) -> dict:
    return page.evaluate(
        """({source, quotes}) => {
            const container = document.createElement('pre');
            const results = renderHighlightedText(container, source, quotes);
            return {
                results,
                text: container.textContent,
                marks: [...container.querySelectorAll('mark')].map(mark => ({
                    text: mark.textContent,
                    quoteIds: mark.dataset.quoteIds,
                })),
            };
        }""",
        {"source": source, "quotes": quotes},
    )


def _quote(quote_id: str, text: str, method: str = "EXACT") -> dict:
    return {"quote_id": quote_id, "text_original": text, "link_method": method}


def test_production_quotes_are_highlighted_without_changing_chunk_text(page):
    expected = page.evaluate(
        "evidenceMaps.chunks.get('CHUNK-DOC-0021-0105').text"
    )
    _open_sample(page)
    source = page.locator("#evidence-chunk-text")
    assert source.text_content() == expected
    assert source.locator("mark").count() >= 3
    assert page.locator('.evidence-quote[data-highlight-status="exact"]').count() == 3


@pytest.mark.parametrize(
    "source,quotes,expected_status,expected_marks",
    [
        ("alpha / alpha", [_quote("Q1", "alpha")], "ambiguous", 2),
        ("abcde", [_quote("Q1", "abc"), _quote("Q2", "cde")], "exact", 3),
        ("A \n\t B", [_quote("Q1", "A B", "NORMALIZED")], "normalized", 1),
        ("source remains", [_quote("Q1", "absent")], "not_found", 0),
        ("x 😀 Članak y", [_quote("Q1", "😀 Članak")], "exact", 1),
    ],
)
def test_matcher_discloses_repetition_overlap_normalization_failure_and_unicode(
    page, source, quotes, expected_status, expected_marks
):
    rendered = _synthetic_highlight(page, source, quotes)
    assert rendered["text"] == source
    assert rendered["results"][0]["status"] == expected_status
    assert len(rendered["marks"]) == expected_marks
    if source == "abcde":
        assert rendered["marks"][1] == {"text": "c", "quoteIds": "Q1 Q2"}


def test_failed_highlight_keeps_quote_locator_chunk_and_warning(page):
    page.evaluate(
        """() => {
            evidenceMaps.quotes.get('QUOTE-DOC-0021-0003-01').text_original =
                'text that is not in the source chunk';
        }"""
    )
    _open_sample(page)
    failed = page.locator(
        '[data-quote-id="QUOTE-DOC-0021-0003-01"][data-highlight-status="not_found"]'
    )
    assert failed.count() == 1
    assert "lines 1341-1353" in failed.text_content()
    assert "text that is not in the source chunk" in failed.text_content()
    assert page.locator("#evidence-highlight-status").get_attribute("role") == "status"
    assert page.locator("#evidence-highlight-status").text_content()
    assert page.locator("#evidence-chunk-text").text_content()


def test_previous_next_navigation_stays_inside_document_and_stops_at_boundaries(page):
    _open_sample(page)
    previous = page.locator("#evidence-previous-chunk")
    following = page.locator("#evidence-next-chunk")
    assert page.locator("#evidence-current-chunk-id").text_content() == "CHUNK-DOC-0021-0105"
    previous.click()
    assert page.locator("#evidence-current-chunk-id").text_content() == "CHUNK-DOC-0021-0104"
    assert previous.is_disabled()
    assert page.locator("#evidence-document-id").text_content() == "DOC-0021"
    following.click()
    following.click()
    assert page.locator("#evidence-current-chunk-id").text_content() == "CHUNK-DOC-0021-0106"
    assert following.is_disabled()
    assert page.locator("#evidence-document-id").text_content() == "DOC-0021"
