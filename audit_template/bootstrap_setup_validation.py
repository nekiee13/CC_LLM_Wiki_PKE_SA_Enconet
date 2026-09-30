"""Preview or copy neutral setup structure checks and empty local folders.

This bundle contains no source, criterion, approval, project state, or audit
result. It creates only a header-only validation log and empty wiki markers.
"""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core


BUNDLE = Path(__file__).resolve().parent / "setup_validation" / "v1"
MANIFEST = BUNDLE / "manifest.json"
SETUP_VALIDATION = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="setup-structure-and-empty-validation-log",
    roots=frozenset({".gitattributes", "manifests", "schemas", "scripts", "wiki"}),
    journal_name="setup-validation-v1",
    lock_name=".setup-validation-bootstrap.lock",
    exact_paths=frozenset({
        ".gitattributes", "manifests/validation_runs.csv", "schemas/wiki_structure.yml",
        "scripts/validate_structure.py", "wiki/actions/.gitkeep",
        "wiki/criteria/.gitkeep", "wiki/dashboards/.gitkeep",
        "wiki/evidence/.gitkeep", "wiki/findings/.gitkeep",
        "wiki/gates/.gitkeep",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(SETUP_VALIDATION)


def preview(target: str | Path) -> dict:
    return core.preview(target, SETUP_VALIDATION)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, SETUP_VALIDATION)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, SETUP_VALIDATION)


if __name__ == "__main__":
    raise SystemExit(main())
