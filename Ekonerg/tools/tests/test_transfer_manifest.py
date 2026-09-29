"""EK-0.2 tests: inventory and verification never transfer framework files."""
import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from transfer_manifest import Blob, build_manifest, read_snapshot, validate_manifest


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.blobs = {
            "scripts/agent_coord.py": Blob("100644", "a" * 40, b"ROOT = 'Enconet'\n"),
            "Enconet/raw/company.md": Blob("100644", "b" * 40, b"private source"),
            "Enconet/schemas/evidence_access_uat.yml": Blob("100644", "c" * 40, b"status: approved\n"),
        }
        self.manifest = build_manifest(self.blobs, "d" * 40)

    def test_complete_inventory_passes(self):
        self.assertEqual(validate_manifest(self.manifest, self.blobs, "d" * 40), [])

    def test_omitted_file_fails(self):
        self.manifest["files"].pop()
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_unlisted_file_fails(self):
        self.blobs["Enconet/new.py"] = Blob("100644", "e" * 40, b"new")
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_changed_source_hash_fails(self):
        self.blobs["scripts/agent_coord.py"] = Blob("100644", "a" * 40, b"changed")
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_forged_hash_fails(self):
        self.manifest["files"][0]["sha256"] = "0" * 64
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_wrong_revision_fails(self):
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "e" * 40))

    def test_unexpected_approval_metadata_fails(self):
        self.manifest["approved"] = True
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_approved_status_cannot_be_self_asserted(self):
        self.manifest["status"] = "approved"
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_excluded_evidence_has_no_destination(self):
        row = next(r for r in self.manifest["files"] if r["source"].startswith("Enconet/raw/"))
        self.assertIsNone(row["destination"])

    def test_all_required_workspace_tools_need_adaptation(self):
        paths = ("agent_coord.py", "run_validation.py", "make_handoff.py")
        blobs = {"scripts/" + p: Blob("100644", "a" * 40, b"# source") for p in paths}
        for row in build_manifest(blobs, "d" * 40)["files"]:
            self.assertEqual(row["treatment"], "adapt")
            self.assertEqual(row["destination"], "Ekonerg/" + row["source"])

    def test_empty_regular_file_and_utf8_filename_preserved(self):
        blobs = {"Enconet/tests/test_č.py": Blob("100644", "a" * 40, b"")}
        manifest = build_manifest(blobs, "d" * 40)
        self.assertEqual(validate_manifest(manifest, blobs, "d" * 40), [])
        self.assertEqual(manifest["files"][0]["bytes"], 0)

    def test_duplicate_row_fails(self):
        self.manifest["files"].append(copy.deepcopy(self.manifest["files"][0]))
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_unsafe_destination_fails(self):
        self.manifest["files"][0]["destination"] = "Ekonerg/../Enconet/raw/x"
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_wrong_treatment_fails(self):
        self.manifest["files"][0]["treatment"] = "copy"
        self.assertTrue(validate_manifest(self.manifest, self.blobs, "d" * 40))

    def test_code_adapt_evidence_exclude_approval_recreate(self):
        rows = {r["source"]: r for r in self.manifest["files"]}
        self.assertEqual(rows["scripts/agent_coord.py"]["treatment"], "adapt")
        self.assertEqual(rows["Enconet/raw/company.md"]["treatment"], "exclude")
        self.assertEqual(rows["Enconet/schemas/evidence_access_uat.yml"]["treatment"], "recreate")

    def test_claude_owned_files_never_have_codex_destination(self):
        blobs = {p: Blob("100644", "a" * 40, b"guidance") for p in
                 ("Enconet/CLAUDE.md", "Enconet/.claude/skills/x/SKILL.md",
                  "Enconet/decisions/CC_ADR-0017.md")}
        for row in build_manifest(blobs, "d" * 40)["files"]:
            self.assertEqual((row["treatment"], row["destination"]), ("exclude", None))

    def test_link_cannot_enter_transfer(self):
        blobs = {"Enconet/scripts/link.py": Blob("120000", "f" * 40, b"../../raw/file")}
        row = build_manifest(blobs, "d" * 40)["files"][0]
        self.assertEqual(row["treatment"], "exclude")

    def test_dirty_and_untracked_worktree_is_not_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.STDOUT)
            git("init", "-q")
            file = root / "source.txt"
            file.write_bytes(b"committed\n")
            git("add", "source.txt")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "commit", "-qm", "fixture")
            revision = git("rev-parse", "HEAD").decode().strip()
            file.write_bytes(b"dirty\n")
            (root / "untracked.txt").write_bytes(b"never ingest")
            actual_revision, blobs = read_snapshot(root, revision)
            self.assertEqual(actual_revision, revision)
            self.assertEqual(list(blobs), ["source.txt"])
            self.assertEqual(blobs["source.txt"].data, b"committed\n")
            self.assertEqual(file.read_bytes(), b"dirty\n")


if __name__ == "__main__":
    unittest.main()
