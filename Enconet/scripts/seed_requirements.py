#!/usr/bin/env python3
"""Preview or seed requirement rows from active local RULE crumbs.

The source of a requirement is a RULE crumb.  The command is deterministic:
for each criterion it keeps the first active crumb for each distinct statement
in the explicitly chosen RULE run. Other regulatory runs are never swept in.
Preview is the default; apply is idempotent and never deletes existing rows.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path

ROOT = Path(__file__).resolve().parents[1]


def _plan(conn: sqlite3.Connection, run_id: str) -> list[dict[str, str | int | None]]:
    criteria = [row[0] for row in conn.execute(
        "SELECT criterion_id FROM criteria ORDER BY criterion_id"
    )]
    if not criteria:
        raise ValueError("criteria table is empty")
    rows = conn.execute(
        "SELECT c.item_id, c.criterion_id, c.statement "
        "FROM crumbs c JOIN sieve_runs r ON r.run_id=c.sieve_run_id "
        "WHERE c.document_side='RULE' AND r.is_active=1 AND r.run_id=? "
        "ORDER BY c.criterion_id, c.item_id", (run_id,)
    ).fetchall()
    by_criterion: dict[str, list[sqlite3.Row]] = {criterion: [] for criterion in criteria}
    for row in rows:
        if row["criterion_id"] in by_criterion:
            by_criterion[row["criterion_id"]].append(row)
    planned: list[dict[str, str | int | None]] = []
    for criterion in criteria:
        seen: set[str] = set()
        ordinal = 0
        for row in by_criterion[criterion]:
            text = (row["statement"] or "").strip()
            if not text or text in seen:
                continue
            seen.add(text)
            ordinal += 1
            if ordinal > 99:
                raise ValueError(f"too many distinct requirements for {criterion}")
            planned.append({
                "requirement_id": f"REQ-{criterion}-{ordinal:02d}",
                "criterion_id": criterion,
                "requirement_text": text,
                "source_item_id": row["item_id"],
                "parent_requirement_id": None,
                "is_subrequirement": 0,
            })
        if ordinal == 0:
            raise ValueError(f"no active RULE crumb for {criterion}")
    return planned


def seed(db: Path = db_util.DEFAULT_DB, *, apply: bool = False,
         run_id: str | None = None) -> dict[str, int | str]:
    database = local_path(db)
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("an explicit RULE run is required")
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    if apply:
        with closing(db_util.connect(database)) as conn, conn:
            planned = _plan(conn, run_id)
            existing = {
                row["requirement_id"]: dict(row)
                for row in conn.execute("SELECT * FROM requirements")
            }
            inserted = 0
            for row in planned:
                current = existing.get(row["requirement_id"])
                if current is not None:
                    if any(current[key] != row[key] for key in row):
                        raise ValueError(
                            f"existing requirement conflicts: {row['requirement_id']}"
                        )
                    continue
                db_util.insert(conn, "requirements", row)
                inserted += 1
    else:
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            planned = _plan(conn, run_id)
            inserted = 0
            existing = {row[0] for row in conn.execute(
                "SELECT requirement_id FROM requirements"
            )}
            inserted = sum(row["requirement_id"] not in existing for row in planned)
    return {
        "mode": "apply" if apply else "preview",
        "criteria": len({row["criterion_id"] for row in planned}),
        "planned": len(planned),
        "inserted": inserted,
    }


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True, help="Approved active RULE run only")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(seed(args.db, apply=args.apply, run_id=args.run_id), sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"seed_requirements: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
