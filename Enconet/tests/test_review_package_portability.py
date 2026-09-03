"""EA4.3 deterministic package-manifest and relocation tests."""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import browser_harness  # noqa: E402
import build_review_package  # noqa: E402
import validate_review_package  # noqa: E402


CATALOG = ENCONET / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"
CONFIG = ENCONET / "schemas" / "browser_harness.yml"
RUN_ID = "RUN-20260728-01"
SAMPLE_CRUMB = "CRUMB-DOC-0021-APP_B_I-0003"


def _build(destination: Path) -> Path:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    return build_review_package.build(catalog, ENCONET, destination)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*") if path.is_file()
    }


def test_manifest_is_deterministic_complete_and_valid(tmp_path: Path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    manifest_path = _build(first)
    _build(second)
    assert _snapshot(first) == _snapshot(second)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.0"
    assert manifest["package_id"] == "REVIEW-PACKAGE-RUN-20260728-01"
    assert manifest["run_ids"] == [RUN_ID]
    assert manifest["entrypoint"] == "review_workspace.html"
    assert len(manifest["files"]) == 6
    assert [row["path"] for row in manifest["files"]] == sorted(
        row["path"] for row in manifest["files"]
    )
    assert validate_review_package.validate(first) == []


def test_portable_links_contain_no_repository_drive_or_username(tmp_path: Path):
    package_root = tmp_path / "portable"
    _build(package_root)
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in package_root.rglob("*")
        if path.is_file() and path.suffix in {".html", ".md", ".json"}
    )
    assert "C:\\" not in text and "C:/" not in text
    assert "Users/PC" not in text and "Users\\PC" not in text
    assert "../" not in (package_root / "review_workspace.html").read_text(encoding="utf-8")


def test_complete_package_passes_after_non_ascii_relocation(tmp_path: Path):
    source = tmp_path / "source"
    _build(source)
    relocated = tmp_path / "Premješteni paket č dokaza"
    shutil.copytree(source, relocated)
    assert validate_review_package.validate(relocated) == []


def test_missing_renamed_and_changed_files_fail_with_precise_paths(tmp_path: Path):
    missing_root = tmp_path / "missing"
    _build(missing_root)
    report = missing_root / RUN_ID / "evaluation_report.md"
    report.unlink()
    errors = validate_review_package.validate(missing_root)
    assert any("missing manifest file: RUN-20260728-01/evaluation_report.md" in error for error in errors)

    renamed_root = tmp_path / "renamed"
    _build(renamed_root)
    viewer = renamed_root / RUN_ID / "evidence_explorer.html"
    viewer.rename(viewer.with_name("renamed.html"))
    errors = validate_review_package.validate(renamed_root)
    assert any("missing manifest file: RUN-20260728-01/evidence_explorer.html" in error for error in errors)
    assert any("unlisted package file: RUN-20260728-01/renamed.html" in error for error in errors)

    changed_root = tmp_path / "changed"
    _build(changed_root)
    workspace = changed_root / "review_workspace.html"
    workspace.write_text(workspace.read_text(encoding="utf-8") + "\nchanged", encoding="utf-8")
    errors = validate_review_package.validate(changed_root)
    assert any("manifest hash mismatch: review_workspace.html" in error for error in errors)


def test_cli_returns_nonzero_for_invalid_package(tmp_path: Path, capsys):
    root = tmp_path / "package"
    _build(root)
    assert validate_review_package.main([str(root)]) == 0
    assert "validate_review_package: PASS" in capsys.readouterr().out
    (root / "review_catalog.json").unlink()
    assert validate_review_package.main([str(root)]) == 1
    assert "missing manifest file: review_catalog.json" in capsys.readouterr().err


def test_relocated_workspace_opens_exact_source_evidence_in_browser(tmp_path: Path):
    assert browser_harness.preflight(CONFIG) == []
    source = tmp_path / "source"
    _build(source)
    relocated = tmp_path / "Vlasnik paket č s razmacima"
    shutil.copytree(source, relocated)
    config = browser_harness.load_config(CONFIG)
    previous = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = config["browser"]["root"]
    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto((relocated / "review_workspace.html").resolve().as_uri(), wait_until="load")
                page.locator('a[data-artifact="viewer"]').click()
                page.wait_for_load_state("load")
                page.goto(page.url + f"#evidence/crumb/{SAMPLE_CRUMB}", wait_until="load")
                assert page.locator("#evidence-drawer").is_visible()
                assert page.locator("#evidence-reference-id").text_content() == SAMPLE_CRUMB
                assert page.locator(".evidence-quote").count() == 3
                assert page.locator("#evidence-chunk-text").text_content()
            finally:
                browser.close()
    finally:
        if previous is None:
            os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
        else:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous
