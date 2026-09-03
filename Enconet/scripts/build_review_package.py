#!/usr/bin/env python3
"""Build a deterministic, relocatable offline evidence review package."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import generate_report
import generate_review_catalog
import generate_review_workspace
import validate_review_catalog


ENCONET = Path(__file__).resolve().parents[1]
CATALOG = ENCONET / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"
OUTPUT = ENCONET / "outputs" / "candidates" / "evidence_access" / "portable_package"
NAMES = {
    "bundle": "evidence_bundle.json",
    "package": "evaluation_package.json",
    "report": "evaluation_report.md",
    "viewer": "evidence_explorer.html",
}


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source(root: Path, relative: str) -> Path:
    root = root.resolve()
    path = (root / Path(relative)).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"catalog artifact escapes source root: {relative}") from exc
    if not path.is_file():
        raise ValueError(f"catalog artifact is missing: {relative}")
    return path


def _package_id(run_ids: list[str]) -> str:
    if len(run_ids) == 1:
        return f"REVIEW-PACKAGE-{run_ids[0]}"
    digest = hashlib.sha256("\n".join(run_ids).encode("ascii")).hexdigest()[:12]
    return f"REVIEW-PACKAGE-MULTI-{digest}"


def build(catalog: dict, source_root: Path, destination: Path) -> Path:
    """Build into a new empty directory and return its manifest path."""
    errors = validate_review_catalog.validate(catalog)
    if errors:
        raise ValueError("invalid source review catalog: " + errors[0])
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"destination must be absent or empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    portable_rows = []
    manifest_files: list[dict] = []
    for row in catalog["runs"]:
        run_id = row["run_id"]
        run_dir = destination / run_id
        run_dir.mkdir()
        source_paths = {
            kind: _source(source_root, row["artifacts"][kind]["path"])
            for kind in NAMES
        }
        targets = {kind: run_dir / name for kind, name in NAMES.items()}
        for kind in ("bundle", "package", "viewer"):
            shutil.copyfile(source_paths[kind], targets[kind])
        package = json.loads(targets["package"].read_text(encoding="utf-8"))
        report = generate_report.render(package, viewer_path=NAMES["viewer"])
        targets["report"].write_text(report, encoding="utf-8", newline="\n")
        artifacts = {}
        for kind in sorted(NAMES):
            relative = targets[kind].relative_to(destination).as_posix()
            digest = _hash(targets[kind])
            artifacts[kind] = {"path": relative, "sha256": digest}
            manifest_files.append({
                "path": relative, "role": kind, "run_id": run_id, "sha256": digest,
            })
        portable_rows.append({**row, "artifacts": artifacts})
    portable_catalog = {
        "schema_version": "1.0", "ordering_policy": "run-id-v1",
        "runs": portable_rows,
    }
    catalog_path = destination / "review_catalog.json"
    catalog_path.write_bytes(generate_review_catalog.canonical_bytes(portable_catalog))
    workspace_path = destination / "review_workspace.html"
    workspace_path.write_text(
        generate_review_workspace.render(
            portable_catalog, output_path=workspace_path, project_root=destination
        ),
        encoding="utf-8", newline="\n",
    )
    manifest_files.extend([
        {"path": "review_catalog.json", "role": "catalog", "run_id": None,
         "sha256": _hash(catalog_path)},
        {"path": "review_workspace.html", "role": "workspace", "run_id": None,
         "sha256": _hash(workspace_path)},
    ])
    manifest_files.sort(key=lambda item: item["path"])
    run_ids = [row["run_id"] for row in portable_rows]
    manifest = {
        "schema_version": "1.0", "package_id": _package_id(run_ids),
        "run_ids": run_ids, "entrypoint": "review_workspace.html",
        "ordering_policy": "path-v1", "files": manifest_files,
    }
    manifest_path = destination / "package_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8", newline="\n",
    )
    from validate_review_package import validate
    validation_errors = validate(destination)
    if validation_errors:
        raise ValueError("built package failed validation: " + validation_errors[0])
    return manifest_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--source-root", type=Path, default=ENCONET)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        manifest = build(catalog, args.source_root, args.output)
        print(f"build_review_package: PASS - {manifest}")
        return 0
    except Exception as exc:  # noqa: BLE001 - package boundary fails closed
        print(f"build_review_package: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
