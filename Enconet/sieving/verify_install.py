#!/usr/bin/env python3
"""Non-mutating, ASCII-safe installation verifier (C4.3)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REQUIRED_PACKAGES = ("pandas", "openpyxl", "typer", "rich")
REQUIRED_PATHS = (
    "cli.py", "requirements.txt", "README.md", "DATA", "src",
    "src/json_extractor", "src/json_extractor/extract", "src/json_extractor/io",
    "src/json_extractor/query", "src/json_extractor/templates",
    "src/__init__.py", "src/json_extractor/__init__.py",
    "src/json_extractor/extract/__init__.py", "src/json_extractor/io/__init__.py",
    "src/json_extractor/query/__init__.py", "src/json_extractor/templates/__init__.py",
)
WRONG_PATHS = ("src/extract", "src/query", "src/io", "src/templates")
PROJECT_IMPORTS = (
    ("src.json_extractor.config", "get_config"),
    ("src.json_extractor.pipeline", "run_pipeline"),
    ("src.json_extractor.io", "discover_json_files"),
    ("src.json_extractor.extract", "flatten_json_to_records"),
    ("src.json_extractor.query", "parse_filter_dsl"),
    ("src.json_extractor.templates.app_b", "AppBTemplate"),
)


def verify_installation(project_root: Path = PROJECT_ROOT) -> int:
    dependency_errors: list[str] = []
    structure_errors: list[str] = []
    import_errors: list[str] = []
    print("JSON Extractor vNext - Installation Verification")
    print("=" * 60)

    print("\n1. Checking dependencies before project imports...")
    for package in REQUIRED_PACKAGES:
        if importlib.util.find_spec(package) is None:
            dependency_errors.append(f"Missing dependency: {package}")
            print(f"  [FAIL] {package}: missing")
        else:
            print(f"  [PASS] {package}")

    print("\n2. Checking structure...")
    for relative in REQUIRED_PATHS:
        if not (project_root / relative).exists():
            structure_errors.append(f"Missing path: {relative}")
            print(f"  [FAIL] missing: {relative}")
    for relative in WRONG_PATHS:
        if (project_root / relative).exists():
            structure_errors.append(f"Incorrect path: {relative}")
            print(f"  [FAIL] incorrect: {relative}")
    if not structure_errors:
        print("  [PASS] required layout")

    print("\n3. Checking project imports...")
    if dependency_errors:
        print("  [SKIP] project imports blocked by missing dependencies")
    elif structure_errors:
        print("  [SKIP] project imports blocked by structure errors")
    else:
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        for module_name, attribute in PROJECT_IMPORTS:
            try:
                module = __import__(module_name, fromlist=[attribute])
                getattr(module, attribute)
                print(f"  [PASS] {module_name}.{attribute}")
            except (ImportError, AttributeError) as exc:
                import_errors.append(f"Import failure: {module_name}.{attribute}: {exc}")
                print(f"  [FAIL] {module_name}.{attribute}: {exc}")

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    for label, errors in (("dependency", dependency_errors),
                          ("structure", structure_errors), ("import", import_errors)):
        print(f"{label}_errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    if dependency_errors:
        print("Install declared dependencies, then rerun this verifier.")
    if structure_errors:
        print("Restore the expected files from version control; no repair script is recommended.")
    if not dependency_errors and not structure_errors and not import_errors:
        print("PASS: installation verified")
        return 0
    print("FAIL: installation verification failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(verify_installation())
