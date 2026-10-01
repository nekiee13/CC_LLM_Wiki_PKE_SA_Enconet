"""Preview or install guarded local golden-set scoring and an empty approval ledger."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "sieving_score" / "v1"
MANIFEST = BUNDLE / "manifest.json"
SIEVING_SCORE = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="sieving-score-and-empty-approvals-only",
    roots=frozenset({"manifests", "scripts"}),
    journal_name="sieving-score-v1",
    lock_name=".sieving-score-bootstrap.lock",
    exact_paths=frozenset({"manifests/approvals.csv", "scripts/score_sieving.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(SIEVING_SCORE)


def preview(target: str | Path) -> dict:
    return core.preview(target, SIEVING_SCORE)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, SIEVING_SCORE)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, SIEVING_SCORE)


if __name__ == "__main__":
    raise SystemExit(main())
