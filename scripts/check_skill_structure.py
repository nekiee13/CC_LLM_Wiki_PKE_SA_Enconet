#!/usr/bin/env python3
"""Skill-structure validator (Task C2.3, ADR-0014/0016).

Scans the Claude Code and Codex skill trees at every scope and fails when the
same skill name appears at two scopes whose resolution order overlaps — i.e.
when it is ambiguous which copy owns the name:

  scopes per agent:  user-global (~/.claude/skills, ~/.agents/skills)
                     workspace   (<root>/.claude/skills, <root>/.agents/skills)
                     project     (<root>/<project>/.{claude,agents}/skills)

Rules enforced (exit 1 on any violation):
  1. Same agent, same skill name at two nesting scopes (global/workspace,
     global/project, workspace/project) — conflicting ownership.
  2. Paired skills (same name on both agents) must live at the SAME scope on
     both sides (ADR-0014 pattern: /handoff is user-global on both).
  3. A skill directory must contain SKILL.md — anything else is malformed.

Same name in two different *projects* (same agent) does not conflict: project
scopes never shadow each other. Reading Codex trees is allowed under ADR-0016;
this tool never writes anywhere.

Stdlib only. Usage:
    python scripts/check_skill_structure.py             # validate, exit 0/1
    python scripts/check_skill_structure.py --list      # show the inventory
    # test hooks: --workspace-root, --claude-home, --codex-home
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AGENT_DIRS = {"claude-code": ".claude", "codex": ".agents"}


def scan_scope(root: Path) -> dict[str, list[str]]:
    """Return {skill_name: [problems]} for one <...>/skills directory."""
    skills: dict[str, list[str]] = {}
    if not root.is_dir():
        return skills
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue  # stray files next to skill dirs are not skills
        problems = []
        if not (entry / "SKILL.md").is_file():
            problems.append("missing SKILL.md")
        skills[entry.name] = problems
    return skills


def collect(workspace_root: Path, claude_home: Path, codex_home: Path):
    """Return [(agent, scope_kind, scope_label, {name: problems})]."""
    homes = {"claude-code": claude_home, "codex": codex_home}
    scopes = []
    for agent, dot in AGENT_DIRS.items():
        scopes.append((agent, "user-global", "~", homes[agent] / "skills"))
        scopes.append((agent, "workspace", "<workspace>",
                       workspace_root / dot / "skills"))
        for child in sorted(p for p in workspace_root.iterdir() if p.is_dir()):
            if child.name.startswith(".") or child.name in ("scripts", "doc"):
                continue
            candidate = child / dot / "skills"
            if candidate.is_dir():
                scopes.append((agent, f"project:{child.name}", child.name,
                               candidate))
    return [(agent, kind, label, scan_scope(path), path)
            for agent, kind, label, path in scopes]


def nesting_conflict(kind_a: str, kind_b: str) -> bool:
    """Two scopes conflict unless both are (distinct) project scopes."""
    if kind_a == kind_b:
        return not kind_a.startswith("project:")
    both_projects = kind_a.startswith("project:") and kind_b.startswith("project:")
    return not both_projects


def validate(entries) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    infos: list[str] = []

    # Rule 3: malformed skill directories.
    for agent, kind, _label, skills, path in entries:
        for name, problems in skills.items():
            for problem in problems:
                errors.append(f"[{agent}] {kind} skill '{name}': {problem} "
                              f"({path / name})")

    # Rule 1: same agent, same name, overlapping scopes.
    for agent in AGENT_DIRS:
        seen: dict[str, list[tuple[str, Path]]] = {}
        for entry_agent, kind, _label, skills, path in entries:
            if entry_agent != agent:
                continue
            for name in skills:
                seen.setdefault(name, []).append((kind, path))
        for name, locations in seen.items():
            for i in range(len(locations)):
                for j in range(i + 1, len(locations)):
                    (kind_a, path_a), (kind_b, path_b) = locations[i], locations[j]
                    if nesting_conflict(kind_a, kind_b):
                        errors.append(
                            f"[{agent}] duplicate skill '{name}' with "
                            f"conflicting ownership: {kind_a} ({path_a}) vs "
                            f"{kind_b} ({path_b})")

    # Rule 2: paired skills must sit at the same scope on both agents.
    by_agent: dict[str, dict[str, set[str]]] = {a: {} for a in AGENT_DIRS}
    for agent, kind, _label, skills, _path in entries:
        for name in skills:
            by_agent[agent].setdefault(name, set()).add(kind)
    shared = set(by_agent["claude-code"]) & set(by_agent["codex"])
    for name in sorted(shared):
        cc, cx = by_agent["claude-code"][name], by_agent["codex"][name]
        if cc == cx:
            infos.append(f"paired skill '{name}' at scope(s) "
                         f"{', '.join(sorted(cc))} on both sides")
        else:
            errors.append(f"paired skill '{name}' scope mismatch: "
                          f"claude-code={sorted(cc)} vs codex={sorted(cx)}")
    return errors, infos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true",
                        help="print the full skill inventory")
    parser.add_argument("--workspace-root", type=Path,
                        default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--claude-home", type=Path,
                        default=Path.home() / ".claude")
    parser.add_argument("--codex-home", type=Path,
                        default=Path.home() / ".agents")
    args = parser.parse_args()

    entries = collect(args.workspace_root.resolve(), args.claude_home,
                      args.codex_home)

    if args.list:
        for agent, kind, _label, skills, path in entries:
            names = ", ".join(sorted(skills)) if skills else "(none)"
            print(f"{agent:11s} {kind:20s} {path} -> {names}")

    errors, infos = validate(entries)
    for info in infos:
        print(f"INFO  {info}")
    for error in errors:
        print(f"ERROR {error}")
    total = sum(len(skills) for _a, _k, _l, skills, _p in entries)
    print(f"skill-structure: {len(errors)} error(s); {total} skill "
          f"location(s) scanned.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
