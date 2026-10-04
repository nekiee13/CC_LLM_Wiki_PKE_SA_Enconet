#!/usr/bin/env python3
"""Run the three read-only PIVOT-3 context-runtime checks."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
from pathlib import Path

import build_matrix
import db_util
import import_crumbs
import init_db
from project_paths import local_path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = Path("db/nqa_audit.sqlite")
DEFAULT_COPY = Path(".runtime-check/context-db-copy.sqlite")
DEFAULT_OUTPUT = Path("docs/reviews/PIVOT_3_CONTEXT_RUNTIME_DRY_RUN.json")
MATRIX_RUN = "RUN-20261003-32"


def _snapshot(path: Path) -> dict:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    schema = [dict(row) for row in conn.execute(
        "SELECT type, name, sql FROM sqlite_master "
        "WHERE type IN ('table','index') ORDER BY type,name"
    )]
    counts = {
        row["name"]: int(conn.execute(f"SELECT count(*) FROM {row['name']}").fetchone()[0])
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    }
    conn.close()
    digest = hashlib.sha256(json.dumps(
        {"schema": schema, "counts": counts}, sort_keys=True,
        ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")).hexdigest()
    return {"schema_hash": digest, "table_count": len(counts), "row_counts": counts}


def _matrix_snapshot(db: Path) -> dict:
    rows = build_matrix.build(db, MATRIX_RUN)
    payload = build_matrix.render_json(rows)
    type_counts: dict[str, int] = {}
    unanchored = 0
    for row in rows:
        for name, count in row["evidence_type_counts"].items():
            type_counts[name] = type_counts.get(name, 0) + count
        unanchored += max(0, row["document_evidence_count"] - row["anchored_document_evidence_count"])
    return {
        "run_id": MATRIX_RUN,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "criteria": len(rows),
        "evidence_type_counts": type_counts,
        "untyped_count": type_counts.get("untyped", 0),
        "unanchored_document_count": unanchored,
    }


def verify(*, db: Path = DEFAULT_DB, copy_db: Path = DEFAULT_COPY,
           output: Path = DEFAULT_OUTPUT) -> dict:
    database = local_path(db)
    copy_path = local_path(copy_db)
    output_path = local_path(output)
    copy_path.parent.mkdir(parents=True, exist_ok=True)
    if copy_path.exists():
        copy_path.unlink()
    shutil.copy2(database, copy_path)
    before_copy = _snapshot(copy_path)
    init_db.initialize(copy_path)
    after_first = _snapshot(copy_path)
    init_db.initialize(copy_path)
    after_second = _snapshot(copy_path)
    migration = {
        "before": before_copy,
        "after_first": after_first,
        "after_second": after_second,
        "idempotent": after_first == after_second,
    }

    try:
        import_crumbs._validate_context_requirements([{"evidence_type": "objective_record"}])
    except ValueError as exc:
        importer_refusal = {"passed": True, "error": str(exc)}
    else:
        importer_refusal = {"passed": False, "error": None}

    matrix_before = _matrix_snapshot(database)
    matrix_after = _matrix_snapshot(database)
    matrix = {
        "before": matrix_before,
        "after": matrix_after,
        "hash_unchanged": matrix_before["sha256"] == matrix_after["sha256"],
        "evaluation_runs_checked": [MATRIX_RUN],
        "active_sieve_run_count": sqlite3.connect(database).execute(
            "SELECT count(*) FROM sieve_runs WHERE is_active=1"
        ).fetchone()[0],
    }
    result = {
        "schema_version": "1.0",
        "database": str(database),
        "migration_idempotence": migration,
        "importer_anchor_refusal": importer_refusal,
        "matrix_read_only": matrix,
        "all_checks_pass": bool(
            migration["idempotent"] and importer_refusal["passed"] and matrix["hash_unchanged"]
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--copy-db", type=Path, default=DEFAULT_COPY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = verify(db=args.db, copy_db=args.copy_db, output=args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
