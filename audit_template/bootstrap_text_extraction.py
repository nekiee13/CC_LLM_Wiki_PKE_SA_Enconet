"""Preview or install first-write local plain-text extraction."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "text_extraction" / "v1"
MANIFEST = BUNDLE / "manifest.json"
TEXT_EXTRACTION = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="registered-plain-text-extraction-only",
    roots=frozenset({"scripts"}),
    journal_name="text-extraction-v1",
    lock_name=".text-extraction-bootstrap.lock",
    exact_paths=frozenset({"scripts/extract_text.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(TEXT_EXTRACTION)


def preview(target: str | Path) -> dict:
    return core.preview(target, TEXT_EXTRACTION)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, TEXT_EXTRACTION)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, TEXT_EXTRACTION)


if __name__ == "__main__":
    raise SystemExit(main())
