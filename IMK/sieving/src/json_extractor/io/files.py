"""Deterministic local JSON discovery and reading, adapted from Enconet."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ._paths import local_io_path


@dataclass
class BadFileReport:
    """Report for a local file that could not be processed."""
    path: str
    reason: str
    error_type: str


def discover_json_files(
    data_dir: Path,
    file_patterns: Optional[List[str]] = None,
    recursive: bool = True,
) -> List[Path]:
    """Find local JSON files in stable relative-path order."""
    root = local_io_path(data_dir)
    if not root.exists() or not root.is_dir():
        return []
    patterns = file_patterns or ["*.json"]
    files: List[Path] = []
    for pattern in patterns:
        pattern_path = Path(pattern)
        if pattern_path.is_absolute() or ".." in pattern_path.parts:
            raise ValueError("File pattern must stay below the data directory")
        matches = root.rglob(pattern) if recursive else root.glob(pattern)
        for candidate in matches:
            checked = local_io_path(candidate)
            if not checked.is_relative_to(root):
                raise ValueError("File pattern reached outside the data directory")
            if checked.is_file():
                files.append(checked)
    unique_files = list(set(files))
    unique_files.sort(key=lambda path: path.relative_to(root).as_posix().lower())
    return unique_files


def read_json_file(file_path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[BadFileReport]]:
    """Parse one local JSON object; report file and JSON errors."""
    path = local_io_path(file_path)
    try:
        with path.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
        if not isinstance(data, dict):
            return None, BadFileReport(
                path=str(path),
                reason="Root JSON value is not an object (must be a dict)",
                error_type="INVALID_ROOT",
            )
        return data, None
    except OSError as exc:
        return None, BadFileReport(str(path), f"OS error: {exc}", "OS_ERROR")
    except json.JSONDecodeError as exc:
        return None, BadFileReport(str(path), f"JSON decode error: {exc}", "JSON_DECODE_ERROR")
    except Exception as exc:
        return None, BadFileReport(str(path), f"Unexpected error: {exc}", "OS_ERROR")


def read_multiple_json_files(
    file_paths: List[Path],
) -> Tuple[List[Dict[str, Any]], List[BadFileReport]]:
    """Parse local JSON files and collect ordinary parse errors."""
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
    """Show local paths with their subfolder context."""
    root = local_io_path(data_dir)
    display: List[str] = []
    for candidate in paths:
        path = local_io_path(candidate)
        try:
            display.append(path.relative_to(root).as_posix())
        except ValueError:
            display.append(path.name)
    return display
