"""Project-local discovery, extraction, filtering, and guarded export."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import pandas as pd

from .config import get_config
from .extract import ValidationError, flatten_multiple_files
from .io import BadFileReport, discover_json_files, export_dataframe, read_json_file
from .query import QueryEngine, parse_filter_dsl
from .query.compiler import DSLParseError


@dataclass
class PipelineResult:
    df: pd.DataFrame
    bad_files: List[BadFileReport] = field(default_factory=list)
    validation_errors: List[ValidationError] = field(default_factory=list)
    files_processed: int = 0
    items_loaded: int = 0
    items_after_filter: int = 0
    filter_error: Optional[str] = None
    unfiltered_preview_used: bool = False
    validation_override_reason: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.items_loaded > 0 or not self.df.empty

    def get_error_summary(self) -> str:
        lines: List[str] = []
        if self.filter_error:
            lines.extend(("Filter error:", f"  - {self.filter_error}"))
        if self.bad_files:
            lines.append(f"Bad files: {len(self.bad_files)}")
            lines.extend(f"  - {item.path}: {item.reason}" for item in self.bad_files[:5])
            if len(self.bad_files) > 5:
                lines.append(f"  ... and {len(self.bad_files) - 5} more")
        if self.validation_errors:
            count = sum(item.severity == "ERROR" for item in self.validation_errors)
            warnings = sum(item.severity == "WARNING" for item in self.validation_errors)
            lines.append(f"Validation issues: {count} errors, {warnings} warnings")
            lines.extend(f"  - {item.file_path} [{item.item_id}] {item.rule_id}: {item.message}"
                         for item in self.validation_errors if item.severity == "ERROR")
        return "\n".join(lines) if lines else "No errors"


def run_pipeline(
    file_paths: Optional[List[Path]] = None,
    data_dir: Optional[Path] = None,
    file_patterns: Optional[List[str]] = None,
    filter_expr: Optional[str] = None,
    columns: Optional[List[str]] = None,
    allow_unfiltered_preview: bool = False,
    strict: bool = False,
) -> PipelineResult:
    """Run against project-local files; never treat validation as approval."""
    config = get_config()
    paths = (discover_json_files(data_dir or config.data_dir, file_patterns)
             if file_paths is None else list(file_paths))
    if not paths:
        return PipelineResult(df=pd.DataFrame())

    parsed = []
    labels = []
    bad_files: List[BadFileReport] = []
    for path in paths:
        data, error = read_json_file(path)
        if error:
            bad_files.append(error)
        else:
            parsed.append(data)
            labels.append(str(path))
    if not parsed:
        return PipelineResult(df=pd.DataFrame(), bad_files=bad_files, files_processed=len(paths))

    flattened = flatten_multiple_files(parsed, labels, strict=strict)
    df = pd.DataFrame(flattened.records)
    if not df.empty:
        ordered = [name for name in config.all_columns if name in df.columns]
        if ordered:
            df = df[ordered]
    loaded = len(df)
    filter_error: Optional[str] = None
    preview = False
    if filter_expr and filter_expr.strip():
        try:
            df = QueryEngine.execute_on_df(df, parse_filter_dsl(filter_expr.strip()))
        except DSLParseError as exc:
            filter_error = str(exc)
        except Exception as exc:
            filter_error = f"Filter execution error: {exc}"
        if filter_error:
            if allow_unfiltered_preview:
                preview = True
            else:
                df = df.iloc[0:0].copy()
    after_filter = len(df)
    if columns:
        selected = [name for name in columns if name in df.columns]
        if selected:
            df = df[selected]
    return PipelineResult(
        df=df, bad_files=bad_files, validation_errors=flattened.validation_errors,
        files_processed=len(paths), items_loaded=loaded, items_after_filter=after_filter,
        filter_error=filter_error, unfiltered_preview_used=preview,
    )


def export_pipeline_result(
    result: PipelineResult,
    output_path: Path,
    columns: Optional[List[str]] = None,
    fmt: Optional[str] = None,
    validation_override_reason: Optional[str] = None,
) -> Path:
    """Block failed filters, bad files, and unreviewed validation errors."""
    if result.filter_error:
        raise ValueError("Export blocked: filter_error is set; unfiltered data is preview-only")
    if result.bad_files:
        raise ValueError(f"Export blocked: {len(result.bad_files)} bad file(s)")
    errors = [item for item in result.validation_errors if item.severity == "ERROR"]
    if errors:
        reason = (validation_override_reason or "").strip()
        if not reason:
            raise ValueError(f"Export blocked: {len(errors)} ERROR validation issue(s); an explicit validation override reason is required")
        result.validation_override_reason = reason
    if result.df.empty:
        raise ValueError("Cannot export empty result")
    df = result.df
    if columns:
        selected = [name for name in columns if name in df.columns]
        if selected:
            df = df[selected]
    return export_dataframe(df, output_path, fmt=fmt or "xlsx", sheet_name="RESULT")
