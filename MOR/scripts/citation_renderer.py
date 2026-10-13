#!/usr/bin/env python3
"""Render validated, typed Markdown citations for Evidence Explorer targets."""
from __future__ import annotations

import re
from urllib.parse import quote, urlsplit

import evidence_navigation


def _escape_label(value: str) -> str:
    """Escape Markdown link-label metacharacters without hiding stable IDs."""
    return value.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def _portable_path(viewer_path: str | None) -> str:
    if viewer_path is None or viewer_path == "":
        return ""
    if not isinstance(viewer_path, str) or "\r" in viewer_path or "\n" in viewer_path:
        raise ValueError("viewer path must be one relative path")
    parsed = urlsplit(viewer_path)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("viewer path must be relative and contain no URL components")
    if viewer_path.startswith(("/", "\\")) or "\\" in viewer_path:
        raise ValueError("viewer path must use relative POSIX separators")
    parts = viewer_path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("viewer path contains an unsafe segment")
    if re.match(r"^[A-Za-z]:", viewer_path):
        raise ValueError("viewer path must not be an absolute Windows path")
    return quote(viewer_path, safe="/._-")


def render(
    entity_type: str,
    entity_id: str,
    *,
    label: str | None = None,
    viewer_path: str | None = None,
) -> str:
    """Return one canonical Markdown link or fail on an invalid reference."""
    fragment = evidence_navigation.target(entity_type, entity_id)
    visible = f"{entity_type}:{entity_id}" if label is None else str(label)
    if not visible or "\r" in visible or "\n" in visible:
        raise ValueError("citation label must be one non-empty line")
    return f"[{_escape_label(visible)}]({_portable_path(viewer_path)}{fragment})"
