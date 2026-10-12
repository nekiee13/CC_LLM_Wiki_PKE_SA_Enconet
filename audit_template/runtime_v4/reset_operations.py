"""Delete one already fingerprint-checked reset target, never a directory.

Caller must have checked the external plan, confirmation and current file hash.
This handles Windows' read-only file flag, not directory ACLs. It does not grant
reset authority, follow links, or relax a stale plan.
"""
import os
from pathlib import Path
import stat


def remove_generated(path, *, unlink=None):
    path = Path(path)
    original = path.lstat()
    if (not stat.S_ISREG(original.st_mode) or original.st_nlink != 1
            or getattr(original, 'st_file_attributes', 0) & 0x400):
        raise ValueError('reset deletion requires one regular, unlinked file')
    changed = os.name == 'nt' and not original.st_mode & stat.S_IWRITE
    if changed:
        path.chmod(original.st_mode | stat.S_IWRITE)
    try:
        (unlink or Path.unlink)(path)
    except BaseException:
        if changed and path.exists():
            current = path.lstat()
            if (current.st_dev, current.st_ino) == (original.st_dev, original.st_ino):
                path.chmod(original.st_mode)
        raise
