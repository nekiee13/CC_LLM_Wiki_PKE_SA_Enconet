#!/usr/bin/env python3
"""Compare two immutable sieve generations of the same document."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import db_util


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _crumbs(conn, run_id: str) -> list[dict[str, object]]:
    rows = []
    for crumb in conn.execute("SELECT * FROM crumbs WHERE sieve_run_id=? ORDER BY criterion_id,item_id", (run_id,)):
        quotes = [row[0] for row in conn.execute(
            "SELECT quote_original FROM crumb_quotes WHERE item_id=? ORDER BY quote_id", (crumb["item_id"],)
        )]
        rows.append({"item_id": crumb["item_id"], "criterion_id": crumb["criterion_id"],
                     "statement": crumb["statement"], "quotes": quotes})
    return rows


def compare(db: Path, old_run: str, new_run: str) -> dict[str, object]:
    with db_util.connect(db) as conn:
        old_meta = db_util.lookup(conn, "sieve_runs", "run_id", old_run)
        new_meta = db_util.lookup(conn, "sieve_runs", "run_id", new_run)
        if old_meta is None or new_meta is None:
            raise ValueError("both sieve runs must exist")
        if old_meta["doc_id"] != new_meta["doc_id"]:
            raise ValueError("sieve diff requires generations of the same document")
        old, new = _crumbs(conn, old_run), _crumbs(conn, new_run)
    result: dict[str, dict[str, list[object]]] = {}
    criteria = sorted({str(row["criterion_id"]) for row in old + new})
    for criterion in criteria:
        old_items = [row for row in old if row["criterion_id"] == criterion]
        new_items = [row for row in new if row["criterion_id"] == criterion]
        used_old: set[str] = set()
        used_new: set[str] = set()
        changed = []
        for left in old_items:
            left_quotes = {normalize(q) for q in left["quotes"]}
            candidates = []
            for right in new_items:
                if right["item_id"] in used_new:
                    continue
                overlap = len(left_quotes & {normalize(q) for q in right["quotes"]})
                if overlap:
                    candidates.append((overlap, right))
            if not candidates:
                continue
            right = max(candidates, key=lambda pair: pair[0])[1]
            used_old.add(str(left["item_id"])); used_new.add(str(right["item_id"]))
            if (normalize(str(left["statement"])) != normalize(str(right["statement"])) or
                    {normalize(q) for q in left["quotes"]} != {normalize(q) for q in right["quotes"]}):
                changed.append({"old": left, "new": right})
        old_exact = {(normalize(str(row["statement"])), tuple(sorted(normalize(q) for q in row["quotes"]))): row for row in old_items if row["item_id"] not in used_old}
        new_exact = {(normalize(str(row["statement"])), tuple(sorted(normalize(q) for q in row["quotes"]))): row for row in new_items if row["item_id"] not in used_new}
        unchanged = set(old_exact) & set(new_exact)
        result[criterion] = {
            "added": [row for key, row in new_exact.items() if key not in unchanged],
            "removed": [row for key, row in old_exact.items() if key not in unchanged],
            "changed": changed,
        }
    return {"schema_version": "1.0", "doc_id": old_meta["doc_id"],
            "old_run_id": old_run, "new_run_id": new_run, "criteria": result}


def render_markdown(data: dict[str, object]) -> str:
    lines = [f"# Sieve diff — {data['old_run_id']} → {data['new_run_id']}", ""]
    for criterion, changes in data["criteria"].items():
        lines.extend([f"## {criterion}", "", f"Added: {len(changes['added'])}; removed: {len(changes['removed'])}; changed: {len(changes['changed'])}", ""])
        for row in changes["added"]:
            lines.append(f"- Added `{row['item_id']}`: {row['statement']}")
        for row in changes["removed"]:
            lines.append(f"- Removed `{row['item_id']}`: {row['statement']}")
        for row in changes["changed"]:
            lines.extend([f"- Changed `{row['old']['item_id']}` → `{row['new']['item_id']}`",
                          f"  - Old: {row['old']['statement']}", f"  - New: {row['new']['statement']}"])
        lines.append("")
    return "\n".join(lines)


def generate(db: Path, old_run: str, new_run: str, output_dir: Path) -> tuple[Path, Path, dict[str, object]]:
    data = compare(db, old_run, new_run)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"diff-{old_run}-to-{new_run}"
    json_path, markdown_path = output_dir / f"{stem}.json", output_dir / f"{stem}.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(data), encoding="utf-8")
    return json_path, markdown_path, data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_run")
    parser.add_argument("new_run")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        json_path, markdown_path, _ = generate(args.db, args.old_run, args.new_run, args.output_dir)
        print(f"sieve_diff: PASS - {json_path}; {markdown_path}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"sieve_diff: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
