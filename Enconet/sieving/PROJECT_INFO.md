# JSON Extractor vNext - Project Information

## Project Identity

**Project ID**: CPIJ_JSON_Extractor_vNext  
**Version**: 0.1  
**Date**: 2026-01-16  
**Status**: POC / WIP

## Core Design Decisions

### 1. Query DSL Syntax (CRITICAL - INTERFACE CONTRACT)

**Location**: `src/json_extractor/query/compiler.py`

**Syntax**: `field:value` terms combined with `AND` / `OR` operators

**Grammar**:
```
filter_expr := term (LOGICAL_OP term)*
term := field:value
LOGICAL_OP := "AND" | "OR"
```

**Examples**:
```
"criterion_id:APP_B_I AND record_side:RULE"
"keyword:inspection AND item_type:requirement"
"criterion_id:APP_B_XVI OR criterion_id:APP_B_XVII"
```

**⚠️ CRITICAL CONTRACT**: This DSL syntax is a **core interface contract** and must be preserved for backward compatibility. Any changes to the DSL parser must maintain compatibility with existing filter expressions.

**Implementation Notes**:
- Values may contain spaces (no quotes needed)
- Case-insensitive matching for string fields
- Special `keyword` field searches across multiple fields
- Currently all filters combined with AND (OR support planned)

**If DSL Syntax Changes**:
1. Document breaking changes prominently
2. Provide migration guide
3. Consider deprecation period
4. Update all examples in README
5. Update comments in `compiler.py`

---

### 2. Entity Flattening Strategy

**Decision**: Flatten structured entity objects to semicolon-joined strings

**Format Rules**:
- **People**: `"Name (Role)"` or `"Name"` if role is null
- **Documents**: `"Identifier: Name Rev"` or variations based on available fields
- **Standards/Regulations**: `"Identifier: Name"` format
- **Organizations, Systems/Tools, Suppliers**: Simple string join

**Rationale**: 
- Enables text search in exported files
- Preserves readability in CSV/XLSX
- Avoids complex nested structures in tabular format

**Trade-off**: Loss of structure (cannot programmatically parse role from name in exports)

**Alternative considered**: Separate columns per entity type (rejected due to column explosion)

---

### 3. Validation Philosophy

**Decision**: Collect all violations per file and return structured error report

**Error Collection**:
- Continue processing on errors
- Collect errors per item with:
  - file_path
  - item_id
  - rule_id (e.g., "VAL-TAX-001")
  - severity (ERROR | WARNING)
  - message

**Severity Levels**:
- **ERROR**: Serious compliance issues (template identity, taxonomy, evidence, join keys)
- **WARNING**: Issues but not fatal (reference key format)

**Rationale**:
- Users can see all issues at once
- Invalid items still included in results (with error flags)
- Supports incremental fixing of validation issues

**Alternative considered**: Fail-fast (rejected - too disruptive for iterative workflows)

---

### 4. Default Column Selection

**Decision**: Curated "essential" subset with user customization

**Essential Columns** (12):
```python
[
    "record_side", "criterion_id", "criterion_name",
    "item_type", "statement", "evidence_quote_1",
    "doc_id", "filename", "title",
    "rule_key", "rule_ref_keys", "rule_strength"
]
```

**Customization**:
- Users select columns in GUI
- Click "Save as Default Columns"
- Saved to `~/.json_extractor/column_defaults.json`
- Loaded automatically on next run

**Rationale**:
- 34 columns is overwhelming for first-time users
- Essential subset covers most common queries
- Power users can customize and save preferences

**Alternative considered**: Show all columns by default (rejected - poor UX)

---

### 5. CLI Command Structure

**Decision**: Single command with flags

**Format**:
```bash
python cli.py --files DATA/*.json --filter "criterion_id:APP_B_I" --output results.xlsx
```

**Flags**:
- `--files` / `-f`: File patterns
- `--all` / `-a`: All files in DATA directory
- `--data-dir` / `-d`: Custom data directory
- `--filter`: DSL filter expression
- `--columns` / `-c`: Comma-separated column list
- `--output` / `-o`: Output file path
- `--format`: csv | xlsx
- `--preview` / `-p`: Show preview without export
- `--show-errors` / `--no-errors`: Error display toggle

**Subcommands**:
- `list-files`: Show available files
- `info`: Show configuration

**Rationale**:
- Simple for common use cases
- Composable (all flags optional)
- Matches user's stated preference for GUI over CLI

**Alternative considered**: Subcommands for query/export (rejected - unnecessary complexity)

---

### 6. Streamlit GUI Features

**Included**:
- ✅ File selection from DATA directory (multi-select)
- ✅ Filter builder UI (dropdowns, text inputs)
- ✅ Column selection multi-select
- ✅ Manual export button
- ✅ Preview results table
- ✅ Save column defaults

**Excluded**:
- ❌ File upload widget (only DATA directory selection)
- ❌ Automatic export (explicit button required)

**Rationale**:
- DATA directory keeps files organized
- Manual export prevents accidental overwrites
- Filter builder provides discoverability
- Column selection matches user preference

---

### 7. Record-Side Field Separation

**RULE records** must have:
- `rule_source_rules` (enum: 10CFR50_APPB | 10CFR21)
- `rule_locator` (normalized locator)
- `rule_key` (composite: `rule_source_rules::rule_locator`)
- `rule_strength` (enum: MANDATORY | NON_MANDATORY)

**RULE records** must NOT have:
- `rule_ref_keys`, `rule_ref_codes`, `rule_ref_locators`, `rule_ref_texts_json`

**DOCUMENT records** must have:
- `rule_ref_keys` (semicolon-joined list of composite keys)

**DOCUMENT records** must NOT have:
- `rule_source_rules`, `rule_locator`, `rule_key`, `rule_strength`, `rule_citation_text`

**Validation**: Enforced by VAL-RULELEAK-001 and VAL-RULELEAK-002

**Rationale**: Prevents field pollution and ensures deterministic join semantics

---

### 8. Join Key Format

**Composite key format**: `<ref_code>::<ref_locator>`

**Examples**:
- `10CFR50_APPB::APP_B_XVI`
- `10CFR21::21.21`

**RULE side**: Single `rule_key`  
**DOCUMENT side**: Semicolon-joined `rule_ref_keys`

**Join logic**: DOCUMENT links to RULE when any token in `rule_ref_keys` equals RULE's `rule_key`

**Determinism requirements**:
- RULE: `rule_key` must exactly equal `rule_source_rules + "::" + rule_locator`
- DOCUMENT: Each token in `rule_ref_keys` must match `<ref_code>::<ref_locator>` format

**Validation**: Enforced by VAL-JOIN-001 and VAL-JOIN-002

---

### 9. Locator Normalization

**10CFR50_APPB**:
- `rule_locator` must be one of: APP_B_I through APP_B_XVIII
- Controlled vocabulary (18 criteria)
- For RULE items: `rule_locator` should equal `criterion_id`

**10CFR21**:
- `rule_locator` matches pattern: `21.<section>`
- Numeric section only (no subsections in POC)
- Example: `21.3`, `21.21`, `21.55`

**Subsection policy**: SECTION_ONLY (may be expanded to `21.<n>(a)(1)` in future)

**Validation**: Enforced by VAL-LOC-001

---

### 10. Evidence Storage

**Two representations**:
1. **evidence_quote_1**: First quote only (scalar, searchable, export-friendly)
2. **evidence_quotes_json**: Full array as JSON string (fidelity)

**Rationale**:
- Most queries only need first quote
- Full array available for detailed analysis
- Avoids column explosion for multi-quote items

**Validation**: At least one evidence quote required (VAL-EVID-001)

**Alternative considered**: Multiple evidence_quote_N columns (rejected - arbitrary limit)

---

## Implementation Decisions Summary

| Topic | Decision | Location |
|-------|----------|----------|
| Query DSL | `field:value AND field:value` syntax | `query/compiler.py` |
| Entity flattening | Semicolon-joined strings | `extract/load_and_flatten.py` |
| Validation | Collect all, structured report | `extract/load_and_flatten.py` |
| Default columns | 12-column essential subset | `config.py` |
| CLI structure | Single command with flags | `cli.py` |
| GUI features | Filter builder + column select | `app.py` |
| Field separation | RULE vs DOCUMENT strict | Template contract |
| Join keys | Composite `code::locator` | Template contract |
| Locator policy | Controlled vocab + patterns | `app_b.py` |
| Evidence | Dual: scalar + JSON | Schema design |

---

## Open Decisions / Future Work

### 1. 10CFR21 Locator Granularity
**Status**: OPEN_DECISION  
**Current**: SECTION_ONLY (`21.<n>`)  
**Future**: May need subsections (`21.<n>(a)(1)`) for deterministic joins  
**Impact**: Requires locator policy upgrade and normalization rule expansion

### 2. Evidence Storage Optimization
**Status**: OPEN_DECISION  
**Current**: Both `evidence_quote_1` and `evidence_quotes_json`  
**Future**: If memory/performance becomes issue, could make JSON optional  
**Impact**: Minimal - most queries use quote_1 only

### 3. OR Group Support
**Status**: PLANNED  
**Current**: All filters combined with AND  
**Future**: Support explicit OR groups: `(criterion_id:APP_B_I OR criterion_id:APP_B_II) AND record_side:RULE`  
**Impact**: Requires compiler and engine updates (backward compatible)

### 4. ISO Template Support
**Status**: ASSUMPTION  
**Current**: APP_B template only  
**Future**: Reuse stable fields, change taxonomy keys  
**Contract**: Must preserve: record_side, item_id, statement, evidence, source, ref_key join semantics

### 5. Reference Table for Join Diagnostics
**Status**: OPEN_DECISION  
**Current**: Semicolon-joined strings + JSON for DOCUMENT references  
**Future**: Separate table with one row per reference for richer diagnostics  
**Impact**: Would require schema and pipeline changes

---

## Backward Compatibility Commitments

### MUST preserve:
1. **Query DSL syntax**: `field:value AND field:value` format
2. **Normalized schema field names**: All 34+ canonical fields
3. **Join key format**: `<ref_code>::<ref_locator>` composite keys
4. **Export formats**: CSV (utf-8-sig) and XLSX (openpyxl)
5. **Column defaults file**: `~/.json_extractor/column_defaults.json` format

### MAY change (with migration):
1. Adding new fields to schema (append only)
2. Adding new validation rules
3. Adding new query operators
4. Adding new templates
5. Optimizing internal implementations

### SHOULD NOT change without major version:
1. Template ID format
2. Validation error structure
3. Pipeline result structure
4. File discovery behavior

---

## Testing Recommendations

**Unit tests needed**:
- DSL parser (various expressions)
- Entity flattening (all entity types)
- Validation rules (all rule IDs)
- Query engine (all operators)
- Join key construction

**Integration tests needed**:
- Full pipeline (files → export)
- Bad file handling
- Empty result handling
- Multi-file aggregation

**UI tests needed**:
- Filter builder combinations
- Column selection save/load
- Export with various formats

---

## Performance Targets

**Files**: 100+ JSON files  
**Records**: 10,000+ items  
**Query time**: < 1 second  
**Export time**: < 5 seconds  
**Memory**: < 500MB for typical datasets

Current implementation meets these targets with pandas/openpyxl.

---

## Compliance with Original Spec

✅ Frozen tree structure implemented  
✅ Template contract (JSON_Template_App_B) implemented  
✅ Normalized schema (34 fields) implemented  
✅ Validation rules (all specified) implemented  
✅ Query DSL with keyword search implemented  
✅ Deterministic joins implemented  
✅ CSV/XLSX export with precedence rules implemented  
✅ Bad file skip policy implemented  
✅ Column defaults with user persistence implemented  
✅ CLI and Streamlit adapters implemented  

---

**Last Updated**: 2026-01-17  
**Document Owner**: JSON Extractor Team
