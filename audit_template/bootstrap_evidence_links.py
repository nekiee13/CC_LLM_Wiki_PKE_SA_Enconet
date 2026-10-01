"""Preview or install local offline evidence-link helpers and their contract."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "evidence_links" / "v1"
MANIFEST = BUNDLE / "manifest.json"
EVIDENCE_LINKS = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="offline-evidence-links-only",
    roots=frozenset({"schemas", "scripts"}),
    journal_name="evidence-links-v1",
    lock_name=".evidence-links-bootstrap.lock",
    exact_paths=frozenset({
        "schemas/evidence_navigation.yml", "scripts/citation_renderer.py",
        "scripts/evidence_navigation.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(EVIDENCE_LINKS)


def preview(target: str | Path) -> dict:
    return core.preview(target, EVIDENCE_LINKS)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, EVIDENCE_LINKS)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, EVIDENCE_LINKS)


if __name__ == "__main__":
    raise SystemExit(main())
