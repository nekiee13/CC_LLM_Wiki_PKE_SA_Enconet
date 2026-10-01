"""Preview or install first-write local document chunking."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "chunking" / "v1"
MANIFEST = BUNDLE / "manifest.json"
CHUNKING = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="first-write-document-chunking-only",
    roots=frozenset({"scripts"}),
    journal_name="chunking-v1",
    lock_name=".chunking-bootstrap.lock",
    exact_paths=frozenset({"scripts/chunk_document.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(CHUNKING)


def preview(target: str | Path) -> dict:
    return core.preview(target, CHUNKING)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, CHUNKING)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, CHUNKING)


if __name__ == "__main__":
    raise SystemExit(main())
