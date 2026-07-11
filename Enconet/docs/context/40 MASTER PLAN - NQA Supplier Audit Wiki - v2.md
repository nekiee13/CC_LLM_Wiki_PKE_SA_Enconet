# MASTER PLAN v2 — NQA Supplier Audit Wiki

## Revision Focus: Dashboard as a First-Class Generated Deliverable

**Project:** Project03 — Nuclear Quality Assurance Supplier Audit Wiki / NQA-1 Wiki  
**Revision basis:** Master Plan v1 plus corrected TEKOL static dashboard example  
**Primary deliverables:** Evaluation Report and standalone HTML Dashboard  
**Execution model:** Claude Code inside Ubuntu VM, Obsidian as human-facing wiki interface, Git as version history

***

## Change Log — v1 → v2

| Area                         | v1 State                                                | v2 Revision                                                                                                                                 |
| ---------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Dashboard                    | Defined as static HTML output with general feature list | Upgraded into a formal **dashboard rendering contract** based on the corrected TEKOL example                                                |
| Dashboard data model         | General `dashboard_data.json` mentioned                 | Explicit criterion-object schema added: `n`, `order`, `title`, `rating`, `score`, `refs`, `aff`, `con`, `judge`, `verify`                   |
| Dashboard generator          | Required offline HTML                                   | Must generate embedded CSS, embedded JavaScript, no external libraries, criterion cards, filters, sorting, matrix, verification actions     |
| Dashboard validation         | Checked for no external CDN and score match             | Expanded to validate DOM sections, data schema, classification counts, weighted score, filter buttons, matrix rows, and offline portability |
| Report/dashboard consistency | General consistency required                            | Dashboard must be generated from the same evaluation records as the Evaluation Report                                                       |
| TEKOL benchmark              | Regression benchmark noted                              | TEKOL dashboard becomes a formal **visual and functional benchmark**                                                                        |
| Invalid dashboard sources    | Microsoft login HTML excluded                           | Exclusion rule retained and strengthened: authentication pages are rejected by validator                                                    |

***

## 1. Revised Design Rationale

The NQA Supplier Audit Wiki remains a PKE-based audit knowledge system. Raw supplier documents are preserved, derived layers support extraction, wiki pages compile evidence, and final outputs are generated from validated evidence. This follows the PKE pattern of shared schema, phase-aware validation, deterministic IDs, citation checking, and traceability gates. [\[CodeInterpreter \| Undefined\]](https://eu-prod.asyncgw.teams.microsoft.com/v1/objects/0-neu-d14-4ebc0d42a6a8b615b4e17c3809f27a96/views/original/NQA_Supplier_Audit_Wiki_Session_Export.md)

The main v2 change is that the **Dashboard** is no longer treated only as a final HTML file. It is now a controlled deliverable with a schema, template, generator, validation script, and regression benchmark. The TEKOL audit export already required a standalone dashboard with overall score, classification distribution, criterion cards, search/filter functions, sortable matrix, remediation gaps, auditor verification actions, and print/PDF support. [\[35 Evaluat...and Report \| PDF\]](https://mynek-my.sharepoint.com/personal/rdolovcak_nek_si/Documents/Microsoft%20Copilot%20Chat%20Files/35%20Evaluation%20Method%20and%20Report.pdf)

The corrected TEKOL dashboard example confirms the desired implementation pattern: one standalone HTML file with embedded CSS, embedded JavaScript, an internal criterion data array, metric cards, classification filters, search, sorting, expandable criterion cards, conformance matrix, and priority verification actions. This design is now adopted as the dashboard reference contract.

***

## 2. Revised Core Output Chain

```text
raw supplier documents
  → extracted text
  → semantic chunks
  → APP_B crumbs
  → chunk-linked evidence pages
  → compliance matrix
  → criterion evaluations
  → findings and auditor actions
  → evaluation report
  → dashboard data object
  → standalone HTML dashboard
```

The Evaluation Report and Dashboard must be generated from the same evidence-controlled evaluation layer. A dashboard score must never diverge from the report score unless a validation failure is raised. The evaluation method requires evidence-supported coverage, completeness, accuracy, clarity, alignment, and objective evidence support. [\[CodeInterpreter \| Undefined\]](https://eu-prod.asyncgw.teams.microsoft.com/v1/objects/0-neu-d14-4ebc0d42a6a8b615b4e17c3809f27a96/views/original/NQA_Supplier_Audit_Wiki_Session_Export.md)

***

## 3. Revised Dashboard Contract

### 3.1 Dashboard File Contract

Each supplier dashboard must be generated as:

```text
wiki/dashboards/<supplier>_appendix_b_dashboard.html
outputs/<supplier>_appendix_b_dashboard.html
outputs/<supplier>_appendix_b_dashboard_data.json
```

**Comment:** The wiki copy is retained for Obsidian navigation. The output copy is packaged as the formal deliverable.

### 3.2 Dashboard Independence Contract

The dashboard must be:

```text
standalone
offline-capable
self-contained
free of external CDN references
free of authentication scripts
free of external library dependencies
print-friendly
```

**Comment:** The corrected TEKOL dashboard confirms that embedded CSS and embedded JavaScript are sufficient. The prior Microsoft sign-in HTML is explicitly rejected as a non-dashboard artifact.

### 3.3 Dashboard Data Object Contract

Each criterion object must contain these fields:

```json
{
  "n": "I",
  "order": 1,
  "title": "Organization",
  "rating": "fully",
  "score": 1.00,
  "refs": "SP 4.1.1 §3.1–3.2; audit crumbs",
  "aff": "Evidence supporting conformance.",
  "con": "Evidence gaps or contrary points.",
  "judge": "Final criterion ruling.",
  "verify": "Auditor verification action."
}
```

Allowed `rating` values:

```text
fully
substantially
partially
minimally
unmet
undetermined
na
```

**Comment:** This schema maps directly to the corrected TEKOL dashboard behavior. It also aligns with the classification model from the evaluation method. [\[CodeInterpreter \| Undefined\]](https://eu-prod.asyncgw.teams.microsoft.com/v1/objects/0-neu-d14-4ebc0d42a6a8b615b4e17c3809f27a96/views/original/NQA_Supplier_Audit_Wiki_Session_Export.md)

### 3.4 Dashboard Section Contract

The HTML dashboard must include:

```text
header
top metric bar
executive summary section
classification distribution section
criterion card section
controls section
conformance matrix section
priority verification actions section
footer
```

### 3.5 Dashboard Feature Contract

The generated HTML must support:

```text
classification filters
text search
sort by criterion order
sort by highest risk first
sort by highest score first
expand all cards
collapse all cards
print view
```

**Comment:** These functions match the corrected TEKOL dashboard pattern and the TEKOL audit-session dashboard description. [\[35 Evaluat...and Report \| PDF\]](https://mynek-my.sharepoint.com/personal/rdolovcak_nek_si/Documents/Microsoft%20Copilot%20Chat%20Files/35%20Evaluation%20Method%20and%20Report.pdf)

***

# Revised GitHub-Issues Style Plan Sections

Only changed or expanded epics are listed below. All unchanged v1 epics remain valid.

***

## EPIC 2 — Machine-Readable Schema

### v2 Revision: Add Dashboard-Specific Schema

### What & Why

The dashboard must be generated from validated data. Therefore, `dashboard_schema.yml` must define the exact dashboard data contract. Schema-driven validation prevents drift between criterion evaluation pages, report output, and dashboard rendering.

### Revised Tasks

#### Task 2.5 — Create `dashboard_schema.yml`

The file must define:

```yaml
dashboard:
  required_sections:
    - header
    - topbar
    - executive_summary
    - classification_distribution
    - criterion_cards
    - controls
    - conformance_matrix
    - priority_verification_actions
    - footer

criterion_object:
  required_fields:
    - n
    - order
    - title
    - rating
    - score
    - refs
    - aff
    - con
    - judge
    - verify

rating_values:
  - fully
  - substantially
  - partially
  - minimally
  - unmet
  - undetermined
  - na

required_features:
  - classification_filter
  - search
  - sort_order
  - sort_risk
  - sort_score
  - expand_all
  - collapse_all
  - print_css

forbidden_patterns:
  - login.microsoftonline.com
  - aadcdn.msauth.net
  - aadcdn.msftauth.net
  - oauth
  - auth
  - signin
  - CDN script reference
```

**Comment:** The forbidden-pattern list blocks accidental use of login pages or captured authentication HTML.

### Revised Acceptance Criteria

* `dashboard_schema.yml` exists.
* The schema defines the criterion object fields used by the corrected TEKOL dashboard.
* The schema defines forbidden external authentication and CDN patterns.
* `validate_dashboard_data.py` loads the schema and rejects nonconforming dashboard data.

***

## EPIC 13 — Evaluation Report Generation

### v2 Revision: Add Dashboard-Report Consistency Contract

### What & Why

The Evaluation Report and Dashboard must be two views over the same evaluation data. The TEKOL example showed that the report and dashboard must agree on the score, classification distribution, gaps, and verification actions. [\[35 Evaluat...and Report \| PDF\]](https://mynek-my.sharepoint.com/personal/rdolovcak_nek_si/Documents/Microsoft%20Copilot%20Chat%20Files/35%20Evaluation%20Method%20and%20Report.pdf)

### Revised Tasks

#### Task 13.4 — Generate shared report/dashboard data package

The report generator must create:

```text
outputs/<supplier>_appendix_b_evaluation_data.json
```

This JSON object must contain:

```json
{
  "supplier": "",
  "overall_score": 0.0,
  "overall_classification": "",
  "criteria": [],
  "classification_counts": {},
  "top_gaps": [],
  "priority_verification_actions": []
}
```

**Comment:** The dashboard generator reads the same data package. This prevents separate report and dashboard logic from drifting.

### Revised Acceptance Criteria

* Evaluation Report and Dashboard use the same evaluation data package.
* Overall score in the report equals overall score in dashboard data.
* Classification counts in the report equal dashboard classification counts.
* Every priority verification action in the dashboard appears in the report or its supporting action pages.

***

## EPIC 14 — Dashboard Generation

### v2 Replacement Epic

### What & Why

The Dashboard is now a controlled static HTML deliverable. It must reproduce the corrected TEKOL dashboard pattern while staying supplier-neutral and generated from validated evaluation data. The prior TEKOL audit export established the expected dashboard content: score, classification distribution, cards, matrix, gaps, verification actions, and print/PDF support. [\[35 Evaluat...and Report \| PDF\]](https://mynek-my.sharepoint.com/personal/rdolovcak_nek_si/Documents/Microsoft%20Copilot%20Chat%20Files/35%20Evaluation%20Method%20and%20Report.pdf)

***

### Task 14.1 — Create `dashboard-template.html`

File:

```text
_shared/templates/dashboard-template.html
```

The template must contain placeholders for:

```text
supplier name
document set
overall score
weighted score
overall classification
criterion count
classification counts
executive summary
classification distribution
criterion data array
priority verification actions
footer
```

**Comment:** The template should follow the corrected TEKOL structure: header, metric bar, summary panel, distribution bar, controls, cards, matrix, verification actions, and footer.

#### Acceptance Criteria

* `dashboard-template.html` exists.
* The template uses embedded CSS.
* The template uses embedded JavaScript.
* No external CSS, JS, or font dependency exists.
* The template can render empty test data without runtime errors.

***

### Task 14.2 — Create dashboard data builder

File:

```text
_shared/scripts/build_dashboard_data.py
```

The script must read:

```text
manifests/evaluations.csv
wiki/criteria/*.md
wiki/findings/*.md
wiki/auditor-actions/*.md
outputs/<supplier>_appendix_b_evaluation_data.json
```

The script must produce:

```text
outputs/<supplier>_appendix_b_dashboard_data.json
```

Each criterion object must include:

```text
n
order
title
rating
score
refs
aff
con
judge
verify
```

**Comment:** The fields match the corrected TEKOL dashboard data array. `aff`, `con`, and `judge` may be generated from criterion evaluation pages. `verify` must come from auditor-action pages.

#### Acceptance Criteria

* The generated JSON contains exactly 18 criterion objects unless a formal scope exception is recorded.
* Every criterion object has all required fields.
* Every `rating` value is in the allowed dashboard vocabulary.
* Every `score` value is numeric and between 0 and 1.
* Every criterion has a `verify` field, even if the value is “No additional action required.”

***

### Task 14.3 — Create dashboard renderer

File:

```text
_shared/scripts/generate_dashboard.py
```

The renderer must:

1. Load `dashboard-template.html`.
2. Load `<supplier>_appendix_b_dashboard_data.json`.
3. Embed the data array into the HTML.
4. Render score metrics.
5. Render classification counts.
6. Render criterion cards.
7. Render matrix rows.
8. Render verification-action list.
9. Save the final dashboard.

Output files:

```text
wiki/dashboards/<supplier>_appendix_b_dashboard.html
outputs/<supplier>_appendix_b_dashboard.html
```

**Comment:** The final dashboard must be a static file that opens directly in a browser without server support.

#### Acceptance Criteria

* Dashboard HTML is generated without manual editing.
* Dashboard opens locally without internet.
* Criterion cards render all 18 criteria.
* Matrix contains all 18 criteria.
* Filters work for all rating types present in data.
* Search works across criterion, evidence, gap, and verification text.
* Sorting works by order, risk, and score.
* Expand/collapse controls work.
* Print view displays all card content.

***

### Task 14.4 — Create visual classification model

The dashboard CSS must include a consistent class for each rating:

```text
fully
substantially
partially
minimally
unmet
undetermined
na
```

Each class must have:

```text
text color
background color
badge style
distribution bar color
```

**Comment:** This supports quick visual risk scanning.

#### Acceptance Criteria

* Every rating class has a CSS rule.
* Every criterion badge uses the correct class.
* Classification distribution uses the same colors as badges.
* No missing or fallback rating class appears in the rendered HTML.

***

### Task 14.5 — Create dashboard validation script

File:

```text
_shared/scripts/validate_dashboard_data.py
```

The validator must check:

```text
dashboard data JSON exists
dashboard HTML exists
exactly 18 criterion objects exist
required fields exist on each criterion object
ratings are valid
scores are numeric
classification counts match criterion objects
overall score matches evaluations.csv
all criterion IDs are present once
HTML contains no external script references
HTML contains no external stylesheet references
HTML contains no login/authentication patterns
HTML contains required sections
HTML contains search/filter/sort controls
HTML contains conformance matrix
HTML contains priority verification actions
```

**Comment:** This validator prevents accidental use of non-dashboard HTML and ensures generated dashboards remain audit-ready.

#### Acceptance Criteria

* `validate_dashboard_data.py Company_X` returns PASS for a valid generated dashboard.
* The validator fails if `login.microsoftonline.com` or similar authentication content appears.
* The validator fails if an external CDN script or stylesheet appears.
* The validator fails if any criterion is missing.
* The validator fails if report score and dashboard score differ.

***

### Task 14.6 — Add dashboard regression fixture

Create:

```text
_shared/test_fixtures/dashboard/tekol_dashboard_fixture.json
_shared/test_fixtures/dashboard/tekol_dashboard_expected.html
```

The fixture should reflect the corrected TEKOL dashboard pattern:

```text
18 criteria
2 fully matched
12 substantially matched
4 partially matched
0 unmet
overall score 72.2%
classification: Substantially Matched
```

**Comment:** The corrected TEKOL dashboard uses a 72.2% score and a 13.0 / 18 weighted-unit display. This differs from the earlier session-export summary score of 83.3%. Both values should be preserved as separate historical artifacts. The v2 implementation treats the corrected HTML as the dashboard rendering benchmark, not as the universal scoring benchmark.

#### Acceptance Criteria

* Fixture data renders successfully.
* Rendered fixture contains 18 cards.
* Rendered fixture contains 18 matrix rows.
* Classification counts match fixture data.
* Overall score displays as 72.2% for the fixture.
* The fixture is used by dashboard generator tests.

***

## EPIC 15 — Validation Layer

### v2 Revision: Strengthen Dashboard Validation

### What & Why

Dashboard validation must verify both data and generated HTML. The previous v1 validation checked offline status and score match. The v2 validator must also check structure, controls, classification counts, forbidden content, and section presence.

### Revised Tasks

#### Task 15.6 — Add dashboard validator to `run_all_validations.py`

Validation order must include:

```text
validate_evaluation.py
validate_dashboard_data.py
```

`validate_dashboard_data.py` must run only from phase:

```text
dashboard_ready
```

or when dashboard files exist.

**Comment:** Dashboard validation depends on completed evaluations.

### Revised Acceptance Criteria

* `run_all_validations.py Company_X` includes dashboard validation.
* Dashboard validation is skipped with a clear message before dashboard generation.
* Dashboard validation becomes mandatory when `project-state.yml` has `phase: dashboard_ready`.
* Dashboard validation failures block commits tagged `[dashboard]`.

***

## EPIC 16 — Claude Code Slash Commands

### v2 Revision: Dashboard Command Contract

### What & Why

The `/nqa-dashboard` command must follow the new dashboard pipeline. It must not create a hand-written dashboard. It must call the data builder, renderer, and validator.

### Revised Task 16.2 — Update `/nqa-dashboard`

Command procedure:

```text
1. Read supplier project-state.yml.
2. Confirm evaluation phase is complete.
3. Run validate_evaluation.py.
4. Run build_dashboard_data.py.
5. Run generate_dashboard.py.
6. Run validate_dashboard_data.py.
7. Update wiki/dashboards index entry.
8. Append log.md entry.
9. Commit with [dashboard] tag if validation passes.
```

**Comment:** Dashboard generation becomes reproducible and auditable.

### Revised Acceptance Criteria

* `/nqa-dashboard` refuses to run before evaluation is complete.
* `/nqa-dashboard` produces dashboard data JSON and dashboard HTML.
* `/nqa-dashboard` runs dashboard validation.
* `/nqa-dashboard` appends a log entry.
* `/nqa-dashboard` creates a `[dashboard]` commit when validation passes.

***

## EPIC 20 — Supplier Run: TEKOL Regression Benchmark

### v2 Revision: Split Scoring Benchmark and Dashboard Rendering Benchmark

### What & Why

The earlier TEKOL audit-session export recorded an overall score of 83.3 / 100 and a classification of Substantially Matched.  The corrected TEKOL dashboard example displays 72.2%, 13.0 / 18 weighted units, 2 fully matched, 12 substantially matched, and 4 partially matched. These are not identical. Therefore, v2 separates two benchmark types: [\[35 Evaluat...and Report \| PDF\]](https://mynek-my.sharepoint.com/personal/rdolovcak_nek_si/Documents/Microsoft%20Copilot%20Chat%20Files/35%20Evaluation%20Method%20and%20Report.pdf)

```text
TEKOL scoring benchmark
TEKOL dashboard rendering benchmark
```

### Revised Tasks

#### Task 20.1 — Preserve TEKOL scoring benchmark

Benchmark data from the prior audit-session export:

```text
Overall score: 83.3 / 100
Overall classification: Substantially Matched
Fully Matched: 3
Substantially Matched: 11
Partially Matched: 4
Minimal / Unmet: 0
```

**Comment:** This benchmark tests evaluation reproduction when the same evidence basis is used. [\[35 Evaluat...and Report \| PDF\]](https://mynek-my.sharepoint.com/personal/rdolovcak_nek_si/Documents/Microsoft%20Copilot%20Chat%20Files/35%20Evaluation%20Method%20and%20Report.pdf)

#### Task 20.2 — Preserve TEKOL dashboard rendering benchmark

Benchmark data from the corrected dashboard example:

```text
Overall score: 72.2%
Weighted units: 13.0 / 18
Overall classification: Substantially Matched
Fully Matched: 2
Substantially Matched: 12
Partially Matched: 4
Unmet: 0
```

**Comment:** This benchmark tests dashboard layout, rendering, filtering, sorting, and static HTML behavior.

#### Task 20.3 — Add variance explanation rule

If scoring output and dashboard fixture output differ, the difference must be documented as:

```text
different source basis
different scoring model
different dashboard fixture
different historical export
manual correction
```

### Revised Acceptance Criteria

* TEKOL scoring benchmark and TEKOL dashboard rendering benchmark are stored separately.
* Dashboard tests do not overwrite scoring tests.
* Scoring tests do not require the dashboard fixture score to match 83.3%.
* Any TEKOL variance is recorded in a benchmark note.

***

# Revised Final Success Criteria — v2 Additions

The system is complete only when these additional dashboard criteria pass:

```text
[ ] dashboard_schema.yml defines required sections and criterion object fields.
[ ] dashboard-template.html exists and contains embedded CSS and JavaScript.
[ ] build_dashboard_data.py generates dashboard_data.json.
[ ] generate_dashboard.py creates standalone HTML.
[ ] validate_dashboard_data.py rejects external CDN, login, or authentication content.
[ ] Dashboard contains all 18 Appendix B criteria.
[ ] Dashboard score matches evaluation data for generated supplier runs.
[ ] Dashboard classification counts match criterion objects.
[ ] Dashboard filters, search, sorting, expand/collapse, and matrix render correctly.
[ ] Dashboard print view displays expanded audit content.
[ ] Corrected TEKOL dashboard fixture passes rendering tests.
[ ] Earlier TEKOL scoring benchmark remains preserved as a separate benchmark.
```

***

# Revised Core Dashboard Principle

The Dashboard is not a screenshot, browser capture, or manually edited web page. It is a generated audit interface over validated evidence data. A valid dashboard must be traceable to criterion evaluation pages, crumb-linked evidence, findings, and auditor verification actions. It must open offline and must contain no authentication artifacts, external scripts, or unsupported score values.
