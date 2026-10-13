#!/usr/bin/env python3
"""Preview or write one human judgment under the local G2 and G3 gates."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

import db_util
from evaluation_engine import write_evaluation
from project_paths import configure_standard_streams, local_path


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        record = json.loads(local_path(args.record).read_text(encoding="utf-8"))
        result = write_evaluation(args.db, run_id=args.run_id, record=record,
                                  evidence_ids=args.evidence, apply=args.apply)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"write_evaluation: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
