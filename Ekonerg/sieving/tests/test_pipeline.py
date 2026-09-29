"""End-to-end synthetic pipeline tests, never using a live audit corpus."""
from __future__ import annotations

import copy
import importlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
PACKAGE = PROJECT / "sieving" / "src" / "json_extractor"


def payload() -> dict:
    return {
        "document": {"doc_id": "EK-SYN-PIPE", "filename": "made-up.json", "title": "Synthetic"},
        "items": [{
            "item_id": "D-1", "record_side": "DOCUMENT", "template_id": "JSON_Template_App_B",
            "template_version": "1.1", "taxonomy_id": "APP_B", "criterion_id": "APP_B_I",
            "criterion_name": "Organization", "item_type": "control", "statement": "Synthetic control",
            "evidence_quotes": ["Made-up evidence"], "source": [{"page": 1}],
        }],
    }


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-pipeline-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        target = self.project / "sieving" / "src" / "json_extractor"
        target.mkdir(parents=True)
        for name in ("__init__.py", "config.py", "contract.py", "pipeline.py"):
            shutil.copyfile(PACKAGE / name, target / name)
        for folder in ("extract", "io", "query"):
            shutil.copytree(PACKAGE / folder, target / folder)
        schemas = self.project / "schemas"
        schemas.mkdir()
        for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schemas / name)
        sys.path.insert(0, str(self.project / "sieving"))
        self.addCleanup(lambda: sys.path.remove(str(self.project / "sieving")))
        self.addCleanup(self._forget)
        self._forget()
        self.module = importlib.import_module("src.json_extractor")
        self.pipeline = importlib.import_module("src.json_extractor.pipeline")
        self.data = self.project / "sieving" / "DATA"
        self.data.mkdir(exist_ok=True)
        self.output = self.project / "sieving" / "outputs"
        self.output.mkdir()

    @staticmethod
    def _forget() -> None:
        for name in tuple(sys.modules):
            if name == "src" or name.startswith("src."):
                del sys.modules[name]

    def _write(self, name: str, data: dict) -> Path:
        path = self.data / name
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def test_public_import_and_valid_local_export(self) -> None:
        source = self._write("valid.json", payload())
        self.assertTrue(Path(self.module.__file__).is_relative_to(self.project))
        result = self.module.run_pipeline(file_paths=[source], filter_expr="criterion_id:APP_B_I")
        self.assertEqual(result.items_loaded, 1)
        self.assertEqual(result.items_after_filter, 1)
        self.assertEqual(result.validation_errors, [])
        path = self.pipeline.export_pipeline_result(result, self.output / "result.csv")
        self.assertEqual(path, self.output / "result.csv")
        self.assertIn("EK-SYN-PIPE", path.read_text(encoding="utf-8-sig"))

    def test_validation_error_blocks_export_without_reason(self) -> None:
        data = copy.deepcopy(payload())
        data["items"][0]["evidence_quotes"] = []
        result = self.module.run_pipeline(file_paths=[self._write("bad.json", data)])
        target = self.output / "must-not-exist.csv"
        self.assertTrue(any(error.severity == "ERROR" for error in result.validation_errors))
        with self.assertRaisesRegex(ValueError, "Export blocked"):
            self.pipeline.export_pipeline_result(result, target)
        self.assertFalse(target.exists())

    def test_explicit_validation_reason_is_recorded_not_approval(self) -> None:
        data = copy.deepcopy(payload())
        data["items"][0]["evidence_quotes"] = []
        result = self.module.run_pipeline(file_paths=[self._write("bad.json", data)])
        with self.assertRaises(ValueError):
            self.pipeline.export_pipeline_result(result, self.output / "blank.csv",
                                                 validation_override_reason="   ")
        self.assertFalse((self.output / "blank.csv").exists())
        target = self.pipeline.export_pipeline_result(
            result, self.output / "review-needed.csv",
            validation_override_reason="synthetic test exception",
        )
        self.assertEqual(result.validation_override_reason, "synthetic test exception")
        self.assertTrue(target.is_file())
        self.assertTrue(any(item.severity == "ERROR" for item in result.validation_errors))

    def test_strict_drift_blocks_export(self) -> None:
        data = copy.deepcopy(payload())
        data["unexpected"] = "drift"
        result = self.module.run_pipeline(file_paths=[self._write("drift.json", data)], strict=True)
        target = self.output / "must-not-exist.csv"
        with self.assertRaisesRegex(ValueError, "Export blocked"):
            self.pipeline.export_pipeline_result(result, target)
        self.assertFalse(target.exists())

    def test_invalid_filter_fails_closed_even_with_preview_override(self) -> None:
        source = self._write("valid.json", payload())
        result = self.module.run_pipeline(file_paths=[source], filter_expr="criterion_id:")
        self.assertTrue(result.filter_error)
        self.assertTrue(result.df.empty)
        preview = self.module.run_pipeline(file_paths=[source], filter_expr="criterion_id:",
                                           allow_unfiltered_preview=True)
        self.assertTrue(preview.unfiltered_preview_used)
        self.assertEqual(len(preview.df), 1)
        target = self.output / "must-not-exist.csv"
        with self.assertRaisesRegex(ValueError, "Export blocked"):
            self.pipeline.export_pipeline_result(preview, target)
        self.assertFalse(target.exists())

    def test_bad_file_blocks_mixed_export(self) -> None:
        good = self._write("good.json", payload())
        bad = self.data / "bad.json"
        bad.write_text("{broken", encoding="utf-8")
        result = self.module.run_pipeline(file_paths=[good, bad])
        self.assertEqual(result.items_loaded, 1)
        self.assertEqual(len(result.bad_files), 1)
        target = self.output / "must-not-exist.csv"
        with self.assertRaisesRegex(ValueError, "Export blocked"):
            self.pipeline.export_pipeline_result(result, target)
        self.assertFalse(target.exists())

    def test_foreign_input_and_output_are_rejected_without_change(self) -> None:
        sibling = self.project.parent / "Enconet"
        sibling.mkdir()
        marker = sibling / "source.json"
        marker.write_text(json.dumps(payload()), encoding="utf-8")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
        with self.assertRaises(ValueError):
            self.module.run_pipeline(file_paths=[marker])
        result = self.module.run_pipeline(file_paths=[self._write("valid.json", payload())])
        with self.assertRaises(ValueError):
            self.pipeline.export_pipeline_result(result, sibling / "foreign.csv")
        self.assertFalse((sibling / "foreign.csv").exists())
        self.assertEqual((marker.read_bytes(), marker.stat().st_mtime_ns), before)
        self.assertFalse((self.project / "Enconet").exists())

    def test_empty_project_does_not_export(self) -> None:
        result = self.module.run_pipeline(data_dir=self.data)
        self.assertEqual(result.files_processed, 0)
        target = self.output / "empty.csv"
        with self.assertRaises(ValueError):
            self.pipeline.export_pipeline_result(result, target)
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
