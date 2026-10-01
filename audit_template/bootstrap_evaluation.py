"""Preview or install the project-local, approval-gated evaluation bundle."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "evaluation" / "v1"
MANIFEST = BUNDLE / "manifest.json"
EVALUATION = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="approval-gated-evaluation-workflow-only",
    roots=frozenset({"scripts"}),
    journal_name="evaluation-v1",
    lock_name=".evaluation-bootstrap.lock",
    exact_paths=frozenset({
        "scripts/evaluation_engine.py", "scripts/rule_applicability.py",
        "scripts/score_evaluation.py", "scripts/validate_evaluation.py",
        "scripts/write_evaluation.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(EVALUATION)


def preview(target: str | Path) -> dict:
    return core.preview(target, EVALUATION)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, EVALUATION)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, EVALUATION)


if __name__ == "__main__":
    raise SystemExit(main())
