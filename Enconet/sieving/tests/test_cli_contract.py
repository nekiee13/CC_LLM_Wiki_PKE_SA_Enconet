from __future__ import annotations

from typer.testing import CliRunner

from cli import app


def test_query_requires_files_or_all():
    result = CliRunner().invoke(app, ["query"])
    assert result.exit_code == 1
    assert "Must specify --files or --all" in result.stdout


def test_missing_file_is_reported_without_crashing(tmp_path):
    result = CliRunner().invoke(app, ["query", "--files", str(tmp_path / "missing.json")])
    assert result.exit_code == 0
    assert "Files processed: 1" in result.stdout
    assert "Items loaded: 0" in result.stdout
    assert "Issues detected" in result.stdout
    assert "missing.json" in result.stdout


def test_list_files_missing_directory_is_nonzero(tmp_path):
    result = CliRunner().invoke(app, ["list-files", "--data-dir", str(tmp_path / "missing")])
    assert result.exit_code == 1
    assert "Data directory does not exist" in result.stdout
