# Sieving Method Specification Guide

## 0. Document control

| Field | Value |
|---|---|
| Project | Project03 / PKE_SA_Enconet |
| Document | Sieving_method_specification_Guide |
| Version | 1.2 — §10.1 configuration ownership corrected against pipeline source code |
| Date | 2026-07-11 |
| Status | AS-IS specification of the **current** sieving method (baseline before EPIC 5 / EPIC 18 upgrades) |
| Governing template | `JSON_Template_App_B`, template_version **0.1** (`templates/app_b.py::AppBTemplate`) |
| Primary sources | **`sieving/` — the vendored pipeline implementation** (`sieving/src/json_extractor/`; enforcement verified at code level; upstream origin github.com/nekiee13/opencode-JSON, recorded in `sieving/PROVENANCE.md`), `docs/context/31 Sieving - Crumb generation.md` (both transformation prompts), `docs/context/32 Crumbs proccessing - json_extractor_session_exp.md` (v0.1-era description, partially superseded — see §10), `docs/context/30 Ingestion phase.md` (pipeline position) |
| Related plan sections | MASTER_DEVELOPMENT_PLAN.md — EPIC 5 (sieving pipeline), EPIC 6 (traceability), EPIC 15 (extractor integration), EPIC 18 (tuning harness) |
| Change note | **v1.1 → v1.2:** corrected §10.1: `config.py` duplicates the criteria and rule-code tables locally; it does not derive them from `AppBTemplate`. Consolidation remains planned under ALIGNMENT_PLAN Task C4.4. |

**Purpose of this guide.** Sieving is the crown activity of this project: crumb quality
bounds every downstream result. This guide records, in one place, exactly how the current
method works — its prompts, its data contract, what is enforced versus merely required,
its runtime interface, its downstream consumers, and its known defects and limitations —
so that every future prompt iteration starts from a precisely known baseline.

---

## 1. What sieving is

**Sieving** is the transformation of a source document into **crumbs**: small, structured,
evidence-bearing JSON records, each classified under exactly one of the 18 criteria of
10 CFR 50 Appendix B (the APP_B taxonomy). A crumb captures one statement of audit-relevant
content together with its verbatim evidence quote(s) and source location.
(source: docs/context/31)

Crumbs are treated downstream as **grounded facts** — objective evidence for the
criterion-by-criterion conformance evaluation. Reasoning or inference is never allowed to
substitute for them. (source: docs/context/36)

### 1.1 Position in the ingestion architecture

The project uses two coordinated ingestion pipelines (source: docs/context/30):

| Pipeline | Output | Purpose |
|---|---|---|
| 1 — Semantic chunking | Chapter / sub-chapter chunks in DB | RAG-like source access; human source review |
| 2 — **Sieving** | APP_B crumbs (structured JSON) | Structured evidence layer for evaluation |

A required feature is the **connection between chunks and crumbs** (pipeline 1 ↔ pipeline 2).
The current method does **not** implement this link — it is a planned upgrade (EPIC 6).

### 1.2 Execution model

Sieving is executed by an LLM acting under a fixed **transformation prompt** in the role
of *Information Extraction Analyst*. The instruction is to reason exhaustively for
correctness but to output **only valid JSON** — no markdown, no commentary, exactly one
JSON object. (source: docs/context/31)

There are two prompt variants, selected by the source type:

- **Transformation prompt — RULE** — for regulation / requirements documents
  (e.g. 10 CFR 50 Appendix B itself, 10 CFR 21).
- **Transformation prompt — DOC** — for supplier documents
  (procedures, QA manuals, plans, audit reports, etc.).

The two prompt bodies are **identical in sections 0–8**; they differ only in the runtime
input block (section 9), where the run context is filled in (see §8 of this guide, incl.
the known defect). (source: docs/context/31)

---

## 2. The two-tier enforcement model

The defining design property of the current method: the prompt distinguishes two levels
of requirement, because the downstream pipeline (`load_and_flatten.py`, `config.py`,
`query/schema.py`) validates only a subset of the template. (source: docs/context/31)

| Tier | Meaning | Consequence of violation |
|---|---|---|
| **REPO-ENFORCED** | Validation implemented in `extract/load_and_flatten.py::validate_item` | `ValidationError` (severity ERROR) recorded against the item |
| **TEMPLATE-REQUIRED** | Data-quality contract stated by the prompt, **not enforced in code** | Low-quality record passes silently |

**Verified enforcement semantics (code level).** Validation in the current pipeline is
**advisory, not blocking**: `validate_item` returns a list of `ValidationError` objects,
but `flatten_item_to_record` still emits the record, and `run_pipeline` collects the
errors into `PipelineResult.validation_errors` while the rows flow into the DataFrame and
exports. "REPO-ENFORCED" therefore means *detected and flagged as ERROR*, not *rejected*.
Blocking import on ERROR is a planned upgrade (plan Task 5.3/5.4 — the importer refuses
files that fail validation). (source: opencode-JSON `load_and_flatten.py`, `pipeline.py`)

### 2.1 Verified validation rule registry (code level)

The actual checks in `validate_item`, with their in-code rule IDs:

| Rule ID | Severity | Checks |
|---|---|---|
| VAL-COMMON-001 | ERROR | `template_id` non-empty; `template_version` non-empty; `taxonomy_id == "APP_B"` |
| VAL-TAX-001 | ERROR | `criterion_id` in the canonical 18 |
| VAL-TAX-002 | ERROR | `criterion_name` matches canonical name for `criterion_id` |
| VAL-EVID-001 | ERROR | ≥1 non-empty `evidence_quotes` entry |
| VAL-PROV-001 | ERROR | ≥1 `source` entry |
| VAL-RULELEAK-001 | ERROR | RULE item carries no `rule_references` / `rule_reference_ids` |
| VAL-JOIN-001 | ERROR | RULE `rule` object: `source_rules` canonical; `rule_locator` non-empty; `rule_key == source_rules::rule_locator`; `rule_strength ∈ {MANDATORY, NON_MANDATORY}` |
| VAL-LOC-001 | ERROR | Locator policy: `10CFR50_APPB` → locator is a valid criterion_id; `10CFR21` → regex `^21\.[0-9]+$` |
| VAL-RULELEAK-002 | ERROR | DOCUMENT item carries no `rule` object |
| VAL-JOIN-002 | **WARNING** | DOCUMENT `rule_reference_ids` entries contain `::` |

**Verified gaps in code enforcement** (fields the prompt requires but `validate_item`
never checks): `statement` non-emptiness, `item_id` uniqueness, `item_type` enum
membership, and — notably — **`record_side` itself**: an item whose `record_side` is
missing or misspelled silently skips *all* side-specific checks (both RULELEAK rules,
JOIN, LOC). These gaps are the concrete work list for the strict tier of
`schemas/app_b_json_schema.yml` (plan Task 1.4).

Every field requirement in this guide is tagged with its tier. The remaining gap between
tiers is a known weakness of the current method; the target state (plan Task 1.4 / 5.3)
promotes all audit-critical TEMPLATE-REQUIRED fields to code-enforced *and blocking*.

---

## 3. Run context (REPO-ENFORCED)

Each run is parameterized by user-provided context before the document content:

**DOCUMENT_SIDE** — exact enum, required:
- `"RULE"`
- `"DOCUMENT"`

**SOURCE_RULES** — conditional:
- If `DOCUMENT_SIDE == "RULE"` → REQUIRED, exactly one of `"10CFR50_APPB"` | `"10CFR21"`.
- If `DOCUMENT_SIDE == "DOCUMENT"` → MUST be omitted or null.

**Mandatory classification rule** (template-required, repo-aligned):
1. Organizational procedures, manuals, plans, and internal documents are **always DOCUMENT**.
2. Embedded regulatory references inside DOCUMENTs remain DOCUMENT items (captured via
   `rule_reference_ids`, never via a `rule` object).
3. Regulatory material intended to function as a RULE must be processed in a **separate
   RULE run**.

(source: docs/context/31, §0)

---

## 4. The APP_B taxonomy (REPO-ENFORCED)

Each extracted item MUST be assigned to **exactly one** of the 18 Appendix B criteria.
`criterion_id` and `criterion_name` MUST match these canonical pairs exactly:

| criterion_id | criterion_name |
|---|---|
| APP_B_I | Organization |
| APP_B_II | Quality Assurance Program |
| APP_B_III | Design Control |
| APP_B_IV | Procurement Document Control |
| APP_B_V | Instructions, Procedures, and Drawings |
| APP_B_VI | Document Control |
| APP_B_VII | Control of Purchased Material, Equipment, and Services |
| APP_B_VIII | Identification and Control of Materials, Parts, and Components |
| APP_B_IX | Control of Special Processes |
| APP_B_X | Inspection |
| APP_B_XI | Test Control |
| APP_B_XII | Control of Measuring and Test Equipment |
| APP_B_XIII | Handling, Storage, and Shipping |
| APP_B_XIV | Inspection, Test, and Operating Status |
| APP_B_XV | Nonconforming Materials, Parts, or Components |
| APP_B_XVI | Corrective Action |
| APP_B_XVII | Quality Assurance Records |
| APP_B_XVIII | Audits |

(source: docs/context/31, §1; verified against the official public text of
10 CFR 50 Appendix B)

Note: the taxonomy is fixed by regulation and never edited per supplier. Criterion
**applicability** (whether a criterion applies to a given company) is a separate,
downstream ruling — it plays no role during sieving; sieving extracts whatever the
document contains.

---

## 5. Crumb data contract (item level)

Each extracted item MUST include the following fields
(TEMPLATE-REQUIRED unless marked otherwise):

| Field | Type / constraint | Tier (code-verified) |
|---|---|---|
| `item_id` | string; unique within document | template-required (uniqueness **not** checked in code) |
| `record_side` | `"RULE"` or `"DOCUMENT"` | template-required — enum itself **not** checked; invalid value silently skips all side checks (§2.1) |
| `template_id` | `= "JSON_Template_App_B"` | **REPO-ENFORCED** non-empty (exact value not checked) — VAL-COMMON-001 |
| `template_version` | `= "0.1"` | **REPO-ENFORCED** non-empty (exact value not checked) — VAL-COMMON-001 |
| `taxonomy_id` | `= "APP_B"` | **REPO-ENFORCED** — VAL-COMMON-001 |
| `criterion_id` | one of the 18 (see §4) | **REPO-ENFORCED** — VAL-TAX-001 |
| `criterion_name` | exact canonical name for `criterion_id` | **REPO-ENFORCED** — VAL-TAX-002 |
| `item_type` | exact enum (below) | template-required (enum defined in `AppBTemplate.ITEM_TYPE_VALUES` but **not** checked at validation) |
| `statement` | non-empty string | template-required (**not** checked in code) |
| `evidence_quotes` | array with ≥1 non-empty string | **REPO-ENFORCED** — VAL-EVID-001 |
| `source` | array with ≥1 object | **REPO-ENFORCED** — VAL-PROV-001 |

**`item_type` enum (12 values, exact):**

```text
requirement | process_step | role_responsibility | definition |
control | record | reference | finding |
recommendation | action | status_statement | other
```

(source: docs/context/31, §2)

**Reading of the contract:** a crumb is, at minimum-enforced level, *"an APP_B-classified
record with at least one verbatim evidence quote and at least one source pointer."*
Everything else — including the statement itself, the item type, and uniqueness of
`item_id` — currently rides on prompt discipline alone.

---

## 6. Provenance model (PARTIALLY ENFORCED)

Each item MUST include `source`: a non-empty list (**REPO-ENFORCED**).

Each source object SHOULD include (best effort; NOT strictly enforced):

| Field | Type |
|---|---|
| `page` | number \| null |
| `page_label` | string \| null |
| `heading_path` | array of strings |
| `section_id` | string \| null |
| `block_type` | string — SHOULD be one of: `heading | prose | table | diagram | list | figure | footer | header | annex | other` |
| `location_cue` | string |

**Critical flattening note (code-verified):** only the **first** source entry is
projected into the normalized scalar columns (`source_page`, `source_page_label`,
`source_heading_path` — joined with ` > `, `source_section_id`, `source_block_type`,
`source_location_cue`). Additional source entries survive in the raw JSON but disappear
from tabular views. Evidence quotes fare better: `evidence_quote_1` carries the first
quote **and `evidence_quotes_json` preserves the full quote array** as a JSON string
column. (source: opencode-JSON `flatten_source`, `flatten_item_to_record`)

Sources-beyond-first remain the information-loss point of the current method (see §11);
the target state preserves all sources and quotes in dedicated relational tables
(plan Task 5.4).

---

## 7. RULE vs DOCUMENT semantics

### 7.1 RULE side (`DOCUMENT_SIDE == "RULE"`)

REPO-ENFORCED:
- `record_side` MUST be `"RULE"`.
- If a `rule` object is present, its join semantics are validated (below).

TEMPLATE-REQUIRED (expected in practice) — each item SHOULD include a `rule` object:

| Field | Constraint |
|---|---|
| `source_rules` | `= SOURCE_RULES` from run context |
| `rule_strength` | `"MANDATORY"` or `"NON_MANDATORY"` |
| `rule_locator` | if `source_rules == "10CFR50_APPB"` → MUST equal one of `APP_B_I` … `APP_B_XVIII`; if `source_rules == "10CFR21"` → MUST match `21.<n>` (**section only, no subsections**) |
| `rule_key` | `= "<source_rules>::<rule_locator>"` |
| `rule_citation_text` | string |

REPO-ENFORCED **when the rule object exists**:
- `rule_key` MUST equal `source_rules + "::" + rule_locator`.
- `rule_strength` MUST be valid.
- `rule_locator` MUST match the policy for `source_rules`.

REPO-ENFORCED side-leak check (RULE items must not carry DOCUMENT-side machinery):
- `item.rule_references` MUST be absent or empty.
- `item.rule_reference_ids` MUST be absent or empty.

### 7.2 DOCUMENT side (`DOCUMENT_SIDE == "DOCUMENT"`)

REPO-ENFORCED:
- `record_side` MUST be `"DOCUMENT"`.
- `item.rule` MUST be absent or null (DOCUMENT items never carry a rule object).

TEMPLATE-REQUIRED:
- RULE-only semantics must not be represented via a rule object.

Embedded regulatory references MAY be captured via:
- `rule_reference_ids` — array of strings.

**Join determinism (PARTIALLY ENFORCED):** entries SHOULD have the form
`"<ref_code>::<ref_locator>"`. The presence of `::` is **warned** on mismatch; the
structure is not otherwise validated. (source: docs/context/31, §4)

**Design intent of the split:** RULE crumbs carry authoritative requirement anchors
(`rule_key` is the join key for requirement mapping); DOCUMENT crumbs carry the supplier's
implementation evidence, optionally pointing at regulations via `rule_reference_ids`. The
side-leak checks keep the two vocabularies from contaminating each other, which is what
makes the later requirement↔evidence join deterministic.

---

## 8. Runtime interface and output requirements

### 8.1 Output requirements (STRICT)

- Output exactly **one** JSON object; no text outside JSON.
- JSON MUST include at least: `document` and `items`.
- JSON MUST satisfy all REPO-ENFORCED constraints above.
- TEMPLATE-REQUIRED fields MUST be populated unless explicitly marked optional.

(source: docs/context/31, §8)

### 8.2 Document-level metadata

REPO-CONSUMED fields (everything else is optional and may be ignored by the pipeline):

- `document.doc_id`
- `document.filename`
- `document.title`
- `document.control_metadata.revision`

(source: docs/context/31, §5)

### 8.3 Runtime input blocks

The prompt ends with user-filled blocks:

```text
DOCUMENT_SIDE:
"<RULE|DOCUMENT>"

SOURCE_RULES (only if DOCUMENT_SIDE == RULE):
"<10CFR50_APPB | 10CFR21>"

DOCUMENT CONTENT:
"<<PASTE DOCUMENT HERE>>"

END OF DOCUMENT CONTENT
```

### 8.4 ⚠ KNOWN DEFECT — DOC prompt runtime block

The current **Transformation prompt — DOC** carries a malformed runtime block
(source: docs/context/31, lines 491–495, quoted verbatim):

```text
DOCUMENT_SIDE:
"DOCUMENT>"                      ← stray ">" in the enum value

SOURCE_RULES (only if DOCUMENT_SIDE == RULE):
"<10CFR50_APPB>"                 ← non-null placeholder; DOCUMENT runs require null
```

**Correct form for a DOCUMENT run:**

```text
DOCUMENT_SIDE:
"DOCUMENT"

SOURCE_RULES: null
```

Until the prompt file is corrected (plan Task 5.1) and fixture-tested (plan Task 5.6),
any operator using the DOC prompt must fix the runtime block manually at run time.
This defect class is the origin of the plan's prompt-versioning + fixture-test requirement.

---

## 9. Entities (flattening behavior precisely defined)

The pipeline flattens **only item-level** entity groups:

- `items[].entities.organizations`
- `items[].entities.people`
- `items[].entities.documents`
- `items[].entities.systems_tools`
- `items[].entities.standards_regulations`

Rules:
- These MUST be arrays if present (empty arrays allowed).
- Entities SHOULD be placed at item level to appear in normalized outputs.
- **Root-level entity arrays MAY appear but are IGNORED** by the current pipeline.
- Additional entity groups (e.g. suppliers, contracts) are optional / non-enforced and
  may be dropped during normalization.

(source: docs/context/31, §6)

### 9.1 Optional / non-enforced fields

The following may appear but are **not validated, queried, or exported**:

- `document.structure_map`, `document.doc_type_guess`, `document.language_guess`
- `document.control_metadata` fields other than `revision`
- `items[].other_sources`, `items[].tags`
- structured `rule_references` objects beyond `rule_reference_ids`
- confidence levels, authority levels, rule versions, rule IDs

(source: docs/context/31, §7)

---

## 10. Downstream processing — the sieving subsystem (`sieving/`)

Crumb JSON files are consumed by the **JSON Extractor**, a substantially evolved
successor to the v0.1 tool described in docs/context/32. The implementation is
**vendored into this project at `sieving/`** as an integral, locally-maintained
subsystem — one location where sieving is implemented, maintained, modified, and
interconnected with the wiki system. Upstream origin: github.com/nekiee13/opencode-JSON,
recorded with commit hash in `sieving/PROVENANCE.md`. Facts below are verified against
that source code; where doc 32 differs, the code wins.

### 10.1 Current subsystem layout

```text
sieving/                                (vendored, project-integral)
├── cli.py                             ← headless dev/debug entry (retired at EPIC 15 close)
├── src/json_extractor/
│   ├── config.py                      ← Config (locally duplicated criteria/codes; not derived from AppBTemplate)
│   ├── pipeline.py                    ← run_pipeline / export_pipeline_result
│   ├── extract/load_and_flatten.py    ← validate_item + flattening (the enforcement core)
│   ├── templates/app_b.py             ← AppBTemplate: canonical criteria, codes, enums
│   ├── query/                         ← filter DSL: schema.py, compiler.py, engine.py
│   └── io/                            ← file discovery, JSON reading, export
├── DATA/RULE/                         ← real RULE runs: 10CFR50_AppendixB, 10CFR21
├── DATA/DOCUMENT/                     ← ~60 real DOCUMENT crumb files (worked examples)
├── tests/                             ← pytest suite (pipeline, DSL, export)
├── tools/fix_*.py                     ← post-hoc data repair scripts (drift history)
└── PROVENANCE.md                      ← upstream origin + commit + divergence log
```

`config.py` does **not** import or derive its canonical criteria or rule-code tables
from `AppBTemplate`. `Config.get_canonical_criteria()` and
`Config.get_canonical_codes()` define local literal tables, while
`templates/app_b.py::AppBTemplate` independently defines `CRITERIA` and
`CANONICAL_CODES`. These are duplicate contract owners in the current subsystem and
can drift. ALIGNMENT_PLAN Task C4.4 will replace them with one machine-readable schema
owner and a drift test; until then, changes to either table must be synchronized
manually. (source: `sieving/src/json_extractor/config.py`,
`sieving/src/json_extractor/templates/app_b.py`; cross-reference: C4.4)

**No separate GUI (decision 2026-07-04).** The upstream Streamlit review UI
(`adapters/streamlit_app/`, `app.py`) was removed at vendoring: sieving is operated
through project scripts and slash commands, and reviewed through generated reports/wiki
pages, DB queries, and CSV/XLSX exports. See `sieving/PROVENANCE.md` divergence log;
recoverable from git history if ever needed.

### 10.2 Verified input shape

`flatten_json_to_records` reads `document` (with `control_metadata.revision`) and
**`items[]` directly at the JSON root** — exactly matching the prompt's output contract
(§8.1). The `topics[] → topic_name` nesting described in docs/context/32 §3.3 was the
legacy v0.1 shape and **does not exist in the current pipeline**; there is no
`topic_name` column. Bad files are skipped with a `BadFileReport`; non-dict JSON roots
are rejected defensively. (source: opencode-JSON `pipeline.py`, `load_and_flatten.py`)

### 10.3 Verified flattened record schema (one row per item)

```text
template_id | template_version | taxonomy_id | record_side |
doc_id | filename | title | revision |
item_id | item_type | criterion_id | criterion_name | statement |
evidence_quote_1 | evidence_quotes_json |
source_page | source_page_label | source_heading_path | source_section_id |
source_block_type | source_location_cue |
entities_organizations | entities_people | entities_documents |
entities_systems_tools | entities_standards_regulations |
rule_source_rules | rule_locator | rule_key | rule_strength |        (RULE-only)
rule_ref_keys | rule_ref_codes | rule_ref_locators                   (DOCUMENT-only)
```

Key invariants (code-verified):
- One row per item; column order normalized to the canonical schema in Config.
- `source_heading_path` joined with ` > `; entity strings joined with `; `
  (deduplicated + sorted); people rendered `Name (Role)`; documents
  `Identifier: Name Rev N`; standards `Identifier: Name`.
- **There is no `confidence` column** — the v0.1 schema's `confidence` field is gone,
  consistent with the prompt's non-enforced list (§9.1).
- All evidence quotes survive in `evidence_quotes_json`; only the first source entry
  survives in scalar columns (§6).

### 10.4 Filtering and export

Filtering uses a typed **DSL** over `query/schema.py` fields — e.g.
`criterion_id:APP_B_I AND record_side:RULE` — with enum fields validated against
controlled vocabularies and side-specific fields (RULE-only / DOCUMENT-only) marked in
the schema. DSL parse or execution errors are surfaced via `filter_error` while the
DataFrame is returned **unfiltered** (fail-loud, non-blocking). Export goes to CSV/XLSX
via `io/export.py`. (source: opencode-JSON `query/`, `pipeline.py`)

### 10.5 Status of the v0.1 risks (docs/context/32 §6.9) in the current repo

| v0.1 risk | Current status (verified) |
|---|---|
| Duplicate implementation (`Read_Json.py` vs `json_tool/core.py`) | **Resolved** — neither file exists; single implementation in `src/json_extractor/` |
| Private pandas API (`df._append`) | **Resolved** — no `_append` usage in the codebase |
| Format/suffix precedence | Handled in `export_pipeline_result` (fmt parameter) — verify behavior during EPIC 15 vendoring |
| Schema drift masking | **Still relevant** — column normalization selects existing canonical columns; drift visibility remains a plan item (Task 15.3) |

The `tools/fix_*.py` scripts (e.g. `fix_mor_taxonomy_id.py`, `fix_rule_refs_from_criterion.py`)
are recorded evidence that crumb-data drift happened in practice and was repaired
post-hoc — reinforcing the plan's move to blocking validation at import time.

---

## 11. Known limitations of the current method (baseline gaps)

Recorded so every future tuning iteration knows what the baseline does **not** do.
Each maps to a planned upgrade in MASTER_DEVELOPMENT_PLAN.md.

| # | Limitation | Consequence | Planned fix |
|---|---|---|---|
| 1 | **Validation is advisory, not blocking** (§2): ERROR-flagged records still flow into DataFrame and exports | Invalid crumbs can reach review/export unnoticed | Task 5.3/5.4 (blocking import gate) |
| 2 | Two-tier enforcement gap — code-verified unchecked fields: `statement` non-empty, `item_id` uniqueness, `item_type` enum, **`record_side` enum** (invalid side silently skips all side checks) | Low-quality or side-ambiguous crumbs pass silently | Task 1.4 + 5.3 (strict schema tier) |
| 3 | First-source scalar flattening (all quotes survive via `evidence_quotes_json`; sources beyond the first only in raw JSON) | Secondary source locations invisible in tabular review | Task 5.4 (`crumb_sources`, `crumb_quotes` tables) |
| 4 | No chunk linkage | Crumb cites filename/page at best; weak source review | EPIC 6 (`crumb_chunk_links`, quote-in-chunk verification) |
| 5 | DOC prompt runtime-block defect (§8.4) | Mislabeled runs possible; side leakage | Task 5.1 (corrected versioned prompts) + 5.6 (fixtures) |
| 6 | No prompt versioning, no run generations (drift repaired post-hoc via `tools/fix_*.py`) | "Which prompt made these crumbs?" unanswerable; re-runs destructive | Task 5.2 (`sieve_runs`), EPIC 18.2 (generations), 18.6 (CHANGELOG) |
| 7 | No effectiveness measurement | Tuning is blind; first-attempt quality unknowable | EPIC 18.3 (metrics), 18.4 (diff), 18.5 (golden set) |
| 8 | No multilingual fields | Slovenian evidence and English analysis not systematically separated | Task 5.5 (`quote_original`, `quote_language`, `statement_en`, `translation_status`) |
| 9 | Criterion XIII name: system canon is "Handling, Storage, and Shipping" (Oxford comma) vs official CFR heading "Handling, Storage and Shipping" | Cosmetic; exact-match validators must use the system canon consistently | Note in `schemas/app_b_taxonomy.yml` (Task 1.1) |

Resolved since docs/context/32 (verified in opencode-JSON): the `topics[]` input-shape
question (current pipeline reads `items[]` at root, matching the prompt), the
`confidence` column ambiguity (no such column exists), duplicate flattening
implementations (single `src/json_extractor/`), and `df._append` (gone).

---

## 12. Change control for this method

- This guide describes **baseline v0.1** (template_version `0.1`, prompts as captured in
  docs/context/31, code as vendored in `sieving/` — see `sieving/PROVENANCE.md`). It is
  the reference point for the first versioned prompts
  (`sieving/prompts/appb_rule_v1.md`, `sieving/prompts/appb_document_v1.md`, plan Task 5.1).
- From EPIC 18 onward, the sieving method changes **only** through the tuning loop:
  new prompt version → golden-set score → metrics + diff vs previous generation →
  human promotion decision → `sieving/prompts/CHANGELOG.md` entry.
- `sieving/SIEVING_PLAYBOOK.md` (Task 18.1) will be the operational how-to companion to
  this specification; this guide remains the *what-and-why* contract reference.
- Code changes to `sieving/src/` are ordinary project changes (this repo's git history);
  the upstream GitHub repo is historical origin only and is not pulled from.
- Any change to the crumb data contract (§5–§7) is a schema change: it must update
  `schemas/app_b_json_schema.yml`, the prompt files, the fixtures, and this guide together.

---

*End of Sieving Method Specification Guide v1.2 — AS-IS baseline recorded 2026-07-04;
§10.1 configuration ownership corrected 2026-07-11 against the vendored pipeline
source; enforcement details verified against github.com/nekiee13/opencode-JSON.*
