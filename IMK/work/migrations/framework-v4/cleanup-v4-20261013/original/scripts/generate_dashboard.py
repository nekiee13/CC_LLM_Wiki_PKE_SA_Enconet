"""Generate a self-contained offline HTML dashboard."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from report_stack_core import render_dashboard

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dashboard_data", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.dashboard_data.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_dashboard(data), encoding="utf-8", newline="\n")
    print(f"generate_dashboard: PASS - {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
