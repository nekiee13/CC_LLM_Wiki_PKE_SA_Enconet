"""Preview or copy local evidence validators and empty contracts into one audit.

This bundle adds no real evidence, approval, source document, or audit result.
"""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "evidence_validation" / "v1"
MANIFEST = BUNDLE / "manifest.json"
EVIDENCE_VALIDATION = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="evidence-validation-runtime-only",
    roots=frozenset({"manifests", "schemas", "scripts"}),
    journal_name="evidence-validation-v1",
    lock_name=".evidence-validation-bootstrap.lock",
    exact_paths=frozenset({
        "manifests/link_exceptions.csv", "schemas/page_types.yml",
        "schemas/required_fields.yml", "scripts/validate_frontmatter.py",
        "scripts/validate_traceability.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(EVIDENCE_VALIDATION)


def preview(target: str | Path) -> dict:
    return core.preview(target, EVIDENCE_VALIDATION)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, EVIDENCE_VALIDATION)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, EVIDENCE_VALIDATION)


if __name__ == "__main__":
    raise SystemExit(main())
