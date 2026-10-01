"""Preview or install three company-neutral, project-local Codex sieving skills."""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core

BUNDLE = Path(__file__).resolve().parent / "codex_sieving_skills" / "v1"
MANIFEST = BUNDLE / "manifest.json"
CODEX_SIEVING_SKILLS = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="codex-sieving-skills-only",
    roots=frozenset({".agents"}),
    journal_name="codex-sieving-skills-v1",
    lock_name=".codex-sieving-skills-bootstrap.lock",
    exact_paths=frozenset({
        ".agents/skills/.gitattributes",
        ".agents/skills/crumb-quality/SKILL.md",
        ".agents/skills/sieving-run/SKILL.md",
        ".agents/skills/sieving-tuning/SKILL.md",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(CODEX_SIEVING_SKILLS)


def preview(target: str | Path) -> dict:
    return core.preview(target, CODEX_SIEVING_SKILLS)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, CODEX_SIEVING_SKILLS)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, CODEX_SIEVING_SKILLS)


if __name__ == "__main__":
    raise SystemExit(main())
