"""Local extraction and normalization of parsed JSON records."""

from .load_and_flatten import (
    flatten_json_to_records,
    flatten_multiple_files,
    ValidationError,
)

__all__ = ["flatten_json_to_records", "flatten_multiple_files", "ValidationError"]
