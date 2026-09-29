"""TDD safety cases use only fresh, isolated mock workspaces."""
import copy
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from transfer_manifest import Blob, build_manifest
import safe_transfer as transfer


def tree_snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class TransferTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ek11-")
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / "Radni prostor Č"
        self.target = self.workspace / "Ekonerg"
        self.target.mkdir(parents=True)
        self.sibling = self.workspace / "Enconet"
        self.sibling.mkdir()
        (self.sibling / "HANDOFF.md").write_bytes(b"do not change")
        (self.target / "plan.md").write_bytes(b"owner plan")
        self.blobs = {
            "handoff_schema.yml": Blob("100644", "a" * 40, b'{"schema":1}\n'),
            "scripts/agent_coord.py": Blob("100644", "b" * 40, b"# adapt first\n"),
            "Enconet/project-state.yml": Blob("100644", "c" * 40, b"phase: closed\n"),
            "Enconet/raw/source.txt": Blob("100644", "d" * 40, b"never copy"),
        }
        self.revision = "e" * 40
        self.manifest = build_manifest(self.blobs, self.revision)

    def plan(self, **kwargs):
        return transfer.prepare(self.manifest, self.blobs, self.revision,
                                self.workspace, kwargs.pop("target", self.target), **kwargs)

    def test_preview_writes_nothing_and_lists_deferred(self):
        before = tree_snapshot(self.workspace)
        directories = sorted(str(p) for p in self.workspace.rglob("*"))
        plan = self.plan()
        self.assertEqual(plan["copy"][0]["state"], "create")
        self.assertEqual(len(plan["adapt"]), 1)
        self.assertEqual(len(plan["recreate"]), 1)
        self.assertEqual(plan["excluded"], 1)
        self.assertEqual(tree_snapshot(self.workspace), before)
        self.assertEqual(sorted(str(p) for p in self.workspace.rglob("*")), directories)

    def test_apply_exact_bytes_and_second_run_preserves(self):
        before = tree_snapshot(self.sibling)
        result = transfer.apply(self.plan(), self.blobs, "test-01")
        dest = self.target / "handoff_schema.yml"
        self.assertEqual(dest.read_bytes(), self.blobs["handoff_schema.yml"].data)
        self.assertEqual(result["created"], ["Ekonerg/handoff_schema.yml"])
        mtime = dest.stat().st_mtime_ns
        second = transfer.apply(self.plan(), self.blobs, "test-02")
        self.assertEqual(second["created"], [])
        self.assertEqual(dest.stat().st_mtime_ns, mtime)
        self.assertEqual(tree_snapshot(self.sibling), before)
        self.assertEqual((self.target / "plan.md").read_bytes(), b"owner plan")
        self.assertFalse((self.target / "scripts").exists())
        self.assertFalse((self.target / "project-state.yml").exists())

    def test_wrong_targets_rejected(self):
        for target in (self.workspace, self.sibling, self.target / "Enconet",
                       self.target / ".." / "Ekonerg"):
            with self.subTest(target=target), self.assertRaises(transfer.TransferError):
                self.plan(target=target)

    def test_conflict_prevents_any_journal_or_write(self):
        (self.target / "handoff_schema.yml").write_bytes(b"owner changed")
        before = tree_snapshot(self.workspace)
        with self.assertRaises(transfer.TransferError):
            self.plan()
        self.assertEqual(tree_snapshot(self.workspace), before)
        self.assertFalse((self.target / "docs").exists())

    def test_foreign_source_and_noncopy_source_rejected(self):
        for source in ("unknown.txt", "scripts/agent_coord.py", "Enconet/project-state.yml",
                       "Enconet/raw/source.txt"):
            with self.subTest(source=source), self.assertRaises(transfer.TransferError):
                self.plan(sources=[source])

    def test_manifest_tampering_rejected(self):
        for value in ("Ekonerg/../Enconet/handoff_schema.yml", "Ekonerg/.claude/file",
                      "Ekonerg/CX_unapproved.md"):
            changed = copy.deepcopy(self.manifest)
            row = next(r for r in changed["files"] if r["treatment"] == "copy")
            row["destination"] = value
            with self.assertRaises(transfer.TransferError):
                transfer.prepare(changed, self.blobs, self.revision, self.workspace, self.target)

    def test_source_bytes_changed_after_preview_rejected(self):
        plan = self.plan()
        self.blobs["handoff_schema.yml"] = Blob("100644", "a" * 40, b"changed")
        with self.assertRaises(transfer.TransferError):
            transfer.apply(plan, self.blobs, "test-01")
        self.assertFalse((self.target / "handoff_schema.yml").exists())

    def test_conflict_added_after_preview_is_preserved(self):
        plan = self.plan()
        (self.target / "handoff_schema.yml").write_bytes(b"new owner work")
        with self.assertRaises(transfer.TransferError):
            transfer.apply(plan, self.blobs, "test-01")
        self.assertEqual((self.target / "handoff_schema.yml").read_bytes(), b"new owner work")

    def test_destination_hardlink_is_rejected(self):
        source = self.sibling / "shared.yml"
        source.write_bytes(self.blobs["handoff_schema.yml"].data)
        os.link(source, self.target / "handoff_schema.yml")
        with self.assertRaises(transfer.TransferError):
            self.plan()

    def test_reparse_component_rejected(self):
        with patch.object(transfer, "is_redirect", side_effect=lambda p: p == self.target):
            with self.assertRaises(transfer.TransferError):
                self.plan()

    def test_directory_at_file_target_rejected(self):
        (self.target / "handoff_schema.yml").mkdir()
        with self.assertRaises(transfer.TransferError):
            self.plan()

    def test_lock_prevents_apply(self):
        (self.target / ".ek-transfer.lock").write_bytes(b"another writer")
        with self.assertRaises(transfer.TransferError):
            transfer.apply(self.plan(), self.blobs, "test-01")
        self.assertFalse((self.target / "handoff_schema.yml").exists())

    def test_run_id_cannot_escape(self):
        for run_id in ("../escape", "a/b", "CON", "x.", "x y", ""):
            with self.subTest(run_id=run_id), self.assertRaises(transfer.TransferError):
                transfer.apply(self.plan(), self.blobs, run_id)

    def test_existing_run_requires_explicit_resume(self):
        transfer.apply(self.plan(), self.blobs, "test-01")
        with self.assertRaises(transfer.TransferError):
            transfer.apply(self.plan(), self.blobs, "test-01")
        result = transfer.apply(self.plan(), self.blobs, "test-01", resume=True)
        self.assertTrue(result["complete"])

    def test_resume_missing_journal_refused(self):
        with self.assertRaises(transfer.TransferError):
            transfer.apply(self.plan(), self.blobs, "missing", resume=True)

    def test_interruption_after_receipt_resumes_without_rewrite(self):
        append = transfer.append_event
        def interrupt(path, event):
            append(path, event)
            if event["event"] == "created":
                raise RuntimeError("simulated interruption")
        with patch.object(transfer, "append_event", side_effect=interrupt):
            with self.assertRaises(RuntimeError):
                transfer.apply(self.plan(), self.blobs, "test-01")
        dest = self.target / "handoff_schema.yml"
        mtime = dest.stat().st_mtime_ns
        report = transfer.diagnose(self.plan(), "test-01")
        self.assertFalse(report["complete"])
        self.assertEqual(report["removal_candidates"], ["Ekonerg/handoff_schema.yml"])
        transfer.apply(self.plan(), self.blobs, "test-01", resume=True)
        self.assertEqual(dest.stat().st_mtime_ns, mtime)

    def test_interruption_before_receipt_never_claims_ownership(self):
        append = transfer.append_event
        def interrupt(path, event):
            if event["event"] == "created":
                raise RuntimeError("receipt not durable")
            append(path, event)
        with patch.object(transfer, "append_event", side_effect=interrupt):
            with self.assertRaises(RuntimeError):
                transfer.apply(self.plan(), self.blobs, "test-01")
        self.assertEqual(transfer.diagnose(self.plan(), "test-01")["removal_candidates"], [])
        result = transfer.apply(self.plan(), self.blobs, "test-01", resume=True)
        self.assertEqual(result["created"], [])

    def test_partial_file_is_never_overwritten_or_removed(self):
        append = transfer.append_event
        def interrupt(path, event):
            append(path, event)
            if event["event"] == "intent":
                (self.target / "handoff_schema.yml").write_bytes(b"partial")
                raise RuntimeError("interrupted")
        with patch.object(transfer, "append_event", side_effect=interrupt):
            with self.assertRaises(RuntimeError):
                transfer.apply(self.plan(), self.blobs, "test-01")
        with self.assertRaises(transfer.TransferError):
            self.plan()
        self.assertEqual((self.target / "handoff_schema.yml").read_bytes(), b"partial")

    def test_diagnosis_never_removes_files_and_rejects_changed_ownership(self):
        transfer.apply(self.plan(), self.blobs, "test-01")
        before = tree_snapshot(self.workspace)
        self.assertEqual(transfer.diagnose(self.plan(), "test-01")["removal_candidates"], [])
        self.assertEqual(tree_snapshot(self.workspace), before)

    def test_truncated_journal_fails_closed(self):
        transfer.apply(self.plan(), self.blobs, "test-01")
        journal = self.target / "docs/transfer/runs/test-01.jsonl"
        with journal.open("ab") as stream:
            stream.write(b'{"event":')
        with self.assertRaises(transfer.TransferError):
            transfer.apply(self.plan(), self.blobs, "test-01", resume=True)

    def test_approved_manifest_identity_pinned(self):
        self.assertEqual(transfer.APPROVED_MANIFEST_SHA256,
                         "fd9d69ff5c7836c1696402aa7012177de3e625efd301274f8eeddedbaeafc3a4")

    def test_real_directory_redirect_cannot_reach_sibling(self):
        link = self.target / "docs"
        if os.name == "nt":
            # New junction in this test fixture only; no live project path.
            command = ["cmd", "/c", "mklink", "/J", str(link), str(self.sibling)]
            subprocess.run(command, check=True, capture_output=True)
            self.addCleanup(lambda: link.rmdir() if link.exists() else None)
        else:
            link.symlink_to(self.sibling, target_is_directory=True)
        before = tree_snapshot(self.sibling)
        self.assertTrue(transfer.is_redirect(link))
        with self.assertRaises(transfer.TransferError):
            transfer.apply(self.plan(), self.blobs, "test-01")
        self.assertEqual(tree_snapshot(self.sibling), before)
        self.assertFalse((self.target / "handoff_schema.yml").exists())

    def test_readonly_preview_cli_defaults_and_crlf_manifest(self):
        raw = json.dumps(self.manifest, indent=2).encode() + b"\n"
        artifact = self.workspace / "manifest.json"
        artifact.write_bytes(raw.replace(b"\n", b"\r\n"))
        before = tree_snapshot(self.workspace)
        with patch.multiple(transfer, WORKSPACE=self.workspace, MANIFEST=artifact,
                            APPROVED_MANIFEST_SHA256=transfer.digest(raw)), \
             patch.object(transfer, "read_snapshot", return_value=(self.revision, self.blobs)), \
             contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(transfer.main([]), 0)
        self.assertEqual(json.loads(out.getvalue())["mode"], "preview")
        self.assertEqual(tree_snapshot(self.workspace), before)

    def test_cli_manifest_hash_tamper_rejected_before_git(self):
        artifact = self.workspace / "manifest.json"
        artifact.write_bytes(b"{}\n")
        with patch.object(transfer, "MANIFEST", artifact), \
             patch.object(transfer, "read_snapshot") as git_read, \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(transfer.main([]), 1)
            git_read.assert_not_called()

    def test_cli_apply_needs_explicit_run_id(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(transfer.main(["--apply"]), 1)
            self.assertEqual(transfer.main(["--resume"]), 1)

    def test_completed_receipt_changed_timestamp_refuses_resume(self):
        transfer.apply(self.plan(), self.blobs, "test-01")
        dest = self.target / "handoff_schema.yml"
        info = dest.stat()
        os.utime(dest, ns=(info.st_atime_ns, info.st_mtime_ns + 1_000_000_000))
        with self.assertRaises(transfer.TransferError):
            transfer.apply(self.plan(), self.blobs, "test-01", resume=True)
        report = transfer.diagnose(self.plan(), "test-01")
        self.assertEqual(report["changed_or_missing"], ["Ekonerg/handoff_schema.yml"])
        self.assertEqual(report["removal_candidates"], [])

    def test_journal_header_tampering_rejected(self):
        transfer.apply(self.plan(), self.blobs, "test-01")
        path = self.target / "docs/transfer/runs/test-01.jsonl"
        lines = path.read_bytes().splitlines()
        header = json.loads(lines[0])
        header["identity"]["source_commit"] = "f" * 40
        lines[0] = transfer.canonical(header)
        path.write_bytes(b"\n".join(lines) + b"\n")
        with self.assertRaises(transfer.TransferError):
            transfer.apply(self.plan(), self.blobs, "test-01", resume=True)

    def test_apply_plan_forgery_refused(self):
        plan = self.plan()
        plan["copy"][0]["destination"] = "Ekonerg/owner.txt"
        with self.assertRaises(transfer.TransferError):
            transfer.apply(plan, self.blobs, "test-01")
        self.assertFalse((self.target / "owner.txt").exists())

    def test_partial_conflict_can_be_diagnosed_without_deletion(self):
        append = transfer.append_event
        def interrupt(path, event):
            append(path, event)
            if event["event"] == "intent":
                (self.target / "handoff_schema.yml").write_bytes(b"partial")
                raise RuntimeError("interrupted")
        with patch.object(transfer, "append_event", side_effect=interrupt):
            with self.assertRaises(RuntimeError):
                transfer.apply(self.plan(), self.blobs, "test-01")
        report = transfer.diagnose(self.plan(allow_conflicts=True), "test-01")
        self.assertEqual(report["unrecorded_do_not_remove"], ["Ekonerg/handoff_schema.yml"])
        self.assertEqual(report["removal_candidates"], [])

    def test_invalid_receipt_fingerprint_type_rejected(self):
        transfer.apply(self.plan(), self.blobs, "test-01")
        path = self.target / "docs/transfer/runs/test-01.jsonl"
        events = [json.loads(line) for line in path.read_bytes().splitlines()]
        events[2]["fingerprint"]["st_ino"] = "not an integer"
        path.write_bytes(b"\n".join(transfer.canonical(e) for e in events) + b"\n")
        with self.assertRaises(transfer.TransferError):
            transfer.read_journal(path, self.plan())


if __name__ == "__main__":
    unittest.main()
