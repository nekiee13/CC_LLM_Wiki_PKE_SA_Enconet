#!/usr/bin/env python3
"""Confirm one owner-approved conditional applicability ruling before G3."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from evaluation_engine import confirm_applicability
from project_paths import configure_standard_streams


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--criterion-id", required=True)
    parser.add_argument("--confirmation-ref", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        result = confirm_applicability(
            args.db, run_id=args.run_id, criterion_id=args.criterion_id,
            confirmation_ref=args.confirmation_ref, apply=args.apply,
        )
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"confirm_applicability: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
