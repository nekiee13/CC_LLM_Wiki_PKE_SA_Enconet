"""EA5.2 tests for phase-aware, release-blocking evidence-access validation."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import run_all_validations  # noqa: E402


RUN_ID = "RUN-20260728-01"
EVIDENCE_ROOT = ENCONET / "outputs" / "candidates" / "evidence_access"


def test_evidence_checks_are_additive_ordered_and_phase_aware():
    new_checks = ["evidence_bundle", "report_links", "browser_evidence", "review_package"]
    assert all(name in run_all_validations.ORDER for name in new_checks)
    assert run_all_validations.ORDER.index("evaluation") < run_all_validations.ORDER.index(
        "evidence_bundle"
    ) < run_all_validations.ORDER.index("findings")
    assert run_all_validations.ORDER.index("report") < run_all_validations.ORDER.index(
        "report_links"
    ) < run_all_validations.ORDER.index("browser_evidence") < run_all_validations.ORDER.index(
        "dashboard"
    ) < run_all_validations.ORDER.index("review_package")
    assert not run_all_validations.applicable("evidence_bundle", "evidence_reviewed")
    assert run_all_validations.applicable("evidence_bundle", "evaluated")
    assert not run_all_validations.applicable("report_links", "findings_approved")
    assert run_all_validations.applicable("report_links", "report_ready")
    assert run_all_validations.applicable("browser_evidence", "report_ready")
    assert not run_all_validations.applicable("review_package", "report_ready")
    assert run_all_validations.applicable("review_package", "dashboard_ready")


def test_evidence_commands_name_exact_artifact_paths_and_browser_contract(tmp_path: Path):
    command_map = run_all_validations.commands(
        phase="closed", supplier="enconet", db=ENCONET / "db" / "nqa_audit.sqlite",
        outputs=tmp_path / "output root", run_id=RUN_ID,
        app_b_json=ENCONET / "fixture.json", no_record=True,
    )
    root = tmp_path / "output root" / "candidates" / "evidence_access"
    run_root = root / RUN_ID
    assert command_map["evidence_bundle"][-1] == str(run_root / "evidence_bundle.json")
    assert command_map["report_links"][2:5] == [
        str(run_root / "enconet_appendix_b_evaluation_report.md"),
        str(run_root / "enconet_appendix_b_dashboard.html"),
        str(tmp_path / "output root" / "enconet_appendix_b_evaluation_package.json"),
    ]
    assert command_map["browser_evidence"] == [
        sys.executable, str(ENCONET / "scripts" / "browser_harness.py"), "check",
        str(run_root / "enconet_appendix_b_dashboard.html"), "--artifacts",
        str(root / "validation_artifacts" / "browser_evidence"), "--require-interactive",
    ]
    assert command_map["review_package"][-1] == str(root / "portable_package")


def test_check_summary_preserves_exact_command_exit_count_and_paths():
    command = (
        sys.executable, str(ENCONET / "scripts" / "validate_review_package.py"),
        str(EVIDENCE_ROOT / "portable_package"),
    )
    check = run_all_validations.Check(
        "review_package", "PASS", 0,
        "validate_review_package: PASS - files=6 runs=1 - portable_package", command,
    )
    rendered = run_all_validations.format_check(check)
    assert "exit=0" in rendered
    assert "files=6 runs=1" in rendered
    encoded = rendered.split(" command=", 1)[1].split(" - ", 1)[0]
    assert json.loads(encoded) == list(command)


def test_broken_report_link_blocks_aggregate_while_evaluation_passes(tmp_path: Path):
    run_root = EVIDENCE_ROOT / RUN_ID
    report = tmp_path / "evaluation_report.md"
    viewer = tmp_path / "evidence_explorer.html"
    package = tmp_path / "evaluation_package.json"
    shutil.copyfile(run_root / "enconet_appendix_b_evaluation_report.md", report)
    shutil.copyfile(run_root / "enconet_appendix_b_dashboard.html", viewer)
    shutil.copyfile(ENCONET / "outputs" / "enconet_appendix_b_evaluation_package.json", package)
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            "#evidence/crumb/CRUMB-DOC-0021-APP_B_I-0003",
            "#evidence/crumb/CRUMB-DOC-9999-APP_B_I-9999", 1,
        ),
        encoding="utf-8",
    )
    commands = {name: [name] for name in run_all_validations.ORDER}
    commands["report_links"] = [
        sys.executable, str(ENCONET / "scripts" / "validate_report_links.py"),
        str(report), str(viewer), str(package), "--project-root", str(ENCONET),
    ]

    def executor(command: list[str]) -> tuple[int, str]:
        if command == commands["report_links"]:
            return run_all_validations.execute(command)
        return 0, "fixture: PASS"

    checks = run_all_validations.run("closed", commands, executor)
    assert next(check for check in checks if check.name == "evaluation").state == "PASS"
    broken = next(check for check in checks if check.name == "report_links")
    assert broken.state == "FAIL" and broken.code == 1
    assert "report citation" in broken.detail
    assert "CRUMB-DOC-9999-APP_B_I-9999" in broken.detail
