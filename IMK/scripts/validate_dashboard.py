"""Validate dashboard data, package lineage, and offline HTML."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from report_stack_core import validate_dashboard

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("dashboard_data", type=Path)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    errors = validate_dashboard(json.loads(args.package.read_text(encoding="utf-8")), json.loads(args.dashboard_data.read_text(encoding="utf-8")), args.html.read_text(encoding="utf-8"))
    if errors:
        for error in errors: print(f"validate_dashboard: FAIL - {error}")
        return 1
    print("validate_dashboard: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
