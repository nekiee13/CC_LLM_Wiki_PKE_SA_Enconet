# ------------------------
# src/json_extractor/io/__init__.py
# ------------------------
"""
I/O operations: file discovery, reading, and export.
"""

from .files import discover_json_files, read_json_file, BadFileReport
from .export import export_to_csv, export_to_xlsx, export_dataframe

__all__ = [
    "discover_json_files",
    "read_json_file",
    "BadFileReport",
    "export_to_csv",
    "export_to_xlsx",
    "export_dataframe",
]
