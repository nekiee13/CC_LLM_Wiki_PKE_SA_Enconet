"""Conservative matching for quoted evidence and extracted chunks."""
from __future__ import annotations

import re


_IMAGE_OR_LINK = re.compile(r"!?(?:\[([^\]]*)\]\([^)]*\))")
_HTML_TAG = re.compile(r"<[^>]+>")
_MARKDOWN_MARKER = re.compile(r"(?<!\w)[*_`~]+|[*_`~]+(?!\w)")
_DUPLICATE_LIST_MARKER = re.compile(r"(?<!\w)(\d+)\.\s*\1\.\s*")


def normalize(value: str) -> str:
    """Remove presentation-only markup and normalize whitespace for matching.

    This intentionally does not case-fold or Unicode-normalize text. Evidence
    links must remain exact source-substring decisions after presentation-only
    markup is removed.
    """
    text = value or ""
    text = _IMAGE_OR_LINK.sub(lambda match: match.group(1) or " ", text)
    text = _HTML_TAG.sub(" ", text)
    text = _MARKDOWN_MARKER.sub("", text)
    text = _DUPLICATE_LIST_MARKER.sub(r"\1. ", text)
    return re.sub(r"\s+", " ", text).strip()


def quote_matches(quote: str, chunk: str) -> bool:
    """Return true only when the quote is a source substring.

    Presentation-only Markdown/HTML noise may be removed, but omitted text
    marked with an ellipsis is not a linkable quote.
    """
    normalized_quote = normalize(quote)
    normalized_chunk = normalize(chunk)
    return bool(normalized_quote) and normalized_quote in normalized_chunk
