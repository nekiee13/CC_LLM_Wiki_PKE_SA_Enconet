#!/usr/bin/env python3
"""Project entry point for querying and exporting vendored sieving JSON."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import sieving_lib  # noqa: F401
from json_extractor.config import get_config
from json_extractor.io import discover_json_files
from json_extractor.pipeline import export_pipeline_result, run_pipeline


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    query = sub.add_parser("query", help="load, validate, filter, and optionally export JSON")
    source = query.add_mutually_exclusive_group(required=True)
    source.add_argument("--files", nargs="+", type=Path)
    source.add_argument("--all", action="store_true")
    query.add_argument("--data-dir", type=Path)
    query.add_argument("--filter")
    query.add_argument("--columns", help="comma-separated output columns")
    query.add_argument("--output", type=Path)
    query.add_argument("--format", choices=("csv", "xlsx", "md", "markdown"))
    query.add_argument("--strict", action="store_true", help="fail on missing or unexpected fields")
    listing = sub.add_parser("list-files", help="list discoverable JSON inputs")
    listing.add_argument("--data-dir", type=Path)
    sub.add_parser("info", help="show the canonical source and column counts")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    config = get_config()
    if args.command == "list-files":
        paths = discover_json_files(args.data_dir or config.data_dir)
        for path in paths:
            print(path)
        print(f"query_crumbs: {len(paths)} file(s)")
        return 0
    if args.command == "info":
        print(f"library={sieving_lib.SIEVING_SRC}")
        print(f"data_dir={config.data_dir}")
        print(f"columns={len(config.all_columns)} criteria={len(config.get_canonical_criteria())}")
        return 0

    columns = [value.strip() for value in (args.columns or "").split(",") if value.strip()] or None
    result = run_pipeline(
        file_paths=args.files if not args.all else None,
        data_dir=(args.data_dir or config.data_dir) if args.all else None,
        filter_expr=args.filter,
        columns=columns,
        strict=args.strict,
    )
    for issue in result.validation_errors:
        if issue.rule_id == "VAL-DRIFT-001":
            print(f"{issue.severity} {issue.file_path}: {issue.message}", file=sys.stderr)
    if result.bad_files or result.filter_error:
        print(result.get_error_summary(), file=sys.stderr)
        return 2
    error_count = sum(issue.severity == "ERROR" for issue in result.validation_errors)
    if error_count:
        print(result.get_error_summary(), file=sys.stderr)
        return 2
    if args.output:
        try:
            actual = export_pipeline_result(result, args.output, columns=columns, fmt=args.format)
        except (OSError, ValueError) as exc:
            print(f"query_crumbs: FAIL - {exc}", file=sys.stderr)
            return 2
        print(f"query_crumbs: PASS - {actual}")
    else:
        print(f"query_crumbs: PASS - {result.items_after_filter} item(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
