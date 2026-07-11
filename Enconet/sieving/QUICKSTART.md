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

## 3. Run the GUI (Streamlit)

```bash
streamlit run app.py
```

Then:

1. Select one or more JSON files in the sidebar
2. Start with a simple filter such as: `criterion_id:APP_B_XVI`
3. Click **Run query**
4. Review results and export if needed

Notes:

* The Streamlit filter builder emits:

  * `OR` when explicitly typed in the DSL input
  * `IN` for ENUM multi-select fields as comma-joined values (example: `criterion_id:APP_B_I,APP_B_II`)
* If a filter is invalid, an explicit filter error is shown in the UI (E4-T2).

## 4. Run the CLI

Commands are implemented as Typer subcommands. Use `query`, `list-files`, and `info`.

```bash
# Query all discovered files for Corrective Action items (preview)
python cli.py query --all --filter "criterion_id:APP_B_XVI" --preview

# Export to Excel
python cli.py query --all --filter "criterion_id:APP_B_XVI" --output corrective_action.xlsx
```

### Strict filter mode (E4-T2)

By default, an invalid filter returns unfiltered results and surfaces a `filter_error`.
To fail fast in scripts, add `--strict-filter` to exit with code `2` when the filter is invalid.

```bash
python cli.py query --all --filter "criterion_id OR" --strict-filter --preview
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

### GUI Method

1. Run `streamlit run app.py`
2. Select columns in the sidebar
3. Click **Save current selection**

### CLI Method

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

* Invalid DSL now surfaces as a filter error (E4-T2)
* CLI automation: add `--strict-filter` to fail fast (exit code `2`)

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

1. Explore the GUI: `streamlit run app.py`
2. Read the full README: `README.md`
3. Use OR and IN filters:

   * `OR` unions clauses
   * comma lists create `IN` for ENUM fields
4. Customize columns and save defaults
5. Add repository data under `DATA/`
