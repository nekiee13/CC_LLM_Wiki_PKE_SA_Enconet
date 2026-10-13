#!/usr/bin/env python3
"""Validate the deterministic EA4.1 review catalog contract."""
from __future__ import annotations

import argparse
import json
import re
from supplier_identity import supplier_label
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCHEMA = PROJECT / "schemas" / "review_catalog.schema.json"
ROOT_FIELDS = {"schema_version", "ordering_policy", "runs"}
ROW_FIELDS = {
    "run_id", "supplier", "framework", "status", "language",
    "generated_at_utc", "artifacts",
}
ARTIFACT_KINDS = {"bundle", "package", "report", "viewer"}
SHA256 = re.compile(r"[0-9a-f]{64}")
RUN_ID = re.compile(r"RUN-[0-9]{8}-[0-9]{2}")
TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


def validate(catalog: object) -> list[str]:
    errors: list[str] = []
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append("unsupported review catalog schema declaration")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"review catalog schema unavailable: {exc}"]
    if not isinstance(catalog, dict):
        return ["catalog must be an object"]
    if set(catalog) != ROOT_FIELDS:
        errors.append("catalog root fields mismatch")
    if catalog.get("schema_version") != "1.0":
        errors.append("unsupported catalog schema_version")
    if catalog.get("ordering_policy") != "run-id-v1":
        errors.append("unsupported catalog ordering_policy")
    rows = catalog.get("runs")
    if not isinstance(rows, list):
        return errors + ["catalog runs must be an array"]
    identifiers: list[str] = []
    for index, row in enumerate(rows):
        prefix = f"runs[{index}]"
        if not isinstance(row, dict) or set(row) != ROW_FIELDS:
            errors.append(f"catalog row fields mismatch: {prefix}")
            continue
        run_id = row.get("run_id")
        if not isinstance(run_id, str) or RUN_ID.fullmatch(run_id) is None:
            errors.append(f"invalid catalog run_id: {prefix}")
        else:
            identifiers.append(run_id)
        if row.get("status") not in {"candidate", "approved"}:
            errors.append(f"invalid catalog status: {prefix}")
        if row.get("language") not in {"en", "sl", "hr"}:
            errors.append(f"invalid catalog language: {prefix}")
        timestamp = row.get("generated_at_utc")
        if not isinstance(timestamp, str) or TIMESTAMP.fullmatch(timestamp) is None:
            errors.append(f"invalid catalog generated_at_utc: {prefix}")
        for field in ("framework",):
            value = row.get(field)
            if not isinstance(value, str) or re.fullmatch(r"[a-z0-9_-]+", value) is None:
                errors.append(f"invalid catalog {field}: {prefix}")
        try:
            supplier_label(row.get("supplier"))
        except ValueError:
            errors.append(f"invalid catalog supplier: {prefix}")
        artifacts = row.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != ARTIFACT_KINDS:
            errors.append(f"catalog artifacts mismatch: {prefix}")
            continue
        for kind in sorted(ARTIFACT_KINDS):
            artifact = artifacts[kind]
            if not isinstance(artifact, dict) or set(artifact) != {"path", "sha256"}:
                errors.append(f"catalog artifact fields mismatch: {prefix}.{kind}")
                continue
            path = artifact.get("path")
            if (not isinstance(path, str) or not path or Path(path).is_absolute()
                    or ".." in Path(path).parts or "\\" in path):
                errors.append(f"invalid artifact path: {prefix}.{kind}")
            digest = artifact.get("sha256")
            if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
                errors.append(f"invalid artifact sha256: {prefix}.{kind}")
    if len(identifiers) != len(set(identifiers)):
        errors.append("duplicate catalog run_id")
    if identifiers != sorted(identifiers):
        errors.append("non-deterministic run order")
    return list(dict.fromkeys(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args(argv)
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        errors = validate(catalog)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"validate_review_catalog: FAIL - {error}", file=sys.stderr)
        return 1
    print(f"validate_review_catalog: PASS - {len(catalog['runs'])} run(s)")
    return 0


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
