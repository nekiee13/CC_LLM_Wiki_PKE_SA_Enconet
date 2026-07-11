# ------------------------
# src/json_extractor/io/files.py
# ------------------------
"""
File discovery and JSON reading with robust error handling.

Repo-aligned behavior:
- Recursive discovery so DATA/RULE and DATA/DOCUMENT are discoverable.
- Stable deterministic ordering by relative path (not just filename).
- Robust error reporting for unreadable/invalid JSON files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class BadFileReport:
    """Report for a file that could not be processed."""
    path: str
    reason: str
    error_type: str  # "OS_ERROR" | "JSON_DECODE_ERROR" | "INVALID_ROOT"


def discover_json_files(
    data_dir: Path,
    file_patterns: Optional[List[str]] = None,
    recursive: bool = True,
) -> List[Path]:
    """
    Discover JSON files under the given data directory.

    Behavior:
    - If recursive=True (default), searches data_dir and all subdirectories (rglob).
    - If recursive=False, searches only the top-level (glob).
    - Supports multiple glob patterns (union).
    - Returns stable deterministic ordering sorted by relative path.

    Args:
        data_dir: Root directory to search.
        file_patterns: Glob patterns (e.g., ["*.json", "10CFR*.json"]).
                      If None, defaults to ["*.json"].
        recursive: If True, search recursively.

    Returns:
        Sorted list of Path objects.
    """
    if not data_dir.exists() or not data_dir.is_dir():
        return []

    patterns = file_patterns or ["*.json"]

    files: List[Path] = []
    for pattern in patterns:
        matches = data_dir.rglob(pattern) if recursive else data_dir.glob(pattern)
        for p in matches:
            if p.is_file():
                files.append(p)

    unique_files = list(set(files))
    unique_files.sort(key=lambda p: p.relative_to(data_dir).as_posix().lower())
    return unique_files


def read_json_file(file_path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[BadFileReport]]:
    """
    Read and parse a JSON file.

    Args:
        file_path: Path to JSON file.

    Returns:
        (parsed_data, None) on success
        (None, BadFileReport) on failure
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return None, BadFileReport(
                path=str(file_path),
                reason="Root JSON value is not an object (must be a dict)",
                error_type="INVALID_ROOT",
            )

        return data, None

    except OSError as e:
        return None, BadFileReport(
            path=str(file_path),
            reason=f"OS error: {e}",
            error_type="OS_ERROR",
        )

    except json.JSONDecodeError as e:
        return None, BadFileReport(
            path=str(file_path),
            reason=f"JSON decode error: {e}",
            error_type="JSON_DECODE_ERROR",
        )

    except Exception as e:
        return None, BadFileReport(
            path=str(file_path),
            reason=f"Unexpected error: {e}",
            error_type="OS_ERROR",
        )


def read_multiple_json_files(
    file_paths: List[Path],
) -> Tuple[List[Dict[str, Any]], List[BadFileReport]]:
    """
    Read multiple JSON files and collect errors.

    Args:
        file_paths: List of file paths to read.

    Returns:
        (list_of_successfully_parsed_dicts, list_of_BadFileReport)
    """
    successful: List[Dict[str, Any]] = []
    errors: List[BadFileReport] = []

    for file_path in file_paths:
        data, error = read_json_file(file_path)
        if error is not None:
            errors.append(error)
        else:
            successful.append(data)  # type: ignore[arg-type]

    return successful, errors


def format_paths_for_display(data_dir: Path, paths: List[Path]) -> List[str]:
    """
    Helper for UI adapters to display file options with subfolder context.

    Example output:
      - "RULE/10CFR50_AppendixB__RULE__v1.json"
      - "DOCUMENT/ASME_NQA-1__DOCUMENT__v1.json"
    """
    display: List[str] = []
    for p in paths:
        try:
            display.append(p.relative_to(data_dir).as_posix())
        except ValueError:
            display.append(p.name)
    return display
