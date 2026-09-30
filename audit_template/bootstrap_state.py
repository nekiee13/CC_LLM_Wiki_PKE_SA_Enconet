"""Preview or copy the versioned, empty database and audit-state runtime.

This wrapper uses the shared guarded copy engine. It copies SQL and scripts,
not an initialized database, an approved gate, or any source document.
"""
from __future__ import annotations

from pathlib import Path

import bootstrap_sieving as core


BUNDLE = Path(__file__).resolve().parent / "state" / "v1"
MANIFEST = BUNDLE / "manifest.json"
STATE = core.BundleSpec(
    bundle=BUNDLE,
    version="1.0.0",
    scope="database-and-state-runtime",
    roots=frozenset({"db", "schemas", "scripts"}),
    journal_name="state-v1",
    lock_name=".state-bootstrap.lock",
    exact_paths=frozenset({
        "db/schema.sql", "schemas/id_patterns.yml", "schemas/vocabularies.yml",
        "scripts/project_paths.py", "scripts/db_util.py", "scripts/init_db.py",
        "scripts/audit_state.py",
    }),
)
BootstrapError = core.BootstrapError


def load_manifest() -> dict:
    return core.load_manifest(STATE)


def preview(target: str | Path) -> dict:
    return core.preview(target, STATE)


def apply(target: str | Path, run_id: str) -> dict:
    return core.apply(target, run_id, STATE)


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, STATE)


if __name__ == "__main__":
    raise SystemExit(main())
