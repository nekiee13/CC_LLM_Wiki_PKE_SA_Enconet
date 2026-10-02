#!/usr/bin/env python3
"""Preview or safely reset Ekonerg's generated audit state.

The command deliberately does not reset the project framework, incoming
documents, coordination history, or immutable handoff/review records. It
removes only known runtime/output locations and clears mutable validation
manifests back to their headers. Preview is the default. Apply requires a
hash-checked external plan and an exact confirmation token. Normal apply
creates an external backup; a deliberate no-backup mode uses a different
confirmation token.
"""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from zipfile import ZIP_DEFLATED, ZipFile

from project_paths import configure_standard_streams


ROOT = Path(__file__).resolve().parents[1]
CONFIRMATION = "RESET-EKONERG"
NO_BACKUP_CONFIRMATION = "RESET-EKONERG-NO-BACKUP"
PLAN_VERSION = 1

# These are generated audit state locations. Framework code, schemas, prompts,
# tests, incoming sources, docs, coordination, and handoffs are not targets.
RESET_DIRS = (
    "raw",
    "derived",
    "work",
    "outputs",
    "results",
    "reports",
    "artifacts",
    "audit_runs",
    "db/backups",
    "sieving/DATA",
    "sieving/outputs",
    "sieving/runs",
    "sieving/results",
    "wiki/actions",
    "wiki/criteria",
    "wiki/dashboards",
    "wiki/evidence",
    "wiki/findings",
    "wiki/gates",
)

RESET_TEXT_FILES = {
    "manifests/approvals.csv": "object_id,decision,date,reviewer,notes",
    "manifests/link_exceptions.csv": "crumb_id,quote_id,reason,approved_by,date",
    "manifests/validation_runs.csv": "run_utc,validator,phase,result,exit_code,details",
}
RESET_FILES = (
    "db/nqa_audit.sqlite",
    "project-state.yml",
    "wiki/current-status.md",
    "wiki/index.md",
)


class ResetError(ValueError):
    """Raised when a reset would be ambiguous, unsafe, or stale."""


def _canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _assert_root(root: Path) -> Path:
    root = Path(root).absolute()
    if not root.is_dir():
        raise ResetError(f"project root is not a directory: {root}")
    if root.is_symlink() or getattr(root.stat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
        raise ResetError(f"redirected project root refused: {root}")
    incoming = root / "incoming"
    if not incoming.is_dir() or incoming.is_symlink():
        raise ResetError("incoming directory is missing or redirected")
    return root


def _assert_safe(path: Path, root: Path, *, allow_missing: bool = False) -> None:
    if not _is_within(path, root):
        raise ResetError(f"reset path leaves project: {path}")
    current = root
    for part in path.relative_to(root).parts:
        current /= part
        if not current.exists():
            if allow_missing:
                continue
            raise ResetError(f"reset path disappeared: {current}")
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            raise ResetError(f"redirected reset path refused: {current}")


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fingerprint(path: Path, root: Path) -> dict[str, object]:
    _assert_safe(path, root)
    if not path.is_file():
        raise ResetError(f"reset target is not a regular file: {path}")
    info = path.stat()
    if info.st_nlink != 1:
        raise ResetError(f"hard-linked reset file refused: {path}")
    return {
        "relative_path": path.relative_to(root).as_posix(),
        "sha256": _file_hash(path),
        "size": info.st_size,
        "mtime_ns": info.st_mtime_ns,
    }


def _incoming_snapshot(root: Path) -> list[dict[str, object]]:
    incoming = root / "incoming"
    rows: list[dict[str, object]] = []
    for path in sorted(incoming.rglob("*")):
        if path.is_dir():
            _assert_safe(path, root)
            continue
        rows.append(_fingerprint(path, root))
    return rows


def _candidate_files(root: Path) -> list[tuple[Path, str, str | None]]:
    found: dict[str, tuple[Path, str, str | None]] = {}
    for relative in RESET_DIRS:
        directory = root / Path(relative)
        if not directory.exists():
            continue
        _assert_safe(directory, root)
        if not directory.is_dir():
            raise ResetError(f"reset directory is not a directory: {directory}")
        for path in sorted(directory.rglob("*")):
            _assert_safe(path, root)
            if path.is_dir():
                continue
            if path.name == ".gitkeep":
                continue
            found[path.relative_to(root).as_posix()] = (path, "delete", None)
    for relative, header in RESET_TEXT_FILES.items():
        path = root / Path(relative)
        if not path.exists():
            continue
        _assert_safe(path, root)
        if not path.is_file():
            raise ResetError(f"reset manifest is not a file: {path}")
        first = path.read_text(encoding="utf-8-sig").splitlines()
        if not first or first[0] != header:
            raise ResetError(f"unexpected manifest header; refusing reset: {path}")
        found[relative] = (path, "truncate", header + "\n")
    for relative in RESET_FILES:
        path = root / Path(relative)
        if not path.exists():
            continue
        _assert_safe(path, root)
        if not path.is_file():
            raise ResetError(f"reset file is not a regular file: {path}")
        found[relative] = (path, "delete", None)
    return [found[key] for key in sorted(found)]


def build_plan(project_root: Path | str = ROOT) -> dict[str, object]:
    """Build a read-only plan and fingerprint every file before apply."""
    root = _assert_root(Path(project_root))
    candidates = []
    for path, action, header in _candidate_files(root):
        entry = _fingerprint(path, root)
        entry["action"] = action
        if header is not None:
            entry["header_b64"] = base64.b64encode(header.encode("utf-8")).decode("ascii")
        candidates.append(entry)
    summary = {
        "delete": sum(item["action"] == "delete" for item in candidates),
        "truncate": sum(item["action"] == "truncate" for item in candidates),
        "files": len(candidates),
    }
    body = {
        "plan_version": PLAN_VERSION,
        "project_root": str(root),
        "incoming_files": _incoming_snapshot(root),
        "candidates": candidates,
        "summary": summary,
    }
    return {**body, "plan_sha256": _digest(body)}


def write_plan(plan: dict[str, object], path: Path | str) -> Path:
    """Write a plan outside the project; plans inside the target are unsafe."""
    destination = Path(path).absolute()
    root = Path(str(plan["project_root"])).absolute()
    if _is_within(destination, root):
        raise ResetError("plan must be stored outside the project root")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(_canonical(plan))
    return destination


def _load_plan(path: Path | str) -> dict[str, object]:
    source = Path(path).absolute()
    if not source.is_file():
        raise ResetError(f"plan file is missing: {source}")
    try:
        plan = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResetError(f"invalid reset plan: {source}") from exc
    if not isinstance(plan, dict) or plan.get("plan_version") != PLAN_VERSION:
        raise ResetError("unsupported reset plan")
    recorded = plan.pop("plan_sha256", None)
    if not isinstance(recorded, str) or recorded != _digest(plan):
        raise ResetError("reset plan hash is invalid")
    plan["plan_sha256"] = recorded
    return plan


def _compare_plan(plan: dict[str, object], current: dict[str, object], root: Path) -> None:
    if Path(str(plan.get("project_root"))).absolute() != root:
        raise ResetError("reset plan belongs to a different project root")
    keys = ("incoming_files", "candidates", "summary")
    if any(plan.get(key) != current.get(key) for key in keys):
        raise ResetError("project state changed since preview; create a new plan")


def _backup_path(backup_dir: Path, plan_hash: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return backup_dir / f"ekonerg-reset-{timestamp}-{plan_hash[:12]}.zip"


def _external_backup_dir(backup_dir: Path, root: Path) -> Path:
    backup_dir = backup_dir.absolute()
    if _is_within(backup_dir, root):
        raise ResetError("backup directory must be outside the project root")
    backup_dir.mkdir(parents=True, exist_ok=True)
    if backup_dir.is_symlink() or getattr(backup_dir.stat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
        raise ResetError("redirected backup directory refused")
    return backup_dir


def apply_plan(plan_path: Path | str, project_root: Path | str,
               backup_dir: Path | str | None, *, confirmation: str) -> dict[str, object]:
    """Apply a plan only after all fingerprints still match.

    ``backup_dir=None`` deliberately skips the generated-state backup. This
    owner-controlled trade-off has a separate confirmation token.
    """
    expected_confirmation = NO_BACKUP_CONFIRMATION if backup_dir is None else CONFIRMATION
    if confirmation != expected_confirmation:
        raise ResetError(f"exact confirmation required: {expected_confirmation}")
    root = _assert_root(Path(project_root))
    plan = _load_plan(plan_path)
    current = build_plan(root)
    _compare_plan(plan, current, root)
    archive: Path | None = None
    if backup_dir is not None:
        backup_root = _external_backup_dir(Path(backup_dir), root)
        archive = _backup_path(backup_root, str(plan["plan_sha256"]))
        if archive.exists():
            raise ResetError(f"backup already exists: {archive}")

    candidates = list(plan["candidates"])
    entries: list[dict[str, object]] = []
    if archive is not None:
        with ZipFile(archive, "x", compression=ZIP_DEFLATED) as bundle:
            for entry in candidates:
                relative = str(entry["relative_path"])
                path = root / Path(relative)
                actual = _fingerprint(path, root)
                expected = {key: entry[key] for key in ("relative_path", "sha256", "size", "mtime_ns")}
                if actual != expected:
                    raise ResetError(f"reset target changed since preview: {relative}")
                bundle.write(path, arcname=relative)
                entries.append(actual)
            bundle.writestr("reset-plan.json", _canonical(plan))

        with ZipFile(archive, "r") as bundle:
            names = set(bundle.namelist())
            expected_names = {str(entry["relative_path"]) for entry in candidates} | {"reset-plan.json"}
            if names != expected_names:
                raise ResetError("backup archive contents do not match the reset plan")
    else:
        for entry in candidates:
            relative = str(entry["relative_path"])
            path = root / Path(relative)
            actual = _fingerprint(path, root)
            expected = {key: entry[key] for key in ("relative_path", "sha256", "size", "mtime_ns")}
            if actual != expected:
                raise ResetError(f"reset target changed since preview: {relative}")
            entries.append(actual)

    deleted = truncated = 0
    for entry in candidates:
        path = root / Path(str(entry["relative_path"]))
        actual = _fingerprint(path, root)
        expected = {key: entry[key] for key in ("relative_path", "sha256", "size", "mtime_ns")}
        if actual != expected:
            raise ResetError(f"reset target changed before removal: {path}")
        if entry["action"] == "delete":
            path.unlink()
            deleted += 1
        else:
            header = base64.b64decode(str(entry["header_b64"])).decode("utf-8")
            path.write_bytes(header.encode("utf-8"))
            truncated += 1
    _prune_empty_dirs(root)
    return {"backup": str(archive) if archive is not None else None,
            "backup_status": "created" if archive is not None else "owner-waived",
            "deleted": deleted, "truncated": truncated,
            "plan_sha256": plan["plan_sha256"]}


def _prune_empty_dirs(root: Path) -> None:
    for relative in RESET_DIRS:
        directory = root / Path(relative)
        if not directory.is_dir() or directory.is_symlink():
            continue
        for path in sorted(directory.rglob("*"), reverse=True):
            if path.is_dir() and not path.is_symlink():
                try:
                    path.rmdir()
                except OSError:
                    pass


def main(argv: list[str] | None = None) -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, help="external plan file (write in preview, read in apply)")
    parser.add_argument("--apply", action="store_true", help="apply a previously written plan")
    parser.add_argument("--backup-dir", type=Path, help="external backup directory for normal apply")
    parser.add_argument("--no-backup", action="store_true",
                        help="skip generated-state backup; requires the no-backup token")
    parser.add_argument("--confirm", help=f"must equal {CONFIRMATION} for --apply")
    args = parser.parse_args(argv)
    try:
        if not args.apply:
            plan = build_plan(ROOT)
            if args.plan:
                destination = write_plan(plan, args.plan)
                print(json.dumps({"mode": "preview", "plan": str(destination), **plan}, ensure_ascii=False, sort_keys=True))
            else:
                print(json.dumps({"mode": "preview", **plan}, ensure_ascii=False, sort_keys=True))
            return 0
        if not args.plan or (args.backup_dir is not None and args.no_backup) or (args.backup_dir is None and not args.no_backup):
            raise ResetError("--apply requires exactly one of --backup-dir or --no-backup")
        result = apply_plan(args.plan, ROOT, None if args.no_backup else args.backup_dir,
                            confirmation=args.confirm or "")
        print(json.dumps({"mode": "apply", **result}, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ResetError, UnicodeError, ValueError) as exc:
        print(f"reset_audit: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
