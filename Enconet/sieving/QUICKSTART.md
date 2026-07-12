# Quick Start Guide

Get up and running with JSON Extractor vNext in 5 minutes.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
````

## 2. Verify Input Files

Valid extraction JSON files must be placed under `DATA/`. Recommended layout:

* `DATA/DOCUMENT/` for DOCUMENT-side extractions
* `DATA/RULE/` for RULE-side extractions

Files must follow the active template contract (currently JSON_Template_App_B). If the repository includes example files, they should already be under `DATA/`.

## 3. Interface

The CLI (`cli.py`) is the only supported interface. The former Streamlit GUI
(`app.py`) was retired by owner decision on 2026-07-04 (ADR-0007) and must not be
reintroduced without a superseding ADR.

## 4. Run the CLI

Commands are implemented as Typer subcommands. Use `query`, `list-files`, and `info`.

```bash
# Query all discovered files for Corrective Action items (preview)
python cli.py query --all --filter "criterion_id:APP_B_XVI" --preview

# Export to Excel
python cli.py query --all --filter "criterion_id:APP_B_XVI" --output corrective_action.xlsx
```

### Fail-closed filtering (C4.1)

An invalid filter fails closed: the CLI prints the filter error, exits with code `2`,
and writes no output file. Development only: combine `--allow-unfiltered-preview` with
`--preview` to inspect unfiltered rows; export remains blocked.

```bash
python cli.py query --all --filter "criterion_id OR" --allow-unfiltered-preview --preview
```

## 5. Filter DSL Quick Reference

Filters are composed of `field:value` terms combined with `AND` and `OR`.

### Operators and precedence

* Supported operators: `AND`, `OR`
* Precedence: `AND` binds tighter than `OR`

  * Example: `A OR B AND C` is evaluated as `A OR (B AND C)`
* Parentheses are not supported.

### Multi-select for ENUM fields (compiled IN)

Comma-separated values on ENUM fields are compiled to an `IN` operator:

* `criterion_id:APP_B_I,APP_B_II`
* `item_type:control,reference`

Notes:

* `IN` applies automatically for ENUM fields only.
* Commas in STRING fields are treated as literal characters.

## 6. Common Queries

### Get all RULE records

```bash
python cli.py query --all --filter "record_side:RULE" --output rules.xlsx
```

### Get all DOCUMENT records

```bash
python cli.py query --all --filter "record_side:DOCUMENT" --output documents.xlsx
```

### Search for keyword "quality"

```bash
python cli.py query --all --filter "keyword:quality" --output quality_items.xlsx
```

### Get mandatory rules only

```bash
python cli.py query --all --filter "record_side:RULE AND rule_strength:MANDATORY" --output mandatory_rules.xlsx
```

### Combine filters (AND)

```bash
python cli.py query --all --filter "criterion_id:APP_B_XVI AND record_side:DOCUMENT" --output doc_corrective_action.xlsx
```

### OR union (OR-of-AND clauses)

```bash
python cli.py query --all --filter "criterion_id:APP_B_I OR criterion_id:APP_B_II" --output org_or_qap.xlsx
```

### AND precedence over OR (A OR (B AND C))

```bash
python cli.py query --all --filter "criterion_id:APP_B_I OR record_side:RULE AND rule_source_rules:10CFR21" --preview
```

### ENUM multi-select using compiled IN (comma-separated values)

```bash
python cli.py query --all --filter "criterion_id:APP_B_XVI,APP_B_XVII" --preview
python cli.py query --all --filter "item_type:control,reference" --preview
```

## 7. List Available Files

```bash
python cli.py list-files
```

## 8. View Configuration

```bash
python cli.py info
```

## 9. Add Your Own Files

1. Place JSON extraction files under `DATA/` (subfolders are supported)
2. Files must follow JSON_Template_App_B format
3. Run queries as above

## 10. Customize Columns

Pass `--columns` explicitly (the former GUI save-selection flow was retired with the
GUI, ADR-0007; persisted defaults live in `~/.json_extractor/column_defaults.json`):

```bash
python cli.py query --all --columns "item_id,statement,criterion_name,evidence_quote_1" --output custom.xlsx
```

## 11. Understanding Results

### Key Columns

* **record_side**: RULE (regulation) or DOCUMENT (procedure/manual)
* **criterion_id**: One of 18 Appendix B criteria (APP_B_I through APP_B_XVIII)
* **criterion_name**: Human-readable criterion name
* **statement**: Extracted requirement/process/control text
* **evidence_quote_1**: First supporting quote from source
* **rule_key**: Join key for RULE records
* **rule_ref_keys**: Join keys for DOCUMENT records (links to RULEs)

### Record Types

* **RULE records**: Regulatory requirements from 10 CFR / other rule sources
* **DOCUMENT records**: Implementing procedures/manuals and supporting documents

### Joining RULEs and DOCUMENTs

DOCUMENT records link to RULE records via `rule_ref_keys` matching `rule_key`:

* RULE: `rule_key = "10CFR50_APPB::APP_B_XVI"`
* DOCUMENT: `rule_ref_keys = "10CFR50_APPB::APP_B_XVI; 10CFR50_APPB::APP_B_VI"`

## Need Help?

* Full documentation: `README.md`
* Implementation details: `PROJECT_INFO.md`
* Filter syntax: README.md section “Filter DSL Syntax”

## Common Issues

### "No JSON files found"

* Check `DATA/` directory exists
* Check files have `.json` extension
* Run `python cli.py list-files` to verify

### "Filter error"

* Invalid DSL fails closed (C4.1): the CLI exits with code `2` and writes no output
* Development only: `--allow-unfiltered-preview` with `--preview` shows unfiltered rows; export stays blocked

### "Validation errors"

* Check JSON files match template format
* Validation errors are collected and shown in output

### "Empty results after filter"

* Try without filter first: `python cli.py query --all --preview`
* Check filter syntax: `field:value AND field:value`
* Verify field names are correct

### "Column not found"

* Run `python cli.py info` to see available columns
* Check spelling and case sensitivity

## Next Steps

1. Read the full README: `README.md`
2. Use OR and IN filters:

   * `OR` unions clauses
   * comma lists create `IN` for ENUM fields
3. Customize columns with `--columns`
4. Add repository data under `DATA/`
