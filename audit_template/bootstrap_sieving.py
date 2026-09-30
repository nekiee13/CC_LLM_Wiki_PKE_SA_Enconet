"""Copy a versioned, source-free sieving runtime into one new audit project.

Preview is read-only. Apply needs a run ID and never overwrites a file. A new
run ID can safely pick up matching files left by an interrupted prior run.
This tool is only a bootstrap tool; copied runtime code does not import it.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any


sys.dont_write_bytecode = True
BUNDLE = Path(__file__).resolve().parent / "sieving" / "v1"
MANIFEST = BUNDLE / "manifest.json"
_VERSION = "1.0.0"
_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_BAD_NAMES = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
              *(f"LPT{i}" for i in range(1, 10))}


@dataclass(frozen=True)
class BundleSpec:
    """A pinned copy set; all company choices stay outside the bundle."""

    bundle: Path
    version: str
    scope: str
    roots: frozenset[str]
    journal_name: str
    lock_name: str
    exact_paths: frozenset[str] | None = None


SIEVING = BundleSpec(BUNDLE, _VERSION, "sieving-runtime-only",
                     frozenset({"sieving", "schemas"}), "sieving-v1",
                     ".sieving-bootstrap.lock")


class BootstrapError(ValueError):
    """The bundle or destination is unsafe; no overwrite is allowed."""


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_link(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def _check_existing_chain(path: Path) -> None:
    for part in (path, *path.parents):
        if part.is_symlink() or (part.exists() and _is_link(part)):
            raise BootstrapError(f"Link or junction in path: {part}")


def _relative_path(raw: Any, spec: BundleSpec = SIEVING) -> Path:
    if not isinstance(raw, str) or not raw or "\\" in raw or raw.startswith("/"):
        raise BootstrapError(f"Unsafe bundle path: {raw!r}")
    parts = raw.split("/")
    if parts[0] not in spec.roots or (len(parts) < 2 and raw not in (spec.exact_paths or ())):
        raise BootstrapError(f"Out-of-scope bundle path: {raw!r}")
    if spec.exact_paths is not None and raw not in spec.exact_paths:
        raise BootstrapError(f"Unexpected bundle file: {raw!r}")
    for part in parts:
        if (not part or part in {".", ".."} or ":" in part or
                part.endswith((".", " ")) or part.upper().split(".")[0] in _BAD_NAMES):
            raise BootstrapError(f"Unsafe bundle path: {raw!r}")
    if "DATA" in parts or "fixtures" in parts or "__pycache__" in parts:
        raise BootstrapError(f"Source data is not part of this bundle: {raw!r}")
    return Path(*parts)


def load_manifest(spec: BundleSpec = SIEVING) -> dict[str, Any]:
    """Validate every declared file and reject undeclared files."""
    bundle = spec.bundle
    manifest_path = bundle / "manifest.json"
    _check_existing_chain(bundle)
    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapError(f"Cannot read template manifest: {exc}") from exc
    if manifest.get("template_version") != spec.version or manifest.get("scope") != spec.scope:
        raise BootstrapError("Wrong template version or scope")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise BootstrapError("Template has no file list")
    names: list[str] = []
    for entry in files:
        if not isinstance(entry, dict):
            raise BootstrapError("Invalid manifest entry")
        relative = _relative_path(entry.get("path"), spec)
        name = relative.as_posix()
        if name in names or not _HASH.fullmatch(str(entry.get("sha256"))):
            raise BootstrapError(f"Duplicate path or bad hash: {name}")
        if type(entry.get("bytes")) is not int or entry["bytes"] < 0:
            raise BootstrapError(f"Bad byte count: {name}")
        source = bundle / relative
        _check_existing_chain(source)
        if not source.is_file() or source.stat().st_nlink != 1:
            raise BootstrapError(f"Missing or linked template file: {name}")
        data = source.read_bytes()
        if len(data) != entry["bytes"] or _digest(data) != entry["sha256"]:
            raise BootstrapError(f"Template hash mismatch: {name}")
        names.append(name)
    if names != sorted(names):
        raise BootstrapError("Manifest paths must be sorted")
    actual = sorted(p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file()
                    and p != manifest_path)
    if actual != names:
        raise BootstrapError("Manifest does not list every bundle file")
    return manifest


def _target(path: str | Path, spec: BundleSpec = SIEVING) -> Path:
    raw = Path(path)
    if ".." in raw.parts:
        raise BootstrapError("Target path must not contain '..'")
    absolute = raw.absolute()
    _check_existing_chain(absolute)
    if not absolute.is_dir() or absolute == Path(absolute.anchor):
        raise BootstrapError("Target must be an existing project directory, not a drive root")
    resolved = absolute.resolve(strict=True)
    if (resolved == spec.bundle or spec.bundle in resolved.parents or
            resolved in spec.bundle.parents):
        raise BootstrapError("Target must not be the template or its parent")
    return resolved


def _plan(target: Path, manifest: dict[str, Any], spec: BundleSpec = SIEVING) -> list[dict[str, str]]:
    rows = []
    for entry in manifest["files"]:
        name = entry["path"]
        destination = target / _relative_path(name, spec)
        _check_existing_chain(destination)
        for ancestor in destination.parents:
            if ancestor == target:
                break
            if ancestor.exists() and not ancestor.is_dir():
                raise BootstrapError(f"File blocks destination directory: {ancestor}")
        state = "create"
        if destination.exists():
            if not destination.is_file() or destination.stat().st_nlink != 1:
                raise BootstrapError(f"Unsafe existing target: {name}")
            data = destination.read_bytes()
            if len(data) != entry["bytes"] or _digest(data) != entry["sha256"]:
                raise BootstrapError(f"Existing file differs; no overwrite: {name}")
            state = "preserve"
        rows.append({"path": name, "sha256": entry["sha256"], "state": state})
    return rows


def preview(target: str | Path, spec: BundleSpec = SIEVING) -> dict[str, Any]:
    """Show all creates/preserves without writing to the target."""
    manifest = load_manifest(spec)
    root = _target(target, spec)
    return {"mode": "preview", "template_version": spec.version,
            "target": str(root), "files": _plan(root, manifest, spec)}


def _record(stream: Any, event: dict[str, Any]) -> None:
    stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    stream.flush()
    os.fsync(stream.fileno())


def apply(target: str | Path, run_id: str, spec: BundleSpec = SIEVING) -> dict[str, Any]:
    """Copy only missing files, with an append-only journal per unique run ID."""
    if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
        raise BootstrapError("Run ID must be 1-80 letters, digits, '-' or '_'")
    manifest = load_manifest(spec)
    root = _target(target, spec)
    rows = _plan(root, manifest, spec)  # All source bytes and target conflicts are checked first.
    journal_dir = root / ".bootstrap" / spec.journal_name
    journal = journal_dir / f"{run_id}.jsonl"
    lock = root / spec.lock_name
    _check_existing_chain(journal)
    _check_existing_chain(lock)
    if journal.exists() or lock.exists():
        raise BootstrapError("Run ID already used, or another bootstrap is active")
    for folder in (journal_dir, journal_dir.parent):
        if folder.exists() and not folder.is_dir():
            raise BootstrapError(f"Journal directory blocked: {folder}")
    try:
        with lock.open("x", encoding="utf-8") as lock_stream:
            lock_stream.write(run_id + "\n")
            lock_stream.flush()
            os.fsync(lock_stream.fileno())
        try:
            journal_dir.mkdir(parents=True, exist_ok=True)
            created: list[str] = []
            preserved: list[str] = []
            with journal.open("x", encoding="utf-8", newline="\n") as stream:
                _record(stream, {"event": "start", "run_id": run_id,
                                 "target": str(root), "template_version": spec.version,
                                 "manifest_sha256": _digest((spec.bundle / "manifest.json").read_bytes())})
                for row in rows:
                    name = row["path"]
                    destination = root / _relative_path(name, spec)
                    _check_existing_chain(destination)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    data = (spec.bundle / _relative_path(name, spec)).read_bytes()
                    if _digest(data) != row["sha256"]:
                        raise BootstrapError(f"Template changed during apply: {name}")
                    _record(stream, {"event": "intent", "path": name, "sha256": row["sha256"]})
                    if row["state"] == "create":
                        try:
                            with destination.open("xb") as output:
                                output.write(data)
                                output.flush()
                                os.fsync(output.fileno())
                        except FileExistsError as exc:
                            raise BootstrapError(f"Target changed during apply: {name}") from exc
                        created.append(name)
                        _record(stream, {"event": "created", "path": name, "sha256": row["sha256"]})
                    else:
                        if _digest(destination.read_bytes()) != row["sha256"]:
                            raise BootstrapError(f"Target changed during apply: {name}")
                        preserved.append(name)
                        _record(stream, {"event": "preserved", "path": name, "sha256": row["sha256"]})
                _record(stream, {"event": "complete", "created": len(created),
                                 "preserved": len(preserved)})
            return {"mode": "apply", "template_version": spec.version, "target": str(root),
                    "created": created, "preserved": preserved, "journal": str(journal)}
        finally:
            lock.unlink(missing_ok=True)
    except FileExistsError as exc:
        raise BootstrapError("Run ID already used, or another bootstrap is active") from exc


def main(argv: list[str] | None = None, spec: BundleSpec = SIEVING) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Existing new audit project folder")
    parser.add_argument("--apply", action="store_true", help="Copy the manifest files")
    parser.add_argument("--run-id", help="Unique journal ID; required with --apply")
    args = parser.parse_args(argv)
    if bool(args.run_id) != args.apply:
        parser.error("--apply and --run-id must be given together")
    try:
        result = apply(args.target, args.run_id, spec) if args.apply else preview(args.target, spec)
    except (BootstrapError, OSError) as exc:
        print(f"bootstrap error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
