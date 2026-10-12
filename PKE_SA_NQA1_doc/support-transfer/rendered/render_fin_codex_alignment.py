"""Render the exact CC_FIN Codex-owned minimal-alignment candidate."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PARENT_OBJECT = "d04bf3b8d1167e993e1c5c2d8d9cf33c296b5747"

OLD_VALIDATION = (
    "- Treat skipped, unavailable, blocked, unknown, and not-run checks literally; never imply pass."
)
NEW_VALIDATION = (
    "- Treat skipped, unavailable, blocked, unknown, not-run, and not-configured checks literally; "
    "never imply pass."
)
OWNERSHIP_BLOCK = (
    "- Preserve ownership: Codex authors `AGENTS.md`, `.agents/`, and `CX_` records; Claude Code authors\n"
    "  `CLAUDE.md`, `.claude/`, and `CC_` records; shared-neutral records follow their own contracts.\n"
)
ALIGNMENT_ADDITION = (
    "- Use evidence-first, scoped recovery: name the exact commit(s), obtain owner approval before\n"
    "  destructive or published recovery, prefer `git revert`, and preserve unrelated work; never use\n"
    "  `reset --hard` as routine recovery.\n"
    "- M2, M3, and later owner gates cannot be inferred from completed work, passing validation, review\n"
    "  acceptance, or publication; record the explicit owner decision before advancing a gated state.\n"
)


def git_object(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def render(source: Path) -> bytes:
    raw = source.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    if b"\r" in normalized:
        raise ValueError("source contains unsupported bare CR bytes")
    if git_object(normalized) != PARENT_OBJECT:
        raise ValueError("source does not match the reviewed CC_FIN AGENTS parent object")
    text = normalized.decode("utf-8")
    if text.count(OLD_VALIDATION) != 1:
        raise ValueError("validation anchor is not unique")
    if text.count(OWNERSHIP_BLOCK) != 1:
        raise ValueError("ownership anchor is not unique")
    if "not-configured checks literally" in text or ALIGNMENT_ADDITION in text:
        raise ValueError("alignment candidate appears already applied")
    text = text.replace(OLD_VALIDATION, NEW_VALIDATION)
    text = text.replace(OWNERSHIP_BLOCK, OWNERSHIP_BLOCK + ALIGNMENT_ADDITION)
    candidate = text.encode("utf-8")
    if not candidate.endswith(b"\n") or b"\r" in candidate:
        raise ValueError("candidate must be LF UTF-8 with a final newline")
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    candidate = render(args.source.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(candidate)
    print(f"sha256={hashlib.sha256(candidate).hexdigest().upper()}")
    print(f"git_object={git_object(candidate)}")
    print(f"bytes={len(candidate)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
