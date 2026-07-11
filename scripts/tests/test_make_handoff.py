"""C3 acceptance tests for scripts/make_handoff.py."""
from __future__ import annotations
import importlib.util, json, os, subprocess, sys
from argparse import Namespace
from pathlib import Path
import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "make_handoff.py"
SPEC = importlib.util.spec_from_file_location("make_handoff", SCRIPT)
mh = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mh)

def args(root: Path, **kw):
    values = dict(project_root=str(root), project_id="test/Prøject", source_agent="codex",
        status="partial", objective="Phase: test", completed=[], decision=[], check=[],
        index_state="unknown", blocker=[], next_action="Continue safely.", follow_up=[])
    values.update(kw); return Namespace(**values)

def git(cwd, *parts):
    subprocess.run(["git", *parts], cwd=cwd, check=True, capture_output=True, text=True, encoding="utf-8")

def init_repo(root):
    git(root, "init", "-b", "main"); git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test"); (root / "tracked.txt").write_text("one", encoding="utf-8")
    git(root, "add", "tracked.txt"); git(root, "commit", "-m", "initial")

def test_no_git_publishes_nogit_with_warning(tmp_path):
    record = mh.publish(args(tmp_path))
    assert record.name.endswith("-nogit.md") and "WARNING: Git metadata unavailable" in record.read_text(encoding="utf-8")
    assert mh.validate_text(record.read_text(encoding="utf-8"), record) == []

def test_dirty_worktree_and_detached_head_are_visible(tmp_path):
    init_repo(tmp_path); (tmp_path / "tracked.txt").write_text("dirty", encoding="utf-8")
    assert mh.git_facts(tmp_path)["dirty"] is True
    git(tmp_path, "checkout", "--detach"); assert mh.git_facts(tmp_path)["detached"] is True

def test_stale_index_state_is_rendered(tmp_path):
    record = mh.publish(args(tmp_path, index_state="stale: indexed HEAD abc != current def"))
    assert "stale: indexed HEAD abc != current def" in record.read_text(encoding="utf-8")

def test_passed_check_without_command_and_exit_code_fails(tmp_path):
    record = mh.publish(args(tmp_path)); text = record.read_text(encoding="utf-8").replace(
        "validation_checks_json: []", 'validation_checks_json: [{"name":"bad","state":"passed"}]')
    assert any("passed requires command" in e for e in mh.validate_text(text, record))

def test_failed_validation_state_is_valid_evidence(tmp_path):
    check = json.dumps({"name":"suite","state":"failed","command":"pytest","exit_code":1,"summary":"one failure"})
    assert "**failed**" in mh.publish(args(tmp_path, check=[check])).read_text(encoding="utf-8")

def test_windows_safe_pipe_check_format():
    check = mh.parse_check("passed|suite|python -m pytest|0|all passed")
    assert check["state"] == "passed" and check["exit_code"] == 0

def test_repeat_runs_never_overwrite_history(tmp_path):
    first = mh.publish(args(tmp_path)); before = first.read_text(encoding="utf-8"); second = mh.publish(args(tmp_path))
    assert first != second and first.read_text(encoding="utf-8") == before
    assert second.name in (tmp_path / "HANDOFF.md").read_text(encoding="utf-8")

def test_interrupted_pointer_write_leaves_prior_pointer(tmp_path, monkeypatch):
    mh.publish(args(tmp_path)); pointer = tmp_path / "HANDOFF.md"; before = pointer.read_text(encoding="utf-8"); real = mh.atomic_write
    def fail(path, text):
        if path.name == "HANDOFF.md": raise OSError("simulated interruption")
        real(path, text)
    monkeypatch.setattr(mh, "atomic_write", fail)
    with pytest.raises(OSError): mh.publish(args(tmp_path))
    assert pointer.read_text(encoding="utf-8") == before

def test_unicode_path_and_cp1252_console_validation(tmp_path):
    root = tmp_path / "Zażółć"; root.mkdir(); record = mh.publish(args(root)); env = os.environ.copy(); env["PYTHONIOENCODING"] = "cp1252:replace"
    result = subprocess.run([sys.executable, str(SCRIPT), "--validate", str(record)], text=True, encoding="cp1252", errors="replace", capture_output=True, env=env)
    assert result.returncode == 0, result.stderr

def test_staleness_warns_after_head_moves(tmp_path, capsys):
    init_repo(tmp_path); mh.publish(args(tmp_path)); (tmp_path / "tracked.txt").write_text("two", encoding="utf-8")
    git(tmp_path, "add", "tracked.txt"); git(tmp_path, "commit", "-m", "move head")
    assert mh.check_staleness(tmp_path) == 0
    assert "WARN: handoff is stale" in capsys.readouterr().out
