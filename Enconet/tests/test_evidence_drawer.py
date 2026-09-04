"""EA2.2 real-browser tests for evidence controls and the read-only drawer."""
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
SAMPLE_STATEMENT = (
    "Organizacijska shema prikazuje osiguranje kvalitete kao zasebnu cjelinu "
    "neposredno povezanu s upravom društva."
)


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


def _sample_control(page):
    return page.locator(f'[data-evidence-id="{SAMPLE_CRUMB}"]').first


def test_click_opens_exact_statement_document_quotes_chunk_and_traceability(page):
    control = _sample_control(page)
    assert control.count() == 1
    control.click()
    drawer = page.locator("#evidence-drawer")
    assert drawer.is_visible()
    assert page.locator("#evidence-statement").text_content() == SAMPLE_STATEMENT
    assert page.locator("#evidence-document-id").text_content() == "DOC-0021"
    assert page.locator("#evidence-criterion-id").text_content() == "APP_B_I"
    assert page.locator("#evidence-reference-id").text_content() == SAMPLE_CRUMB
    assert page.locator(".evidence-quote").count() == 3
    assert page.locator('[data-quote-id="QUOTE-DOC-0021-0003-01"]').count() == 1
    assert page.locator('[data-quote-id="QUOTE-DOC-0021-0003-02"]').count() == 1
    assert page.locator('[data-quote-id="QUOTE-DOC-0021-0003-03"]').count() == 1
    chapter_references = page.locator(".quote-chapter-reference").all_text_contents()
    assert len(chapter_references) == 3
    assert all("Poglavlje:" in value for value in chapter_references)
    assert all("OPIS RADNIH MJESTA" in value for value in chapter_references)
    assert page.locator('[data-chunk-id="CHUNK-DOC-0021-0105"]').count() == 1
    assert "OPIS RADNIH MJESTA" in page.locator("#evidence-heading-path").text_content()
    assert "Članak 4." in page.locator("#evidence-chunk-text").text_content()


def test_each_criterion_reference_is_an_individual_control(page):
    first_card = page.locator(".criterion-card").first
    assert first_card.locator(".evidence-control").count() == 3
    ids = first_card.locator(".evidence-control").evaluate_all(
        "elements => elements.map(element => element.dataset.evidenceId)"
    )
    assert ids == [
        "CRUMB-DOC-0021-APP_B_I-0003",
        "CRUMB-DOC-0022-APP_B_I-0002",
        "CRUMB-DOC-0027-APP_B_I-0001",
    ]


def test_close_escape_focus_return_and_keyboard_activation(page):
    control = _sample_control(page)
    control.focus()
    control.press("Enter")
    assert page.locator("#evidence-drawer").is_visible()
    assert page.evaluate("document.activeElement.id") == "evidence-panel-heading"
    page.locator("#evidence-close").click()
    assert page.locator("#evidence-drawer").is_hidden()
    assert control.evaluate("element => element === document.activeElement")

    control.press("Space")
    assert page.locator("#evidence-drawer").is_visible()
    page.keyboard.press("Escape")
    assert page.locator("#evidence-drawer").is_hidden()
    assert control.evaluate("element => element === document.activeElement")


def test_unknown_target_shows_localized_announced_error_without_blank_panel(page):
    requested = "#evidence/crumb/CRUMB-DOC-0021-APP_B_I-9999"
    page.evaluate("target => openEvidence(target)", requested)
    assert page.locator("#evidence-drawer").is_visible()
    status = page.locator("#evidence-status")
    assert status.get_attribute("role") == "status"
    assert status.get_attribute("aria-live") == "polite"
    assert status.text_content() == "Dokaz nije dostupan"
    assert page.locator("#evidence-requested-target").text_content() == requested
    assert page.evaluate("document.activeElement.id") == "evidence-panel-heading"


@pytest.mark.parametrize(
    ("target", "expected_context"),
    [
        ("#evidence/document/DOC-0024", "DOC-0024"),
        ("#evidence/source/package", "RUN-20260728-01"),
    ],
)
def test_document_and_package_targets_show_only_the_requested_entity(
    page, target: str, expected_context: str
):
    """Broad entity links must not present an arbitrary crumb as exact evidence."""
    page.evaluate("target => openEvidence(target)", target)

    assert page.locator("#evidence-drawer").is_visible()
    assert page.locator("#evidence-requested-target").text_content() == target
    context = page.locator("#evidence-entity-context")
    assert context.is_visible()
    assert expected_context in context.text_content()
    crumb_content = page.locator("#evidence-crumb-content")
    assert crumb_content.count() == 1
    assert crumb_content.is_hidden()
    assert "CRUMB-" not in page.locator("#evidence-resolved-content").text_content()


def test_direct_fragment_survives_refresh_and_browser_history(page):
    target = f"#evidence/crumb/{SAMPLE_CRUMB}"
    page.goto(CANDIDATE.resolve().as_uri() + target, wait_until="load")
    assert page.locator("#evidence-drawer").is_visible()
    assert page.locator("#evidence-statement").text_content() == SAMPLE_STATEMENT

    page.reload(wait_until="load")
    assert page.locator("#evidence-drawer").is_visible()
    assert page.locator("#evidence-requested-target").text_content() == target

    page.goto(CANDIDATE.resolve().as_uri(), wait_until="load")
    _sample_control(page).click()
    assert page.locator("#evidence-drawer").is_visible()
    page.go_back(wait_until="load")
    assert page.locator("#evidence-drawer").is_hidden()
    page.go_forward(wait_until="load")
    assert page.locator("#evidence-drawer").is_visible()
    assert page.locator("#evidence-statement").text_content() == SAMPLE_STATEMENT


def test_open_and_close_do_not_mutate_embedded_evaluation_data(page):
    before = page.locator("#evidence-bundle").text_content()
    _sample_control(page).click()
    page.locator("#evidence-close").click()
    after = page.locator("#evidence-bundle").text_content()
    assert after == before


def test_existing_filter_search_sort_expand_collapse_and_print_still_work(page):
    cards = page.locator(".criterion-card")
    assert cards.count() == 18
    page.locator("#rating-filter").select_option("partially")
    assert 0 < cards.count() < 18
    page.locator("#rating-filter").select_option("")
    page.locator("#criterion-search").fill("APP_B_XVIII")
    assert cards.count() == 1
    page.locator("#criterion-search").fill("")
    page.locator("#sort-button").click()
    assert "APP_B_XVIII" in cards.first.locator("h3").text_content()
    page.locator("#collapse-button").click()
    assert page.locator(".criterion-body:not([hidden])").count() == 0
    page.locator("#expand-button").click()
    assert page.locator(".criterion-body[hidden]").count() == 0
    page.evaluate("window.print = () => { window.__printCalled = true; }")
    page.locator("#print-button").click()
    assert page.evaluate("window.__printCalled") is True
