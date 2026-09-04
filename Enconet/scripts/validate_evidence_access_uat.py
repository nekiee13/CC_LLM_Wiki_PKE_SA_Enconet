#!/usr/bin/env python3
"""Validate the fixed EA5.4 Owner UAT packet without making a human decision."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

import validate_review_package


EXPECTED_ACTIONS = [
    "open_report",
    "open_multi_quote_crumb",
    "confirm_source_identity",
    "navigate_adjacent_context",
    "copy_traceable_citation",
    "print_evidence_card",
    "open_second_criterion",
    "select_run_from_workspace",
    "open_document_record",
    "open_package_record",
]
EXPECTED_ROLES = ["manifest", "workspace", "report", "viewer"]
SHA256 = re.compile(r"[0-9a-f]{64}")


def load_contract(path: Path) -> dict:
    """Load the controlled YAML contract, failing closed on a non-object root."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("UAT contract must be an object")
    return value


def _safe_project_path(project_root: Path, relative: object) -> Path | None:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        return None
    candidate = (project_root / relative).resolve()
    root = project_root.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _load_bundle(package_root: Path, run_id: str) -> dict:
    path = package_root / run_id / "evidence_bundle.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("evidence bundle must be an object")
    return value


def validate(contract_path: Path, packet_path: Path, project_root: Path) -> tuple[list[str], dict]:
    """Return deterministic preflight errors and a compact human-gate summary."""
    errors: list[str] = []
    summary = {"steps": 0, "artifacts": 0, "decision": "unknown"}
    try:
        contract = load_contract(contract_path)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [f"UAT contract is unreadable: {exc}"], summary

    required = {
        "schema_version", "uat_id", "status", "run_id", "package_root",
        "primary_crumb_id", "secondary_crumb_id", "artifacts", "steps",
        "owner_decision",
    }
    if set(contract) != required:
        errors.append("UAT contract fields mismatch")
    if contract.get("schema_version") != "1.0":
        errors.append("unsupported UAT schema_version")
    if contract.get("uat_id") != "EA5.4-RUN-20260728-01":
        errors.append("unexpected UAT identity")
    status = contract.get("status")
    if status not in {"awaiting_owner", "approved", "rejected"}:
        errors.append("invalid UAT status")
    run_id = contract.get("run_id")
    if run_id != "RUN-20260728-01":
        errors.append("unexpected UAT run_id")

    steps = contract.get("steps")
    if not isinstance(steps, list):
        steps = []
        errors.append("UAT steps must be an array")
    summary["steps"] = len(steps)
    if [row.get("id") for row in steps if isinstance(row, dict)] != [f"UAT-{n}" for n in range(1, 11)]:
        errors.append("UAT step identities mismatch")
    if [row.get("action") for row in steps if isinstance(row, dict)] != EXPECTED_ACTIONS:
        errors.append("UAT step actions mismatch")
    for index, row in enumerate(steps):
        if not isinstance(row, dict) or set(row) != {"id", "action", "expected"}:
            errors.append(f"UAT step fields mismatch: steps[{index}]")
        elif not isinstance(row["expected"], str) or not row["expected"].strip():
            errors.append(f"missing expected observation: steps[{index}]")

    decision = contract.get("owner_decision")
    expected_blank = {
        "decision": None,
        "decided_at_utc": None,
        "decision_reference": None,
        "observed_defects": [],
    }
    if status == "awaiting_owner":
        if decision != expected_blank:
            errors.append("awaiting packet contains a premature Owner decision")
        summary["decision"] = "awaiting_owner"
    else:
        expected_decision = "approve" if status == "approved" else "reject"
        complete = (
            isinstance(decision, dict)
            and decision.get("decision") == expected_decision
            and isinstance(decision.get("decided_at_utc"), str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", decision["decided_at_utc"]) is not None
            and isinstance(decision.get("decision_reference"), str)
            and bool(decision["decision_reference"].strip())
            and isinstance(decision.get("observed_defects"), list)
        )
        if not complete:
            errors.append(f"{status} UAT requires a complete Owner decision")
        elif status == "approved" and decision["observed_defects"]:
            errors.append("approved UAT cannot contain unresolved observed defects")
        elif status == "rejected" and not decision["observed_defects"]:
            errors.append("rejected UAT requires at least one observed defect")
        summary["decision"] = expected_decision

    artifacts = contract.get("artifacts")
    if not isinstance(artifacts, list):
        artifacts = []
        errors.append("UAT artifacts must be an array")
    summary["artifacts"] = len(artifacts)
    roles = [row.get("role") for row in artifacts if isinstance(row, dict)]
    if roles != EXPECTED_ROLES:
        errors.append("UAT artifact roles mismatch")
    for index, row in enumerate(artifacts):
        if not isinstance(row, dict) or set(row) != {"role", "path", "sha256"}:
            errors.append(f"UAT artifact fields mismatch: artifacts[{index}]")
            continue
        path = _safe_project_path(project_root, row.get("path"))
        if path is None:
            errors.append(f"unsafe UAT artifact path: artifacts[{index}]")
            continue
        if not path.is_file():
            errors.append(f"missing UAT artifact: {path.name}")
            continue
        expected_hash = row.get("sha256")
        if not isinstance(expected_hash, str) or SHA256.fullmatch(expected_hash) is None:
            errors.append(f"invalid artifact hash: {path.name}")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"artifact hash mismatch: {path.name}")

    package_root = _safe_project_path(project_root, contract.get("package_root"))
    if package_root is None:
        errors.append("unsafe UAT package_root")
    elif package_root.is_dir():
        try:
            errors.extend(f"review package: {error}" for error in validate_review_package.validate(package_root))
            bundle = _load_bundle(package_root, str(run_id))
            crumbs = {row.get("crumb_id"): row for row in bundle.get("crumbs", []) if isinstance(row, dict)}
            chunks = {row.get("chunk_id"): row for row in bundle.get("chunks", []) if isinstance(row, dict)}
            primary = crumbs.get(contract.get("primary_crumb_id"))
            secondary = crumbs.get(contract.get("secondary_crumb_id"))
            if not primary or len(primary.get("quote_ids", [])) < 2:
                errors.append("primary UAT crumb is missing or does not have multiple quotes")
            else:
                chunk = chunks.get(primary.get("chunk_ids", [None])[0])
                if not chunk or not chunk.get("previous_chunk_id") or not chunk.get("next_chunk_id"):
                    errors.append("primary UAT crumb lacks adjacent context")
            if not secondary or secondary.get("criterion_id") != "APP_B_II":
                errors.append("secondary UAT criterion is missing")
            if primary and secondary and primary.get("criterion_id") == secondary.get("criterion_id"):
                errors.append("UAT crumbs must exercise different criteria")
        except (OSError, UnicodeError, ValueError, KeyError, json.JSONDecodeError) as exc:
            errors.append(f"UAT package evidence is unreadable: {exc}")
    else:
        errors.append("missing UAT package_root")

    try:
        packet = packet_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"UAT packet is unreadable: {exc}")
        packet = ""
    decision_marker = {
        "awaiting_owner": "Owner decision: **AWAITING OWNER**",
        "approved": "Owner decision: **APPROVED**",
        "rejected": "Owner decision: **REJECTED**",
    }.get(status, "Owner decision:")
    for marker in [str(contract.get("uat_id")), str(run_id), decision_marker]:
        if marker not in packet:
            errors.append(f"UAT packet missing marker: {marker}")
    for row in artifacts:
        if isinstance(row, dict) and isinstance(row.get("sha256"), str) and row["sha256"] not in packet:
            errors.append(f"UAT packet missing artifact hash: {row.get('role')}")
    return list(dict.fromkeys(errors)), summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args(argv)
    errors, summary = validate(args.contract, args.packet, args.project_root)
    if errors:
        for error in errors:
            print(f"validate_evidence_access_uat: FAIL - {error}", file=sys.stderr)
        return 1
    print(
        "validate_evidence_access_uat: PASS - "
        f"steps={summary['steps']} artifacts={summary['artifacts']} decision={summary['decision']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
