"""Local query DSL compiler, adapted from the pinned Enconet source.

The established grammar is kept: AND binds tighter than OR, enum commas
mean IN, and spaces inside values remain part of the value.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .schema import FieldType, QuerySchema


@dataclass(frozen=True)
class QueryFilter:
    field: str
    operator: str
    value: str


@dataclass(frozen=True)
class CompiledQuery:
    filters: List[QueryFilter] = field(default_factory=list)
    clauses: List[List[QueryFilter]] = field(default_factory=list)
    combination: str = "AND"


class DSLParseError(Exception):
    """The filter expression is invalid or ambiguous."""


def tokenize_filter_expression(expr: str) -> List[str]:
    """Split into terms and logical operators, preserving value spaces."""
    tokens: List[str] = []
    current_term: List[str] = []

    def looks_like_term_start(word: str) -> bool:
        if ":" not in word:
            return False
        candidate = word.split(":", 1)[0].strip()
        return candidate == "keyword" or bool(candidate and QuerySchema.get_field(candidate))

    for word in (expr or "").split():
        upper = word.upper()
        if upper in ("AND", "OR"):
            if current_term:
                tokens.append(" ".join(current_term))
                current_term = []
            tokens.append(upper)
        elif current_term and looks_like_term_start(word):
            tokens.append(" ".join(current_term))
            current_term = [word]
        else:
            current_term.append(word)
    if current_term:
        tokens.append(" ".join(current_term))
    return tokens


def _normalize_in_values(raw_value: str) -> List[str]:
    return [part for part in (value.strip() for value in (raw_value or "").split(",")) if part]


def parse_term(term: str) -> QueryFilter:
    """Parse one field:value term using the local contract's field types."""
    if ":" not in term:
        raise DSLParseError(f"Term must contain ':' separator: {term}")
    field_part, value_part = term.split(":", 1)
    field_name, value_raw = field_part.strip(), value_part.strip()
    if not field_name or not value_raw:
        raise DSLParseError(f"Empty field or value in term: {term}")
    if field_name == "keyword":
        return QueryFilter("keyword", "contains_ci", value_raw)
    field_def = QuerySchema.get_field(field_name)
    if not field_def:
        raise DSLParseError(f"Unknown field: {field_name}")
    if field_def.field_type == FieldType.ENUM:
        if "," in value_raw:
            values = _normalize_in_values(value_raw)
            if len(values) < 2:
                if not values:
                    raise DSLParseError(f"Empty value list in term: {term}")
                return QueryFilter(field_name, "equals", values[0])
            return QueryFilter(field_name, "in", ",".join(values))
        return QueryFilter(field_name, "equals", value_raw)
    if field_def.field_type == FieldType.STRING:
        return QueryFilter(field_name, "contains_ci", value_raw)
    if field_def.field_type == FieldType.NUMBER:
        return QueryFilter(field_name, "equals", value_raw)
    return QueryFilter(field_name, "equals", value_raw)


def parse_filter_dsl(expr: str) -> CompiledQuery:
    """Compile terms into OR-of-AND clauses; reject missing terms or operators."""
    if not expr or not expr.strip():
        return CompiledQuery()
    tokens = tokenize_filter_expression(expr.strip())
    if not tokens:
        return CompiledQuery()
    clauses: List[List[QueryFilter]] = []
    current_clause: List[QueryFilter] = []
    expecting_term = True
    for token in tokens:
        if token in ("AND", "OR"):
            if expecting_term:
                raise DSLParseError(f"Unexpected operator '{token}' (missing term)")
            if token == "OR":
                if not current_clause:
                    raise DSLParseError("Empty clause before OR")
                clauses.append(current_clause)
                current_clause = []
            expecting_term = True
            continue
        if not expecting_term:
            raise DSLParseError(f"Missing operator between terms near: '{token}'")
        try:
            current_clause.append(parse_term(token))
        except DSLParseError as exc:
            raise DSLParseError(f"Error parsing term '{token}': {exc}") from exc
        expecting_term = False
    if expecting_term:
        raise DSLParseError("Expression cannot end with an operator")
    if current_clause:
        clauses.append(current_clause)
    return CompiledQuery(
        filters=[item for clause in clauses for item in clause],
        clauses=clauses,
        combination="AND",
    )


def validate_compiled_query(query: CompiledQuery) -> List[str]:
    """Return clause-local warnings for conflicting sides and side-only fields."""
    warnings: List[str] = []
    rule_only = {"rule_source_rules", "rule_locator", "rule_key", "rule_strength"}
    document_only = {"rule_ref_keys", "rule_ref_codes", "rule_ref_locators"}

    def warn_clause(filters: List[QueryFilter], number: Optional[int]) -> None:
        prefix = f"Clause {number}: " if number is not None else ""
        sides = [item.value for item in filters if item.field == "record_side"]
        if len(sides) > 1 and len(set(sides)) > 1:
            warnings.append(prefix + "Multiple conflicting record_side filters - clause may return no results")
        has_rule = any(item.field in rule_only for item in filters)
        has_rule_side = any(item.field == "record_side" and item.value == "RULE" for item in filters)
        if has_rule and not has_rule_side:
            warnings.append(prefix + "Query uses RULE-only fields but doesn't filter record_side=RULE - consider adding it")
        has_document = any(item.field in document_only for item in filters)
        has_document_side = any(item.field == "record_side" and item.value == "DOCUMENT" for item in filters)
        if has_document and not has_document_side:
            warnings.append(prefix + "Query uses DOCUMENT-only fields but doesn't filter record_side=DOCUMENT - consider adding it")

    if getattr(query, "clauses", None):
        for number, clause in enumerate(query.clauses, start=1):
            warn_clause(clause, number)
    else:
        warn_clause(getattr(query, "filters", []) or [], None)
    return warnings
