# ------------------------
# tests/test_query_engine_or.py
# ------------------------
from __future__ import annotations

import pandas as pd

from src.json_extractor.query import QueryEngine, parse_filter_dsl


def _df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "criterion_id": ["APP_B_I", "APP_B_II", "APP_B_II", "APP_B_III", "APP_B_IV"],
            "item_type": ["control", "reference", "control", "control", "reference"],
            "statement": ["a", "b", "c", "d", "e"],
        }
    )


def test_or_returns_union() -> None:
    df = _df()
    q = parse_filter_dsl("criterion_id:APP_B_I OR criterion_id:APP_B_II")
    out = QueryEngine.execute_on_df(df, q)

    assert len(out) == 3
    assert set(out["statement"].tolist()) == {"a", "b", "c"}


def test_and_precedence_inside_or() -> None:
    df = _df()
    # A OR (B AND C)
    q = parse_filter_dsl("criterion_id:APP_B_I OR criterion_id:APP_B_II AND item_type:control")
    out = QueryEngine.execute_on_df(df, q)

    assert len(out) == 2
    assert set(out["statement"].tolist()) == {"a", "c"}


def test_mixed_or_of_and() -> None:
    df = _df()
    # (APP_B_II AND reference) OR APP_B_IV
    q = parse_filter_dsl("criterion_id:APP_B_II AND item_type:reference OR criterion_id:APP_B_IV")
    out = QueryEngine.execute_on_df(df, q)

    assert len(out) == 2
    assert set(out["statement"].tolist()) == {"b", "e"}


def test_empty_query_returns_all_rows() -> None:
    df = _df()
    q = parse_filter_dsl("")
    out = QueryEngine.execute_on_df(df, q)

    assert len(out) == len(df)
