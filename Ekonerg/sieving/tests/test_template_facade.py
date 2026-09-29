"""Synthetic tests for the project-local Appendix B template facade."""
from __future__ import annotations

import importlib
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
PACKAGE = PROJECT / "sieving" / "src" / "json_extractor"
PREFIX = "ekonerg_template_fixture"


class TemplateFacadeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-template-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        package = self.project / "sieving" / "src" / "json_extractor"
        templates = package / "templates"
        templates.mkdir(parents=True)
        shutil.copyfile(PACKAGE / "contract.py", package / "contract.py")
        for name in ("__init__.py", "app_b.py"):
            shutil.copyfile(PACKAGE / "templates" / name, templates / name)
        schema_dir = self.project / "schemas"
        schema_dir.mkdir()
        for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schema_dir / name)
        self.sibling = self.project.parent / "Enconet"
        self.sibling.mkdir()
        self.marker = self.sibling / "untouched.txt"
        self.marker.write_text("unchanged", encoding="utf-8")
        self.before = (self.marker.read_bytes(), self.marker.stat().st_mtime_ns)
        self.addCleanup(self._forget)
        self._forget()
        fixture = types.ModuleType(PREFIX)
        fixture.__path__ = [str(package)]
        sys.modules[PREFIX] = fixture

    @staticmethod
    def _forget() -> None:
        for name in tuple(sys.modules):
            if name == PREFIX or name.startswith(PREFIX + "."):
                del sys.modules[name]

    def _load(self):
        facade = importlib.import_module(PREFIX + ".templates")
        contract = importlib.import_module(PREFIX + ".contract")
        return facade.AppBTemplate, contract

    def test_public_export_reads_only_local_contract(self) -> None:
        template, contract = self._load()
        self.assertEqual(contract.CONTRACT_PATH, self.project / "schemas" / "sieving_contract.yml")
        self.assertEqual(template.TEMPLATE_ID, "JSON_Template_App_B")
        self.assertEqual(template.TEMPLATE_VERSION, "1.1")
        self.assertEqual(template.TAXONOMY_ID, "APP_B")
        self.assertEqual((self.marker.read_bytes(), self.marker.stat().st_mtime_ns), self.before)
        self.assertFalse((self.project / "Enconet").exists())

    def test_criterion_methods_match_local_taxonomy(self) -> None:
        template, contract = self._load()
        pairs = {item["criterion_id"]: item["criterion_name"] for item in contract.load_contract()["criteria"]}
        self.assertEqual(template.get_criterion_map(), pairs)
        self.assertEqual(template.get_criterion_ids(), list(pairs))
        self.assertEqual(template.get_criterion_names(), list(pairs.values()))
        self.assertEqual(len(pairs), 18)
        self.assertTrue(template.validate_criterion_id("APP_B_I"))
        self.assertTrue(template.validate_criterion_name("APP_B_I", "Organization"))
        self.assertFalse(template.validate_criterion_id("APP_B_XIX"))
        self.assertFalse(template.validate_criterion_name("APP_B_I", "Invented"))

    def test_codes_and_enums_match_local_contract(self) -> None:
        template, contract = self._load()
        data = contract.load_contract()
        self.assertEqual(template.get_ref_codes(), [code["ref_code"] for code in data["canonical_codes"]])
        self.assertEqual(template.CANONICAL_CODES[0]["allowed_locators"], template.get_criterion_ids())
        self.assertEqual(template.RECORD_SIDE_VALUES, data["enums"]["record_side"])
        self.assertEqual(template.RULE_STRENGTH_VALUES, data["enums"]["rule_strength"])
        self.assertEqual(template.ITEM_TYPE_VALUES, data["enums"]["item_type"])

    def test_missing_local_contract_does_not_fall_back_to_enconet(self) -> None:
        (self.project / "schemas" / "sieving_contract.yml").unlink()
        with self.assertRaises(FileNotFoundError):
            self._load()
        self.assertEqual((self.marker.read_bytes(), self.marker.stat().st_mtime_ns), self.before)


if __name__ == "__main__":
    unittest.main()
