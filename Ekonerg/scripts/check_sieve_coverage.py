#!/usr/bin/env python3
"""Report whether every registered company document has recall coverage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path


def coverage(db: Path, document_side: str = "DOCUMENT") -> dict[str, object]:
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    with db_util.connect(database) as conn:
        rows = conn.execute(
            """
            SELECT d.doc_id, d.filename,
                   CASE WHEN EXISTS (
                       SELECT 1 FROM sieve_runs s
                       WHERE s.doc_id=d.doc_id AND s.is_active=1
                   ) THEN 1 ELSE 0 END AS has_active_run,
                   COALESCE((
                       SELECT count(*) FROM crumbs c JOIN sieve_runs s ON s.run_id=c.sieve_run_id
                       WHERE c.doc_id=d.doc_id AND s.is_active=1
                   ), 0) AS active_crumbs
            FROM documents d
            WHERE d.document_side=?
            ORDER BY d.doc_id
            """, (document_side,),
        ).fetchall()
    documents = [
        {"doc_id": row["doc_id"], "filename": row["filename"],
         "has_active_run": bool(row["has_active_run"]),
         "active_crumbs": int(row["active_crumbs"])}
        for row in rows
    ]
    missing = [row for row in documents if not row["has_active_run"]]
    zero = [row for row in documents if row["has_active_run"] and row["active_crumbs"] == 0]
    return {
        "document_side": document_side,
        "document_count": len(documents),
        "active_run_count": sum(row["has_active_run"] for row in documents),
        "active_crumb_count": sum(row["active_crumbs"] for row in documents),
        "missing_active_runs": missing,
        "zero_crumb_active_runs": zero,
        "documents": documents,
    }


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--document-side", default="DOCUMENT")
    args = parser.parse_args()
    try:
        result = coverage(args.db, args.document_side)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        if result["missing_active_runs"] or result["zero_crumb_active_runs"]:
            print("check_sieve_coverage: FAIL - incomplete recall coverage", file=sys.stderr)
            return 1
        print("check_sieve_coverage: PASS - every document has active crumbs")
        return 0
    except (OSError, ValueError, sqlite3.Error) as exc:
        print(f"check_sieve_coverage: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
