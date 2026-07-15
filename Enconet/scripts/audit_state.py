#!/usr/bin/env python3
"""Fail-closed audit state transitions and human-gate recording."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "project-state.yml"
DEFAULT_APPROVALS = ROOT / "manifests" / "approvals.csv"
DEFAULT_EXCEPTIONS = ROOT / "manifests" / "link_exceptions.csv"
DEFAULT_LOG = ROOT / "wiki" / "log.md"
VOCABULARIES = ROOT / "schemas" / "vocabularies.yml"

GATE_FOR_TARGET = {
    "registered": "G1",
    "evidence_reviewed": "G2",
    "evaluated": "G3",
    "findings_approved": "G4",
    "report_ready": "G5",
    "dashboard_ready": "G6",
    "closed": "G7",
}


class StateError(ValueError):
    """Raised when state or approval evidence is invalid."""


def audit_states(vocabularies: Path = VOCABULARIES) -> list[str]:
    data = yaml.safe_load(vocabularies.read_text(encoding="utf-8"))
    states = list(data["vocabularies"]["audit_states"]["values"])
    if not states or states[0] != "setup" or states[-1] != "failed":
        raise StateError("audit_states must begin with setup and end with failed")
    return states


def legal_successors(current: str, states: list[str]) -> list[str]:
    if current not in states:
        raise StateError(f"unknown current state: {current}")
    if current == "failed":
        return []
    normal = [state for state in states if state != "failed"]
    successors: list[str] = []
    if current in normal and normal.index(current) + 1 < len(normal):
        successors.append(normal[normal.index(current) + 1])
    successors.append("failed")
    return successors


def load_state(path: Path = DEFAULT_STATE) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("gates"), dict):
        raise StateError(f"invalid project state: {path}")
    return data


def _yaml_scalar(value: str | None) -> str:
    if value is None:
        return "null"
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", value):
        raise StateError(f"unsafe state scalar: {value!r}")
    return value


def update_state_file(
    path: Path,
    *,
    phase: str | None = None,
    gate: str | None = None,
    gate_status: str | None = None,
    gate_date: str | None = None,
    decision_ref: str | None = None,
) -> None:
    """Atomically update only mutable state fields, preserving the inline schema."""
    text = path.read_text(encoding="utf-8")
    if phase is not None:
        text, count = re.subn(r"(?m)^phase:\s*\S+\s*$", f"phase: {phase}", text)
        if count != 1:
            raise StateError("project-state.yml must contain exactly one phase field")
    if gate is not None:
        if gate_status not in {"pending", "approved", "rejected", "deferred"}:
            raise StateError(f"invalid gate status: {gate_status}")
        pattern = rf"(?m)^(\s{{2}}{re.escape(gate)}:\s*)\{{[^\r\n]*?\}}(\s*(?:#.*)?)$"
        replacement = (
            rf"\1{{status: {gate_status}, date: {_yaml_scalar(gate_date)}, "
            rf"decision_ref: {_yaml_scalar(decision_ref)}}}\2"
        )
        text, count = re.subn(pattern, replacement, text)
        if count != 1:
            raise StateError(f"project-state.yml must contain exactly one {gate} entry")
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8", newline="")
    temp.replace(path)


def approval_for(object_id: str, approvals: Path = DEFAULT_APPROVALS) -> dict[str, str]:
    with approvals.open(newline="", encoding="utf-8-sig") as handle:
        matches = [row for row in csv.DictReader(handle) if row.get("object_id") == object_id]
    if not matches:
        raise StateError(f"no approval record for {object_id}")
    signatures = {(r.get("decision"), r.get("date"), r.get("reviewer")) for r in matches}
    if len(signatures) != 1:
        raise StateError(f"conflicting approval records for {object_id}")
    row = matches[-1]
    if row.get("decision") not in {"approved", "rejected", "deferred"}:
        raise StateError(f"invalid decision for {object_id}: {row.get('decision')}")
    if not row.get("date") or not row.get("reviewer"):
        raise StateError(f"unsigned approval record for {object_id}")
    return row


def append_log(log: Path, event: str, details: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with log.open("a", encoding="utf-8", newline="") as handle:
        handle.write(f"\n- {stamp} | `{event}` | {details}\n")


def record_gate_decision(
    gate: str,
    decision_ref: str,
    *,
    state_path: Path = DEFAULT_STATE,
    approvals: Path = DEFAULT_APPROVALS,
    log: Path = DEFAULT_LOG,
) -> dict[str, str]:
    if not re.fullmatch(r"G[1-7]", gate):
        raise StateError(f"invalid gate: {gate}")
    if not decision_ref.startswith(gate + "-"):
        raise StateError(f"decision reference {decision_ref} does not belong to {gate}")
    row = approval_for(decision_ref, approvals)
    update_state_file(
        state_path,
        gate=gate,
        gate_status=row["decision"],
        gate_date=row["date"],
        decision_ref=decision_ref,
    )
    append_log(log, "gate-decision", f"{gate} {row['decision']} as `{decision_ref}` by {row['reviewer']}")
    return row


def transition(
    target: str,
    *,
    state_path: Path = DEFAULT_STATE,
    approvals: Path = DEFAULT_APPROVALS,
    log: Path = DEFAULT_LOG,
    vocabularies: Path = VOCABULARIES,
    reason: str | None = None,
) -> None:
    states = audit_states(vocabularies)
    data = load_state(state_path)
    current = str(data.get("phase"))
    legal = legal_successors(current, states)
    if target not in legal:
        rendered = ", ".join(legal) if legal else "none"
        raise StateError(f"illegal transition from {current} to {target}; legal successors: {rendered}")
    if target == "failed":
        if not reason or not reason.strip():
            raise StateError("transition to failed requires --reason")
    else:
        gate = GATE_FOR_TARGET.get(target)
        if gate:
            gate_state = data["gates"].get(gate, {})
            decision_ref = gate_state.get("decision_ref")
            if gate_state.get("status") != "approved" or not decision_ref:
                raise StateError(f"{gate} approval must be recorded in project-state.yml before {target}")
            row = approval_for(str(decision_ref), approvals)
            if row["decision"] != "approved":
                raise StateError(f"{gate} decision {decision_ref} is not approved")
    update_state_file(state_path, phase=target)
    detail = f"{current} -> {target}"
    if reason:
        detail += f"; reason: {reason.strip()}"
    append_log(log, "state-transition", detail)


def open_exception_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return sum(1 for row in rows if row and row.get("status", "open").lower() not in {"closed", "resolved"})


def status_text(
    *, state_path: Path = DEFAULT_STATE, exceptions: Path = DEFAULT_EXCEPTIONS,
    vocabularies: Path = VOCABULARIES,
) -> str:
    data = load_state(state_path)
    current = str(data["phase"])
    normal = [s for s in audit_states(vocabularies) if s != "failed"]
    pending = "none"
    if current in normal:
        for target in normal[normal.index(current) + 1:]:
            gate = GATE_FOR_TARGET.get(target)
            if gate and data["gates"].get(gate, {}).get("status") != "approved":
                pending = gate
                break
    return f"current_state: {current}\npending_gate: {pending}\nopen_exceptions: {open_exception_count(exceptions)}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--status", action="store_true")
    action.add_argument("--transition", metavar="STATE")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--approvals", type=Path, default=DEFAULT_APPROVALS)
    parser.add_argument("--exceptions", type=Path, default=DEFAULT_EXCEPTIONS)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--vocabularies", type=Path, default=VOCABULARIES)
    parser.add_argument("--reason")
    args = parser.parse_args(argv)
    try:
        if args.status:
            print(status_text(state_path=args.state, exceptions=args.exceptions,
                              vocabularies=args.vocabularies))
        else:
            transition(args.transition, state_path=args.state, approvals=args.approvals,
                       log=args.log, vocabularies=args.vocabularies, reason=args.reason)
            print(f"transitioned to {args.transition}")
    except (OSError, KeyError, StateError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
