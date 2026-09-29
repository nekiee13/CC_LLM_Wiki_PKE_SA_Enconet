"""EK-1.2 continuity checks use only disposable, invented project records."""
from __future__ import annotations

import hashlib
import importlib.util
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import yaml


PROJECT = Path(__file__).resolve().parents[2]
SUPPORT = ("audit_state.py", "db_util.py", "project_paths.py")


def snapshot(root: Path):
    return {str(path.relative_to(root)): (
        hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns
    ) if path.is_file() else None for path in root.rglob("*")}


class LocalContinuityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ek12-continuity-")
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name) / "Rad s razmacima Županija"
        self.project = self.workspace / "Ekonerg"
        self.sibling = self.workspace / "Enconet"
        self.nested = self.project / "Enconet"
        for directory in (self.project / "scripts", self.sibling, self.nested):
            directory.mkdir(parents=True)
        for directory in (self.sibling, self.nested):
            (directory / "HANDOFF.md").write_text("wrong project\n", encoding="utf-8")
        for name in SUPPORT:
            shutil.copyfile(PROJECT / "scripts" / name, self.project / "scripts" / name)
        target = PROJECT / "scripts/session_continuity.py"
        self.assertTrue(target.is_file(), "local continuity script is missing")
        shutil.copyfile(target, self.project / "scripts/session_continuity.py")

    def invoke(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, "-B", str(self.project / "scripts/session_continuity.py"), *args],
            cwd=cwd or self.workspace, capture_output=True, text=True, encoding="utf-8",
            timeout=30, env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONPATH": ""},
        )

    def load(self):
        saved = {key: sys.modules.pop(key, None)
                 for key in ("audit_state", "db_util", "project_paths")}
        sys.path.insert(0, str(self.project / "scripts"))
        def cleanup():
            sys.path.remove(str(self.project / "scripts"))
            for key, prior in saved.items():
                sys.modules.pop(key, None)
                if prior is not None:
                    sys.modules[key] = prior
        self.addCleanup(cleanup)
        spec = importlib.util.spec_from_file_location(
            "ek12_fake_continuity", self.project / "scripts/session_continuity.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def records(self, phase="setup", head="abc123"):
        (self.project / "HANDOFF.md").write_text(
            f"**Git:** `{head}`\n", encoding="utf-8")
        wiki = self.project / "wiki"
        wiki.mkdir(exist_ok=True)
        (wiki / "current-status.md").write_text(
            f"phase: **{phase}**\n## Next action\nSynthetic next action.\n",
            encoding="utf-8")
        (wiki / "index.md").write_text("# Synthetic index\n", encoding="utf-8")
        (self.project / "project-state.yml").write_text(
            yaml.safe_dump({"phase": phase, "gates": {}}), encoding="utf-8")

    def test_missing_records_warn_from_three_working_folders_without_wrong_writes(self):
        before = [snapshot(p) for p in (self.sibling, self.nested)]
        for cwd in (self.project, self.workspace, self.workspace.parent):
            result = self.invoke(cwd=cwd)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn(str(self.project / "wiki/current-status.md"), result.stdout)
            self.assertNotIn(str(self.sibling), result.stdout)
            self.assertNotIn(str(self.nested), result.stdout)
            self.assertIn("WARNING: missing continuity record", result.stdout)
        self.assertEqual(before, [snapshot(p) for p in (self.sibling, self.nested)])

    def test_runs_without_any_enconet_folder(self):
        shutil.rmtree(self.sibling)
        shutil.rmtree(self.nested)
        self.assertEqual(0, self.invoke().returncode)
        self.assertFalse(self.sibling.exists())
        self.assertFalse(self.nested.exists())

    def test_global_cli_paths_are_local_even_when_records_are_missing(self):
        before = snapshot(self.sibling)
        for option in ("--handoff", "--current-status", "--index", "--state", "--database"):
            result = self.invoke(option, str(self.sibling / "foreign.md"))
            self.assertEqual(1, result.returncode, (option, result.stdout, result.stderr))
            self.assertIn("local", result.stderr.lower())
            self.assertEqual(before, snapshot(self.sibling))

    def test_relative_cli_paths_anchor_to_project_not_caller(self):
        self.records()
        result = self.invoke("--handoff", "HANDOFF.md", cwd=self.workspace.parent)
        self.assertEqual(1, result.returncode)  # no Git repo: explicit failure
        self.assertNotIn("No such file", result.stderr)
        self.assertNotIn("missing continuity record", result.stdout)

    def test_direct_inspection_refuses_foreign_handoff_before_read(self):
        module = self.load()
        before = snapshot(self.sibling)
        with self.assertRaises(ValueError):
            module.inspect_start(handoff=self.sibling / "HANDOFF.md")
        self.assertEqual(before, snapshot(self.sibling))

    def test_direct_database_probe_refuses_foreign_path(self):
        module = self.load()
        with self.assertRaises(ValueError):
            module.unfinished_evaluations(self.sibling / "not-created.sqlite")
        self.assertFalse((self.sibling / "not-created.sqlite").exists())

    def test_missing_database_does_not_create_one(self):
        module = self.load()
        self.assertEqual([], module.unfinished_evaluations(self.project / "db/missing.sqlite"))
        self.assertFalse((self.project / "db").exists())

    def test_database_query_is_read_only_and_releases_file(self):
        db = self.project / "db/audit.sqlite"
        db.parent.mkdir()
        with closing(sqlite3.connect(db)) as conn:
            conn.execute("CREATE TABLE evaluation_runs(run_id TEXT, completed_at TEXT)")
            conn.executemany("INSERT INTO evaluation_runs VALUES (?, ?)", [
                ("RUN-2", None), ("RUN-1", None), ("RUN-3", "done")])
            conn.commit()
        module = self.load()
        before = snapshot(self.project)
        with patch.object(module.sqlite3, "connect", wraps=sqlite3.connect) as connect:
            self.assertEqual(["RUN-1", "RUN-2"], module.unfinished_evaluations(db))
            self.assertTrue(connect.call_args.kwargs.get("uri"))
            self.assertIn("mode=ro", connect.call_args.args[0])
        self.assertEqual(before, snapshot(self.project))
        db.rename(self.project / "db/moved.sqlite")

    def test_setup_records_have_no_resume_warning(self):
        self.records()
        module = self.load()
        info, warnings = module.inspect_start(actual_head="abc123")
        self.assertIn("current_state: setup", info)
        self.assertEqual([], warnings)

    def test_in_progress_phase_and_unfinished_run_warn_without_transition(self):
        self.records("registered")
        db = self.project / "db/nqa_audit.sqlite"
        db.parent.mkdir()
        with closing(sqlite3.connect(db)) as conn:
            conn.execute("CREATE TABLE evaluation_runs(run_id TEXT, completed_at TEXT)")
            conn.execute("INSERT INTO evaluation_runs VALUES ('RUN-SYNTHETIC', NULL)")
            conn.commit()
        before = snapshot(self.project)
        module = self.load()
        info, warnings = module.inspect_start(actual_head="abc123")
        self.assertIn("unfinished_evaluation_runs: RUN-SYNTHETIC", info)
        self.assertTrue(any("IN-PROGRESS" in warning for warning in warnings))
        self.assertTrue(any("unfinished evaluation runs" in warning for warning in warnings))
        self.assertEqual(before, snapshot(self.project))

    def test_git_and_state_divergence_still_warn(self):
        self.records("setup", head="abc123")
        (self.project / "wiki/current-status.md").write_text(
            "phase: **registered**\n## Next action\nSynthetic.\n", encoding="utf-8")
        module = self.load()
        _, warnings = module.inspect_start(actual_head="fffffff")
        self.assertTrue(any("Git divergence" in warning for warning in warnings))
        self.assertTrue(any("state divergence" in warning for warning in warnings))

    def test_junction_and_hardlink_inputs_are_refused(self):
        module = self.load()
        foreign = self.sibling / "state.yml"
        foreign.write_text("phase: setup\n", encoding="utf-8")
        os.link(foreign, self.project / "project-state.yml")
        with self.assertRaises(ValueError):
            module.inspect_start(state=self.project / "project-state.yml")
        link = self.project / "wiki"
        target = self.sibling / "wiki"
        target.mkdir()
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.addCleanup(link.rmdir)
        else:
            link.symlink_to(target, target_is_directory=True)
            self.addCleanup(link.unlink)
        with self.assertRaises(ValueError):
            module.inspect_start(current_status=link / "current-status.md")

    def test_git_identity_comes_from_actual_shared_root(self):
        for args in (("init", "-q"),
                     ("-c", "user.name=EK Test", "-c", "user.email=ek@example.invalid",
                      "commit", "--allow-empty", "-qm", "synthetic")):
            result = subprocess.run(["git", *args], cwd=self.workspace,
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
        module = self.load()
        head = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                       cwd=self.workspace, text=True).strip()
        self.assertEqual(head, module.git_head())
        self.assertNotEqual(self.project, self.workspace)

    def test_git_identity_also_works_when_project_is_git_root(self):
        for args in (("init", "-q"),
                     ("-c", "user.name=EK Test", "-c", "user.email=ek@example.invalid",
                      "commit", "--allow-empty", "-qm", "synthetic")):
            result = subprocess.run(["git", *args], cwd=self.project,
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
        module = self.load()
        head = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                       cwd=self.project, text=True).strip()
        self.assertEqual(head, module.git_head())


if __name__ == "__main__":
    unittest.main()
