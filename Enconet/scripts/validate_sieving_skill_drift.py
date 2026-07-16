#!/usr/bin/env python3
"""Validate equivalent Codex/Claude sieving-skill semantics with tool-specific wording allowed."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "schemas" / "sieving_skill_contract.yml"
CODEX = ROOT / ".agents" / "skills"
CLAUDE = ROOT / ".claude" / "skills"


def validate(
    *, contract: Path = CONTRACT, codex: Path = CODEX, claude: Path = CLAUDE,
    allow_pending_claude: bool = False,
) -> list[str]:
    data = yaml.safe_load(contract.read_text(encoding="utf-8"))
    errors: list[str] = []
    for name, spec in data["skills"].items():
        required = [str(value).casefold() for value in spec["required_semantics"]]
        for agent, root in (("Codex", codex), ("Claude", claude)):
            path = root / name / "SKILL.md"
            if not path.is_file():
                if agent == "Claude" and allow_pending_claude:
                    continue
                errors.append(f"{agent} skill missing: {name}")
                continue
            text = path.read_text(encoding="utf-8").casefold()
            for marker in required:
                if marker not in text:
                    errors.append(f"{agent} {name} lacks semantic marker: {marker}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--codex", type=Path, default=CODEX)
    parser.add_argument("--claude", type=Path, default=CLAUDE)
    parser.add_argument("--allow-pending-claude", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(contract=args.contract, codex=args.codex, claude=args.claude,
                          allow_pending_claude=args.allow_pending_claude)
    except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"validate_sieving_skill_drift: FAIL - {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"validate_sieving_skill_drift: FAIL - {len(errors)} error(s)", file=sys.stderr)
        return 1
    suffix = " (Claude synchronization pending)" if args.allow_pending_claude else ""
    print(f"validate_sieving_skill_drift: PASS - 3 paired skills{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
