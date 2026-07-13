#!/usr/bin/env python3
"""Apply a manifest-backed approval to one EPIC10 finding or auditor action."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import db_util
from finding_workflow import (
    ACTIONS_DIR, APPROVALS, FINDINGS_DIR, ACTION_TEMPLATE, FINDING_TEMPLATE,
    action_page_values, approved, finding_page_values, render_template, _atomic_write,
)


def approve_object(db: Path, object_id: str, *, approvals: Path = APPROVALS,
                   findings_dir: Path = FINDINGS_DIR, actions_dir: Path = ACTIONS_DIR) -> None:
    decision = approved(object_id, approvals)
    if not decision or not decision.get("date") or not decision.get("reviewer"):
        raise ValueError(f"approved manifest row with date/reviewer missing for {object_id}")
    # Approval must not repair or overwrite a broken draft projection.  Re-prove
    # the complete EPIC10 state before changing the authoritative DB row.
    from validate_findings import validate
    errors = validate(db, approvals=approvals, findings_dir=findings_dir, actions_dir=actions_dir)
    if errors:
        raise ValueError(f"finding/action validation failed before approval: {errors[0]}")
    with db_util.connect(db) as conn:
        if object_id.startswith("FIND-"):
            row = conn.execute("SELECT * FROM findings WHERE finding_id=?", (object_id,)).fetchone()
            if not row:
                raise ValueError("unknown finding")
            if bool(row["evidence_item_id"]) == bool(row["gap_id"]):
                raise ValueError("finding has broken evidence/gap links")
            conn.execute("UPDATE findings SET status='approved', approval_ref=? WHERE finding_id=?",
                         (object_id, object_id))
            projected = dict(conn.execute("SELECT * FROM findings WHERE finding_id=?", (object_id,)).fetchone())
            target, template, values = findings_dir / f"{object_id}.md", FINDING_TEMPLATE, finding_page_values(projected)
        elif object_id.startswith("ACT-"):
            row = conn.execute("SELECT * FROM auditor_actions WHERE action_id=?", (object_id,)).fetchone()
            if not row:
                raise ValueError("unknown action")
            if bool(row["finding_id"]) == bool(row["gap_id"]):
                raise ValueError("action has broken finding/gap links")
            conn.execute("UPDATE auditor_actions SET approval_status='approved', approval_ref=? WHERE action_id=?",
                         (object_id, object_id))
            projected = dict(conn.execute("SELECT * FROM auditor_actions WHERE action_id=?", (object_id,)).fetchone())
            target, template, values = actions_dir / f"{object_id}.md", ACTION_TEMPLATE, action_page_values(projected)
        else:
            raise ValueError("object_id must be FIND-* or ACT-*")
    _atomic_write(target, render_template(template, values))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("object_id")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--findings-dir", type=Path, default=FINDINGS_DIR)
    parser.add_argument("--actions-dir", type=Path, default=ACTIONS_DIR)
    args = parser.parse_args()
    try:
        approve_object(args.db, args.object_id, approvals=args.approvals,
                       findings_dir=args.findings_dir, actions_dir=args.actions_dir)
        print(f"approve: PASS - {args.object_id}")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI fail-closed boundary
        print(f"approve: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
