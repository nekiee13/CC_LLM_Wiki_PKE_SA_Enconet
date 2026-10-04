#!/usr/bin/env python3
"""Create the pending DOC-0016 v3 golden fixture from a candidate input."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


PROMPT_VERSION = "appb_document_v3_context_anchors"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    candidate = json.loads(args.input.read_text(encoding="utf-8"))
    expected = []
    for item in candidate["items"]:
        expected.append({
            "item_id": item["item_id"],
            "criterion_id": item["criterion_id"],
            "criterion_name": item["criterion_name"],
            "statement": item["statement"],
            "source": item["sources"][0],
            "quotes": [quote["quote_original"] for quote in item["evidence_quotes"]],
            "evidence_type": item.get("evidence_type"),
            "context": item.get("context", {}),
        })
    fixture = {
        "schema_version": "1.0",
        "fixture_version": "ekonerg-document-doc0016-v3-draft-2026-10-04",
        "status": "pending_human_approval",
        "approval_ref": None,
        "document": {
            "doc_id": candidate["document"]["doc_id"],
            "filename": candidate["document"]["name"],
            "side": candidate["document"]["document_side"],
            "purpose": "Fresh calibration for the versioned source-context-anchor prompt.",
        },
        "prompt_version": PROMPT_VERSION,
        "expected_crumbs": expected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(fixture, sort_keys=False, allow_unicode=True),
                           encoding="utf-8", newline="\n")
    print(f"created pending golden draft: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
