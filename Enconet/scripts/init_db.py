#!/usr/bin/env python3
"""Initialize the EPIC2 SQLite data backbone reproducibly."""
from __future__ import annotations

import argparse
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import yaml

ENCONET = Path(__file__).resolve().parents[1]
DEFAULT_DB = ENCONET / "db" / "nqa_audit.sqlite"
SCHEMA = ENCONET / "db" / "schema.sql"
TAXONOMY = ENCONET / "schemas" / "app_b_taxonomy.yml"
REQUIRED_TABLES = {
    "criteria", "documents", "document_chunks", "crumbs", "crumb_sources",
    "crumb_quotes", "crumb_chunk_links", "requirements", "criterion_applicability",
    "criterion_evaluations", "gaps", "findings", "auditor_actions", "sieve_runs",
    "evaluation_runs", "dashboard_runs", "validation_runs",
}


def initialize(db_path: Path, *, reset: bool = False) -> str:
    db_path = db_path.resolve()
    if db_path.exists() and reset:
        db_path.unlink()
    elif db_path.exists() and db_path.stat().st_size > 0:
        with closing(sqlite3.connect(db_path)) as probe:
            tables = {row[0] for row in probe.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
        if REQUIRED_TABLES <= tables:
            return "already initialized; existing data preserved"
        raise RuntimeError(
            f"refusing to clobber non-empty incomplete/non-Enconet DB: {db_path}; "
            f"missing tables: {sorted(REQUIRED_TABLES - tables)}"
        )

    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = SCHEMA.read_text(encoding="utf-8")
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))["criteria"]
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
            raise RuntimeError("SQLite foreign-key enforcement could not be enabled")
        conn.executescript(schema_sql)
        conn.executemany(
            "INSERT OR IGNORE INTO criteria(criterion_id, criterion_name, description) "
            "VALUES (:criterion_id, :criterion_name, :description)",
            taxonomy,
        )
        conn.commit()
    return "initialized"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--reset", action="store_true",
                        help="delete and recreate the target DB (destructive)")
    args = parser.parse_args()
    try:
        result = initialize(args.db, reset=args.reset)
        print(f"init_db: PASS - {result}: {args.db.resolve()}")
        return 0
    except (OSError, RuntimeError, sqlite3.Error, yaml.YAMLError) as exc:
        print(f"init_db: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
