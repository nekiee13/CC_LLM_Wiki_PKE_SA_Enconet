from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from cli import app
from src.json_extractor.pipeline import export_pipeline_result, run_pipeline


def sample_file() -> Path:
    return sorted((Path(__file__).parents[1] / "DATA" / "DOCUMENT").rglob("*.json"))[0]


def test_parse_error_fails_closed():
    result = run_pipeline(file_paths=[sample_file()], filter_expr="criterion_id:")
    assert result.filter_error
    assert result.df.empty
    assert not result.unfiltered_preview_used


def test_execution_error_fails_closed():
    with patch("src.json_extractor.pipeline.QueryEngine.execute_on_df", side_effect=RuntimeError("boom")):
        result = run_pipeline(file_paths=[sample_file()], filter_expr="criterion_id:APP_B_I")
    assert result.filter_error == "Filter execution error: boom"
    assert result.df.empty


def test_preview_override_is_visible_and_keeps_rows():
    result = run_pipeline(file_paths=[sample_file()], filter_expr="criterion_id:",
                          allow_unfiltered_preview=True)
    assert result.filter_error and result.unfiltered_preview_used
    assert not result.df.empty
    runner = CliRunner()
    cli = runner.invoke(app, ["query", "--files", str(sample_file()), "--filter",
                              "criterion_id:", "--preview", "--allow-unfiltered-preview"])
    assert cli.exit_code == 0
    assert "DEVELOPMENT OVERRIDE" in cli.stdout


def test_export_blocked_even_with_preview_override(tmp_path):
    result = run_pipeline(file_paths=[sample_file()], filter_expr="criterion_id:",
                          allow_unfiltered_preview=True)
    output = tmp_path / "must-not-exist.csv"
    with pytest.raises(ValueError, match="Export blocked"):
        export_pipeline_result(result, output, fmt="csv")
    assert not output.exists()


def test_cli_invalid_filter_nonzero_and_no_output(tmp_path):
    output = tmp_path / "must-not-exist.csv"
    cli = CliRunner().invoke(app, ["query", "--files", str(sample_file()), "--filter",
                                   "criterion_id:", "--output", str(output)])
    assert cli.exit_code == 2
    assert not output.exists()


def test_preview_override_requires_preview_flag():
    cli = CliRunner().invoke(app, ["query", "--files", str(sample_file()), "--filter",
                                   "criterion_id:", "--allow-unfiltered-preview"])
    assert cli.exit_code == 2
    assert "requires --preview" in cli.stdout
