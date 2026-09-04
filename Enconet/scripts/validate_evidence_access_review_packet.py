#!/usr/bin/env python3
"""Validate the prepared EA6.3 independent-review packet without reviewing it."""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml

import validate_evidence_access_candidate
import validate_evidence_access_docs


SHA256 = re.compile(r"[0-9a-f]{64}")


def load_contract(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("review protocol must be an object")
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(contract_path: Path, packet_path: Path, project_root: Path) -> tuple[list[str], dict]:
    errors: list[str] = []
    summary = {"commands": 0, "risks": 0, "decision": "unknown"}
    try:
        contract = load_contract(contract_path)
        packet = packet_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [f"review packet is unreadable: {exc}"], summary
    required = {
        "schema_version", "review_id", "status", "reviewer", "implementation_base",
        "implementation_tip", "run_id", "candidate_manifest_sha256",
        "approved_report_sha256", "approved_dashboard_sha256", "expected_counts",
        "commands", "risk_checks", "review_decision",
    }
    if set(contract) != required:
        errors.append("review protocol fields mismatch")
    if contract.get("schema_version") != "1.0":
        errors.append("unsupported review protocol schema_version")
    if contract.get("status") != "awaiting_claude" or contract.get("reviewer") != "claude-code":
        errors.append("independent review must remain assigned to Claude")
    if contract.get("run_id") != "RUN-20260728-01":
        errors.append("review run identity mismatch")
    commands = contract.get("commands") if isinstance(contract.get("commands"), list) else []
    risks = contract.get("risk_checks") if isinstance(contract.get("risk_checks"), list) else []
    summary.update(commands=len(commands), risks=len(risks), decision="awaiting_claude")
    if len(commands) != 8 or len({row.get("id") for row in commands if isinstance(row, dict)}) != 8:
        errors.append("review command set must contain eight unique commands")
    if len(risks) != 10 or len({row.get("id") for row in risks if isinstance(row, dict)}) != 10:
        errors.append("review risk set must contain ten unique checks")
    for row in commands:
        if not isinstance(row, dict) or set(row) != {"id", "text"}:
            errors.append("review command fields mismatch")
            continue
        if f"review-command:{row['id']}" not in packet:
            errors.append(f"review packet missing command: {row['id']}")
        if row["text"] not in packet:
            errors.append(f"review packet command text drift: {row['id']}")
    for row in risks:
        if not isinstance(row, dict) or set(row) != {"id", "description"}:
            errors.append("review risk fields mismatch")
            continue
        if f"risk-check:{row['id']}" not in packet or row["description"] not in packet:
            errors.append(f"review packet missing risk check: {row['id']}")
    blank = {"decision": None, "reviewed_at_utc": None, "message_id": None, "findings": []}
    if contract.get("review_decision") != blank:
        errors.append("awaiting review contains a premature reviewer decision")
    for marker in [
        str(contract.get("review_id")), str(contract.get("implementation_tip")),
        str(contract.get("candidate_manifest_sha256")), "Reviewer decision: **AWAITING CLAUDE**",
    ]:
        if marker not in packet:
            errors.append(f"review packet missing marker: {marker}")

    hashes = {
        "candidate manifest": (
            project_root / "outputs" / "candidates" / "evidence_access" / "portable_package" / "package_manifest.json",
            contract.get("candidate_manifest_sha256"),
        ),
        "approved report": (
            project_root / "outputs" / "enconet_appendix_b_evaluation_report.md",
            contract.get("approved_report_sha256"),
        ),
        "approved dashboard": (
            project_root / "outputs" / "enconet_appendix_b_dashboard.html",
            contract.get("approved_dashboard_sha256"),
        ),
    }
    for label, (path, expected) in hashes.items():
        if not isinstance(expected, str) or SHA256.fullmatch(expected) is None:
            errors.append(f"invalid {label} hash")
        elif not path.is_file() or _digest(path) != expected:
            errors.append(f"{label} hash mismatch")
    for revision in (contract.get("implementation_base"), contract.get("implementation_tip")):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", f"{revision}^{{commit}}"], cwd=project_root,
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            errors.append(f"review revision is unavailable: {revision}")

    candidate_errors, _ = validate_evidence_access_candidate.validate(
        project_root / "schemas" / "evidence_access_release_candidate.yml", project_root
    )
    errors.extend(f"candidate preflight: {error}" for error in candidate_errors)
    docs_errors, _ = validate_evidence_access_docs.validate(
        project_root / "schemas" / "evidence_access_operations.yml",
        project_root / "docs" / "EVIDENCE_ACCESS_OPERATIONS.md",
        project_root / "docs" / "EVIDENCE_ACCESS_ARCHITECTURE.md",
        project_root / "docs" / "EVIDENCE_ACCESS_UPGRADE_GUIDE.md",
        project_root, rehearse=False,
    )
    errors.extend(f"documentation preflight: {error}" for error in docs_errors)
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
            print(f"validate_evidence_access_review_packet: FAIL - {error}", file=sys.stderr)
        return 1
    print(
        "validate_evidence_access_review_packet: PASS - "
        f"commands={summary['commands']} risks={summary['risks']} decision={summary['decision']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
