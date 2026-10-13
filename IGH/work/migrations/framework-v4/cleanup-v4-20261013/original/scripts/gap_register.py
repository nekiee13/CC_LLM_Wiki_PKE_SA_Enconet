#!/usr/bin/env python3
"""Preview or create one draft gap and its explicit missing-evidence action."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path

STATUSES = {"covered", "mostly-covered", "partially-covered", "minimally-covered",
            "not-covered", "not-applicable", "undetermined", "missing-evidence"}
ACTION_TYPES = {"verification", "document_request"}
FIELDS = {"gap_id", "evaluation_id", "status", "description", "evidence_item_id",
          "missing_evidence_ref", "action_type", "action_description"}


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")
    return value.strip()


def _normalize(record: object) -> dict[str, str | None]:
    if not isinstance(record, dict) or set(record) - FIELDS:
        raise ValueError("gap record is not an object or has unknown fields")
    gap_id = _text(record.get("gap_id"), "gap_id")
    eval_id = _text(record.get("evaluation_id"), "evaluation_id")
    if db_util.id_patterns()["gap_id"].fullmatch(gap_id) is None:
        raise ValueError(f"invalid gap ID: {gap_id}")
    if db_util.id_patterns()["evaluation_id"].fullmatch(eval_id) is None:
        raise ValueError(f"invalid evaluation ID: {eval_id}")
    status = _text(record.get("status"), "status")
    if status not in STATUSES:
        raise ValueError(f"invalid gap status: {status}")
    description = _text(record.get("description"), "description")
    evidence = record.get("evidence_item_id")
    missing = record.get("missing_evidence_ref")
    if (evidence is not None) == (missing is not None):
        raise ValueError("exactly one weak/missing evidence pointer required")
    evidence = _text(evidence, "evidence_item_id") if evidence is not None else None
    missing = _text(missing, "missing_evidence_ref") if missing is not None else None
    if evidence is not None and db_util.id_patterns()["crumb_id"].fullmatch(evidence) is None:
        raise ValueError("invalid evidence crumb ID")
    action_type = record.get("action_type")
    action_description = record.get("action_description")
    if status == "missing-evidence":
        if missing is None:
            raise ValueError("missing-evidence gap needs missing_evidence_ref")
        action_type = _text(action_type, "action_type")
        if action_type not in ACTION_TYPES:
            raise ValueError("missing-evidence action must be verification or document_request")
        action_description = _text(action_description, "action_description")
    elif action_type is not None or action_description is not None:
        raise ValueError("action fields are only valid for missing-evidence gaps")
    return {"gap_id": gap_id, "evaluation_id": eval_id, "status": status,
            "description": description, "evidence_item_id": evidence,
            "missing_evidence_ref": missing, "action_type": action_type,
            "action_description": action_description}


def _plan(conn: sqlite3.Connection, record: dict[str, str | None]) -> dict[str, object]:
    evaluation = db_util.lookup(conn, "criterion_evaluations", "evaluation_id", record["evaluation_id"])
    if evaluation is None:
        raise ValueError(f"unknown criterion evaluation: {record['evaluation_id']}")
    evidence = record["evidence_item_id"]
    if evidence is not None:
        crumb = conn.execute(
            "SELECT c.criterion_id,r.is_active FROM crumbs c "
            "JOIN sieve_runs r ON r.run_id=c.sieve_run_id WHERE c.item_id=?", (evidence,),
        ).fetchone()
        if crumb is None or crumb["criterion_id"] != evaluation["criterion_id"] or not crumb["is_active"]:
            raise ValueError("evidence crumb is missing, inactive, or from another criterion")
    existing = db_util.lookup(conn, "gaps", "gap_id", record["gap_id"])
    if existing is not None:
        if any(existing[key] != record[key] for key in
               ("evaluation_id", "status", "description", "evidence_item_id", "missing_evidence_ref")):
            raise ValueError(f"existing gap differs; refusing rewrite: {record['gap_id']}")
        action_id = None
        if record["status"] == "missing-evidence":
            actions = conn.execute(
                "SELECT * FROM auditor_actions WHERE gap_id=? ORDER BY action_id",
                (record["gap_id"],),
            ).fetchall()
            if len(actions) != 1 or actions[0]["action_type"] != record["action_type"] or \
                    actions[0]["description"] != record["action_description"] or \
                    actions[0]["approval_status"] != "draft" or actions[0]["state"] != "open":
                raise ValueError("existing missing-evidence action differs or has progressed")
            action_id = actions[0]["action_id"]
        return {"state": "preserve", "gap_id": record["gap_id"],
                "evaluation_run_id": evaluation["evaluation_run_id"], "action_id": action_id}
    action_id = None
    if record["status"] == "missing-evidence":
        ids = [row[0] for row in conn.execute("SELECT action_id FROM auditor_actions")]
        pattern = db_util.id_patterns()["action_id"]
        if any(pattern.fullmatch(value) is None for value in ids):
            raise ValueError("existing action ID is invalid")
        next_number = max((int(value[4:]) for value in ids), default=0) + 1
        action_id = f"ACT-{next_number:04d}"
        if pattern.fullmatch(action_id) is None:
            raise ValueError("action ID space is exhausted")
    return {"state": "create", "gap_id": record["gap_id"],
            "evaluation_run_id": evaluation["evaluation_run_id"], "action_id": action_id}


def register(db: Path, record: object, *, apply: bool = False) -> dict[str, object]:
    normalized = _normalize(record)
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    if apply:
        # mode=rw refuses a vanished database instead of creating an empty one.
        with closing(sqlite3.connect(database.as_uri() + "?mode=rw", uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys=ON")
            if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
                raise RuntimeError("SQLite foreign-key enforcement is unavailable")
            conn.execute("BEGIN IMMEDIATE")
            try:
                plan = _plan(conn, normalized)
                if plan["state"] == "create":
                    db_util.insert(conn, "gaps", {key: normalized[key] for key in
                        ("gap_id", "evaluation_id", "status", "description",
                         "evidence_item_id", "missing_evidence_ref")})
                    if plan["action_id"] is not None:
                        db_util.insert(conn, "auditor_actions", {
                            "action_id": plan["action_id"],
                            "evaluation_run_id": plan["evaluation_run_id"],
                            "gap_id": normalized["gap_id"],
                            "action_type": normalized["action_type"],
                            "description": normalized["action_description"],
                        })
                conn.commit()
            except Exception:
                conn.rollback()
                raise
        plan["mode"] = "apply" if plan["state"] == "create" else "preserve"
    else:
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA query_only=ON")
            plan = _plan(conn, normalized)
        plan["mode"] = "preview"
    plan["approval"] = "not-granted"
    return plan


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        record = json.loads(local_path(args.record).read_text(encoding="utf-8"))
        print(json.dumps(register(args.db, record, apply=args.apply), ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, sqlite3.Error,
            json.JSONDecodeError) as exc:
        print(f"gap_register: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
