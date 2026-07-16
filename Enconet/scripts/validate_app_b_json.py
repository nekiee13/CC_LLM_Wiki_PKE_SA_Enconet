#!/usr/bin/env python3
"""Validate EPIC5 crumb JSON through the vendored sieving library."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import sieving_lib  # noqa: F401 - installs the documented vendored source root
from json_extractor.crumb_validation import (  # noqa: F401
    ValidationResult,
    check_authority_references,
    validate_file,
    validate_payload,
)

# Transitional compatibility for callers written before EPIC15.
_check_refs = check_authority_references


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    _, result = validate_file(args.json_file, strict=args.strict)
    for warning in result.warnings:
        print(f"WARNING {warning}")
    for error in result.errors:
        print(f"FAIL {error}", file=sys.stderr)
    print(f"validate_app_b_json: {'PASS' if result.passed else 'FAIL'}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
