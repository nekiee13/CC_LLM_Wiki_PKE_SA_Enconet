"""Run the CLI in a fake Ekonerg project; never use a live audit corpus."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]


def payload() -> dict:
    return {
        "document": {"doc_id": "EK-SYN-CLI", "filename": "made-up.json", "title": "Synthetic"},
        "items": [{
            "item_id": "D-1", "record_side": "DOCUMENT", "template_id": "JSON_Template_App_B",
            "template_version": "1.1", "taxonomy_id": "APP_B", "criterion_id": "APP_B_I",
            "criterion_name": "Organization", "item_type": "control", "statement": "Made-up control",
            "evidence_quotes": ["Made-up quote"], "source": [{"page": 1}],
        }],
    }


class LocalCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-cli-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        self.sieving = self.project / "sieving"
        self.sieving.mkdir(parents=True)
        shutil.copyfile(PROJECT / "sieving" / "cli.py", self.sieving / "cli.py")
        shutil.copytree(PROJECT / "sieving" / "src", self.sieving / "src",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        schemas = self.project / "schemas"
        schemas.mkdir()
        for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schemas / name)
        self.data = self.sieving / "DATA"
        self.data.mkdir()
        (self.sieving / "outputs").mkdir()
        self.sibling = self.project.parent / "Enconet"
        self.sibling.mkdir()
        self.marker = self.sibling / "untouched.json"
        self.marker.write_text(json.dumps(payload()), encoding="utf-8")
        self.before = (self.marker.read_bytes(), self.marker.stat().st_mtime_ns)

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(self.sieving / "cli.py"), *args],
            cwd=self.sibling, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            timeout=30, check=False,
        )

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload(), ensure_ascii=False), encoding="utf-8")

    def assert_foreign_unchanged(self) -> None:
        self.assertEqual((self.marker.read_bytes(), self.marker.stat().st_mtime_ns), self.before)
        self.assertFalse((self.project / "Enconet").exists())

    def test_query_requires_files_or_all_and_info_is_local(self) -> None:
        missing = self.run_cli("query")
        self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
        self.assertIn("Must specify --files or --all", missing.stdout)
        info = self.run_cli("info")
        self.assertEqual(info.returncode, 0, info.stdout + info.stderr)
        self.assertIn(str(self.data), info.stdout.replace("\n", ""))
        self.assertNotIn(str(self.sibling), info.stdout)
        self.assert_foreign_unchanged()

    def test_project_relative_file_exports_inside_ekonerg(self) -> None:
        self.write_json(self.data / "valid.json")
        result = self.run_cli("query", "--files", "sieving/DATA/valid.json",
                              "--output", "sieving/outputs/result.csv", "--format", "csv")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Files processed: 1", result.stdout)
        self.assertTrue((self.sieving / "outputs" / "result.csv").is_file())
        self.assert_foreign_unchanged()

    def test_recursive_glob_and_all_use_local_data(self) -> None:
        self.write_json(self.data / "nested" / "valid.json")
        globbed = self.run_cli("query", "--files", "sieving/DATA/**/*.json")
        self.assertEqual(globbed.returncode, 0, globbed.stdout + globbed.stderr)
        self.assertIn("Files processed: 1", globbed.stdout)
        all_files = self.run_cli("query", "--all", "--data-dir", "sieving/DATA")
        self.assertEqual(all_files.returncode, 0, all_files.stdout + all_files.stderr)
        self.assertIn("Files processed: 1", all_files.stdout)
        self.assert_foreign_unchanged()

    def test_foreign_direct_input_output_and_data_roots_are_refused(self) -> None:
        self.write_json(self.data / "valid.json")
        for args in (
            ("query", "--files", str(self.marker)),
            ("query", "--files", "sieving/DATA/valid.json", "--output", str(self.sibling / "result.csv")),
            ("query", "--all", "--data-dir", str(self.sibling)),
            ("list-files", "--data-dir", str(self.sibling)),
            ("query", "--files", str(self.project / "Enconet" / "bad.json")),
        ):
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 2, (args, result.stdout, result.stderr))
        self.assertFalse((self.sibling / "result.csv").exists())
        self.assert_foreign_unchanged()

    def test_foreign_glob_and_link_are_refused_before_read(self) -> None:
        outside_glob = self.run_cli("query", "--files", str(self.sibling / "*.json"))
        self.assertEqual(outside_glob.returncode, 2, outside_glob.stdout + outside_glob.stderr)
        link = self.data / "linked.json"
        try:
            link.symlink_to(self.marker)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")
        linked = self.run_cli("query", "--files", "sieving/DATA/linked.json")
        self.assertEqual(linked.returncode, 2, linked.stdout + linked.stderr)
        self.assert_foreign_unchanged()

    def test_recursive_glob_does_not_enter_linked_foreign_directory(self) -> None:
        link = self.data / "linked_dir"
        try:
            link.symlink_to(self.sibling, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"directory symlink unavailable: {exc}")
        result = self.run_cli("query", "--files", "sieving/DATA/**/*.json")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assert_foreign_unchanged()

    def test_invalid_filter_is_preview_only_and_never_exports(self) -> None:
        self.write_json(self.data / "valid.json")
        base = ("query", "--files", "sieving/DATA/valid.json", "--filter", "not_a_field:value")
        blocked = self.run_cli(*base)
        self.assertEqual(blocked.returncode, 2, blocked.stdout + blocked.stderr)
        preview = self.run_cli(*base, "--allow-unfiltered-preview", "--preview")
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertIn("DEVELOPMENT OVERRIDE", preview.stdout)
        export = self.run_cli(*base, "--allow-unfiltered-preview", "--preview",
                              "--output", "sieving/outputs/blocked.csv", "--format", "csv")
        self.assertEqual(export.returncode, 2, export.stdout + export.stderr)
        self.assertFalse((self.sieving / "outputs" / "blocked.csv").exists())
        self.assert_foreign_unchanged()

    def test_missing_local_file_and_list_files_are_diagnostic(self) -> None:
        missing = self.run_cli("query", "--files", "sieving/DATA/missing.json")
        self.assertEqual(missing.returncode, 0, missing.stdout + missing.stderr)
        self.assertIn("missing.json", missing.stdout)
        self.write_json(self.data / "valid.json")
        listed = self.run_cli("list-files", "--data-dir", "sieving/DATA")
        self.assertEqual(listed.returncode, 0, listed.stdout + listed.stderr)
        self.assertIn("valid.json", listed.stdout)
        self.assert_foreign_unchanged()

    def test_validation_error_export_needs_explicit_reason(self) -> None:
        invalid = payload()
        invalid["items"][0]["criterion_name"] = "Invented criterion"
        (self.data / "invalid.json").write_text(json.dumps(invalid), encoding="utf-8")
        base = ("query", "--files", "sieving/DATA/invalid.json",
                "--output", "sieving/outputs/diagnostic.csv", "--format", "csv")
        blocked = self.run_cli(*base)
        self.assertEqual(blocked.returncode, 2, blocked.stdout + blocked.stderr)
        self.assertFalse((self.sieving / "outputs" / "diagnostic.csv").exists())
        no_reason = self.run_cli(*base, "--allow-validation-errors")
        self.assertEqual(no_reason.returncode, 2, no_reason.stdout + no_reason.stderr)
        allowed = self.run_cli(*base, "--allow-validation-errors",
                               "--validation-override-reason", "Synthetic diagnostic only")
        self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
        self.assertTrue((self.sieving / "outputs" / "diagnostic.csv").is_file())
        self.assertIn("VALIDATION OVERRIDE", allowed.stdout)
        self.assert_foreign_unchanged()


if __name__ == "__main__":
    unittest.main()
