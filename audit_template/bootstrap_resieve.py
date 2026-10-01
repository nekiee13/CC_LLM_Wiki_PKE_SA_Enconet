"""Preview or install a local, guarded measured-resieve command."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "resieve" / "v1"
MANIFEST = BUNDLE / "manifest.json"
RESIEVE = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="measured-resieve-only",
    roots=frozenset({"scripts"}),
    journal_name="resieve-v1",
    lock_name=".resieve-bootstrap.lock",
    exact_paths=frozenset({"scripts/resieve_run.py", "scripts/sieve_run.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(RESIEVE)


def preview(target: str | Path) -> dict:
    return core.preview(target, RESIEVE)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, RESIEVE)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, RESIEVE)


if __name__ == "__main__":
    raise SystemExit(main())
