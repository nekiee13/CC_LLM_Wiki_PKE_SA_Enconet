"""Generate an approval-gated Markdown report."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from report_stack_core import render_report, validate_package

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = json.loads(args.package.read_text(encoding="utf-8"))
    errors = validate_package(package)
    if errors:
        raise SystemExit("generate_report: FAIL - " + "; ".join(errors))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(package), encoding="utf-8", newline="\n")
    print(f"generate_report: PASS - {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
