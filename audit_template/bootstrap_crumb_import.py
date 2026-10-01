"""Preview or install strict, project-local sieve crumb import."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "crumb_import" / "v1"
MANIFEST = BUNDLE / "manifest.json"
CRUMB_IMPORT = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="strict-crumb-import-only",
    roots=frozenset({"scripts"}),
    journal_name="crumb-import-v1",
    lock_name=".crumb-import-bootstrap.lock",
    exact_paths=frozenset({"scripts/import_crumbs.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(CRUMB_IMPORT)


def preview(target: str | Path) -> dict:
    return core.preview(target, CRUMB_IMPORT)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, CRUMB_IMPORT)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, CRUMB_IMPORT)


if __name__ == "__main__":
    raise SystemExit(main())
