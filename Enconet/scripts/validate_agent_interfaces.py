#!/usr/bin/env python3
"""Validate EPIC17 Codex and Claude adapters against the canonical command registry."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from audit_command import REGISTRY, ROOT, load_registry


AGENTS = ROOT / "AGENTS.md"
CLAUDE_COMMANDS = ROOT / ".claude" / "commands"


def validate(
    *, agents: Path = AGENTS, claude_commands: Path = CLAUDE_COMMANDS,
    registry: Path = REGISTRY, allow_pending_claude: bool = False,
) -> list[str]:
    errors: list[str] = []
    specs = load_registry(registry)
    agents_text = agents.read_text(encoding="utf-8")
    for name, spec in specs.items():
        phases = ", ".join(str(item) for item in spec["phases"])
        if f"`{name}`" not in agents_text:
            errors.append(f"AGENTS.md does not list {name}")
        if f"`{phases}`" not in agents_text:
            errors.append(f"AGENTS.md phase contract differs for {name}")
        if f"audit_command.py {name}" not in agents_text:
            errors.append(f"AGENTS.md does not route {name} through the dispatcher")
        command_file = claude_commands / f"{name}.md"
        if not command_file.exists():
            if not allow_pending_claude:
                errors.append(f"Claude adapter is missing: {command_file}")
            continue
        text = command_file.read_text(encoding="utf-8")
        if "scripts/audit_command.py" not in text or name not in text:
            errors.append(f"Claude adapter bypasses canonical dispatcher: {command_file}")
        if phases not in text:
            errors.append(f"Claude adapter phase contract differs: {command_file}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=Path, default=AGENTS)
    parser.add_argument("--claude-commands", type=Path, default=CLAUDE_COMMANDS)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--allow-pending-claude", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(agents=args.agents, claude_commands=args.claude_commands,
                          registry=args.registry,
                          allow_pending_claude=args.allow_pending_claude)
    except (OSError, ValueError) as exc:
        print(f"validate_agent_interfaces: FAIL - {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"validate_agent_interfaces: FAIL - {len(errors)} error(s)", file=sys.stderr)
        return 1
    suffix = " (Claude synchronization pending)" if args.allow_pending_claude else ""
    print(f"validate_agent_interfaces: PASS - {len(load_registry(args.registry))} commands{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
