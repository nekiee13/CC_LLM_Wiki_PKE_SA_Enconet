"""Local dispatcher tests use only disposable, synthetic project data."""
from __future__ import annotations

import hashlib
from contextlib import closing
import importlib.util
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


PROJECT = Path(__file__).resolve().parents[2]
FILES = ("scripts/audit_command.py", "scripts/audit_state.py",
         "scripts/db_util.py", "schemas/audit_commands.yml")


def snapshot(root):
    return {str(p.relative_to(root)): (hashlib.sha256(p.read_bytes()).hexdigest(),
            p.stat().st_mtime_ns) if p.is_file() else None for p in root.rglob("*")}


class LocalDispatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ek12-dispatch-")
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / "Rad s razmacima Županija"
        self.project = self.workspace / "Ekonerg"
        self.sibling = self.workspace / "Enconet"
        self.nested = self.project / "Enconet"
        for root in (self.project, self.sibling, self.nested):
            root.mkdir(parents=True)
        for root in (self.sibling, self.nested):
            (root / "HANDOFF.md").write_text("unchanged\n", encoding="utf-8")
        for name in FILES:
            self.assertTrue((PROJECT / name).is_file(), f"missing local file: {name}")
            destination = self.project / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PROJECT / name, destination)
        helper = PROJECT / "scripts/project_paths.py"
        if helper.exists():
            shutil.copyfile(helper, self.project / "scripts/project_paths.py")
        self.state("setup")

    def state(self, phase):
        (self.project / "project-state.yml").write_text(yaml.safe_dump({
            "phase": phase, "gates": {f"G{i}": {"status": "pending",
            "decision_ref": None} for i in range(1, 8)}}, sort_keys=False), encoding="utf-8")

    def invoke(self, *args, cwd=None, script="audit_command.py"):
        return subprocess.run([sys.executable, "-B",
            str(self.project / "scripts" / script), *args], cwd=cwd or self.workspace,
            capture_output=True, text=True, encoding="utf-8", timeout=30,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONPATH": ""})

    def load(self, name):
        # Load real copied modules. No mock of state loading, phase or gate checks.
        saved = {key: sys.modules.pop(key, None)
                 for key in ("audit_state", "db_util", "project_paths")}
        sys.path.insert(0, str(self.project / "scripts"))
        def cleanup():
            sys.path.remove(str(self.project / "scripts"))
            for key, value in saved.items():
                sys.modules.pop(key, None)
                if value is not None:
                    sys.modules[key] = value
        self.addCleanup(cleanup)
        spec = importlib.util.spec_from_file_location(name, self.project / "scripts" / (name + ".py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def stage(self, name, body="raise SystemExit(0)\n"):
        (self.project / "scripts" / name).write_text(body, encoding="utf-8")

    def test_registry_has_all_twelve_commands_and_local_closeout(self):
        registry = yaml.safe_load((self.project / "schemas/audit_commands.yml").read_text(encoding="utf-8"))
        self.assertEqual(12, len(registry["commands"]))
        self.assertEqual(["scripts/run_all_validations.py", "scripts/make_handoff.py"],
                         registry["commands"]["audit-close"]["scripts"])

    def test_status_reads_only_local_state_from_three_working_folders(self):
        before = [snapshot(p) for p in (self.sibling, self.nested)]
        for cwd in (self.project, self.workspace, self.workspace.parent):
            result = self.invoke("audit-status", cwd=cwd)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("phase: setup", result.stdout)
            self.assertIn("G7: pending", result.stdout)
        self.assertEqual(before, [snapshot(p) for p in (self.sibling, self.nested)])

    def test_isolated_copy_needs_no_enconet_or_shared_script(self):
        shutil.rmtree(self.sibling)
        shutil.rmtree(self.nested)
        result = self.invoke("--describe")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(self.sibling.exists())
        self.assertFalse(self.nested.exists())

    def test_closeout_runs_local_validation_before_local_handoff(self):
        module = self.load("audit_command")
        self.stage("run_all_validations.py")
        self.stage("make_handoff.py")
        with patch.object(module.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
            self.assertEqual(0, module.dispatch("audit-close", ["--status", "partial"]))
        self.assertEqual(2, run.call_count)
        for call, name in zip(run.call_args_list, ("run_all_validations.py", "make_handoff.py")):
            self.assertEqual(str(self.project / "scripts" / name), call.args[0][1])
            self.assertEqual(self.project, call.kwargs["cwd"])
        self.assertIn("--no-record", run.call_args_list[0].args[0])

    def test_failed_validation_cannot_publish_handoff(self):
        module = self.load("audit_command")
        self.stage("run_all_validations.py")
        self.stage("make_handoff.py")
        with patch.object(module.subprocess, "run", return_value=subprocess.CompletedProcess([], 7)) as run:
            self.assertEqual(7, module.dispatch("audit-close", []))
        self.assertEqual(1, run.call_count)
        self.assertFalse((self.project / "HANDOFF.md").exists())

    def test_missing_closeout_dependency_refuses_even_dry_run(self):
        result = self.invoke("--dry-run", "audit-close", "--status", "partial")
        self.assertEqual(1, result.returncode)
        self.assertIn("missing", result.stderr.lower())
        self.assertNotIn("invoke:", result.stdout)

    def test_wrong_phase_and_misplaced_options_refuse_before_subprocess(self):
        self.stage("chunk_document.py")
        for args, expected in ((("--dry-run", "audit-chunk", "DOC-0001"), "refuses phase setup"),
                               (("audit-gate", "--dry-run", "create", "--gate", "G1"), "must precede")):
            result = self.invoke(*args)
            self.assertEqual(1, result.returncode)
            self.assertIn(expected, result.stderr)
            self.assertNotIn("invoke:", result.stdout)

    def test_gate_packets_preserve_all_seven_phase_mappings(self):
        self.stage("gate_packet.py")
        phases = ("setup", "sieved", "evidence_reviewed", "findings_drafted",
                  "findings_approved", "report_ready", "dashboard_ready")
        for index, phase in enumerate(phases, 1):
            self.state(phase)
            result = self.invoke("--dry-run", "audit-gate", "create", "--gate", f"G{index}")
            self.assertEqual(0, result.returncode, result.stderr)
            wrong = self.invoke("--dry-run", "audit-gate", "create", "--gate", f"G{index % 7 + 1}")
            self.assertEqual(1, wrong.returncode)
            self.assertNotIn("invoke:", wrong.stdout)

    def test_foreign_global_paths_refused_even_when_describing(self):
        for flag in ("--state", "--db", "--runs", "--registry"):
            result = self.invoke(flag, str(self.sibling / "foreign.yml"), "--describe")
            self.assertEqual(1, result.returncode)
            self.assertIn("local", result.stderr.lower())

    def test_relative_paths_are_project_relative_not_cwd_relative(self):
        result = self.invoke("--state", "project-state.yml", "audit-status", cwd=self.workspace.parent)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_registry_cannot_route_outside_local_scripts(self):
        registry = yaml.safe_load((self.project / "schemas/audit_commands.yml").read_text(encoding="utf-8"))
        registry["commands"]["audit-register"]["scripts"] = ["../Enconet/evil.py"]
        path = self.project / "schemas/audit_commands.yml"
        path.write_text(yaml.safe_dump(registry), encoding="utf-8")
        result = self.invoke("--dry-run", "audit-register")
        self.assertEqual(1, result.returncode)
        self.assertNotIn("invoke:", result.stdout)

    def test_status_reads_existing_database_without_changes(self):
        (self.project / "db").mkdir()
        database = self.project / "db/nqa_audit.sqlite"
        with closing(sqlite3.connect(database)) as conn:
            conn.execute("CREATE TABLE auditor_actions(state TEXT)")
            conn.execute("INSERT INTO auditor_actions VALUES ('open')")
            conn.commit()
        before = snapshot(self.project)
        result = self.invoke("audit-status")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("open_actions: 1", result.stdout)
        self.assertEqual(before, snapshot(self.project))

    def test_db_helper_cannot_create_foreign_database(self):
        module = self.load("db_util")
        with self.assertRaises(ValueError):
            conn = module.connect(self.sibling / "new.sqlite")
            conn.close()
        self.assertFalse((self.sibling / "new.sqlite").exists())

    def test_state_cli_cannot_write_foreign_state(self):
        foreign = self.sibling / "project-state.yml"
        shutil.copyfile(self.project / "project-state.yml", foreign)
        before = snapshot(self.sibling)
        result = self.invoke("--state", str(foreign), "--transition", "failed",
                             "--reason", "synthetic", script="audit_state.py")
        self.assertEqual(1, result.returncode)
        self.assertIn("local", result.stderr.lower())
        self.assertEqual(before, snapshot(self.sibling))

    def redirect(self, link, target):
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.addCleanup(link.rmdir)
        else:
            link.symlink_to(target, target_is_directory=True)
            self.addCleanup(link.unlink)

    def test_redirected_schema_folder_refused_before_read(self):
        shutil.copytree(self.project / "schemas", self.sibling / "schemas")
        shutil.rmtree(self.project / "schemas")
        self.redirect(self.project / "schemas", self.sibling / "schemas")
        before = snapshot(self.sibling)
        result = self.invoke("--describe")
        self.assertEqual(1, result.returncode)
        self.assertIn("redirected", result.stderr)
        self.assertEqual(before, snapshot(self.sibling))

    def test_hardlinked_database_refused_before_open(self):
        (self.project / "db").mkdir()
        foreign = self.sibling / "audit.sqlite"
        with closing(sqlite3.connect(foreign)) as conn:
            conn.execute("CREATE TABLE example(value TEXT)")
        os.link(foreign, self.project / "db/nqa_audit.sqlite")
        before = snapshot(self.sibling)
        result = self.invoke("audit-status")
        self.assertEqual(1, result.returncode)
        self.assertIn("hard-linked", result.stderr)
        self.assertEqual(before, snapshot(self.sibling))

    def test_closeout_foreign_root_refused_before_validation(self):
        module = self.load("audit_command")
        self.stage("run_all_validations.py")
        self.stage("make_handoff.py")
        for args in (["--project-root", str(self.sibling)],
                     ["--project-root=" + str(self.sibling)],
                     ["--project-root", "handoffs"],
                     ["--validate", "../Enconet/HANDOFF.md"]):
            with patch.object(module.subprocess, "run") as run:
                with self.assertRaises(ValueError):
                    module.dispatch("audit-close", args)
                run.assert_not_called()

    def test_real_closeout_publishes_local_handoff_after_synthetic_validator(self):
        for relative in ("scripts/make_handoff.py", "handoff_schema.yml"):
            shutil.copyfile(PROJECT / relative, self.project / relative)
        self.stage("run_all_validations.py", "from pathlib import Path\n"
                   "Path('validation-was-run.txt').write_text('synthetic check')\n")
        before = [snapshot(p) for p in (self.sibling, self.nested)]
        result = self.invoke("audit-close", "--source-agent", "codex", "--status", "partial")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.project / "validation-was-run.txt").exists())
        self.assertTrue((self.project / "HANDOFF.md").exists())
        records = list((self.project / "handoffs").glob("*.md"))
        self.assertEqual(1, len(records))
        check = self.invoke("--validate", str(records[0]), script="make_handoff.py")
        self.assertEqual(0, check.returncode, check.stderr)
        self.assertEqual(before, [snapshot(p) for p in (self.sibling, self.nested)])

    def test_stage_foreign_output_refused_before_subprocess(self):
        self.state("findings_approved")
        self.stage("generate_report.py")
        module = self.load("audit_command")
        for flag in ("--output", "--viewer-output", "--db", "--approvals", "--out"):
            with patch.object(module.subprocess, "run") as run:
                with self.assertRaises(ValueError):
                    module.dispatch("audit-report", ["fixture.json", flag, str(self.sibling / "new.md")])
                run.assert_not_called()

    def test_stage_relative_output_is_normalized_to_project(self):
        self.state("findings_approved")
        self.stage("generate_report.py")
        module = self.load("audit_command")
        with patch.object(module.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
            self.assertEqual(0, module.dispatch("audit-report", ["fixture.json", "--output=outputs/report.md"]))
        self.assertIn("--output=" + str(self.project / "outputs/report.md"), run.call_args.args[0])

    def test_db_helper_keeps_foreign_keys_and_local_relative_paths(self):
        (self.project / "db").mkdir()
        module = self.load("db_util")
        with closing(module.connect("db/synthetic.sqlite")) as conn:
            self.assertEqual(1, conn.execute("PRAGMA foreign_keys").fetchone()[0])
        self.assertTrue((self.project / "db/synthetic.sqlite").exists())

    def test_state_transitions_require_each_gate_and_do_not_skip_phases(self):
        module = self.load("audit_state")
        states = ["setup", "registered", "chunked", "sieved", "evidence_reviewed",
                  "evaluated", "findings_drafted", "findings_approved", "report_ready",
                  "dashboard_ready", "closed", "failed"]
        vocab = self.project / "schemas/vocabularies.yml"
        vocab.write_text(yaml.safe_dump({"vocabularies": {"audit_states": {"values": states}}}), encoding="utf-8")
        for target, gate in module.GATE_FOR_TARGET.items():
            self.state(states[states.index(target) - 1])
            before = snapshot(self.project)
            with self.assertRaisesRegex(module.StateError, gate + " approval"):
                module.transition(target)
            self.assertEqual(before, snapshot(self.project))
        self.state("setup")
        with self.assertRaisesRegex(module.StateError, "illegal transition"):
            module.transition("closed")

    def test_state_checks_all_write_targets_before_changing_state(self):
        module = self.load("audit_state")
        before = snapshot(self.project)
        with self.assertRaises(ValueError):
            module.transition("failed", reason="synthetic", log=self.sibling / "log.md")
        self.assertEqual(before, snapshot(self.project))

    def test_db_helper_keeps_id_and_sql_identifier_checks(self):
        (self.project / "db").mkdir()
        (self.project / "schemas/id_patterns.yml").write_text(
            "patterns:\n  doc_id:\n    regex: '^DOC-[0-9]{4}$'\n", encoding="utf-8")
        module = self.load("db_util")
        with closing(module.connect("db/synthetic.sqlite")) as conn:
            conn.execute("CREATE TABLE documents(doc_id TEXT PRIMARY KEY)")
            module.insert(conn, "documents", {"doc_id": "DOC-0001"})
            self.assertTrue(module.exists(conn, "documents", "doc_id", "DOC-0001"))
            with self.assertRaisesRegex(ValueError, "invalid doc_id"):
                module.insert(conn, "documents", {"doc_id": "INVALID"})
            with self.assertRaisesRegex(ValueError, "unsafe SQL identifier"):
                module.exists(conn, "documents; DROP TABLE documents", "doc_id", "DOC-0001")

    def test_valid_synthetic_approval_allows_one_local_state_transition(self):
        (self.project / "schemas/vocabularies.yml").write_text(
            "vocabularies:\n  audit_states:\n    values: [setup, registered, failed]\n",
            encoding="utf-8")
        (self.project / "project-state.yml").write_text(
            "phase: setup\ngates:\n  G1: {status: approved, date: 2026-01-01, "
            "decision_ref: G1-SYNTHETIC}\n", encoding="utf-8")
        (self.project / "manifests").mkdir()
        (self.project / "manifests/approvals.csv").write_text(
            "object_id,decision,date,reviewer\nG1-SYNTHETIC,approved,2026-01-01,fixture\n",
            encoding="utf-8")
        (self.project / "wiki").mkdir()
        (self.project / "wiki/log.md").write_text("synthetic log\n", encoding="utf-8")
        before = [snapshot(p) for p in (self.sibling, self.nested)]
        module = self.load("audit_state")
        module.transition("registered")
        self.assertEqual("registered", module.load_state()["phase"])
        self.assertIn("state-transition", (self.project / "wiki/log.md").read_text(encoding="utf-8"))
        self.assertEqual(before, [snapshot(p) for p in (self.sibling, self.nested)])

    def test_state_temp_hardlink_refused_before_write(self):
        module = self.load("audit_state")
        foreign = self.sibling / "state-backup.yml"
        foreign.write_text("unchanged\n", encoding="utf-8")
        os.link(foreign, self.project / "project-state.yml.tmp")
        before = [snapshot(p) for p in (self.project, self.sibling)]
        with self.assertRaises(ValueError):
            module.update_state_file(self.project / "project-state.yml", phase="failed")
        self.assertEqual(before, [snapshot(p) for p in (self.project, self.sibling)])

    def test_gate_state_source_provenance_text_is_not_rewritten(self):
        module = self.load("audit_command")
        arguments = ["create", "--gate", "G1", "--state-source", "project-state.yml"]
        self.assertEqual(arguments, module._local_arguments(arguments))


if __name__ == "__main__":
    unittest.main()
