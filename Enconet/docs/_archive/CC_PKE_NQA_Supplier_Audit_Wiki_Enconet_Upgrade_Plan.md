# NQA Supplier Audit Wiki — Objective Critique and Upgrade Plan

## 1. Context Analysis

The project has evolved from a general LLM Wiki pattern into a controlled audit knowledge system. The target system is no longer only a markdown wiki. It now includes raw-source preservation, derived extraction layers, semantic chunks, APP_B crumbs, criterion pages, evaluation records, an Evaluation Report, and a standalone Dashboard.

The core audit reference is **10 CFR 50 Appendix B**, interpreted through an ASME NQA-1-style evidence-based method. The evaluation method requires requirement-by-requirement comparison, objective evidence support, gap detection, classification, recommendations, and a consolidated conformance score. A positive compliance claim must not be classified as Fully or Substantially Compliant unless at least one objective crumb supports it.

The ingestion design uses two pipelines. The first pipeline chunks raw documentation by chapter and sub-chapter for RAG-like source access. The second pipeline performs “sieving” and generates structured APP_B crumbs. A required project feature is the connection between chunked documents and sieved crumbs.

The APP_B sieving prompt is detailed. It defines RULE and DOCUMENT modes, the 18 Appendix B criteria, required item fields, evidence quotes, source provenance, RULE-specific rule objects, DOCUMENT-side regulatory references, and entity flattening behavior. Some rules are already repo-enforced, while other fields remain template-required but not fully enforced.

The JSON Extractor context adds a practical processing layer. It supports local JSON loading, flattening, filtering, CSV/XLSX export, and Streamlit review. Its expected flattened fields include document metadata, item fields, source fields, evidence quote, and entity references. Known risks include duplicate implementation, private pandas API use, schema drift masking, and malformed DOCUMENT prompt placeholders.

The latest master plan v2 formally upgrades the Dashboard into a first-class generated deliverable. The Dashboard must be generated from validated evaluation data. It must include embedded CSS and JavaScript, no external libraries, no authentication artifacts, criterion cards, filters, search, sorting, a matrix, verification actions, and print support.

The TEKOL examples show two benchmark objects. The audit-session export records an 83.3 / 100 conformance result with 3 Fully Matched, 11 Substantially Matched, and 4 Partially Matched criteria. The corrected dashboard example records 72.2%, 13.0 / 18 weighted units, 2 Fully Matched, 12 Substantially Matched, and 4 Partially Matched criteria. The v2 master plan correctly separates these as a scoring benchmark and a dashboard rendering benchmark.

---

# 2. Critique

## 2.1 Major Strengths

### Strength 1 — Evidence discipline is strong

The evaluation method correctly treats crumbs as grounded facts. Reasoning and inference are not allowed to replace evidence. This rule is essential for an audit-defensible system.

### Strength 2 — The dual-ingestion concept is suitable for audit work

Chunking supports source review. Sieving supports structured evaluation. This split is useful because audit review needs both paragraph-level source access and normalized evidence items.

### Strength 3 — APP_B taxonomy is already well defined

The 18 criteria are named, fixed, and strongly controlled in the sieving prompt. This reduces classification drift.

### Strength 4 — The Dashboard has become a controlled deliverable

The latest v2 plan correctly treats the Dashboard as generated audit software, not a hand-edited artifact. Required data schema, HTML contract, validation, fixture testing, and report consistency are included.

### Strength 5 — Historical benchmark separation is correct

The TEKOL report benchmark and the TEKOL dashboard fixture differ. The plan avoids forcing one value to overwrite the other. This is a sound configuration-control decision.

---

## 2.2 Main Weaknesses and AFI

## AFI-1 — Chunk-to-crumb traceability is still under-specified

### Critique

The ingestion concept states that chunked documents and sieved crumbs must be connected. However, the exact join model is not fully defined. If a crumb only cites a filename, page, or quote, later source review may become weak.

### Improvement

Every crumb should include stable links to:

- `doc_id`
- `chunk_id`
- `quote_id`
- source heading path
- source locator
- raw file checksum

---

## AFI-2 — The database model needs stronger control

### Critique

SQLite is mentioned as an option for chunk storage, but the full schema is not yet fully described in the ingestion context.

### Improvement

A controlled SQLite schema should be added for documents, chunks, crumbs, sources, evaluations, findings, actions, dashboards, and validation results.

---

## AFI-3 — Prompt contract and code validation are not yet equal

### Critique

The APP_B prompt separates repo-enforced fields from template-required fields. This is practical at first, but it can allow low-quality records to pass into later stages.

### Improvement

Validation should be expanded until all audit-critical template-required fields are code-enforced.

---

## AFI-4 — DOCUMENT prompt placeholder defect must be corrected

### Critique

The JSON Extractor session found a malformed DOCUMENT runtime block. The DOCUMENT prompt showed `DOCUMENT>` and a non-null `SOURCE_RULES` placeholder, although DOCUMENT runs should use `DOCUMENT` and `SOURCE_RULES: null`.

### Improvement

Both RULE and DOCUMENT prompts should be versioned, tested, and validated with fixture files.

---

## AFI-5 — Crumb flattening may hide source richness

### Critique

The JSON Extractor flattens the primary source and first evidence quote into scalar columns. The APP_B prompt notes that only the first source entry is projected into normalized scalar columns. This can hide secondary evidence.

### Improvement

A separate `crumb_sources` table and `crumb_quotes` table should preserve all source and quote entries.

---

## AFI-6 — Evaluation scoring needs one canonical scoring model

### Critique

The TEKOL examples show two different score sets: 83.3 / 100 in the audit-session export and 72.2% in the corrected dashboard example. The v2 plan preserves both, but a canonical scoring model for future supplier evaluations still needs to be selected.

### Improvement

A `scoring_model.yml` file should define rating weights, score calculation, rounding rules, and classification thresholds.

---

## AFI-7 — Evaluation Report and Dashboard must be locked to one data source

### Critique

The master plan requires the report and dashboard to be generated from the same evaluation package. This is correct, but it needs hard validation because manual edits could create divergence.

### Improvement

Any generated report or dashboard should fail validation if scores, counts, gaps, or verification actions differ from the shared evaluation JSON.

---

## AFI-8 — Dashboard validation should include functional smoke tests

### Critique

The dashboard validator checks sections, fields, counts, forbidden patterns, and offline status. The feature contract includes filtering, search, sorting, expand/collapse, and print view.

### Improvement

The validation layer should include static JavaScript smoke checks. It should verify that required function names, data bindings, button IDs, and card containers exist.

---

## AFI-9 — Audit findings require a stricter approval state

### Critique

The evaluation method allows gap detection and recommendations. The dashboard includes priority verification actions. However, findings and auditor actions should be separated from generated analysis until reviewed.

### Improvement

Finding pages should remain `draft` until approval is recorded. Auditor actions should be classified as `verification`, `document_request`, `sample_test`, or `interview`.

---

## AFI-10 — Multilingual evidence needs normalization rules

### Critique

Crumbs contain Slovenian evidence and English statements. The system must preserve original language evidence while supporting English evaluation text.

### Improvement

Each crumb should contain:

- original quote
- quote language
- normalized English statement
- translation status
- reviewer flag when translation affects meaning

---

# 3. Project Upgrade Plan — GitHub-Issues Style

## EPIC 1 — Controlled Audit Data Backbone

**Labels:** `epic`, `database`, `traceability`, `must-have`

### What & Why

A controlled data backbone is required because audit results must be traceable from raw documents to final dashboard metrics. The current concept contains documents, chunks, crumbs, reports, and dashboards, but the database contract should be formalized.

### Task 1.1 — Define SQLite schema

**What & Why**  
A fixed schema prevents ad hoc JSON and CSV drift.

**Required tables**

```text
documents
document_chunks
crumbs
crumb_sources
crumb_quotes
rule_items
document_items
criterion_evaluations
findings
auditor_actions
evaluation_runs
dashboard_runs
validation_runs
```

**Acceptance Criteria**

- `db/nqa_audit.sqlite` exists.
- Foreign keys are enabled.
- `documents.doc_id` is unique.
- `document_chunks.chunk_id` is unique.
- `crumbs.item_id` is unique.
- Each crumb has at least one linked chunk or approved exception.

### Task 1.2 — Define stable ID grammar

**What & Why**  
Traceability requires predictable IDs.

**Required ID patterns**

```text
DOC-0001
CHUNK-DOC-0001-0001
QUOTE-DOC-0001-0001-01
CRUMB-DOC-0001-APP_B_IV-0001
EVAL-APP_B_IV
FIND-0001
ACT-0001
DASH-20260703-0001
```

**Acceptance Criteria**

- `schemas/id_patterns.yml` exists.
- Duplicate IDs fail validation.
- Invalid ID formats fail validation.
- All generated outputs use the same IDs.

### Task 1.3 — Preserve all source entries and quotes

**What & Why**  
The first-source-only flattening pattern is not enough for audit review. Full provenance must be preserved.

**Acceptance Criteria**

- `crumb_sources` stores all source objects.
- `crumb_quotes` stores all evidence quotes.
- Primary-source scalar export remains available for tables.
- No secondary source is lost during export.

---

## EPIC 2 — Dual Ingestion Pipeline Upgrade

**Labels:** `epic`, `ingestion`, `chunks`, `crumbs`, `must-have`

### What & Why

The project requires two coordinated ingestion streams: semantic chunking and APP_B crumb generation. The two outputs must be joined.

### Task 2.1 — Build semantic chunking pipeline

**What & Why**  
Large audit documents need reviewable source units.

**Acceptance Criteria**

- Documents are chunked by chapter and sub-chapter.
- Third-level sections, such as `1.1.1`, do not create separate top-level chunks unless configured.
- Each chunk has `doc_id`, `chunk_id`, heading path, text, source filename, and checksum.
- Empty chunks are rejected.

### Task 2.2 — Build APP_B sieving pipeline

**What & Why**  
APP_B crumbs are the structured audit evidence layer.

**Acceptance Criteria**

- RULE and DOCUMENT runs are separate.
- JSON output is valid.
- Each item maps to exactly one APP_B criterion.
- Criterion ID and criterion name pairs match canonical values.
- DOCUMENT items do not contain RULE-only objects.
- RULE items do not contain DOCUMENT-side rule references.

### Task 2.3 — Link crumbs to chunks

**What & Why**  
A crumb must be traceable to its source chunk.

**Acceptance Criteria**

- Each crumb has at least one `chunk_id`.
- Each `chunk_id` exists in `document_chunks`.
- Evidence quote text appears in the linked chunk or has a documented extraction exception.
- A traceability validation script fails on broken links.

---

## EPIC 3 — APP_B JSON Contract Enforcement

**Labels:** `epic`, `schema`, `validation`, `app-b`, `must-have`

### What & Why

The prompt contract must become a code-enforced contract. Prompt discipline alone is not sufficient for audit data.

### Task 3.1 — Create `app_b_json_schema.yml`

**What & Why**  
A machine-readable schema is needed for repeatable validation.

**Acceptance Criteria**

- Required document fields are defined.
- Required item fields are defined.
- Allowed `item_type` values are defined.
- Required RULE object fields are defined.
- DOCUMENT-side rule-reference rules are defined.

### Task 3.2 — Create `validate_app_b_json.py`

**What & Why**  
Invalid JSON must be blocked before import.

**Acceptance Criteria**

- Missing `document` fails validation.
- Missing `items` fails validation.
- Empty `statement` fails validation.
- Empty `evidence_quotes` fails validation.
- Empty `source` fails validation.
- Invalid APP_B criterion fails validation.
- RULE/DOCUMENT side leakage fails validation.

### Task 3.3 — Add prompt fixture tests

**What & Why**  
The malformed DOCUMENT placeholder defect must not recur.

**Acceptance Criteria**

- RULE fixture passes.
- DOCUMENT fixture passes.
- DOCUMENT fixture uses `DOCUMENT_SIDE: "DOCUMENT"`.
- DOCUMENT fixture uses `SOURCE_RULES: null`.
- Malformed placeholder fixture fails.

---

## EPIC 4 — Evaluation Engine

**Labels:** `epic`, `evaluation`, `scoring`, `must-have`

### What & Why

The evaluation method is central to the system. It requires requirement extraction, implementation evidence, conformance analysis, gap detection, recommendations, and score synthesis.

### Task 4.1 — Create requirement registry

**What & Why**  
Each Appendix B criterion needs a controlled requirement record.

**Acceptance Criteria**

- All 18 Appendix B criteria exist.
- Each criterion has sub-requirements where needed.
- Each requirement has a stable ID.
- Each requirement is linked to RULE crumbs.

### Task 4.2 — Create evaluation record model

**What & Why**  
Criterion rulings need structured storage before reports and dashboards are generated.

**Required fields**

```text
criterion_id
criterion_name
classification
score
coverage
completeness
accuracy
clarity
alignment
evidence_supported
affirmative_summary
contrary_summary
judge_ruling
gaps
verification_actions
```

**Acceptance Criteria**

- One evaluation record exists per Appendix B criterion.
- Positive classification requires evidence support.
- Missing evidence downgrades the classification.
- All gap statements point to missing or weak evidence.

### Task 4.3 — Create canonical scoring model

**What & Why**  
Future supplier runs need one score logic. Historical TEKOL variance should remain preserved, not repeated by accident.

**Acceptance Criteria**

- `schemas/scoring_model.yml` exists.
- Rating weights are defined.
- Rounding rules are defined.
- Classification thresholds are defined.
- TEKOL scoring benchmark and dashboard rendering benchmark remain separate fixtures.

---

## EPIC 5 — Evaluation Report Generator

**Labels:** `epic`, `report`, `deliverable`, `must-have`

### What & Why

The Evaluation Report is a formal output. It must be generated from evidence-controlled evaluation records, not hand-written separately.

### Task 5.1 — Create report template

**What & Why**  
A fixed structure improves consistency across suppliers.

**Required sections**

```text
Executive Summary
Scope and Source Documents
Method
Coverage Summary
Criterion-by-Criterion Evaluation
Gap Analysis
Priority Verification Actions
Recommendations
Consolidated Conformance Score
Limitations
Appendix: Evidence Matrix
```

**Acceptance Criteria**

- Template exists in `_shared/templates/evaluation-report-template.md`.
- All required sections are present.
- Evidence claims use crumb IDs or source references.
- Unsupported conclusions are blocked.

### Task 5.2 — Generate report from evaluation data

**What & Why**  
Report/dashboard consistency requires shared data.

**Acceptance Criteria**

- `outputs/<supplier>_appendix_b_evaluation_report.md` is generated.
- `outputs/<supplier>_appendix_b_evaluation_data.json` is generated.
- Report score equals evaluation data score.
- Classification counts match evaluation data.
- Priority actions match action records.

---

## EPIC 6 — Dashboard Generator

**Labels:** `epic`, `dashboard`, `html`, `deliverable`, `must-have`

### What & Why

The Dashboard is a first-class generated deliverable. It must be standalone, offline, self-contained, and consistent with the Evaluation Report.

### Task 6.1 — Create dashboard schema

**What & Why**  
The dashboard data contract must be machine-readable.

**Required criterion object**

```json
{
  "n": "I",
  "order": 1,
  "title": "Organization",
  "rating": "fully",
  "score": 1.00,
  "refs": "Evidence references.",
  "aff": "Evidence supporting conformance.",
  "con": "Evidence gaps or contrary points.",
  "judge": "Final criterion ruling.",
  "verify": "Auditor verification action."
}
```

**Acceptance Criteria**

- `schemas/dashboard_schema.yml` exists.
- Required fields match the v2 contract.
- Rating values include `fully`, `substantially`, `partially`, `minimally`, `unmet`, `undetermined`, and `na`.
- Forbidden authentication and CDN patterns are listed.

### Task 6.2 — Create dashboard template

**What & Why**  
The HTML output must follow the corrected TEKOL dashboard pattern.

**Acceptance Criteria**

- `_shared/templates/dashboard-template.html` exists.
- Embedded CSS is used.
- Embedded JavaScript is used.
- No external CSS, JS, or font reference exists.
- Header, metric bar, executive summary, distribution, controls, cards, matrix, actions, and footer exist.

### Task 6.3 — Create dashboard data builder

**What & Why**  
Dashboard data must come from the same evaluation package as the report.

**Acceptance Criteria**

- `build_dashboard_data.py` reads evaluation data.
- Exactly 18 criterion objects are produced unless a scope exception exists.
- Classification counts are generated.
- Weighted score is generated.
- Priority verification actions are included.

### Task 6.4 — Create dashboard renderer

**What & Why**  
A reproducible renderer prevents manual dashboard edits.

**Acceptance Criteria**

- `generate_dashboard.py` creates:
  - `wiki/dashboards/<supplier>_appendix_b_dashboard.html`
  - `outputs/<supplier>_appendix_b_dashboard.html`
  - `outputs/<supplier>_appendix_b_dashboard_data.json`
- Dashboard opens locally without internet.
- All cards render.
- All matrix rows render.
- Filters, search, sorting, expand/collapse, and print view are present.

### Task 6.5 — Add dashboard validation

**What & Why**  
Invalid HTML, login captures, external scripts, and score drift must be blocked.

**Acceptance Criteria**

- `validate_dashboard_data.py` exists.
- Missing criterion fails validation.
- Wrong rating fails validation.
- Score mismatch fails validation.
- Missing required section fails validation.
- `login.microsoftonline.com`, `oauth`, `signin`, and CDN references fail validation.
- Dashboard validation is mandatory when `phase: dashboard_ready`.

---

## EPIC 7 — Evidence Matrix and Gap Model

**Labels:** `epic`, `matrix`, `gaps`, `audit-output`, `must-have`

### What & Why

The evaluation method requires direct gap detection and auditor verification actions.

### Task 7.1 — Build APP_B evidence matrix

**What & Why**  
The matrix shows coverage by criterion.

**Acceptance Criteria**

- Every criterion is listed.
- RULE evidence count is shown.
- DOCUMENT evidence count is shown.
- Gap count is shown.
- Finding count is shown.
- Verification action count is shown.

### Task 7.2 — Define gap statuses

**What & Why**  
Gaps must be classified in a consistent way.

**Allowed statuses**

```text
covered
mostly-covered
partially-covered
minimally-covered
not-covered
not-applicable
undetermined
missing-evidence
```

**Acceptance Criteria**

- Each gap has one status.
- Each gap links to a criterion.
- Each gap links to missing evidence or weak evidence.
- `missing-evidence` gaps create auditor actions.

### Task 7.3 — Create finding template

**What & Why**  
Findings must remain separate from raw evaluation notes until approved.

**Acceptance Criteria**

- `templates/finding-template.md` exists.
- Each finding links to criterion ID.
- Each finding links to evidence crumbs or missing evidence.
- Each finding has severity, confidence, basis, gap, and verification status.
- Findings remain `draft` until approval exists.

---

## EPIC 8 — Review Gates and State Machine

**Labels:** `epic`, `workflow`, `approval`, `must-have`

### What & Why

Audit work needs controlled phase transitions. The Travel Guide plan used preview/apply gates; the audit system needs stricter gates because audit conclusions can affect formal outputs.

### Task 8.1 — Create audit state machine

**What & Why**  
Unreviewed outputs should not move into final reports.

**States**

```text
registered
chunked
sieved
evidence_reviewed
evaluated
findings_drafted
findings_approved
report_ready
dashboard_ready
closed
failed
```

**Acceptance Criteria**

- `audit_state.py` exists.
- Invalid transitions fail.
- In-progress states are detected at session start.
- Final deliverables require approved evaluation data.

### Task 8.2 — Create approvals manifest

**What & Why**  
Approval records are needed for audit defensibility.

**Acceptance Criteria**

- `manifests/approvals.csv` exists.
- Each row has object ID, decision, date, reviewer label, and notes.
- Finding approval is required before final report release.
- Dashboard release requires validation PASS.

---

## EPIC 9 — JSON Extractor Refactor and Integration

**Labels:** `epic`, `json-extractor`, `tooling`, `should-have`

### What & Why

The JSON Extractor is a useful review and export tool, but known risks should be corrected before deeper integration.

### Task 9.1 — Consolidate flattening logic

**What & Why**  
Duplicate flattening creates drift risk.

**Acceptance Criteria**

- `json_tool/core.py` is the only flattening source.
- Legacy script calls the core library or is marked deprecated.
- CLI and Streamlit outputs match for the same input.

### Task 9.2 — Replace private pandas API use

**What & Why**  
Private APIs may break after dependency updates.

**Acceptance Criteria**

- `df._append` is removed.
- `pd.concat(..., ignore_index=True)` is used.
- Regression export tests pass.

### Task 9.3 — Add schema drift warnings

**What & Why**  
Automatic missing-column creation can hide upstream changes.

**Acceptance Criteria**

- Missing expected fields are logged.
- Unexpected fields are logged.
- Export continues in warning mode.
- Strict mode fails on schema drift.

---

## EPIC 10 — TEKOL Benchmark Fixtures

**Labels:** `epic`, `benchmark`, `regression`, `must-have`

### What & Why

TEKOL data provides two useful benchmark classes: scoring reproduction and dashboard rendering. These must stay separate.

### Task 10.1 — Preserve TEKOL scoring benchmark

**What & Why**  
The audit-session export provides a historical scoring benchmark.

**Acceptance Criteria**

- Fixture records 83.3 / 100.
- Fixture records Substantially Matched.
- Fixture records 3 Fully, 11 Substantially, 4 Partially, and 0 Minimal/Unmet.
- Fixture is used only for scoring regression.

### Task 10.2 — Preserve TEKOL dashboard rendering benchmark

**What & Why**  
The corrected dashboard example provides a visual and functional benchmark.

**Acceptance Criteria**

- Fixture records 72.2%.
- Fixture records 13.0 / 18 weighted units.
- Fixture records 2 Fully, 12 Substantially, 4 Partially, and 0 Unmet.
- Fixture is used only for dashboard rendering tests.

### Task 10.3 — Add variance note

**What & Why**  
The two TEKOL scores should not be treated as a conflict if their basis differs.

**Acceptance Criteria**

- `benchmarks/TEKOL_VARIANCE_NOTE.md` exists.
- Difference is explained as benchmark-type variance.
- Scoring tests do not require 72.2%.
- Dashboard tests do not require 83.3%.

---

# 4. Recommended Implementation Order

1. **EPIC 1 — Controlled Audit Data Backbone**
2. **EPIC 2 — Dual Ingestion Pipeline Upgrade**
3. **EPIC 3 — APP_B JSON Contract Enforcement**
4. **EPIC 4 — Evaluation Engine**
5. **EPIC 7 — Evidence Matrix and Gap Model**
6. **EPIC 5 — Evaluation Report Generator**
7. **EPIC 6 — Dashboard Generator**
8. **EPIC 8 — Review Gates and State Machine**
9. **EPIC 9 — JSON Extractor Refactor and Integration**
10. **EPIC 10 — TEKOL Benchmark Fixtures**

This order places traceability and validation before report and dashboard generation. This reduces the risk of producing polished outputs from weak evidence.

---

# 5. Final Upgrade Position

The project should be upgraded from an LLM-maintained wiki into a **validated audit evidence compiler**. The strongest design point is the evidence-bounded evaluation method. The main remaining risk is traceability drift between raw documents, chunks, crumbs, evaluation records, report text, and dashboard metrics.

The most important project upgrade is therefore a shared, validated data spine:

```text
raw document
→ extracted text
→ semantic chunk
→ evidence quote
→ APP_B crumb
→ criterion evaluation
→ finding / action
→ evaluation report
→ dashboard data
→ dashboard HTML
```

A valid final system should produce both the Evaluation Report and Dashboard from the same evaluation data package. The Dashboard should not be a screenshot, browser capture, or manual HTML edit. It should be a generated, offline, validated audit interface over evidence-controlled records.
