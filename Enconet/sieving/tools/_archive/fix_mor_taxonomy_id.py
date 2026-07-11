# ------------------------
# fix_mor_taxonomy_id.py
# ------------------------
#!/usr/bin/env python3
"""
Fix taxonomy_id errors in APP_B extraction JSON files.

Problem observed:
  items[].taxonomy_id incorrectly set to APP_B_I / APP_B_II / ... (criterion_id values)

Repo-enforced requirement:
  items[].taxonomy_id must be exactly "APP_B"

This script:
- Creates a .bak backup for each modified file
- Repairs taxonomy_id and (when needed) criterion_id / criterion_name
- Prints a summary of changes
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Tuple

APP_B_CRITERIA: Dict[str, str] = {
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


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def fix_item(item: Dict[str, Any]) -> Tuple[int, int]:
    """
    Returns: (num_fixes, num_warnings)
    """
    fixes = 0
    warns = 0

    tax = (item.get("taxonomy_id") or "").strip()
    crit = (item.get("criterion_id") or "").strip()
    crit_name = (item.get("criterion_name") or "").strip()

    # Case A: taxonomy_id mistakenly set to a criterion id
    if tax in APP_B_CRITERIA and crit == tax:
        item["taxonomy_id"] = "APP_B"
        fixes += 1

        # Ensure criterion_name is canonical (optional but strongly recommended)
        canonical = APP_B_CRITERIA.get(crit, "")
        if canonical and crit_name and crit_name != canonical:
            item["criterion_name"] = canonical
            fixes += 1
        elif canonical and not crit_name:
            item["criterion_name"] = canonical
            fixes += 1

        return fixes, warns

    # Case B: taxonomy_id is a criterion id, criterion_id missing/empty -> migrate
    if tax in APP_B_CRITERIA and not crit:
        item["taxonomy_id"] = "APP_B"
        item["criterion_id"] = tax
        fixes += 2

        canonical = APP_B_CRITERIA[tax]
        if crit_name != canonical:
            item["criterion_name"] = canonical
            fixes += 1

        return fixes, warns

    # Case C: taxonomy_id is wrong in some other way -> do not auto-change blindly
    if tax and tax != "APP_B":
        # If it looks like APP_B_* but not recognized (e.g., typo), warn
        if tax.upper().startswith("APP_B_"):
            warns += 1

    return fixes, warns


def fix_file(path: Path) -> Tuple[bool, int, int]:
    """
    Returns: (modified, total_fixes, total_warnings)
    """
    obj = load_json(path)
    items = obj.get("items")
    if not isinstance(items, list):
        return False, 0, 0

    total_fixes = 0
    total_warns = 0
    for it in items:
        if isinstance(it, dict):
            f, w = fix_item(it)
            total_fixes += f
            total_warns += w

    modified = total_fixes > 0
    if modified:
        backup = path.with_suffix(path.suffix + ".bak")
        if not backup.exists():
            backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        save_json(path, obj)

    return modified, total_fixes, total_warns


def main() -> None:
    repo_root = Path.cwd()

    # Adjust if your DATA directory is elsewhere
    data_dir = repo_root / "DATA" / "DOCUMENT"
    if not data_dir.exists():
        raise SystemExit(f"DATA folder not found at: {data_dir}")

    paths = sorted(data_dir.rglob("*.json"))
    if not paths:
        raise SystemExit(f"No JSON files found under: {data_dir}")

    modified_files = 0
    fixes_sum = 0
    warns_sum = 0

    for p in paths:
        modified, fixes, warns = fix_file(p)
        if modified:
            modified_files += 1
            fixes_sum += fixes
        warns_sum += warns

    print("=== Fix Summary ===")
    print(f"Scanned files: {len(paths)}")
    print(f"Modified files: {modified_files}")
    print(f"Total fixes applied: {fixes_sum}")
    print(f"Warnings (possible typos not auto-fixed): {warns_sum}")
    print("Backups written as: *.json.bak (only for modified files)")
    print("=== End ===")


if __name__ == "__main__":
    main()
