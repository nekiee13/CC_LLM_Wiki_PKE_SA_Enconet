"""Project-local path guard for sieving reads and exports."""
from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]
SIEVING_ROOT = PROJECT_ROOT / "sieving"


def local_io_path(value: Path) -> Path:
    """Resolve a project-relative path and refuse foreign or linked files.

    This bounds normal workflows. It does not guard a race where another
    process changes a path after validation.
    """
    raw = Path(value)
    path = (raw if raw.is_absolute() else PROJECT_ROOT / raw).resolve()
    root = PROJECT_ROOT.resolve()
    # The CLI may use the project root to start a glob. Actual sieving
    # inputs and outputs must live below the local sieving tree.
    if path != root and not path.is_relative_to(SIEVING_ROOT.resolve()):
        raise ValueError("Sieving I/O path must stay inside the project's sieving tree")
    if path.is_file() and path.stat().st_nlink > 1:
        raise ValueError("Sieving I/O refuses a hard-linked file")
    return path
