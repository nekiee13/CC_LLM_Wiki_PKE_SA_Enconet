"""Fast, offline contract checks for the UMBRA dashboard prototype.

These tests guard the design shell only. They do not approve evidence, calculate a
score, or replace browser and accessibility testing for the production dashboard.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
VIEW = ROOT / "docs" / "design" / "EKONERG_UMBRA_DASHBOARD.html"
SCHEMA = ROOT / "schemas" / "dashboard_schema.yml"


class _Inventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if values.get("href"):
            self.hrefs.append(values["href"] or "")


def _read() -> tuple[str, _Inventory]:
    text = VIEW.read_text(encoding="utf-8")
    parser = _Inventory()
    parser.feed(text)
    return text, parser


def test_view_is_self_contained_and_uses_umbra_tokens() -> None:
    text, _ = _read()
    required = (
        "--bg-0: #0B0F14",
        "--surface-1: #111821",
        "--accent-fill: #3CCFB4",
        "--accent-text: #5FDCC6",
        "--text-primary: #E8EEF4",
        "--text-secondary: #A9B6C4",
    )
    assert all(token in text for token in required)
    forbidden = (
        "login.microsoftonline.com",
        "oauth",
        "signin",
        "https://cdn.",
        "cdnjs.cloudflare.com",
        "unpkg.com",
        "jsdelivr.net",
        "googleapis.com",
        "<script src=\"http",
        "<link href=\"http",
        "@import url(http",
    )
    assert not any(item in text for item in forbidden)


def test_view_has_landmarks_and_safe_draft_state() -> None:
    text, inventory = _read()
    assert inventory.tags.count("main") == 1
    assert 'aria-label="Audit navigation"' in text
    assert inventory.tags.count("h1") == 1
    assert inventory.tags.count("h2") >= 4
    assert inventory.tags.count("thead") == 2
    assert "Final score" in text
    assert "Withheld" in text
    assert not re.search(r"(?:weighted|conformity).{0,80}\b\d+(?:\.\d+)?%?\b", text, re.I)


def test_navigation_targets_and_all_criteria_groups_are_present() -> None:
    text, inventory = _read()
    assert {"#overview", "#criteria", "#evidence", "#sources", "#gates"}.issubset(
        set(inventory.hrefs)
    )
    assert {"overview", "criteria", "evidence", "sources", "gates"}.issubset(inventory.ids)
    for group in ("B-01—B-04", "B-05—B-08", "B-09—B-12", "B-13—B-18"):
        assert group in text
    assert "No direct quote" in text
    assert "Review pending" in text


def test_dashboard_schema_keeps_the_view_bound_to_18_criteria() -> None:
    schema = SCHEMA.read_text(encoding="utf-8")
    for field in ("supplier", "generated_date", "dash_id", "run_id", "weighted_score"):
        assert f"{field}:" in schema
    assert "count: 18" in schema
    assert "forbidden_patterns:" in schema
