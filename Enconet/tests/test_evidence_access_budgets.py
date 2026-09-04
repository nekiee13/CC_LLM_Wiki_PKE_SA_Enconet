"""EA5.3 security, encoding, size, projection, and browser-budget tests."""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import pytest
import yaml


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import browser_harness  # noqa: E402
import generate_dashboard  # noqa: E402
import run_all_validations  # noqa: E402
import validate_evidence_access_budgets as budgets_validator  # noqa: E402


BUDGETS_PATH = ENCONET / "schemas" / "evidence_access_budgets.yml"
PACKAGE_ROOT = ENCONET / "outputs" / "candidates" / "evidence_access" / "portable_package"
DATA_PATH = ENCONET / "outputs" / "enconet_appendix_b_dashboard_data.json"
BUNDLE_PATH = PACKAGE_ROOT / "RUN-20260728-01" / "evidence_bundle.json"
VIEWER_PATH = PACKAGE_ROOT / "RUN-20260728-01" / "evidence_explorer.html"
CONFIG = ENCONET / "schemas" / "browser_harness.yml"


def test_budget_contract_is_explicit_versioned_and_owner_authorized():
    budgets = budgets_validator.load_budgets(BUDGETS_PATH)
    assert budgets["schema_version"] == "1.0"
    assert budgets["approval"]["authority"] == "project_owner"
    assert budgets["approval"]["decision"] == "EA5.3 execution authorized"
    assert budgets["size_bytes"] == {
        "bundle": 524_288, "viewer": 524_288, "workspace": 65_536,
        "package_payload_total": 1_048_576,
    }
    assert budgets["performance_ms"] == {
        "viewer_initial_render": 3_000, "workspace_initial_render": 2_000,
        "evidence_open": 500, "search_response": 500,
    }


def test_budget_validator_is_a_dashboard_ready_release_check():
    assert run_all_validations.ORDER[-1] == "evidence_budgets"
    assert not run_all_validations.applicable("evidence_budgets", "report_ready")
    assert run_all_validations.applicable("evidence_budgets", "dashboard_ready")
    command = run_all_validations.commands(
        phase="closed", supplier="enconet", db=ENCONET / "db" / "nqa_audit.sqlite",
        outputs=ENCONET / "outputs", run_id="RUN-20260728-01",
        app_b_json=ENCONET / "fixture.json", no_record=True,
    )["evidence_budgets"]
    assert command == [
        sys.executable, str(ENCONET / "scripts" / "validate_evidence_access_budgets.py"),
        str(PACKAGE_ROOT), "--budgets", str(BUDGETS_PATH), "--browser-config", str(CONFIG),
    ]


def test_production_package_passes_static_budgets_with_exact_metrics():
    budgets = budgets_validator.load_budgets(BUDGETS_PATH)
    errors, metrics = budgets_validator.validate_static(PACKAGE_ROOT, budgets)
    assert errors == []
    assert metrics["bundle_bytes"] == BUNDLE_PATH.stat().st_size
    assert metrics["viewer_bytes"] == VIEWER_PATH.stat().st_size
    assert metrics["workspace_bytes"] == (PACKAGE_ROOT / "review_workspace.html").stat().st_size
    assert metrics["documents"] == 14
    assert metrics["chunks"] == 99
    assert metrics["crumbs"] == 62
    assert metrics["quotes"] == 88


def test_size_projection_and_utf8_fail_closed_with_precise_artifacts(tmp_path: Path):
    budgets = budgets_validator.load_budgets(BUDGETS_PATH)
    oversized = tmp_path / "oversized"
    shutil.copytree(PACKAGE_ROOT, oversized)
    viewer = oversized / "RUN-20260728-01" / "evidence_explorer.html"
    viewer.write_bytes(viewer.read_bytes() + b"x" * 600_000)
    errors, _metrics = budgets_validator.validate_static(oversized, budgets)
    assert any("viewer size budget exceeded" in error and "evidence_explorer.html" in error for error in errors)

    projected = tmp_path / "projected"
    shutil.copytree(PACKAGE_ROOT, projected)
    bundle_path = projected / "RUN-20260728-01" / "evidence_bundle.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundle["chunks"] *= 6
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
    errors, _metrics = budgets_validator.validate_static(projected, budgets)
    assert any("chunks projection budget exceeded" in error for error in errors)

    invalid = tmp_path / "invalid-utf8"
    shutil.copytree(PACKAGE_ROOT, invalid)
    report = invalid / "RUN-20260728-01" / "evaluation_report.md"
    report.write_bytes(b"\xff\xfe")
    errors, _metrics = budgets_validator.validate_static(invalid, budgets)
    assert any("UTF-8 round-trip failed" in error and "evaluation_report.md" in error for error in errors)

    malicious = tmp_path / "malicious-name"
    shutil.copytree(PACKAGE_ROOT, malicious)
    manifest_path = malicious / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["path"] = "../dokaz<script>.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    errors, _metrics = budgets_validator.validate_static(malicious, budgets)
    assert any("unsafe package artifact path: ../dokaz<script>.json" in error for error in errors)


def test_renderer_blocks_over_budget_bundle_before_building_html(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    budgets = budgets_validator.load_budgets(BUDGETS_PATH)
    budgets["projection_counts"]["chunks"] = 98
    restrictive = tmp_path / "restrictive.yml"
    restrictive.write_text(yaml.safe_dump(budgets, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(generate_dashboard, "EVIDENCE_BUDGETS", restrictive)
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="chunks projection budget exceeded"):
        generate_dashboard.render(data, evidence_bundle=bundle)


def test_hostile_source_is_text_only_and_multilingual_content_round_trips(tmp_path: Path):
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    hostile = (
        '</script><script>window.__eaAttack=1</script>'
        '<img src=x onerror="window.__eaImg=1"> '
        '[klik](javascript:window.__eaLink=1) \u202e čćžšđ ČĆŽŠĐ čšž ČŠŽ'
    )
    crumb = bundle["crumbs"][0]
    document = next(row for row in bundle["documents"] if row["document_id"] == crumb["document_id"])
    chunk = next(row for row in bundle["chunks"] if row["chunk_id"] == crumb["chunk_ids"][0])
    quote = next(row for row in bundle["quotes"] if row["quote_id"] == crumb["quote_ids"][0])
    crumb["statement"] = hostile
    document["filename"] = hostile
    chunk["text"] = f"prefix {hostile} suffix"
    quote["text_original"] = hostile
    html = generate_dashboard.render(data, evidence_bundle=bundle)
    assert "</script><script>window.__eaAttack" not in html
    assert "<img src=x" not in html
    assert "\\u202e" in html
    assert json.loads(json.dumps(hostile, ensure_ascii=False)) == hostile
    target = tmp_path / "napad č š ž.html"
    target.write_text(html, encoding="utf-8", newline="\n")

    config = browser_harness.load_config(CONFIG)
    previous = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = config["browser"]["root"]
    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page_errors: list[str] = []
                external: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.on("request", lambda request: external.append(request.url)
                        if request.url.startswith(("http://", "https://")) else None)
                page.goto(target.resolve().as_uri() + crumb["viewer_target"], wait_until="load")
                assert page_errors == [] and external == []
                assert page.evaluate("typeof window.__eaAttack === 'undefined'")
                assert page.evaluate("typeof window.__eaImg === 'undefined'")
                assert page.evaluate("typeof window.__eaLink === 'undefined'")
                assert page.locator("#evidence-statement").text_content() == hostile
                assert page.locator("#evidence-document-filename").text_content() == hostile
                assert hostile in page.locator("#evidence-chunk-text").text_content()
                assert page.locator("img").count() == 0
            finally:
                browser.close()
    finally:
        if previous is None:
            os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
        else:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous


def test_production_browser_performance_and_network_budgets():
    budgets = budgets_validator.load_budgets(BUDGETS_PATH)
    errors, metrics = budgets_validator.validate_browser(PACKAGE_ROOT, budgets, CONFIG)
    assert errors == []
    assert metrics["external_requests"] == 0
    for name, limit in budgets["performance_ms"].items():
        assert 0 <= metrics[f"{name}_ms"] <= limit


def test_budget_cli_is_release_usable(capsys):
    assert budgets_validator.main([
        str(PACKAGE_ROOT), "--budgets", str(BUDGETS_PATH),
        "--browser-config", str(CONFIG),
    ]) == 0
    output = capsys.readouterr().out
    assert "validate_evidence_access_budgets: PASS" in output
    assert "bundle_bytes=" in output and "evidence_open_ms=" in output
