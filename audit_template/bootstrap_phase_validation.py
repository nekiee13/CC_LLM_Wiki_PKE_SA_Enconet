"""Preview or copy the phase-aware validator and criterion checks into one audit.

The bundle carries code, not approved sources, rows, or a validation verdict.
Other child validators remain separate dependencies and fail closed if absent.
"""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core


BUNDLE = Path(__file__).resolve().parent / "phase_validation" / "v1"
MANIFEST = BUNDLE / "manifest.json"
PHASE_VALIDATION = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="phase-aware-validation-runtime",
    roots=frozenset({"scripts"}),
    journal_name="phase-validation-v1",
    lock_name=".phase-validation-bootstrap.lock",
    exact_paths=frozenset({
        "scripts/run_all_validations.py", "scripts/sieving_lib.py",
        "scripts/validate_app_b_json.py", "scripts/validate_requirements.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(PHASE_VALIDATION)


def preview(target: str | Path) -> dict:
    return core.preview(target, PHASE_VALIDATION)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, PHASE_VALIDATION)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, PHASE_VALIDATION)


if __name__ == "__main__":
    raise SystemExit(main())
