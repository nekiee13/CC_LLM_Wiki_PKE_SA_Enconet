"""EF-1.2 local work copies and exact Markdown quote checks.

This tool does not approve source intake or create a tested backup. Its default
mode is a read-only preview. It never reads another company project.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
from pathlib import Path, PurePosixPath


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def _within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _no_reparse(path: Path, root: Path) -> None:
    """Reject existing links/junctions on a project-local path."""
    if not _within(path, root):
        raise ValueError(f"path leaves project: {path}")
    parts = [root]
    current = root
    for name in path.relative_to(root).parts:
        current = current / name
        parts.append(current)
    for part in parts:
        if not part.exists() and not part.is_symlink():
            continue
        flags = getattr(part.lstat(), "st_file_attributes", 0)
        if part.is_symlink() or flags & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            raise ValueError(f"reparse point refused: {part}")


def _load(project_root: Path, register: Path, expected_hash: str):
    root = project_root.absolute()
    register = register.absolute()
    if ".." in register.parts:
        raise ValueError("unsafe register path")
    work_base = root / "work" / "fast_audit"
    if not _within(register, work_base) or register.name != "source_register.csv":
        raise ValueError("register must be a local fast-audit source_register.csv")
    _no_reparse(register, root)
    if sha256(register) != expected_hash.lower():
        raise ValueError("register hash differs from the pinned value")
    rows = []
    ids, paths = set(), set()
    with register.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            source_id = row["source_id"]
            relative = row["relative_path"]
            posix = PurePosixPath(relative)
            if ("\\" in relative or posix.is_absolute() or len(posix.parts) < 2
                    or posix.parts[0] != "incoming" or any(p in (".", "..") for p in posix.parts)):
                raise ValueError(f"unsafe source path: {relative}")
            if source_id in ids or relative in paths:
                raise ValueError(f"duplicate source ID or path: {source_id}")
            ids.add(source_id)
            paths.add(relative)
            expected = row["sha256"].lower()
            if not re.fullmatch(r"[0-9a-f]{64}", expected):
                raise ValueError(f"invalid SHA-256: {source_id}")
            source = root.joinpath(*posix.parts)
            target = register.parent / "sources" / Path(*posix.parts)
            _no_reparse(source, root)
            _no_reparse(target, root)
            if not source.is_file() or source.stat().st_size != int(row["bytes"]):
                raise ValueError(f"source size or type changed: {source_id}")
            if sha256(source) != expected:
                raise ValueError(f"source hash changed: {source_id}")
            if target.exists() and (not target.is_file() or sha256(target) != expected):
                raise ValueError(f"work-copy conflict: {source_id}")
            rows.append((source_id, source, target, expected))
    if not rows:
        raise ValueError("empty source register")
    actual = set()
    for entry in (root / "incoming").rglob("*"):
        _no_reparse(entry, root)
        if entry.is_file():
            actual.add(entry.relative_to(root).as_posix())
    if actual != paths:
        raise ValueError("incoming set differs from the frozen register")
    return rows


def prepare_copies(project_root: Path, register: Path, expected_hash: str,
                   *, apply: bool = False) -> dict[str, int]:
    """Preflight the full set, then copy only missing targets without overwrite."""
    rows = _load(Path(project_root), Path(register), expected_hash)
    result = {"planned": len(rows), "copied": 0, "preserved": sum(t.exists() for _, _, t, _ in rows)}
    if not apply:
        return result
    for source_id, source, target, expected in rows:
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(prefix=".ef12-", dir=target.parent, delete=False) as out:
                temporary = Path(out.name)
                with source.open("rb") as inp:
                    shutil.copyfileobj(inp, out)
            if sha256(temporary) != expected or sha256(source) != expected:
                raise ValueError(f"source hash changed during copy: {source_id}")
            os.link(temporary, target)  # atomic create; never replace existing work
            result["copied"] += 1
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    _load(Path(project_root), Path(register), expected_hash)
    return result


def verify_quote(project_root: Path, register: Path, expected_hash: str,
                 source_id: str, heading: str, first_line: int, last_line: int,
                 expected_text: str) -> str:
    """Return text only if its source ID, nearest heading, and lines match."""
    rows = _load(Path(project_root), Path(register), expected_hash)
    matches = [(target, digest) for row_id, _, target, digest in rows if row_id == source_id]
    if not matches:
        raise ValueError(f"unknown source ID: {source_id}")
    target, digest = matches[0]
    if not target.is_file() or sha256(target) != digest:
        raise ValueError(f"work-copy conflict: {source_id}")
    lines = target.read_text(encoding="utf-8-sig").splitlines()
    if first_line < 1 or last_line < first_line or last_line > len(lines):
        raise ValueError("invalid quote line range")
    nearest = next((line for line in reversed(lines[:first_line - 1])
                    if re.match(r"^#{1,6} ", line)), None)
    if nearest != heading:
        raise ValueError("heading mismatch")
    found = "\n".join(lines[first_line - 1:last_line])
    if found != expected_text:
        raise ValueError("quote mismatch")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--register-sha256", required=True)
    parser.add_argument("--apply", action="store_true", help="create missing local work copies")
    args = parser.parse_args()
    try:
        result = prepare_copies(args.project_root, args.register, args.register_sha256,
                                apply=args.apply)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"EF-1.2 refused: {exc}\n")
    print(json.dumps({"mode": "apply" if args.apply else "preview", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
