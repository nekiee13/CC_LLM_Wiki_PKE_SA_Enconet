"""Preview or install a read-only, company-local evidence matrix builder."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "evidence_matrix" / "v1"
MANIFEST = BUNDLE / "manifest.json"
EVIDENCE_MATRIX = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="read-only-evidence-matrix-only",
    roots=frozenset({"scripts"}),
    journal_name="evidence-matrix-v1",
    lock_name=".evidence-matrix-bootstrap.lock",
    exact_paths=frozenset({"scripts/build_matrix.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(EVIDENCE_MATRIX)


def preview(target: str | Path) -> dict:
    return core.preview(target, EVIDENCE_MATRIX)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, EVIDENCE_MATRIX)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, EVIDENCE_MATRIX)


if __name__ == "__main__":
    raise SystemExit(main())
