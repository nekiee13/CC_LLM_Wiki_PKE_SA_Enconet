#!/usr/bin/env python3
"""Check local Appendix B requirement coverage and RULE-crumb traceability."""
from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

import yaml

import db_util
from project_paths import local_path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ROOT / "schemas" / "app_b_taxonomy.yml"
RUNS = ROOT / "manifests" / "validation_runs.csv"
RUN_HEADER = ["run_utc", "validator", "phase", "result", "exit_code", "details"]


def validate(db: Path) -> list[str]:
    """Read only: missing data is a failure, never an empty-audit PASS."""
    database = local_path(db)
    if not database.is_file():
        return [f"local database is missing: {database}"]
    taxonomy = yaml.safe_load(local_path(TAXONOMY).read_text(encoding="utf-8"))
    if not isinstance(taxonomy, dict) or taxonomy.get("taxonomy_id") != "APP_B":
        return ["local Appendix B taxonomy is missing or mismatched"]
    criteria = taxonomy.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != 18:
        return ["local Appendix B taxonomy must define 18 criteria"]
    expected = {item.get("criterion_id") for item in criteria if isinstance(item, dict)}
    if len(expected) != 18 or not all(isinstance(value, str) and value for value in expected):
        return ["local Appendix B taxonomy has invalid or duplicate criterion IDs"]
    pattern = db_util.id_patterns()["requirement_id"]
    errors: list[str] = []
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        actual = [row[0] for row in conn.execute("SELECT criterion_id FROM criteria")]
        if len(actual) != 18 or set(actual) != expected:
            errors.append("database criteria do not match all 18 local Appendix B criteria")
        rows = conn.execute(
            "SELECT r.*, c.document_side FROM requirements r "
            "LEFT JOIN crumbs c ON c.item_id=r.source_item_id"
        ).fetchall()
        covered = {row["criterion_id"] for row in rows}
        for criterion_id in sorted(expected - covered):
            errors.append(f"criterion without requirement: {criterion_id}")
        for row in rows:
            identifier = row["requirement_id"]
            if pattern.fullmatch(identifier) is None:
                errors.append(f"invalid requirement ID: {identifier}")
            if row["criterion_id"] not in expected:
                errors.append(f"requirement has unknown criterion: {identifier}")
            if row["document_side"] != "RULE":
                errors.append(f"requirement without RULE crumb: {identifier}")
            if bool(row["is_subrequirement"]) != bool(row["parent_requirement_id"]):
                errors.append(f"invalid hierarchy: {identifier}")
    return errors


def append_result(result: str, code: int, details: str, path: Path = RUNS) -> None:
    """Append only to an existing, correctly shaped local validation log."""
    with local_path(path).open("r+", newline="", encoding="utf-8") as handle:
        header = next(csv.reader(handle), None)
        if header != RUN_HEADER:
            raise ValueError("validation manifest header is missing or invalid")
        handle.seek(0, 2)
        csv.writer(handle).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_requirements.py", "unknown", result, code, details,
        ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(args.db)
    except (OSError, ValueError, KeyError, sqlite3.Error, yaml.YAMLError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"validate_requirements: FAIL - {error}", file=sys.stderr)
    code = int(bool(errors))
    if not args.no_record:
        try:
            append_result("FAIL" if code else "PASS", code,
                          f"{len(errors)} error(s); first: {errors[0][:120]}" if errors
                          else "18 criteria covered; every requirement traces to a RULE crumb")
        except (OSError, ValueError) as exc:
            print(f"validate_requirements: FAIL - record could not be written: {exc}",
                  file=sys.stderr)
            return 1
    if not code:
        print("validate_requirements: PASS - 18 criteria covered")
    return code


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
