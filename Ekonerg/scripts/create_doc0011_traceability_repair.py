"""Create an exact-source DOC-0011 candidate for the list quote."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_ITEM = "CRUMB-DOC-0011-APP_B_VI-0008"
PREFIX = "Opći postupak sustava kvalitete sadrži sljedeće točke:"
SOURCE = ROOT / "raw" / "PQ07.5-2_r8_Postupci_sustava_kvalitete,_sustava_za.md"


def exact_quote() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    start = text.index(PREFIX)
    end = text.index("\n\n3.3.3.", start)
    return text[start:end]


def create(source: Path, output: Path) -> None:
    if output.exists():
        raise ValueError(f"output already exists: {output}")
    payload = json.loads(source.read_text(encoding="utf-8"))
    replacement = exact_quote()
    matches = 0
    for item in payload.get("items", []):
        if item.get("item_id") != TARGET_ITEM:
            continue
        for quote in item.get("evidence_quotes", []):
            if quote.get("quote_original", "").startswith(PREFIX):
                quote["quote_original"] = replacement
                matches += 1
    if matches != 1:
        raise ValueError(f"expected one target quote, found {matches}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    create(args.source, args.output)
    print(f"create_doc0011_traceability_repair: PASS - {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
