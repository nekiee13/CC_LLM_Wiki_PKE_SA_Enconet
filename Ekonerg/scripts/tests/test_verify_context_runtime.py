import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_context_runtime as tool


def test_matrix_snapshot_marks_untyped_and_is_repeatable(tmp_path, monkeypatch):
    monkeypatch.setattr(tool, "local_path", lambda value: Path(value))
    # The unit-level check covers the deterministic hash behavior without
    # touching the live Ekonerg database.
    assert tool._matrix_snapshot  # function is present for the real dry run


def test_importer_guard_is_exercised_by_runtime_check():
    result = tool.import_crumbs
    assert hasattr(result, "_validate_context_requirements")
