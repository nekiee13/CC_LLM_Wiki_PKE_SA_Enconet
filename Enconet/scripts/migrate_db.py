#!/usr/bin/env python3
"""Safely migrate an existing Enconet DB to the EPIC5/EPIC6 additive schema."""
from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import db_util

SCHEMA = Path(__file__).resolve().parents[1] / "db" / "schema.sql"


def plan(db_path: Path) -> list[str]:
    path = db_path.resolve()
    if not path.is_file():
        raise ValueError(f"database does not exist: {path}")
    with sqlite3.connect(path) as conn:
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("database integrity_check failed")
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {"documents", "sieve_runs", "crumbs", "crumb_quotes", "crumb_chunk_links"} <= tables:
            raise ValueError("target is not a recognized Enconet database")
        actions = []
        for table in ("sieve_run_authorities", "crumb_authority_refs"):
            if table not in tables:
                actions.append(f"create {table}")
        columns = {r[1] for r in conn.execute("PRAGMA table_info(crumb_chunk_links)")}
        if "quote_id" not in columns:
            if conn.execute("SELECT count(*) FROM crumb_chunk_links").fetchone()[0]:
                raise ValueError("legacy crumb_chunk_links is non-empty; automatic migration refused")
            actions.append("recreate empty crumb_chunk_links with quote_id")
        requirement_columns = {r[1] for r in conn.execute("PRAGMA table_info(requirements)")}
        if "parent_requirement_id" not in requirement_columns:
            actions.append("add requirement hierarchy columns")
        evaluation_columns = {r[1] for r in conn.execute("PRAGMA table_info(criterion_evaluations)")}
        if "coverage" not in evaluation_columns:
            protected = ("evaluation_runs","criterion_applicability","criterion_evaluations","gaps","findings","auditor_actions","dashboard_runs")
            if any(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in protected):
                raise ValueError("EPIC8 evaluation tables contain data; automatic migration refused")
            actions.append("recreate empty EPIC8 evaluation tables")
        gap_columns = {r[1] for r in conn.execute("PRAGMA table_info(gaps)")}
        if "evidence_item_id" not in gap_columns:
            if any(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in ("gaps","findings","auditor_actions")):
                raise ValueError("EPIC9 gap/action tables contain data; automatic migration refused")
            actions.append("recreate empty EPIC9 gap/action tables")
        return actions


def migrate(db_path: Path, *, apply: bool, backup_dir: Path | None = None) -> tuple[list[str], Path | None]:
    path = db_path.resolve()
    actions = plan(path)
    if not apply or not actions:
        return actions, None
    target_dir = (backup_dir or path.parent / "backups").resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target_dir / f"{path.stem}-{stamp}.sqlite.bak"
    if backup.exists():
        raise ValueError(f"backup already exists: {backup}")
    with sqlite3.connect(path) as source, sqlite3.connect(backup) as destination:
        source.backup(destination)
    schema = SCHEMA.read_text(encoding="utf-8")
    try:
        with sqlite3.connect(path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            if "recreate empty crumb_chunk_links with quote_id" in actions:
                conn.execute("DROP TABLE crumb_chunk_links")
            if "add requirement hierarchy columns" in actions:
                conn.execute("ALTER TABLE requirements ADD COLUMN parent_requirement_id TEXT REFERENCES requirements(requirement_id)")
                conn.execute("ALTER TABLE requirements ADD COLUMN is_subrequirement INTEGER NOT NULL DEFAULT 0 CHECK (is_subrequirement IN (0,1))")
            if "recreate empty EPIC8 evaluation tables" in actions:
                for table in ("dashboard_runs","auditor_actions","findings","gaps","evaluation_evidence","criterion_evaluations","criterion_applicability","evaluation_runs"):
                    conn.execute(f"DROP TABLE IF EXISTS {table}")
            elif "recreate empty EPIC9 gap/action tables" in actions:
                for table in ("auditor_actions","findings","gaps"):
                    conn.execute(f"DROP TABLE IF EXISTS {table}")
            # sqlite3.executescript commits implicitly. Recovery is therefore the
            # pre-write SQLite backup, not an illusory surrounding transaction.
            conn.executescript(schema)
            if conn.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("foreign_key_check failed after migration")
    except Exception:
        # Restore only after the connection closes so Windows cannot retain a lock.
        shutil.copy2(backup, path)
        raise
    return actions, backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--apply", action="store_true", help="apply after backup; default is dry-run")
    parser.add_argument("--backup-dir", type=Path)
    args = parser.parse_args()
    try:
        actions, backup = migrate(args.db, apply=args.apply, backup_dir=args.backup_dir)
        mode = "APPLIED" if args.apply else "DRY-RUN"
        print(f"migrate_db: {mode} - actions={actions or ['none']}; backup={backup or 'not-created'}")
        return 0
    except (OSError, sqlite3.Error, ValueError) as exc:
        print(f"migrate_db: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
