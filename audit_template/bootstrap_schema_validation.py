"""Preview or copy neutral schema contracts and their local validator."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "schema_validation" / "v1"
MANIFEST = BUNDLE / "manifest.json"
SCHEMA_VALIDATION = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="schema-contract-validation-runtime",
    roots=frozenset({"schemas", "scripts"}),
    journal_name="schema-validation-v1",
    lock_name=".schema-validation-bootstrap.lock",
    exact_paths=frozenset({
        "schemas/app_b_json_schema.yml", "schemas/dashboard_schema.yml",
        "schemas/evaluation_package_schema.yml", "schemas/scoring_model.yml",
        "scripts/validate_schemas.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(SCHEMA_VALIDATION)


def preview(target: str | Path) -> dict:
    return core.preview(target, SCHEMA_VALIDATION)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, SCHEMA_VALIDATION)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, SCHEMA_VALIDATION)


if __name__ == "__main__":
    raise SystemExit(main())
