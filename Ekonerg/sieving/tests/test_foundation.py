"""Synthetic path and contract checks for the first sieving transfer slice."""
from __future__ import annotations

import importlib
import json
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
PACKAGE_FILES = ("config.py", "contract.py")
SCHEMA_FILES = ("sieving_contract.yml", "app_b_taxonomy.yml")


class FoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-sieving-")
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.project = root / "Županija with spaces" / "Ekonerg"
        self.package = self.project / "sieving" / "src" / "json_extractor"
        self.schema_dir = self.project / "schemas"
        self.package.mkdir(parents=True)
        self.schema_dir.mkdir()
        for name in PACKAGE_FILES:
            shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / name,
                            self.package / name)
        for name in SCHEMA_FILES:
            shutil.copyfile(PROJECT / "schemas" / name, self.schema_dir / name)
        self.addCleanup(self._forget_modules)
        self._forget_modules()
        package = types.ModuleType("ekonerg_sieving_fixture")
        package.__path__ = [str(self.package)]
        sys.modules[package.__name__] = package
        self.config = importlib.import_module("ekonerg_sieving_fixture.config")
        self.contract = importlib.import_module("ekonerg_sieving_fixture.contract")

    @staticmethod
    def _forget_modules() -> None:
        for name in tuple(sys.modules):
            if name == "ekonerg_sieving_fixture" or name.startswith("ekonerg_sieving_fixture."):
                del sys.modules[name]

    def test_defaults_stay_within_project_not_home_or_sibling(self) -> None:
        sibling = self.project.parent / "Enconet"
        sibling.mkdir()
        marker = sibling / "untouched.txt"
        marker.write_text("same", encoding="utf-8")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
        cfg = self.config.Config()
        self.assertEqual(cfg.data_dir, self.project / "sieving" / "DATA")
        self.assertEqual(cfg.config_dir, self.project / "sieving" / "config" / "json_extractor")
        self.assertFalse((self.project / "Enconet").exists())
        self.assertEqual((marker.read_bytes(), marker.stat().st_mtime_ns), before)

    def test_outside_explicit_roots_are_rejected_before_write(self) -> None:
        outside = self.project.parent / "Enconet" / "DATA"
        with self.assertRaises(ValueError):
            self.config.Config(data_dir=outside)
        with self.assertRaises(ValueError):
            self.config.Config(config_dir=outside)
        self.assertFalse(outside.exists())

    def test_nested_enconet_route_is_rejected(self) -> None:
        nested = self.project / "Enconet" / "sieving" / "DATA"
        with self.assertRaises(ValueError):
            self.config.Config(data_dir=nested)
        with self.assertRaises(ValueError):
            self.config.Config(config_dir=nested)
        self.assertFalse(nested.exists())

    def test_symlink_escape_is_rejected(self) -> None:
        outside = self.project.parent / "Enconet"
        outside.mkdir()
        link = self.project / "sieving" / "linked"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")
        with self.assertRaises(ValueError):
            self.config.Config(data_dir=link / "DATA")
        self.assertFalse((outside / "DATA").exists())

    def test_contract_is_local_and_canonical_but_not_an_approval(self) -> None:
        contract = self.contract.load_contract()
        self.assertEqual(self.contract.CONTRACT_PATH, self.schema_dir / "sieving_contract.yml")
        self.assertEqual(len(contract["criteria"]), 18)
        ids = [item["criterion_id"] for item in contract["criteria"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.contract.canonical_codes(), [])
        self.assertEqual(json.loads((self.schema_dir / "sieving_contract.yml").read_text(encoding="utf-8"))["template"]["taxonomy_id"], "APP_B")

    def test_taxonomy_config_rejects_foreign_path_mismatch_and_duplicates(self) -> None:
        path = self.schema_dir / "sieving_contract.yml"
        original = json.loads(path.read_text(encoding="utf-8"))
        foreign = self.project.parent / "Enconet" / "taxonomy.yml"
        foreign.parent.mkdir(exist_ok=True)
        foreign.write_text("taxonomy_id: FOREIGN\ncriteria: []\n", encoding="utf-8")
        before = (foreign.read_bytes(), foreign.stat().st_mtime_ns)

        contract = json.loads(json.dumps(original))
        del contract["template"]["taxonomy_file"]
        path.write_text(json.dumps(contract), encoding="utf-8")
        self.contract.load_contract.cache_clear()
        with self.assertRaises(ValueError):
            self.contract.load_contract()

        contract = json.loads(json.dumps(original))
        contract["template"]["taxonomy_file"] = "../Enconet/taxonomy.yml"
        path.write_text(json.dumps(contract), encoding="utf-8")
        self.contract.load_contract.cache_clear()
        with self.assertRaises(ValueError):
            self.contract.load_contract()

        contract["template"]["taxonomy_file"] = "synthetic_taxonomy.yml"
        path.write_text(json.dumps(contract), encoding="utf-8")
        taxonomy = self.schema_dir / "synthetic_taxonomy.yml"
        taxonomy.write_text("taxonomy_id: WRONG\ncriteria:\n"
                            "  - criterion_id: AREA_2\n    criterion_name: Area Two\n",
                            encoding="utf-8")
        self.contract.load_contract.cache_clear()
        with self.assertRaises(ValueError):
            self.contract.load_contract()

        contract["template"]["taxonomy_id"] = "TEST_SET"
        path.write_text(json.dumps(contract), encoding="utf-8")
        taxonomy.write_text("taxonomy_id: TEST_SET\ncriteria:\n"
                            "  - criterion_id: AREA_2\n    criterion_name: Area Two\n"
                            "  - criterion_id: AREA_2\n    criterion_name: Duplicate\n",
                            encoding="utf-8")
        self.contract.load_contract.cache_clear()
        with self.assertRaises(ValueError):
            self.contract.load_contract()

        taxonomy.write_text("taxonomy_id: TEST_SET\ncriteria: []\n", encoding="utf-8")
        self.contract.load_contract.cache_clear()
        with self.assertRaises(ValueError):
            self.contract.load_contract()
        self.assertEqual((foreign.read_bytes(), foreign.stat().st_mtime_ns), before)


if __name__ == "__main__":
    unittest.main()
