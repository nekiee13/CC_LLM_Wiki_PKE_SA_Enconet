# Crumbs processing - JSON Extractor Project Session Export

**Export date:** 2026-06-23  
**Session topic:** JSON Extractor project documentation, requirements, architecture, and APP_B transformation prompts

---

## 1. User Instruction Style

The requested response style for this session was:

- Strictly objective narrative.
- Third-person perspective only.
- Avoidance of personal pronouns such as “I”, “me”, “you”, and “your”.
- Focus on objects rather than people.
- Passive voice where appropriate.
- Beginner-friendly readability.
- Multi-step processing without interaction unless action by the user is required.
- If user action is required, a single-step instruction should be provided, then confirmation should be awaited.

---

## 2. Provided Project Context

The session included the following source documents and prompt materials:

1. `README.md`
2. `Manual.md`
3. `Software_requirement_specification.md`
4. `Arhitectural_and_functional_analysis.md`
5. Initial transformation prompt for RULES documents
6. Initial transformation prompt for DOCUMENT documents

---

# 3. README.md Summary

## 3.1 Project Identity

- **Project name:** JSON Extractor
- **Date:** 2026-01-16
- **Version:** 0.1

## 3.2 Purpose

A local toolset is provided for extracting structured tables from JSON extraction files stored in `./DATA`. The output can be exported to CSV or Excel XLSX.

Two user interfaces are included:

- A command-line interface for repeatable batch work.
- A Streamlit web app for interactive filtering, preview, and download.

## 3.3 Input JSON Concept

Each input file is expected to be a JSON object with a structure similar to:

- `document`
- `topics`
  - `topic_name`
  - `items`
    - `item_id`
    - `item_type`
    - `statement`
    - `confidence`
    - `source`
    - `evidence_quotes`
    - `entities`

Missing fields are handled defensively. Invalid JSON files can be skipped.

## 3.4 Flattening Concept

Nested topic and item data is flattened into one table row per item. Each row contains:

- Document metadata.
- Topic name and item fields.
- Primary source fields.
- Compact entity references joined with `; `.

## 3.5 Filtering Concept

Filters are supported for:

- `topic`
- `item_type`
- `doc_id`
- `keyword`

The keyword filter searches across:

- `statement`
- `evidence_quote_1`
- `ref_docs`
- `ref_standards`
- `ref_tools`

## 3.6 Project Layout

```text
F:\xPy\Json
DATA\                         # input JSON files (*.json)
cli.py                        # Typer + Rich CLI front-end
app.py                        # Streamlit front-end
json_tool
__init__.py
core.py                       # shared core library
Read_Json.py                  # legacy script
```

## 3.7 Interfaces

### CLI

The CLI supports file selection, filtering, column selection, and export.

Examples:

```bat
python cli.py list
python cli.py run --files 02.json --files 03.json --out out.xlsx --format xlsx
python cli.py run --glob "02*.json" --out out.csv --format csv
python cli.py run --all --out results.xlsx --format xlsx
python cli.py run --all --topic "Procurement" --item-type "requirement" --out out.xlsx
python cli.py run --all --fields doc_id,item_type,statement --out out.csv --format csv
```

### Streamlit App

The app supports:

- Multi-file selection.
- Filters.
- Column picking.
- Preview.
- Download.

Launch command:

```bat
streamlit run app.py
```

## 3.8 Output Formats

- CSV uses UTF-8 with BOM: `utf-8-sig`.
- XLSX uses `openpyxl` and writes a sheet named `RESULT`.

## 3.9 Supported Platforms

- Primary target: Windows 11 with Conda.
- Core code is cross-platform.
- CLI `--open` feature is Windows-only.

---

# 4. Manual.md Summary

## 4.1 Audience

The manual targets users who need to:

- Install dependencies.
- Configure the environment.
- Run the CLI or Streamlit app.
- Diagnose common failures.

## 4.2 Supported Environment

- Windows 11
- Conda
- Python 3.10
- VS Code optional

## 4.3 Conda Environment

A prefix-based Conda environment is stored at:

```text
F:\vEnv\Json
```

Setup commands:

```bat
conda create --prefix F:\vEnv\Json python=3.10 -y
conda activate F:\vEnv\Json
python --version
python -m pip install --upgrade pip
```

## 4.4 Dependencies

Recommended installation uses conda-forge:

```bat
conda install -y -c conda-forge pandas openpyxl rich typer streamlit
```

Optional checks:

```bat
pip install pipdeptree
pipdeptree --warn silence
pip check
```

## 4.5 Required Project Folder Objects

The project root should contain:

- `cli.py`
- `app.py`
- `json_tool\core.py`
- `DATA\`

## 4.6 DATA Directory

- Input JSON files must be placed in `./DATA/`.
- Files must use `.json` extension.
- Files are read with `utf-8-sig`.

## 4.7 Output Paths

- Default output is `results.xlsx`.
- CSV output is produced when `--format csv` is used or the output path ends in `.csv`.

## 4.8 CLI Usage

Common commands:

```bat
cd /d F:\xPy\Json
python cli.py list
python cli.py run --all --out results.xlsx --format xlsx
python cli.py run --files 02.json --files 03.json --out out.xlsx --format xlsx
python cli.py run --glob "02*.json" --out out.csv --format csv
```

Filter examples:

```bat
python cli.py run --all --topic "Corrective actions" --out ca.xlsx --format xlsx
python cli.py run --all --item-type "requirement" --out req.xlsx --format xlsx
python cli.py run --all --keyword "PP-85-01" --out mentions.xlsx --format xlsx
python cli.py run --all --doc-id "DOC-001" --out doc001.xlsx --format xlsx
```

Column selection examples:

```bat
python cli.py run --all --fields doc_id,item_type,statement --out out.csv --format csv
python cli.py run --all --fields doc_id --fields item_type --fields statement --out out.xlsx --format xlsx
python cli.py run --all --fields ALL --out out.xlsx --format xlsx
```

## 4.9 Streamlit Usage

Launch command:

```bat
cd /d F:\xPy\Json
conda activate F:\vEnv\Json
streamlit run app.py
```

In-app workflow:

1. Select JSON files.
2. Fill filters.
3. Select all fields or picked fields.
4. Review preview table.
5. Download CSV or XLSX.

## 4.10 Troubleshooting Areas

Covered areas include:

- Conda activation failures.
- Slow or failed package installation.
- Streamlit command not found.
- No JSON files found.
- Invalid JSON.
- Excel export failures.
- Unicode CSV display issues.
- VS Code `code` command not found.

---

# 5. Software Requirements Specification Summary

## 5.1 Purpose

The SRS defines functional and non-functional requirements for a local JSON extraction toolset. The toolset converts JSON extraction files into tabular CSV/XLSX outputs with filtering and column selection.

## 5.2 Scope

The system shall:

- Discover JSON files in `DATA/`.
- Load and flatten nested JSON content.
- Filter the table.
- Export to CSV or XLSX.
- Provide CLI and Streamlit interfaces.

The system shall not:

- Modify input JSON files.
- Require network connectivity.
- Provide authentication or multi-user access control.

## 5.3 Definitions

- **Project root:** Folder containing `cli.py`, `app.py`, `json_tool/`, and `DATA/`.
- **Flattening:** Converting nested JSON topics and items into one row per item.
- **Primary source:** First element in an item’s `source` list.
- **Keyword filter:** Case-insensitive substring match across multiple text columns.

## 5.4 Functional Requirements Groups

### File Discovery

- List `.json` files in `DATA/`.
- Display file list with file sizes.
- Support exact file names and wildcard patterns.

### JSON Loading and Validation

- Open JSON files using `utf-8-sig`.
- Skip bad files when configured.
- Report skipped files with reasons.

### Flattening

- Produce one row per `topic.items[]` entry.
- Include document metadata.
- Include item fields.
- Include primary source fields.
- Include first evidence quote.
- Normalize entity lists into semicolon-separated text.

### Filtering

- Filter by `topic_name`.
- Filter by `item_type`.
- Filter by `doc_id`.
- Filter by keyword across statement, evidence, and entity reference columns.
- Combine filters by intersection.

### Column Selection

- Keep all columns.
- Select a subset of columns.
- Warn or produce clear behavior for missing requested columns.

### Export

- Export to CSV.
- Encode CSV as `utf-8-sig`.
- Export XLSX using `openpyxl`.
- Use worksheet name `RESULT`.
- Streamlit download should match displayed rows and columns.

### Progress and Feedback

- CLI should display progress.
- CLI should display record counts before and after filtering.

## 5.5 Non-Functional Requirements Groups

- Reliability.
- Performance.
- Usability.
- Maintainability.
- Portability.
- Security and privacy.

## 5.6 Acceptance Criteria

Examples include:

- `python cli.py list` shows JSON file names when valid files exist.
- Runs with valid and invalid JSON files complete when skip mode is enabled.
- Keyword filters export only matching rows.
- Streamlit column-pick downloads contain only selected columns.

---

# 6. Architectural and Functional Analysis Summary

## 6.1 Scope

The analysis describes current architecture, runtime behavior, risks, invariants, and consolidation points.

## 6.2 Primary Components

- **Core library:** `json_tool/core.py`
- **CLI front-end:** `cli.py`
- **UI front-end:** `app.py`
- **Legacy script:** `Read_Json.py`

## 6.3 Layering

The architecture has these layers:

- Presentation layer.
- Domain layer.
- Data processing layer.
- Export layer.

## 6.4 CLI Data Flow

The CLI run flow:

1. Resolve project root.
2. Validate `DATA/`.
3. Discover candidate JSON files.
4. Compute selected file set.
5. Load files iteratively.
6. Collect skipped files.
7. Concatenate extracted frames.
8. Apply filters.
9. Reduce fields.
10. Export output.
11. Optionally auto-open output on Windows.

## 6.5 Streamlit Data Flow

The Streamlit flow:

1. Treat current directory as project root.
2. Validate `DATA/`.
3. List files.
4. Build selected paths.
5. Load selected files.
6. Apply filters.
7. Derive column names.
8. Apply column selection.
9. Show preview.
10. Generate CSV and XLSX downloads.

## 6.6 Flattened Schema

Expected columns:

- `doc_id`
- `filename`
- `title`
- `revision`
- `topic_name`
- `item_id`
- `item_type`
- `statement`
- `confidence`
- `page`
- `page_label`
- `section_id`
- `heading_path`
- `block_type`
- `location_cue`
- `evidence_quote_1`
- `ref_docs`
- `ref_standards`
- `ref_tools`

## 6.7 Key Invariants

- One row is produced per item.
- `heading_path` is produced as a string with ` > ` separators.
- Entity lists tolerate strings and dictionaries.

## 6.8 Filtering Behavior

- Required columns are created if missing.
- Matching is case-insensitive.
- Matching is NaN-safe.
- Active filters are combined as intersection logic.

## 6.9 Observed Risks

### Duplicate Implementation

`Read_Json.py` re-implements flattening and filtering. Drift risk is present.

### Private pandas API

The CLI uses `df._append`, which is a private API. `pd.concat(dfs, ignore_index=True)` is recommended.

### Format and Suffix Precedence

A `.csv` suffix can cause CSV output even when `fmt` is set to `xlsx`. This should be documented or validated.

### Schema Drift Masking

Automatic missing-column creation prevents crashes but may hide upstream schema changes.

## 6.10 Recommended Refactor Plan

1. Consolidate extraction code in `json_tool/core.py`.
2. Replace private pandas calls.
3. Clarify format precedence.
4. Add schema drift visibility.
5. Normalize CLI file-selection examples.

---

# 7. APP_B Transformation Prompt Summary

## 7.1 Purpose

Two prompt variants were provided for extracting content relevant to the APP_B taxonomy:

- RULE documents.
- DOCUMENT documents.

The target taxonomy is:

```text
10 CFR 50 Appendix B – 18 criteria
```

The output must conform to:

```text
JSON_Template_App_B
```

Version:

```text
0.1
```

## 7.2 Output Contract

The transformation prompt requires:

- Valid JSON only.
- Exactly one JSON object.
- No markdown.
- No commentary.
- No explanations outside JSON.
- Top-level `document` and `items` objects.

## 7.3 Run Context

The prompt uses:

- `DOCUMENT_SIDE`
- `SOURCE_RULES`

Allowed `DOCUMENT_SIDE` values:

- `RULE`
- `DOCUMENT`

If `DOCUMENT_SIDE` is `RULE`, `SOURCE_RULES` is required and must be:

- `10CFR50_APPB`
- `10CFR21`

If `DOCUMENT_SIDE` is `DOCUMENT`, `SOURCE_RULES` must be omitted or null.

## 7.4 APP_B Taxonomy

Each item must be assigned to exactly one of the following criteria:

| Criterion ID | Criterion Name |
|---|---|
| `APP_B_I` | Organization |
| `APP_B_II` | Quality Assurance Program |
| `APP_B_III` | Design Control |
| `APP_B_IV` | Procurement Document Control |
| `APP_B_V` | Instructions, Procedures, and Drawings |
| `APP_B_VI` | Document Control |
| `APP_B_VII` | Control of Purchased Material, Equipment, and Services |
| `APP_B_VIII` | Identification and Control of Materials, Parts, and Components |
| `APP_B_IX` | Control of Special Processes |
| `APP_B_X` | Inspection |
| `APP_B_XI` | Test Control |
| `APP_B_XII` | Control of Measuring and Test Equipment |
| `APP_B_XIII` | Handling, Storage, and Shipping |
| `APP_B_XIV` | Inspection, Test, and Operating Status |
| `APP_B_XV` | Nonconforming Materials, Parts, or Components |
| `APP_B_XVI` | Corrective Action |
| `APP_B_XVII` | Quality Assurance Records |
| `APP_B_XVIII` | Audits |

## 7.5 Item-Level Fields

Each extracted item must include:

- `item_id`
- `record_side`
- `template_id`
- `template_version`
- `taxonomy_id`
- `criterion_id`
- `criterion_name`
- `item_type`
- `statement`
- `evidence_quotes`
- `source`

Fixed values:

```json
{
  "template_id": "JSON_Template_App_B",
  "template_version": "0.1",
  "taxonomy_id": "APP_B"
}
```

Allowed `item_type` values:

- `requirement`
- `process_step`
- `role_responsibility`
- `definition`
- `control`
- `record`
- `reference`
- `finding`
- `recommendation`
- `action`
- `status_statement`
- `other`

## 7.6 Provenance

Each item must include a non-empty `source` list.

Each source object should include:

- `page`
- `page_label`
- `heading_path`
- `section_id`
- `block_type`
- `location_cue`

Allowed `block_type` examples:

- `heading`
- `prose`
- `table`
- `diagram`
- `list`
- `figure`
- `footer`
- `header`
- `annex`
- `other`

## 7.7 RULE Semantics

For RULE input:

- `record_side` must be `RULE`.
- A `rule` object is expected.
- `rule_reference_ids` and `rule_references` must be absent or empty.

The `rule` object should include:

- `source_rules`
- `rule_strength`
- `rule_locator`
- `rule_key`
- `rule_citation_text`

The `rule_key` must equal:

```text
<source_rules>::<rule_locator>
```

## 7.8 DOCUMENT Semantics

For DOCUMENT input:

- `record_side` must be `DOCUMENT`.
- `item.rule` must be absent or null.
- Embedded regulatory references may be captured through `rule_reference_ids`.

Preferred reference format:

```text
<ref_code>::<ref_locator>
```

## 7.9 Document Metadata

Repo-consumed fields:

- `document.doc_id`
- `document.filename`
- `document.title`
- `document.control_metadata.revision`

## 7.10 Entities

The pipeline flattens only item-level entities:

- `items[].entities.organizations`
- `items[].entities.people`
- `items[].entities.documents`
- `items[].entities.systems_tools`
- `items[].entities.standards_regulations`

Root-level entities may appear but are ignored by the current pipeline.

## 7.11 Observed Prompt Issue

The DOCUMENT prompt runtime block contains malformed placeholder text:

```text
DOCUMENT_SIDE:
"DOCUMENT&gt;"

SOURCE_RULES:
"&lt;10CFR50_APPB&gt;"
```

For DOCUMENT runs, the cleaner form should be:

```text
DOCUMENT_SIDE:
"DOCUMENT"

SOURCE_RULES:
null
```

---

# 8. Detailed Project Summary Produced During Session

## 8.1 Project Identity

JSON Extractor is a local Python-based toolset for extracting structured tabular data from JSON extraction files. The project converts nested JSON content into flat tables that can be filtered, previewed, and exported to CSV or Excel XLSX.

The project is documented as:

- **Project name:** JSON Extractor
- **Version:** 0.1
- **Main date across documents:** 2026-01-16
- **Primary platform:** Windows 11
- **Recommended environment:** Conda with Python 3.10
- **Primary project path:** `F:\xPy\Json`
- **Recommended Conda environment path:** `F:\vEnv\Json`

The toolset is designed for local use. No network access, authentication, or multi-user access control is required.

## 8.2 Main Purpose

The project provides a repeatable workflow for processing JSON extraction files stored in a local `DATA` directory. These JSON files are expected to contain structured extraction results, including document metadata, topics, items, evidence, provenance, and entity references.

The main purpose is to:

1. Discover JSON files in `./DATA`.
2. Load JSON files safely.
3. Flatten nested topic and item structures into one row per extracted item.
4. Apply text-based filters.
5. Select all or selected columns.
6. Export results to CSV or XLSX.
7. Support both batch and interactive workflows.

## 8.3 Main Components

The project is organized around:

- A shared core library.
- A CLI front-end.
- A Streamlit front-end.
- A legacy script.

The intended single source of truth is:

```text
json_tool/core.py
```

## 8.4 Overall Evaluation

The JSON Extractor project is a small but well-structured local extraction and export tool. The project has clear separation between core logic and user interfaces. It supports both automated batch workflows and interactive review workflows.

Main strengths:

- Clear shared core design.
- Simple beginner-friendly CLI.
- Streamlit interface for interactive use.
- Defensive JSON loading.
- Practical filtering and export features.
- Excel-friendly CSV output.
- XLSX output with a consistent sheet name.
- Good documentation coverage.
- Clear APP_B extraction prompt design for upstream JSON generation.

Main improvement areas:

- Removal or wrapping of the legacy script.
- Replacement of private pandas API usage.
- Clear documentation of output format precedence.
- Optional warnings for schema drift.
- Correction of malformed placeholders in the DOCUMENT transformation prompt.
- Continued alignment between transformation prompts and pipeline validation rules.

---

# 9. Final User Request

The final request was:

```text
Export this session as markdown file.
```

This Markdown file was generated as the session export.
