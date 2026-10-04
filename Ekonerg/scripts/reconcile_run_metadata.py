#!/usr/bin/env python3
"""Safely reconcile one approved scoring-model run metadata value.

The default mode is a read-only preview.  Applying the change requires an
approved decision reference and an exact old value, so a stale or wrong run
cannot be changed by accident.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import db_util


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "db" / "nqa_audit.sqlite"
DEFAULT_APPROVALS = ROOT / "manifests" / "approvals.csv"
DEFAULT_RUN_ID = "RUN-20261003-32"
DEFAULT_OLD = "0.1-placeholder"
DEFAULT_NEW = "1.0-ekonerg-20261004"


def _approved(ref: str, approvals: Path) -> bool:
    approvals = db_util.local_path(approvals)
    if not approvals.is_file():
        return False
    with approvals.open(encoding="utf-8-sig", newline="") as handle:
        return any(row["object_id"] == ref and row["decision"].lower() == "approved"
                   for row in csv.DictReader(handle))


def _row(conn, run_id: str):
    return conn.execute(
        "SELECT run_id, supplier, deliverable_language, scoring_model_version, "
        "started_at, completed_at FROM evaluation_runs WHERE run_id=?", (run_id,)
    ).fetchone()


def _digest(row) -> str:
    payload = {key: row[key] for key in row.keys()}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def reconcile(*, db: Path, run_id: str = DEFAULT_RUN_ID,
              old_version: str = DEFAULT_OLD, new_version: str = DEFAULT_NEW,
              decision_ref: str | None = None, approvals: Path = DEFAULT_APPROVALS,
              apply: bool = False, evidence: Path | None = None) -> dict:
    """Preview or apply the one-row metadata correction and return evidence."""
    if run_id != DEFAULT_RUN_ID:
        raise ValueError(f"refused: only controlled target {DEFAULT_RUN_ID} is allowed")
    if old_version != DEFAULT_OLD or new_version != DEFAULT_NEW:
        raise ValueError("refused: controlled old/new model versions do not match")
    if apply and not decision_ref:
        raise ValueError("apply requires --decision-ref")
    if apply and not _approved(decision_ref, approvals):
        raise ValueError(f"approved decision missing: {decision_ref}")

    with db_util.connect(db) as conn:
        before = _row(conn, run_id)
        if before is None:
            raise ValueError(f"unknown evaluation run: {run_id}")
        if before["scoring_model_version"] != old_version:
            raise ValueError(
                "refused: current scoring_model_version is not the exact expected "
                f"old value {old_version!r}"
            )
        before_hash = _digest(before)
        changed = False
        if apply:
            updated = conn.execute(
                "UPDATE evaluation_runs SET scoring_model_version=? "
                "WHERE run_id=? AND scoring_model_version=?",
                (new_version, run_id, old_version),
            ).rowcount
            if updated != 1:
                raise ValueError(f"refused: expected one row update, got {updated}")
            after = _row(conn, run_id)
            if after["scoring_model_version"] != new_version:
                raise ValueError("refused: post-update value did not match new version")
            conn.commit()
            changed = True
        else:
            after = before
        result = {
            "schema_version": "1.0",
            "run_id": run_id,
            "mode": "apply" if apply else "dry-run",
            "decision_ref": decision_ref,
            "old_version": old_version,
            "new_version": new_version,
            "before_hash": before_hash,
            "after_hash": _digest(after),
            "changed": changed,
            "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        }
    if evidence is not None:
        evidence = db_util.local_path(evidence)
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("db/nqa_audit.sqlite"))
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--old-version", default=DEFAULT_OLD)
    parser.add_argument("--new-version", default=DEFAULT_NEW)
    parser.add_argument("--decision-ref")
    parser.add_argument("--approvals", type=Path, default=Path("manifests/approvals.csv"))
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        result = reconcile(db=args.db, run_id=args.run_id, old_version=args.old_version,
                           new_version=args.new_version, decision_ref=args.decision_ref,
                           approvals=args.approvals, apply=args.apply, evidence=args.evidence)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"reconcile_run_metadata: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
