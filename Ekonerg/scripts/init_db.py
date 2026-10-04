#!/usr/bin/env python3
"""Create a fresh, empty, project-local audit database without reset support."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

from project_paths import configure_standard_streams, local_path
import db_util


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "db" / "nqa_audit.sqlite"
SCHEMA = ROOT / "db" / "schema.sql"
SCHEMA_VERSION = 1
REQUIRED_TABLES = {
    "criteria", "documents", "document_chunks", "crumbs", "crumb_sources",
    "crumb_quotes", "crumb_chunk_links", "requirements", "criterion_applicability",
    "criterion_evaluations", "gaps", "findings", "auditor_actions", "sieve_runs",
    "evaluation_runs", "dashboard_runs", "validation_runs", "sieve_run_authorities",
    "crumb_authority_refs", "evaluation_evidence", "sieve_generation_events",
    "approved_sources", "crumb_context",
}


def _check_existing(db_path: Path) -> str:
    """Inspect an existing database; never reset or seed it."""
    if not db_path.is_file() or db_path.stat().st_size == 0:
        raise RuntimeError(f"refusing incomplete existing database: {db_path}")
    with closing(sqlite3.connect(db_path)) as conn:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
    legacy_required = REQUIRED_TABLES - {"crumb_context"}
    if (version != SCHEMA_VERSION or not legacy_required <= tables or
            integrity != "ok" or foreign_errors):
        missing = sorted(legacy_required - tables)
        raise RuntimeError(
            f"refusing incomplete or incompatible existing database: {db_path}; "
            f"schema version {version}; missing tables {missing}; integrity {integrity}; "
            f"foreign key errors {len(foreign_errors)}"
        )
    with closing(sqlite3.connect(db_path)) as conn:
        db_util.ensure_crumb_context_schema(conn)
        conn.commit()
    if "crumb_context" not in tables:
        tables.add("crumb_context")
    if not REQUIRED_TABLES <= tables:
        raise RuntimeError(f"database migration did not create required tables: {db_path}")
    return "already initialized; existing data preserved"


def initialize(db_path: Path | str = DEFAULT_DB) -> str:
    """Create one empty local database; existing files are never overwritten."""
    db_path = local_path(db_path)
    if db_path.exists():
        return _check_existing(db_path)
    schema_sql = local_path(SCHEMA).read_text(encoding="utf-8")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path = local_path(db_path)
    # Exclusive create prevents a second initializer from silently replacing a DB.
    with db_path.open("xb"):
        pass
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
            raise RuntimeError("SQLite foreign-key enforcement could not be enabled")
        try:
            conn.executescript("BEGIN IMMEDIATE;\n" + schema_sql + "\nCOMMIT;")
        except sqlite3.Error:
            conn.rollback()
            # Keep the incomplete file for diagnosis. A retry refuses to overwrite it.
            raise
    return "initialized empty database; no source or criterion approved"


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = parser.parse_args()
    try:
        result = initialize(args.db)
        print(f"init_db: PASS - {result}: {local_path(args.db)}")
        return 0
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
        print(f"init_db: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
