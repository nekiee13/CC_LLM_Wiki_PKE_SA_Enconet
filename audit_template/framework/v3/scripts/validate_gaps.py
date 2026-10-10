#!/usr/bin/env python3
"""Read-only structural check of local gaps and missing-evidence actions."""
from __future__ import annotations

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path


def validate(db: Path) -> tuple[list[str], int]:
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    errors: list[str] = []
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only=ON")
        gaps = conn.execute(
            "SELECT g.*,e.criterion_id,e.evaluation_run_id FROM gaps g "
            "JOIN criterion_evaluations e ON e.evaluation_id=g.evaluation_id ORDER BY g.gap_id"
        ).fetchall()
        for gap in gaps:
            gap_id = gap["gap_id"]
            if db_util.id_patterns()["gap_id"].fullmatch(gap_id) is None:
                errors.append(f"invalid gap ID: {gap_id}")
            if (gap["evidence_item_id"] is None) == (gap["missing_evidence_ref"] is None):
                errors.append(f"gap evidence pointer invalid: {gap_id}")
            if gap["evidence_item_id"] is not None:
                crumb = conn.execute(
                    "SELECT c.criterion_id,r.is_active FROM crumbs c "
                    "JOIN sieve_runs r ON r.run_id=c.sieve_run_id WHERE c.item_id=?",
                    (gap["evidence_item_id"],),
                ).fetchone()
                if crumb is None or crumb["criterion_id"] != gap["criterion_id"] or not crumb["is_active"]:
                    errors.append(f"gap evidence crumb is missing, inactive, or wrong criterion: {gap_id}")
            if gap["status"] == "missing-evidence":
                if not gap["missing_evidence_ref"]:
                    errors.append(f"missing-evidence gap lacks missing reference: {gap_id}")
                actions = conn.execute(
                    "SELECT action_type,evaluation_run_id FROM auditor_actions WHERE gap_id=?",
                    (gap_id,),
                ).fetchall()
                if not actions:
                    errors.append(f"missing-evidence gap without action: {gap_id}")
                elif any(action["action_type"] not in {"verification", "document_request"} or
                         action["evaluation_run_id"] != gap["evaluation_run_id"] for action in actions):
                    errors.append(f"invalid missing-evidence action type or run: {gap_id}")
        for row in conn.execute("PRAGMA foreign_key_check"):
            errors.append(f"foreign key violation: {tuple(row)}")
    return errors, len(gaps)


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    args = parser.parse_args()
    try:
        errors, count = validate(args.db)
    except (OSError, ValueError, KeyError, sqlite3.Error) as exc:
        print(f"validate_gaps: FAIL - {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"validate_gaps: FAIL - {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"validate_gaps: PASS - {count} gap(s); structural only, not audit approval")
    return 0


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
