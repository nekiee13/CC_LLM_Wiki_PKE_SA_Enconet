"""Preview or copy versioned local support tools and an empty incoming folder.

This bootstrap wrapper shares the guarded copy engine with the sieving bundle.
The copied scripts do not import either bootstrap file at run time.
"""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core


BUNDLE = Path(__file__).resolve().parent / "support" / "v1"
MANIFEST = BUNDLE / "manifest.json"
SUPPORT = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="project-support-and-empty-incoming",
    roots=frozenset({"handoff_schema.yml", "incoming", "scripts"}),
    journal_name="support-v1",
    lock_name=".support-bootstrap.lock",
    exact_paths=frozenset({
        "handoff_schema.yml", "incoming/.gitkeep", "scripts/agent_coord.py",
        "scripts/make_handoff.py", "scripts/check_guidance_drift.py",
        "scripts/check_skill_structure.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(SUPPORT)


def preview(target: str | Path) -> dict:
    return core.preview(target, SUPPORT)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, SUPPORT)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, SUPPORT)


if __name__ == "__main__":
    raise SystemExit(main())
