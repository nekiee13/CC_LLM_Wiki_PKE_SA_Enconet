#!/usr/bin/env python3
"""Check local Codex/Claude sieving skill semantics without editing either side."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

from project_paths import local_path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "schemas" / "sieving_skill_contract.yml"
CODEX = ROOT / ".agents" / "skills"
CLAUDE = ROOT / ".claude" / "skills"


def validate(*, contract: Path = CONTRACT, codex: Path = CODEX,
             claude: Path = CLAUDE, allow_pending_claude: bool = False) -> list[str]:
    data = yaml.safe_load(local_path(contract).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("skills"), dict):
        raise ValueError("local sieving skill contract is missing or invalid")
    errors: list[str] = []
    for name, spec in data["skills"].items():
        if not isinstance(name, str) or not name or "/" in name or "\\" in name or name in {".", ".."}:
            errors.append(f"invalid skill name: {name!r}")
            continue
        required = [str(value).casefold() for value in spec["required_semantics"]]
        for agent, root in (("Codex", codex), ("Claude", claude)):
            path = local_path(root / name / "SKILL.md")
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
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"validate_sieving_skill_drift: FAIL - {error}", file=sys.stderr)
    if errors:
        return 1
    suffix = " (Claude side pending)" if args.allow_pending_claude else ""
    print(f"validate_sieving_skill_drift: PASS - local skill semantics{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
