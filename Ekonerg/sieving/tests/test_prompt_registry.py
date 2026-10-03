"""Synthetic tests for the owner-authorized Ekonerg prompt bundle."""
from __future__ import annotations

import importlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[2]
PROMPTS = ("active.yml", "appb_rule_v1.md", "appb_document_v1.md", "CHANGELOG.md")
FIXTURES = ("valid_rule.json", "valid_document.json", "malformed_placeholder.json")


class PromptRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-prompts-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        self.prompts = self.project / "sieving" / "prompts"
        fixture_dir = self.prompts / "fixtures"
        fixture_dir.mkdir(parents=True)
        for name in PROMPTS:
            shutil.copyfile(PROJECT / "sieving" / "prompts" / name, self.prompts / name)
        for name in FIXTURES:
            shutil.copyfile(PROJECT / "sieving" / "prompts" / "fixtures" / name, fixture_dir / name)
        package = self.project / "sieving" / "src" / "json_extractor"
        package.mkdir(parents=True)
        for name in ("crumb_validation.py", "contract.py"):
            shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / name,
                            package / name)
        schemas = self.project / "schemas"
        schemas.mkdir()
        for name in ("app_b_json_schema.yml", "app_b_taxonomy.yml", "sieving_contract.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schemas / name)
        contract_path = schemas / "sieving_contract.yml"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        contract["canonical_codes"] = [{
            "ref_code": "DEMO_RULE", "ref_type": "REGULATION",
            "authority_role": "GOVERNING", "allowed_locators": "criteria",
        }]
        contract_path.write_text(json.dumps(contract), encoding="utf-8")
        self.sibling = self.project.parent / "Enconet"
        self.sibling.mkdir()
        self.marker = self.sibling / "untouched.txt"
        self.marker.write_text("same", encoding="utf-8")
        self.before = (self.marker.read_bytes(), self.marker.stat().st_mtime_ns)
        sys.path.insert(0, str(self.project / "sieving"))
        self.addCleanup(lambda: sys.path.remove(str(self.project / "sieving")))
        self.addCleanup(self._forget)
        self._forget()
        self.validator = importlib.import_module("src.json_extractor.crumb_validation")

    @staticmethod
    def _forget() -> None:
        for name in tuple(sys.modules):
            if name == "src" or name.startswith("src."):
                del sys.modules[name]

    def test_registry_has_owner_authorized_active_prompts(self) -> None:
        registry = yaml.safe_load((self.prompts / "active.yml").read_text(encoding="utf-8"))
        self.assertEqual(registry["schema_version"], "1.0")
        self.assertEqual(registry["active"], {
            "RULE": "appb_rule_v1", "DOCUMENT": "appb_document_v1",
        })
        self.assertIn("owner", (self.prompts / "active.yml").read_text(encoding="utf-8").lower())

    def test_candidates_match_local_schema_without_company_specific_text(self) -> None:
        schema = yaml.safe_load((self.project / "schemas" / "app_b_json_schema.yml").read_text(encoding="utf-8"))
        self.assertEqual(set(schema["targets_prompt_versions"]),
                         {"appb_rule_v1", "appb_document_v1"})
        for version in schema["targets_prompt_versions"]:
            text = (self.prompts / f"{version}.md").read_text(encoding="utf-8")
            self.assertIn("schemas/app_b_json_schema.yml", text)
            self.assertIn("approved", text.lower())
            self.assertNotIn("Enconet", text)
        rule = (self.prompts / "appb_rule_v1.md").read_text(encoding="utf-8")
        document = (self.prompts / "appb_document_v1.md").read_text(encoding="utf-8")
        self.assertIn('DOCUMENT_SIDE: "RULE"', rule)
        self.assertIn('DOCUMENT_SIDE: "DOCUMENT"', document)
        self.assertIn("AUTHORITY_REFERENCES: []", document)
        self.assertIn("Recall-first collection rule", rule)
        self.assertIn("Recall-first collection rule", document)

    def test_fresh_history_has_no_old_promotion_or_score(self) -> None:
        history = (self.prompts / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("active", history.lower())
        self.assertIn("owner", history.lower())
        self.assertNotIn("Enconet", history)
        self.assertNotIn("2026-07-13", history)
        self.assertNotIn("baseline", history.lower())

    def test_invented_valid_fixtures_pass_format_only(self) -> None:
        for name in ("valid_rule.json", "valid_document.json"):
            data = json.loads((self.prompts / "fixtures" / name).read_text(encoding="utf-8"))
            self.assertIn("synthetic", data["document"]["name"].lower())
            self.assertTrue(self.validator.validate_payload(data, strict=True).passed, name)
            for item in data["items"]:
                for quote in item["evidence_quotes"]:
                    self.assertIn("invented", quote["quote_original"].lower())

    def test_malformed_fixture_is_rejected_and_sibling_is_untouched(self) -> None:
        data = json.loads((self.prompts / "fixtures" / "malformed_placeholder.json").read_text(encoding="utf-8"))
        result = self.validator.validate_payload(data)
        self.assertFalse(result.passed)
        self.assertGreaterEqual(len(result.errors), 3)
        self.assertEqual((self.marker.read_bytes(), self.marker.stat().st_mtime_ns), self.before)
        self.assertFalse((self.project / "Enconet").exists())


if __name__ == "__main__":
    unittest.main()
