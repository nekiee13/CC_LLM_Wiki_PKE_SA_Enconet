# ------------------------
# src/json_extractor/query/__init__.py
# ------------------------
"""
Query system: schema, DSL compiler, and execution engine.
"""

from .schema import QuerySchema, FieldDef
from .compiler import parse_filter_dsl, QueryFilter, CompiledQuery
from .engine import QueryEngine

__all__ = [
    "QuerySchema",
    "FieldDef",
    "parse_filter_dsl",
    "QueryFilter",
    "CompiledQuery",
    "QueryEngine",
]
