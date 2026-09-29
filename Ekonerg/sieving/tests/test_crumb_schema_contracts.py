"""Synthetic checks for the local crumb schema and vocabulary pair."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[2]
SCHEMAS = ("sieving_contract.yml", "app_b_taxonomy.yml", "app_b_json_schema.yml", "vocabularies.yml")


class CrumbSchemaContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-crumb-schema-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        self.schema_dir = self.project / "schemas"
        self.schema_dir.mkdir(parents=True)
        for name in SCHEMAS:
            shutil.copyfile(PROJECT / "schemas" / name, self.schema_dir / name)
        self.sibling = self.project.parent / "Enconet"
        self.sibling.mkdir()
        self.marker = self.sibling / "untouched.txt"
        self.marker.write_text("same", encoding="utf-8")
        self.before = (self.marker.read_bytes(), self.marker.stat().st_mtime_ns)
        self.crumb = yaml.safe_load((self.schema_dir / "app_b_json_schema.yml").read_text(encoding="utf-8"))
        self.vocab = yaml.safe_load((self.schema_dir / "vocabularies.yml").read_text(encoding="utf-8"))
        self.contract = json.loads((self.schema_dir / "sieving_contract.yml").read_text(encoding="utf-8"))

    def test_schema_names_local_prompt_versions_and_required_shape(self) -> None:
        self.assertEqual(self.crumb["schema_version"], "1.1")
        self.assertEqual(set(self.crumb["targets_prompt_versions"]),
                         {"appb_rule_v1", "appb_document_v1"})
        self.assertEqual(set(self.crumb["document_block"]["required_fields"]),
                         {"name", "date", "document_side", "authority_references"})
        self.assertTrue({"item_id", "criterion_id", "criterion_name", "statement",
                         "evidence_quotes", "source"}.issubset(
                             self.crumb["item_block"]["required_fields"]))

    def test_quote_rules_keep_original_text_and_forbid_transforms(self) -> None:
        quotes = self.crumb["evidence_quote"]
        self.assertEqual(quotes["required_fields"]["quote_original"]["tier"], "strict")
        self.assertEqual(quotes["required_fields"]["quote_language"]["enum"], "languages")
        self.assertEqual(set(quotes["forbidden_fields"]),
                         {"statement_en", "translation_status", "meaning_flag"})
        self.assertEqual(set(self.vocab["vocabularies"]["languages"]["values"]),
                         {"sl", "en", "hr"})

    def test_vocabularies_mirror_local_contract_without_approval(self) -> None:
        values = self.vocab["vocabularies"]
        codes = self.contract["canonical_codes"]
        self.assertEqual(values["document_sides"]["values"], self.contract["enums"]["record_side"])
        self.assertEqual(values["source_rules"]["values"],
                         [item["ref_code"] for item in codes if item["authority_role"] == "GOVERNING"])
        self.assertEqual(values["authority_sources"]["values"],
                         [item["ref_code"] for item in codes])
        self.assertEqual(values["authority_roles"]["values"],
                         self.contract["enums"]["authority_role"])
        for name in ("app_b_json_schema.yml", "vocabularies.yml"):
            text = (self.schema_dir / name).read_text(encoding="utf-8")
            self.assertIn("not approved", text.lower())
            self.assertNotIn("Enconet", text)

    def test_fake_sibling_is_untouched_and_no_nested_enconet_exists(self) -> None:
        self.assertEqual((self.marker.read_bytes(), self.marker.stat().st_mtime_ns), self.before)
        self.assertFalse((self.project / "Enconet").exists())


if __name__ == "__main__":
    unittest.main()
