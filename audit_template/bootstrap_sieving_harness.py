"""Preview or install the local sieving-readiness checks and blank records."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "sieving_harness" / "v1"
MANIFEST = BUNDLE / "manifest.json"
SIEVING_HARNESS = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="sieving-harness-readiness-only",
    roots=frozenset({"benchmarks", "schemas", "scripts", "sieving"}),
    journal_name="sieving-harness-v1",
    lock_name=".sieving-harness-bootstrap.lock",
    exact_paths=frozenset({
        "benchmarks/sieving_golden/manifest.yml", "schemas/sieving_skill_contract.yml",
        "scripts/validate_sieving_harness.py", "scripts/validate_sieving_skill_drift.py",
        "sieving/SIEVING_PLAYBOOK.md", "sieving/prompts/.gitattributes",
        "sieving/prompts/CHANGELOG.md", "sieving/prompts/appb_document_v1.md",
        "sieving/prompts/appb_rule_v1.md",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(SIEVING_HARNESS)


def preview(target: str | Path) -> dict:
    return core.preview(target, SIEVING_HARNESS)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, SIEVING_HARNESS)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, SIEVING_HARNESS)


if __name__ == "__main__":
    raise SystemExit(main())
