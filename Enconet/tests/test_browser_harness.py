"""EA5.1 tests for the pinned offline headless-browser harness."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import browser_harness  # noqa: E402


CONFIG = ENCONET / "schemas" / "browser_harness.yml"
CANDIDATE = (
    ENCONET / "outputs" / "candidates" / "evidence_access" /
    "RUN-20260728-01" / "enconet_appendix_b_dashboard.html"
)


def test_harness_contract_pins_dependency_runtime_and_failure_policy():
    config = browser_harness.load_config(CONFIG)
    assert config["dependency"] == "playwright==1.62.0"
    assert config["browser"]["name"] == "chromium"
    assert config["browser"]["installation_mode"] == "only-shell"
    assert isinstance(config["browser"]["revision"], str)
    assert config["browser"]["revision"]
    assert config["browser"]["root"] == r"C:\xPY\vEnv\WikiEnconet\pw-browsers"
    assert config["navigation"]["required_scheme"] == "file"
    assert config["artifacts"]["retention"] == "on-failure"
    assert config["artifacts"]["required"] == ["screenshot.png", "dom.html", "console.log"]


def test_preflight_passes_for_pinned_library_and_runtime():
    assert browser_harness.preflight(CONFIG) == []


def test_missing_runtime_is_actionable_nonzero_failure(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.delenv("PLAYWRIGHT_BROWSERS_PATH", raising=False)
    config = browser_harness.load_config(CONFIG)
    config["browser"]["root"] = str(tmp_path / "missing-browser-root")
    broken = tmp_path / "missing-runtime.yml"
    broken.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    assert browser_harness.main(["preflight", "--config", str(broken)]) == 1
    error = capsys.readouterr().err
    assert "browser runtime missing" in error
    assert "playwright install --only-shell chromium" in error


def test_smoke_opens_candidate_directly_through_file_url(tmp_path: Path):
    result = browser_harness.run_check(
        CANDIDATE,
        artifact_dir=tmp_path / "artifacts",
        config_path=CONFIG,
    )
    assert result["passed"] is True
    assert result["url"].startswith("file:///")
    assert result["network_requests"] == []
    assert result["evidence_bundle_count"] == 1
    assert not (tmp_path / "artifacts").exists()


def test_failure_retains_screenshot_dom_and_console_log(tmp_path: Path):
    broken_html = tmp_path / "broken.html"
    broken_html.write_text(
        "<!doctype html><title>broken</title><script>console.error('fixture failure')</script>",
        encoding="utf-8",
    )
    artifact_dir = tmp_path / "retained"
    result = browser_harness.run_check(
        broken_html,
        artifact_dir=artifact_dir,
        config_path=CONFIG,
    )
    assert result["passed"] is False
    assert "evidence bundle" in result["error"]
    for name in ("screenshot.png", "dom.html", "console.log"):
        assert (artifact_dir / name).is_file()
        assert (artifact_dir / name).stat().st_size > 0
    assert "<title>broken</title>" in (artifact_dir / "dom.html").read_text(encoding="utf-8")
    assert "fixture failure" in (artifact_dir / "console.log").read_text(encoding="utf-8")


def test_http_navigation_is_rejected_before_browser_launch(tmp_path: Path):
    with pytest.raises(browser_harness.BrowserHarnessError, match="local HTML file"):
        browser_harness.run_check(
            "https://example.invalid/dashboard.html",
            artifact_dir=tmp_path / "artifacts",
            config_path=CONFIG,
        )


def test_candidate_has_interactive_crumb_control(tmp_path: Path):
    result = browser_harness.run_check(
        CANDIDATE,
        artifact_dir=tmp_path / "artifacts",
        config_path=CONFIG,
        require_interactive=True,
    )
    assert result["passed"] is True, result["error"]
