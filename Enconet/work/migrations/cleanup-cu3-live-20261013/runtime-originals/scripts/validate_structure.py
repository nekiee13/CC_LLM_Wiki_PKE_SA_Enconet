#!/usr/bin/env python3
"""Validate EPIC13 wiki directories, page placement, and filename contracts."""
from __future__ import annotations

import argparse
import csv
import fnmatch
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ENCONET = Path(__file__).resolve().parents[1]
WIKI = ENCONET / "wiki"
SCHEMA = ENCONET / "schemas" / "page_types.yml"
RUNS = ENCONET / "manifests" / "validation_runs.csv"
ROOT_FILES = {"index.md", "log.md", "current-status.md"}
EXTRA_DIRS = {"dashboards"}


def contracts(schema_path: Path = SCHEMA) -> dict:
    return yaml.safe_load(schema_path.read_text(encoding="utf-8"))["page_types"]


def validate(root: Path = WIKI, *, schema_path: Path = SCHEMA) -> list[str]:
    errors: list[str] = []
    page_types = contracts(schema_path)
    expected_dirs = {Path(spec["location"]).name for spec in page_types.values()} | EXTRA_DIRS
    if not root.is_dir():
        return [f"wiki root missing: {root}"]
    actual_dirs = {path.name for path in root.iterdir() if path.is_dir()}
    for name in sorted(expected_dirs - actual_dirs):
        errors.append(f"required wiki directory missing: {name}")
    for name in sorted(actual_dirs - expected_dirs):
        errors.append(f"unexpected wiki directory: {name}")
    for path in root.iterdir():
        if path.is_file() and path.name not in ROOT_FILES and path.name != ".gitkeep":
            errors.append(f"unexpected wiki root file: {path.name}")
    by_dir = {Path(spec["location"]).name: spec for spec in page_types.values()}
    for dirname, spec in by_dir.items():
        directory = root / dirname
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.is_dir():
                errors.append(f"nested wiki directory forbidden: {path.relative_to(root)}")
            elif path.name == ".gitkeep":
                continue
            elif path.suffix.casefold() == ".md" and not fnmatch.fnmatchcase(path.name, spec["filename_pattern"]):
                errors.append(f"invalid {dirname} page filename: {path.name}")
            elif path.suffix.casefold() != ".md":
                if not (dirname == "evidence" and path.name == "matrix.json"):
                    errors.append(f"unexpected file in wiki/{dirname}: {path.name}")
    dashboards = root / "dashboards"
    if dashboards.is_dir():
        for path in dashboards.iterdir():
            if path.name != ".gitkeep" and (path.is_dir() or path.suffix.casefold() != ".html"):
                errors.append(f"invalid dashboard artifact: {path.name}")
    return errors


def append(result: str, code: int, details: str, *, path: Path = RUNS,
           phase: str = "verification") -> None:
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     "validate_structure.py", phase, result, code, details])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki", type=Path, default=WIKI)
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    parser.add_argument("--phase", default="verification")
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(args.wiki, schema_path=args.schema)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]
    code = int(bool(errors))
    if not args.no_record:
        append("FAIL" if code else "PASS", code,
               f"{len(errors)} error(s); first: {errors[0][:120]}" if errors else "wiki directory and filename contracts verified",
               phase=args.phase)
    for error in errors:
        print(f"validate_structure: FAIL - {error}", file=sys.stderr)
    print(f"validate_structure: {'FAIL' if code else 'PASS'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
