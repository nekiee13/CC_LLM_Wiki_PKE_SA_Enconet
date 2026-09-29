"""EK-1.2: relocated support tools must write inside their own project."""
from __future__ import annotations

import hashlib
import ast
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
TOOLS = ("agent_coord.py", "run_validation.py", "make_handoff.py",
         "check_guidance_drift.py", "check_skill_structure.py")


def snapshot(root: Path) -> dict[str, tuple[str, int] | None]:
    return {
        str(path.relative_to(root)): (
            (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            if path.is_file() else None
        )
        for path in root.rglob("*")
    }


class LocalSupportPathTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ek12-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name) / "Rad s razmacima Županija"
        self.project = self.workspace / "Ekonerg"
        self.sibling = self.workspace / "Enconet"
        self.nested = self.project / "Enconet"
        for path in (self.project / "scripts", self.sibling / "coordination",
                     self.nested / "coordination"):
            path.mkdir(parents=True)
        for wrong in (self.sibling, self.nested):
            (wrong / "HANDOFF.md").write_text("untouched handoff\n", encoding="utf-8")
            (wrong / "coordination" / "BOARD.md").write_text(
                "untouched board\n", encoding="utf-8")
        for name in TOOLS:
            shutil.copyfile(PROJECT / "scripts" / name,
                            self.project / "scripts" / name)
        shutil.copyfile(PROJECT / "handoff_schema.yml",
                        self.project / "handoff_schema.yml")

    def command(self, name: str, *args: str, cwd: Path | None = None):
        result = self.invoke(name, *args, cwd=cwd)
        self.assertEqual(0, result.returncode,
                         (result.stderr or "") + (result.stdout or ""))
        return result.stdout

    def invoke(self, name: str, *args: str, cwd: Path | None = None):
        result = subprocess.run(
            [sys.executable, "-B", str(self.project / "scripts" / name), *args],
            cwd=cwd or self.workspace, text=True, encoding="utf-8",
            capture_output=True, timeout=30,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return result

    def test_coordination_never_targets_sibling_or_nested_enconet(self):
        before = [snapshot(path) for path in (self.sibling, self.nested)]
        self.command("agent_coord.py", "claim", "EK-FAKE", "--agent", "codex",
                     cwd=self.project)
        self.command("agent_coord.py", "message", "--from", "codex",
                     "--to", "claude-code", "--type", "note", "--task", "EK-FAKE",
                     "--topic", "fake-path-check", "--body", "synthetic",
                     cwd=self.workspace)
        self.command("agent_coord.py", "status", "--write",
                     cwd=self.workspace.parent)
        self.assertTrue((self.project / "coordination" / "claims" / "EK-FAKE.yml").is_file())
        self.assertEqual(1, len(list((self.project / "coordination" / "messages").glob("CX_*.md"))))
        self.assertTrue((self.project / "coordination" / "BOARD.md").is_file())
        self.assertEqual(before, [snapshot(path) for path in (self.sibling, self.nested)])

    def test_handoff_default_and_runner_list_are_project_local(self):
        before = [snapshot(path) for path in (self.sibling, self.nested)]
        output = self.command("run_validation.py", "--list", cwd=self.workspace.parent)
        self.assertIn("L0", output)
        self.assertIn(str(self.project / "scripts" / "agent_coord.py"), output)
        self.assertNotIn(str(self.sibling), output)
        self.assertNotIn(str(self.nested), output)
        self.command("make_handoff.py", "--source-agent", "codex",
                     "--status", "partial", cwd=self.workspace.parent)
        pointer = self.project / "HANDOFF.md"
        self.assertTrue(pointer.is_file())
        self.assertEqual(1, len(list((self.project / "handoffs").glob("*.md"))))
        self.assertEqual(before, [snapshot(path) for path in (self.sibling, self.nested)])

    def test_support_tools_work_without_any_enconet_folder(self):
        shutil.rmtree(self.sibling)
        shutil.rmtree(self.nested)
        self.command("agent_coord.py", "claim", "EK-ALONE", "--agent", "codex")
        self.command("agent_coord.py", "status", "--write")
        self.command("make_handoff.py", "--source-agent", "codex",
                     "--status", "partial")
        self.assertTrue((self.project / "HANDOFF.md").exists())
        self.assertFalse(self.sibling.exists())
        self.assertFalse(self.nested.exists())

    def test_handoff_uses_project_output_with_shared_git_root(self):
        before = [snapshot(path) for path in (self.sibling, self.nested)]
        for args in (("init", "-q"),
                     ("-c", "user.name=EK Test", "-c", "user.email=ek@example.invalid",
                      "commit", "--allow-empty", "-qm", "synthetic baseline")):
            result = subprocess.run(["git", *args], cwd=self.workspace,
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(0, result.returncode, result.stderr)
        self.command("make_handoff.py", "--source-agent", "codex",
                     "--status", "partial", cwd=self.project)
        pointer = self.project / "HANDOFF.md"
        self.assertTrue(pointer.is_file())
        records = list((self.project / "handoffs").glob("*.md"))
        self.assertEqual(1, len(records))
        body = records[0].read_text(encoding="utf-8")
        self.assertIn(f"Git root: `{self.workspace.as_posix()}", body)
        self.assertEqual(before, [snapshot(path) for path in (self.sibling, self.nested)])

    def test_guidance_and_skill_checks_use_local_scope(self):
        (self.sibling / "doc").mkdir()
        (self.sibling / "doc" / "GUIDANCE_PAIRS.json").write_text(
            '{"pairs": []}', encoding="utf-8")
        before = [snapshot(path) for path in (self.sibling, self.nested)]
        check = subprocess.run(
            [sys.executable, "-B", str(self.project / "scripts" /
                                           "check_guidance_drift.py")],
            cwd=self.workspace, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(1, check.returncode)
        self.assertIn(str(self.project / "doc" / "GUIDANCE_PAIRS.json"),
                      check.stderr)
        self.assertNotIn(str(self.sibling / "doc"), check.stderr)
        homes = self.workspace / "agent homes"
        (homes / "claude").mkdir(parents=True)
        (homes / "codex").mkdir()
        (self.project / ".agents" / "skills").mkdir(parents=True)
        output = self.command(
            "check_skill_structure.py", "--list", "--claude-home",
            str(homes / "claude"), "--codex-home", str(homes / "codex"))
        self.assertIn(str(self.project / ".agents" / "skills"), output)
        self.assertNotIn(str(self.sibling / ".agents"), output)
        self.assertNotIn(str(self.nested / ".agents"), output)
        self.assertEqual(before, [snapshot(path) for path in (self.sibling, self.nested)])

    def test_validator_step_working_folders_are_project_local(self):
        script = self.project / "scripts" / "run_validation.py"
        spec = importlib.util.spec_from_file_location("ek12_fake_runner", script)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        self.addCleanup(sys.modules.pop, spec.name, None)
        spec.loader.exec_module(module)
        self.assertEqual(self.project, module.PROJECT)
        self.assertEqual(self.project / "sieving", module.SIEVING)
        for layer in module.build_layers():
            for step in layer.steps:
                self.assertTrue(step.cwd == self.project or
                                self.project in step.cwd.parents,
                                (layer.name, step.name, step.cwd))
                for arg in step.command or []:
                    self.assertNotIn(str(self.sibling), arg)
                    self.assertNotIn(str(self.nested), arg)

    def test_handoff_cli_refuses_foreign_output_root(self):
        before = [snapshot(path) for path in (self.sibling, self.nested)]
        result = self.invoke("make_handoff.py", "--project-root",
                             str(self.sibling), "--status", "partial")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("project root", result.stderr.lower())
        self.assertEqual(before, [snapshot(path) for path in (self.sibling, self.nested)])

    def test_coordination_identifiers_cannot_form_paths(self):
        self.command("agent_coord.py", "claim", "SAFE", "--agent", "codex")
        before = snapshot(self.workspace)
        commands = (
            ("claim", "../ESCAPED", "--agent", "codex"),
            ("claim", "..\\ESCAPED", "--agent", "codex"),
            ("release", "../ESCAPED", "--agent", "codex"),
            ("message", "--from", "codex", "--to", "claude-code",
             "--type", "note", "--task", "SAFE", "--topic", "../bad", "--body", "fake"),
        )
        for args in commands:
            with self.subTest(args=args):
                result = self.invoke("agent_coord.py", *args)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("identifier", result.stderr.lower())
                self.assertEqual(before, snapshot(self.workspace))

    def redirect(self, link: Path, target: Path):
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.addCleanup(link.rmdir)
        else:
            link.symlink_to(target, target_is_directory=True)
            self.addCleanup(link.unlink)

    def test_coordination_redirect_is_refused_before_writes(self):
        self.redirect(self.project / "coordination", self.sibling / "coordination")
        before = snapshot(self.sibling)
        result = self.invoke("agent_coord.py", "claim", "SAFE", "--agent", "codex")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("redirected", result.stderr.lower())
        self.assertEqual(before, snapshot(self.sibling))

    def test_handoff_redirect_is_refused_before_writes(self):
        self.redirect(self.project / "handoffs", self.sibling / "coordination")
        before = snapshot(self.sibling)
        result = self.invoke("make_handoff.py", "--status", "partial")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("redirected", result.stderr.lower())
        self.assertEqual(before, snapshot(self.sibling))

    def test_validator_refuses_handoff_pointer_traversal(self):
        (self.project / "HANDOFF.md").write_text(
            "[record](handoffs/../../Enconet/HANDOFF.md)\n", encoding="utf-8")
        script = self.project / "scripts" / "run_validation.py"
        spec = importlib.util.spec_from_file_location("ek12_pointer_runner", script)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        self.addCleanup(sys.modules.pop, spec.name, None)
        spec.loader.exec_module(module)
        self.assertIsNone(module._pointer_record())

    def test_handoff_validation_cannot_read_sibling_record(self):
        result = self.invoke("make_handoff.py", "--validate",
                             str(self.sibling / "HANDOFF.md"))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("local", result.stderr.lower())

    def test_support_imports_require_no_shared_scripts_or_packages(self):
        for name in TOOLS:
            tree = ast.parse((self.project / "scripts" / name).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    self.assertEqual(0, node.level, (name, node.lineno))
                    modules = [(node.module or "").split(".")[0]]
                else:
                    continue
                self.assertTrue(set(modules) <= sys.stdlib_module_names,
                                (name, node.lineno, modules))

    def test_skill_default_ignores_shared_and_sibling_scopes(self):
        for wrong in (self.workspace / ".agents" / "skills" / "broken",
                      self.sibling / ".agents" / "skills" / "broken",
                      self.nested / ".agents" / "skills" / "broken"):
            wrong.mkdir(parents=True)
        local = self.project / ".agents" / "skills" / "local"
        local.mkdir(parents=True)
        (local / "SKILL.md").write_text("synthetic\n", encoding="utf-8")
        output = self.command("check_skill_structure.py", "--list")
        self.assertIn("project:Ekonerg", output)
        self.assertIn("local", output)
        self.assertNotIn("broken", output)
        self.assertNotIn("user-global", output)
        self.assertNotIn("<workspace>", output)


if __name__ == "__main__":
    unittest.main()
