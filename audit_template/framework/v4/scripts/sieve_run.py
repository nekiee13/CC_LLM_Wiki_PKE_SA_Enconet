#!/usr/bin/env python3
"""Create a guarded local sieve run from local prompt and source records."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import yaml

import db_util
from project_paths import local_path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "sieving" / "prompts"
ACTIVE = PROMPTS / "active.yml"
CHANGELOG = PROMPTS / "CHANGELOG.md"
SIDES = {"RULE", "DOCUMENT"}
ROLES = {"GOVERNING", "INTERPRETIVE"}
APPLICABILITY = {"APPLICABLE", "CONDITIONAL", "NOT_APPLICABLE"}
VERSION_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_prompt(side: str, version: str, *, is_candidate: bool) -> None:
    if VERSION_NAME.fullmatch(version) is None:
        raise ValueError("prompt_version must be a simple local version name")
    registry = yaml.safe_load(local_path(ACTIVE).read_text(encoding="utf-8"))
    active = registry.get("active") if isinstance(registry, dict) else None
    active_version = active.get(side) if isinstance(active, dict) else None
    if not _nonempty(active_version):
        raise ValueError(f"active prompt is missing for {side}")
    if not is_candidate and version != active_version:
        raise ValueError(f"first run must use the active prompt for {side}")
    if not local_path(PROMPTS / f"{version}.md").is_file():
        raise ValueError(f"local prompt file is missing: {version}.md")
    if is_candidate and version != active_version:
        history = local_path(CHANGELOG).read_text(encoding="utf-8")
        rows = (
            line.strip().strip("|").split("|", 1)[0].strip().strip("`")
            for line in history.splitlines() if line.lstrip().startswith("|")
        )
        if version not in rows:
            raise ValueError(f"candidate prompt has no CHANGELOG row: {version}")


def _check_references(authorities: object, side: str) -> list[dict[str, object]]:
    if not isinstance(authorities, list):
        raise ValueError("authority references must be a list")
    if side == "RULE" and not authorities:
        raise ValueError("RULE run requires authority references")
    if side == "DOCUMENT" and authorities:
        raise ValueError("DOCUMENT run forbids authority references")
    checked: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for index, ref in enumerate(authorities):
        if not isinstance(ref, dict):
            raise ValueError(f"authority reference {index} must be an object")
        role, code, locator = (ref.get("authority_role"), ref.get("source_code"),
                               ref.get("source_locator"))
        if not isinstance(role, str) or role not in ROLES or not _nonempty(code) or not _nonempty(locator):
            raise ValueError(f"authority reference {index} needs a role, source_code, and locator")
        applicability = ref.get("applicability", "APPLICABLE")
        if not isinstance(applicability, str) or applicability not in APPLICABILITY:
            raise ValueError(f"authority reference {index} has invalid applicability")
        if applicability == "CONDITIONAL" and not _nonempty(ref.get("applicability_basis")):
            raise ValueError(f"authority reference {index} needs a conditional applicability basis")
        key = (str(role), str(code), str(locator))
        if key in seen:
            raise ValueError(f"duplicate authority reference: {key}")
        seen.add(key)
        checked.append(ref)
    if side == "RULE" and not any(ref["authority_role"] == "GOVERNING" for ref in checked):
        raise ValueError("RULE run needs at least one governing source")
    return checked


def create_run(
    db: Path, *, run_id: str, doc_id: str, prompt_version: str,
    document_side: str, authorities: list[dict], rejected_item_count: int = 0,
    failed_item_count: int = 0,
) -> dict[str, object]:
    if document_side not in SIDES:
        raise ValueError(f"invalid document_side: {document_side!r}")
    if rejected_item_count < 0 or failed_item_count < 0:
        raise ValueError("rejected/failed item counts cannot be negative")
    refs = _check_references(authorities, document_side)
    db_path = local_path(db)
    if not db_path.is_file():
        raise ValueError(f"local database is not initialized: {db_path}")
    with closing(db_util.connect(db_path)) as conn:
        with conn:
            document = db_util.lookup(conn, "documents", "doc_id", doc_id)
            if document is None:
                raise ValueError(f"unknown document: {doc_id}")
            if document["document_side"] != document_side:
                raise ValueError("run side does not match registered document side")
            prior = conn.execute(
                "SELECT * FROM sieve_runs WHERE doc_id=? ORDER BY generation", (doc_id,)
            ).fetchall()
            active = [row for row in prior if row["is_active"]]
            if prior and len(active) != 1:
                raise ValueError(f"document {doc_id} must have exactly one active generation")
            _check_prompt(document_side, prompt_version, is_candidate=bool(prior))
            for ref in refs:
                row = conn.execute(
                    "SELECT 1 FROM approved_sources WHERE source_code=? AND authority_role=?",
                    (ref["source_code"], ref["authority_role"]),
                ).fetchone()
                if row is None:
                    raise ValueError(
                        f"source is not registered with this role: {ref['source_code']}"
                    )
            generation = max((int(row["generation"]) for row in prior), default=0) + 1
            previous = active[0] if active else None
            warning = None
            if previous and previous["prompt_version"] == prompt_version:
                warning = f"unchanged prompt version {prompt_version}; no-op tuning candidate"
            governing = next(
                (ref["source_code"] for ref in refs if ref["authority_role"] == "GOVERNING"), None
            )
            db_util.insert(conn, "sieve_runs", {
                "run_id": run_id, "doc_id": doc_id,
                "prompt_version": prompt_version, "document_side": document_side,
                "source_rule": governing, "generation": generation,
                "status": "candidate" if previous else "active",
                "is_active": 0 if previous else 1,
                "supersedes_run_id": previous["run_id"] if previous else None,
                "rejected_item_count": rejected_item_count,
                "failed_item_count": failed_item_count,
            })
            for ref in refs:
                db_util.insert(conn, "sieve_run_authorities", {
                    "run_id": run_id, "authority_role": ref["authority_role"],
                    "source_code": ref["source_code"], "source_locator": ref["source_locator"],
                    "applicability": ref.get("applicability", "APPLICABLE"),
                    "applicability_basis": ref.get("applicability_basis"),
                })
            return {
                "generation": generation, "status": "candidate" if previous else "active",
                "supersedes_run_id": previous["run_id"] if previous else None,
                "warning": warning,
            }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--prompt-version", required=True)
    parser.add_argument("--document-side", required=True)
    parser.add_argument("--authority-json", action="append", default=[],
                        help="one JSON authority object; repeatable")
    parser.add_argument("--rejected-item-count", type=int, default=0)
    parser.add_argument("--failed-item-count", type=int, default=0)
    args = parser.parse_args()
    try:
        refs = [json.loads(value) for value in args.authority_json]
        result = create_run(
            args.db, run_id=args.run_id, doc_id=args.doc_id,
            prompt_version=args.prompt_version, document_side=args.document_side,
            authorities=refs, rejected_item_count=args.rejected_item_count,
            failed_item_count=args.failed_item_count,
        )
        print(f"sieve_run: PASS - {args.run_id}; generation={result['generation']}; status={result['status']}")
        if result["warning"]:
            print(f"WARNING: {result['warning']}")
        return 0
    except (ValueError, OSError, sqlite3.Error, KeyError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"sieve_run: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
