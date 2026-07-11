from __future__ import annotations
import ast
from pathlib import Path

from verify_install import verify_installation

ROOT = Path(__file__).parents[1]
TOOLS = ROOT / "tools"


def test_only_non_mutating_manifest_verifier_remains_active():
    active = sorted(p.name for p in TOOLS.glob("*.py"))
    assert active == ["verify_data_manifest.py"]


def test_archived_tool_inventory_and_tombstone():
    archive = TOOLS / "_archive"
    expected = {"check_files.py", "fix_files.py", "fix_structure.py", "fix_init_files.py",
        "print_run_pipeline_sig.py", "fix_mor_rule_refs.py", "fix_mor_taxonomy_id.py",
        "fix_nqa1_to_midlayer.py", "fix_rule_refs_from_criterion.py"}
    assert expected.issubset({p.name for p in archive.glob("*.py")})
    assert "must not be executed" in (archive / "README.md").read_text(encoding="utf-8")


def test_no_active_tool_uses_tools_directory_as_project_root():
    for path in TOOLS.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        text = ast.unparse(tree)
        assert "Path(__file__).parent" not in text


def test_verifier_distinguishes_structure_failure_without_mutation(tmp_path, capsys):
    assert verify_installation(tmp_path) == 1
    output = capsys.readouterr().out
    assert "structure_errors:" in output
    assert "no repair script is recommended" in output
    assert list(tmp_path.iterdir()) == []
