# ------------------------
# fix_rule_refs_from_criterion.py
# ------------------------
#!/usr/bin/env python3
"""
fix_rule_refs_from_criterion.py

Purpose
- Populate missing rule_reference_ids on DOCUMENT items based on criterion_id.
- Enable DOCUMENT filtering by explicit rule reference fields (rule_ref_codes/rule_ref_keys),
  which are derived from item["rule_reference_ids"].

Default behavior
- Scans DATA/DOCUMENT recursively for *.json (excluding *.bak).
- For each item where:
    - taxonomy_id == APP_B (or missing but criterion_id starts with APP_B_)
    - record_side == DOCUMENT (or missing; treated as DOCUMENT)
    - criterion_id is present and starts with APP_B_
  Ensure rule_reference_ids includes: 10CFR50_APPB::<criterion_id>

Safety
- Optional backups are written next to modified files using suffix ".bak" (default enabled).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Root JSON is not an object")
    return data


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _as_str_list(v: Any) -> List[str]:
    if isinstance(v, list):
        out: List[str] = []
        for x in v:
            s = str(x).strip()
            if s:
                out.append(s)
        return out
    return []


def _should_treat_as_document(item: Dict[str, Any]) -> bool:
    rs = (item.get("record_side") or "").strip()
    if not rs:
        return True
    return rs == "DOCUMENT"


def _is_app_b_item(item: Dict[str, Any], taxonomy_id: str) -> bool:
    t = (item.get("taxonomy_id") or "").strip()
    crit = (item.get("criterion_id") or "").strip()
    if t == taxonomy_id:
        return True
    # Allow classification from criterion_id when taxonomy_id is missing or mis-set
    if crit.startswith("APP_B_"):
        return True
    return False


def _ensure_rule_ref(
    item: Dict[str, Any],
    ref_code: str,
    taxonomy_id: str,
) -> int:
    """
    Returns 1 if modified, 0 otherwise.
    """
    if not _should_treat_as_document(item):
        return 0

    if not _is_app_b_item(item, taxonomy_id):
        return 0

    crit = (item.get("criterion_id") or "").strip()
    if not crit.startswith("APP_B_"):
        return 0

    required = f"{ref_code}::{crit}"
    current = _as_str_list(item.get("rule_reference_ids"))

    if required in current:
        return 0

    current.append(required)
    item["rule_reference_ids"] = current
    return 1


def _iter_files(root: Path, glob_pattern: str, backup_suffix: str) -> List[Path]:
    files = [p for p in root.rglob(glob_pattern) if p.is_file()]
    # Exclude backups and non-json-like suffixes
    files = [p for p in files if not p.name.endswith(backup_suffix)]
    files.sort(key=lambda p: p.relative_to(root).as_posix().lower())
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=str, default=str(Path("DATA") / "DOCUMENT"))
    ap.add_argument("--glob", dest="glob_pattern", type=str, default="*.json")
    ap.add_argument("--ref-code", type=str, default="10CFR50_APPB")
    ap.add_argument("--taxonomy-id", type=str, default="APP_B")
    ap.add_argument("--backup", action="store_true", default=True)
    ap.add_argument("--no-backup", action="store_true", default=False)
    ap.add_argument("--backup-suffix", type=str, default=".bak")
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Directory not found: {data_dir}")
        return 1

    do_backup = bool(args.backup) and not bool(args.no_backup)
    backup_suffix = str(args.backup_suffix)

    files = _iter_files(data_dir, args.glob_pattern, backup_suffix)
    if not files:
        print(f"No files found under {data_dir} matching {args.glob_pattern}")
        return 0

    modified_files = 0
    fixed_items_total = 0
    errors: List[Tuple[str, str]] = []

    for path in files:
        try:
            data = _read_json(path)
            items = data.get("items", [])
            if not isinstance(items, list):
                continue

            fixed_in_file = 0
            for item in items:
                if isinstance(item, dict):
                    fixed_in_file += _ensure_rule_ref(
                        item=item,
                        ref_code=args.ref_code,
                        taxonomy_id=args.taxonomy_id,
                    )

            if fixed_in_file > 0:
                if do_backup:
                    bak_path = path.with_suffix(path.suffix + backup_suffix)
                    if not bak_path.exists():
                        bak_path.write_bytes(path.read_bytes())
                _write_json(path, data)
                modified_files += 1
                fixed_items_total += fixed_in_file
                print(f"{path.name}: added rule_reference_ids to {fixed_in_file} items")

        except Exception as e:
            errors.append((str(path), str(e)))

    print("-" * 72)
    print(f"Modified files: {modified_files}")
    print(f"Fixed items:    {fixed_items_total}")
    if errors:
        print(f"Errors:         {len(errors)}")
        for p, msg in errors:
            print(f"  - {p}: {msg}")
        return 1

    print("Done.")
    print("Recommended validation:")
    print("  - Re-run Streamlit and filter DOCUMENT by Referenced Rule Code = 10CFR50_APPB")
    print("  - Or run CLI with filter: record_side:DOCUMENT rule_ref_codes:10CFR50_APPB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
