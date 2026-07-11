"""Load the ADR-0003 canonical sieving contract."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "schemas" / "sieving_contract.yml"


@lru_cache(maxsize=1)
def load_contract() -> dict[str, Any]:
    """Return the JSON-compatible YAML contract after structural checks."""
    data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    required = {"template", "criteria", "canonical_codes", "enums", "columns", "query_fields"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Sieving contract missing sections: {sorted(missing)}")
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
