"""Preview or install project-local raw-source and chunk validators.

This code-only bundle does not register, promote, or read incoming documents.
"""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "source_validation" / "v1"
MANIFEST = BUNDLE / "manifest.json"
SOURCE_VALIDATION = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="source-validation-runtime-only",
    roots=frozenset({"scripts"}),
    journal_name="source-validation-v1",
    lock_name=".source-validation-bootstrap.lock",
    exact_paths=frozenset({
        "scripts/source_registry.py", "scripts/validate_chunks.py",
        "scripts/validate_raw_sources.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(SOURCE_VALIDATION)


def preview(target: str | Path) -> dict:
    return core.preview(target, SOURCE_VALIDATION)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, SOURCE_VALIDATION)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, SOURCE_VALIDATION)


if __name__ == "__main__":
    raise SystemExit(main())
