#!/usr/bin/env python3
"""Validate the fixed EA6.1 release candidate and unchanged approved baseline."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

import validate_review_package


SHA256 = re.compile(r"[0-9a-f]{64}")


def load_contract(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("candidate contract must be an object")
    return value


def _safe(root: Path, relative: object) -> Path | None:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        return None
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def _hash_error(path: Path | None, expected: object, label: str) -> str | None:
    if path is None:
        return f"unsafe {label} path"
    if not path.is_file():
        return f"missing {label}: {path.name}"
    if not isinstance(expected, str) or SHA256.fullmatch(expected) is None:
        return f"invalid {label} hash"
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        return f"{label} hash mismatch: {path.name}"
    return None


def validate(contract_path: Path, project_root: Path) -> tuple[list[str], dict]:
    errors: list[str] = []
    summary = {"run_id": "unknown", "files": 0, "criteria": 0, "crumbs": 0}
    try:
        contract = load_contract(contract_path)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [f"candidate contract is unreadable: {exc}"], summary
    required = {
        "schema_version", "candidate_id", "status", "run_id", "package_root",
        "package_manifest_sha256", "expected_counts", "source_sha256", "approved_baseline",
    }
    if set(contract) != required:
        errors.append("candidate contract fields mismatch")
    if contract.get("schema_version") != "1.0" or contract.get("status") != "candidate":
        errors.append("invalid candidate contract version or status")
    run_id = contract.get("run_id")
    summary["run_id"] = run_id
    if contract.get("candidate_id") != f"EA6.1-{run_id}":
        errors.append("candidate/run identity mismatch")
    package_root = _safe(project_root, contract.get("package_root"))
    manifest_path = package_root / "package_manifest.json" if package_root else None
    error = _hash_error(manifest_path, contract.get("package_manifest_sha256"), "candidate manifest")
    if error:
        errors.append(error)
    if package_root and package_root.is_dir():
        try:
            package_errors = validate_review_package.validate(package_root)
            errors.extend(f"review package: {item}" for item in package_errors)
            manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
            summary["files"] = len(manifest.get("files", []))
            if manifest.get("run_ids") != [run_id]:
                errors.append("candidate manifest run mismatch")
            bundle = json.loads((package_root / run_id / "evidence_bundle.json").read_text(encoding="utf-8"))
            summary["criteria"] = len(bundle.get("evaluations", []))
            summary["crumbs"] = len(bundle.get("crumbs", []))
            if bundle.get("metadata", {}).get("run_id") != run_id:
                errors.append("candidate bundle run mismatch")
            expected_counts = contract.get("expected_counts", {})
            if summary["criteria"] != expected_counts.get("criteria"):
                errors.append("candidate criterion count mismatch")
            if summary["crumbs"] != expected_counts.get("crumbs"):
                errors.append("candidate crumb count mismatch")
            actual_sources = sorted({row.get("source_sha256") for row in bundle.get("documents", [])})
            if actual_sources != contract.get("source_sha256"):
                errors.append("candidate source lineage mismatch")
        except (OSError, UnicodeError, KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"candidate package is unreadable: {exc}")

    baseline = contract.get("approved_baseline")
    if not isinstance(baseline, dict) or set(baseline) != {
        "report_path", "report_sha256", "dashboard_path", "dashboard_sha256"
    }:
        errors.append("approved baseline fields mismatch")
    else:
        release_manifest = (
            project_root / "outputs" / f"evidence_access_release_manifest_{run_id}.json"
        )
        released_hashes: dict[str, object] | None = None
        if release_manifest.is_file():
            try:
                release = json.loads(release_manifest.read_text(encoding="utf-8"))
                if (
                    release.get("release_id") != f"EA6.4-{run_id}"
                    or release.get("status") != "promoted"
                    or release.get("candidate_manifest_sha256")
                    != contract.get("package_manifest_sha256")
                ):
                    errors.append("promoted release manifest identity mismatch")
                released_hashes = {
                    row.get("path"): row.get("sha256")
                    for row in release.get("artifacts", []) if isinstance(row, dict)
                }
            except (OSError, UnicodeError, AttributeError, json.JSONDecodeError) as exc:
                errors.append(f"promoted release manifest is unreadable: {exc}")
        for role in ("report", "dashboard"):
            path = _safe(project_root, baseline[f"{role}_path"])
            expected = baseline[f"{role}_sha256"]
            if released_hashes is not None and path is not None:
                relative = path.relative_to(project_root.resolve()).as_posix()
                expected = released_hashes.get(relative)
            error = _hash_error(
                path, expected, f"approved {role}",
            )
            if error:
                errors.append(error)
    return list(dict.fromkeys(errors)), summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args(argv)
    errors, summary = validate(args.contract, args.project_root)
    if errors:
        for error in errors:
            print(f"validate_evidence_access_candidate: FAIL - {error}", file=sys.stderr)
        return 1
    print(
        "validate_evidence_access_candidate: PASS - "
        f"run={summary['run_id']} files={summary['files']} "
        f"criteria={summary['criteria']} crumbs={summary['crumbs']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
