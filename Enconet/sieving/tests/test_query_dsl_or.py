# ------------------------
# tests/test_query_dsl_or.py
# ------------------------
from __future__ import annotations

import pytest

from src.json_extractor.query import parse_filter_dsl
from src.json_extractor.query.compiler import DSLParseError


def test_or_splits_into_clauses() -> None:
    q = parse_filter_dsl("criterion_id:APP_B_I AND record_side:RULE OR criterion_id:APP_B_II")

    assert q.clauses is not None
    assert len(q.clauses) == 2
    assert len(q.clauses[0]) == 2
    assert len(q.clauses[1]) == 1

    # Clause 1 contains criterion_id and record_side
    assert q.clauses[0][0].field == "criterion_id"
    assert q.clauses[0][1].field == "record_side"

    # Clause 2 contains criterion_id only
    assert q.clauses[1][0].field == "criterion_id"


def test_and_precedence_over_or() -> None:
    q = parse_filter_dsl("criterion_id:APP_B_I OR criterion_id:APP_B_II AND item_type:control")
    assert len(q.clauses) == 2

    # AND binds tighter than OR => [[A], [B, C]]
    assert len(q.clauses[0]) == 1
    assert q.clauses[0][0].field == "criterion_id"
    assert q.clauses[0][0].value == "APP_B_I"

    assert len(q.clauses[1]) == 2
    assert q.clauses[1][0].field == "criterion_id"
    assert q.clauses[1][0].value == "APP_B_II"
    assert q.clauses[1][1].field == "item_type"
    assert q.clauses[1][1].value == "control"


@pytest.mark.parametrize(
    "expr",
    [
        "OR criterion_id:APP_B_I",
        "criterion_id:APP_B_I OR",
        "criterion_id:APP_B_I AND OR criterion_id:APP_B_II",
        "criterion_id:APP_B_I criterion_id:APP_B_II",  # missing operator
    ],
)
def test_invalid_or_syntax_raises(expr: str) -> None:
    with pytest.raises(DSLParseError):
        parse_filter_dsl(expr)
