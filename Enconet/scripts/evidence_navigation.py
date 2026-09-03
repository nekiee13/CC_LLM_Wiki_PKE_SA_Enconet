#!/usr/bin/env python3
"""Executable EA0.4 navigation and safe-presentation contract."""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Collection

import yaml


ENCONET = Path(__file__).resolve().parents[1]
CONTRACT = ENCONET / "schemas" / "evidence_navigation.yml"


@lru_cache(maxsize=1)
def _contract() -> dict:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _patterns() -> dict[str, re.Pattern[str]]:
    return {
        entity_type: re.compile(spec["id_regex"])
        for entity_type, spec in _contract()["targets"]["entity_types"].items()
    }


def target(entity_type: str, entity_id: str) -> str:
    """Build one validated canonical evidence fragment."""
    pattern = _patterns().get(entity_type)
    if pattern is None or pattern.fullmatch(entity_id) is None:
        raise ValueError(f"invalid evidence target: {entity_type}/{entity_id}")
    return f"#evidence/{entity_type}/{entity_id}"


def parse(fragment: str) -> tuple[str, str] | None:
    """Parse only the exact canonical ASCII fragment; reject encoded aliases and URLs."""
    if not isinstance(fragment, str) or "%" in fragment or "?" in fragment or "\\" in fragment:
        return None
    match = re.fullmatch(r"#evidence/([a-z]+)/([^/]+)", fragment)
    if match is None:
        return None
    entity_type, entity_id = match.groups()
    pattern = _patterns().get(entity_type)
    if pattern is None or pattern.fullmatch(entity_id) is None:
        return None
    if target(entity_type, entity_id) != fragment:
        return None
    return entity_type, entity_id


def resolve(
    fragment: str, known_targets: Collection[str], *, language: str = "en"
) -> dict:
    """Return a complete visible state for known, malformed, or unavailable targets."""
    parsed = parse(fragment)
    if parsed is None or fragment not in known_targets:
        failure = _contract()["failure_state"]
        messages = failure["messages"]
        message = messages.get(language, messages[failure["default_language"]])
        return {
            "status": "unavailable",
            "message": message,
            "requested_target": fragment,
            "focus_id": _contract()["interaction"]["focus_after_navigation"],
            "announce": True,
        }
    entity_type, entity_id = parsed
    return {
        "status": "resolved",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "requested_target": fragment,
        "focus_id": _contract()["interaction"]["focus_after_navigation"],
        "announce": False,
    }


def history_action(cause: str) -> str:
    """Choose the history operation without creating back/forward loops."""
    try:
        return _contract()["history"][cause]
    except KeyError as exc:
        raise ValueError(f"unknown navigation cause: {cause}") from exc


def safe_text(value: object) -> dict:
    """Package untrusted evidence for literal DOM text insertion, never HTML execution."""
    return {
        "text": str(value),
        "insertion_api": "textContent",
        "trusted_html": False,
        "linkify": False,
    }
