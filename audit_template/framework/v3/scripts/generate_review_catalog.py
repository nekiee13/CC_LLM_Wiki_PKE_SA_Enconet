#!/usr/bin/env python3
"""Build a deterministic catalog from explicitly registered, validated review packages."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Callable

import yaml

import validate_evidence_bundle
import validate_report_links
import validate_review_catalog


PROJECT = Path(__file__).resolve().parents[1]
REGISTRY = PROJECT / "schemas" / "review_packages.yml"
OUTPUT = PROJECT / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"
ARTIFACT_KINDS = ("bundle", "package", "report", "viewer")
ENTRY_FIELDS = {
    "run_id", "status",
    *(field for kind in ARTIFACT_KINDS for field in (kind, f"{kind}_sha256")),
}


def canonical_bytes(catalog: dict) -> bytes:
    return (
        json.dumps(catalog, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _safe_path(root: Path, relative: object, kind: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError(f"{kind} artifact path must be a relative POSIX path")
    root = root.resolve()
    target = (root / Path(relative)).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{kind} artifact path escapes project root: {relative}") from exc
    return target


def _verified_artifact(entry: dict, kind: str, root: Path) -> dict:
    relative = entry.get(kind)
    target = _safe_path(root, relative, kind)
    if not target.is_file():
        raise ValueError(f"{kind} artifact is missing: {target}")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    expected = entry.get(f"{kind}_sha256")
    if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
        raise ValueError(f"{kind} registered sha256 is missing or invalid")
    if digest != expected:
        raise ValueError(
            f"{kind} artifact hash mismatch: {target}; expected {expected}, got {digest}"
        )
    return {"path": str(relative), "sha256": digest}


def validate_entry(entry: dict, root: Path) -> dict:
    """Validate one registered artifact quartet and return its catalog row."""
    if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
        raise ValueError("registered package fields mismatch")
    run_id = entry.get("run_id")
    if not isinstance(run_id, str) or re.fullmatch(r"RUN-[0-9]{8}-[0-9]{2}", run_id) is None:
        raise ValueError(f"invalid registered run_id: {run_id}")
    if entry.get("status") not in {"candidate", "approved"}:
        raise ValueError(f"invalid registered status: {entry.get('status')}")
    artifacts = {
        kind: _verified_artifact(entry, kind, root) for kind in ARTIFACT_KINDS
    }
    paths = {kind: _safe_path(root, entry[kind], kind) for kind in ARTIFACT_KINDS}
    link_errors = validate_report_links.validate_paths(
        paths["report"], paths["viewer"], paths["package"], project_root=root
    )
    if link_errors:
        raise ValueError("registered review package failed validation: " + link_errors[0])
    try:
        package = json.loads(paths["package"].read_text(encoding="utf-8"))
        bundle = json.loads(paths["bundle"].read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"registered review package JSON is unreadable: {exc}") from exc
    bundle_errors = validate_evidence_bundle.validate(bundle)
    if bundle_errors:
        raise ValueError("registered evidence bundle is invalid: " + bundle_errors[0])
    embedded_errors: list[str] = []
    embedded = validate_report_links._extract_bundle(
        paths["viewer"].read_text(encoding="utf-8"), paths["viewer"], embedded_errors
    )
    if embedded_errors or embedded is None:
        raise ValueError("registered viewer bundle is invalid: " + embedded_errors[0])
    if validate_evidence_bundle.canonical_bytes(bundle) != validate_evidence_bundle.canonical_bytes(embedded):
        raise ValueError("standalone and embedded evidence bundles differ")
    metadata = bundle["metadata"]
    package_run = package.get("run", {})
    if metadata.get("run_id") != run_id or package_run.get("run_id") != run_id:
        raise ValueError(f"registered run mismatch: {run_id}")
    return {
        "run_id": run_id,
        "supplier": metadata["supplier"],
        "framework": metadata["framework"],
        "status": entry["status"],
        "language": metadata["deliverable_language"],
        "generated_at_utc": metadata["generated_at_utc"],
        "artifacts": artifacts,
    }


def build_catalog(
    packages: list[dict],
    root: Path,
    *,
    validator: Callable[[dict, Path], dict] = validate_entry,
) -> dict:
    """Build only from explicit registry rows; never enumerate the output directory."""
    if not isinstance(packages, list):
        raise ValueError("registered packages must be a list")
    identifiers = [row.get("run_id") for row in packages if isinstance(row, dict)]
    if len(identifiers) != len(packages) or len(identifiers) != len(set(identifiers)):
        raise ValueError("duplicate registered run_id")
    rows = [validator(row, root) for row in packages]
    rows.sort(key=lambda row: row["run_id"])
    catalog = {
        "schema_version": "1.0", "ordering_policy": "run-id-v1", "runs": rows,
    }
    errors = validate_review_catalog.validate(catalog)
    if errors:
        raise ValueError("generated review catalog is invalid: " + errors[0])
    return catalog


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix=f".{path.name}.", suffix=".tmp", dir=path.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--project-root", type=Path, default=PROJECT)
    args = parser.parse_args(argv)
    try:
        registry = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
        if not isinstance(registry, dict) or set(registry) != {"schema_version", "packages"}:
            raise ValueError("review package registry fields mismatch")
        if registry["schema_version"] != "1.0":
            raise ValueError("unsupported review package registry schema_version")
        catalog = build_catalog(registry["packages"], args.project_root)
        _atomic_write(args.output, canonical_bytes(catalog))
        print(f"generate_review_catalog: PASS - {len(catalog['runs'])} run(s) - {args.output}")
        return 0
    except Exception as exc:  # noqa: BLE001 - controlled generation boundary
        print(f"generate_review_catalog: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
