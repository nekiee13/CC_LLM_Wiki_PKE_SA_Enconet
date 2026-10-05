#!/usr/bin/env python3
"""Create an owner-approved golden snapshot from an exported sieve run."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

from project_paths import local_path


def create(actual: Path, output: Path, *, fixture_version: str,
           approval_ref: str) -> None:
    payload = yaml.safe_load(local_path(actual).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError("exported run must contain an items list")
    document = payload.get("document")
    if not isinstance(document, dict) or not document.get("doc_id"):
        raise ValueError("exported run document is missing")
    expected = []
    for item in payload["items"]:
        sources = item.get("sources") or []
        quotes = item.get("evidence_quotes") or []
        if not sources or not quotes:
            raise ValueError("every item needs a source and quote")
        expected.append({
            "item_id": item["item_id"],
            "criterion_id": item["criterion_id"],
            "criterion_name": item["criterion_name"],
            "statement": item["statement"],
            "source": {"source_locator": sources[0]["source_locator"]},
            "quotes": [quote["quote_original"] for quote in quotes],
        })
    fixture = {
        "schema_version": "1.0",
        "fixture_version": fixture_version,
        "status": "approved",
        "approval_ref": approval_ref,
        "document": {
            "doc_id": document["doc_id"],
            "filename": document["name"],
            "side": document["document_side"],
            "purpose": "Owner-approved repair snapshot for controlled generation promotion.",
        },
        "expected_crumbs": expected,
    }
    destination = local_path(output)
    if destination.exists():
        raise ValueError(f"refusing to overwrite existing output: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(yaml.safe_dump(fixture, allow_unicode=True, sort_keys=False),
                           encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("actual", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fixture-version", required=True)
    parser.add_argument("--approval-ref", required=True)
    args = parser.parse_args()
    create(args.actual, args.output, fixture_version=args.fixture_version,
           approval_ref=args.approval_ref)
    print(f"create_run_golden: PASS - {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
