"""Tests for scripts/check_skill_structure.py (Task C2.3 acceptance).

The acceptance criterion is behavioral: the structure test must FAIL on
duplicate skill names with conflicting ownership. Each test builds a synthetic
workspace + fake agent homes in tmp_path and runs the checker CLI against
them, so the real user-global trees never influence results.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "check_skill_structure.py"


def make_skill(base: Path, dot: str, name: str, with_skill_md: bool = True):
    skill_dir = base / dot / "skills" / name
    skill_dir.mkdir(parents=True)
    if with_skill_md:
        (skill_dir / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")


def run_checker(workspace: Path, claude_home: Path, codex_home: Path):
    for p in (workspace, claude_home, codex_home):
        p.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--workspace-root", str(workspace),
         "--claude-home", str(claude_home),
         "--codex-home", str(codex_home)],
        capture_output=True, text=True)
    return result.returncode, result.stdout


def test_clean_paired_skill_passes(tmp_path):
    """A skill paired at the same scope on both sides is valid (ADR-0014)."""
    make_skill(tmp_path / "home_cc", "", "handoff")
    make_skill(tmp_path / "home_cx", "", "handoff")
    code, out = run_checker(tmp_path / "ws", tmp_path / "home_cc",
                            tmp_path / "home_cx")
    assert code == 0, out
    assert "paired skill 'handoff'" in out


def test_duplicate_name_global_vs_workspace_fails(tmp_path):
    """Same agent, same name at user-global AND workspace scope must fail."""
    ws = tmp_path / "ws"
    make_skill(tmp_path / "home_cc", "", "deploy")
    make_skill(ws, ".claude", "deploy")
    code, out = run_checker(ws, tmp_path / "home_cc", tmp_path / "home_cx")
    assert code == 1
    assert "conflicting ownership" in out and "deploy" in out


def test_duplicate_name_workspace_vs_project_fails(tmp_path):
    ws = tmp_path / "ws"
    make_skill(ws, ".claude", "sieve")
    make_skill(ws / "Enconet", ".claude", "sieve")
    code, out = run_checker(ws, tmp_path / "home_cc", tmp_path / "home_cx")
    assert code == 1
    assert "conflicting ownership" in out


def test_same_name_in_two_projects_passes(tmp_path):
    """Project scopes never shadow each other -> no ownership conflict."""
    ws = tmp_path / "ws"
    make_skill(ws / "Enconet", ".agents", "report")
    make_skill(ws / "TEKOL", ".agents", "report")
    code, out = run_checker(ws, tmp_path / "home_cc", tmp_path / "home_cx")
    assert code == 0, out


def test_paired_skill_scope_mismatch_fails(tmp_path):
    """Same name on both agents but at different scopes breaks the pair."""
    ws = tmp_path / "ws"
    make_skill(tmp_path / "home_cc", "", "handoff")   # claude: user-global
    make_skill(ws, ".agents", "handoff")              # codex: workspace
    code, out = run_checker(ws, tmp_path / "home_cc", tmp_path / "home_cx")
    assert code == 1
    assert "scope mismatch" in out


def test_missing_skill_md_fails(tmp_path):
    ws = tmp_path / "ws"
    make_skill(ws / "Enconet", ".claude", "broken", with_skill_md=False)
    code, out = run_checker(ws, tmp_path / "home_cc", tmp_path / "home_cx")
    assert code == 1
    assert "missing SKILL.md" in out
