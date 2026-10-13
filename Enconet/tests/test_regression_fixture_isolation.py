"""Fail-closed fixture isolation; never restore historical data into a live audit."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import regression_fixture

def test_archive_has_pinned_provenance_and_complete_manifest():
    plan = regression_fixture.validate_archive()
    assert len(plan["candidates"]) == 358
    assert regression_fixture.ARCHIVE_SHA256 == "38018c13eb9c17172c7c3486b4041dbb54e27618f78cfb9989ebb56cbfcfaedf"

def test_corrupt_archive_refused_before_extraction(tmp_path):
    archive = tmp_path / "bad.zip"
    archive.write_bytes(b"not a trusted archive")
    with pytest.raises(ValueError, match="checksum"):
        regression_fixture.validate_archive(archive)

def test_zip_traversal_refused_even_with_matching_archive_checksum(tmp_path):
    archive = tmp_path / "traversal.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("reset-plan.json", json.dumps({"candidates": []}))
        z.writestr("../outside.txt", "unsafe")
    with pytest.raises(ValueError, match="unsafe archive"):
        regression_fixture.validate_archive(archive, hashlib.sha256(archive.read_bytes()).hexdigest())
    assert not (tmp_path.parent / "outside.txt").exists()

def test_live_root_and_existing_target_refused(tmp_path):
    with pytest.raises(ValueError, match="isolated"):
        regression_fixture.require_target(ROOT, ROOT)
    with pytest.raises(ValueError, match="isolated"):
        regression_fixture.require_target(ROOT / "work" / "not-scratch", ROOT)


def test_v4_fixture_uses_local_temp_and_rejects_old_scratch(tmp_path):
    source = tmp_path / "supplier"
    source.mkdir()
    (source / "project-layout.json").write_text(
        '{"schema_version":1,"layout":"v4"}', encoding="utf-8")
    target = source / ".tmp" / "history"
    assert regression_fixture.require_target(target, source) == target
    with pytest.raises(ValueError, match="isolated"):
        regression_fixture.require_target(source / ".test-tmp" / "history", source)
    target.mkdir(parents=True)
    with pytest.raises(ValueError, match="exists"):
        regression_fixture.require_target(target, source)


def test_fixture_maps_current_v4_contracts_to_isolated_legacy_homes(tmp_path):
    source = tmp_path / "supplier"
    source.mkdir()
    (source / "project-layout.json").write_text(
        '{"schema_version":1,"layout":"v4"}', encoding="utf-8")
    for name, text in {"scripts/current.py": "current code", "schemas/spec.json": "{}",
                       "docs/plans/PLAN.md": "current plan", "work/decisions/CX_ADR.md": "own ADR",
                       "work/decisions/CC_ADR.md": "Claude ADR", "work/benchmarks/input.yml": "locked"}.items():
        file = source / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")
    for name in ("db/schema.sql", "wiki/index.md", "wiki/log.md", "wiki/current-status.md"):
        file = source / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
    target = source / ".tmp" / "history"
    regression_fixture.build(target, source=source)
    assert json.loads((target / "project-layout.json").read_text())["layout"] == "legacy"
    assert (target / "scripts/current.py").read_text() == "current code"
    assert (target / "benchmarks/input.yml").read_text() == "locked"
    assert (target / "decisions/CX_ADR.md").read_text() == "own ADR"
    assert not (target / "decisions/CC_ADR.md").exists()
    assert (target / "docs/PLAN.md").read_text() == "current plan"
    assert not (source / "benchmarks").exists()
    assert not (source / "decisions").exists()

def test_no_claude_infrastructure_or_agent_messages_are_copied():
    for path in ("CLAUDE.md", ".claude/commands/audit-close.md", "coordination/messages/CC_test.md", "docs/CC_note.md"):
        assert not regression_fixture.copyable(Path(path))

def test_runtime_coupled_tests_are_explicitly_routed_to_fixture():
    assert regression_fixture.historical_test("test_epic7_requirements.py")
    assert regression_fixture.historical_test("test_evidence_bundle_cli.py")
    assert not regression_fixture.historical_test("test_epic17_agent_commands.py")
    assert not regression_fixture.historical_test("test_regression_fixture_isolation.py")
