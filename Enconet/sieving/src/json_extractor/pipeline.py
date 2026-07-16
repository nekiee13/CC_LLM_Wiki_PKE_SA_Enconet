# ------------------------
# src/json_extractor/pipeline.py
# ------------------------
"""
Main pipeline orchestration.

Coordinates:
- File discovery and reading
- JSON flattening and validation
- Query execution
- Export

Provides a single entry point for both CLI and Streamlit adapters.

C4.1 (fail-closed filtering):
- filter failures return no rows by default;
- an explicit preview-only override may retain unfiltered rows;
- export is always blocked while filter_error is set.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

import pandas as pd

from .config import get_config
from .extract import ValidationError, flatten_multiple_files
from .io import BadFileReport, discover_json_files, export_dataframe, read_json_file
from .query import QueryEngine, parse_filter_dsl
from .query.compiler import DSLParseError


@dataclass
class PipelineResult:
    """
    Result of a complete pipeline run.

    Contains:
    - Resulting DataFrame (potentially filtered and column-selected)
    - Bad file reports
    - Validation errors
    - Query statistics
    - filter_error: populated when filter parsing/execution fails
    """

    df: pd.DataFrame
    bad_files: List[BadFileReport] = field(default_factory=list)
    validation_errors: List[ValidationError] = field(default_factory=list)
    files_processed: int = 0
    items_loaded: int = 0
    items_after_filter: int = 0

    # E4-T2: explicit filter error signal
    filter_error: Optional[str] = None
    unfiltered_preview_used: bool = False
    validation_override_reason: Optional[str] = None

    @property
    def success(self) -> bool:
        """True if pipeline produced results (even with warnings)."""
        return (self.items_loaded > 0) or (self.df is not None and not self.df.empty)

    def get_error_summary(self) -> str:
        """Get human-readable error summary."""
        lines: List[str] = []

        if self.filter_error:
            lines.append("Filter error:")
            lines.append(f"  - {self.filter_error}")

        if self.bad_files:
            lines.append(f"Bad files: {len(self.bad_files)}")
            for bad_file in self.bad_files[:5]:
                lines.append(f"  - {bad_file.path}: {bad_file.reason}")
            if len(self.bad_files) > 5:
                lines.append(f"  ... and {len(self.bad_files) - 5} more")

        if self.validation_errors:
            error_count = sum(1 for e in self.validation_errors if e.severity == "ERROR")
            warning_count = sum(1 for e in self.validation_errors if e.severity == "WARNING")
            lines.append(f"Validation issues: {error_count} errors, {warning_count} warnings")

            errors = [e for e in self.validation_errors if e.severity == "ERROR"][:5]
            for err in errors:
                lines.append(f"  - {err.file_path} [{err.item_id}] {err.rule_id}: {err.message}")
            if error_count > 5:
                lines.append(f"  ... and {error_count - 5} more errors")

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
    """
    Run the complete extraction and query pipeline.

    Args:
        file_paths: Explicit list of file paths to process. If None, discover files.
        data_dir: Directory to discover files in (default: config.data_dir).
        file_patterns: Glob patterns for file discovery (default: ["*.json"]).
        filter_expr: DSL filter expression (e.g., "criterion_id:APP_B_I AND record_side:RULE").
        columns: List of columns to include in result. If None, uses all columns.
        allow_unfiltered_preview: Development-only escape that retains unfiltered rows
            for preview. Export remains blocked while filter_error is set.
        strict: Convert schema-drift warnings into blocking validation errors.

    Returns:
        PipelineResult with DataFrame and diagnostics.

    C4.1 behavior: filter errors fail closed unless preview override is explicit.
    """
    config = get_config()

    # Step 1: File discovery
    if file_paths is None:
        if data_dir is None:
            data_dir = config.data_dir

        file_paths = discover_json_files(
            data_dir=data_dir,
            file_patterns=file_patterns,
        )

    if not file_paths:
        return PipelineResult(
            df=pd.DataFrame(),
            files_processed=0,
            items_loaded=0,
            items_after_filter=0,
            filter_error=None,
        )

    # Step 2: Read JSON files
    # read_json_file() is expected to return parsed JSON root objects (dict-like).
    successful_data: List[Dict[str, Any]] = []
    bad_files: List[BadFileReport] = []
    file_path_strings: List[str] = []

    for file_path in file_paths:
        data, error = read_json_file(file_path)
        if error:
            bad_files.append(error)
            continue

        # Defensive typing: downstream expects dict roots
        if not isinstance(data, dict):
            bad_files.append(
                BadFileReport(
                    path=str(file_path),
                    reason=f"Invalid JSON root type: {type(data).__name__} (expected object/dict)",
                    error_type="InvalidJSONRoot",
                )
            )
            continue

        successful_data.append(cast(Dict[str, Any], data))
        file_path_strings.append(str(file_path))

    if not successful_data:
        return PipelineResult(
            df=pd.DataFrame(),
            bad_files=bad_files,
            files_processed=len(file_paths),
            items_loaded=0,
            items_after_filter=0,
            filter_error=None,
        )

    # Step 3: Flatten to normalized records
    flatten_result = flatten_multiple_files(successful_data, file_path_strings, strict=strict)

    if not flatten_result.records:
        return PipelineResult(
            df=pd.DataFrame(),
            bad_files=bad_files,
            validation_errors=flatten_result.validation_errors,
            files_processed=len(file_paths),
            items_loaded=0,
            items_after_filter=0,
            filter_error=None,
        )

    # Convert to DataFrame
    df = pd.DataFrame(flatten_result.records)

    # Ensure column order matches canonical schema
    all_columns = list(getattr(config, "all_columns", []) or [])
    if all_columns:
        existing_columns = [col for col in all_columns if col in df.columns]
        if existing_columns:
            df = df[existing_columns]

    items_loaded = int(len(df))

    # Step 4: Apply filter if provided
    filter_error: Optional[str] = None
    unfiltered_preview_used = False
    if filter_expr is not None and filter_expr.strip():
        try:
            query = parse_filter_dsl(filter_expr.strip())
            df = QueryEngine.execute_on_df(df, query)
        except DSLParseError as e:
            filter_error = str(e)
        except Exception as e:
            filter_error = f"Filter execution error: {e}"
        if filter_error:
            if allow_unfiltered_preview:
                unfiltered_preview_used = True
            else:
                df = df.iloc[0:0].copy()

    items_after_filter = int(len(df))

    # Step 5: Column selection
    if columns:
        valid_columns = [col for col in columns if col in df.columns]
        if valid_columns:
            df = df[valid_columns]

    return PipelineResult(
        df=df,
        bad_files=bad_files,
        validation_errors=flatten_result.validation_errors,
        files_processed=len(file_paths),
        items_loaded=items_loaded,
        items_after_filter=items_after_filter,
        filter_error=filter_error,
        unfiltered_preview_used=unfiltered_preview_used,
    )


def export_pipeline_result(
    result: PipelineResult,
    output_path: Path,
    columns: Optional[List[str]] = None,
    fmt: Optional[str] = None,
    validation_override_reason: Optional[str] = None,
) -> Path:
    """
    Export pipeline result to file.

    Supports: CSV, XLSX, Markdown.

    Args:
        result: PipelineResult to export.
        output_path: Output file path.
        columns: Optional subset of columns to export (validated against result.df).
        fmt: Optional format hint: 'csv', 'xlsx', 'md', or 'markdown'.
             If output_path already has a known suffix (.csv/.xlsx/.md), suffix wins.

    Returns:
        Actual output path (may have adjusted extension).

    Raises:
        ValueError: If filtering failed, ERROR validation exists without a recorded
            override reason, or DataFrame is empty.
    """
    if result.filter_error:
        raise ValueError("Export blocked: filter_error is set; unfiltered data is preview-only")
    validation_errors = [e for e in result.validation_errors if e.severity == "ERROR"]
    if validation_errors:
        reason = (validation_override_reason or "").strip()
        if not reason:
            raise ValueError(
                f"Export blocked: {len(validation_errors)} ERROR validation issue(s); "
                "an explicit validation override reason is required"
            )
        result.validation_override_reason = reason
    if result.df is None or result.df.empty:
        raise ValueError("Cannot export empty result")

    df = result.df

    # Apply export-time column selection (robust regardless of export_dataframe signature)
    if columns:
        cols_existing = [c for c in columns if c in df.columns]
        if cols_existing:
            df = df[cols_existing]

    fmt_norm = (fmt or "").strip().lower()
    if fmt_norm == "":
        fmt_norm = "xlsx"

    if fmt_norm == "markdown":
        fmt_norm = "md"

    # Delegate to IO exporter (suffix or fmt determines final output)
    return export_dataframe(
        df=df,
        output_path=output_path,
        fmt=fmt_norm,
        sheet_name="RESULT",
    )
