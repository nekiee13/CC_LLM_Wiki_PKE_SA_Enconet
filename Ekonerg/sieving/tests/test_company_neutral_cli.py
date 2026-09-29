"""A copied sieving CLI should name its own project, not the first audit."""
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


def synthetic_document() -> dict:
    return {
        "document": {"doc_id": "SYN-CLI-1", "filename": "made-up.json", "title": "Synthetic"},
        "items": [{
            "item_id": "D-1", "record_side": "DOCUMENT", "template_id": "JSON_Template_App_B",
            "template_version": "1.1", "taxonomy_id": "APP_B", "criterion_id": "APP_B_I",
            "criterion_name": "Organization", "item_type": "control", "statement": "Made-up control",
            "evidence_quotes": ["Made-up quote"], "source": [{"page": 1}],
        }],
    }


class CompanyNeutralCliTests(unittest.TestCase):
    @staticmethod
    def _snapshot(folder: Path) -> dict[str, tuple[bytes, int]]:
        return {
            path.relative_to(folder).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in folder.rglob("*") if path.is_file()
        }

    def test_cli_uses_two_local_company_names_and_keeps_sibling_unchanged(self) -> None:
        for company, has_sibling in (("Čista Tvrtka", True), ("Žuti Pogon", False)):
            with self.subTest(company=company, has_sibling=has_sibling):
                with tempfile.TemporaryDirectory(prefix="neutral-cli-") as temp:
                    project = Path(temp) / company
                    sieving = project / "sieving"
                    sieving.mkdir(parents=True)
                    shutil.copyfile(PROJECT / "sieving" / "cli.py", sieving / "cli.py")
                    shutil.copytree(PROJECT / "sieving" / "src", sieving / "src",
                                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                    schemas = project / "schemas"
                    schemas.mkdir()
                    for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
                        shutil.copyfile(PROJECT / "schemas" / name, schemas / name)
                    data_dir = sieving / "DATA"
                    data_dir.mkdir()
                    (sieving / "outputs").mkdir()
                    (data_dir / "made-up.json").write_text(
                        json.dumps(synthetic_document()), encoding="utf-8"
                    )

                    sibling = project.parent / "Old Audit"
                    caller = sibling if has_sibling else project.parent / "unrelated caller"
                    caller.mkdir()
                    if has_sibling:
                        (sibling / "marker.txt").write_text("unchanged", encoding="utf-8")
                        before = self._snapshot(sibling)

                    def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(sieving / "cli.py"), *args],
                            cwd=caller, capture_output=True, text=True, encoding="utf-8",
                            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                            timeout=30, check=False,
                        )

                    info = run_cli("info")
                    self.assertEqual(info.returncode, 0, info.stdout + info.stderr)
                    self.assertIn(f"{company} JSON Sieving - Configuration", info.stdout)
                    self.assertNotIn("Ekonerg", info.stdout)
                    help_result = run_cli("query", "--help")
                    self.assertEqual(help_result.returncode, 0, help_result.stdout + help_result.stderr)
                    self.assertIn(f"{company}-local JSON", help_result.stdout)
                    self.assertIn("files or globs", help_result.stdout)
                    self.assertNotIn("Ekonerg", help_result.stdout)
                    query = run_cli(
                        "query", "--files", "sieving/DATA/made-up.json",
                        "--output", "sieving/outputs/result.csv", "--format", "csv",
                    )
                    self.assertEqual(query.returncode, 0, query.stdout + query.stderr)
                    self.assertIn("Files processed: 1", query.stdout)
                    self.assertTrue((sieving / "outputs" / "result.csv").is_file())
                    if has_sibling:
                        self.assertEqual(self._snapshot(sibling), before)
                    else:
                        self.assertFalse(sibling.exists())

    def test_reusable_runtime_has_no_first_company_literal(self) -> None:
        for path in (
            PROJECT / "sieving" / "cli.py",
            PROJECT / "sieving" / "src" / "json_extractor" / "pipeline.py",
            PROJECT / "sieving" / "src" / "json_extractor" / "io" / "export.py",
        ):
            with self.subTest(path=path.name):
                self.assertNotIn("Ekonerg", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
