"""EA4.2 static offline review-workspace tests."""
from __future__ import annotations

import copy
import json
import os
import re
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import browser_harness  # noqa: E402
import generate_review_workspace  # noqa: E402
import validate_review_workspace  # noqa: E402


CATALOG = ENCONET / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"
WORKSPACE = CATALOG.with_name("review_workspace.html")
CONFIG = ENCONET / "schemas" / "browser_harness.yml"
RUN_ID = "RUN-20260728-01"


@pytest.fixture(scope="module")
def catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


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
                yield browser_page
            finally:
                browser.close()
    finally:
        if previous is None:
            os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
        else:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous


def test_render_is_self_contained_and_catalog_bound(catalog: dict):
    html = generate_review_workspace.render(
        catalog, output_path=WORKSPACE, project_root=ENCONET
    )
    assert html == generate_review_workspace.render(
        copy.deepcopy(catalog), output_path=WORKSPACE, project_root=ENCONET
    )
    assert html.count('id="review-catalog"') == 1
    assert RUN_ID in html
    assert 'data-status="candidate"' in html
    assert validate_review_workspace.validate(catalog, html) == []
    assert re.search(r'https?://', html, re.IGNORECASE) is None


def test_candidate_and_approved_rows_have_distinct_status_contract(catalog: dict):
    approved = copy.deepcopy(catalog["runs"][0])
    approved["run_id"] = "RUN-20260729-02"
    approved["status"] = "approved"
    expanded = copy.deepcopy(catalog)
    expanded["runs"].append(approved)
    html = generate_review_workspace.render(
        expanded, output_path=WORKSPACE, project_root=ENCONET,
        validate_catalog=False,
    )
    assert 'data-status="candidate"' in html
    assert 'data-status="approved"' in html
    assert ".status-candidate" in html and ".status-approved" in html


def test_missing_or_hash_changed_artifact_is_visible_but_not_linked(catalog: dict, tmp_path: Path):
    broken = copy.deepcopy(catalog)
    broken["runs"][0]["artifacts"]["viewer"]["path"] = "missing/viewer.html"
    html = generate_review_workspace.render(
        broken, output_path=tmp_path / "review_workspace.html", project_root=tmp_path,
        validate_catalog=False,
    )
    assert 'data-availability="unavailable"' in html
    assert 'data-artifact="viewer"' not in html
    assert "Unavailable: file missing" in html


def test_security_contract_has_no_directory_or_network_access(catalog: dict):
    html = generate_review_workspace.render(
        catalog, output_path=WORKSPACE, project_root=ENCONET
    )
    forbidden = (
        "fetch(", "XMLHttpRequest", "WebSocket", "showDirectoryPicker",
        "showOpenFilePicker", "webkitdirectory", "FileSystemDirectoryHandle",
    )
    assert all(marker not in html for marker in forbidden)
    assert "directory scan" in html


def test_browser_filters_and_keyboard_selects_registered_run(page):
    requests: list[str] = []
    page.on("request", lambda request: requests.append(request.url))
    page.goto(WORKSPACE.resolve().as_uri(), wait_until="load")
    assert page.url.startswith("file://")
    card = page.locator(f'[data-run-id="{RUN_ID}"]')
    assert card.is_visible()
    page.locator("#run-filter").fill("does-not-exist")
    assert card.is_hidden()
    page.locator("#run-filter").fill("enconet appendix_b")
    assert card.is_visible()

    select = card.locator(".run-select")
    select.focus()
    select.press("Enter")
    assert select.get_attribute("aria-expanded") == "false"
    select.press("Enter")
    assert select.get_attribute("aria-expanded") == "true"
    assert card.locator(".run-details").is_visible()
    assert all(url.startswith("file://") for url in requests)


def test_owner_opens_matched_evidence_explorer_in_one_action(page):
    page.goto(WORKSPACE.resolve().as_uri(), wait_until="load")
    card = page.locator(f'[data-run-id="{RUN_ID}"]')
    links = card.locator("a[data-artifact]")
    assert set(links.evaluate_all("nodes => nodes.map(node => node.dataset.artifact)")) == {
        "bundle", "package", "report", "viewer"
    }
    viewer = card.locator('a[data-artifact="viewer"]')
    assert viewer.is_visible()
    viewer.click()
    page.wait_for_load_state("load")
    assert page.url.startswith("file://")
    assert page.locator("#dashboard-title").is_visible()
    assert "Appendix B" in page.title() or "Dodatka B" in page.title()


def test_validator_rejects_missing_controls_and_unregistered_run(catalog: dict):
    html = generate_review_workspace.render(
        catalog, output_path=WORKSPACE, project_root=ENCONET
    )
    assert "missing workspace control: run-filter" in validate_review_workspace.validate(
        catalog, html.replace('id="run-filter"', 'id="removed"')
    )
    assert any(
        "workspace/catalog run mismatch" in error
        for error in validate_review_workspace.validate(
            catalog, html.replace(RUN_ID, "RUN-20990101-99")
        )
    )
