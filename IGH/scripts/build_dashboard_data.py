"""Build the offline dashboard-data projection."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from report_stack_core import build_dashboard_data

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--generated-date", required=True)
    parser.add_argument("--dash-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = json.loads(args.package.read_text(encoding="utf-8"))
    data = build_dashboard_data(package, args.generated_date, args.dash_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    print(f"build_dashboard_data: PASS - {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
