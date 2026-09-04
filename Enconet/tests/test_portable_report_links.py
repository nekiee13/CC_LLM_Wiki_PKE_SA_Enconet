"""EA3.2 tests for movable report-to-evidence navigation."""
from __future__ import annotations

import re
import json
import os
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import generate_report  # noqa: E402
import browser_harness  # noqa: E402
from test_epic11_report import package  # noqa: E402


VIEWER_NAME = "enconet_appendix_b_dashboard.html"
CONFIG = ENCONET / "schemas" / "browser_harness.yml"
CANDIDATE_VIEWER = (
    ENCONET / "outputs" / "candidates" / "evidence_access" /
    "RUN-20260728-01" / VIEWER_NAME
)


@pytest.mark.parametrize(
    ("report", "viewer"),
    [
        (
            ENCONET / "outputs" / "enconet_appendix_b_evaluation_report.md",
            ENCONET / "outputs" / VIEWER_NAME,
        ),
        (
            ENCONET / "outputs" / "candidates" / "evidence_access" /
            "RUN-20260728-01" / "enconet_appendix_b_evaluation_report.md",
            ENCONET / "outputs" / "candidates" / "evidence_access" /
            "RUN-20260728-01" / VIEWER_NAME,
        ),
    ],
)
def test_published_and_candidate_sibling_locations_get_the_same_portable_path(
    report: Path, viewer: Path
):
    assert generate_report.portable_viewer_path(report, viewer) == VIEWER_NAME


def test_report_citations_point_to_the_sibling_viewer_without_absolute_paths():
    report = generate_report.render(package(), viewer_path=VIEWER_NAME)
    links = re.findall(r"\[[^\]]+\]\(([^)]+#evidence/[^)]+)\)", report)
    assert links
    assert all(link.startswith(f"{VIEWER_NAME}#evidence/") for link in links)
    assert "file://" not in report.casefold()
    assert re.search(r"[A-Za-z]:[/\\]", report) is None


def test_non_ascii_sibling_viewer_name_is_url_encoded():
    viewer = ENCONET / "outputs" / "candidates" / "Dokazi č" / "pregled dokazov č.html"
    report_path = viewer.with_name("izvješće.md")
    portable = generate_report.portable_viewer_path(report_path, viewer)
    report = generate_report.render(package("hr"), viewer_path=portable)
    href = re.search(r"\[[^\]]+\]\(([^)]+#evidence/crumb/[^)]+)\)", report).group(1)
    parsed = urlsplit(href)
    assert unquote(parsed.path) == viewer.name
    assert " " not in parsed.path and "č" not in parsed.path


def test_portable_path_refuses_cross_directory_and_absolute_targets(tmp_path: Path):
    report = tmp_path / "package" / "report.md"
    with pytest.raises(ValueError, match="sibling"):
        generate_report.portable_viewer_path(report, tmp_path / "viewer.html")
    with pytest.raises(ValueError, match="relative|absolute"):
        generate_report.render(package(), viewer_path="C:/private/viewer.html")


@pytest.mark.parametrize("language", ["en", "hr"])
def test_language_variants_preserve_run_binding_and_viewer_target(language: str):
    data = package(language)
    report = generate_report.render(data, viewer_path=VIEWER_NAME)
    assert f'"run_id":"{data["run"]["run_id"]}"' in report
    assert f"]({VIEWER_NAME}#evidence/crumb/" in report


def test_moved_report_href_opens_exact_evidence_for_all_report_entity_types(
    tmp_path: Path,
):
    assert browser_harness.preflight(CONFIG) == []
    production = json.loads(
        (ENCONET / "outputs" / "enconet_appendix_b_evaluation_package.json")
        .read_text(encoding="utf-8")
    )
    report = generate_report.render(production, viewer_path=VIEWER_NAME)
    moved = tmp_path / "Premješteni dokazi č"
    moved.mkdir()
    viewer = moved / VIEWER_NAME
    shutil.copy2(CANDIDATE_VIEWER, viewer)
    hrefs = re.findall(r"\[([^\]]+)\]\(([^)]+#evidence/[^)]+)\)", report)
    by_type = {}
    for label, href in hrefs:
        entity_type = urlsplit(href).fragment.split("/", 2)[1]
        by_type.setdefault(entity_type, (label, href))
    by_type["source"] = (
        "source:package", f"{VIEWER_NAME}#evidence/source/package"
    )
    assert set(by_type) >= {
        "crumb", "document", "evaluation", "gap", "finding", "action", "source"
    }

    config = browser_harness.load_config(CONFIG)
    previous = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = config["browser"]["root"]
    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                for _label, href in by_type.values():
                    parsed = urlsplit(href)
                    target = f"#{parsed.fragment}"
                    entity_type = parsed.fragment.split("/", 2)[1]
                    destination = moved / unquote(parsed.path)
                    page.goto(destination.resolve().as_uri() + target, wait_until="load")
                    assert page.locator("#evidence-drawer").is_visible()
                    assert page.locator("#evidence-requested-target").text_content() == target
                    context = page.locator("#evidence-entity-context")
                    assert context.is_hidden() is (entity_type == "crumb")
                    crumb_content = page.locator("#evidence-crumb-content")
                    if entity_type in {"document", "source"}:
                        assert crumb_content.is_hidden()
                        assert "CRUMB-" not in context.text_content()
                    else:
                        assert crumb_content.is_visible()
                        assert page.locator(
                            "#evidence-reference-id"
                        ).text_content().startswith("CRUMB-")
                        assert page.locator(".evidence-quote").count() > 0
                    if entity_type == "gap":
                        assert "description" in context.text_content()
                        assert target.rsplit("/", 1)[1] in context.text_content()
            finally:
                browser.close()
    finally:
        if previous is None:
            os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
        else:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous
