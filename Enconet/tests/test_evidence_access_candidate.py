"""EA6.1 controlled production-candidate contract tests."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import validate_evidence_access_candidate as candidate  # noqa: E402


CONTRACT = ENCONET / "schemas" / "evidence_access_release_candidate.yml"


def test_contract_pins_candidate_lineage_counts_and_approved_baseline():
    value = candidate.load_contract(CONTRACT)
    assert value["schema_version"] == "1.0"
    assert value["candidate_id"] == "EA6.1-RUN-20260728-01"
    assert value["run_id"] == "RUN-20260728-01"
    assert value["expected_counts"] == {"criteria": 18, "crumbs": 62}
    assert len(value["source_sha256"]) == 14
    assert value["approved_baseline"]["report_sha256"] == (
        "0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175"
    )
    assert value["approved_baseline"]["dashboard_sha256"] == (
        "15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07"
    )


def test_candidate_passes_without_mutating_candidate_or_approved_outputs():
    protected = [
        ENCONET / "outputs" / "enconet_appendix_b_evaluation_report.md",
        ENCONET / "outputs" / "enconet_appendix_b_dashboard.html",
    ]
    package = ENCONET / "outputs" / "candidates" / "evidence_access" / "portable_package"
    before = {path: path.read_bytes() for path in [*protected, *[p for p in package.rglob("*") if p.is_file()]]}
    errors, summary = candidate.validate(CONTRACT, ENCONET)
    assert errors == []
    assert summary == {"run_id": "RUN-20260728-01", "files": 6, "criteria": 18, "crumbs": 62}
    assert {path: path.read_bytes() for path in before} == before


def test_candidate_fails_closed_on_manifest_drift(tmp_path: Path):
    root = tmp_path / "project"
    source = ENCONET / "outputs" / "candidates" / "evidence_access" / "portable_package"
    shutil.copytree(source, root / "outputs" / "candidates" / "evidence_access" / "portable_package")
    (root / "outputs").mkdir(exist_ok=True)
    for name in ("enconet_appendix_b_evaluation_report.md", "enconet_appendix_b_dashboard.html"):
        shutil.copyfile(ENCONET / "outputs" / name, root / "outputs" / name)
    manifest = root / "outputs" / "candidates" / "evidence_access" / "portable_package" / "package_manifest.json"
    manifest.write_text(manifest.read_text(encoding="utf-8") + "tamper", encoding="utf-8")
    errors, _ = candidate.validate(CONTRACT, root)
    assert any("candidate manifest hash mismatch" in error for error in errors)


def test_cli_reports_exact_candidate(capsys):
    assert candidate.main(["--contract", str(CONTRACT), "--project-root", str(ENCONET)]) == 0
    output = capsys.readouterr().out
    assert "validate_evidence_access_candidate: PASS" in output
    assert "files=6 criteria=18 crumbs=62" in output
