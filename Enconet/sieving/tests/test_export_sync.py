from __future__ import annotations

import codecs
from pathlib import Path

import pandas as pd
import pytest

from src.json_extractor.io.export import determine_export_format, export_dataframe


@pytest.fixture
def frame() -> pd.DataFrame:
    return pd.DataFrame({"second": ["zluťoučký"], "first": ["alpha"]})


def test_csv_uses_requested_column_order_and_utf8_bom(tmp_path, frame):
    output = export_dataframe(frame, tmp_path / "result.csv", columns=["first", "second"])
    raw = output.read_bytes()
    assert raw.startswith(codecs.BOM_UTF8)
    assert raw.decode("utf-8-sig").splitlines() == ["first,second", "alpha,zluťoučký"]


def test_xlsx_uses_requested_columns_and_sheet_name(tmp_path, frame):
    output = export_dataframe(
        frame, tmp_path / "result.xlsx", columns=["first"], sheet_name="EVIDENCE"
    )
    workbook = pd.ExcelFile(output, engine="openpyxl")
    assert workbook.sheet_names == ["EVIDENCE"]
    exported = pd.read_excel(output, engine="openpyxl")
    assert exported.to_dict(orient="list") == {"first": ["alpha"]}


@pytest.mark.parametrize(
    ("name", "hint", "expected"),
    [
        ("result.csv", "xlsx", "csv"),
        ("result.markdown", "xlsx", "md"),
        ("result.xlsx", "csv", "xlsx"),
        ("result", "markdown", "md"),
        ("result", None, "xlsx"),
    ],
)
def test_suffix_precedes_format_hint_then_defaults_to_xlsx(name, hint, expected):
    assert determine_export_format(Path(name), hint) == expected


def test_export_adds_suffix_selected_by_format_hint(tmp_path, frame):
    output = export_dataframe(frame, tmp_path / "result", fmt="csv")
    assert output.suffix == ".csv"
    assert output.exists()


def test_missing_requested_column_fails_without_output(tmp_path, frame):
    output = tmp_path / "result.csv"
    with pytest.raises(ValueError, match="Columns not found"):
        export_dataframe(frame, output, columns=["missing"])
    assert not output.exists()
