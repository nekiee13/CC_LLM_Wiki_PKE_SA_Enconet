"""EPIC15 vendored-library integration and consumer-contract regression tests."""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

import openpyxl

ENCONET = Path(__file__).resolve().parents[1]
SIEVING = ENCONET / "sieving"
FIXTURES = SIEVING / "tests" / "fixtures"
sys.path.insert(0, str(SIEVING / "src"))

from json_extractor.pipeline import export_pipeline_result, run_pipeline  # noqa: E402

COLUMNS = ["item_id", "criterion_id", "statement", "source_page",
           "entities_organizations", "rule_key"]
PRIVATE_PANDAS_METHODS = {"_append"}


def _private_pandas_api_offenders(source: str, label: str = "<source>") -> list[str]:
    """Return private pandas API uses, including instance methods and modules."""
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute):
            direct_private = (
                node.attr.startswith("_")
                and isinstance(node.value, ast.Name)
                and node.value.id in {"pd", "pandas"}
            )
            if direct_private or node.attr in PRIVATE_PANDAS_METHODS:
                offenders.append(f"{label}:{node.lineno}:{node.attr}")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(("pandas.core", "pandas._")):
                    offenders.append(f"{label}:{node.lineno}:{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            private_member = module == "pandas" and any(
                alias.name.startswith("_") for alias in node.names
            )
            if module.startswith(("pandas.core", "pandas._")) or private_member:
                offenders.append(f"{label}:{node.lineno}:{module}")
    return offenders


def test_project_scripts_resolve_only_the_vendored_implementation() -> None:
    for name in ("import_crumbs.py", "sieve_run.py", "validate_app_b_json.py", "query_crumbs.py"):
        text = (ENCONET / "scripts" / name).read_text(encoding="utf-8")
        assert "json_extractor" in text or "sieving_lib" in text
        assert "sieving.cli" not in text and "src.json_extractor" not in text
    duplicate_names = {"flatten_entities", "flatten_source", "flatten_json_to_records",
                       "flatten_multiple_files", "validate_payload", "validate_file"}
    for path in (ENCONET / "scripts").glob("*.py"):
        definitions = {node.name for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
                       if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        assert not definitions & duplicate_names, f"duplicated crumb logic in {path.name}"


def test_dependencies_are_exactly_pinned_and_private_pandas_apis_are_absent() -> None:
    requirements = (SIEVING / "requirements.txt").read_text(encoding="utf-8").splitlines()
    assert requirements and all(re.fullmatch(r"[A-Za-z0-9_-]+==[^=<>!~]+", line) for line in requirements)
    offenders = []
    for path in (SIEVING / "src").rglob("*.py"):
        offenders.extend(_private_pandas_api_offenders(
            path.read_text(encoding="utf-8"), str(path.relative_to(SIEVING))
        ))
    assert offenders == []


def test_private_pandas_guard_detects_historical_and_internal_api_patterns() -> None:
    snippets = {
        "dataframe-instance-method": "df = pd.DataFrame(); df = df._append(row)",
        "private-module-from": "from pandas.core.frame import DataFrame",
        "private-module-import": "import pandas._libs",
        "private-member": "from pandas import _testing",
    }
    for label, snippet in snippets.items():
        assert _private_pandas_api_offenders(snippet, label), label
    assert _private_pandas_api_offenders("class A:\n    def f(self): return self._helper()") == []


def test_schema_drift_warns_by_default_and_strict_mode_blocks(tmp_path: Path) -> None:
    original = (FIXTURES / "epic15_export_input.json").read_text(encoding="utf-8")
    drifted = original.replace('"item_type": "requirement",', '"unexpected_epic15": true,')
    path = tmp_path / "drifted.json"
    path.write_text(drifted, encoding="utf-8")
    warning_result = run_pipeline(file_paths=[path])
    warnings = [issue.message for issue in warning_result.validation_errors
                if issue.rule_id == "VAL-DRIFT-001" and issue.severity == "WARNING"]
    assert any("missing expected field: items[0].item_type" in message for message in warnings)
    assert any("unexpected field: items[0].unexpected_epic15" in message for message in warnings)
    strict_result = run_pipeline(file_paths=[path], strict=True)
    strict_drift = [issue for issue in strict_result.validation_errors
                    if issue.rule_id == "VAL-DRIFT-001"]
    assert strict_drift and all(issue.severity == "ERROR" for issue in strict_drift)
    with __import__("pytest").raises(ValueError, match="Export blocked"):
        export_pipeline_result(strict_result, tmp_path / "blocked.csv")


def test_project_wrapper_strict_mode_returns_nonzero_on_drift(tmp_path: Path) -> None:
    source = (FIXTURES / "epic15_export_input.json").read_text(encoding="utf-8")
    path = tmp_path / "drift.json"
    path.write_text(source.replace('"item_type": "requirement",', '"new_field": 1,'), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(ENCONET / "scripts" / "query_crumbs.py"), "query",
         "--files", str(path), "--strict"], text=True, capture_output=True, check=False,
    )
    assert proc.returncode == 2
    assert "missing expected field" in proc.stderr and "unexpected field" in proc.stderr


def test_csv_and_xlsx_exports_match_locked_fixtures(tmp_path: Path) -> None:
    result = run_pipeline(file_paths=[FIXTURES / "epic15_export_input.json"])
    assert not result.validation_errors
    actual_csv = export_pipeline_result(result, tmp_path / "actual.csv", columns=COLUMNS)
    expected_csv = (FIXTURES / "epic15_expected.csv").read_text(encoding="utf-8")
    assert actual_csv.read_text(encoding="utf-8-sig") == expected_csv

    actual_xlsx = export_pipeline_result(result, tmp_path / "actual.xlsx", columns=COLUMNS)
    expected_xlsx = FIXTURES / "epic15_expected.xlsx"
    actual_sheet = openpyxl.load_workbook(actual_xlsx, read_only=True, data_only=True)["RESULT"]
    expected_sheet = openpyxl.load_workbook(expected_xlsx, read_only=True, data_only=True)["RESULT"]
    assert list(actual_sheet.values) == list(expected_sheet.values)
