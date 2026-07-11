# ------------------------
# cli.py
# ------------------------
#!/usr/bin/env python3
"""
JSON Extractor vNext - CLI Adapter

Command-line interface for extraction and querying.

Usage:
    python cli.py query --files DATA/*.json --filter "criterion_id:APP_B_I" --output results.xlsx
    python cli.py query --files DATA/doc1.json DATA/doc2.json --output results.csv
    python cli.py query --all --filter "record_side:RULE AND rule_strength:MANDATORY"
    python cli.py query --all --filter "criterion_id:APP_B_I OR criterion_id:APP_B_II" --preview
    python cli.py query --all --filter "criterion_id:APP_B_I,APP_B_II" --preview

C4.1: invalid filters exit 2 by default. --allow-unfiltered-preview is an
explicit development-only preview escape; export remains blocked.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from src.json_extractor.config import get_config
from src.json_extractor.pipeline import export_pipeline_result, run_pipeline

app = typer.Typer(help="JSON Extractor vNext - Query and export extraction results")
console = Console()


def _expand_globs(patterns: List[str]) -> List[Path]:
    """
    Expand CLI --files inputs into concrete Paths.
    Supports:
      - direct file paths
      - glob patterns (including recursive **)

    Note:
      - Non-existent direct paths are passed through so the pipeline can report them.
    """
    expanded: List[Path] = []
    for raw in patterns:
        raw = (raw or "").strip()
        if not raw:
            continue

        p = Path(raw)

        # If wildcards are present, expand via glob (relative or absolute).
        if any(ch in raw for ch in ("*", "?", "[")):
            base = p.parent if str(p.parent) not in ("", ".") else Path(".")
            pat = p.name
            try:
                matches = list(base.glob(pat))
            except Exception:
                matches = []
            expanded.extend([m.resolve() for m in matches if m.is_file()])
            continue

        # Direct path
        if p.exists():
            expanded.append(p.resolve())
        else:
            expanded.append(p)

    # De-duplicate while preserving order
    seen = set()
    uniq: List[Path] = []
    for pp in expanded:
        key = str(pp)
        if key not in seen:
            seen.add(key)
            uniq.append(pp)
    return uniq


@app.command()
def query(
    files: Optional[List[str]] = typer.Option(
        None,
        "--files",
        "-f",
        help="JSON files to process (glob patterns supported). Example: --files DATA/*.json",
    ),
    all_files: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Process all JSON files in DATA directory",
    ),
    data_dir: Optional[str] = typer.Option(
        None,
        "--data-dir",
        "-d",
        help="Data directory (default: ./DATA)",
    ),
    filter_expr: Optional[str] = typer.Option(
        None,
        "--filter",
        help='Filter expression (e.g., "criterion_id:APP_B_I AND record_side:RULE")',
    ),
    allow_unfiltered_preview: bool = typer.Option(
        False,
        "--allow-unfiltered-preview",
        help="Development only: show unfiltered preview after a filter error; export stays blocked.",
    ),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        "-c",
        help="Comma-separated list of columns to export",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (.csv or .xlsx)",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        help="Output format: csv or xlsx",
    ),
    allow_validation_errors: bool = typer.Option(
        False,
        "--allow-validation-errors",
        help="Development only: permit export with ERROR validation issues; requires a reason.",
    ),
    validation_override_reason: Optional[str] = typer.Option(
        None,
        "--validation-override-reason",
        help="Recorded reason for development-only export of validation errors.",
    ),
    show_errors: bool = typer.Option(
        True,
        "--show-errors/--no-errors",
        help="Show validation errors and warnings",
    ),
    show_preview: bool = typer.Option(
        False,
        "--preview",
        "-p",
        help="Show preview of results (first 10 rows)",
    ),
) -> None:
    """
    Query JSON extraction files and optionally export results.
    """
    config = get_config()

    # Validate inputs
    if not files and not all_files:
        console.print("[red]Error: Must specify --files or --all[/red]")
        raise typer.Exit(1)

    # Prepare file paths
    file_paths: Optional[List[Path]] = None
    if files:
        expanded = _expand_globs(files)
        file_paths = expanded if expanded else []

    # Prepare data directory
    data_dir_path = Path(data_dir) if data_dir else config.data_dir

    # Prepare columns
    column_list: Optional[List[str]] = None
    if columns:
        parsed = [c.strip() for c in columns.split(",") if c.strip()]
        column_list = parsed if parsed else None

    # Run pipeline
    console.print("[cyan]Running pipeline...[/cyan]")
    try:
        result = run_pipeline(
            file_paths=file_paths,
            data_dir=data_dir_path if all_files else None,
            filter_expr=filter_expr,
            columns=column_list,
            allow_unfiltered_preview=allow_unfiltered_preview,
        )
    except Exception as e:
        console.print(f"[red]Pipeline error: {str(e)}[/red]")
        raise typer.Exit(1)

    filter_error = getattr(result, "filter_error", None)
    if filter_error:
        console.print(f"[red]Filter error:[/red] {filter_error}")
        if not allow_unfiltered_preview or not show_preview:
            if allow_unfiltered_preview and not show_preview:
                console.print("[red]--allow-unfiltered-preview requires --preview.[/red]")
            raise typer.Exit(2)
        console.print("[bold yellow]DEVELOPMENT OVERRIDE: showing unfiltered preview; export is blocked.[/bold yellow]")
        if output:
            console.print("[red]Export blocked while filter_error is set.[/red]")
            raise typer.Exit(2)

    # Show statistics
    console.print("\n[green]✓[/green] Pipeline complete")
    console.print(f"  Files processed: {getattr(result, 'files_processed', 0)}")
    console.print(f"  Items loaded: {getattr(result, 'items_loaded', 0)}")
    console.print(f"  Items after filter: {getattr(result, 'items_after_filter', 0)}")

    # Show errors if requested
    if show_errors and (getattr(result, "bad_files", None) or getattr(result, "validation_errors", None)):
        console.print("\n[yellow]Issues detected:[/yellow]")
        console.print(result.get_error_summary())

    # Show preview if requested
    df = getattr(result, "df", None)
    if show_preview and df is not None and not df.empty:
        console.print("\n[cyan]Preview (first 10 rows):[/cyan]")
        table = Table(show_header=True, header_style="bold magenta")

        # Add columns (limit for readability)
        preview_columns = list(df.columns)[:6]
        for col in preview_columns:
            table.add_column(col, overflow="fold")

        # Add rows
        for _, row in df.head(10).iterrows():
            table.add_row(*[str(row[col])[:80] for col in preview_columns])

        console.print(table)

        if len(df.columns) > len(preview_columns):
            console.print(f"  ... and {len(df.columns) - len(preview_columns)} more columns")

    # Export if output path provided
    if output:
        if df is None or df.empty:
            console.print("[yellow]Warning: No results to export[/yellow]")
        else:
            error_count = sum(1 for e in getattr(result, "validation_errors", []) if e.severity == "ERROR")
            if error_count:
                reason = (validation_override_reason or "").strip()
                if not allow_validation_errors or not reason:
                    console.print(
                        f"[red]Export blocked: {error_count} ERROR validation issue(s). "
                        "Development override requires --allow-validation-errors and "
                        "--validation-override-reason.[/red]"
                    )
                    raise typer.Exit(2)
                console.print(f"[bold yellow]VALIDATION OVERRIDE:[/bold yellow] {reason}")
            output_path = Path(output)
            try:
                actual_path = export_pipeline_result(
                    result=result,
                    output_path=output_path,
                    columns=column_list,
                    fmt=format,
                    validation_override_reason=(validation_override_reason if allow_validation_errors else None),
                )
                console.print(f"\n[green]✓[/green] Exported to: {actual_path}")
            except Exception as e:
                console.print(f"[red]Export error: {str(e)}[/red]")
                raise typer.Exit(1)
    else:
        console.print("\n[dim]No output file specified. Use --output to export results.[/dim]")


@app.command()
def list_files(
    data_dir: Optional[str] = typer.Option(
        None,
        "--data-dir",
        "-d",
        help="Data directory (default: ./DATA)",
    )
) -> None:
    """List available JSON files in the data directory."""
    config = get_config()
    data_dir_path = Path(data_dir) if data_dir else config.data_dir

    if not data_dir_path.exists():
        console.print(f"[red]Data directory does not exist: {data_dir_path}[/red]")
        raise typer.Exit(1)

    from src.json_extractor.io import discover_json_files

    files = discover_json_files(data_dir_path)

    if not files:
        console.print(f"[yellow]No JSON files found in {data_dir_path}[/yellow]")
        return

    console.print(f"\n[cyan]JSON files in {data_dir_path}:[/cyan]")
    for i, file_path in enumerate(files, 1):
        console.print(f"  {i}. {file_path.name}")

    console.print(f"\n[green]Total: {len(files)} files[/green]")


@app.command()
def info() -> None:
    """Show configuration and system information."""
    config = get_config()

    console.print("\n[cyan]JSON Extractor vNext - Configuration[/cyan]")
    console.print(f"Data directory: {config.data_dir}")
    console.print(f"Config directory: {config.config_dir}")
    console.print(f"Column defaults file: {config.column_defaults_path}")

    console.print(f"\n[cyan]Default columns ({len(config.default_columns)}):[/cyan]")
    for col in config.default_columns:
        console.print(f"  - {col}")

    console.print("\n[cyan]Appendix B Criteria (18 total):[/cyan]")
    criteria = config.get_canonical_criteria()
    for criterion in criteria[:5]:
        console.print(f"  - {criterion['criterion_id']}: {criterion['criterion_name']}")
    if len(criteria) > 5:
        console.print(f"  ... and {len(criteria) - 5} more")


if __name__ == "__main__":
    app()
