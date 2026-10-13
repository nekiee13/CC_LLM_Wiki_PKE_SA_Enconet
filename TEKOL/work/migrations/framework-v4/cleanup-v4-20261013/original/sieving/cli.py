#!/usr/bin/env python3
"""Project-local JSON sieving query and export command.

Paths start at this project root, even when run from another folder.
Diagnostic overrides are not owner approval or audit findings.
"""
from __future__ import annotations

from fnmatch import fnmatchcase
from pathlib import Path
from typing import Iterator, List, Optional

import typer
from rich.console import Console
from rich.table import Table

from src.json_extractor.config import get_config
from src.json_extractor.io import discover_json_files
from src.json_extractor.io._paths import PROJECT_ROOT, local_io_path
from src.json_extractor.pipeline import export_pipeline_result, run_pipeline


app = typer.Typer(help=f"{PROJECT_ROOT.name}-local JSON sieving query and export")
console = Console()
_WILDCARDS = "*?["


def _glob_parts(base: Path, parts: tuple[str, ...]) -> Iterator[Path]:
    """Walk only checked local directories; never recurse through a link."""
    base = local_io_path(base)
    if not parts:
        yield base
        return
    if not base.is_dir():
        return
    head, *rest = parts
    tail = tuple(rest)
    if head == "**":
        yield from _glob_parts(base, tail)
        for child in sorted(base.iterdir()):
            checked = local_io_path(child)
            if checked.is_dir() and not child.is_symlink():
                yield from _glob_parts(checked, parts)
        return
    if any(char in head for char in _WILDCARDS):
        for child in sorted(base.iterdir()):
            if fnmatchcase(child.name, head):
                checked = local_io_path(child)
                if not tail or (checked.is_dir() and not child.is_symlink()):
                    yield from _glob_parts(checked, tail)
        return
    checked = local_io_path(base / head)
    if not tail or (checked.is_dir() and not (base / head).is_symlink()):
        yield from _glob_parts(checked, tail)


def _expand_globs(patterns: List[str]) -> List[Path]:
    """Return stable, de-duplicated local files or missing direct paths."""
    expanded: List[Path] = []
    for raw in patterns:
        raw = (raw or "").strip()
        if not raw:
            continue
        pattern = Path(raw)
        if any(char in raw for char in _WILDCARDS):
            if ".." in pattern.parts:
                raise ValueError("Glob patterns may not traverse parent folders")
            full = pattern if pattern.is_absolute() else PROJECT_ROOT / pattern
            parts = full.parts
            first_glob = next(index for index, part in enumerate(parts)
                              if any(char in part for char in _WILDCARDS))
            base = local_io_path(Path(*parts[:first_glob]))
            for candidate in _glob_parts(base, tuple(parts[first_glob:])):
                checked = local_io_path(candidate)
                if checked.is_file():
                    expanded.append(checked)
        else:
            expanded.append(local_io_path(pattern))
    return list(dict.fromkeys(expanded))


def _checked_path(raw: Optional[str], default: Path) -> Path:
    return local_io_path(Path(raw)) if raw else local_io_path(default)


@app.command()
def query(
    files: Optional[List[str]] = typer.Option(None, "--files", "-f", help=f"{PROJECT_ROOT.name}-local JSON files or globs"),
    all_files: bool = typer.Option(False, "--all", "-a", help="Process all JSON files in the local data folder"),
    data_dir: Optional[str] = typer.Option(None, "--data-dir", "-d", help="Project-relative data folder"),
    filter_expr: Optional[str] = typer.Option(None, "--filter", help="Query filter expression"),
    allow_unfiltered_preview: bool = typer.Option(
        False, "--allow-unfiltered-preview", help="Development preview after a filter error; export stays blocked"
    ),
    columns: Optional[str] = typer.Option(None, "--columns", "-c", help="Comma-separated export columns"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Project-relative .csv or .xlsx output"),
    format: Optional[str] = typer.Option(None, "--format", help="Output format: csv or xlsx"),
    allow_validation_errors: bool = typer.Option(
        False, "--allow-validation-errors", help="Development export of validation errors; requires a reason"
    ),
    validation_override_reason: Optional[str] = typer.Option(
        None, "--validation-override-reason", help="Recorded reason for development-only validation override"
    ),
    show_errors: bool = typer.Option(True, "--show-errors/--no-errors", help="Show validation issues"),
    show_preview: bool = typer.Option(False, "--preview", "-p", help="Show first 10 result rows"),
) -> None:
    """Query local extraction files and optionally export guarded results."""
    config = get_config()
    if not files and not all_files:
        console.print("[red]Error: Must specify --files or --all[/red]")
        raise typer.Exit(1)
    try:
        file_paths = _expand_globs(files) if files else None
        data_dir_path = _checked_path(data_dir, config.data_dir)
        output_path = _checked_path(output, PROJECT_ROOT) if output else None
    except ValueError as exc:
        console.print(f"[red]Path error: {exc}[/red]")
        raise typer.Exit(2) from exc

    column_list = ([value.strip() for value in columns.split(",") if value.strip()]
                   if columns else None)
    console.print("[cyan]Running pipeline...[/cyan]")
    try:
        result = run_pipeline(
            file_paths=file_paths,
            data_dir=data_dir_path if all_files else None,
            filter_expr=filter_expr,
            columns=column_list,
            allow_unfiltered_preview=allow_unfiltered_preview,
        )
    except Exception as exc:
        console.print(f"[red]Pipeline error: {exc}[/red]")
        raise typer.Exit(1) from exc

    if result.filter_error:
        console.print(f"[red]Filter error:[/red] {result.filter_error}")
        if not allow_unfiltered_preview or not show_preview:
            if allow_unfiltered_preview and not show_preview:
                console.print("[red]--allow-unfiltered-preview requires --preview.[/red]")
            raise typer.Exit(2)
        console.print("[bold yellow]DEVELOPMENT OVERRIDE: showing unfiltered preview; export is blocked.[/bold yellow]")
        if output_path:
            console.print("[red]Export blocked while filter_error is set.[/red]")
            raise typer.Exit(2)

    console.print("\n[green]✓[/green] Pipeline complete")
    console.print(f"  Files processed: {result.files_processed}")
    console.print(f"  Items loaded: {result.items_loaded}")
    console.print(f"  Items after filter: {result.items_after_filter}")
    if show_errors and (result.bad_files or result.validation_errors):
        console.print("\n[yellow]Issues detected:[/yellow]")
        console.print(result.get_error_summary())
    df = result.df
    if show_preview and not df.empty:
        console.print("\n[cyan]Preview (first 10 rows):[/cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        preview_columns = list(df.columns)[:6]
        for column in preview_columns:
            table.add_column(column, overflow="fold")
        for _, row in df.head(10).iterrows():
            table.add_row(*[str(row[column])[:80] for column in preview_columns])
        console.print(table)
        if len(df.columns) > len(preview_columns):
            console.print(f"  ... and {len(df.columns) - len(preview_columns)} more columns")

    if not output_path:
        console.print("\n[dim]No output file specified. Use --output to export results.[/dim]")
        return
    if df.empty:
        console.print("[yellow]Warning: No results to export[/yellow]")
        return
    error_count = sum(issue.severity == "ERROR" for issue in result.validation_errors)
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
    try:
        actual_path = export_pipeline_result(
            result=result, output_path=output_path, columns=column_list, fmt=format,
            validation_override_reason=(validation_override_reason if allow_validation_errors else None),
        )
    except Exception as exc:
        console.print(f"[red]Export error: {exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"\n[green]✓[/green] Exported to: {actual_path}")


@app.command()
def list_files(data_dir: Optional[str] = typer.Option(None, "--data-dir", "-d", help="Project-relative data folder")) -> None:
    """List JSON files under the local data folder."""
    config = get_config()
    try:
        data_dir_path = _checked_path(data_dir, config.data_dir)
    except ValueError as exc:
        console.print(f"[red]Path error: {exc}[/red]")
        raise typer.Exit(2) from exc
    if not data_dir_path.exists():
        console.print(f"[red]Data directory does not exist: {data_dir_path}[/red]")
        raise typer.Exit(1)
    try:
        paths = discover_json_files(data_dir_path)
    except ValueError as exc:
        console.print(f"[red]Path error: {exc}[/red]")
        raise typer.Exit(2) from exc
    if not paths:
        console.print(f"[yellow]No JSON files found in {data_dir_path}[/yellow]")
        return
    console.print(f"\n[cyan]JSON files in {data_dir_path}:[/cyan]")
    for index, file_path in enumerate(paths, 1):
        console.print(f"  {index}. {file_path.name}")
    console.print(f"\n[green]Total: {len(paths)} files[/green]")


@app.command()
def info() -> None:
    """Show paths and unapproved template labels, without reading documents."""
    config = get_config()
    console.print(f"\n[cyan]{PROJECT_ROOT.name} JSON Sieving - Configuration[/cyan]")
    console.print(f"Data directory: {config.data_dir}")
    console.print(f"Config directory: {config.config_dir}")
    console.print(f"Column defaults file: {config.column_defaults_path}")
    console.print(f"\n[cyan]Default columns ({len(config.default_columns)}):[/cyan]")
    for column in config.default_columns:
        console.print(f"  - {column}")
    criteria = config.get_canonical_criteria()
    console.print(f"\n[cyan]Appendix B template criteria ({len(criteria)} total; scope not approved):[/cyan]")
    for criterion in criteria[:5]:
        console.print(f"  - {criterion['criterion_id']}: {criterion['criterion_name']}")
    if len(criteria) > 5:
        console.print(f"  ... and {len(criteria) - 5} more")


if __name__ == "__main__":
    app()
