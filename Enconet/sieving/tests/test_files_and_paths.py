from __future__ import annotations

from pathlib import Path

from src.json_extractor.config import Config
from src.json_extractor.io.files import discover_json_files, read_json_file


def test_bad_json_and_non_object_roots_are_classified(tmp_path):
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    sequence = tmp_path / "sequence.json"
    sequence.write_text("[]", encoding="utf-8")

    assert read_json_file(malformed)[1].error_type == "JSON_DECODE_ERROR"
    assert read_json_file(sequence)[1].error_type == "INVALID_ROOT"


def test_discovery_is_recursive_unique_and_relative_path_sorted(tmp_path):
    for relative in ("z.json", "nested/B.json", "nested/a.json"):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")
    found = discover_json_files(tmp_path, ["*.json", "a.json"])
    assert [path.relative_to(tmp_path).as_posix() for path in found] == [
        "nested/a.json", "nested/B.json", "z.json"
    ]


def test_default_data_path_is_package_anchored_across_working_directories(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = Config(config_dir=tmp_path / "config")
    expected = Path(__file__).resolve().parents[1] / "DATA"
    assert config.data_dir.resolve() == expected.resolve()
