#!/usr/bin/env python3
"""Preview or apply downstream evidence links when a sieve generation changes.

The default operation is a read-only dry run. It maps old and new crumbs by
criterion and normalized statement, then reports every downstream link that
would change. Applying requires an explicit decision reference and is refused
if the mapping is incomplete or ambiguous.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _crumbs(conn: sqlite3.Connection, run_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT item_id,criterion_id,statement FROM crumbs "
        "WHERE sieve_run_id=? ORDER BY item_id", (run_id,)
    ).fetchall()


def _mapping(conn: sqlite3.Connection, old_run: str, new_run: str) -> dict[str, object]:
    old = _crumbs(conn, old_run)
    new = _crumbs(conn, new_run)
    by_key: dict[tuple[str, str], list[str]] = {}
    for row in new:
        by_key.setdefault((row["criterion_id"], _norm(row["statement"])), []).append(row["item_id"])
    mappings: list[dict[str, str]] = []
    ambiguous: list[str] = []
    missing: list[str] = []
    for row in old:
        key = (row["criterion_id"], _norm(row["statement"]))
        candidates = by_key.get(key, [])
        if len(candidates) != 1:
            (ambiguous if candidates else missing).append(row["item_id"])
            continue
        mappings.append({"old_item_id": row["item_id"], "new_item_id": candidates[0],
                         "criterion_id": row["criterion_id"]})
    downstream: list[dict[str, str]] = []
    old_ids = {row["old_item_id"] for row in mappings}
    for row in conn.execute(
        "SELECT evaluation_id,item_id FROM evaluation_evidence "
        "WHERE item_id IN ({}) ORDER BY evaluation_id,item_id".format(
            ",".join("?" for _ in old_ids)), tuple(old_ids)
    ) if old_ids else []:
        replacement = next(item["new_item_id"] for item in mappings if item["old_item_id"] == row["item_id"])
        downstream.append({"evaluation_id": row["evaluation_id"],
                           "old_item_id": row["item_id"], "new_item_id": replacement})
    collisions = []
    for item in downstream:
        exists = conn.execute(
            "SELECT 1 FROM evaluation_evidence WHERE evaluation_id=? AND item_id=?",
            (item["evaluation_id"], item["new_item_id"])).fetchone()
        if exists:
            collisions.append(item)
    return {"schema_version": "1.0", "old_run_id": old_run, "new_run_id": new_run,
            "old_crumbs": len(old), "new_crumbs": len(new),
            "mapping_count": len(mappings), "mappings": mappings,
            "downstream_link_count": len(downstream), "downstream_links": downstream,
            "missing": missing, "ambiguous": ambiguous, "collisions": collisions,
            "ready": bool(mappings and not missing and not ambiguous and not collisions)}


def reconcile(db: Path, old_run: str, new_run: str, *, apply: bool,
              decision_ref: str | None) -> dict[str, object]:
    database = local_path(db)
    with closing(db_util.connect(database)) as conn:
        old = db_util.lookup(conn, "sieve_runs", "run_id", old_run)
        new = db_util.lookup(conn, "sieve_runs", "run_id", new_run)
        if old is None or new is None or old["doc_id"] != new["doc_id"]:
            raise ValueError("runs must exist and belong to the same document")
        if old["is_active"] != 1 or new["status"] != "candidate" or new["is_active"]:
            raise ValueError("reconciliation requires one active old run and one inactive candidate")
        data = _mapping(conn, old_run, new_run)
        if apply:
            if not decision_ref or not str(decision_ref).strip():
                raise ValueError("apply requires --decision-ref")
            if not data["ready"]:
                raise ValueError("mapping is not complete and collision-free")
            with conn:
                for item in data["downstream_links"]:
                    conn.execute(
                        "UPDATE evaluation_evidence SET item_id=? "
                        "WHERE evaluation_id=? AND item_id=?",
                        (item["new_item_id"], item["evaluation_id"], item["old_item_id"]),
                    )
            data["applied"] = True
            data["decision_ref"] = decision_ref
        else:
            data["applied"] = False
    return data


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_run")
    parser.add_argument("new_run")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--decision-ref")
    args = parser.parse_args()
    try:
        result = reconcile(args.db, args.old_run, args.new_run,
                           apply=args.apply, decision_ref=args.decision_ref)
        output = local_path(args.output)
        if output.exists():
            raise ValueError(f"refusing to overwrite existing output: {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8", newline="\n")
        print(f"reconcile_generation_evidence: PASS - links={result['downstream_link_count']}; "
              f"ready={result['ready']}; applied={result['applied']}")
        return 0
    except (OSError, ValueError, KeyError, sqlite3.Error) as exc:
        print(f"reconcile_generation_evidence: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
