from __future__ import annotations

import pandas as pd
import pytest
from typer.testing import CliRunner

import cli
from src.json_extractor.config import Config
from src.json_extractor.extract.load_and_flatten import ValidationError, validate_item
from src.json_extractor.pipeline import PipelineResult, export_pipeline_result


def validation_error() -> ValidationError:
    return ValidationError("fixture.json", "I-1", "VAL-TEST", "ERROR", "invalid fixture")


def result_with_error() -> PipelineResult:
    return PipelineResult(df=pd.DataFrame({"statement": ["unsafe"]}),
                          validation_errors=[validation_error()], items_loaded=1,
                          items_after_filter=1)


def test_record_side_is_hard_enum_before_side_checks(tmp_path):
    item = {"template_id":"t", "template_version":"1", "taxonomy_id":"APP_B",
            "criterion_id":"APP_B_I", "criterion_name":"Organization",
            "record_side":"INVALID", "evidence_quotes":["quote"], "source":[{}]}
    config = Config(data_dir=tmp_path / "data", config_dir=tmp_path / "config")
    errors = validate_item(item, "fixture.json", config)
    assert any(e.rule_id == "VAL-SIDE-001" and e.severity == "ERROR" for e in errors)


def test_error_validation_blocks_export_by_default(tmp_path):
    output = tmp_path / "blocked.csv"
    with pytest.raises(ValueError, match="ERROR validation"):
        export_pipeline_result(result_with_error(), output, fmt="csv")
    assert not output.exists()


def test_warning_only_does_not_block_export(tmp_path):
    result = PipelineResult(df=pd.DataFrame({"statement": ["review"]}),
        validation_errors=[ValidationError("f", "i", "VAL-WARN", "WARNING", "review")])
    output = export_pipeline_result(result, tmp_path / "warning.csv", fmt="csv")
    assert output.exists()


def test_explicit_override_reason_is_recorded(tmp_path):
    result = result_with_error()
    output = export_pipeline_result(result, tmp_path / "override.csv", fmt="csv",
                                    validation_override_reason="fixture investigation only")
    assert output.exists()
    assert result.validation_override_reason == "fixture investigation only"


def test_cli_override_requires_reason_and_is_visible(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "run_pipeline", lambda **kwargs: result_with_error())
    blocked = CliRunner().invoke(cli.app, ["query", "--files", "fixture.json", "--output",
        str(tmp_path / "blocked.csv"), "--allow-validation-errors"])
    assert blocked.exit_code == 2
    assert not (tmp_path / "blocked.csv").exists()
    allowed = CliRunner().invoke(cli.app, ["query", "--files", "fixture.json", "--output",
        str(tmp_path / "allowed.csv"), "--allow-validation-errors",
        "--validation-override-reason", "fixture investigation only"])
    assert allowed.exit_code == 0
    assert "VALIDATION OVERRIDE" in allowed.stdout
    assert (tmp_path / "allowed.csv").exists()
