#!/usr/bin/env python3
"""Score local crumbs against a local golden set; never grant approval."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import sys

import yaml

from project_paths import configure_standard_streams, local_path

ROOT = Path(__file__).resolve().parents[1]
APPROVALS = ROOT / "manifests" / "approvals.csv"
HEADER = ["object_id", "decision", "date", "reviewer", "notes"]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def approved(reference: str | None, approvals: Path) -> bool:
    path = local_path(approvals)
    if not reference or not path.is_file():
        return False
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        if rows.fieldnames != HEADER:
            return False
        return any(row.get("object_id") == reference
                   and row.get("decision", "").lower() == "approved"
                   and row.get("date") and row.get("reviewer") for row in rows)


def _key(item: object) -> tuple[str, str, tuple[str, ...]]:
    if not isinstance(item, dict):
        raise ValueError("crumb must be an object")
    criterion = item.get("criterion_id")
    statement = item.get("statement")
    quotes = item.get("evidence_quotes", item.get("quotes"))
    if not isinstance(criterion, str) or not criterion.strip():
        raise ValueError("crumb criterion_id is missing")
    if not isinstance(statement, str) or not statement.strip():
        raise ValueError("crumb statement is missing")
    if not isinstance(quotes, list) or not quotes:
        raise ValueError("crumb quotes are missing")
    values: list[str] = []
    for quote in quotes:
        value = quote.get("quote_original") if isinstance(quote, dict) else quote
        if not isinstance(value, str) or not value.strip():
            raise ValueError("crumb has an empty quote")
        values.append(normalize(value))
    return criterion, normalize(statement), tuple(sorted(values))


def _keys(items: list[object], side: str) -> set[tuple[str, str, tuple[str, ...]]]:
    keys = [_key(item) for item in items]
    if len(keys) != len(set(keys)):
        raise ValueError(f"duplicate {side} crumb")
    return set(keys)


def score(expected: object, actual: object, *, approvals: Path = APPROVALS) -> dict[str, object]:
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        raise ValueError("golden and actual files must be objects")
    expected_items = expected.get("expected_crumbs")
    actual_items = actual.get("items")
    if not isinstance(expected_items, list) or not isinstance(actual_items, list):
        raise ValueError("expected_crumbs and actual items must be lists")
    prompt = actual.get("prompt_version")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("actual prompt_version is missing")
    golden_document = expected.get("document")
    actual_document = actual.get("document")
    if expected.get("status") == "approved":
        if (not isinstance(golden_document, dict) or
                not isinstance(actual_document, dict) or
                not isinstance(golden_document.get("doc_id"), str) or
                not golden_document["doc_id"] or
                golden_document["doc_id"] != actual_document.get("doc_id")):
            raise ValueError("golden and actual document IDs must match")
    expected_keys = _keys(expected_items, "golden")
    actual_keys = _keys(actual_items, "actual")
    found = expected_keys & actual_keys
    missed = expected_keys - actual_keys
    spurious = actual_keys - expected_keys
    criteria = sorted({key[0] for key in expected_keys | actual_keys})
    per_criterion = {
        criterion: {
            "found": sum(key[0] == criterion for key in found),
            "missed": sum(key[0] == criterion for key in missed),
            "spurious": sum(key[0] == criterion for key in spurious),
        } for criterion in criteria
    }
    reference = expected.get("approval_ref")
    is_approved = (expected.get("status") == "approved"
                   and isinstance(reference, str) and bool(reference)
                   and bool(expected.get("document")) and bool(expected_keys)
                   and approved(reference, approvals))
    return {
        "schema_version": "1.0", "fixture_version": expected.get("fixture_version"),
        "prompt_version": prompt, "golden_approval_ref": reference,
        "golden_approved": is_approved, "found": len(found),
        "missed": len(missed), "spurious": len(spurious),
        "per_criterion": per_criterion,
        "promotion_ready": bool(is_approved and not missed and not spurious),
    }


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--golden", type=Path, required=True)
    parser.add_argument("--actual", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--allow-draft", action="store_true",
                        help="diagnostic only; never grants approval")
    args = parser.parse_args()
    try:
        golden = local_path(args.golden)
        actual = local_path(args.actual)
        output = local_path(args.output)
        approvals = local_path(args.approvals)
        expected = yaml.safe_load(golden.read_text(encoding="utf-8"))
        extracted = json.loads(actual.read_text(encoding="utf-8"))
        result = score(expected, extracted, approvals=approvals)
        if not result["golden_approved"] and not args.allow_draft:
            print("score_sieving: FAIL - golden set lacks a recorded human approval", file=sys.stderr)
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
        print(f"score_sieving: PASS - found={result['found']}; missed={result['missed']}; "
              f"spurious={result['spurious']}; promotion_ready={result['promotion_ready']}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError,
            yaml.YAMLError) as exc:
        print(f"score_sieving: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
