"""Apply the local query DSL to synthetic or approved record tables."""
from __future__ import annotations

from typing import List

import pandas as pd

from .compiler import CompiledQuery, QueryFilter


class QueryEngine:
    """Apply OR-of-AND query clauses to a pandas DataFrame."""

    KEYWORD_SEARCH_FIELDS = [
        "statement", "evidence_quote_1", "entities_organizations", "entities_people",
        "entities_documents", "entities_systems_tools", "entities_standards_regulations",
        "rule_citation_text", "rule_ref_keys", "rule_ref_codes", "rule_ref_locators",
    ]
    MAX_CLAUSES = 1000

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def apply_filter(self, filter_obj: QueryFilter) -> pd.Series:
        """Return the matching-row mask for one supported predicate."""
        if self.df.empty:
            return pd.Series([], dtype=bool, index=self.df.index)
        if filter_obj.field == "keyword":
            return self._apply_keyword_filter(filter_obj.value)
        if filter_obj.field not in self.df.columns:
            return pd.Series([False] * len(self.df), index=self.df.index)
        series = self.df[filter_obj.field]
        op = (filter_obj.operator or "").strip().lower()
        if op == "equals":
            return series == filter_obj.value
        if op == "equals_ci":
            return series.fillna("").astype(str).str.lower() == str(filter_obj.value).lower()
        if op == "contains_ci":
            return series.fillna("").astype(str).str.contains(
                str(filter_obj.value), case=False, regex=False, na=False,
            )
        if op == "in":
            values = [value.strip() for value in str(filter_obj.value).split(",") if value.strip()]
            if not values:
                return pd.Series([False] * len(self.df), index=self.df.index)
            return series.isin(values)
        return pd.Series([False] * len(self.df), index=self.df.index)

    def _apply_keyword_filter(self, keyword: str) -> pd.Series:
        if self.df.empty:
            return pd.Series([], dtype=bool, index=self.df.index)
        value = (keyword or "").strip()
        if not value:
            return pd.Series([True] * len(self.df), index=self.df.index)
        mask = pd.Series([False] * len(self.df), index=self.df.index)
        for field in self.KEYWORD_SEARCH_FIELDS:
            if field in self.df.columns:
                mask = mask | self.df[field].fillna("").astype(str).str.contains(
                    value, case=False, regex=False, na=False,
                )
        return mask

    def _execute_or_of_and(self, clauses: List[List[QueryFilter]]) -> pd.DataFrame:
        if len(clauses) > self.MAX_CLAUSES:
            raise ValueError(
                f"Too many OR clauses ({len(clauses)}). Reduce expression complexity or use IN where possible."
            )
        if self.df.empty or not clauses:
            return self.df
        final_mask = pd.Series([False] * len(self.df), index=self.df.index)
        for clause in clauses:
            if final_mask.all():
                break
            if not clause:
                continue
            clause_mask = pd.Series([True] * len(self.df), index=self.df.index)
            for item in clause:
                if not clause_mask.any():
                    break
                clause_mask = clause_mask & self.apply_filter(item)
            final_mask = final_mask | clause_mask
        return self.df[final_mask]

    def execute(self, query: CompiledQuery) -> pd.DataFrame:
        """Filter rows, enforcing expression limits even for an empty table."""
        clauses = getattr(query, "clauses", None)
        if clauses:
            return self._execute_or_of_and(clauses)
        if self.df.empty:
            return self.df
        filters = getattr(query, "filters", None) or []
        if not filters:
            return self.df
        mask = pd.Series([True] * len(self.df), index=self.df.index)
        for item in filters:
            if not mask.any():
                break
            mask = mask & self.apply_filter(item)
        return self.df[mask]

    @classmethod
    def execute_on_df(cls, df: pd.DataFrame, query: CompiledQuery) -> pd.DataFrame:
        return cls(df).execute(query)
