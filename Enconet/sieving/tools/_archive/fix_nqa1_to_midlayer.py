# ------------------------
# fix_nqa1_to_midlayer.py
# ------------------------
#!/usr/bin/env python3
"""
fix_nqa1_to_midlayer.py

Deterministically normalize an ASME NQA-1 extraction JSON so it can be used as the
"mid-layer DOCUMENT" (interpretive guidance) aligned to 10CFR50 Appendix B.

Key outcomes (repo-aligned, pipeline-friendly):
- Treat NQA-1 as DOCUMENT (never RULE):
    document.record_side = "DOCUMENT"
    items[].record_side  = "DOCUMENT"

- Keep strict APP_B taxonomy classification:
    items[].taxonomy_id  = "APP_B"
    items[].criterion_id must be one of APP_B_I .. APP_B_XVIII
    items[].criterion_name must match canonical for criterion_id (fixed if wrong/missing)

- Add deterministic join links to Appendix B via DOCUMENT-side references:
    items[].rule_reference_ids = ["10CFR50_APPB::APP_B_<X>"]
  (adds if missing; optionally overwrite with --force)

- Enforce minimal item-level requirements the pipeline expects:
    item_id, record_side, template_id, template_version, taxonomy_id, criterion_id,
    criterion_name, item_type, statement, evidence_quotes (>=1), source (>=1 object)

- Add required-but-empty entities structure (arrays):
    organizations, people, documents, systems_tools, standards_regulations

- Ensure each source entry has at least:
    block_type (valid enum, else "other")
    location_cue (string, auto-filled if missing)

- Keep additional metadata if present; do not remove fields unless requested.

Usage:
  python fix_nqa1_to_midlayer.py --in ASME_NQA-1.json --out ASME_NQA-1__DOCUMENT__midlayer.json
  python fix_nqa1_to_midlayer.py --in ASME_NQA-1.json --out fixed.json --force

Notes:
- This script does not "invent" content; it only:
  - normalizes required structural keys
  - repairs obvious schema violations
  - adds deterministic Appendix B join keys based on criterion_id
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


TEMPLATE_ID = "JSON_Template_App_B"
TEMPLATE_VERSION = "0.1"
TAXONOMY_ID = "APP_B"
APPB_REF_CODE = "10CFR50_APPB"

CRITERIA_CANON: Dict[str, str] = {
    "APP_B_I": "Organization",
    "APP_B_II": "Quality Assurance Program",
    "APP_B_III": "Design Control",
    "APP_B_IV": "Procurement Document Control",
    "APP_B_V": "Instructions, Procedures, and Drawings",
    "APP_B_VI": "Document Control",
    "APP_B_VII": "Control of Purchased Material, Equipment, and Services",
    "APP_B_VIII": "Identification and Control of Materials, Parts, and Components",
    "APP_B_IX": "Control of Special Processes",
    "APP_B_X": "Inspection",
    "APP_B_XI": "Test Control",
    "APP_B_XII": "Control of Measuring and Test Equipment",
    "APP_B_XIII": "Handling, Storage, and Shipping",
    "APP_B_XIV": "Inspection, Test, and Operating Status",
    "APP_B_XV": "Nonconforming Materials, Parts, or Components",
    "APP_B_XVI": "Corrective Action",
    "APP_B_XVII": "Quality Assurance Records",
    "APP_B_XVIII": "Audits",
}

ITEM_TYPE_ALLOWED = {
    "requirement",
    "process_step",
    "role_responsibility",
    "definition",
    "control",
    "record",
    "reference",
    "finding",
    "recommendation",
    "action",
    "status_statement",
    "other",
}

BLOCK_TYPE_ALLOWED = {
    "heading",
    "prose",
    "table",
    "diagram",
    "list",
    "figure",
    "footer",
    "header",
    "annex",
    "other",
}

REQUIRED_ENTITIES_KEYS = [
    "organizations",
    "people",
    "documents",
    "systems_tools",
    "standards_regulations",
]


@dataclass
class FixStats:
    items_total: int = 0
    items_fixed: int = 0
    document_fixed: int = 0
    added_rule_reference_ids: int = 0
    overwritten_rule_reference_ids: int = 0
    fixed_criterion_name: int = 0
    fixed_item_type: int = 0
    fixed_evidence_quotes: int = 0
    fixed_source: int = 0
    fixed_entities: int = 0
    added_missing_item_id: int = 0
    warnings: int = 0


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: JSON decode error in {path}: {e}") from e
    except OSError as e:
        raise SystemExit(f"ERROR: Cannot read {path}: {e}") from e

    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: Root JSON must be an object/dict: {path}")
    return data


def save_json(path: Path, data: Dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except OSError as e:
        raise SystemExit(f"ERROR: Cannot write {path}: {e}") from e


def ensure_document_root(data: Dict[str, Any], stats: FixStats) -> None:
    """
    Ensure document root exists and contains required keys consumed by pipeline:
    - template_id, template_version, record_side
    Keep existing doc_id/filename/title/control_metadata if present.
    """
    doc = data.get("document")
    if not isinstance(doc, dict):
        doc = {}
        data["document"] = doc
        stats.document_fixed += 1

    changed = False

    if doc.get("template_id") != TEMPLATE_ID:
        doc["template_id"] = TEMPLATE_ID
        changed = True
    if doc.get("template_version") != TEMPLATE_VERSION:
        doc["template_version"] = TEMPLATE_VERSION
        changed = True

    # Mid-layer must be DOCUMENT
    if doc.get("record_side") != "DOCUMENT":
        doc["record_side"] = "DOCUMENT"
        changed = True

    # Ensure control_metadata exists (pipeline consumes revision, but keep optional fields)
    cm = doc.get("control_metadata")
    if cm is None or not isinstance(cm, dict):
        doc["control_metadata"] = {"revision": doc.get("revision") or None}
        changed = True
    else:
        if "revision" not in cm:
            cm["revision"] = None
            changed = True

    if changed:
        stats.document_fixed += 1


def normalize_item_type(item_type: Any) -> str:
    if isinstance(item_type, str):
        t = item_type.strip()
        if t in ITEM_TYPE_ALLOWED:
            return t
    return "other"


def ensure_nonempty_string(value: Any) -> Optional[str]:
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    return None


def ensure_evidence_quotes(item: Dict[str, Any], stats: FixStats) -> None:
    ev = item.get("evidence_quotes")
    quotes: List[str] = []
    if isinstance(ev, list):
        for q in ev:
            s = ensure_nonempty_string(q)
            if s:
                quotes.append(s)

    if not quotes:
        # Fallback: use statement if present; else a placeholder to satisfy non-empty requirement
        stmt = ensure_nonempty_string(item.get("statement"))
        if stmt:
            quotes = [stmt]
        else:
            quotes = ["AUTO:missing_evidence_quote"]

        item["evidence_quotes"] = quotes
        stats.fixed_evidence_quotes += 1
    else:
        # keep cleaned list (strip empties)
        if quotes != ev:
            item["evidence_quotes"] = quotes
            stats.fixed_evidence_quotes += 1


def ensure_source(item: Dict[str, Any], stats: FixStats) -> None:
    src = item.get("source")
    changed = False

    if not isinstance(src, list) or len(src) == 0:
        item["source"] = [{
            "page": None,
            "page_label": None,
            "heading_path": [],
            "section_id": None,
            "block_type": "other",
            "location_cue": "AUTO:missing_source",
        }]
        stats.fixed_source += 1
        return

    # Normalize each source entry minimally
    for i, s in enumerate(src):
        if not isinstance(s, dict):
            src[i] = {
                "page": None,
                "page_label": None,
                "heading_path": [],
                "section_id": None,
                "block_type": "other",
                "location_cue": f"AUTO:invalid_source_entry:{i}",
            }
            changed = True
            continue

        bt = s.get("block_type")
        bt_norm = bt.strip() if isinstance(bt, str) else "other"
        if bt_norm not in BLOCK_TYPE_ALLOWED:
            bt_norm = "other"
        if s.get("block_type") != bt_norm:
            s["block_type"] = bt_norm
            changed = True

        lc = ensure_nonempty_string(s.get("location_cue"))
        if not lc:
            # Try to derive from heading_path if present
            hp = s.get("heading_path")
            if isinstance(hp, list) and hp and all(isinstance(x, str) for x in hp):
                lc = "AUTO:" + " > ".join([x.strip() for x in hp if x.strip()])[:240]
            else:
                lc = f"AUTO:missing_location_cue:{i}"
            s["location_cue"] = lc
            changed = True

        # Ensure heading_path is list of strings (optional but helpful)
        hp = s.get("heading_path")
        if hp is None:
            s["heading_path"] = []
            changed = True
        elif isinstance(hp, list):
            cleaned = [x.strip() for x in hp if isinstance(x, str) and x.strip()]
            if cleaned != hp:
                s["heading_path"] = cleaned
                changed = True
        else:
            s["heading_path"] = []
            changed = True

    if changed:
        stats.fixed_source += 1


def ensure_entities(item: Dict[str, Any], stats: FixStats) -> None:
    ent = item.get("entities")
    if not isinstance(ent, dict):
        ent = {}
        item["entities"] = ent
        stats.fixed_entities += 1

    changed = False
    for k in REQUIRED_ENTITIES_KEYS:
        v = ent.get(k)
        if not isinstance(v, list):
            ent[k] = []
            changed = True

    if changed:
        stats.fixed_entities += 1


def ensure_rule_reference_ids_midlayer(
    item: Dict[str, Any],
    criterion_id: str,
    stats: FixStats,
    force: bool,
) -> None:
    """
    For mid-layer DOCUMENT NQA-1, link each item to Appendix B criterion using:
      rule_reference_ids = ["10CFR50_APPB::<criterion_id>"]
    """
    desired = [f"{APPB_REF_CODE}::{criterion_id}"]

    existing = item.get("rule_reference_ids")
    if existing is None:
        item["rule_reference_ids"] = desired
        stats.added_rule_reference_ids += 1
        return

    if not isinstance(existing, list):
        item["rule_reference_ids"] = desired
        stats.overwritten_rule_reference_ids += 1
        return

    cleaned = []
    for x in existing:
        s = ensure_nonempty_string(x)
        if s:
            cleaned.append(s)

    if force:
        if cleaned != desired:
            item["rule_reference_ids"] = desired
            stats.overwritten_rule_reference_ids += 1
        else:
            item["rule_reference_ids"] = cleaned
        return

    # If already contains the desired key, keep existing (cleaned)
    if desired[0] in cleaned:
        if cleaned != existing:
            item["rule_reference_ids"] = cleaned
            stats.items_fixed += 1
        return

    # Otherwise append desired
    cleaned.append(desired[0])
    item["rule_reference_ids"] = cleaned
    stats.added_rule_reference_ids += 1


def ensure_required_item_fields(
    item: Dict[str, Any],
    idx: int,
    stats: FixStats,
    force: bool,
) -> Tuple[bool, Optional[str]]:
    """
    Ensure all required item fields exist with correct minimum constraints.
    Returns (changed, error_message_if_unfixable).
    """
    changed = False

    # item_id (required)
    item_id = ensure_nonempty_string(item.get("item_id"))
    if not item_id:
        # Create deterministic id
        item["item_id"] = f"auto_{idx+1:06d}"
        stats.added_missing_item_id += 1
        changed = True

    # Force DOCUMENT side
    if item.get("record_side") != "DOCUMENT":
        item["record_side"] = "DOCUMENT"
        changed = True

    # Template identity
    if item.get("template_id") != TEMPLATE_ID:
        item["template_id"] = TEMPLATE_ID
        changed = True
    if item.get("template_version") != TEMPLATE_VERSION:
        item["template_version"] = TEMPLATE_VERSION
        changed = True
    if item.get("taxonomy_id") != TAXONOMY_ID:
        item["taxonomy_id"] = TAXONOMY_ID
        changed = True

    # Criterion id/name
    cid = ensure_nonempty_string(item.get("criterion_id"))
    if not cid or cid not in CRITERIA_CANON:
        return changed, f"Item {item.get('item_id')} has invalid or missing criterion_id: {cid!r}"

    canon_name = CRITERIA_CANON[cid]
    cname = ensure_nonempty_string(item.get("criterion_name"))
    if cname != canon_name:
        item["criterion_name"] = canon_name
        stats.fixed_criterion_name += 1
        changed = True

    # item_type
    it = normalize_item_type(item.get("item_type"))
    if item.get("item_type") != it:
        item["item_type"] = it
        stats.fixed_item_type += 1
        changed = True

    # statement
    st = ensure_nonempty_string(item.get("statement"))
    if not st:
        # If no statement, try to synthesize from evidence or heading_path, else placeholder.
        ev = item.get("evidence_quotes")
        synthesized = None
        if isinstance(ev, list) and ev:
            synthesized = ensure_nonempty_string(ev[0])
        if not synthesized:
            src = item.get("source")
            if isinstance(src, list) and src and isinstance(src[0], dict):
                hp = src[0].get("heading_path")
                if isinstance(hp, list) and hp:
                    synthesized = " | ".join([x.strip() for x in hp if isinstance(x, str) and x.strip()])[:240]
        item["statement"] = synthesized or "AUTO:missing_statement"
        changed = True

    # evidence_quotes and source are required by pipeline validation
    ensure_evidence_quotes(item, stats)
    ensure_source(item, stats)

    # entities (pipeline flattens certain groups; ensure arrays exist)
    ensure_entities(item, stats)

    # Mid-layer join keys
    ensure_rule_reference_ids_midlayer(item, cid, stats, force=force)

    # Ensure RULE-only object is absent/null to avoid conceptual confusion
    # (If present, remove or null it; safest is set to None)
    if "rule" in item and item.get("rule") not in (None, {}):
        item["rule"] = None
        changed = True

    return changed, None


def fix_midlayer_nqa1(data: Dict[str, Any], force_rule_refs: bool) -> Tuple[Dict[str, Any], FixStats]:
    stats = FixStats()

    ensure_document_root(data, stats)

    items = data.get("items")
    if not isinstance(items, list):
        raise SystemExit("ERROR: Root must contain 'items' as a list.")

    stats.items_total = len(items)

    errors: List[str] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            # Replace invalid item with minimal placeholder (but cannot infer criterion_id)
            errors.append(f"Item index {idx} is not an object/dict.")
            continue

        changed, err = ensure_required_item_fields(item, idx, stats, force=force_rule_refs)
        if err:
            errors.append(err)
            continue

        if changed:
            stats.items_fixed += 1

    if errors:
        # Fail fast: invalid criterion_id cannot be guessed safely.
        msg = "ERROR: Unfixable issues detected:\n" + "\n".join(f"- {e}" for e in errors[:50])
        if len(errors) > 50:
            msg += f"\n... and {len(errors) - 50} more."
        raise SystemExit(msg)

    # Optionally: promote any top-level "organizations"/"documents" etc. into document metadata?
    # Do not modify: keep as-is. Pipeline ignores these root extras.

    return data, stats


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Normalize ASME NQA-1 JSON into mid-layer DOCUMENT for Appendix B.")
    p.add_argument("--in", dest="in_path", required=True, help="Input JSON path (ASME NQA-1 extraction).")
    p.add_argument("--out", dest="out_path", required=True, help="Output JSON path (fixed mid-layer).")
    p.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite rule_reference_ids to exactly ['10CFR50_APPB::<criterion_id>'] for every item.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    in_path = Path(args.in_path)
    out_path = Path(args.out_path)

    data = load_json(in_path)
    fixed, stats = fix_midlayer_nqa1(data, force_rule_refs=bool(args.force))
    save_json(out_path, fixed)

    print("OK: wrote fixed mid-layer JSON")
    print(f"- Input:  {in_path}")
    print(f"- Output: {out_path}")
    print("")
    print("Stats:")
    print(f"- items_total: {stats.items_total}")
    print(f"- items_fixed: {stats.items_fixed}")
    print(f"- document_fixed: {stats.document_fixed}")
    print(f"- added_missing_item_id: {stats.added_missing_item_id}")
    print(f"- fixed_criterion_name: {stats.fixed_criterion_name}")
    print(f"- fixed_item_type: {stats.fixed_item_type}")
    print(f"- fixed_evidence_quotes: {stats.fixed_evidence_quotes}")
    print(f"- fixed_source: {stats.fixed_source}")
    print(f"- fixed_entities: {stats.fixed_entities}")
    print(f"- added_rule_reference_ids: {stats.added_rule_reference_ids}")
    print(f"- overwritten_rule_reference_ids: {stats.overwritten_rule_reference_ids}")


if __name__ == "__main__":
    main()
