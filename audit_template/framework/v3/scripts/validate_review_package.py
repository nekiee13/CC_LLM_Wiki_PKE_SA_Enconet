#!/usr/bin/env python3
"""Validate a relocated offline evidence review package and its manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import validate_report_links
import validate_review_catalog
import validate_review_workspace


PROJECT = Path(__file__).resolve().parents[1]
SCHEMA = PROJECT / "schemas" / "review_package_manifest.schema.json"
ROLES = {"catalog", "workspace", "bundle", "package", "report", "viewer"}
SHA256 = re.compile(r"[0-9a-f]{64}")
PACKAGE_ID = re.compile(r"REVIEW-PACKAGE-(?:RUN-[0-9]{8}-[0-9]{2}|MULTI-[0-9a-f]{12})")


def _manifest_errors(manifest: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["package manifest must be an object"]
    required = {"schema_version", "package_id", "run_ids", "entrypoint", "ordering_policy", "files"}
    if set(manifest) != required:
        errors.append("package manifest fields mismatch")
    if manifest.get("schema_version") != "1.0":
        errors.append("unsupported package manifest schema_version")
    package_id = manifest.get("package_id")
    if not isinstance(package_id, str) or PACKAGE_ID.fullmatch(package_id) is None:
        errors.append("invalid package_id")
    if manifest.get("entrypoint") != "review_workspace.html":
        errors.append("invalid package entrypoint")
    if manifest.get("ordering_policy") != "path-v1":
        errors.append("invalid package ordering_policy")
    run_ids = manifest.get("run_ids")
    if (not isinstance(run_ids, list) or not run_ids or run_ids != sorted(set(run_ids))
            or any(not isinstance(value, str) or re.fullmatch(r"RUN-[0-9]{8}-[0-9]{2}", value) is None for value in run_ids)):
        errors.append("invalid package run_ids")
    files = manifest.get("files")
    if not isinstance(files, list):
        return errors + ["package manifest files must be an array"]
    paths = []
    for index, row in enumerate(files):
        if not isinstance(row, dict) or set(row) != {"path", "role", "run_id", "sha256"}:
            errors.append(f"manifest file fields mismatch: files[{index}]")
            continue
        path = row.get("path")
        if (not isinstance(path, str) or not path or Path(path).is_absolute()
                or ".." in Path(path).parts or "\\" in path):
            errors.append(f"invalid manifest path: files[{index}]")
        else:
            paths.append(path)
        if row.get("role") not in ROLES:
            errors.append(f"invalid manifest role: files[{index}]")
        if row.get("run_id") is not None and row.get("run_id") not in (run_ids or []):
            errors.append(f"invalid manifest run reference: files[{index}]")
        digest = row.get("sha256")
        if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
            errors.append(f"invalid manifest sha256: files[{index}]")
    if paths != sorted(paths):
        errors.append("non-deterministic manifest file order")
    if len(paths) != len(set(paths)):
        errors.append("duplicate manifest file path")
    return errors


def validate(package_root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = package_root / "package_manifest.json"
    if not manifest_path.is_file():
        return ["missing package manifest: package_manifest.json"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"package manifest is unreadable: {exc}"]
    errors.extend(_manifest_errors(manifest))
    files = manifest.get("files", []) if isinstance(manifest, dict) else []
    declared = {row.get("path") for row in files if isinstance(row, dict) and isinstance(row.get("path"), str)}
    for row in files:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            continue
        relative = row["path"]
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts or "\\" in relative:
            continue
        path = package_root / relative_path
        if not path.is_file():
            errors.append(f"missing manifest file: {relative}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != row.get("sha256"):
            errors.append(f"manifest hash mismatch: {relative}")
    actual_files = {
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*") if path.is_file()
    } - {"package_manifest.json"}
    for relative in sorted(actual_files - declared):
        errors.append(f"unlisted package file: {relative}")
    if errors:
        return list(dict.fromkeys(errors))
    by_role_run = {(row["role"], row["run_id"]): package_root / row["path"] for row in files}
    catalog_path = by_role_run[("catalog", None)]
    workspace_path = by_role_run[("workspace", None)]
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    errors.extend(validate_review_catalog.validate(catalog))
    errors.extend(validate_review_workspace.validate(
        catalog, workspace_path.read_text(encoding="utf-8")
    ))
    if [row["run_id"] for row in catalog.get("runs", [])] != manifest["run_ids"]:
        errors.append("manifest/catalog run mismatch")
    for run_id in manifest["run_ids"]:
        report = by_role_run.get(("report", run_id))
        viewer = by_role_run.get(("viewer", run_id))
        package = by_role_run.get(("package", run_id))
        bundle = by_role_run.get(("bundle", run_id))
        if any(path is None for path in (report, viewer, package, bundle)):
            errors.append(f"incomplete run artifact roles: {run_id}")
            continue
        errors.extend(validate_report_links.validate_paths(
            report, viewer, package, project_root=package_root, verify_lineage=False
        ))
        row = next(item for item in catalog["runs"] if item["run_id"] == run_id)
        for role, path in (("report", report), ("viewer", viewer), ("package", package), ("bundle", bundle)):
            relative = path.relative_to(package_root).as_posix()
            if row["artifacts"][role]["path"] != relative:
                errors.append(f"catalog artifact path mismatch: {run_id}/{role}")
            if row["artifacts"][role]["sha256"] != hashlib.sha256(path.read_bytes()).hexdigest():
                errors.append(f"catalog artifact hash mismatch: {run_id}/{role}")
    return list(dict.fromkeys(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_root", type=Path)
    args = parser.parse_args(argv)
    try:
        errors = validate(args.package_root)
    except Exception as exc:  # noqa: BLE001 - portable package boundary fails closed
        errors = [f"package validation failed: {exc}"]
    if errors:
        for error in errors:
            print(f"validate_review_package: FAIL - {error}", file=sys.stderr)
        return 1
    manifest = json.loads((args.package_root / "package_manifest.json").read_text(encoding="utf-8"))
    print(
        "validate_review_package: PASS - "
        f"files={len(manifest['files'])} runs={len(manifest['run_ids'])} - {args.package_root}"
    )
    return 0


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
