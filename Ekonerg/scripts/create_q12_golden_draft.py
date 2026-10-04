#!/usr/bin/env python3
"""Create a pending golden-calibration draft from the reviewed Q12 candidate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from project_paths import local_path


def create(input_path: Path, output_path: Path) -> None:
    candidate = json.loads(local_path(input_path).read_text(encoding="utf-8"))
    expected = []
    for item in candidate["items"]:
        expected.append({
            "item_id": item["item_id"],
            "criterion_id": item["criterion_id"],
            "criterion_name": item["criterion_name"],
            "statement": item["statement"],
            "source": item["sources"][0],
            "quotes": [quote["quote_original"] for quote in item["evidence_quotes"]],
        })
    fixture = {
        "schema_version": "1.0",
        "fixture_version": "ekonerg-document-doc0021-q12-v2-draft-2026-10-04",
        "status": "pending_human_approval",
        "approval_ref": None,
        "document": {
            "doc_id": candidate["document"]["doc_id"],
            "filename": candidate["document"]["name"],
            "side": candidate["document"]["document_side"],
            "purpose": "Draft calibration for the corrected Q12 exact-source generation.",
        },
        "prompt_version": candidate["prompt_version"],
        "expected_crumbs": expected,
    }
    target = local_path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(fixture, sort_keys=False, allow_unicode=True),
                      encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path,
                        default=Path("sieving/runs/q12_doc0021_corrected.json"))
    parser.add_argument("--output", type=Path,
                        default=Path("benchmarks/sieving_golden/manifest_document_doc0021_q12_v2.yml"))
    args = parser.parse_args()
    create(args.input, args.output)
    print(f"created pending golden draft: {local_path(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
