"""EA6.2 executable operations, recovery, architecture, and upgrade documentation tests."""
from __future__ import annotations

import sys
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import validate_evidence_access_docs as docs_validator  # noqa: E402


CONTRACT = ENCONET / "schemas" / "evidence_access_operations.yml"
OPERATIONS = ENCONET / "docs" / "EVIDENCE_ACCESS_OPERATIONS.md"
ARCHITECTURE = ENCONET / "docs" / "EVIDENCE_ACCESS_ARCHITECTURE.md"
UPGRADE = ENCONET / "docs" / "EVIDENCE_ACCESS_UPGRADE_GUIDE.md"


def test_documentation_contract_covers_commands_and_clean_rehearsal():
    contract = docs_validator.load_contract(CONTRACT)
    assert contract["schema_version"] == "1.0"
    assert contract["python"] == r"C:\xPY\vEnv\WikiEnconet\python.exe"
    assert len(contract["commands"]) >= 8
    assert {row["id"] for row in contract["commands"]} >= {
        "verify-environment", "validate-candidate", "validate-package", "validate-uat",
        "aggregate", "build-portable", "open-workspace", "hash-baseline",
    }
    assert contract["rehearsal"]["expected_manifest_sha256"] == (
        "efcbada9b59862f8f0ba00c739147a2a5e4076d0009f87b3af539a5cb60a0012"
    )


def test_all_documented_commands_and_required_topics_validate():
    errors, summary = docs_validator.validate(CONTRACT, OPERATIONS, ARCHITECTURE, UPGRADE, ENCONET)
    assert errors == []
    assert summary["commands"] >= 8
    assert summary["rehearsal_files"] == 6
    assert summary["rehearsal_runs"] == 1


def test_docs_distinguish_current_operation_from_future_upgrade():
    operations = OPERATIONS.read_text(encoding="utf-8")
    architecture = ARCHITECTURE.read_text(encoding="utf-8")
    upgrade = UPGRADE.read_text(encoding="utf-8")
    for marker in ["Conda environment", "Open and use", "Build", "Validate", "Transfer", "Recovery", "Failure guide"]:
        assert marker in operations
    for marker in ["Data flow", "Trust boundaries", "Artifact model", "Extension points"]:
        assert marker in architecture
    for marker in ["Current approved behavior", "Upgrade decision gate", "Compatibility contract", "Rollback plan"]:
        assert marker in upgrade
    assert "streamlit run" not in (operations + architecture + upgrade).lower()
    assert "a web service is not required" in architecture.lower()


def test_missing_command_marker_fails_closed(tmp_path: Path):
    broken = tmp_path / "operations.md"
    broken.write_text(OPERATIONS.read_text(encoding="utf-8").replace("command:validate-candidate", "command:removed"), encoding="utf-8")
    errors, _ = docs_validator.validate(CONTRACT, broken, ARCHITECTURE, UPGRADE, ENCONET, rehearse=False)
    assert any("missing documented command: validate-candidate" in error for error in errors)


def test_cli_reports_clean_rehearsal(capsys):
    assert docs_validator.main([
        "--contract", str(CONTRACT), "--operations", str(OPERATIONS),
        "--architecture", str(ARCHITECTURE), "--upgrade", str(UPGRADE),
        "--project-root", str(ENCONET),
    ]) == 0
    output = capsys.readouterr().out
    assert "validate_evidence_access_docs: PASS" in output
    assert "rehearsal_files=6 rehearsal_runs=1" in output
