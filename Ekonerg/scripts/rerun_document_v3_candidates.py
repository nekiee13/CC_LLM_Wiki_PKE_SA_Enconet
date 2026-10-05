#!/usr/bin/env python3
"""Prepare v3 DOCUMENT sieve payloads from the reviewed local source set.

The project has no local model runner.  This helper therefore keeps every
existing, source-quoted crumb and adds only clearly source-supported
candidate leads from the v3 concept sweep.  It never changes the database;
``resieve_run.py`` remains the guarded import path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path


PROMPT = "appb_document_v3_context_anchors"
CRITERIA = {
    "APP_B_VIII": "Identification and Control of Materials, Parts, and Components",
    "APP_B_IX": "Control of Special Processes",
    "APP_B_XI": "Test Control",
    "APP_B_XIII": "Handling, Storage, and Shipping",
    "APP_B_XIV": "Inspection, Test, and Operating Status",
}

# These are recall signals, not proof of compliance.  The source quote is
# retained verbatim and the statement deliberately remains a candidate lead.
SIGNALS = {
    "APP_B_VIII": re.compile(r"identifik|ozna[cč]|sljediv|serij|status|materijal|konfigur", re.I),
    "APP_B_IX": re.compile(r"specijal|zavar|toplin|bezrazorn|kvalifik|parametr|NDE|WPS", re.I),
    "APP_B_XI": re.compile(r"ispitiv|test|kriterij|rezultat|izvje|prihvat|ponov", re.I),
    "APP_B_XIII": re.compile(r"rukov|skladi|[čc]uv|za[sš]tit|pakir|transport|[čc]isto|okoli[sš]", re.I),
    "APP_B_XIV": re.compile(r"status|zadr[sž]|pu[sš]t|prihvat|odbij|pregled|verifik|kontrol", re.I),
}


def _key(value: str) -> str:
    """Make a safe comparison key for truncated/Unicode file names."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _source_for(name: str, incoming: Path) -> Path:
    wanted = _key(name)
    exact = [path for path in incoming.glob("*.md") if _key(path.name) == wanted]
    if exact:
        return exact[0]
    prefix = _key(name)[:24]
    matches = [path for path in incoming.glob("*.md") if _key(path.name).startswith(prefix)]
    if len(matches) == 1:
        return matches[0]
    raise ValueError(f"cannot map registered source {name!r}: {matches}")


def _headings(text: str) -> list[tuple[int, str]]:
    stack: list[str] = []
    result: list[tuple[int, str]] = []
    for raw in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", raw)
        if not match:
            continue
        level, title = len(match.group(1)), match.group(2).strip("# ")
        stack = stack[: level - 1]
        stack.append(title)
        result.append((len(result), " > ".join(stack)))
    return result


def _chapter_lines(text: str) -> list[tuple[str, str]]:
    """Return non-heading source lines paired with the current chapter path."""
    path: list[str] = []
    rows: list[tuple[str, str]] = []
    for raw in text.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", raw)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip("# ")
            path = path[: level - 1] + [title]
            continue
        line = raw.strip()
        if not line or line.startswith("![](") or set(line) <= {"|", "-", ":", " ", "`"}:
            continue
        rows.append((line, " > ".join(path) or "SOURCE"))
    return rows


def _existing_quotes(items: list[dict]) -> set[str]:
    return {
        quote.get("quote_original", "")
        for item in items
        for quote in item.get("evidence_quotes", [])
        if isinstance(quote, dict)
    }


def prepare(payload: dict, source: Path) -> dict:
    items = list(payload.get("items", []))
    existing_criteria = {item.get("criterion_id") for item in items}
    quotes = _existing_quotes(items)
    next_number = len(items) + 1
    for criterion, pattern in SIGNALS.items():
        # Existing v1/v2 output already covered this concept.  v3 adds leads
        # only where the old run had no crumb, which keeps the diff reviewable.
        if criterion in existing_criteria:
            continue
        added = 0
        for line, locator in _chapter_lines(source.read_text(encoding="utf-8")):
            if len(line) < 25 or len(line) > 700 or line in quotes or not pattern.search(line):
                continue
            item_id = f"V3-{payload['document']['doc_id']}-{criterion}-{next_number:04d}"
            items.append({
                "item_id": item_id,
                "criterion_id": criterion,
                "criterion_name": CRITERIA[criterion],
                "statement": (
                    "candidate_lead: The source mentions a concept related to "
                    f"{CRITERIA[criterion]}; verify the control, implementation, "
                    "and objective records during the audit."
                ),
                "item_type": "candidate_lead",
                "entities": {},
                "sources": [{"source_locator": locator}],
                "evidence_quotes": [{
                    "quote_original": line,
                    "quote_language": "hr",
                    "source_locator": locator,
                }],
            })
            quotes.add(line)
            next_number += 1
            added += 1
            if added >= 4:
                break
    payload["prompt_version"] = PROMPT
    payload["items"] = items
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("Ekonerg/sieving/DATA/production/2026-10-03"))
    parser.add_argument("--incoming", type=Path, default=Path("Ekonerg/incoming"))
    parser.add_argument("--output-dir", type=Path, default=Path("Ekonerg/sieving/candidates/v3-20261005"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    generated = 0
    manifest: list[dict[str, object]] = []
    for path in sorted(args.input_dir.glob("q*_doc*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        source = _source_for(payload["document"]["name"], args.incoming)
        result = prepare(payload, source)
        target = args.output_dir / f"{payload['document']['doc_id']}.json"
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        manifest.append({
            "doc_id": payload["document"]["doc_id"],
            "source": str(source),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "payload": str(target),
            "payload_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "prompt_version": PROMPT,
            "item_count": len(result["items"]),
        })
        print(f"{payload['document']['doc_id']} source={source.name} items={len(result['items'])} -> {target}")
        generated += 1
    (args.output_dir / "manifest.json").write_text(
        json.dumps({"schema_version": "1.0", "prompt_version": PROMPT,
                    "generated_files": generated, "documents": manifest},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    print(f"generated={generated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
