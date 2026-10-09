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
    with pytest.raises(ValueError, match="exists"):
        regression_fixture.require_target(tmp_path, ROOT)

def test_no_claude_infrastructure_or_agent_messages_are_copied():
    for path in ("CLAUDE.md", ".claude/commands/audit-close.md", "coordination/messages/CC_test.md", "docs/CC_note.md"):
        assert not regression_fixture.copyable(Path(path))

def test_runtime_coupled_tests_are_explicitly_routed_to_fixture():
    assert regression_fixture.historical_test("test_epic7_requirements.py")
    assert regression_fixture.historical_test("test_evidence_bundle_cli.py")
    assert not regression_fixture.historical_test("test_epic17_agent_commands.py")
    assert not regression_fixture.historical_test("test_regression_fixture_isolation.py")
