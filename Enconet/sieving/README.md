# JSON Extractor vNext

## Project integration

The canonical project entry point is `python scripts/query_crumbs.py`. Project
scripts resolve the integral library from `sieving/src` through
`scripts/sieving_lib.py`; no editable install and no second copy of flattening or
validation logic is used. `sieving/cli.py` is retained only as a headless
development/debug adapter and is not a project process dependency.

Use `query --strict` to make missing or unexpected input fields blocking. The
default warning mode reports drift while allowing inspection and export when no
other blocking validation error exists.

A taxonomy-driven extraction and query system for nuclear quality assurance documents.

## Overview

JSON Extractor vNext processes JSON extraction files (from upstream LLM extraction) and provides:

- **Strict Appendix B taxonomy**: 18-criterion classification per 10 CFR Part 50 Appendix B
- **RULE vs DOCUMENT separation**: Explicit segregation of regulatory requirements vs. implementer documents
- **Deterministic join semantics**: Composite key joins (`ref_code::ref_locator`) between RULE and DOCUMENT records
- **DSL-based querying**: Filter expressions for precise slicing of normalized records
- **Flexible export**: CSV/XLSX with stable column ordering
- **Command-line interface**: Typer-based CLI (`cli.py`). The standalone Streamlit GUI
  was retired by owner decision on 2026-07-04 (ADR-0007); the CLI is the only
  supported interface.

## Project Status

**Status**: POC / WIP  
**Version**: 0.1  
**Template**: JSON_Template_App_B v0.1

## Installation

### Prerequisites

- Python 3.10+
- Windows 11 (primary target; should work on other OS)

### Setup

From the project root (`Enconet/sieving`):

```bash
# Install dependencies
pip install -r requirements.txt

# Create the DATA directory if it does not exist
mkdir DATA

# Add JSON extraction files to DATA/
````

## Quick Start

> The former Streamlit GUI (`app.py`) was retired per ADR-0007 (2026-07-04) and must
> not be reintroduced without a superseding ADR. Use the CLI.

### CLI

Commands are implemented as Typer subcommands. Use `query`, `list-files`, and `info`.

```bash
# Query by criterion and export to Excel
python cli.py query --files DATA/*.json --filter "criterion_id:APP_B_I" --output results.xlsx

# Process all files, filter RULE records
python cli.py query --all --filter "record_side:RULE" --output rules.xlsx

# Keyword search with custom columns
python cli.py query --all --filter "keyword:inspection" --columns "item_id,statement,criterion_name" --output inspection.csv

# Preview results without exporting
python cli.py query --files DATA/doc1.json --filter "item_type:requirement" --preview
```

#### Fail-closed filtering (C4.1)

An invalid filter fails closed: the CLI prints the filter error, exits with code `2`,
and writes no output file. For development-only inspection, combine
`--allow-unfiltered-preview` with `--preview` to display unfiltered rows behind a
visible override notice; export remains blocked while the filter error is set.

```bash
# Development only: preview unfiltered rows after a filter error (export stays blocked)
python cli.py query --all --filter "criterion_id OR" --allow-unfiltered-preview --preview
```

### List available files

```bash
python cli.py list-files
```

### Show configuration

```bash
python cli.py info
```

## Architecture

### Directory Structure

```
PROJECT_ROOT/
  cli.py                    # CLI adapter (Typer); sole adapter since ADR-0007
  requirements.txt          # Python dependencies
  README.md                 # This file
  QUICKSTART.md             # Quick start guide
  DATA/                     # JSON extraction files (created by user)
  src/
    json_extractor/
      __init__.py
      config.py              # Configuration and preferences
      pipeline.py            # Main orchestration
      io/
        __init__.py
        files.py             # File discovery and reading
        export.py            # CSV/XLSX export
      extract/
        __init__.py
        load_and_flatten.py  # JSON → normalized records
      templates/
        __init__.py
        app_b.py             # Appendix B template definition
      query/
        __init__.py
        schema.py            # Queryable field definitions
        compiler.py          # DSL parser (OR + IN compilation)
        engine.py            # Query execution (OR-of-AND)
```

### Data Flow

```
JSON Files → Read → Flatten → Validate → Query → Export
                                    ↓
                            DataFrame (pandas)
```

1. **File Discovery**: Discover JSON files in the DATA directory
2. **Reading**: Parse JSON with error handling
3. **Flattening**: Transform nested JSON items into flat records
4. **Validation**: Check template compliance and collect diagnostics
5. **Querying**: Apply DSL filters (OR-of-AND semantics)
6. **Export**: Write CSV/XLSX with stable column order

## Filter DSL Syntax

**CRITICAL**: This DSL syntax is a core interface contract and must be preserved for backward compatibility.

### Grammar

```
filter_expr := term (LOGICAL_OP term)*
term := field:value
LOGICAL_OP := "AND" | "OR"
```

### Operators and precedence

* Supported operators: `AND`, `OR`
* Precedence: `AND` binds tighter than `OR`

  * Example: `A OR B AND C` is evaluated as `A OR (B AND C)`
* Parentheses are not supported.

### Field matching rules

* **ENUM fields** (e.g., `criterion_id`, `item_type`, `record_side`)

  * Default operator: exact match (`equals`)
  * Multi-value operator: comma-separated list compiled as `IN` (set membership)

    * Example: `criterion_id:APP_B_I,APP_B_II`
* **STRING fields** (e.g., `filename`, `title`, `statement`)

  * Case-insensitive substring match (`contains_ci`)
  * Commas are treated as literal characters (no automatic IN)
* **keyword:...**

  * Case-insensitive substring match across a fixed, engine-defined set of fields

### Examples

```bash
# Single field (ENUM equals)
"criterion_id:APP_B_I"

# Multiple fields (AND)
"criterion_id:APP_B_I AND record_side:RULE"

# OR union (OR-of-AND clauses)
"criterion_id:APP_B_I OR criterion_id:APP_B_II"

# AND precedence over OR (A OR (B AND C))
"criterion_id:APP_B_I OR record_side:RULE AND rule_source_rules:10CFR21"

# Keyword search (contains_ci across engine-defined fields)
"keyword:inspection AND item_type:requirement"

# RULE-specific
"record_side:RULE AND rule_strength:MANDATORY"

# ENUM multi-select using compiled IN (comma-separated values)
"criterion_id:APP_B_XVI,APP_B_XVII"
"item_type:control,reference"

# Complex example (STRING contains_ci; commas are literal for STRING fields)
"criterion_id:APP_B_XVI AND keyword:corrective action"
```

## Queryable Fields

### Core Fields

* `record_side`: RULE | DOCUMENT
* `criterion_id`: APP_B_I through APP_B_XVIII
* `criterion_name`: Organization, Quality Assurance Program, etc.
* `item_type`: requirement, process_step, etc.
* `doc_id`, `filename`, `title`, `revision`
* `statement`: Extracted text
* `keyword`: Special field that searches across multiple fields

### RULE-only Fields

* `rule_source_rules`: 10CFR50_APPB | 10CFR21
* `rule_locator`: Locator within rule source
* `rule_key`: Composite join key
* `rule_strength`: MANDATORY | NON_MANDATORY

### DOCUMENT-only Fields

* `rule_ref_keys`: Semicolon-joined reference keys
* `rule_ref_codes`: Referenced rule codes
* `rule_ref_locators`: Referenced rule locators

## Normalized Record Schema

Every extracted item becomes a flat record with 34+ fields.

### Identity and taxonomy

* `template_id`, `template_version`, `taxonomy_id`
* `record_side`, `criterion_id`, `criterion_name`
* `item_type`, `item_id`

### Content

* `statement`: Main extracted text
* `evidence_quote_1`: First evidence quote (for convenience)
* `evidence_quotes_json`: Full evidence array (JSON)

### Provenance

* `doc_id`, `filename`, `title`, `revision`
* `source_page`, `source_page_label`, `source_heading_path`
* `source_section_id`, `source_block_type`, `source_location_cue`

### Entities (flattened)

* `entities_organizations`
* `entities_people`: "Name (Role)" format
* `entities_documents`: "Identifier: Name Rev" format
* `entities_systems_tools`
* `entities_standards_regulations`: "Identifier: Name" format

### RULE fields

* `rule_source_rules`, `rule_locator`, `rule_key`
* `rule_strength`, `rule_citation_text`

### DOCUMENT fields

* `rule_ref_keys`, `rule_ref_codes`, `rule_ref_locators`
* `rule_ref_texts_json`

## Join Semantics

Deterministic joins between RULE and DOCUMENT records.

### RULE side

```
rule_key = "10CFR50_APPB::APP_B_XVI"
         = rule_source_rules + "::" + rule_locator
```

### DOCUMENT side

```
rule_ref_keys = "10CFR50_APPB::APP_B_IV; 10CFR50_APPB::APP_B_XVI"
              = semicolon-joined list of ref_code::ref_locator
```

Join rule: a DOCUMENT record links to a RULE record when any token in `rule_ref_keys` equals the RULE record's `rule_key`.

## Validation Rules

The pipeline validates all items and collects errors and warnings.

### ERROR-level (must pass)

* Template identity consistency
* Criterion ID in canonical 18-criterion table
* Criterion name matches criterion ID
* Evidence presence
* Provenance presence
* RULE/DOCUMENT field separation
* Join key determinism

### WARNING-level (issues but not fatal)

* DOCUMENT reference key format

Run results include structured error reports with:

* File path
* Item ID
* Validation rule ID
* Severity
* Message

## Column Selection and Defaults

### Default Columns

The system includes a curated "essential" subset:

```python
DEFAULT_COLUMNS = [
    "record_side", "criterion_id", "criterion_name",
    "item_type", "statement", "evidence_quote_1",
    "doc_id", "filename", "title",
    "rule_key", "rule_ref_keys", "rule_strength"
]
```

### Custom Defaults

* **Location**: Saved to `~/.json_extractor/column_defaults.json`
* **CLI**: Uses saved defaults automatically; override with `--columns`.
* The former GUI "Save current selection" flow was retired with the GUI (ADR-0007);
  edit the JSON file directly to change persisted defaults.

## Configuration

### Data Directory

Default: `./DATA`

Override:

* CLI: `--data-dir PATH`
* Code: `Config(data_dir=Path("custom/path"))`

### Config Directory

Default: `~/.json_extractor`

Contains:

* `column_defaults.json`: saved column preferences

## Template Contract

Current template: **JSON_Template_App_B v0.1**

* Taxonomy: APP_B (18 criteria from 10 CFR Part 50 Appendix B)

Canonical rule codes:

* `10CFR50_APPB`: Appendix B (locators = APP_B_I through APP_B_XVIII)
* `10CFR21`: Part 21 (locators = 21.<section>)

Future ISO templates are expected to reuse stable fields while changing taxonomy keys.

## Error Handling

### Bad Files

Files that cannot be processed are reported with:

* Path
* Reason (OS error, JSON decode error, invalid root)
* Error type

Policy: bad files are skipped and processing continues on valid files.

### Validation Errors

Items with validation errors are included in results but flagged with structured error reports.

Severity levels:

* ERROR: serious compliance issues
* WARNING: issues but not fatal

### Filter Errors (C4.1 — fail closed)

If the filter DSL is invalid:

* The pipeline fails closed: the filtered result is empty and
  `PipelineResult.filter_error` is populated.
* Export is blocked while `filter_error` is set, in both the API and the CLI.
* The CLI exits with code `2` and creates no output file.
* Development only: `--allow-unfiltered-preview` together with `--preview` shows
  unfiltered rows behind a visible override notice; export remains blocked.

### Empty Results

If all files are bad or yield zero items, the pipeline returns an empty DataFrame plus diagnostics.

## Export Formats

### CSV

* Encoding: UTF-8 with BOM (`utf-8-sig`)
* No index column
* Stable column order

### XLSX

* Engine: openpyxl
* Sheet name: `RESULT`
* No index column
* Stable column order

### Format Precedence

1. If output path ends with `.csv` → CSV
2. Else if `--format csv` → CSV
3. Otherwise → XLSX (extension enforced to `.xlsx`)

## Performance Considerations

* Memory: all records loaded into a pandas DataFrame
* File count: tested with dozens of files; hundreds should work
* Record count: pandas handles 100K+ rows efficiently
* Validation: O(n) per item; collected and non-blocking

## Future Enhancements

Planned:

* Parentheses and nested boolean expressions in DSL
* 10CFR21 subsection locator normalization (consistent `21.<section>` handling)
* ISO template support
* Reference table for richer join diagnostics

Out of scope:

* Upstream Markdown → JSON extraction (separate LLM process)
* Document parsing from raw PDF/Word
* Network services, databases
* Multi-user access control

## Troubleshooting

### No files found

* Check DATA directory exists
* Check files have `.json` extension
* Use `python cli.py list-files` to verify

### Validation errors

* Review error summary in output
* Check JSON files match JSON_Template_App_B schema
* Validate criterion_id values against canonical 18 criteria

### Empty results after filter

* Try without filter to see all records
* Use `--preview` to inspect results
* Check filter syntax (`field:value`)

### Column not found

* Use `python cli.py info` to see available columns
* Check spelling and case sensitivity
* Ensure the column exists in the normalized schema

## Contributing

This is a POC/WIP project. Key extension points:

1. New templates: add to `src/json_extractor/templates/`
2. Query operators: extend `query/engine.py`
3. Validation rules: add to `extract/load_and_flatten.py`
4. DSL syntax: modify `query/compiler.py` (preserve backward compatibility)

## License

MIT

## Contact

[Your contact info here]
