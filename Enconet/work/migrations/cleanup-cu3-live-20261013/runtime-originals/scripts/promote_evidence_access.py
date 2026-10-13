#!/usr/bin/env python3
"""Human-gated, rollback-safe promotion of the offline Evidence Explorer."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import yaml

import validate_evidence_access_candidate
import validate_evidence_access_review_packet
import validate_evidence_access_uat
import evidence_access_policy
import validate_report_links
import validate_review_package


ENCONET = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ENCONET / "schemas" / "evidence_access_promotion.yml"
DEFAULT_APPROVALS = ENCONET / "manifests" / "approvals.csv"
SHA256 = re.compile(r"[0-9a-f]{64}")


class PromotionError(RuntimeError):
    """Raised when promotion cannot prove a complete controlled replacement."""


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_path(root: Path, relative: object, label: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise PromotionError(f"unsafe {label} path: {relative}")
    root = root.resolve()
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise PromotionError(f"unsafe {label} path: {relative}") from exc
    return path


def _load_contract(path: Path) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise PromotionError(f"promotion contract is unreadable: {exc}") from exc
    if not isinstance(value, dict):
        raise PromotionError("promotion contract must be an object")
    required = {
        "schema_version", "release_id", "status", "run_id", "candidate_manifest",
        "required_approvals", "independent_review", "promotion", "baseline",
        "post_validation", "result_manifest",
    }
    if set(value) != required or value.get("schema_version") != "1.0":
        raise PromotionError("promotion contract fields or schema version mismatch")
    if value.get("status") != "awaiting_owner_promotion":
        raise PromotionError("promotion contract is not awaiting Owner promotion")
    if not re.fullmatch(r"EA6\.4-RUN-[0-9]{8}-[0-9]{2}", str(value.get("release_id"))):
        raise PromotionError("invalid release identity")
    return value


def _approved_rows(path: Path) -> dict[str, dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise PromotionError(f"approval manifest is unreadable: {exc}") from exc
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row.get("object_id", ""), []).append(row)
    result: dict[str, dict[str, str]] = {}
    for object_id, matches in grouped.items():
        signatures = {(row.get("decision"), row.get("date"), row.get("reviewer")) for row in matches}
        if len(signatures) != 1:
            raise PromotionError(f"conflicting approval records for {object_id}")
        result[object_id] = matches[-1]
    return result


def _require_approvals(contract: dict, approvals: Path) -> None:
    configured = contract.get("required_approvals")
    if not isinstance(configured, dict) or set(configured) != {"report", "dashboard"}:
        raise PromotionError("promotion requires report and dashboard approval references")
    rows = _approved_rows(approvals)
    for role, prefix in (("report", "G5-"), ("dashboard", "G6-")):
        decision_ref = configured.get(role)
        if not isinstance(decision_ref, str) or not decision_ref.startswith(prefix):
            raise PromotionError(f"invalid {role} approval reference")
        row = rows.get(decision_ref)
        if not row:
            raise PromotionError(f"missing Owner approval: {decision_ref}")
        if row.get("decision") != "approved" or not row.get("date") or not row.get("reviewer"):
            raise PromotionError(f"Owner approval is not signed and approved: {decision_ref}")


def _hash_row(root: Path, row: object, label: str, path_key: str = "path") -> tuple[Path, str]:
    if not isinstance(row, dict) or set(row) != {path_key, "sha256"}:
        raise PromotionError(f"invalid {label} hash contract")
    path = _safe_path(root, row[path_key], label)
    expected = row.get("sha256")
    if not isinstance(expected, str) or SHA256.fullmatch(expected) is None:
        raise PromotionError(f"invalid {label} SHA-256")
    if not path.is_file():
        raise PromotionError(f"missing {label}: {path}")
    actual = _digest(path)
    if actual != expected:
        raise PromotionError(f"{label} hash mismatch: {path}; expected {expected}, got {actual}")
    return path, expected


def _promotion_rows(contract: dict, root: Path) -> list[tuple[Path, Path, str]]:
    rows = contract.get("promotion")
    if not isinstance(rows, list) or not rows:
        raise PromotionError("promotion set is empty")
    result: list[tuple[Path, Path, str]] = []
    destinations: set[Path] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"source", "destination", "sha256"}:
            raise PromotionError(f"invalid promotion row {index}")
        source = _safe_path(root, row["source"], f"promotion source {index}")
        destination = _safe_path(root, row["destination"], f"promotion destination {index}")
        expected = row.get("sha256")
        if destination in destinations:
            raise PromotionError(f"duplicate promotion destination: {destination}")
        destinations.add(destination)
        if not isinstance(expected, str) or SHA256.fullmatch(expected) is None:
            raise PromotionError(f"invalid promotion SHA-256 at row {index}")
        if not source.is_file() or _digest(source) != expected:
            raise PromotionError(f"candidate hash mismatch: {source}")
        if root == ENCONET.resolve():
            try:
                source.relative_to(evidence_access_policy.CANDIDATE_ROOT.resolve())
            except ValueError as exc:
                raise PromotionError(f"source is outside the controlled candidate root: {source}") from exc
            relative_destination = destination.relative_to(root).as_posix()
            if relative_destination not in evidence_access_policy.APPROVED_ARTIFACT_SHA256:
                raise PromotionError(f"destination is not a protected approved artifact: {destination}")
        result.append((source, destination, expected))
    return result


def _verify_baseline(contract: dict, root: Path, destinations: set[Path]) -> None:
    rows = contract.get("baseline")
    if not isinstance(rows, list) or len(rows) != len(destinations):
        raise PromotionError("baseline must cover every promotion destination")
    covered: set[Path] = set()
    for index, row in enumerate(rows):
        path, _expected = _hash_row(root, row, f"baseline {index}")
        covered.add(path)
    if covered != destinations:
        raise PromotionError("baseline paths do not exactly match promotion destinations")


def _command_errors(command: list[str], root: Path, label: str) -> list[str]:
    result = subprocess.run(
        command, cwd=root, capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=False,
    )
    if result.returncode == 0:
        return []
    detail = (result.stdout + result.stderr).strip().splitlines()
    return [f"{label} exited {result.returncode}: {detail[-1] if detail else 'no output'}"]


def validate_release_evidence(contract: dict, root: Path) -> list[str]:
    """Validate the approved candidate, UAT, review, package, and aggregate."""
    errors: list[str] = []
    candidate_contract = root / "schemas" / "evidence_access_release_candidate.yml"
    uat_contract = root / "schemas" / "evidence_access_uat.yml"
    uat_packet = root / "docs" / "acceptance" / "EA5.4_OWNER_UAT.md"
    review_contract = root / "schemas" / "evidence_access_review_protocol.yml"
    review_packet = root / "docs" / "reviews" / "EA6.3_CLAUDE_REVIEW_PACKET.md"
    checks = (
        validate_evidence_access_candidate.validate(candidate_contract, root)[0],
        validate_evidence_access_uat.validate(uat_contract, uat_packet, root)[0],
        validate_evidence_access_review_packet.validate(review_contract, review_packet, root)[0],
    )
    for label, check_errors in zip(("candidate", "UAT", "review"), checks):
        errors.extend(f"{label}: {error}" for error in check_errors)
    try:
        review = yaml.safe_load(review_contract.read_text(encoding="utf-8"))
        recorded_review = review.get("review_decision", {}).get("message_id")
        if contract.get("independent_review") != recorded_review:
            errors.append("independent review identity does not match the approved review protocol")
    except (OSError, UnicodeError, AttributeError, yaml.YAMLError) as exc:
        errors.append(f"independent review identity is unreadable: {exc}")
    package_root = _safe_path(root, contract["candidate_manifest"]["path"], "candidate manifest").parent
    errors.extend(f"portable package: {error}" for error in validate_review_package.validate(package_root))
    if errors:
        return errors
    return _command_errors(
        [sys.executable, str(root / "scripts" / "audit_command.py"),
         "audit-validate", "--", "--no-record"],
        root, "aggregate validation",
    )


def validate_published_release(contract: dict, root: Path) -> list[str]:
    """Validate final sibling links, browser behavior, portability, and aggregate state."""
    post = contract.get("post_validation")
    if not isinstance(post, dict) or set(post) != {"report", "viewer", "package"}:
        return ["post_validation paths are invalid"]
    report = _safe_path(root, post["report"], "published report")
    viewer = _safe_path(root, post["viewer"], "published viewer")
    package = _safe_path(root, post["package"], "evaluation package")
    errors = validate_report_links.validate_paths(report, viewer, package, project_root=root)
    package_root = _safe_path(root, contract["candidate_manifest"]["path"], "candidate manifest").parent
    errors.extend(f"portable package: {error}" for error in validate_review_package.validate(package_root))
    if errors:
        return errors
    with tempfile.TemporaryDirectory(prefix="ea6-4-browser-") as temp:
        errors.extend(_command_errors(
            [sys.executable, str(root / "scripts" / "browser_harness.py"), "check",
             str(viewer), "--artifacts", temp, "--require-interactive"],
            root, "published browser validation",
        ))
    errors.extend(_command_errors(
        [sys.executable, str(root / "scripts" / "audit_command.py"),
         "audit-validate", "--", "--no-record"],
        root, "post-promotion aggregate validation",
    ))
    if errors:
        return errors
    with tempfile.TemporaryDirectory(prefix="ea6-4-tests-") as temp:
        errors.extend(_command_errors(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
             "--basetemp", str(Path(temp) / "root")],
            root, "post-promotion project tests",
        ))
        errors.extend(_command_errors(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
             "--basetemp", str(Path(temp) / "sieving")],
            root / "sieving", "post-promotion sieving tests",
        ))
    return errors


def promote(
    contract_path: Path,
    *,
    project_root: Path = ENCONET,
    approvals: Path = DEFAULT_APPROVALS,
    pre_validator: Callable[[dict, Path], list[str]] = validate_release_evidence,
    post_validator: Callable[[dict, Path], list[str]] = validate_published_release,
    replace: Callable[[Path, Path], None] = os.replace,
) -> dict:
    """Promote the fixed set, rolling all replaced artifacts back on any handled failure."""
    root = project_root.resolve()
    contract = _load_contract(contract_path)
    _require_approvals(contract, approvals)
    _hash_row(root, contract.get("candidate_manifest"), "candidate manifest")
    rows = _promotion_rows(contract, root)
    _verify_baseline(contract, root, {destination for _source, destination, _hash in rows})
    result_path = _safe_path(root, contract.get("result_manifest"), "result manifest")
    if result_path.exists():
        raise PromotionError(f"release result already exists: {result_path}")
    pre_errors = pre_validator(contract, root)
    if pre_errors:
        raise PromotionError("pre-promotion validation failed: " + "; ".join(pre_errors))
    # Close the validation/write race: approvals and every pinned byte must still
    # match immediately before staging begins.
    _require_approvals(contract, approvals)
    _hash_row(root, contract.get("candidate_manifest"), "candidate manifest")
    rows = _promotion_rows(contract, root)
    _verify_baseline(contract, root, {destination for _source, destination, _hash in rows})

    transaction = root / ".tmp" / f"promotion-{contract['release_id']}"
    if transaction.exists():
        raise PromotionError(f"unfinished promotion transaction requires recovery: {transaction}")
    transaction.mkdir(parents=True)
    backups = transaction / "backups"
    staged = transaction / "staged"
    backups.mkdir()
    staged.mkdir()
    replaced: list[tuple[Path, Path]] = []
    preserve_transaction = False
    try:
        prepared: list[tuple[Path, Path, Path, str]] = []
        for index, (source, destination, expected) in enumerate(rows):
            backup = backups / f"{index}.bak"
            stage = staged / f"{index}.new"
            shutil.copy2(destination, backup)
            shutil.copy2(source, stage)
            if _digest(stage) != expected:
                raise PromotionError(f"staged candidate hash mismatch: {source}")
            prepared.append((stage, destination, backup, expected))
        for stage, destination, backup, _expected in prepared:
            replace(stage, destination)
            replaced.append((destination, backup))
        result = {
            "schema_version": "1.0",
            "release_id": contract["release_id"],
            "status": "promoted",
            "promoted_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "owner_approval_refs": contract["required_approvals"],
            "independent_review": contract["independent_review"],
            "candidate_manifest_sha256": contract["candidate_manifest"]["sha256"],
            "artifacts": [
                {"path": destination.relative_to(root).as_posix(), "sha256": _digest(destination)}
                for _source, destination, _expected in rows
            ],
        }
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_temp = transaction / "release_manifest.json"
        result_temp.write_text(
            json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8", newline="",
        )
        replace(result_temp, result_path)
        post_errors = post_validator(contract, root)
        if post_errors:
            raise PromotionError("post-promotion validation failed: " + "; ".join(post_errors))
        return result
    except Exception as exc:
        rollback_errors: list[str] = []
        for destination, backup in reversed(replaced):
            try:
                os.replace(backup, destination)
            except OSError as rollback_exc:
                rollback_errors.append(f"{destination}: {rollback_exc}")
        if result_path.exists():
            try:
                result_path.unlink()
            except OSError as rollback_exc:
                rollback_errors.append(f"{result_path}: {rollback_exc}")
        if rollback_errors:
            preserve_transaction = True
            raise PromotionError(
                f"promotion failed and rollback needs recovery at {transaction}: "
                + "; ".join(rollback_errors)
            ) from exc
        raise PromotionError(f"promotion failed and was rolled back: {exc}") from exc
    finally:
        if not preserve_transaction:
            try:
                shutil.rmtree(transaction)
            except OSError:
                pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--project-root", type=Path, default=ENCONET)
    parser.add_argument("--approvals", type=Path, default=DEFAULT_APPROVALS)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    if not args.execute:
        print("STOP: --execute plus signed G5/G6 Owner approvals are required; no files changed")
        return 2
    try:
        result = promote(
            args.contract, project_root=args.project_root, approvals=args.approvals,
        )
    except (OSError, PromotionError, yaml.YAMLError) as exc:
        print(f"promote_evidence_access: FAIL - {exc}", file=sys.stderr)
        return 1
    print(
        f"promote_evidence_access: PASS - release={result['release_id']} "
        f"artifacts={len(result['artifacts'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
