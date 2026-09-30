"""Keep runtime files in the copied project, not the enclosing Git workspace."""
from __future__ import annotations

import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LocalPathError(ValueError):
    """A requested path is foreign or redirected."""


def configure_standard_streams() -> None:
    """Keep CLI path messages readable when Windows redirects console output."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="backslashreplace")
            except (OSError, ValueError):
                pass


def local_path(value: Path | str) -> Path:
    """Anchor relative paths locally and reject existing links before access.

    This is a cooperative local-workflow guard, not protection against an
    attacker changing filesystem paths between this check and later access.
    """
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    for candidate in (path, *path.parents):
        try:
            info = candidate.lstat()
        except FileNotFoundError:
            continue
        if (stat.S_ISLNK(info.st_mode) or
                getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise LocalPathError(f"redirected local path refused: {candidate}")
        if stat.S_ISREG(info.st_mode) and info.st_nlink > 1:
            raise LocalPathError(f"hard-linked local file refused: {candidate}")
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise LocalPathError(f"path must be local to project {ROOT}: {value}")
    return resolved
