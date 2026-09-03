"""EA2.4 browser tests for deterministic citation copy and evidence printing."""
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


def test_citation_is_deterministic_complete_and_visible(page):
    _open_sample(page)
    citation = page.locator("#evidence-citation-output").input_value()
    assert citation == page.evaluate("buildEvidenceCitation(currentEvidenceCrumb)")
    assert citation == page.evaluate("buildEvidenceCitation(currentEvidenceCrumb)")
    required = [
        "Run-ID: RUN-20260728-01",
        "Package-SHA256: 77cf9e84c46fe5d4301424fa402b4cd19aceea7c57a2d0b8386af433a01c5d92",
        "Bundle-SHA256: 6e937b48352dffa65044bb391181e313f4e73768517a1dacf7cc02adb727512b",
        "Document-ID: DOC-0021",
        "Source-SHA256: a2c316258415ae5ea18e9e057f4d1e814992ea59eb40cb70af485433221ddab3",
        f"Crumb-ID: {SAMPLE_CRUMB}",
        "Criterion-ID: APP_B_I",
        "Quote-ID: QUOTE-DOC-0021-0003-01",
        "Link-method: EXACT",
        "Locator: Organizacijska shema ENCONET d.o.o. 1/3, lines 1341-1353",
        "Chunk-ID: CHUNK-DOC-0021-0105",
        "OPIS RADNIH MJESTA",
        "B[UPRAVA DRUŠTVA]",
    ]
    for value in required:
        assert value in citation
    assert page.locator("#evidence-citation-output").is_visible()


def test_copy_uses_clipboard_when_available(page):
    page.evaluate(
        """() => Object.defineProperty(navigator, 'clipboard', {
            configurable: true,
            value: {writeText: async text => { window.__copiedCitation = text; }},
        })"""
    )
    _open_sample(page)
    page.locator("#evidence-copy").click()
    page.wait_for_function("window.__copiedCitation !== undefined")
    assert page.evaluate("window.__copiedCitation") == page.locator(
        "#evidence-citation-output"
    ).input_value()
    assert page.locator("#evidence-copy-status").text_content() == "Citat je kopiran"


def test_denied_clipboard_keeps_visible_selected_fallback(page):
    page.evaluate(
        """() => Object.defineProperty(navigator, 'clipboard', {
            configurable: true,
            value: {writeText: async () => { throw new Error('denied'); }},
        })"""
    )
    _open_sample(page)
    page.locator("#evidence-copy").click()
    status = page.locator("#evidence-copy-status")
    assert status.text_content() == "Kopiranje nije dopušteno; citat je označen ispod"
    output = page.locator("#evidence-citation-output")
    assert output.is_visible()
    assert SAMPLE_CRUMB in output.input_value()
    assert output.evaluate("element => element === document.activeElement")
    assert output.evaluate(
        "element => element.selectionStart === 0 && element.selectionEnd === element.value.length"
    )


def test_print_evidence_expands_selected_record_and_hides_controls(page):
    _open_sample(page)
    page.evaluate(
        """() => { window.print = () => { window.__printState = {
            printClass: document.body.classList.contains('evidence-print'),
            drawerHidden: document.getElementById('evidence-drawer').hidden,
            citation: document.getElementById('evidence-citation-output').value,
        }; }; }"""
    )
    page.locator("#evidence-print").click()
    state = page.evaluate("window.__printState")
    assert state["printClass"] is True
    assert state["drawerHidden"] is False
    for value in (
        "Run-ID: RUN-20260728-01", "Package-SHA256:", "Source-SHA256:",
        f"Crumb-ID: {SAMPLE_CRUMB}", "Quote-ID:", "Chunk-ID:",
    ):
        assert value in state["citation"]

    page.emulate_media(media="print")
    assert page.locator("#evidence-copy").evaluate(
        "element => getComputedStyle(element).display"
    ) == "none"
    assert page.locator("body > main").evaluate(
        "element => getComputedStyle(element).display"
    ) == "none"
    assert page.locator("#evidence-drawer").evaluate(
        "element => getComputedStyle(element).display"
    ) != "none"
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert page.locator("body").get_attribute("class") in (None, "")
