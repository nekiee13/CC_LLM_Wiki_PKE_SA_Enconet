"""Validate report structure and package lineage."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from report_stack_core import validate_report

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    errors = validate_report(json.loads(args.package.read_text(encoding="utf-8")), args.report.read_text(encoding="utf-8"))
    if errors:
        for error in errors: print(f"validate_report: FAIL - {error}")
        return 1
    print("validate_report: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
