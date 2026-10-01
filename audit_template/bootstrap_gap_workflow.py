"""Preview or install project-local gap registration and structural checks."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "gap_workflow" / "v1"
MANIFEST = BUNDLE / "manifest.json"
GAP_WORKFLOW = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="draft-gap-workflow-only",
    roots=frozenset({"scripts"}),
    journal_name="gap-workflow-v1",
    lock_name=".gap-workflow-bootstrap.lock",
    exact_paths=frozenset({"scripts/gap_register.py", "scripts/validate_gaps.py"}),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(GAP_WORKFLOW)


def preview(target: str | Path) -> dict:
    return core.preview(target, GAP_WORKFLOW)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, GAP_WORKFLOW)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, GAP_WORKFLOW)


if __name__ == "__main__":
    raise SystemExit(main())
