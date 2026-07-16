#!/usr/bin/env python3
"""Promote, reject, or roll back immutable sieve generations with recorded decisions."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml

import db_util


ROOT = Path(__file__).resolve().parents[1]
APPROVALS = ROOT / "manifests" / "approvals.csv"
ACTIVE_PROMPTS = ROOT / "sieving" / "prompts" / "active.yml"
CHANGELOG = ROOT / "sieving" / "prompts" / "CHANGELOG.md"


def _approved(reference: str, approvals: Path) -> bool:
    if not approvals.is_file():
        return False
    with approvals.open(encoding="utf-8-sig", newline="") as handle:
        return any(row["object_id"] == reference and row["decision"].lower() == "approved"
                   for row in csv.DictReader(handle))


def _promotion_score(path: Path, prompt_version: str) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("prompt_version") != prompt_version:
        raise ValueError("golden score prompt_version does not match target generation")
    if not data.get("golden_approved") or not data.get("golden_approval_ref"):
        raise ValueError("promotion requires a human-approved golden calibration set")
    if not data.get("promotion_ready"):
        raise ValueError("golden score is not promotion-ready (missed or spurious crumbs remain)")
    return data


def _write_active_prompt(path: Path, side: str, version: str) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {"schema_version": "1.0", "active": {}}
    data.setdefault("active", {})[side] = version
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8", newline="")
    temporary.replace(path)


def _changelog_has_lesson(changelog: Path, prompt_version: str) -> bool:
    if not changelog.is_file():
        return False
    return any(
        prompt_version in line and any(skill in line for skill in
                                       ("sieving-run", "crumb-quality", "sieving-tuning"))
        for line in changelog.read_text(encoding="utf-8").splitlines()
    )


def decide(
    db: Path, *, run_id: str, operation: str, decision_ref: str, reason: str,
    approvals: Path = APPROVALS, score: Path | None = None,
    active_prompts: Path = ACTIVE_PROMPTS, changelog: Path = CHANGELOG,
) -> None:
    if operation not in {"promote", "rollback", "reject"}:
        raise ValueError(f"invalid generation operation: {operation}")
    if not _approved(decision_ref, approvals):
        raise ValueError(f"approved decision missing: {decision_ref}")
    with db_util.connect(db) as conn:
        target = db_util.lookup(conn, "sieve_runs", "run_id", run_id)
        if target is None:
            raise ValueError(f"unknown sieve run: {run_id}")
        current = conn.execute(
            "SELECT * FROM sieve_runs WHERE doc_id=? AND is_active=1", (target["doc_id"],)
        ).fetchone()
        if current is None:
            raise ValueError("document has no active generation")
        if operation == "reject":
            if target["status"] != "candidate" or target["is_active"]:
                raise ValueError("only an inactive candidate can be rejected")
            if not _changelog_has_lesson(changelog, target["prompt_version"]):
                raise ValueError("prompt rejection requires a CHANGELOG-linked skill lesson")
            conn.execute("UPDATE sieve_runs SET status='rejected', decision_ref=? WHERE run_id=?",
                         (decision_ref, run_id))
        else:
            expected = "candidate" if operation == "promote" else "superseded"
            if target["status"] != expected or target["is_active"]:
                raise ValueError(f"{operation} requires an inactive {expected} generation")
            if target["completed_at"] is None:
                raise ValueError("generation must be completed before activation")
            downstream = conn.execute(
                "SELECT count(*) FROM evaluation_evidence e JOIN crumbs c ON c.item_id=e.item_id "
                "WHERE c.doc_id=?", (target["doc_id"],)
            ).fetchone()[0]
            if downstream:
                raise ValueError("generation change refused after downstream evaluation evidence exists")
            if operation == "promote":
                if score is None:
                    raise ValueError("promotion requires --score from score_sieving.py")
                score_data = _promotion_score(score, target["prompt_version"])
                if not _approved(str(score_data["golden_approval_ref"]), approvals):
                    raise ValueError("golden score approval reference is not approved")
                if not _changelog_has_lesson(changelog, target["prompt_version"]):
                    raise ValueError("prompt promotion requires a CHANGELOG-linked skill lesson")
            conn.execute(
                "UPDATE sieve_runs SET is_active=0,status='superseded' WHERE run_id=?",
                (current["run_id"],),
            )
            conn.execute(
                "UPDATE sieve_runs SET is_active=1,status='active',decision_ref=? WHERE run_id=?",
                (decision_ref, run_id),
            )
        db_util.insert(conn, "sieve_generation_events", {
            "doc_id": target["doc_id"], "from_run_id": current["run_id"],
            "to_run_id": run_id, "operation": operation,
            "decision_ref": decision_ref, "reason": reason,
        })
        side = target["document_side"]
        version = target["prompt_version"]
    if operation in {"promote", "rollback"}:
        _write_active_prompt(active_prompts, side, version)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["promote", "rollback", "reject"])
    parser.add_argument("run_id")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--decision-ref", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--score", type=Path)
    parser.add_argument("--active-prompts", type=Path, default=ACTIVE_PROMPTS)
    parser.add_argument("--changelog", type=Path, default=CHANGELOG)
    args = parser.parse_args()
    try:
        decide(args.db, run_id=args.run_id, operation=args.operation,
               decision_ref=args.decision_ref, reason=args.reason,
               approvals=args.approvals, score=args.score,
               active_prompts=args.active_prompts, changelog=args.changelog)
        print(f"sieve_generation: PASS - {args.operation} {args.run_id}")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"sieve_generation: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
