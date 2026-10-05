"""Create immutable, source-exact quote repair candidates.

This script changes only candidate JSON. It does not alter the audit database or
promote a generation. Each replacement is copied from the registered raw source.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sieving" / "candidates" / "repairs-20261005"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def _source_line(source: Path, prefix: str) -> str:
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line
    raise ValueError(f"source line not found: {prefix}")


def _replace_quote(payload: dict, item_id: str, replacement: str, locator: str | None = None) -> None:
    matches = 0
    for item in payload.get("items", []):
        if item.get("item_id") != item_id:
            continue
        for quote in item.get("evidence_quotes", []):
            quote["quote_original"] = replacement
            if locator:
                quote["source_locator"] = locator
            matches += 1
    if matches != 1:
        raise ValueError(f"expected one quote for {item_id}, found {matches}")


def main() -> int:
    source_0011 = ROOT / "raw" / "PQ07.5-2_r8_Postupci_sustava_kvalitete,_sustava_za.md"
    source_0016 = ROOT / "raw" / "PQ07.5-7_r10_Kontrola_zapisa.md"
    source_0021 = ROOT / "raw" / "PQ08.2-2_r5_Priprema_i_postupanje_s_ugovornom_doku.md"

    # DOC-0011: replace flattened list text with the exact chapter block.
    p0011 = _load(ROOT / "docs" / "reviews" / "RUN-20261005-51-export.json")
    source_text = source_0011.read_text(encoding="utf-8")
    start = source_text.index("Opći postupak sustava kvalitete sadrži sljedeće točke:")
    end = source_text.index("\n\n3.3.3.", start)
    _replace_quote(p0011, "CRUMB-DOC-0011-APP_B_VI-0008", source_text[start:end],
                   "POSTUPAK SUSTAVA KVALITETE > 3.2.1.–3.2.4.")
    _write(p0011, OUT / "DOC-0011.json")

    # DOC-0016: correct the singular/plural source wording.
    p0016 = _load(ROOT / "sieving" / "candidates" / "v3-20261005" / "DOC-0016.json")
    exact_0016 = "Zapise s provjere generira tim za provjeru"
    _replace_quote(p0016, "Q09-DOC0016-007", exact_0016,
                   "KONTROLA ZAPISA > 3. POSTUPAK > 3.2. Generiranje zapisa")
    _write(p0016, OUT / "DOC-0016.json")

    # DOC-0021: use the complete clause 3.3.5 line and cite that clause.
    p0021 = _load(ROOT / "sieving" / "candidates" / "v3-20261005" / "DOC-0021.json")
    exact_0021 = _source_line(source_0021, "3.3.5.")
    _replace_quote(p0021, "Q12-DOC0021-006", exact_0021,
                   "PRIPREMA I POSTUPANJE S UGOVORNOM DOKUMENTACIJOM > 3.3.5.")
    _write(p0021, OUT / "DOC-0021.json")

    manifest = []
    for path in sorted(OUT.glob("DOC-*.json")):
        manifest.append({"file": str(path.relative_to(ROOT)),
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    (OUT / "manifest.json").write_text(
        json.dumps({"schema_version": "1.0", "source_exact": True, "files": manifest},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"created {len(manifest)} strict quote repair candidates in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
