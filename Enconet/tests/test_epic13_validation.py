"""EPIC13 phase matrix, aggregate behavior, and wiki hygiene tests."""
from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

import pytest

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import run_all_validations  # noqa: E402
import validate_frontmatter  # noqa: E402
import validate_structure  # noqa: E402


@pytest.fixture
def local_tmp_path():
    with tempfile.TemporaryDirectory(prefix="epic13-", dir=ENCONET / "tests") as directory:
        yield Path(directory)


def wiki_tree(root: Path) -> None:
    for name in ("criteria", "evidence", "findings", "actions", "gates", "dashboards"):
        (root / name).mkdir(parents=True)
    for name in ("index.md", "log.md", "current-status.md"):
        (root / name).write_text(f"# {name}\n", encoding="utf-8")


def test_phase_matrix_is_monotonic_and_failed_runs_full_superset():
    previous: set[str] = set()
    for phase in run_all_validations.PHASES:
        current = {name for name in run_all_validations.ORDER
                   if run_all_validations.applicable(name, phase)}
        assert previous <= current
        previous = current
    assert all(run_all_validations.applicable(name, "failed")
               for name in run_all_validations.ORDER)
    assert not run_all_validations.applicable("report", "findings_approved")
    assert run_all_validations.applicable("report", "report_ready")
    assert not run_all_validations.applicable("dashboard", "report_ready")
    assert run_all_validations.applicable("dashboard", "dashboard_ready")


def test_aggregate_continues_after_failures_and_phase_skips_are_not_passes():
    commands = {name: [name] for name in run_all_validations.ORDER}
    called: list[str] = []

    def fake(command: list[str]) -> tuple[int, str]:
        called.append(command[0])
        return (1, "deliberate failure") if command[0] in {"chunks", "report"} else (0, "ok")

    checks = run_all_validations.run("closed", commands, fake)
    assert called == run_all_validations.ORDER
    assert {check.name for check in checks if check.state == "FAIL"} == {"chunks", "report"}
    setup = run_all_validations.run("setup", commands, fake)
    assert next(check for check in setup if check.name == "raw_sources").detail == "SKIPPED(phase=setup)"
    assert next(check for check in setup if check.name == "structure").state == "PASS"


def test_evaluated_phase_enables_strict_app_b_and_missing_inputs_fail(local_tmp_path: Path):
    app_b = local_tmp_path / "crumbs.json"
    command_map = run_all_validations.commands(
        phase="evaluated", supplier="supplier", db=local_tmp_path / "db.sqlite",
        outputs=local_tmp_path, run_id=None, app_b_json=app_b,
    )
    assert command_map["app_b_json"][-1] == "--strict"
    checks = run_all_validations.run("evaluated", command_map, lambda command: (0, "ok"))
    evaluation = next(check for check in checks if check.name == "evaluation")
    assert evaluation.state == "FAIL" and "could not be discovered" in evaluation.detail


def test_structure_accepts_contract_tree_and_rejects_missing_misnamed_or_misplaced(local_tmp_path: Path):
    wiki_tree(local_tmp_path)
    (local_tmp_path / "evidence" / "matrix.json").write_text("{}\n", encoding="utf-8")
    assert validate_structure.validate(local_tmp_path) == []
    (local_tmp_path / "findings" / "wrong.md").write_text("x\n", encoding="utf-8")
    assert "invalid findings page filename: wrong.md" in validate_structure.validate(local_tmp_path)
    (local_tmp_path / "findings" / "wrong.md").unlink()
    (local_tmp_path / "gates").rmdir()
    assert "required wiki directory missing: gates" in validate_structure.validate(local_tmp_path)


def test_frontmatter_accepts_valid_page_and_rejects_missing_invalid_and_misplaced(local_tmp_path: Path):
    wiki_tree(local_tmp_path)
    page = local_tmp_path / "findings" / "FIND-0001.md"
    page.write_text("""---
id: FIND-0001
type: finding
status: draft
content_origin: mixed
source: GAP-APP_B_I-01
evaluation_run: RUN-20260715-01
criterion_id: APP_B_I
severity: low
confidence: medium
evidence_refs: GAP-APP_B_I-01
basis: fixture
verification_status: pending
approval_ref: n-a
---
# Finding
""", encoding="utf-8")
    assert validate_frontmatter.validate(local_tmp_path) == []
    valid = page.read_text(encoding="utf-8")
    page.write_text(valid.replace("severity: low", "severity: extreme"), encoding="utf-8")
    assert "invalid severity FIND-0001.md: extreme" in validate_frontmatter.validate(local_tmp_path)
    page.write_text(valid.replace("severity: low\n", ""), encoding="utf-8")
    assert "missing frontmatter field FIND-0001.md: severity" in validate_frontmatter.validate(local_tmp_path)
    page.write_text(valid.replace("type: finding", "type: action"), encoding="utf-8")
    assert any("page type/location mismatch" in error for error in validate_frontmatter.validate(local_tmp_path))


def test_new_validators_and_aggregate_append_machine_readable_rows(local_tmp_path: Path):
    manifest = local_tmp_path / "runs.csv"
    validate_structure.append("PASS", 0, "ok", path=manifest, phase="setup")
    validate_frontmatter.append("FAIL", 1, "bad", path=manifest, phase="evidence_reviewed")
    checks = [run_all_validations.Check("structure", "PASS", 0, "ok")]
    run_all_validations.append(checks, "setup", 0, path=manifest)
    rows = list(csv.reader(manifest.read_text(encoding="utf-8").splitlines()))
    assert [row[1] for row in rows] == ["validate_structure.py", "validate_frontmatter.py",
                                       "run_all_validations.py"]
    assert [row[4] for row in rows] == ["0", "1", "0"]
