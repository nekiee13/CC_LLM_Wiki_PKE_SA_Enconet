"""EF-1.2: direct reading must be safe and local to one company."""

from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from Ekonerg.tools.fast_audit_copy import prepare_copies, verify_quote


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class FastAuditCopyTests(unittest.TestCase):
    def make_case(self, with_sibling: bool = False):
        temporary = tempfile.TemporaryDirectory(prefix="ef12-")
        self.addCleanup(temporary.cleanup)
        workspace = Path(temporary.name) / "Rad s razmacima Županija"
        project = workspace / "Nova tvrtka"
        source = project / "incoming" / "sample.md"
        source.parent.mkdir(parents=True)
        data = b"# Example\nA test claim.\nAnother line.\n"
        source.write_bytes(data)
        register = project / "work" / "fast_audit" / "RUN-1" / "source_register.csv"
        register.parent.mkdir(parents=True)
        with register.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["source_id", "relative_path", "bytes", "sha256"])
            writer.writeheader()
            writer.writerow({"source_id": "TEST-001", "relative_path": "incoming/sample.md",
                             "bytes": len(data), "sha256": digest(data)})
        sibling = workspace / "Other company" / "incoming" / "keep.md"
        if with_sibling:
            sibling.parent.mkdir(parents=True)
            sibling.write_bytes(b"do not touch\n")
        return project, source, register, sibling

    def test_preview_apply_retry_and_no_sibling_change(self):
        for with_sibling in (False, True):
            with self.subTest(with_sibling=with_sibling):
                project, source, register, sibling = self.make_case(with_sibling)
                source_before = source.read_bytes()
                sibling_before = sibling.read_bytes() if with_sibling else None
                pinned = digest(register.read_bytes())
                preview = prepare_copies(project, register, pinned, apply=False)
                target = register.parent / "sources" / "incoming" / "sample.md"
                self.assertEqual(preview, {"planned": 1, "copied": 0, "preserved": 0})
                self.assertFalse(target.exists())
                applied = prepare_copies(project, register, pinned, apply=True)
                self.assertEqual(applied, {"planned": 1, "copied": 1, "preserved": 0})
                self.assertEqual(target.read_bytes(), source_before)
                stamp = target.stat().st_mtime_ns
                retry = prepare_copies(project, register, pinned, apply=True)
                self.assertEqual(retry, {"planned": 1, "copied": 0, "preserved": 1})
                self.assertEqual(target.stat().st_mtime_ns, stamp)
                self.assertEqual(source.read_bytes(), source_before)
                if with_sibling:
                    self.assertEqual(sibling.read_bytes(), sibling_before)

    def test_changed_source_and_wrong_register_hash_refuse_copy(self):
        project, source, register, _ = self.make_case()
        pinned = digest(register.read_bytes())
        with self.assertRaisesRegex(ValueError, "register hash"):
            prepare_copies(project, register, "0" * 64, apply=True)
        source.write_bytes(b"X" * source.stat().st_size)
        with self.assertRaisesRegex(ValueError, "source hash"):
            prepare_copies(project, register, pinned, apply=True)
        self.assertFalse((register.parent / "sources").exists())

    def test_conflicting_retry_refuses_overwrite(self):
        project, _, register, _ = self.make_case()
        pinned = digest(register.read_bytes())
        prepare_copies(project, register, pinned, apply=True)
        target = register.parent / "sources" / "incoming" / "sample.md"
        target.write_bytes(b"local note that must not be lost\n")
        with self.assertRaisesRegex(ValueError, "work-copy conflict"):
            prepare_copies(project, register, pinned, apply=True)
        self.assertEqual(target.read_bytes(), b"local note that must not be lost\n")

    def test_quote_resolves_by_id_heading_and_exact_lines(self):
        project, _, register, _ = self.make_case()
        pinned = digest(register.read_bytes())
        prepare_copies(project, register, pinned, apply=True)
        self.assertEqual(verify_quote(project, register, pinned, "TEST-001", "# Example", 2, 3,
                                      "A test claim.\nAnother line."),
                         "A test claim.\nAnother line.")
        with self.assertRaisesRegex(ValueError, "quote mismatch"):
            verify_quote(project, register, pinned, "TEST-001", "# Example", 2, 3, "wrong")
        with self.assertRaisesRegex(ValueError, "heading mismatch"):
            verify_quote(project, register, pinned, "TEST-001", "# Wrong", 2, 2, "A test claim.")

    def test_register_cannot_escape_incoming(self):
        project, _, register, _ = self.make_case()
        text = register.read_text(encoding="utf-8").replace("incoming/sample.md", "../Other company/keep.md")
        register.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsafe source path"):
            prepare_copies(project, register, digest(register.read_bytes()), apply=True)

    def test_new_unregistered_source_refuses_the_frozen_set(self):
        project, _, register, _ = self.make_case()
        (project / "incoming" / "new.md").write_text("# New\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "incoming set differs"):
            prepare_copies(project, register, digest(register.read_bytes()), apply=True)
        self.assertFalse((register.parent / "sources").exists())


if __name__ == "__main__":
    unittest.main()
