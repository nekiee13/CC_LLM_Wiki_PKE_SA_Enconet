# ------------------------
# src/json_extractor/query/compiler.py
# ------------------------
"""
Query DSL compiler.

Parses filter expressions in the format:
    "criterion_id:APP_B_I AND record_side:RULE"
    "keyword:test equipment AND item_type:requirement"
    "criterion_id:APP_B_XVI OR criterion_id:APP_B_XVII"

Adds true OR support via an OR-of-AND clause model:
    clauses = [[A, B], [C]]  meaning  (A AND B) OR (C)

Adds compiled IN support for ENUM fields using comma-separated values:
    "criterion_id:APP_B_I,APP_B_II"  -> operator="in", value="APP_B_I,APP_B_II"

CRITICAL: This DSL syntax is a core interface contract and must be preserved
         for backward compatibility. Existing AND-only expressions must remain valid.

Grammar (vNext):
    filter_expr := term (LOGICAL_OP term)*
    term := field ":" value
    LOGICAL_OP := "AND" | "OR"

Special handling:
    - keyword:value searches across multiple fields (engine-defined)
    - Values may contain spaces (tokenization preserves space-containing values)
    - Field typing controls operator selection:
        ENUM   -> equals, or in (if comma-separated)
        STRING -> contains_ci
        NUMBER -> equals
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .schema import QuerySchema, FieldType


@dataclass(frozen=True)
class QueryFilter:
    """
    A single field filter predicate.

    Examples:
        QueryFilter(field="criterion_id", operator="equals", value="APP_B_I")
        QueryFilter(field="criterion_id", operator="in", value="APP_B_I,APP_B_II")
        QueryFilter(field="statement", operator="contains_ci", value="inspection")
        QueryFilter(field="keyword", operator="contains_ci", value="audit")
    """

    field: str
    operator: str  # "equals", "contains_ci", "in", etc.
    value: str

    def __repr__(self) -> str:
        return f"QueryFilter(field={self.field!r}, operator={self.operator!r}, value={self.value!r})"


@dataclass(frozen=True)
class CompiledQuery:
    """
    Compiled query representation.

    - clauses: OR-of-AND structure (authoritative when non-empty)
        clauses = [[A,B],[C]] means (A AND B) OR (C)
    - filters: flattened list of all filters (backward compatible / diagnostics)
    - combination: retained for backward compatibility; non-authoritative once clauses exist
    """

    filters: List[QueryFilter] = field(default_factory=list)
    clauses: List[List[QueryFilter]] = field(default_factory=list)
    combination: str = "AND"


class DSLParseError(Exception):
    """Error parsing filter DSL."""


def tokenize_filter_expression(expr: str) -> List[str]:
    """
    Tokenize filter expression into terms and operators.

    Strategy:
        - Split on whitespace.
        - Treat words "AND"/"OR" (case-insensitive) as operator tokens.
        - Preserve values containing spaces by accumulating words into a term.
        - Start a NEW term when a word looks like "<known_field>:..." or "keyword:..."
          while a term is already being accumulated.

    Example:
        "keyword:test equipment AND item_type:requirement"
          -> ["keyword:test equipment", "AND", "item_type:requirement"]

        "criterion_id:APP_B_I criterion_id:APP_B_II"
          -> ["criterion_id:APP_B_I", "criterion_id:APP_B_II"]  (missing operator detected later)
    """
    tokens: List[str] = []
    current_term: List[str] = []

    # Schema-aware helper: does a word look like a new term start?
    def looks_like_term_start(word: str) -> bool:
        if ":" not in word:
            return False
        candidate_field = word.split(":", 1)[0].strip()
        if not candidate_field:
            return False
        if candidate_field == "keyword":
            return True
        return QuerySchema.get_field(candidate_field) is not None

    words = (expr or "").split()
    i = 0
    while i < len(words):
        word = words[i]
        upper = word.upper()

        if upper in ("AND", "OR"):
            # Flush any current term
            if current_term:
                tokens.append(" ".join(current_term))
                current_term = []
            tokens.append(upper)
            i += 1
            continue

        # If a new term start appears while building a term, flush current term
        if current_term and looks_like_term_start(word):
            tokens.append(" ".join(current_term))
            current_term = [word]
            i += 1
            continue

        current_term.append(word)
        i += 1

    if current_term:
        tokens.append(" ".join(current_term))

    return tokens


def _normalize_in_values(raw_value: str) -> List[str]:
    """
    Normalize comma-separated values for IN operator:
      - Split on ","
      - Strip whitespace around each element
      - Drop empty elements
      - Preserve order as written
    """
    parts = [p.strip() for p in (raw_value or "").split(",")]
    return [p for p in parts if p]


def parse_term(term: str) -> QueryFilter:
    """
    Parse a single filter term "field:value".

    Raises:
        DSLParseError: if malformed or unknown field.
    """
    if ":" not in term:
        raise DSLParseError(f"Term must contain ':' separator: {term}")

    field_part, value_part = term.split(":", 1)
    field_name = field_part.strip()
    value_raw = value_part.strip()

    if not field_name or not value_raw:
        raise DSLParseError(f"Empty field or value in term: {term}")

    # Special handling for keyword (not a real schema field)
    if field_name == "keyword":
        return QueryFilter(field="keyword", operator="contains_ci", value=value_raw)

    # Validate field exists in schema
    field_def = QuerySchema.get_field(field_name)
    if not field_def:
        raise DSLParseError(f"Unknown field: {field_name}")

    # Determine operator based on field type (and optional IN encoding)
    if field_def.field_type == FieldType.ENUM:
        if "," in value_raw:
            values = _normalize_in_values(value_raw)
            if len(values) < 2:
                # Degenerate "in" case; fall back to equals for single value
                if not values:
                    raise DSLParseError(f"Empty value list in term: {term}")
                return QueryFilter(field=field_name, operator="equals", value=values[0])
            return QueryFilter(field=field_name, operator="in", value=",".join(values))
        return QueryFilter(field=field_name, operator="equals", value=value_raw)

    if field_def.field_type == FieldType.STRING:
        # Preserve legacy meaning: treat comma as literal in string search
        return QueryFilter(field=field_name, operator="contains_ci", value=value_raw)

    if field_def.field_type == FieldType.NUMBER:
        # Preserve legacy equals behavior; no auto-IN for numbers in this change set
        return QueryFilter(field=field_name, operator="equals", value=value_raw)

    # Fallback (should not occur with current schema)
    return QueryFilter(field=field_name, operator="equals", value=value_raw)


def parse_filter_dsl(expr: str) -> CompiledQuery:
    """
    Parse filter DSL expression into compiled query.

    OR-of-AND semantics:
        - AND binds tighter than OR.
        - Parsing splits on OR boundaries to create clauses.
        - Each clause is a list of AND-combined terms.

    Examples:
        "A AND B OR C" -> clauses [[A,B],[C]]
        "A OR B AND C" -> clauses [[A],[B,C]]

    Raises:
        DSLParseError: if expression is malformed.
    """
    if not expr or not expr.strip():
        return CompiledQuery(filters=[], clauses=[], combination="AND")

    tokens = tokenize_filter_expression(expr.strip())
    if not tokens:
        return CompiledQuery(filters=[], clauses=[], combination="AND")

    clauses: List[List[QueryFilter]] = []
    current_clause: List[QueryFilter] = []

    # Enforce alternating TERM / OP / TERM / OP ... structure
    expecting_term = True

    for token in tokens:
        if token in ("AND", "OR"):
            if expecting_term:
                raise DSLParseError(f"Unexpected operator '{token}' (missing term)")
            # Operator received; next must be a term
            if token == "OR":
                if not current_clause:
                    raise DSLParseError("Empty clause before OR")
                clauses.append(current_clause)
                current_clause = []
            expecting_term = True
            continue

        # TERM
        if not expecting_term:
            # Two terms without an operator is ambiguous; treat as syntax error
            raise DSLParseError(f"Missing operator between terms near: '{token}'")

        try:
            fobj = parse_term(token)
        except DSLParseError as e:
            raise DSLParseError(f"Error parsing term '{token}': {e}") from e

        current_clause.append(fobj)
        expecting_term = False

    if expecting_term:
        # Expression ended with operator
        raise DSLParseError("Expression cannot end with an operator")

    if current_clause:
        clauses.append(current_clause)

    # Flatten filters for backward compatibility / diagnostics
    flat_filters: List[QueryFilter] = [f for clause in clauses for f in clause]

    # Preserve legacy combination field (non-authoritative when clauses exist)
    return CompiledQuery(filters=flat_filters, clauses=clauses, combination="AND")


def validate_compiled_query(query: CompiledQuery) -> List[str]:
    """
    Validate a compiled query for common issues.

    Returns:
        List of warning messages (empty if no issues).

    Notes:
        - Validation is clause-aware when query.clauses is populated.
        - Compatibility fallback scans query.filters if clauses are absent/empty.
    """
    warnings: List[str] = []

    rule_only_fields = {"rule_source_rules", "rule_locator", "rule_key", "rule_strength"}
    doc_only_fields = {"rule_ref_keys", "rule_ref_codes", "rule_ref_locators"}

    def warn_clause(clause_filters: List[QueryFilter], clause_idx: Optional[int]) -> None:
        prefix = f"Clause {clause_idx}: " if clause_idx is not None else ""

        # Conflicting record_side filters inside the same AND clause
        rs_filters = [f for f in clause_filters if f.field == "record_side"]
        if len(rs_filters) > 1:
            values = [f.value for f in rs_filters]
            if len(set(values)) > 1:
                warnings.append(prefix + "Multiple conflicting record_side filters - clause may return no results")

        has_rule_field = any(f.field in rule_only_fields for f in clause_filters)
        has_rule_side = any(f.field == "record_side" and f.value == "RULE" for f in clause_filters)
        if has_rule_field and not has_rule_side:
            warnings.append(prefix + "Query uses RULE-only fields but doesn't filter record_side=RULE - consider adding it")

        has_doc_field = any(f.field in doc_only_fields for f in clause_filters)
        has_doc_side = any(f.field == "record_side" and f.value == "DOCUMENT" for f in clause_filters)
        if has_doc_field and not has_doc_side:
            warnings.append(prefix + "Query uses DOCUMENT-only fields but doesn't filter record_side=DOCUMENT - consider adding it")

    if getattr(query, "clauses", None):
        for idx, clause in enumerate(query.clauses, start=1):
            warn_clause(clause, idx)
        return warnings

    # Compatibility fallback (legacy compiled form)
    warn_clause(getattr(query, "filters", []) or [], None)
    return warnings
