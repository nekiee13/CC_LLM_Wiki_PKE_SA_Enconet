"""Local CSV, XLSX, and Markdown export, adapted from Enconet."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import pandas as pd

from ._paths import local_io_path


def _selected(df: pd.DataFrame, columns: Optional[List[str]]) -> pd.DataFrame:
    if not columns:
        return df
    if df.empty:
        return pd.DataFrame(columns=columns)
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"Columns not found in DataFrame: {missing}")
    return df[columns]


def export_to_csv(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None,
) -> None:
    """Write selected columns as UTF-8-BOM CSV inside this project."""
    path = local_io_path(output_path)
    _selected(df, columns).to_csv(path, index=False, encoding="utf-8-sig")


def export_to_xlsx(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None,
    sheet_name: str = "RESULT",
) -> None:
    """Write selected columns as XLSX inside this project."""
    raw = Path(output_path)
    path = local_io_path(raw if raw.suffix.lower() == ".xlsx" else raw.with_suffix(".xlsx"))
    _selected(df, columns).to_excel(
        path, index=False, engine="openpyxl", sheet_name=sheet_name,
    )


def export_to_markdown(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None,
) -> None:
    """Write a Markdown table inside this project."""
    raw = Path(output_path)
    path = local_io_path(raw if raw.suffix.lower() in (".md", ".markdown") else raw.with_suffix(".md"))
    selected = _selected(df, columns)
    try:
        content = selected.to_markdown(index=False)
    except (ImportError, AttributeError):
        headers = [str(column) for column in selected.columns]
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for _, row in selected.iterrows():
            cells = [str(value).replace("\n", " ").replace("|", "\\|") if pd.notna(value) else ""
                     for value in row]
            lines.append("| " + " | ".join(cells) + " |")
        content = "\n".join(lines)
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise OSError(f"Could not write to file {path}: {exc}") from exc


def determine_export_format(output_path: Path, fmt: Optional[str] = None) -> str:
    """Choose by extension, then hint, then XLSX as in the source tool."""
    ext = Path(output_path).suffix.lower()
    if ext == ".csv":
        return "csv"
    if ext in (".md", ".markdown"):
        return "md"
    if ext == ".xlsx":
        return "xlsx"
    if fmt:
        hint = fmt.lower().strip()
        if hint == "csv":
            return "csv"
        if hint in ("md", "markdown"):
            return "md"
        if hint == "xlsx":
            return "xlsx"
    return "xlsx"


def export_dataframe(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None,
    fmt: Optional[str] = None,
    sheet_name: str = "RESULT",
) -> Path:
    """Export data and return the resolved local file path."""
    kind = determine_export_format(output_path, fmt)
    raw = Path(output_path)
    if kind == "csv":
        target = raw if raw.suffix.lower() == ".csv" else raw.with_suffix(".csv")
    elif kind == "md":
        target = raw if raw.suffix.lower() in (".md", ".markdown") else raw.with_suffix(".md")
    else:
        target = raw if raw.suffix.lower() == ".xlsx" else raw.with_suffix(".xlsx")
    path = local_io_path(target)
    if kind == "csv":
        export_to_csv(df, path, columns)
    elif kind == "md":
        export_to_markdown(df, path, columns)
    else:
        export_to_xlsx(df, path, columns, sheet_name=sheet_name)
    return path
