# ------------------------
# tests/test_pipeline_or.py
# ------------------------
"""
Pipeline regression test for OR semantics (end-to-end).

run_pipeline signature (repo-verified):
    run_pipeline(
        file_paths: Optional[List[Path]] = None,
        data_dir: Optional[Path] = None,
        file_patterns: Optional[List[str]] = None,
        filter_expr: Optional[str] = None,
        columns: Optional[List[str]] = None
    ) -> PipelineResult

Test strategy (code-aligned and assumption-minimized):
1) Use real repo JSON files under DATA/ (DOCUMENT preferred).
2) Run pipeline with no filter to obtain df_all and discover two criterion_id values that exist.
3) Run A, B, and A OR B.
4) Because criterion_id is an equality filter on a single column, sets are disjoint:
     len(A OR B) == len(A) + len(B)

Acceptance criteria:
- df_all is non-empty and includes 'criterion_id'.
- Two distinct criterion_id values can be selected.
- OR query returns additive union and only contains {A,B}.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from src.json_extractor.pipeline import run_pipeline


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _pick_data_files() -> List[Path]:
    """
    Deterministic selection of real JSON inputs.

    Preference order:
      1) DATA/DOCUMENT/*.json (first 3)
      2) DATA/RULE/*.json (first 2)

    Excludes *.json.bak (should not match *.json, but kept defensive).
    """
    root = _repo_root()
    data_dir = root / "DATA"
    if not data_dir.exists():
        raise AssertionError(f"Expected DATA directory not found: {data_dir}")

    def collect(dir_path: Path) -> List[Path]:
        if not dir_path.exists():
            return []
        paths = sorted([p for p in dir_path.rglob("*.json") if p.is_file()])
        paths = [p for p in paths if not p.name.lower().endswith(".json.bak")]
        return paths

    doc_paths = collect(data_dir / "DOCUMENT")
    rule_paths = collect(data_dir / "RULE")

    if doc_paths:
        return doc_paths[:3]
    if rule_paths:
        return rule_paths[:2]

    raise AssertionError("No usable *.json files found under DATA/DOCUMENT or DATA/RULE")


def _extract_df(result) -> pd.DataFrame:
    """
    Extract DataFrame from PipelineResult.

    PipelineResult in this repo is expected to expose .df, but keep a small
    compatibility shim to avoid tight coupling.
    """
    if isinstance(result, pd.DataFrame):
        return result
    for attr in ("df", "dataframe", "results_df", "result_df"):
        if hasattr(result, attr):
            df = getattr(result, attr)
            if isinstance(df, pd.DataFrame):
                return df
    raise AssertionError("Unexpected PipelineResult shape: no DataFrame attribute found")


def test_run_pipeline_or_returns_union_on_real_data() -> None:
    file_paths = _pick_data_files()

    # 1) Unfiltered pipeline run (filter_expr=None preserves "no filter" semantics)
    res_all = run_pipeline(
        file_paths=file_paths,
        filter_expr=None,
        columns=None,
        data_dir=None,
        file_patterns=None,
    )
    df_all = _extract_df(res_all)

    assert not df_all.empty, (
        "Pipeline returned an empty DataFrame for real DATA files. "
        "This suggests ingestion failed silently or the selected inputs contain no flattenable items."
    )
    assert "criterion_id" in df_all.columns, (
        "Pipeline output did not include 'criterion_id'. "
        "This indicates an unexpected normalized schema or column projection."
    )

    crit_values = sorted([c for c in df_all["criterion_id"].dropna().astype(str).unique().tolist() if c])
    assert len(crit_values) >= 2, (
        "At least two distinct criterion_id values are required to validate OR union semantics. "
        "Selected DATA files may not include taxonomy fields."
    )

    a = crit_values[0]
    b = crit_values[1]

    # 2) A, B, and A OR B runs
    res_a = run_pipeline(
        file_paths=file_paths,
        filter_expr=f"criterion_id:{a}",
        columns=None,
        data_dir=None,
        file_patterns=None,
    )
    df_a = _extract_df(res_a)

    res_b = run_pipeline(
        file_paths=file_paths,
        filter_expr=f"criterion_id:{b}",
        columns=None,
        data_dir=None,
        file_patterns=None,
    )
    df_b = _extract_df(res_b)

    res_or = run_pipeline(
        file_paths=file_paths,
        filter_expr=f"criterion_id:{a} OR criterion_id:{b}",
        columns=None,
        data_dir=None,
        file_patterns=None,
    )
    df_or = _extract_df(res_or)

    # Guardrails: A and B were selected from df_all, so each should match at least one row.
    assert not df_a.empty, f"Expected non-empty results for criterion_id:{a}"
    assert not df_b.empty, f"Expected non-empty results for criterion_id:{b}"
    assert not df_or.empty, "Expected non-empty results for OR query"

    # Equality filters on a single field are mutually exclusive -> additive union size
    assert len(df_or) == len(df_a) + len(df_b)

    # Sanity: OR results must be restricted to the OR set
    assert set(df_or["criterion_id"].astype(str).unique().tolist()).issubset({a, b})
