#!/usr/bin/env python3
"""Run reproducible headless checks against an offline file:// dashboard."""
from __future__ import annotations

import argparse
import importlib.metadata
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml


ENCONET = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ENCONET / "schemas" / "browser_harness.yml"


class BrowserHarnessError(RuntimeError):
    """Raised when the browser contract cannot be executed safely."""


def load_config(path: Path | str = DEFAULT_CONFIG) -> dict:
    """Load the controlled browser/runtime contract."""
    config_path = Path(path)
    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise BrowserHarnessError(f"browser harness config unavailable: {config_path}") from exc
    if not isinstance(config, dict) or config.get("schema_version") != "1.0":
        raise BrowserHarnessError("unsupported browser harness configuration")
    return config


def _browser_root(config: dict) -> Path:
    override = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    return Path(override if override else config["browser"]["root"]).resolve()


def _runtime_executable(config: dict) -> Path:
    return _browser_root(config) / Path(config["browser"]["executable_relative"])


def preflight(config_path: Path | str = DEFAULT_CONFIG) -> list[str]:
    """Return actionable dependency/runtime errors; absence is never a skip."""
    config = load_config(config_path)
    errors: list[str] = []
    expected_dependency = config["dependency"]
    distribution, expected_version = expected_dependency.split("==", maxsplit=1)
    try:
        installed_version = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        errors.append(
            f"browser library missing: install {expected_dependency} in the project environment"
        )
    else:
        if installed_version != expected_version:
            errors.append(
                f"browser library version mismatch: expected {expected_version}, "
                f"found {installed_version}"
            )

    executable = _runtime_executable(config)
    install_command = config["browser"]["install_command"]
    if not executable.is_file():
        errors.append(
            f"browser runtime missing: {executable}; set PLAYWRIGHT_BROWSERS_PATH to the "
            f"controlled root and run `{install_command}`"
        )
    else:
        completed = subprocess.run(
            [str(executable), "--version"], check=False, capture_output=True,
            text=True, encoding="utf-8",
        )
        expected_browser_version = str(config["browser"]["version"])
        if completed.returncode != 0 or expected_browser_version not in completed.stdout:
            actual = (completed.stdout or completed.stderr).strip() or "no version returned"
            errors.append(
                f"browser runtime version mismatch: expected {expected_browser_version}, "
                f"found {actual}"
            )
    return errors


def _local_file_url(html_path: Path | str) -> tuple[Path, str]:
    raw = str(html_path)
    scheme = urlsplit(raw).scheme.casefold()
    if scheme and scheme != "file" and not (len(scheme) == 1 and raw[1:3] in {":\\", ":/"}):
        raise BrowserHarnessError("browser check requires a local HTML file, not a URL")
    path = Path(html_path).resolve()
    if not path.is_file() or path.suffix.casefold() not in {".html", ".htm"}:
        raise BrowserHarnessError(f"browser check requires an existing local HTML file: {path}")
    return path, path.as_uri()


def _retain_failure_artifacts(
    page, artifact_dir: Path, console_messages: list[str], error: str
) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    if page is None:
        (artifact_dir / "screenshot.png").write_bytes(b"capture unavailable\n")
        dom = "<!-- Page was unavailable before diagnostic capture. -->"
    else:
        try:
            page.screenshot(path=str(artifact_dir / "screenshot.png"), full_page=True)
        except Exception as exc:  # noqa: BLE001 - retain the other diagnostic artifacts
            console_messages.append(f"screenshot-error: {exc}")
            (artifact_dir / "screenshot.png").write_bytes(b"capture unavailable\n")
        try:
            dom = page.content()
        except Exception as exc:  # noqa: BLE001
            dom = f"<!-- DOM capture failed: {exc} -->"
    (artifact_dir / "dom.html").write_text(dom, encoding="utf-8", newline="\n")
    messages = console_messages + [f"harness-error: {error}"]
    (artifact_dir / "console.log").write_text(
        "\n".join(messages) + "\n", encoding="utf-8", newline="\n"
    )


def run_check(
    html_path: Path | str,
    *,
    artifact_dir: Path | str,
    config_path: Path | str = DEFAULT_CONFIG,
    require_interactive: bool = False,
) -> dict:
    """Open a local artifact headlessly and retain diagnostics only on failure."""
    config = load_config(config_path)
    preflight_errors = preflight(config_path)
    if preflight_errors:
        raise BrowserHarnessError("; ".join(preflight_errors))
    _path, file_url = _local_file_url(html_path)
    artifacts = Path(artifact_dir).resolve()
    console_messages: list[str] = []
    network_requests: list[str] = []
    result = {
        "passed": False,
        "url": file_url,
        "network_requests": network_requests,
        "evidence_bundle_count": 0,
        "interactive_crumb_count": 0,
        "error": "",
    }

    previous_browser_root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(_browser_root(config))
    page = None
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page()
                page.on("console", lambda message: console_messages.append(
                    f"{message.type}: {message.text}"
                ))
                page.on(
                    "pageerror", lambda error: console_messages.append(f"pageerror: {error}")
                )
                page.on("request", lambda request: network_requests.append(request.url)
                        if urlsplit(request.url).scheme in {"http", "https"} else None)
                page.goto(file_url, wait_until="load")
                result["url"] = page.url
                result["evidence_bundle_count"] = page.locator("#evidence-bundle").count()
                result["interactive_crumb_count"] = page.locator("[data-evidence-id]").count()
                if urlsplit(page.url).scheme != config["navigation"]["required_scheme"]:
                    raise BrowserHarnessError(f"dashboard did not load through file://: {page.url}")
                if result["evidence_bundle_count"] != 1:
                    raise BrowserHarnessError("expected exactly one embedded evidence bundle")
                if config["navigation"]["forbid_network_requests"] and network_requests:
                    raise BrowserHarnessError(
                        f"offline dashboard made network request: {network_requests[0]}"
                    )
                if require_interactive and result["interactive_crumb_count"] < 1:
                    raise BrowserHarnessError("interactive crumb control is missing")
                result["passed"] = True
            except Exception as exc:  # noqa: BLE001 - capture while the page is live
                result["error"] = str(exc)
                _retain_failure_artifacts(page, artifacts, console_messages, result["error"])
                return result
    except Exception as exc:  # noqa: BLE001 - browser boundary returns diagnostic result
        result["error"] = str(exc)
        _retain_failure_artifacts(page, artifacts, console_messages, result["error"])
        return result
    finally:
        if previous_browser_root is None:
            os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
        else:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous_browser_root
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("html", type=Path)
    check_parser.add_argument("--artifacts", type=Path, required=True)
    check_parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    check_parser.add_argument("--require-interactive", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "preflight":
            errors = preflight(args.config)
            if errors:
                for error in errors:
                    print(f"browser_harness: FAIL - {error}", file=sys.stderr)
                return 1
            print("browser_harness: PASS - pinned Playwright and browser runtime available")
            return 0
        result = run_check(
            args.html,
            artifact_dir=args.artifacts,
            config_path=args.config,
            require_interactive=args.require_interactive,
        )
        if not result["passed"]:
            print(f"browser_harness: FAIL - {result['error']}", file=sys.stderr)
            return 1
        print(
            "browser_harness: PASS - "
            f"bundles={result['evidence_bundle_count']} "
            f"interactive={result['interactive_crumb_count']} - {result['url']}"
        )
        return 0
    except BrowserHarnessError as exc:
        print(f"browser_harness: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
