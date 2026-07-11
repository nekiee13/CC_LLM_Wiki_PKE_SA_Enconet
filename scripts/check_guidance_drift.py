#!/usr/bin/env python3
"""Guidance-pair semantic drift validator (Task C2.1, ADR-0005/0016).

Checks that every anchor rule in doc/GUIDANCE_PAIRS.json matches BOTH sides of
each guidance pair (CLAUDE.md <-> AGENTS.md, and the handoff skill pair).
Documented tool-specific differences are reported as informational; a missing
anchor on either side is silent divergence and fails the run (exit 1).

Stdlib only. Usage:
    python scripts/check_guidance_drift.py            # validate, exit 0/1
    python scripts/check_guidance_drift.py --list     # show rules per pair
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "doc" / "GUIDANCE_PAIRS.json"
SIDES = ("claude", "codex")


def resolve_path(spec: str) -> Path:
    if spec.startswith("~/") or spec == "~":
        return Path.home() / spec[2:]
    return ROOT / spec


def rule_patterns(rule: dict, side: str) -> list[str]:
    """Side-specific patterns win over common ones; 'patterns' wins over 'pattern'."""
    for key in (f"{side}_patterns", f"{side}_pattern", "patterns", "pattern"):
        if key in rule:
            value = rule[key]
            return list(value) if isinstance(value, list) else [value]
    return []


def check_pair(pair: dict) -> tuple[list[str], list[str]]:
    """Return (errors, infos) for one guidance pair."""
    errors: list[str] = []
    infos: list[str] = []
    pair_id = pair["id"]

    texts: dict[str, str] = {}
    for side in SIDES:
        path = resolve_path(pair[side])
        if not path.is_file():
            errors.append(f"[{pair_id}] {side} file missing: {pair[side]}")
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        # Collapse whitespace runs so anchors match across hard line wraps.
        texts[side] = re.sub(r"\s+", " ", raw)

    if len(texts) < len(SIDES):
        return errors, infos  # cannot compare without both sides

    for rule in pair.get("rules", []):
        rule_id = rule.get("id", "<unnamed>")
        for side in SIDES:
            patterns = rule_patterns(rule, side)
            if not patterns:
                errors.append(f"[{pair_id}] rule '{rule_id}' has no pattern for side '{side}'")
                continue
            missing = [p for p in patterns
                       if not re.search(p, texts[side], re.IGNORECASE | re.DOTALL)]
            if missing:
                errors.append(
                    f"[{pair_id}] SILENT DIVERGENCE rule '{rule_id}': "
                    f"{side} side ({pair[side]}) does not match: {missing}"
                )

    for diff in pair.get("documented_differences", []):
        infos.append(f"[{pair_id}] documented difference '{diff['id']}': {diff['description']}")

    return errors, infos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true", help="list rules and exit")
    parser.add_argument("--quiet", action="store_true", help="suppress informational output")
    args = parser.parse_args()

    if not MANIFEST.is_file():
        print(f"ERROR: manifest not found: {MANIFEST}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pairs = manifest.get("pairs", [])

    if args.list:
        for pair in pairs:
            print(f"{pair['id']}: {pair['claude']} <-> {pair['codex']}")
            for rule in pair.get("rules", []):
                print(f"  anchor  {rule.get('id')}: {rule.get('description', '')}")
            for diff in pair.get("documented_differences", []):
                print(f"  allowed {diff['id']}: {diff['description']}")
        return 0

    all_errors: list[str] = []
    total_rules = 0
    total_diffs = 0
    for pair in pairs:
        errors, infos = check_pair(pair)
        total_rules += len(pair.get("rules", []))
        total_diffs += len(pair.get("documented_differences", []))
        all_errors.extend(errors)
        if not args.quiet:
            for line in infos:
                print(f"INFO  {line}")
    for line in all_errors:
        print(f"ERROR {line}", file=sys.stderr)

    print(
        f"guidance-drift: {len(all_errors)} error(s); "
        f"{len(pairs)} pair(s), {total_rules} anchor rule(s), "
        f"{total_diffs} documented difference(s)."
    )
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
