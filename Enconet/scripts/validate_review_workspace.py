#!/usr/bin/env python3
"""Validate a self-contained offline review workspace against its catalog."""
from __future__ import annotations

import argparse
import html as html_module
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import validate_review_catalog


class _CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.capturing = False
        self.records: list[str] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script" and dict(attrs).get("id") == "review-catalog":
            self.capturing = True
            self.parts = []

    def handle_data(self, data: str) -> None:
        if self.capturing:
            self.parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capturing:
            self.records.append("".join(self.parts))
            self.capturing = False


def validate(catalog: dict, html: str) -> list[str]:
    errors = [f"catalog: {error}" for error in validate_review_catalog.validate(catalog)]
    for control in ("run-filter", "filter-status", "run-list", "review-catalog"):
        if f'id="{control}"' not in html:
            errors.append(f"missing workspace control: {control}")
    for marker in ("function toggleRun(", "function filterRuns(", "data-artifact=", "data-status="):
        if marker not in html:
            errors.append(f"missing workspace behavior: {marker}")
    forbidden = (
        "fetch(", "XMLHttpRequest", "WebSocket", "showDirectoryPicker",
        "showOpenFilePicker", "webkitdirectory", "FileSystemDirectoryHandle",
    )
    for marker in forbidden:
        if marker in html:
            errors.append(f"forbidden workspace capability: {marker}")
    if re.search(r"(?:src|href)=[\"']https?://", html, re.IGNORECASE):
        errors.append("external network URL in workspace")
    parser = _CatalogParser()
    parser.feed(html)
    if len(parser.records) != 1:
        errors.append(f"expected exactly one embedded review catalog; found {len(parser.records)}")
        embedded = {}
    else:
        try:
            embedded = json.loads(parser.records[0])
        except json.JSONDecodeError:
            errors.append("embedded review catalog is invalid JSON")
            embedded = {}
    expected_ids = [row["run_id"] for row in catalog.get("runs", [])]
    embedded_ids = [row.get("run_id") for row in embedded.get("runs", [])]
    card_ids = re.findall(r'data-run-id="([^"]+)"', html)
    if embedded_ids != expected_ids or card_ids != expected_ids:
        errors.append("workspace/catalog run mismatch")
    for run_id in expected_ids:
        if html_module.escape(run_id) not in html:
            errors.append(f"workspace omits registered run: {run_id}")
    return list(dict.fromkeys(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args(argv)
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        errors = validate(catalog, args.workspace.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"validate_review_workspace: FAIL - {error}", file=sys.stderr)
        return 1
    print(f"validate_review_workspace: PASS - {len(catalog['runs'])} run(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
