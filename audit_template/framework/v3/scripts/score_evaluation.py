#!/usr/bin/env python3
"""Read-only score of a complete, validated, locally approved evaluation run."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

import db_util
from evaluation_engine import _approved_model, _connect, metrics
from project_paths import configure_standard_streams
from validate_evaluation import validate


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        errors = validate(args.db, args.run_id)
        if errors:
            raise ValueError(f"evaluation incomplete or invalid: {errors[0]}")
        with closing(_connect(args.db, write=False)) as conn:
            rows = [dict(row) for row in conn.execute(
                "SELECT rating FROM criterion_evaluations WHERE evaluation_run_id=? ORDER BY criterion_id", (args.run_id,))]
        print(json.dumps(metrics(rows, scoring_model=_approved_model(args.run_id)), sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"score_evaluation: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
