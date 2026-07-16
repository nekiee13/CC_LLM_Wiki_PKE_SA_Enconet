"""Load the ADR-0003 canonical sieving contract."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "schemas" / "sieving_contract.yml"
TAXONOMY_PATH = CONTRACT_PATH.with_name("app_b_taxonomy.yml")


@lru_cache(maxsize=1)
def load_contract() -> dict[str, Any]:
    """Return the JSON-compatible YAML contract after structural checks."""
    data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    required = {"template", "canonical_codes", "enums", "input_fields", "columns", "query_fields"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Sieving contract missing sections: {sorted(missing)}")
    if "criteria" in data:
        raise ValueError("Sieving contract must not re-declare the APP_B taxonomy")
    taxonomy = yaml.safe_load(TAXONOMY_PATH.read_text(encoding="utf-8"))
    criteria = taxonomy.get("criteria") if isinstance(taxonomy, dict) else None
    if not isinstance(criteria, list) or len(criteria) != 18:
        raise ValueError("APP_B taxonomy must contain exactly 18 criteria")
    data["criteria"] = [
        {"criterion_id": entry["criterion_id"], "criterion_name": entry["criterion_name"]}
        for entry in criteria
    ]
    return data


def canonical_codes() -> list[dict[str, Any]]:
    """Expand symbolic locator sources into runtime-ready code definitions."""
    contract = load_contract()
    criterion_ids = [entry["criterion_id"] for entry in contract["criteria"]]
    codes = []
    for entry in contract["canonical_codes"]:
        code = dict(entry)
        if code.get("allowed_locators") == "criteria":
            code["allowed_locators"] = criterion_ids
        codes.append(code)
    return codes
