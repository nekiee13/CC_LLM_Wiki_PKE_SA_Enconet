#!/usr/bin/env python3
"""Seed the company-neutral 10 CFR 50 Appendix B criteria once."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import yaml

import db_util
from project_paths import configure_standard_streams, local_path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "db" / "nqa_audit.sqlite"
TAXONOMY = ROOT / "schemas" / "app_b_taxonomy.yml"
EXPECTED_TAXONOMY_ID = "APP_B"
EXPECTED_COUNT = 18


def load_criteria(taxonomy_path: Path | str = TAXONOMY) -> list[tuple[str, str, str]]:
    """Read and validate the local, company-neutral criterion taxonomy."""
    source = local_path(taxonomy_path)
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("taxonomy_id") != EXPECTED_TAXONOMY_ID:
        raise ValueError("local Appendix B taxonomy is missing or mismatched")
    rows = data.get("criteria")
    if not isinstance(rows, list) or len(rows) != EXPECTED_COUNT:
        raise ValueError("local Appendix B taxonomy must define exactly 18 criteria")
    result: list[tuple[str, str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("taxonomy criteria must be mapping rows")
        values = tuple(row.get(key) for key in
                       ("criterion_id", "criterion_name", "description"))
        if not all(isinstance(value, str) and value.strip() for value in values):
            raise ValueError("taxonomy criteria require non-empty text fields")
        result.append(values)
    if len({row[0] for row in result}) != EXPECTED_COUNT:
        raise ValueError("taxonomy criterion IDs must be unique")
    return result


def seed(db_path: Path | str = DEFAULT_DB,
         taxonomy_path: Path | str = TAXONOMY) -> str:
    """Insert criteria into an empty table, or preserve an exact existing seed."""
    expected = load_criteria(taxonomy_path)
    database = local_path(db_path)
    if not database.is_file():
        raise FileNotFoundError(f"database is missing: {database}; run init_db.py first")
    with closing(db_util.connect(database)) as conn:
        actual = [tuple(row) for row in conn.execute(
            "SELECT criterion_id, criterion_name, description "
            "FROM criteria ORDER BY rowid"
        )]
        if actual:
            if actual != expected:
                raise ValueError("existing criteria seed mismatch; refusing to overwrite")
            return "criteria already seeded; existing rows preserved"
        try:
            conn.executemany(
                "INSERT INTO criteria(criterion_id, criterion_name, description) "
                "VALUES (?,?,?)", expected,
            )
            conn.commit()
        except sqlite3.Error:
            conn.rollback()
            raise
    return f"seeded {len(expected)} Appendix B criteria"


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--taxonomy", type=Path, default=TAXONOMY)
    args = parser.parse_args()
    try:
        print(f"seed_criteria: PASS - {seed(args.db, args.taxonomy)}")
        return 0
    except (OSError, ValueError, sqlite3.Error, yaml.YAMLError) as exc:
        print(f"seed_criteria: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
