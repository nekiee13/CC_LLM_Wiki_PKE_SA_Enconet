"""EPIC16 supplier-independent benchmark and aggregate-hook regressions."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "benchmarks"))
sys.path.insert(0, str(ENCONET / "scripts"))

import run_all_validations  # noqa: E402
import validate_benchmarks  # noqa: E402


def test_scoring_fixture_is_complete_locked_and_hand_verified() -> None:
    assert validate_benchmarks.validate_scoring() == []
    source = validate_benchmarks._load(validate_benchmarks.SCORING / "input.yml")
    expected = validate_benchmarks._load(validate_benchmarks.SCORING / "expected.yml")
    assert len(source["ratings"]) == 18
    assert set(source["ratings"].values()) == validate_benchmarks.RATINGS
    assert expected["verification"]["verified_at_creation"] is True
    assert expected["metrics"]["consolidated_score"] == 46.9


def test_dashboard_fixture_is_complete_and_passes_epic12_stack() -> None:
    assert validate_benchmarks.validate_dashboard_rendering() == []
    package = validate_benchmarks._load(validate_benchmarks.DASHBOARD / "package.yml")
    expected = validate_benchmarks._load(validate_benchmarks.DASHBOARD / "expected.yml")
    assert len(package["evaluations"]) == expected["expected"]["criterion_card_count"] == 18
    assert set(row["classification"] for row in package["evaluations"]) == validate_benchmarks.RATINGS


def test_benchmark_classes_are_deliberately_separate() -> None:
    scoring = validate_benchmarks._load(validate_benchmarks.SCORING / "expected.yml")
    rendering = validate_benchmarks._load(validate_benchmarks.DASHBOARD / "expected.yml")
    assert scoring["benchmark_class"] == "scoring"
    assert rendering["benchmark_class"] == "dashboard_rendering"
    assert scoring["metrics"]["classification_counts"] != rendering["expected"]["classification_counts"]
    policy = (ENCONET / "benchmarks" / "BENCHMARK_POLICY.md").read_text(encoding="utf-8")
    assert "must never be reconciled" in policy and "human re-approval" in policy


def test_locked_expectations_detect_scoring_and_rendering_changes(tmp_path: Path, monkeypatch) -> None:
    scoring = tmp_path / "scoring"
    scoring.mkdir()
    for name in ("input.yml", "expected.yml"):
        (scoring / name).write_bytes((validate_benchmarks.SCORING / name).read_bytes())
    expected = yaml.safe_load((scoring / "expected.yml").read_text(encoding="utf-8"))
    expected["per_criterion_scores"]["APP_B_I"] = 99.9
    (scoring / "expected.yml").write_text(yaml.safe_dump(expected, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(validate_benchmarks, "SCORING", scoring)
    assert "per-criterion scores differ from locked expected values" in validate_benchmarks.validate_scoring()

    dashboard = tmp_path / "dashboard"
    dashboard.mkdir()
    for name in ("package.yml", "expected.yml"):
        (dashboard / name).write_bytes((validate_benchmarks.DASHBOARD / name).read_bytes())
    contract = yaml.safe_load((dashboard / "expected.yml").read_text(encoding="utf-8"))
    contract["expected"]["criterion_card_count"] = 17
    (dashboard / "expected.yml").write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(validate_benchmarks, "DASHBOARD", dashboard)
    assert "dashboard expected property differs: criterion_card_count" in validate_benchmarks.validate_dashboard_rendering()


def test_aggregate_benchmark_mode_and_release_phase_requirement() -> None:
    assert not run_all_validations.benchmarks_required("setup")
    assert run_all_validations.benchmarks_required("setup", requested=True)
    assert not run_all_validations.benchmarks_required("findings_drafted")
    assert run_all_validations.benchmarks_required("findings_approved")
    assert run_all_validations.benchmarks_required("report_ready")
    assert run_all_validations.benchmarks_required("dashboard_ready")
    commands = run_all_validations.benchmark_commands()
    assert list(commands) == run_all_validations.BENCHMARK_ORDER
    assert commands["benchmark_scoring"][-1] == "--scoring"
    assert commands["benchmark_dashboard"][-1] == "--dashboard"

    result = subprocess.run(
        [sys.executable, str(ENCONET / "scripts" / "run_all_validations.py"),
         "--benchmarks", "--no-record"], cwd=ENCONET, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "[PASS] benchmark_scoring" in result.stdout
    assert "[PASS] benchmark_dashboard" in result.stdout
    assert result.stdout.rstrip().endswith("aggregate: PASS")
