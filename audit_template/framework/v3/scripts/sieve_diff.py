#!/usr/bin/env python3
"""Compare two existing local sieve generations without losing duplicate crumbs."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _crumbs(conn: sqlite3.Connection, run_id: str) -> list[dict[str, object]]:
    rows = []
    for crumb in conn.execute(
        "SELECT * FROM crumbs WHERE sieve_run_id=? ORDER BY criterion_id,item_id", (run_id,)
    ):
        quotes = [row[0] for row in conn.execute(
            "SELECT quote_original FROM crumb_quotes WHERE item_id=? ORDER BY quote_id",
            (crumb["item_id"],)
        )]
        rows.append({"item_id": crumb["item_id"], "criterion_id": crumb["criterion_id"],
                     "statement": crumb["statement"], "quotes": quotes})
    return rows


def _signature(row: dict[str, object]) -> tuple[str, tuple[str, ...]]:
    return normalize(str(row["statement"])), tuple(sorted(normalize(q) for q in row["quotes"]))


def _changes(old: list[dict[str, object]], new: list[dict[str, object]]) -> dict[str, list[object]]:
    used_old: set[int] = set()
    used_new: set[int] = set()
    for old_index, left in enumerate(old):
        for new_index, right in enumerate(new):
            if new_index not in used_new and _signature(left) == _signature(right):
                used_old.add(old_index)
                used_new.add(new_index)
                break
    changed = []
    for old_index, left in enumerate(old):
        if old_index in used_old:
            continue
        left_quotes = {normalize(q) for q in left["quotes"]}
        candidates = [
            (len(left_quotes & {normalize(q) for q in right["quotes"]}), new_index)
            for new_index, right in enumerate(new) if new_index not in used_new
        ]
        candidates = [candidate for candidate in candidates if candidate[0] > 0]
        if not candidates:
            continue
        # Stable tie-break: new rows already sort by item_id.
        new_index = max(candidates, key=lambda candidate: (candidate[0], -candidate[1]))[1]
        used_old.add(old_index)
        used_new.add(new_index)
        changed.append({"old": left, "new": new[new_index]})
    return {
        "added": [row for index, row in enumerate(new) if index not in used_new],
        "removed": [row for index, row in enumerate(old) if index not in used_old],
        "changed": changed,
    }


def compare(db: Path, old_run: str, new_run: str) -> dict[str, object]:
    pattern = db_util.id_patterns()["run_id"]
    if pattern.fullmatch(old_run) is None or pattern.fullmatch(new_run) is None:
        raise ValueError("invalid sieve run ID")
    if old_run == new_run:
        raise ValueError("sieve diff requires two different runs")
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        old_meta = db_util.lookup(conn, "sieve_runs", "run_id", old_run)
        new_meta = db_util.lookup(conn, "sieve_runs", "run_id", new_run)
        if old_meta is None or new_meta is None:
            raise ValueError("both sieve runs must exist")
        if old_meta["doc_id"] != new_meta["doc_id"]:
            raise ValueError("sieve diff requires generations of the same document")
        old, new = _crumbs(conn, old_run), _crumbs(conn, new_run)
    criteria = sorted({str(row["criterion_id"]) for row in old + new})
    result = {
        criterion: _changes(
            [row for row in old if row["criterion_id"] == criterion],
            [row for row in new if row["criterion_id"] == criterion],
        ) for criterion in criteria
    }
    return {"schema_version": "1.0", "doc_id": old_meta["doc_id"],
            "old_run_id": old_run, "new_run_id": new_run, "criteria": result}


def render_markdown(data: dict[str, object]) -> str:
    lines = [f"# Sieve diff — {data['old_run_id']} → {data['new_run_id']}", ""]
    for criterion, changes in data["criteria"].items():
        lines.extend([f"## {criterion}", "",
                      f"Added: {len(changes['added'])}; removed: {len(changes['removed'])}; "
                      f"changed: {len(changes['changed'])}", ""])
        for row in changes["added"]:
            lines.append(f"- Added `{row['item_id']}`: {row['statement']}")
        for row in changes["removed"]:
            lines.append(f"- Removed `{row['item_id']}`: {row['statement']}")
        for row in changes["changed"]:
            lines.extend([f"- Changed `{row['old']['item_id']}` → `{row['new']['item_id']}`",
                          f"  - Old: {row['old']['statement']}",
                          f"  - New: {row['new']['statement']}"])
        lines.append("")
    return "\n".join(lines)


def generate(db: Path, old_run: str, new_run: str,
             output_dir: Path) -> tuple[Path, Path, dict[str, object]]:
    directory = local_path(output_dir)
    stem = f"diff-{old_run}-to-{new_run}"
    json_path, markdown_path = directory / f"{stem}.json", directory / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise ValueError("diff output already exists; prior run evidence is immutable")
    data = compare(db, old_run, new_run)
    directory.mkdir(parents=True, exist_ok=True)
    with json_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    with markdown_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(render_markdown(data))
    return json_path, markdown_path, data


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_run")
    parser.add_argument("new_run")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        json_path, markdown_path, _ = generate(
            args.db, args.old_run, args.new_run, args.output_dir
        )
        print(f"sieve_diff: PASS - {json_path}; {markdown_path}")
        return 0
    except (OSError, ValueError, KeyError, sqlite3.Error) as exc:
        print(f"sieve_diff: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
