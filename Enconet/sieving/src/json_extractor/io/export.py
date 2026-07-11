# ------------------------
# src/json_extractor/io/export.py
# ------------------------
"""
Export functions for CSV, XLSX, and Markdown with stable column ordering.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional


def export_to_csv(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None
) -> None:
    """
    Export DataFrame to CSV with utf-8-sig encoding.
    
    Args:
        df: DataFrame to export.
        output_path: Output file path.
        columns: List of columns to export. If None, exports all columns.
    
    Raises:
        ValueError: If specified columns don't exist in DataFrame.
    """
    if df.empty:
        # Create empty file with headers
        if columns:
            pd.DataFrame(columns=columns).to_csv(
                output_path,
                index=False,
                encoding='utf-8-sig'
            )
        else:
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
        return
    
    # Select columns if specified
    if columns:
        missing = set(columns) - set(df.columns)
        if missing:
            raise ValueError(f"Columns not found in DataFrame: {missing}")
        df_export = df[columns]
    else:
        df_export = df
    
    # Export to CSV
    df_export.to_csv(
        output_path,
        index=False,
        encoding='utf-8-sig'
    )


def export_to_xlsx(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None,
    sheet_name: str = "RESULT"
) -> None:
    """
    Export DataFrame to XLSX using openpyxl engine.
    
    Args:
        df: DataFrame to export.
        output_path: Output file path.
        columns: List of columns to export. If None, exports all columns.
        sheet_name: Name of the worksheet.
    
    Raises:
        ValueError: If specified columns don't exist in DataFrame.
    """
    # Ensure .xlsx extension
    if output_path.suffix.lower() != '.xlsx':
        output_path = output_path.with_suffix('.xlsx')
    
    if df.empty:
        # Create empty workbook with headers
        if columns:
            pd.DataFrame(columns=columns).to_excel(
                output_path,
                index=False,
                engine='openpyxl',
                sheet_name=sheet_name
            )
        else:
            df.to_excel(
                output_path,
                index=False,
                engine='openpyxl',
                sheet_name=sheet_name
            )
        return
    
    # Select columns if specified
    if columns:
        missing = set(columns) - set(df.columns)
        if missing:
            raise ValueError(f"Columns not found in DataFrame: {missing}")
        df_export = df[columns]
    else:
        df_export = df
    
    # Export to XLSX
    df_export.to_excel(
        output_path,
        index=False,
        engine='openpyxl',
        sheet_name=sheet_name
    )


def export_to_markdown(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None
) -> None:
    """
    Export DataFrame to Markdown (GitHub Flavored).
    
    Args:
        df: DataFrame to export.
        output_path: Output file path.
        columns: List of columns to export. If None, exports all columns.
        
    Raises:
        ValueError: If specified columns don't exist in DataFrame.
    """
    # Ensure .md extension
    if output_path.suffix.lower() not in ['.md', '.markdown']:
        output_path = output_path.with_suffix('.md')

    # Handle empty DataFrame
    if df.empty:
        # Create empty DataFrame with headers just to generate the header row
        df_export = pd.DataFrame(columns=columns) if columns else df
    else:
        # Select columns if specified
        if columns:
            missing = set(columns) - set(df.columns)
            if missing:
                raise ValueError(f"Columns not found in DataFrame: {missing}")
            df_export = df[columns]
        else:
            df_export = df

    # Generate Markdown content
    try:
        # Try using pandas built-in to_markdown (requires 'tabulate' package)
        md_content = df_export.to_markdown(index=False)
    except (ImportError, AttributeError):
        # Fallback if tabulate is missing: Simple pipe table implementation
        headers = [str(c) for c in df_export.columns]
        lines = []
        
        # Header
        lines.append("| " + " | ".join(headers) + " |")
        
        # Separator
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        # Rows
        for _, row in df_export.iterrows():
            # Escape pipes and replace newlines to prevent breaking the table structure
            row_str = [
                str(v).replace("\n", " ").replace("|", "\\|") if pd.notna(v) else "" 
                for v in row
            ]
            lines.append("| " + " | ".join(row_str) + " |")
            
        md_content = "\n".join(lines)

    # Write to file
    try:
        with output_path.open("w", encoding="utf-8") as f:
            f.write(md_content)
    except OSError as e:
        raise OSError(f"Could not write to file {output_path}: {e}") from e


def determine_export_format(
    output_path: Path,
    fmt: Optional[str] = None
) -> str:
    """
    Determine export format based on path and format parameter.
    
    Precedence:
    1. File extension (.csv, .md, .xlsx)
    2. Format hint ('csv', 'md', 'markdown', 'xlsx')
    3. Default: 'xlsx'
    
    Args:
        output_path: Output file path.
        fmt: Format hint ('csv', 'xlsx', 'md', 'markdown').
    
    Returns:
        'csv', 'xlsx', or 'md'
    """
    # 1. Check extension
    ext = output_path.suffix.lower()
    if ext == '.csv':
        return 'csv'
    elif ext in ['.md', '.markdown']:
        return 'md'
    elif ext == '.xlsx':
        return 'xlsx'
    
    # 2. Check format hint
    if fmt:
        f = fmt.lower().strip()
        if f == 'csv':
            return 'csv'
        elif f in ['md', 'markdown']:
            return 'md'
        elif f == 'xlsx':
            return 'xlsx'
            
    # 3. Default
    return 'xlsx'


def export_dataframe(
    df: pd.DataFrame,
    output_path: Path,
    columns: Optional[List[str]] = None,
    fmt: Optional[str] = None,
    sheet_name: str = "RESULT"
) -> Path:
    """
    Export DataFrame to CSV, XLSX, or Markdown based on path and format.
    
    Args:
        df: DataFrame to export.
        output_path: Output file path.
        columns: List of columns to export. If None, exports all columns.
        fmt: Format hint ('csv', 'xlsx', 'md').
        sheet_name: Name of the sheet (only used for XLSX).
    
    Returns:
        Actual output path (may have adjusted extension).
    
    Raises:
        ValueError: If columns are invalid.
    """
    export_format = determine_export_format(output_path, fmt)
    
    if export_format == 'csv':
        # Ensure .csv extension
        if output_path.suffix.lower() != '.csv':
            output_path = output_path.with_suffix('.csv')
        export_to_csv(df, output_path, columns)
        
    elif export_format == 'md':
        # Ensure .md extension
        if output_path.suffix.lower() not in ['.md', '.markdown']:
            output_path = output_path.with_suffix('.md')
        export_to_markdown(df, output_path, columns)
        
    else:
        # Ensure .xlsx extension
        if output_path.suffix.lower() != '.xlsx':
            output_path = output_path.with_suffix('.xlsx')
        export_to_xlsx(df, output_path, columns, sheet_name=sheet_name)
    
    return output_path