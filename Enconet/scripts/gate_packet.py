#!/usr/bin/env python3
"""Create human gate packets and record signed decisions without advancing state."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from audit_state import (
    DEFAULT_APPROVALS, DEFAULT_LOG, DEFAULT_STATE, StateError, approval_for,
    record_gate_decision,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "gate-packet-template.md"
GATE_DIR = ROOT / "wiki" / "gates"


def _safe_token(value: str, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise StateError(f"invalid {label}: {value}")
    return value


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
    if not match:
        raise StateError("gate packet has no valid YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise StateError("gate packet frontmatter must be a mapping")
    return data, match.group(2)


def render_frontmatter(data: dict[str, object]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()


def create_packet(
    *, gate: str, supplier: str, decision_ref: str, summary: str,
    evidence: str, validation: str, output: Path, template: Path = TEMPLATE,
) -> Path:
    if not re.fullmatch(r"G[1-7]", gate):
        raise StateError(f"invalid gate: {gate}")
    _safe_token(supplier, "supplier")
    _safe_token(decision_ref, "decision reference")
    if not decision_ref.startswith(gate + "-"):
        raise StateError(f"decision reference {decision_ref} does not belong to {gate}")
    if output.exists():
        raise StateError(f"gate packet already exists: {output}")
    for existing in output.parent.glob("*.md") if output.parent.exists() else []:
        existing_data, _ = split_frontmatter(existing.read_text(encoding="utf-8"))
        if existing_data.get("gate") == gate and existing_data.get("supplier") == supplier:
            raise StateError(f"packet already exists for {gate} and supplier {supplier}: {existing}")
    replacements = {
        "{{GATE}}": gate,
        "{{SUPPLIER}}": supplier,
        "{{DECISION_REF}}": decision_ref,
        "{{SUMMARY}}": summary.strip(),
        "{{EVIDENCE_POINTERS}}": evidence.strip(),
        "{{VALIDATION_RESULTS}}": validation.strip(),
    }
    text = template.read_text(encoding="utf-8")
    for marker, value in replacements.items():
        text = text.replace(marker, value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))
    if unresolved:
        raise StateError(f"unresolved template markers: {', '.join(unresolved)}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8", newline="")
    return output


def record_packet(
    packet: Path, *, state: Path = DEFAULT_STATE,
    approvals: Path = DEFAULT_APPROVALS, log: Path = DEFAULT_LOG,
) -> dict[str, str]:
    data, body = split_frontmatter(packet.read_text(encoding="utf-8"))
    gate = str(data.get("gate", ""))
    decision_ref = str(data.get("id", ""))
    if len(re.findall(r"<!-- DECISION_RECORD_START -->.*?<!-- DECISION_RECORD_END -->",
                      body, flags=re.DOTALL)) != 1:
        raise StateError("gate packet must contain exactly one decision record slot")
    row = approval_for(decision_ref, approvals)
    data["decision"] = row["decision"]
    data["decision_date"] = row["date"]
    data["reviewer"] = row["reviewer"]
    data["status"] = {
        "approved": "approved",
        "rejected": "closed",
        "deferred": "draft",
    }[row["decision"]]
    record = (
        "<!-- DECISION_RECORD_START -->\n"
        f"Decision: **{row['decision']}**  \nDate: {row['date']}  \n"
        f"Reviewer: {row['reviewer']}  \nApproval reference: `{decision_ref}`\n"
        "<!-- DECISION_RECORD_END -->"
    )
    body, count = re.subn(
        r"<!-- DECISION_RECORD_START -->.*?<!-- DECISION_RECORD_END -->",
        record, body, flags=re.DOTALL,
    )
    if count != 1:
        raise StateError("gate packet must contain exactly one decision record slot")
    text = f"---\n{render_frontmatter(data)}\n---\n{body}"
    temp = packet.with_suffix(packet.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8", newline="")
    temp.replace(packet)
    record_gate_decision(gate, decision_ref, state_path=state,
                         approvals=approvals, log=log)
    return row


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--gate", required=True)
    create.add_argument("--supplier", required=True)
    create.add_argument("--decision-ref", required=True)
    create.add_argument("--summary", required=True)
    create.add_argument("--evidence", required=True)
    create.add_argument("--validation", required=True)
    create.add_argument("--output", type=Path)
    create.add_argument("--template", type=Path, default=TEMPLATE)
    record = sub.add_parser("record")
    record.add_argument("packet", type=Path)
    record.add_argument("--state", type=Path, default=DEFAULT_STATE)
    record.add_argument("--approvals", type=Path, default=DEFAULT_APPROVALS)
    record.add_argument("--log", type=Path, default=DEFAULT_LOG)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            output = args.output or GATE_DIR / f"{args.decision_ref}-{args.supplier}.md"
            create_packet(gate=args.gate, supplier=args.supplier,
                          decision_ref=args.decision_ref, summary=args.summary,
                          evidence=args.evidence, validation=args.validation,
                          output=output, template=args.template)
            print(f"created {output}")
            print("STOP: human decision required; no state transition was performed")
        else:
            row = record_packet(args.packet, state=args.state,
                                approvals=args.approvals, log=args.log)
            print(f"recorded {row['decision']}; no state transition was performed")
    except (OSError, StateError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
