#!/usr/bin/env python3
"""Check only local wiki folders and neutral page-name shapes.

This is a setup structure check, not approval of criteria, source editions,
page content, evidence, or human gates.
"""
from __future__ import annotations

import argparse
import csv
import fnmatch
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from audit_state import audit_states
from project_paths import configure_standard_streams, local_path


PROJECT = Path(__file__).resolve().parents[1]
WIKI = PROJECT / "wiki"
SCHEMA = PROJECT / "schemas" / "wiki_structure.yml"
RUNS = PROJECT / "manifests" / "validation_runs.csv"
RUN_HEADER = ["run_utc", "validator", "phase", "result", "exit_code", "details"]
LOCATIONS = {
    "criterion-evaluation": "criteria",
    "evidence": "evidence",
    "finding": "findings",
    "action": "actions",
    "gate-decision": "gates",
}
EXTRA_DIRS = {"dashboards"}
ROOT_FILES = {"index.md", "log.md", "current-status.md", ".gitkeep"}


def _fixed_path(value: Path, expected: Path, label: str) -> Path:
    path = local_path(value)
    if path != expected:
        raise ValueError(f"{label} must be the local project path: {expected}")
    return path


def contracts(schema_path: Path = SCHEMA) -> dict[str, dict[str, str]]:
    schema_path = _fixed_path(schema_path, SCHEMA, "schema")
    data = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        raise ValueError("wiki structure schema version is invalid")
    page_types = data.get("page_types")
    if not isinstance(page_types, dict) or set(page_types) != set(LOCATIONS):
        raise ValueError("wiki structure schema page types are incomplete")
    for kind, directory in LOCATIONS.items():
        spec = page_types[kind]
        if not isinstance(spec, dict) or spec.get("location") != f"wiki/{directory}/":
            raise ValueError(f"wiki structure schema location is invalid: {kind}")
        pattern = spec.get("filename_pattern")
        if (not isinstance(pattern, str) or not pattern.endswith(".md") or
                any(token in pattern for token in ("/", "\\", "..", "?"))):
            raise ValueError(f"wiki structure schema filename pattern is unsafe: {kind}")
    return page_types


def validate(root: Path = WIKI, *, schema_path: Path = SCHEMA) -> list[str]:
    root = _fixed_path(root, WIKI, "wiki")
    page_types = contracts(schema_path)
    if not root.is_dir():
        return [f"wiki root missing: {root}"]
    errors: list[str] = []
    expected_dirs = set(LOCATIONS.values()) | EXTRA_DIRS
    entries = [local_path(path) for path in root.iterdir()]
    actual_dirs = {path.name for path in entries if path.is_dir()}
    for name in sorted(expected_dirs - actual_dirs):
        errors.append(f"required wiki directory missing: {name}")
    for name in sorted(actual_dirs - expected_dirs):
        errors.append(f"unexpected wiki directory: {name}")
    for path in entries:
        if path.is_file() and path.name not in ROOT_FILES:
            errors.append(f"unexpected wiki root file: {path.name}")
    for kind, dirname in LOCATIONS.items():
        directory = root / dirname
        if not directory.is_dir():
            continue
        pattern = page_types[kind]["filename_pattern"]
        for path in directory.iterdir():
            path = local_path(path)
            if path.is_dir():
                errors.append(f"nested wiki directory forbidden: {path.relative_to(root)}")
            elif path.name == ".gitkeep":
                continue
            elif path.suffix.casefold() == ".md" and not fnmatch.fnmatchcase(path.name, pattern):
                errors.append(f"invalid {dirname} page filename: {path.name}")
            elif path.suffix.casefold() != ".md":
                if not (dirname == "evidence" and path.name == "matrix.json"):
                    errors.append(f"unexpected file in wiki/{dirname}: {path.name}")
    dashboards = root / "dashboards"
    if dashboards.is_dir():
        for path in dashboards.iterdir():
            path = local_path(path)
            if path.name != ".gitkeep" and (path.is_dir() or path.suffix.casefold() != ".html"):
                errors.append(f"invalid dashboard artifact: {path.name}")
    return errors


def append(result: str, code: int, details: str, *, path: Path = RUNS,
           phase: str = "verification") -> None:
    path = _fixed_path(path, RUNS, "validation log")
    with path.open("r+", newline="", encoding="utf-8") as handle:
        header = next(csv.reader(handle), None)
        if header:
            header[0] = header[0].lstrip("\ufeff")
        if header != RUN_HEADER:
            raise ValueError("validation log header is missing or invalid")
        handle.seek(0, 2)
        csv.writer(handle).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_structure.py", phase, result, code, details,
        ])


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--wiki", type=Path, default=WIKI)
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    parser.add_argument("--runs", type=Path, default=RUNS)
    parser.add_argument("--phase", default="verification")
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        _fixed_path(args.runs, RUNS, "validation log")
        if args.phase != "verification" and args.phase not in audit_states():
            raise ValueError(f"unknown validation phase: {args.phase}")
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"validate_structure: FAIL - {exc}", file=sys.stderr)
        return 1
    try:
        errors = validate(args.wiki, schema_path=args.schema)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        errors = [str(exc)]
    code = int(bool(errors))
    if not args.no_record:
        try:
            append(
                "FAIL" if code else "PASS", code,
                f"{len(errors)} error(s); first: {errors[0][:120]}" if errors
                else "wiki folder and filename structure verified",
                path=args.runs, phase=args.phase,
            )
        except (OSError, ValueError) as exc:
            print(f"validate_structure: FAIL - validation log could not be written: {exc}",
                  file=sys.stderr)
            return 1
    for error in errors:
        print(f"validate_structure: FAIL - {error}", file=sys.stderr)
    print(f"validate_structure: {'FAIL' if code else 'PASS'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
