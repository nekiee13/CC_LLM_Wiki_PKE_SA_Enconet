# ------------------------
# src/json_extractor/query/engine.py
# ------------------------
"""
Query execution engine.

Applies compiled queries to pandas DataFrames.

Semantics (vNext):
- If CompiledQuery.clauses is present and non-empty:
    clauses = [[A,B],[C]] means (A AND B) OR (C)
- Otherwise (legacy / backward-compatible path):
    query.filters are combined with AND

Operators supported (as emitted by compiler.py):
- equals
- equals_ci
- contains_ci
- in
- keyword (special pseudo-field): contains_ci across KEYWORD_SEARCH_FIELDS
"""

from __future__ import annotations

from typing import List

import pandas as pd

from .compiler import CompiledQuery, QueryFilter


class QueryEngine:
    """
    Execute compiled queries against normalized record DataFrames.
    """

    # Fields to search for keyword queries (engine-defined contract)
    KEYWORD_SEARCH_FIELDS = [
        "statement",
        "evidence_quote_1",
        "entities_organizations",
        "entities_people",
        "entities_documents",
        "entities_systems_tools",
        "entities_standards_regulations",
        "rule_citation_text",
        "rule_ref_keys",
        "rule_ref_codes",
        "rule_ref_locators",
    ]

    # Guardrail against pathological OR expressions
    MAX_CLAUSES = 1000

    def __init__(self, df: pd.DataFrame):
        """
        Initialize query engine with a DataFrame.

        Args:
            df: DataFrame of normalized records.
        """
        self.df = df

    def apply_filter(self, filter_obj: QueryFilter) -> pd.Series:
        """
        Apply a single filter to the DataFrame.

        Args:
            filter_obj: Filter to apply.

        Returns:
            Boolean Series indicating which rows match.
        """
        if self.df.empty:
            return pd.Series([], dtype=bool, index=self.df.index)

        # Special handling for keyword filter (pseudo-field)
        if filter_obj.field == "keyword":
            return self._apply_keyword_filter(filter_obj.value)

        # Field existence check
        if filter_obj.field not in self.df.columns:
            # Field doesn't exist - no matches
            return pd.Series([False] * len(self.df), index=self.df.index)

        series = self.df[filter_obj.field]
        op = (filter_obj.operator or "").strip().lower()

        if op == "equals":
            return series == filter_obj.value

        if op == "equals_ci":
            return series.fillna("").astype(str).str.lower() == str(filter_obj.value).lower()

        if op == "contains_ci":
            return series.fillna("").astype(str).str.contains(
                str(filter_obj.value),
                case=False,
                regex=False,
                na=False,
            )

        if op == "in":
            values = [v.strip() for v in str(filter_obj.value).split(",") if v.strip()]
            if not values:
                return pd.Series([False] * len(self.df), index=self.df.index)
            return series.isin(values)

        # Unknown operator - fail-closed
        return pd.Series([False] * len(self.df), index=self.df.index)

    def _apply_keyword_filter(self, keyword: str) -> pd.Series:
        """
        Apply keyword search across multiple fields.

        Args:
            keyword: Keyword to search for.

        Returns:
            Boolean Series indicating which rows contain the keyword.
        """
        if self.df.empty:
            return pd.Series([], dtype=bool, index=self.df.index)

        kw = (keyword or "").strip()
        if not kw:
            # Empty keyword should not filter out rows
            return pd.Series([True] * len(self.df), index=self.df.index)

        mask = pd.Series([False] * len(self.df), index=self.df.index)

        for field in self.KEYWORD_SEARCH_FIELDS:
            if field not in self.df.columns:
                continue
            field_mask = self.df[field].fillna("").astype(str).str.contains(
                kw,
                case=False,
                regex=False,
                na=False,
            )
            mask = mask | field_mask

        return mask

    def _execute_or_of_and(self, clauses: List[List[QueryFilter]]) -> pd.DataFrame:
        """
        Execute OR-of-AND clauses:
            final_mask = OR over clauses of (AND over filters in clause)
        """
        if self.df.empty:
            return self.df

        if not clauses:
            return self.df

        if len(clauses) > self.MAX_CLAUSES:
            raise ValueError(
                f"Too many OR clauses ({len(clauses)}). Reduce expression complexity or use IN where possible."
            )

        final_mask = pd.Series([False] * len(self.df), index=self.df.index)

        for clause in clauses:
            if final_mask.all():
                break
            if not clause:
                continue

            clause_mask = pd.Series([True] * len(self.df), index=self.df.index)

            for fobj in clause:
                if not clause_mask.any():
                    break
                clause_mask = clause_mask & self.apply_filter(fobj)

            final_mask = final_mask | clause_mask

        return self.df[final_mask]

    def execute(self, query: CompiledQuery) -> pd.DataFrame:
        """
        Execute a compiled query and return filtered DataFrame.

        Args:
            query: Compiled query to execute.

        Returns:
            Filtered DataFrame.
        """
        if self.df.empty:
            return self.df

        clauses = getattr(query, "clauses", None)
        if clauses:
            return self._execute_or_of_and(clauses)

        # Legacy: AND over query.filters
        filters = getattr(query, "filters", None) or []
        if not filters:
            return self.df

        mask = pd.Series([True] * len(self.df), index=self.df.index)
        for fobj in filters:
            if not mask.any():
                break
            mask = mask & self.apply_filter(fobj)

        return self.df[mask]

    @classmethod
    def execute_on_df(cls, df: pd.DataFrame, query: CompiledQuery) -> pd.DataFrame:
        """
        Convenience method to execute a query on a DataFrame.

        Args:
            df: DataFrame to query.
            query: Compiled query.

        Returns:
            Filtered DataFrame.
        """
        return cls(df).execute(query)
