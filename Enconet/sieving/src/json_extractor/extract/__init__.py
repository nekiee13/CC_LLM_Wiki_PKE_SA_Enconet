# ------------------------
# src/json_extractor/extract/__init__.py
# ------------------------
"""
Extraction and normalization: load JSON and flatten to tabular records.
"""

from .load_and_flatten import (
    flatten_json_to_records,
    flatten_multiple_files,
    ValidationError,
)

__all__ = [
    "flatten_json_to_records",
    "flatten_multiple_files",
    "ValidationError",
]
