"""Load the project-local canonical sieving template contract.

The template does not approve source editions or applicability.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "schemas" / "sieving_contract.yml"
_TAXONOMY_FILE = re.compile(r"[a-z][a-z0-9_]*\.yml\Z")


@lru_cache(maxsize=1)
def load_contract() -> dict[str, Any]:
    """Return the local JSON-compatible YAML contract after structural checks."""
    data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    required = {"template", "canonical_codes", "enums", "input_fields", "columns", "query_fields"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Sieving contract missing sections: {sorted(missing)}")
    if "criteria" in data:
        raise ValueError("Sieving contract must not re-declare the taxonomy")
    template = data.get("template")
    if not isinstance(template, dict) or any(
        not isinstance(template.get(key), str) or not template[key].strip()
        for key in ("id", "version", "taxonomy_id", "taxonomy_file")
    ):
        raise ValueError("Sieving template identity and taxonomy file are required")
    filename = template["taxonomy_file"]
    if _TAXONOMY_FILE.fullmatch(filename) is None:
        raise ValueError("Taxonomy file must be a local YAML filename")
    taxonomy_path = CONTRACT_PATH.with_name(filename)
    if taxonomy_path.is_symlink() or taxonomy_path.resolve().parent != CONTRACT_PATH.parent.resolve():
        raise ValueError("Taxonomy file must stay in the local schema directory")
    try:
        taxonomy = yaml.safe_load(taxonomy_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read local taxonomy file: {exc}") from exc
    if not isinstance(taxonomy, dict) or taxonomy.get("taxonomy_id") != template["taxonomy_id"]:
        raise ValueError("Taxonomy ID does not match the sieving contract")
    criteria = taxonomy.get("criteria") if isinstance(taxonomy, dict) else None
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("Taxonomy needs at least one criterion")
    seen: set[str] = set()
    for entry in criteria:
        if not isinstance(entry, dict):
            raise ValueError("Taxonomy criteria must be objects")
        criterion_id, criterion_name = entry.get("criterion_id"), entry.get("criterion_name")
        if (not isinstance(criterion_id, str) or not criterion_id.strip()
                or not isinstance(criterion_name, str) or not criterion_name.strip()
                or criterion_id in seen):
            raise ValueError("Taxonomy needs unique, non-empty criterion IDs and names")
        seen.add(criterion_id)
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
