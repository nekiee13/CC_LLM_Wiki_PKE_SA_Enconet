#!/usr/bin/env python3
"""Report session-start drift and enforce explicit resume/rollback handling."""

from __future__ import annotations

import argparse
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

from audit_state import DEFAULT_STATE, load_state


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
HANDOFF = ROOT / "HANDOFF.md"
CURRENT_STATUS = ROOT / "wiki" / "current-status.md"
INDEX = ROOT / "wiki" / "index.md"
DATABASE = ROOT / "db" / "audit.db"


def git_head(workspace: Path = WORKSPACE) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={workspace.as_posix()}", "rev-parse", "HEAD"],
        cwd=workspace, capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "unable to read Git HEAD")
    return result.stdout.strip()


def unfinished_evaluations(database: Path) -> list[str]:
    if not database.exists():
        return []
    with sqlite3.connect(database) as connection:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='evaluation_runs'"
        ).fetchone()
        if not exists:
            return []
        return [row[0] for row in connection.execute(
            "SELECT run_id FROM evaluation_runs WHERE completed_at IS NULL ORDER BY run_id"
        )]


def inspect_start(
    *, handoff: Path = HANDOFF, current_status: Path = CURRENT_STATUS,
    index: Path = INDEX, state: Path = DEFAULT_STATE, database: Path = DATABASE,
    actual_head: str | None = None,
) -> tuple[list[str], list[str]]:
    """Return informational lines and drift/action warnings in mandated read order."""
    info = [
        "read_order: active agent guidance -> HANDOFF -> current-status -> index -> project-state",
        f"handoff: {handoff}", f"current_status: {current_status}",
        f"index: {index}", f"project_state: {state}",
    ]
    warnings: list[str] = []
    for path in (handoff, current_status, index, state):
        if not path.exists():
            warnings.append(f"missing continuity record: {path}")
    if warnings:
        return info, warnings

    handoff_text = handoff.read_text(encoding="utf-8")
    status_text = current_status.read_text(encoding="utf-8")
    project = load_state(state)
    phase = str(project["phase"])
    head = actual_head or git_head()
    handoff_head = re.search(r"\*\*Git:\*\*\s*`([0-9a-fA-F]+)`", handoff_text)
    if not handoff_head:
        warnings.append("HANDOFF does not name its Git HEAD")
    elif not head.startswith(handoff_head.group(1)):
        warnings.append(f"Git divergence: HANDOFF={handoff_head.group(1)} actual={head}")
    status_phase = re.search(r"phase:\s*\*\*([a-z_]+)\*\*", status_text)
    if not status_phase:
        warnings.append("current-status does not name the project-state phase")
    elif status_phase.group(1) != phase:
        warnings.append(
            f"state divergence: current-status={status_phase.group(1)} project-state={phase}"
        )
    next_action = re.search(r"(?ms)^## Next action\s*$\s*(.+?)(?=^## |\Z)", status_text)
    if not next_action or not next_action.group(1).strip():
        warnings.append("current-status has no explicit next action")
    info.append(f"current_state: {phase}")
    in_progress = phase not in {"setup", "closed", "failed"}
    if in_progress:
        warnings.append(
            f"IN-PROGRESS STATE {phase}: human must choose RESUME from {phase} or "
            "ROLLBACK under an approved recovery procedure; no automatic change is allowed"
        )
    unfinished = unfinished_evaluations(database)
    info.append("unfinished_evaluation_runs: " + (", ".join(unfinished) if unfinished else "none"))
    if unfinished:
        warnings.append("unfinished evaluation runs require explicit resume-or-rollback disposition")
    return info, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, default=HANDOFF)
    parser.add_argument("--current-status", type=Path, default=CURRENT_STATUS)
    parser.add_argument("--index", type=Path, default=INDEX)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--database", type=Path, default=DATABASE)
    args = parser.parse_args(argv)
    try:
        info, warnings = inspect_start(handoff=args.handoff,
                                       current_status=args.current_status,
                                       index=args.index, state=args.state,
                                       database=args.database)
    except (OSError, RuntimeError, sqlite3.Error, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("\n".join(info))
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 2 if any("IN-PROGRESS" in warning for warning in warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
