#!/usr/bin/env python3
"""Prepare a v3 prompt calibration input from the corrected DOC-0016 pilot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


PROMPT_VERSION = "appb_document_v3_context_anchors"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    payload["prompt_version"] = PROMPT_VERSION
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"prepared {args.output} for {PROMPT_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
