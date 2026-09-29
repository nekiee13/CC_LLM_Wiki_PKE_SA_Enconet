"""EK-1.1: preview by default; exclusive, journaled apply of copy-only entries.

No transformation, source ingestion, shared-script execution, overwrite, automatic
rollback, or implicit approval. Single cooperative writer required. Recovery
diagnosis never deletes; ambiguous partial writes stop for human review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

# A preview must not write an import cache in the project.
sys.dont_write_bytecode = True
from transfer_manifest import BASELINE, WORKSPACE, build_manifest, read_snapshot, validate_manifest

APPROVED_MANIFEST_SHA256 = "fd9d69ff5c7836c1696402aa7012177de3e625efd301274f8eeddedbaeafc3a4"
APPROVAL = "CC_2026-09-29T114644Z_ekonerg-transfer-manifest-approve"
MANIFEST = WORKSPACE / "Ekonerg/docs/transfer/transfer-manifest.json"
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
            *(f"LPT{i}" for i in range(1, 10))}


class TransferError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def is_redirect(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def check_chain(path: Path):
    """Reject symlinks and Windows junction/reparse points, including ancestors."""
    for part in reversed((path, *path.parents)):
        if is_redirect(part):
            raise TransferError(f"Redirected path is forbidden: {part}")
        if part != path and part.exists() and not part.is_dir():
            raise TransferError(f"Non-directory ancestor: {part}")


def checked_target(workspace: Path, target: Path) -> Path:
    workspace, target = Path(workspace).absolute(), Path(target).absolute()
    if ".." in target.parts or target != workspace / "Ekonerg":
        raise TransferError("Destination must be the exact workspace/Ekonerg directory")
    check_chain(target)
    if not target.is_dir():
        raise TransferError("Destination must already exist; no new project root is inferred")
    return target


def local_path(workspace: Path, destination: str) -> Path:
    if not isinstance(destination, str) or "\\" in destination or ":" in destination:
        raise TransferError("Invalid destination spelling")
    parts = destination.split("/")
    if len(parts) < 2 or parts[0] != "Ekonerg" or any(
        not p or p in {".", ".."} or p.rstrip(" .") != p or
        p.split(".")[0].upper() in RESERVED for p in parts
    ):
        raise TransferError("Unsafe destination components")
    path = workspace.joinpath(*parts)
    check_chain(path)
    return path


def fingerprint(path: Path) -> dict:
    check_chain(path)
    before = path.stat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise TransferError(f"Expected a regular, unlinked file: {path}")
    content = path.read_bytes()
    after = path.stat()
    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
    if any(getattr(before, key) != getattr(after, key) for key in fields):
        raise TransferError(f"File changed while reading: {path}")
    return {**{key: getattr(after, key) for key in fields}, "sha256": digest(content)}


def prepare(manifest, blobs, revision, workspace, target, *, sources=None, allow_conflicts=False):
    workspace = Path(workspace).absolute()
    target = checked_target(workspace, target)
    errors = validate_manifest(manifest, blobs, revision)
    if errors:
        raise TransferError("Invalid manifest: " + "; ".join(errors[:5]))
    by_source = {row["source"]: row for row in manifest["files"]}
    if sources is None:
        sources = sorted(r["source"] for r in manifest["files"] if r["treatment"] == "copy")
    if not sources or len(sources) != len(set(sources)):
        raise TransferError("Need unique, nonempty copy selections")
    for source in sources:
        if source not in by_source or by_source[source]["treatment"] != "copy":
            raise TransferError(f"Source is unlisted or not approved for unchanged copy: {source}")
    copies = []
    for source in sorted(sources):
        row = by_source[source]
        path = local_path(workspace, row["destination"])
        if not path.exists():
            state = "create"
        else:
            current = fingerprint(path)
            state = "preserve" if current["sha256"] == row["sha256"] else "conflict"
        if state == "conflict" and not allow_conflicts:
            raise TransferError(f"Refusing to overwrite different content: {path}")
        copies.append({key: row[key] for key in ("source", "destination", "sha256", "bytes", "mode", "git_blob")})
        copies[-1]["state"] = state
    return {"schema_version": 1, "workspace": str(workspace), "target": str(target),
            "source_commit": revision, "manifest_sha256": digest(canonical(manifest)),
            "copy": copies,
            "adapt": [{"source": r["source"], "destination": r["destination"]}
                      for r in manifest["files"] if r["treatment"] == "adapt"],
            "recreate": [{"source": r["source"], "destination": r["destination"]}
                         for r in manifest["files"] if r["treatment"] == "recreate"],
            "excluded": sum(r["treatment"] == "exclude" for r in manifest["files"])}


def identity(plan):
    return {key: ([{k: v for k, v in row.items() if k != "state"} for row in value]
                  if key == "copy" else value) for key, value in plan.items()}


def journal_path(plan, run_id):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", run_id) or run_id.upper() in RESERVED:
        raise TransferError("Invalid run ID; use letters, numbers, underscores or hyphens")
    return local_path(Path(plan["workspace"]), f"Ekonerg/docs/transfer/runs/{run_id}.jsonl")


def append_event(path, event):
    """Append durable state; a torn final line is never silently discarded."""
    fingerprint(path)  # Reject redirected or hard-linked journal before opening.
    with path.open("ab") as stream:
        stream.write(canonical(event) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def read_journal(path, plan):
    fingerprint(path)
    raw = path.read_bytes()
    if not raw or not raw.endswith(b"\n"):
        raise TransferError("Empty or truncated journal: manual inspection required")
    try:
        events = [json.loads(line) for line in raw.splitlines()]
    except (ValueError, UnicodeError) as error:
        raise TransferError("Malformed journal: manual inspection required") from error
    if events[0] != {"event": "start", "identity": identity(plan)}:
        raise TransferError("Journal belongs to different inputs, selection or destination")
    sources = {row["source"] for row in plan["copy"]}
    intents, done, complete = set(), {}, False
    for event in events[1:]:
        if not isinstance(event, dict) or complete:
            raise TransferError("Invalid event after completion or malformed journal")
        kind, source = event.get("event"), event.get("source")
        if kind == "intent" and set(event) == {"event", "source"}:
            if source not in sources or source in intents:
                raise TransferError("Invalid or duplicate intent")
            intents.add(source)
        elif kind in {"created", "preserved"} and set(event) == {"event", "source", "fingerprint"}:
            if source not in intents or source in done:
                raise TransferError("Receipt without intent, or duplicate receipt")
            fp = event["fingerprint"]
            if not isinstance(fp, dict) or set(fp) != {"st_dev", "st_ino", "st_size", "st_mtime_ns", "sha256"}:
                raise TransferError("Invalid receipt fingerprint")
            if any(type(fp[key]) is not int or fp[key] < 0
                   for key in ("st_dev", "st_ino", "st_size", "st_mtime_ns")):
                raise TransferError("Receipt file identity fields must be nonnegative integers")
            expected = next(row for row in plan["copy"] if row["source"] == source)
            if fp["sha256"] != expected["sha256"] or fp["st_size"] != expected["bytes"]:
                raise TransferError("Receipt hash or size differs from source")
            done[source] = event
        elif event == {"event": "complete"} and set(done) == sources:
            complete = True
        else:
            raise TransferError("Invalid journal transition")
    return intents, done, complete


def apply(plan, blobs, run_id, *, resume=False):
    """Recheck full manifest and target before writing. No source transformation."""
    workspace = Path(plan["workspace"])
    target = checked_target(workspace, Path(plan["target"]))
    fresh = prepare(build_manifest(blobs, plan["source_commit"]), blobs, plan["source_commit"],
                    workspace, target, sources=[r["source"] for r in plan["copy"]])
    if identity(plan) != identity(fresh):
        raise TransferError("Source or plan changed since preview")
    journal = journal_path(fresh, run_id)
    if journal.exists() != resume:
        raise TransferError("Existing run requires --resume; resume requires an existing journal")
    # Validate an existing journal before any mutation or lock acquisition.
    state = read_journal(journal, fresh) if resume else (set(), {}, False)
    lock = local_path(workspace, "Ekonerg/.ek-transfer.lock")
    try:
        with lock.open("xb") as stream:
            stream.write(canonical({"pid": os.getpid(), "run_id": run_id}) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError as error:
        raise TransferError("Another writer or stale lock exists; never force-remove it") from error
    lock_fp = fingerprint(lock)
    try:
        if not resume:
            check_chain(journal)
            journal.parent.mkdir(parents=True, exist_ok=True)
            check_chain(journal)
            with journal.open("xb") as stream:
                stream.write(canonical({"event": "start", "identity": identity(fresh)}) + b"\n")
                stream.flush()
                os.fsync(stream.fileno())
        intents, done, complete = state
        for row in fresh["copy"]:
            source = row["source"]
            path = local_path(workspace, row["destination"])
            if source in done:
                if not path.exists() or fingerprint(path) != done[source]["fingerprint"]:
                    raise TransferError("Recorded file changed or disappeared; review before resuming")
                continue
            if source not in intents:
                append_event(journal, {"event": "intent", "source": source})
            check_chain(path)
            if path.exists():
                fp = fingerprint(path)
                if fp["sha256"] != row["sha256"]:
                    raise TransferError("Destination changed after preflight; no overwrite")
                kind = "preserved"
            else:
                # Existing manifest has only a root-level copy. Reject new parent
                # creation until its journal/recovery semantics receive review.
                if not path.parent.is_dir():
                    raise TransferError("Copy parent must already exist")
                with path.open("xb") as stream:
                    stream.write(blobs[source].data)
                    stream.flush()
                    os.fsync(stream.fileno())
                if row["mode"] == "100755":
                    path.chmod(path.stat().st_mode | stat.S_IXUSR)
                fp = fingerprint(path)
                if fp["sha256"] != row["sha256"]:
                    raise TransferError("Post-write hash mismatch; inspect partial file")
                kind = "created"
            receipt = {"event": kind, "source": source, "fingerprint": fp}
            append_event(journal, receipt)
            done[source] = receipt
        if not complete:
            append_event(journal, {"event": "complete"})
        return {"complete": True, "journal": str(journal),
                "created": [r["destination"] for r in fresh["copy"] if done[r["source"]]["event"] == "created"],
                "preserved": [r["destination"] for r in fresh["copy"] if done[r["source"]]["event"] == "preserved"],
                "adapt_pending": len(fresh["adapt"]), "recreate_pending": len(fresh["recreate"])}
    finally:
        # Delete only this invocation's unchanged lock, never source/destination data.
        if lock.exists() and fingerprint(lock) == lock_fp:
            lock.unlink()


def diagnose(plan, run_id):
    """Read-only recovery proposal. No file deletion command is exposed."""
    workspace = Path(plan["workspace"])
    checked_target(workspace, Path(plan["target"]))
    intents, done, complete = read_journal(journal_path(plan, run_id), plan)
    candidates, conflicts, uncertain = [], [], []
    for row in plan["copy"]:
        path = local_path(workspace, row["destination"])
        receipt = done.get(row["source"])
        if receipt:
            if not path.exists() or fingerprint(path) != receipt["fingerprint"]:
                conflicts.append(row["destination"])
            elif not complete and receipt["event"] == "created":
                candidates.append(row["destination"])
        elif path.exists() and row["source"] in intents:
            uncertain.append(row["destination"])
    return {"complete": complete, "removal_candidates": candidates,
            "changed_or_missing": conflicts, "unrecorded_do_not_remove": uncertain,
            "policy": "Read-only proposal; human must review provenance and exact paths before removing any recorded unchanged file. Never remove preserved, changed, ambiguous files or directories."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--diagnose", metavar="RUN_ID")
    parser.add_argument("--run-id")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--source", action="append")
    parser.add_argument("--destination", type=Path, default=WORKSPACE / "Ekonerg")
    args = parser.parse_args(argv)
    try:
        if args.resume and not args.apply or args.run_id and not args.apply:
            raise TransferError("--run-id and --resume require --apply")
        if args.apply and not args.run_id:
            raise TransferError("--apply requires --run-id")
        # Normalize CRLF only for review-artifact identity, never source file bytes.
        raw = MANIFEST.read_bytes().replace(b"\r\n", b"\n")
        if digest(raw) != APPROVED_MANIFEST_SHA256:
            raise TransferError("Manifest differs from the independently approved revision")
        manifest = json.loads(raw)
        revision, blobs = read_snapshot(WORKSPACE, BASELINE)
        plan = prepare(manifest, blobs, revision, WORKSPACE, args.destination,
                       sources=args.source, allow_conflicts=bool(args.diagnose))
        if args.apply:
            result = apply(plan, blobs, args.run_id, resume=args.resume)
        elif args.diagnose:
            result = diagnose(plan, args.diagnose)
        else:
            result = {"mode": "preview", "manifest_approval": APPROVAL,
                      "approved_manifest_lf_sha256": APPROVED_MANIFEST_SHA256, **plan}
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f"safe_transfer: FAIL - {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
