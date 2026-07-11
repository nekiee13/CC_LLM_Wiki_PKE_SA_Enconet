# ------------------------
# fix_mor_rule_refs.py
# ------------------------
#!/usr/bin/env python3
"""
Populate missing rule_reference_ids in MOR DOCUMENT JSON files based on criterion_id.

Rationale:
- The Streamlit "Referenced Rule Code" filter operates on flattened rule_ref_codes,
  which are derived exclusively from item["rule_reference_ids"].
- MOR items may be APP_B-classified (criterion_id present) but lack explicit rule_reference_ids.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


DATA_DIR = Path("DATA") / "DOCUMENT"
FILE_GLOB = "mor_*.json"

TARGET_TAXONOMY_ID = "APP_B"
REF_CODE = "10CFR50_APPB"

# Optional safety: write backups next to files
WRITE_BACKUP = True
BACKUP_SUFFIX = ".bak"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Root JSON is not an object/dict")
    return data


def save_json(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize_rule_reference_ids(v: Any) -> List[str]:
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    return []


def ensure_rule_ref(item: Dict[str, Any]) -> int:
    """
    Returns 1 if modified, 0 if unchanged.
    Rule: for APP_B DOCUMENT items with criterion_id APP_B_*,
    ensure rule_reference_ids contains "10CFR50_APPB::<criterion_id>".
    """
    if (item.get("taxonomy_id") or "").strip() != TARGET_TAXONOMY_ID:
        return 0

    crit = (item.get("criterion_id") or "").strip()
    if not crit:
        return 0

    required = f"{REF_CODE}::{crit}"

    current = normalize_rule_reference_ids(item.get("rule_reference_ids", []))
    if required in current:
        # No change needed
        return 0

    # Append while preserving any existing order
    current.append(required)
    item["rule_reference_ids"] = current
    return 1


def iter_target_files() -> List[Path]:
    if not DATA_DIR.exists():
        return []
    # Exclude existing .bak files and non-json by pattern
    files = [p for p in DATA_DIR.rglob(FILE_GLOB) if p.is_file() and not p.name.endswith(BACKUP_SUFFIX)]
    files.sort(key=lambda p: p.relative_to(DATA_DIR).as_posix().lower())
    return files


def main() -> int:
    files = iter_target_files()
    if not files:
        print(f"No target files found under {DATA_DIR} matching {FILE_GLOB}")
        return 0

    total_items_fixed = 0
    files_modified = 0
    errors: List[Tuple[str, str]] = []

    for path in files:
        try:
            data = load_json(path)
            items = data.get("items", [])
            if not isinstance(items, list):
                continue

            fixed_in_file = 0
            for item in items:
                if isinstance(item, dict):
                    fixed_in_file += ensure_rule_ref(item)

            if fixed_in_file > 0:
                if WRITE_BACKUP:
                    backup_path = path.with_suffix(path.suffix + BACKUP_SUFFIX)
                    if not backup_path.exists():
                        backup_path.write_bytes(path.read_bytes())

                save_json(path, data)
                files_modified += 1
                total_items_fixed += fixed_in_file
                print(f"{path.name}: fixed {fixed_in_file} items")

        except Exception as e:
            errors.append((str(path), str(e)))

    print("-" * 60)
    print(f"Modified files: {files_modified}")
    print(f"Fixed items:    {total_items_fixed}")
    if errors:
        print(f"Errors:         {len(errors)}")
        for p, msg in errors:
            print(f"  - {p}: {msg}")
        return 1

    print("Done. Re-run Streamlit/CLI and retry the DOCUMENT Referenced Rule Code filter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
