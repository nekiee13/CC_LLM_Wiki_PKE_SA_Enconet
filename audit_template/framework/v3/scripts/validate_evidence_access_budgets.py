#!/usr/bin/env python3
"""Enforce approved security, encoding, size, projection, and browser budgets."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml

import browser_harness
import validate_review_package


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_BUDGETS = PROJECT / "schemas" / "evidence_access_budgets.yml"
DEFAULT_BROWSER_CONFIG = PROJECT / "schemas" / "browser_harness.yml"
COLLECTIONS = (
    "documents", "chunks", "evaluations", "crumbs", "quotes", "gaps", "findings", "actions"
)
SIZE_ROLES = {"bundle": "bundle", "viewer": "viewer", "workspace": "workspace"}
LITERAL_HTML_CONTROLS = re.compile(
    "[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069]"
)


def load_budgets(path: Path = DEFAULT_BUDGETS) -> dict:
    """Load and strictly check the versioned Owner-authorized budget contract."""
    try:
        budgets = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"budget contract unavailable: {path}: {exc}") from exc
    required = {
        "schema_version", "approval", "size_bytes", "projection_counts",
        "performance_ms", "security",
    }
    if not isinstance(budgets, dict) or set(budgets) != required:
        raise ValueError("budget contract fields mismatch")
    if budgets["schema_version"] != "1.0":
        raise ValueError("unsupported budget contract schema_version")
    expected_sizes = {"bundle", "viewer", "workspace", "package_payload_total"}
    expected_performance = {
        "viewer_initial_render", "workspace_initial_render", "evidence_open", "search_response"
    }
    if set(budgets["size_bytes"]) != expected_sizes:
        raise ValueError("size budget fields mismatch")
    if set(budgets["projection_counts"]) != set(COLLECTIONS):
        raise ValueError("projection budget fields mismatch")
    if set(budgets["performance_ms"]) != expected_performance:
        raise ValueError("performance budget fields mismatch")
    numeric = [
        *budgets["size_bytes"].values(), *budgets["projection_counts"].values(),
        *budgets["performance_ms"].values(), budgets["security"].get("external_requests"),
    ]
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in numeric):
        raise ValueError("budget values must be non-negative integers")
    if budgets["approval"].get("authority") != "project_owner":
        raise ValueError("budget contract lacks project-owner authority")
    return budgets


def _manifest(package_root: Path) -> tuple[dict, list[dict]]:
    manifest = json.loads(
        (package_root / "package_manifest.json").read_text(encoding="utf-8")
    )
    return manifest, manifest["files"]


def validate_static(package_root: Path, budgets: dict) -> tuple[list[str], dict[str, int]]:
    """Return deterministic byte/count/encoding errors and exact measurements."""
    errors = list(validate_review_package.validate(package_root))
    metrics: dict[str, int] = {}
    try:
        _manifest_data, rows = _manifest(package_root)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        return errors + [f"budget manifest read failed: {exc}"], metrics
    actual_files: list[tuple[dict, Path]] = []
    path_pattern = re.compile(budgets["security"]["path_pattern"])
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            continue
        relative = row["path"]
        relative_path = Path(relative)
        if (relative_path.is_absolute() or ".." in relative_path.parts
                or "\\" in relative or path_pattern.fullmatch(relative) is None):
            errors.append(f"unsafe package artifact path: {relative}")
            continue
        path = package_root / relative_path
        if path.is_file():
            actual_files.append((row, path))
    metrics["package_payload_total_bytes"] = sum(path.stat().st_size for _row, path in actual_files)
    total_limit = budgets["size_bytes"]["package_payload_total"]
    if metrics["package_payload_total_bytes"] > total_limit:
        errors.append(
            "package payload total size budget exceeded: "
            f"{metrics['package_payload_total_bytes']} > {total_limit}: {package_root}"
        )
    for role, budget_name in SIZE_ROLES.items():
        matching = [(row, path) for row, path in actual_files if row.get("role") == role]
        sizes = [(path.stat().st_size, path) for _row, path in matching]
        metrics[f"{budget_name}_bytes"] = max((size for size, _path in sizes), default=0)
        limit = budgets["size_bytes"][budget_name]
        for size, path in sizes:
            if size > limit:
                errors.append(
                    f"{budget_name} size budget exceeded: {size} > {limit}: {path}"
                )
    for _row, path in actual_files:
        try:
            raw = path.read_bytes()
            if raw.decode("utf-8").encode("utf-8") != raw:
                errors.append(f"UTF-8 round-trip failed: {path}")
        except (OSError, UnicodeError) as exc:
            errors.append(f"UTF-8 round-trip failed: {path}: {exc}")
    if budgets["security"]["forbid_literal_controls_in_html"]:
        for _row, path in actual_files:
            if path.suffix.casefold() == ".html":
                try:
                    match = LITERAL_HTML_CONTROLS.search(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError):
                    continue
                if match:
                    errors.append(
                        f"literal control character U+{ord(match.group()):04X} in HTML: {path}"
                    )
    totals = {name: 0 for name in COLLECTIONS}
    for row, path in actual_files:
        if row.get("role") != "bundle":
            continue
        try:
            bundle = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        for name in COLLECTIONS:
            value = bundle.get(name)
            if isinstance(value, list):
                totals[name] += len(value)
    for name, count in totals.items():
        metrics[name] = count
        limit = budgets["projection_counts"][name]
        if count > limit:
            errors.append(f"{name} projection budget exceeded: {count} > {limit}")
    return list(dict.fromkeys(errors)), metrics


def _measure_page(page, path: Path) -> float:
    page.goto(path.resolve().as_uri(), wait_until="load")
    return float(page.evaluate(
        "() => performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd"
    ))


def validate_browser(
    package_root: Path,
    budgets: dict,
    browser_config: Path = DEFAULT_BROWSER_CONFIG,
) -> tuple[list[str], dict[str, float | int]]:
    """Measure the fixed production browser workflow once against approved limits."""
    errors = browser_harness.preflight(browser_config)
    metrics: dict[str, float | int] = {}
    if errors:
        return errors, metrics
    try:
        _manifest_data, rows = _manifest(package_root)
        viewer = package_root / next(row["path"] for row in rows if row["role"] == "viewer")
        workspace = package_root / next(row["path"] for row in rows if row["role"] == "workspace")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, StopIteration, TypeError) as exc:
        return [f"browser budget artifact discovery failed: {exc}"], metrics
    config = browser_harness.load_config(browser_config)
    previous = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = config["browser"]["root"]
    external: list[str] = []
    page_errors: list[str] = []
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.on("request", lambda request: external.append(request.url)
                        if urlsplit(request.url).scheme in {"http", "https"} else None)
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                metrics["viewer_initial_render_ms"] = round(_measure_page(page, viewer), 3)
                metrics["evidence_open_ms"] = round(float(page.evaluate("""async () => {
                    const start=performance.now();
                    document.querySelector('[data-evidence-id]').click();
                    await new Promise(requestAnimationFrame);
                    return performance.now()-start;
                }""")), 3)
                metrics["search_response_ms"] = round(float(page.evaluate("""async () => {
                    const input=document.getElementById('criterion-search');
                    const start=performance.now();
                    input.value='APP_B_I';
                    input.dispatchEvent(new Event('input',{bubbles:true}));
                    await new Promise(requestAnimationFrame);
                    return performance.now()-start;
                }""")), 3)
                metrics["workspace_initial_render_ms"] = round(_measure_page(page, workspace), 3)
            finally:
                browser.close()
    except Exception as exc:  # noqa: BLE001 - browser boundary fails closed
        return [f"browser budget measurement failed: {exc}"], metrics
    finally:
        if previous is None:
            os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
        else:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous
    metrics["external_requests"] = len(external)
    if page_errors:
        errors.append(f"browser page error: {page_errors[0]}")
    request_limit = budgets["security"]["external_requests"]
    if len(external) > request_limit:
        errors.append(f"external request budget exceeded: {len(external)} > {request_limit}")
    for name, limit in budgets["performance_ms"].items():
        measured = metrics.get(f"{name}_ms")
        if measured is None or measured > limit:
            errors.append(f"{name} budget exceeded: {measured} > {limit} ms")
    return errors, metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_root", type=Path)
    parser.add_argument("--budgets", type=Path, default=DEFAULT_BUDGETS)
    parser.add_argument("--browser-config", type=Path, default=DEFAULT_BROWSER_CONFIG)
    args = parser.parse_args(argv)
    try:
        budgets = load_budgets(args.budgets)
        static_errors, static_metrics = validate_static(args.package_root, budgets)
        browser_errors, browser_metrics = validate_browser(
            args.package_root, budgets, args.browser_config
        )
        errors = static_errors + browser_errors
        metrics = {**static_metrics, **browser_metrics}
    except Exception as exc:  # noqa: BLE001 - release boundary fails closed
        errors = [f"budget validation failed: {exc}"]
        metrics = {}
    if errors:
        for error in errors:
            print(f"validate_evidence_access_budgets: FAIL - {error}", file=sys.stderr)
        return 1
    summary = " ".join(f"{name}={metrics[name]}" for name in sorted(metrics))
    print(f"validate_evidence_access_budgets: PASS - {summary} - {args.package_root}")
    return 0


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
