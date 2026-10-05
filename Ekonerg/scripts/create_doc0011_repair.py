#!/usr/bin/env python3
"""Create the exact-source DOC-0011 traceability repair candidate."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from project_paths import local_path


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "Revizije i promjene šalju se korisnicima kontroliranih kopija"
EXPECTED = [
    "Revizije i promjene šalju se korisnicima kontroliranih kopija u skladu s postupkom PQ.7.5-5.",
    "Revizije i promjene moraju na dnu svake stranice i naslovnoj stranici imati broj revizije.",
]


def create(source: Path, output: Path) -> None:
    source_path = local_path(source)
    destination = local_path(output)
    if not source_path.is_file() or not source_path.is_relative_to(ROOT / "sieving"):
        raise ValueError("source JSON must be an existing local sieving file")
    if not destination.is_relative_to(ROOT / "sieving") or destination.exists():
        raise ValueError("candidate output must be a new local sieving file")
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    matches = 0
    for item in payload.get("items", []):
        quotes = item.get("evidence_quotes", [])
        for index, quote in enumerate(quotes):
            if quote.get("quote_original", "").startswith(PREFIX):
                if matches:
                    raise ValueError("more than one revision quote found")
                first = copy.deepcopy(quote)
                second = copy.deepcopy(quote)
                first["quote_original"], second["quote_original"] = EXPECTED
                item["evidence_quotes"] = quotes[:index] + [first, second] + quotes[index + 1:]
                matches += 1
    if matches != 1:
        raise ValueError(f"expected one revision quote to split, found {matches}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    create(args.source, args.output)
    print(f"create_doc0011_repair: PASS - {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
