"""Synthetic extraction tests; never load a real audit document."""
from __future__ import annotations

import copy
import importlib
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]


def sample_payload() -> dict:
    return {
        "document": {
            "doc_id": "EK-SYN-001", "filename": "synthetic.json", "title": "Made-up test",
            "control_metadata": {"revision": "0"},
        },
        "items": [
            {
                "item_id": "R-1", "record_side": "RULE", "template_id": "JSON_Template_App_B",
                "template_version": "1.1", "taxonomy_id": "APP_B",
                "criterion_id": "APP_B_I", "criterion_name": "Organization", "item_type": "requirement",
                "statement": "Synthetic rule", "evidence_quotes": ["Izmišljeni citat"],
                "source": [{"page": 2, "heading_path": ["Section A", "Rule"]}],
                "entities": {"organizations": ["Zeta", "Alpha", "Alpha"]},
                "rule": {
                    "source_rules": "10CFR50_APPB", "rule_locator": "APP_B_I",
                    "rule_key": "10CFR50_APPB::APP_B_I", "rule_strength": "MANDATORY",
                    "rule_citation_text": "Synthetic citation",
                },
            },
            {
                "item_id": "D-1", "record_side": "DOCUMENT", "template_id": "JSON_Template_App_B",
                "template_version": "1.1", "taxonomy_id": "APP_B",
                "criterion_id": "APP_B_II", "criterion_name": "Quality Assurance Program",
                "item_type": "control", "statement": "Synthetic procedure",
                "evidence_quotes": ["Made-up quote"], "source": [{"page": 3}],
                "rule_reference_ids": ["10CFR50_APPB::APP_B_II"],
                "rule_references": [{"ref_text": "Synthetic reference"}],
            },
        ],
    }


class ExtractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-extract-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        package_dir = self.project / "sieving" / "src" / "json_extractor"
        extract_dir = package_dir / "extract"
        extract_dir.mkdir(parents=True)
        schema_dir = self.project / "schemas"
        schema_dir.mkdir()
        for name in ("config.py", "contract.py"):
            shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / name,
                            package_dir / name)
        for name in ("__init__.py", "load_and_flatten.py"):
            shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / "extract" / name,
                            extract_dir / name)
        for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schema_dir / name)
        self.addCleanup(self._forget_modules)
        self._forget_modules()
        package = types.ModuleType("ekonerg_extract_fixture")
        package.__path__ = [str(package_dir)]
        sys.modules[package.__name__] = package
        self.extract = importlib.import_module("ekonerg_extract_fixture.extract")
        self.module = importlib.import_module("ekonerg_extract_fixture.extract.load_and_flatten")

    @staticmethod
    def _forget_modules() -> None:
        for name in tuple(sys.modules):
            if name == "ekonerg_extract_fixture" or name.startswith("ekonerg_extract_fixture."):
                del sys.modules[name]

    def test_rule_and_document_fields_stay_separate(self) -> None:
        result = self.extract.flatten_json_to_records(sample_payload(), "synthetic.json")
        self.assertEqual(len(result.records), 2)
        self.assertEqual(result.validation_errors, [])
        rule, document = result.records
        self.assertEqual(rule["rule_key"], "10CFR50_APPB::APP_B_I")
        self.assertIsNone(rule["rule_ref_keys"])
        self.assertEqual(document["rule_ref_keys"], "10CFR50_APPB::APP_B_II")
        self.assertIsNone(document["rule_key"])
        self.assertEqual(rule["entities_organizations"], "Alpha; Zeta")
        self.assertEqual(rule["source_heading_path"], "Section A > Rule")
        self.assertEqual(rule["evidence_quote_1"], "Izmišljeni citat")
        self.assertEqual(rule["doc_id"], "EK-SYN-001")

    def test_canonical_mismatch_and_side_leak_are_errors(self) -> None:
        data = sample_payload()
        data["items"][0]["criterion_name"] = "Wrong name"
        data["items"][1]["rule"] = {"rule_key": "leak"}
        result = self.extract.flatten_json_to_records(data, "synthetic.json")
        ids = {error.rule_id for error in result.validation_errors if error.severity == "ERROR"}
        self.assertIn("VAL-TAX-002", ids)
        self.assertIn("VAL-RULELEAK-002", ids)

    def test_malformed_quote_and_source_shapes_are_errors_not_truncated(self) -> None:
        data = sample_payload()
        item = data["items"][0]
        item["evidence_quotes"] = "not a list"
        item["source"] = {"page": 2}
        result = self.extract.flatten_json_to_records(data, "synthetic.json")
        rule = result.records[0]
        self.assertIsNone(rule["evidence_quote_1"])
        self.assertIsNone(rule["source_page"])
        ids = {error.rule_id for error in result.validation_errors}
        self.assertIn("VAL-EVID-001", ids)
        self.assertIn("VAL-PROV-001", ids)

    def test_strict_schema_drift_changes_warning_to_error(self) -> None:
        data = sample_payload()
        data["unexpected"] = 1
        normal = self.extract.flatten_json_to_records(data, "synthetic.json")
        strict = self.extract.flatten_json_to_records(data, "synthetic.json", strict=True)
        self.assertIn("WARNING", {error.severity for error in normal.validation_errors})
        self.assertIn("ERROR", {error.severity for error in strict.validation_errors})
        self.assertTrue(all(error.rule_id == "VAL-DRIFT-001" for error in strict.validation_errors))

    def test_primary_quote_uses_first_nonempty_string(self) -> None:
        data = sample_payload()
        data["items"][0]["evidence_quotes"] = ["", "  ", "Later valid quote"]
        result = self.extract.flatten_json_to_records(data, "synthetic.json")
        self.assertEqual(result.records[0]["evidence_quote_1"], "Later valid quote")
        self.assertNotIn("VAL-EVID-001", {error.rule_id for error in result.validation_errors})

    def test_malformed_nested_entities_are_reported(self) -> None:
        data = sample_payload()
        data["items"][0]["entities"] = {"organizations": "not a list"}
        result = self.extract.flatten_json_to_records(data, "synthetic.json")
        self.assertIsNone(result.records[0]["entities_organizations"])
        self.assertIn("VAL-ENTITY-001", {error.rule_id for error in result.validation_errors})

    def test_nontext_entity_member_is_reported_without_crash(self) -> None:
        data = sample_payload()
        data["items"][0]["entities"] = {"documents": [{"identifier": 42, "name": "Form"}]}
        result = self.extract.flatten_json_to_records(data, "synthetic.json")
        self.assertIsNone(result.records[0]["entities_documents"])
        self.assertIn("VAL-ENTITY-001", {error.rule_id for error in result.validation_errors})

    def test_malformed_source_heading_is_reported(self) -> None:
        data = sample_payload()
        data["items"][0]["source"][0]["heading_path"] = ["Section", 42]
        result = self.extract.flatten_json_to_records(data, "synthetic.json")
        self.assertIsNone(result.records[0]["source_heading_path"])
        self.assertIn("VAL-PROV-001", {error.rule_id for error in result.validation_errors})

    def test_multiple_files_requires_one_path_per_payload(self) -> None:
        with self.assertRaises(ValueError):
            self.extract.flatten_multiple_files([sample_payload(), sample_payload()], ["one.json"])
        self.assertFalse((self.project / "sieving" / "DATA").exists())

    def test_multiple_files_keep_error_provenance(self) -> None:
        first, second = sample_payload(), sample_payload()
        second["items"][0]["criterion_name"] = "Wrong name"
        result = self.extract.flatten_multiple_files([first, second], ["first.json", "second.json"])
        self.assertEqual(len(result.records), 4)
        mismatches = [error for error in result.validation_errors if error.rule_id == "VAL-TAX-002"]
        self.assertEqual([error.file_path for error in mismatches], ["second.json"])

    def test_non_object_root_is_refused(self) -> None:
        with self.assertRaises(TypeError):
            self.extract.flatten_json_to_records(["not", "an", "object"], "synthetic.json")

    def test_no_enconet_dependency_or_foreign_change(self) -> None:
        sibling = self.project.parent / "Enconet"
        sibling.mkdir()
        marker = sibling / "source.txt"
        marker.write_text("unchanged", encoding="utf-8")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
        result = self.extract.flatten_json_to_records(copy.deepcopy(sample_payload()), "synthetic.json")
        self.assertEqual(len(result.records), 2)
        self.assertEqual((marker.read_bytes(), marker.stat().st_mtime_ns), before)
        self.assertFalse((self.project / "Enconet").exists())


if __name__ == "__main__":
    unittest.main()
