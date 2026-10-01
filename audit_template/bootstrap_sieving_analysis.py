"""Preview or install project-local sieve metrics and generation diffs."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "sieving_analysis" / "v1"
MANIFEST = BUNDLE / "manifest.json"
SIEVING_ANALYSIS = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="sieving-metrics-and-diff-only",
    roots=frozenset({"scripts"}),
    journal_name="sieving-analysis-v1",
    lock_name=".sieving-analysis-bootstrap.lock",
    exact_paths=frozenset({"scripts/sieve_diff.py", "scripts/sieve_metrics.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(SIEVING_ANALYSIS)


def preview(target: str | Path) -> dict:
    return core.preview(target, SIEVING_ANALYSIS)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, SIEVING_ANALYSIS)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, SIEVING_ANALYSIS)


if __name__ == "__main__":
    raise SystemExit(main())
