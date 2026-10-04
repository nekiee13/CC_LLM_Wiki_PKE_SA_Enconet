"""Conservative matching for quoted evidence and extracted chunks."""
from __future__ import annotations

import re
import unicodedata


_IMAGE_OR_LINK = re.compile(r"!?(?:\[([^\]]*)\]\([^)]*\))")
_HTML_TAG = re.compile(r"<[^>]+>")
_MARKDOWN_MARKER = re.compile(r"(?<!\w)[*_`~]+|[*_`~]+(?!\w)")
_DUPLICATE_LIST_MARKER = re.compile(r"(?<!\w)(\d+)\.\s*\1\.\s*")


def normalize(value: str) -> str:
    """Remove presentation-only markup and normalize whitespace for matching."""
    text = unicodedata.normalize("NFKC", value or "")
    text = _IMAGE_OR_LINK.sub(lambda match: match.group(1) or " ", text)
    text = _HTML_TAG.sub(" ", text)
    text = _MARKDOWN_MARKER.sub("", text)
    text = _DUPLICATE_LIST_MARKER.sub(r"\1. ", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def quote_matches(quote: str, chunk: str) -> bool:
    """Return true for a literal quote or explicit-ellipsis excerpt.

    Ellipsis matching is deliberately limited to ordered, non-empty segments.
    It does not use a similarity score and therefore cannot turn unrelated text
    into evidence.
    """
    normalized_quote = normalize(quote)
    normalized_chunk = normalize(chunk)
    if not normalized_quote or normalized_quote in normalized_chunk:
        return bool(normalized_quote)
    parts = [normalize(part) for part in re.split(r"(?:\.\.\.|…)", quote)]
    parts = [part for part in parts if part]
    if len(parts) < 2:
        return False
    position = 0
    for part in parts:
        position = normalized_chunk.find(part, position)
        if position < 0:
            return False
        position += len(part)
    return True
