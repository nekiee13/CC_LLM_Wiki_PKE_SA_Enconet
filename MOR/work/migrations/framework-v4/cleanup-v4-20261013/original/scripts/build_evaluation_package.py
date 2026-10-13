"""Build one local evaluation package from SQLite."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from report_stack_core import build_package, validate_package

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--approvals", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = build_package(args.db, args.run_id, args.approvals)
    errors = validate_package(package)
    if errors:
        raise SystemExit("build_evaluation_package: FAIL - " + "; ".join(errors))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(package, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    print(f"build_evaluation_package: PASS - {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
