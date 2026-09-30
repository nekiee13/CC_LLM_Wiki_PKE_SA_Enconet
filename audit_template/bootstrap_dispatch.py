"""Preview or copy a local dispatcher and layered preflight runner.

This slice does not provide the phase-aware aggregate validator. Audit-validate
and audit-close refuse to run until that separate tool is installed and tested.
"""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core


BUNDLE = Path(__file__).resolve().parent / "dispatch" / "v1"
MANIFEST = BUNDLE / "manifest.json"
DISPATCH = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="dispatcher-and-layered-preflight",
    roots=frozenset({"schemas", "scripts"}),
    journal_name="dispatch-v1",
    lock_name=".dispatch-bootstrap.lock",
    exact_paths=frozenset({
        "schemas/audit_commands.yml", "scripts/audit_command.py",
        "scripts/run_validation.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(DISPATCH)


def preview(target: str | Path) -> dict:
    return core.preview(target, DISPATCH)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, DISPATCH)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, DISPATCH)


if __name__ == "__main__":
    raise SystemExit(main())
