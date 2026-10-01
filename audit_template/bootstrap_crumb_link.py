"""Preview or install safe, project-local quote linking for a sieve run."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "crumb_link" / "v1"
MANIFEST = BUNDLE / "manifest.json"
CRUMB_LINK = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="per-run-crumb-link-only",
    roots=frozenset({"scripts"}),
    journal_name="crumb-link-v1",
    lock_name=".crumb-link-bootstrap.lock",
    exact_paths=frozenset({"scripts/link_crumbs.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(CRUMB_LINK)


def preview(target: str | Path) -> dict:
    return core.preview(target, CRUMB_LINK)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, CRUMB_LINK)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, CRUMB_LINK)


if __name__ == "__main__":
    raise SystemExit(main())
