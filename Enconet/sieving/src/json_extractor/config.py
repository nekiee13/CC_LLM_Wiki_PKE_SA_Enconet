"""Configuration backed by the ADR-0003 canonical sieving contract."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .contract import canonical_codes, load_contract


@dataclass
class Config:
    data_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2] / "DATA")
    config_dir: Path = field(default_factory=lambda: Path.home() / ".json_extractor")
    default_columns: list[str] = field(default_factory=lambda: list(load_contract()["columns"]["default"]))
    all_columns: list[str] = field(default_factory=lambda: list(load_contract()["columns"]["all"]))

    def __post_init__(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    @property
    def column_defaults_path(self) -> Path:
        return self.config_dir / "column_defaults.json"

    def load_column_defaults(self) -> list[str]:
        if self.column_defaults_path.exists():
            try:
                data = json.loads(self.column_defaults_path.read_text(encoding="utf-8"))
                valid = [column for column in data.get("columns", self.default_columns)
                         if column in self.all_columns]
                return valid or self.default_columns
            except Exception as exc:
                print(f"Warning: Could not load column defaults: {exc}")
        return self.default_columns

    def save_column_defaults(self, columns: list[str]) -> None:
        try:
            valid = [column for column in columns if column in self.all_columns]
            data = {"columns": valid, "version": "0.1"}
            self.column_defaults_path.write_text(
                json.dumps(data, indent=2), encoding="utf-8"
            )
            print(f"Saved {len(valid)} columns as default to {self.column_defaults_path}")
        except Exception as exc:
            print(f"Error saving column defaults: {exc}")

    def get_canonical_criteria(self) -> list[dict[str, str]]:
        return list(load_contract()["criteria"])

    def get_canonical_codes(self) -> list[dict[str, Any]]:
        return canonical_codes()

    def criterion_name_for_id(self, criterion_id: str) -> Optional[str]:
        return next((entry["criterion_name"] for entry in self.get_canonical_criteria()
                     if entry["criterion_id"] == criterion_id), None)


_config: Optional[Config] = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(config: Config) -> None:
    global _config
    _config = config
