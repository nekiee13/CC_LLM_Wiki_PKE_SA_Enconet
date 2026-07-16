#!/usr/bin/env python3
"""Score generated crumbs against a versioned, human-approved golden calibration set."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
APPROVALS = ROOT / "manifests" / "approvals.csv"


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def approved(reference: str | None, approvals: Path) -> bool:
    if not reference or not approvals.is_file():
        return False
    with approvals.open(encoding="utf-8-sig", newline="") as handle:
        return any(row["object_id"] == reference and row["decision"].lower() == "approved"
                   for row in csv.DictReader(handle))


def _key(item: dict[str, object]) -> tuple[str, str, tuple[str, ...]]:
    quotes = item.get("evidence_quotes", item.get("quotes", []))
    quote_values = [q["quote_original"] if isinstance(q, dict) else str(q) for q in quotes]
    return str(item["criterion_id"]), normalize(str(item["statement"])), tuple(sorted(normalize(q) for q in quote_values))


def score(expected: dict[str, object], actual: dict[str, object], *, approvals: Path = APPROVALS) -> dict[str, object]:
    expected_items = expected.get("expected_crumbs")
    actual_items = actual.get("items")
    if not isinstance(expected_items, list) or not isinstance(actual_items, list):
        raise ValueError("expected_crumbs and actual items must be lists")
    expected_map, actual_map = {_key(item): item for item in expected_items}, {_key(item): item for item in actual_items}
    found_keys = set(expected_map) & set(actual_map)
    missed_keys = set(expected_map) - set(actual_map)
    spurious_keys = set(actual_map) - set(expected_map)
    criteria = sorted({key[0] for key in expected_map} | {key[0] for key in actual_map})
    per_criterion = {}
    for criterion in criteria:
        per_criterion[criterion] = {
            "found": sum(key[0] == criterion for key in found_keys),
            "missed": sum(key[0] == criterion for key in missed_keys),
            "spurious": sum(key[0] == criterion for key in spurious_keys),
        }
    approval_ref = expected.get("approval_ref")
    is_approved = expected.get("status") == "approved" and approved(
        str(approval_ref) if approval_ref else None, approvals
    )
    return {
        "schema_version": "1.0", "fixture_version": expected.get("fixture_version"),
        "prompt_version": actual.get("prompt_version"),
        "golden_approval_ref": approval_ref, "golden_approved": is_approved,
        "found": len(found_keys), "missed": len(missed_keys), "spurious": len(spurious_keys),
        "per_criterion": per_criterion,
        "promotion_ready": bool(is_approved and not missed_keys and not spurious_keys),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--golden", type=Path, required=True)
    parser.add_argument("--actual", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--allow-draft", action="store_true",
                        help="diagnostic scoring only; never makes promotion eligible")
    args = parser.parse_args()
    try:
        expected = yaml.safe_load(args.golden.read_text(encoding="utf-8"))
        actual = json.loads(args.actual.read_text(encoding="utf-8"))
        result = score(expected, actual, approvals=args.approvals)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        if not result["golden_approved"] and not args.allow_draft:
            print("score_sieving: FAIL - golden set lacks a recorded human approval", file=sys.stderr)
            return 2
        print(f"score_sieving: PASS - found={result['found']}; missed={result['missed']}; spurious={result['spurious']}; promotion_ready={result['promotion_ready']}")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"score_sieving: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
