"""Synthetic local query tests; no audit corpus is read."""
from __future__ import annotations

import importlib
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path

import pandas as pd


PROJECT = Path(__file__).resolve().parents[2]
QUERY_FILES = ("__init__.py", "schema.py", "compiler.py", "engine.py")


class QueryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-query-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        package_dir = self.project / "sieving" / "src" / "json_extractor"
        query_dir = package_dir / "query"
        query_dir.mkdir(parents=True)
        schema_dir = self.project / "schemas"
        schema_dir.mkdir()
        shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / "contract.py",
                        package_dir / "contract.py")
        for name in QUERY_FILES:
            shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / "query" / name,
                            query_dir / name)
        for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schema_dir / name)
        self.addCleanup(self._forget_modules)
        self._forget_modules()
        package = types.ModuleType("ekonerg_query_fixture")
        package.__path__ = [str(package_dir)]
        sys.modules[package.__name__] = package
        self.query = importlib.import_module("ekonerg_query_fixture.query")
        self.compiler = importlib.import_module("ekonerg_query_fixture.query.compiler")
        self.engine = importlib.import_module("ekonerg_query_fixture.query.engine")
        self.frame = pd.DataFrame([
            {"row_id": "R1", "record_side": "RULE", "criterion_id": "APP_B_I",
             "statement": "Independent inspection", "rule_strength": "MANDATORY",
             "evidence_quote_1": "reviewed"},
            {"row_id": "D1", "record_side": "DOCUMENT", "criterion_id": "APP_B_II",
             "statement": "Quality manual", "rule_strength": "",
             "evidence_quote_1": "approved"},
            {"row_id": "D2", "record_side": "DOCUMENT", "criterion_id": "APP_B_III",
             "statement": "Inspection plan", "rule_strength": "",
             "evidence_quote_1": "checked"},
        ])

    @staticmethod
    def _forget_modules() -> None:
        for name in tuple(sys.modules):
            if name == "ekonerg_query_fixture" or name.startswith("ekonerg_query_fixture."):
                del sys.modules[name]

    def _ids(self, expression: str) -> list[str]:
        compiled = self.query.parse_filter_dsl(expression)
        result = self.query.QueryEngine.execute_on_df(self.frame, compiled)
        return list(result["row_id"])

    def test_public_import_and_schema_use_local_contract(self) -> None:
        ids = self.query.QuerySchema.get_field("criterion_id").allowed_values
        self.assertEqual(len(ids), 18)
        self.assertEqual(ids[0], "APP_B_I")
        self.assertIn("statement", self.query.QuerySchema.get_field_names())
        self.assertTrue(Path(self.query.__file__).is_relative_to(self.project))

    def test_and_binds_tighter_than_or(self) -> None:
        expression = "record_side:RULE AND criterion_id:APP_B_I OR criterion_id:APP_B_III"
        compiled = self.query.parse_filter_dsl(expression)
        self.assertEqual([len(clause) for clause in compiled.clauses], [2, 1])
        self.assertEqual(self._ids(expression), ["R1", "D2"])

    def test_in_and_keyword_with_spaces(self) -> None:
        self.assertEqual(self._ids("criterion_id:APP_B_I,APP_B_III"), ["R1", "D2"])
        self.assertEqual(self._ids("keyword:independent inspection"), ["R1"])
        self.assertEqual(self._ids("statement:QUALITY MANUAL"), ["D1"])

    def test_empty_filter_and_legacy_and_form(self) -> None:
        self.assertEqual(self._ids(""), ["R1", "D1", "D2"])
        legacy = self.compiler.CompiledQuery(filters=[
            self.compiler.QueryFilter("record_side", "equals", "DOCUMENT"),
            self.compiler.QueryFilter("criterion_id", "equals", "APP_B_II"),
        ])
        result = self.query.QueryEngine.execute_on_df(self.frame, legacy)
        self.assertEqual(list(result["row_id"]), ["D1"])

    def test_keyword_without_matching_column_returns_no_rows(self) -> None:
        frame = pd.DataFrame([{"row_id": "D1"}])
        compiled = self.query.parse_filter_dsl("keyword:inspection")
        self.assertTrue(self.query.QueryEngine.execute_on_df(frame, compiled).empty)

    def test_invalid_filters_fail_closed(self) -> None:
        for expression in ("unknown:yes", "AND criterion_id:APP_B_I",
                           "criterion_id:APP_B_I OR", "criterion_id:APP_B_I record_side:RULE"):
            with self.subTest(expression=expression):
                with self.assertRaises(self.compiler.DSLParseError):
                    self.query.parse_filter_dsl(expression)
        unknown = self.compiler.QueryFilter("statement", "unexpected", "inspection")
        self.assertFalse(self.query.QueryEngine(self.frame).apply_filter(unknown).any())

    def test_side_warnings_are_clause_local(self) -> None:
        compiled = self.query.parse_filter_dsl("rule_strength:MANDATORY OR record_side:DOCUMENT")
        warnings = self.compiler.validate_compiled_query(compiled)
        self.assertEqual(len(warnings), 1)
        self.assertIn("Clause 1", warnings[0])

    def test_empty_data_does_not_hide_query_limit(self) -> None:
        many = [[self.compiler.QueryFilter("record_side", "equals", "RULE")]
                for _ in range(self.query.QueryEngine.MAX_CLAUSES + 1)]
        compiled = self.compiler.CompiledQuery(clauses=many)
        with self.assertRaises(ValueError):
            self.query.QueryEngine(pd.DataFrame()).execute(compiled)

    def test_no_enconet_dependency_or_foreign_change(self) -> None:
        sibling = self.project.parent / "Enconet"
        sibling.mkdir()
        marker = sibling / "source.txt"
        marker.write_text("unchanged", encoding="utf-8")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
        self.assertEqual(self._ids("record_side:DOCUMENT"), ["D1", "D2"])
        self.assertEqual((marker.read_bytes(), marker.stat().st_mtime_ns), before)
        self.assertFalse((self.project / "Enconet").exists())


if __name__ == "__main__":
    unittest.main()
