"""Project-local path guard for sieving reads and exports."""
from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]


def local_io_path(value: Path) -> Path:
    """Resolve a project-relative path and refuse foreign or linked files.

    This bounds normal workflows. It does not guard a race where another
    process changes a path after validation.
    """
    raw = Path(value)
    path = (raw if raw.is_absolute() else PROJECT_ROOT / raw).resolve()
    root = PROJECT_ROOT.resolve()
    if not path.is_relative_to(root):
        raise ValueError("Sieving I/O path must stay inside Ekonerg")
    parts = path.relative_to(root).parts
    if parts and parts[0].casefold() == "enconet":
        raise ValueError("Sieving I/O path must not target nested Enconet")
    if path.is_file() and path.stat().st_nlink > 1:
        raise ValueError("Sieving I/O refuses a hard-linked file")
    return path
