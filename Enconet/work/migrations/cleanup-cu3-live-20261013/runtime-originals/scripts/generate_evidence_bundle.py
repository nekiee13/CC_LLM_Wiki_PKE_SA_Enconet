#!/usr/bin/env python3
"""Generate one deterministic, validated, run-scoped offline evidence bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path

import build_evaluation_package
import evidence_access_policy
import evidence_resolver
import validate_evidence_bundle


ENCONET = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_MANIFEST = ENCONET / "manifests" / "raw_sources.csv"
GENERATION_TIME_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
COLLECTION_BY_TYPE = {
    "document": "documents",
    "chunk": "chunks",
    "evaluation": "evaluations",
    "crumb": "crumbs",
    "quote": "quotes",
    "gap": "gaps",
    "finding": "findings",
    "action": "actions",
}


class BundleGenerationError(RuntimeError):
    """Raised when a complete valid bundle cannot be built or published."""


def _require_file(path: Path | str, label: str) -> Path:
    resolved = Path(path).resolve()
    if not resolved.is_file():
        raise BundleGenerationError(f"{label} does not exist: {resolved}")
    return resolved


def _database_package_projection(db_path: Path, run_id: str) -> dict:
    """Read the package-owned database rows through a query-only connection."""
    with evidence_resolver._connect_readonly(db_path) as connection:
        run = dict(connection.execute(
            "SELECT * FROM evaluation_runs WHERE run_id=?", (run_id,)
        ).fetchone() or {})
        applicability = [dict(row) for row in connection.execute(
            "SELECT * FROM criterion_applicability WHERE evaluation_run_id=? "
            "ORDER BY criterion_id",
            (run_id,),
        )]
        evaluations = []
        for row in connection.execute(
            "SELECT e.*,c.criterion_name FROM criterion_evaluations AS e "
            "JOIN criteria AS c USING(criterion_id) WHERE evaluation_run_id=? "
            "ORDER BY criterion_id",
            (run_id,),
        ):
            item = dict(row)
            item["classification"] = item.pop("rating")
            item["evidence_ids"] = [value[0] for value in connection.execute(
                "SELECT item_id FROM evaluation_evidence WHERE evaluation_id=? "
                "ORDER BY item_id",
                (item["evaluation_id"],),
            )]
            evaluations.append(item)
        gaps = [dict(row) for row in connection.execute(
            "SELECT g.* FROM gaps AS g JOIN criterion_evaluations AS e "
            "USING(evaluation_id) WHERE e.evaluation_run_id=? ORDER BY gap_id",
            (run_id,),
        )]
        findings = [dict(row) for row in connection.execute(
            "SELECT * FROM findings WHERE evaluation_run_id=? ORDER BY finding_id",
            (run_id,),
        )]
        actions = [dict(row) for row in connection.execute(
            "SELECT * FROM auditor_actions WHERE evaluation_run_id=? ORDER BY action_id",
            (run_id,),
        )]
    return {
        "run": run,
        "applicability": applicability,
        "evaluations": evaluations,
        "gaps": gaps,
        "findings": findings,
        "actions": actions,
    }


def _load_package(path: Path, run_id: str, db_path: Path) -> dict:
    try:
        package = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BundleGenerationError(f"invalid evaluation package: {path}") from exc
    package_errors = build_evaluation_package.validate_package(package)
    if package_errors:
        raise BundleGenerationError(
            "invalid evaluation package: " + "; ".join(package_errors)
        )
    package_run_id = package.get("run", {}).get("run_id")
    if package_run_id != run_id:
        raise BundleGenerationError(
            f"package run mismatch: expected {run_id}, found {package_run_id}"
        )
    try:
        database_projection = _database_package_projection(db_path, run_id)
    except (OSError, sqlite3.Error) as exc:
        raise BundleGenerationError(f"package/database verification failed: {exc}") from exc
    projected_keys = tuple(database_projection)
    if any(package.get(key) != database_projection[key] for key in projected_keys):
        raise BundleGenerationError(
            "package/database mismatch: canonical database projection differs"
        )
    return package


def _lineage_entry(path: Path) -> dict:
    try:
        display_path = path.relative_to(ENCONET).as_posix()
    except ValueError:
        display_path = path.name
    return {
        "path": display_path,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def _ordered_collections(registry: dict) -> dict[str, list[dict]]:
    collections = {name: [] for name in COLLECTION_BY_TYPE.values()}
    for entity in registry["entities"].values():
        collection = COLLECTION_BY_TYPE.get(entity["entity_type"])
        if collection is not None:
            collections[collection].append(dict(entity["data"]))
    order_keys = {
        "documents": lambda row: row["document_id"],
        "chunks": lambda row: (row["document_id"], row["sequence"], row["chunk_id"]),
        "evaluations": lambda row: row["evaluation_id"],
        "crumbs": lambda row: row["crumb_id"],
        "quotes": lambda row: (row["crumb_id"], row["source_order"], row["quote_id"]),
        "gaps": lambda row: row["gap_id"],
        "findings": lambda row: row["finding_id"],
        "actions": lambda row: row["action_id"],
    }
    for name, key in order_keys.items():
        collections[name].sort(key=key)
    return collections


def build_bundle(
    *,
    package_path: Path | str,
    db_path: Path | str,
    run_id: str,
    source_manifest_path: Path | str = DEFAULT_SOURCE_MANIFEST,
    generated_at_utc: str,
) -> dict:
    """Build and validate a bundle in memory without writing any output."""
    if GENERATION_TIME_PATTERN.fullmatch(generated_at_utc) is None:
        raise BundleGenerationError(
            "generated-at-utc must use the exact YYYY-MM-DDTHH:MM:SSZ form"
        )
    try:
        datetime.strptime(generated_at_utc, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise BundleGenerationError("generated-at-utc is not a real UTC timestamp") from exc
    package_file = _require_file(package_path, "package")
    database_file = _require_file(db_path, "database")
    manifest_file = _require_file(source_manifest_path, "source manifest")
    package = _load_package(package_file, run_id, database_file)
    try:
        registry = evidence_resolver.build_entity_registry(
            database_file, run_id, package_path=package_file
        )
    except (OSError, ValueError, evidence_resolver.EvidenceIntegrityError) as exc:
        raise BundleGenerationError(str(exc)) from exc

    bundle = {
        "schema_version": "1.0",
        "metadata": {
            "bundle_id": f"EVIDENCE-BUNDLE-{run_id}",
            "run_id": run_id,
            "supplier": package["run"]["supplier"],
            "framework": "appendix_b",
            "deliverable_language": package["run"]["deliverable_language"],
            "generated_at_utc": generated_at_utc,
            "generation_time_policy": "explicit_utc",
            "ordering_policy": "stable-id-v1",
        },
        "lineage": {
            "package": _lineage_entry(package_file),
            "database": _lineage_entry(database_file),
            "source_manifest": _lineage_entry(manifest_file),
        },
        **_ordered_collections(registry),
    }
    errors = validate_evidence_bundle.validate(bundle)
    if errors:
        raise BundleGenerationError(
            "evidence bundle validation failed: " + "; ".join(errors)
        )
    expected, resolved = evaluation_coverage(bundle)
    if expected != resolved:
        raise BundleGenerationError(
            f"evaluation evidence coverage incomplete: {resolved}/{expected}"
        )
    return bundle


def evaluation_coverage(bundle: dict) -> tuple[int, int]:
    """Return unique evaluation crumb references and how many bundle crumbs resolve."""
    expected_ids = {
        crumb_id
        for evaluation in bundle.get("evaluations", [])
        for crumb_id in evaluation.get("evidence_crumb_ids", [])
    }
    available_ids = {crumb.get("crumb_id") for crumb in bundle.get("crumbs", [])}
    return len(expected_ids), len(expected_ids & available_ids)


def _require_candidate_target(output_path: Path | str, run_id: str) -> Path:
    target = Path(output_path).resolve()
    evidence_access_policy.require_output_target(target)
    expected = evidence_access_policy.candidate_path(run_id, target.name).resolve()
    if target != expected:
        raise evidence_access_policy.PolicyError(
            f"candidate output must be directly under the selected run directory: {expected}"
        )
    return target


def _atomic_write(target: Path, payload: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{target.name}.",
            suffix=".tmp",
            dir=target.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def generate(
    *,
    package_path: Path | str,
    db_path: Path | str,
    run_id: str,
    output_path: Path | str,
    generated_at_utc: str,
    source_manifest_path: Path | str = DEFAULT_SOURCE_MANIFEST,
) -> dict:
    """Validate target and inputs, then atomically publish one candidate bundle."""
    target = _require_candidate_target(output_path, run_id)
    bundle = build_bundle(
        package_path=package_path,
        db_path=db_path,
        run_id=run_id,
        source_manifest_path=source_manifest_path,
        generated_at_utc=generated_at_utc,
    )
    payload = validate_evidence_bundle.canonical_bytes(bundle)
    _atomic_write(target, payload)
    return bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST)
    parser.add_argument("--generated-at-utc", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    bundle = generate(
        package_path=args.package,
        db_path=args.db,
        run_id=args.run_id,
        source_manifest_path=args.source_manifest,
        generated_at_utc=args.generated_at_utc,
        output_path=args.output,
    )
    expected, resolved = evaluation_coverage(bundle)
    bundle_hash = hashlib.sha256(
        validate_evidence_bundle.canonical_bytes(bundle)
    ).hexdigest()
    print(
        f"generate_evidence_bundle: PASS - {args.output} - "
        f"{resolved}/{expected} evaluation crumbs resolved - sha256={bundle_hash}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
