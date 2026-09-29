"""Synthetic crumb-validation tests; no audit corpus is read."""
from __future__ import annotations

import importlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
PACKAGE = PROJECT / "sieving" / "src" / "json_extractor"


def rule_crumb() -> dict:
    return {
        "document": {
            "name": "Synthetic rule", "date": "2026-09-29", "document_side": "RULE",
            "authority_references": [{
                "authority_role": "GOVERNING", "source_code": "DEMO_RULE",
                "source_locator": "APP_B_I", "applicability": "APPLICABLE",
            }],
        },
        "items": [{
            "item_id": "R-1", "criterion_id": "APP_B_I", "criterion_name": "Organization",
            "statement": "Made-up statement", "item_type": "requirement", "entities": {},
            "sources": [{"source_locator": "APP_B_I"}],
            "evidence_quotes": [{"quote_original": "Izmišljeni citat", "quote_language": "hr"}],
        }],
    }


class CrumbValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-crumb-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Čista Tvrtka"
        package = self.project / "sieving" / "src" / "json_extractor"
        package.mkdir(parents=True)
        for name in ("crumb_validation.py", "contract.py"):
            shutil.copyfile(PACKAGE / name, package / name)
        schemas = self.project / "schemas"
        schemas.mkdir()
        for name in ("app_b_taxonomy.yml", "sieving_contract.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schemas / name)
        self.contract_path = schemas / "sieving_contract.yml"
        contract = json.loads(self.contract_path.read_text(encoding="utf-8"))
        contract["canonical_codes"] = [{
            "ref_code": "DEMO_RULE", "ref_type": "REGULATION",
            "authority_role": "GOVERNING", "allowed_locators": "criteria",
        }, {
            "ref_code": "DEMO_GUIDE", "ref_type": "STANDARD",
            "authority_role": "INTERPRETIVE", "locator_pattern": "^G-[0-9]+$",
            "requires_applicability_basis": True,
        }]
        self.contract_path.write_text(json.dumps(contract), encoding="utf-8")
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

    def test_valid_rule_uses_local_taxonomy(self) -> None:
        result = self.validator.validate_payload(rule_crumb(), strict=True)
        self.assertTrue(result.passed)
        self.assertEqual(result.errors, [])
        self.assertTrue(self.validator.TAXONOMY.is_relative_to(self.project))

    def test_document_side_rejects_rule_fields_and_refs(self) -> None:
        data = rule_crumb()
        data["document"]["document_side"] = "DOCUMENT"
        data["items"][0]["rule_key"] = "not allowed"
        result = self.validator.validate_payload(data)
        self.assertFalse(result.passed)
        self.assertTrue(any("DOCUMENT" in error for error in result.errors))

    def test_quote_requires_original_language_and_no_translation(self) -> None:
        data = rule_crumb()
        quote = data["items"][0]["evidence_quotes"][0]
        quote["quote_language"] = "xx"
        quote["statement_en"] = "invented translation"
        result = self.validator.validate_payload(data)
        self.assertTrue(any("quote_language" in error for error in result.errors))
        self.assertTrue(any("statement_en" in error for error in result.errors))

    def test_configured_source_needs_basis_and_role_code_match(self) -> None:
        data = rule_crumb()
        ref = data["document"]["authority_references"][0]
        ref["source_code"] = "DEMO_GUIDE"
        result = self.validator.validate_payload(data)
        self.assertTrue(any("applicability_basis" in error for error in result.errors))
        ref["authority_role"] = "GOVERNING"
        result = self.validator.validate_payload(data)
        self.assertTrue(any("not valid for GOVERNING" in error for error in result.errors))

    def test_empty_contract_rejects_inherited_source_code(self) -> None:
        contract = json.loads(self.contract_path.read_text(encoding="utf-8"))
        contract["canonical_codes"] = []
        self.contract_path.write_text(json.dumps(contract), encoding="utf-8")
        result = self.validator.validate_payload(rule_crumb())
        self.assertFalse(result.passed)
        self.assertTrue(any("DEMO_RULE" in error for error in result.errors))

    def test_source_locator_follows_selected_code_rule(self) -> None:
        data = rule_crumb()
        ref = data["document"]["authority_references"][0]
        ref["source_locator"] = "BAD"
        result = self.validator.validate_payload(data)
        self.assertTrue(any("source_locator" in error for error in result.errors))
        ref.update(source_code="DEMO_GUIDE", authority_role="INTERPRETIVE",
                   source_locator="G-7", applicability_basis="Test-only basis")
        result = self.validator.validate_payload(data)
        self.assertTrue(result.passed)
        ref["source_locator"] = "X-7"
        result = self.validator.validate_payload(data)
        self.assertTrue(any("source_locator" in error for error in result.errors))

    def test_strict_optional_warnings_become_errors(self) -> None:
        data = rule_crumb()
        data["items"][0].pop("entities")
        normal = self.validator.validate_payload(data)
        strict = self.validator.validate_payload(data, strict=True)
        self.assertTrue(normal.passed)
        self.assertFalse(strict.passed)
        self.assertTrue(any("strict warning" in error for error in strict.errors))

    def test_wrong_json_types_report_errors_instead_of_crashing(self) -> None:
        data = rule_crumb()
        data["document"]["document_side"] = ["RULE"]
        data["document"]["authority_references"][0]["authority_role"] = ["GOVERNING"]
        data["items"][0]["criterion_id"] = ["APP_B_I"]
        data["items"][0]["evidence_quotes"][0]["quote_language"] = ["hr"]
        result = self.validator.validate_payload(data)
        self.assertFalse(result.passed)
        for field in ("document_side", "authority_role", "criterion_id/name", "quote_language"):
            self.assertTrue(any(field in error for error in result.errors), field)

    def test_local_file_and_foreign_paths(self) -> None:
        local = self.project / "sieving" / "crumb.json"
        local.write_text(json.dumps(rule_crumb(), ensure_ascii=False), encoding="utf-8")
        parsed, result = self.validator.validate_file(Path("sieving/crumb.json"))
        self.assertTrue(result.passed)
        self.assertEqual(parsed["document"]["name"], "Synthetic rule")
        sibling = self.project.parent / "Enconet"
        sibling.mkdir()
        foreign = sibling / "crumb.json"
        foreign.write_text(json.dumps(rule_crumb()), encoding="utf-8")
        before = (foreign.read_bytes(), foreign.stat().st_mtime_ns)
        with self.assertRaises(ValueError):
            self.validator.validate_file(foreign)
        with self.assertRaises(ValueError):
            self.validator.validate_file(self.project / "Enconet" / "crumb.json")
        self.assertEqual((foreign.read_bytes(), foreign.stat().st_mtime_ns), before)

    def test_link_and_hardlink_to_foreign_file_are_rejected(self) -> None:
        sibling = self.project.parent / "Enconet"
        sibling.mkdir()
        foreign = sibling / "crumb.json"
        foreign.write_text(json.dumps(rule_crumb()), encoding="utf-8")
        local_dir = self.project / "sieving"
        link = local_dir / "linked.json"
        try:
            link.symlink_to(foreign)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")
        with self.assertRaises(ValueError):
            self.validator.validate_file(link)
        hard = local_dir / "hard.json"
        try:
            os.link(foreign, hard)
        except OSError as exc:
            self.skipTest(f"hard link unavailable: {exc}")
        with self.assertRaises(ValueError):
            self.validator.validate_file(hard)


if __name__ == "__main__":
    unittest.main()
