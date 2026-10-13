#!/usr/bin/env python3
"""Preview or write the human-approved local applicability matrix."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

from evaluation_engine import write_rulings
import db_util
from project_paths import configure_standard_streams, local_path


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--supplier", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        rulings = json.loads(local_path(args.matrix).read_text(encoding="utf-8"))
        result = write_rulings(args.db, run_id=args.run_id, supplier=args.supplier,
                               language=args.language, rulings=rulings, apply=args.apply)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"rule_applicability: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
