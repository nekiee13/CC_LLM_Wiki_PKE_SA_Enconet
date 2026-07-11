# MASTER DEVELOPMENT PLAN v1.0 — NQA Supplier Audit Wiki (PKE-SA)

## 0. Document control

| Field | Value |
|---|---|
| Project | Project03 / PKE_SA_Enconet |
| Plan name | Master_development_plan |
| Version | 1.1 |
| Date | 2026-07-11 |
| Status | draft — awaiting human review |
| Author | Claude (from human-supplied context docs and draft upgrade plan) |
| Supersedes | docs/CC_PKE_NQA_Supplier_Audit_Wiki_Enconet_Upgrade_Plan.md (draft input) |

**Inputs this plan is grounded in:**

1. `docs/CC_PKE_NQA_Supplier_Audit_Wiki_Enconet_Upgrade_Plan.md` — draft upgrade plan (critique + EPIC sketch).
2. `docs/context/30 Ingestion phase.md` — dual-pipeline ingestion requirement.
3. `docs/context/31 Sieving - Crumb generation.md` — RULE / DOCUMENT transformation prompts, 18-criterion APP_B taxonomy.
4. `docs/context/32 Crumbs proccessing - json_extractor_session_exp.md` — existing JSON Extractor tool (flatten / filter / export / Streamlit).
5. `docs/context/35 Wiki output.md` — deliverables: Evaluation Report + Dashboard.
6. `docs/context/36 Evaluation Method and Report.md` — evaluation axiom (C/L/A/R/G/E), evidence constraint, 10 CFR 50 Appendix B text.
7. `docs/context/37 Audit_Session_Export Example.md` — illustrative audit-session export (example of the scoring method in action).
8. `docs/context/38 Dashboard example.md` — illustrative standalone HTML dashboard (example of the rendering contract).
9. `docs/context/40 MASTER PLAN - NQA Supplier Audit Wiki - v2.md` — dashboard as first-class generated deliverable; shared evaluation layer.
10. `docs/context/23 FINAL PROJECT FILL-IN.md` — original LLM-Wiki concept (Project01/Project02 heritage).

---

## 1. Mission and end state

**What.** Build, from scratch, a supplier-audit knowledge system that ingests raw supplier
QA documentation, converts it into traceable evidence, evaluates it criterion-by-criterion
against 10 CFR 50 Appendix B (as interpreted by ASME NQA-1), and generates two consistent,
validated deliverables: an **Evaluation Report** and a **standalone HTML Dashboard**.

**The etalon.** 10 CFR 50 Appendix B is the evaluation framework's reference standard. It
is a public document and is **always provided as a raw source** in every project instance
(registered, checksummed, immutable — same spine as supplier documents). It mandates 18
criteria, but **not every criterion applies to every company**: applicability is ruled per
supplier from its documented scope of activity (e.g. an installation-only supplier performs
no design work → Criterion III Design Control is not applicable), justified, and
human-approved before evaluation begins.

**Why.** An audit conclusion is only defensible when every score, gap, and recommendation
can be traced back to objective evidence in the supplier's own documents. A plain
LLM-maintained wiki cannot guarantee that. The end state is therefore a
**validated audit evidence compiler**: raw documents in, evidence-bounded deliverables out,
with machine validation at every joint.

**End state (Definition of Done for the whole project):**

- Full data spine implemented and validated (Section 3).
- All validators PASS via one aggregate runner.
- Both reference benchmarks reproduce (scoring fixture; dashboard rendering fixture).
- Evaluation Report and Dashboard generate from the **same** evaluation data package, and
  a score divergence anywhere fails validation.
- All human gates decided and recorded.
- First production supplier run (Enconet corpus) executable end-to-end.

---

## 2. Design principles

1. **Evidence-bounded evaluation.** Crumbs are grounded facts. Reasoning, inference, or
   interpretation never substitutes for evidence. A positive classification (Fully /
   Substantially) requires at least one supporting objective crumb (source: docs/context/36).
2. **One data spine, one truth.** Report and Dashboard read the same validated evaluation
   package. Divergence is a validation failure, never a footnote (source: docs/context/40).
3. **Contracts before code, code before outputs.** Machine-readable schemas (IDs, taxonomy,
   crumb JSON, scoring, dashboard) are defined first; generators come last.
4. **KISS task sizing.** Every task produces one artifact (one file, one script, one schema)
   and is completable in one working session. Many small tasks beat few complex ones.
5. **Raw is immutable.** `raw/` files are never modified after promotion. Checksums prove it.
6. **Generated, never hand-edited.** Report and Dashboard are compiler outputs. Manual edits
   to generated files are forbidden and detectable (regeneration + validation).
7. **Human gates own the state.** Claude does the work; the human approves phase advances.
   Gate artifacts are standalone, reviewed one supplier at a time, and at each decision
   point the human is offered concrete options with plain-language (ELI5) explanations.
8. **Heritage by copy, not by reference.** Proven patterns from Project01/Project02
   (validator suite, continuity triad, manifests, gate packets) are copied and adapted here.
   No cross-project wiki links.
9. **Supplier-agnostic engine.** Everything is parameterized by `<supplier>`. Enconet is
   the first production target; the same engine is reused for every future company
   evaluation. Context-doc examples are illustrative only — no example data is canon.
10. **Bilingual evidence, English analysis.** Original-language quotes are preserved
    verbatim; evaluation text is English; translations carry status flags.
11. **Applicability before evaluation.** The etalon's 18 criteria are assessed for
    applicability per supplier before any scoring: each criterion is ruled applicable or
    not-applicable from the supplier's documented scope of activity, with written
    justification and human approval. Not-applicable criteria stay visible in every output
    but never enter the score.
12. **Sieving is the crown activity — built for iteration.** Crumb quality bounds every
    downstream result, and sieving effectiveness will not be pinpointed on the first
    attempt. Therefore: prompts are versioned, sieve runs are generational (supersede,
    never overwrite), every run is measured, prompt versions are scored against a golden
    calibration set, and rollback is one recorded operation. Modifying the sieving prompt
    is a routine, low-risk act — the system is designed for frequent tuning.

---

## 3. The data spine (canonical)

**What.** The single ordered chain every fact travels along.
**Why.** Traceability drift between stages is the main project risk; naming the spine makes
every EPIC's position in it explicit.

```text
raw document
  → extracted text            (derived/)
  → semantic chunk            (DB: document_chunks)      [EPIC 4]
  → APP_B crumb + quotes      (DB: crumbs, crumb_quotes) [EPIC 5]
  → chunk↔crumb link          (DB: crumb_chunk_links)    [EPIC 6]
  → requirement registry      (DB: requirements)         [EPIC 7]
  → applicability ruling      (DB: criterion_applicability) [EPIC 8]
  → criterion evaluation      (DB: criterion_evaluations)[EPIC 8]
  → gaps / findings / actions (DB: gaps, findings,
                               auditor_actions)          [EPIC 9, 10]
  → evaluation data package   (outputs/*.json)           [EPIC 8]
  → evaluation report         (outputs/*.md)             [EPIC 11]
  → dashboard data + HTML     (outputs/*.html/.json)     [EPIC 12]
```

---

## 4. Target directory layout

**What.** The full project tree this plan builds.
**Why.** From-scratch development needs an agreed skeleton before the first task starts;
this layout extends the workspace-standard wiki layout (raw/wiki/manifests/templates/
scripts) with the audit-specific layers (db/, prompts/, schemas/, outputs/, benchmarks/).

```text
PKE_SA_Enconet/
├── CLAUDE.md                  ← project control schema (EPIC 0)
├── MASTER_DEVELOPMENT_PLAN.md ← this file
├── project-state.yml          ← phase + gate state (EPIC 0 / 14)
├── docs/                      ← human-prepared context (read-only by convention)
├── incoming/                  ← capture staging (mutable)
├── raw/                       ← promoted sources (IMMUTABLE)
├── derived/                   ← extracted text (locked after extraction)
├── db/                        ← nqa_audit.sqlite + schema.sql
├── schemas/                   ← machine-readable contracts (yml)
├── sieving/                   ← SIEVING SUBSYSTEM — one location for all sieving work
│   ├── src/json_extractor/    ← crumb pipeline code (validate / flatten / query / export)
│   ├── prompts/               ← versioned prompts + fixtures + CHANGELOG (EPIC 5/18)
│   ├── SIEVING_PLAYBOOK.md    ← single entry point for all sieving work
│   ├── DATA/                  ← example crumb JSONs (fixture source)
│   ├── tests/  tools/
│   └── PROVENANCE.md          ← upstream origin (opencode-JSON) + commit record
├── scripts/                   ← pipeline + validators + generators
├── wiki/                      ← LLM-maintained knowledge pages
│   ├── index.md / log.md / current-status.md
│   ├── criteria/              ← 18 criterion evaluation pages
│   ├── evidence/              ← chunk-linked evidence pages
│   ├── findings/  actions/    ← finding + auditor action pages
│   └── dashboards/            ← generated dashboard copies
├── manifests/                 ← CSV control files
├── templates/                 ← page + report + dashboard templates
├── benchmarks/                ← reference fixtures + benchmark policy
├── .claude/                   ← commands (EPIC 17) + sieving skills (Task 18.7)
└── outputs/                   ← generated deliverables per supplier
```

---

## 5. Roles and human gates

**What.** Who does what, and where work stops for approval.
**Why.** Audit conclusions affect formal deliverables; unreviewed material must never flow
into them. Gates are the project's brake system, mirrored from Project02 and made stricter.

| Role | Responsibility |
|---|---|
| Human (auditor/owner) | Supplies raw documents, decides every gate, approves findings, owns final deliverables |
| Claude (executor) | Builds the system, runs pipelines, drafts evaluations/findings, generates deliverables, never advances a phase on its own |

**Gates (each recorded as a decision row in `manifests/approvals.csv` + a gate packet):**

| Gate | After state | What the human approves |
|---|---|---|
| G1 Registry | registered | Documents registered, checksums, metadata correct |
| G2 Evidence | evidence_reviewed | Chunks, crumbs, and links faithful to sources; criterion applicability matrix approved |
| G3 Evaluation | evaluated | Criterion classifications and scores are justified |
| G4 Findings | findings_approved | Findings + auditor actions approved (draft → approved) |
| G5 Report | report_ready | Evaluation Report released |
| G6 Dashboard | dashboard_ready | Dashboard released |
| G7 Closeout | closed | Audit closed; benchmarks and logs archived |

---

## 6. Epic map and implementation order

**What.** 18 epics, ordered so that traceability and validation exist before any polished
output. **Why.** Generating reports or dashboards from unvalidated evidence is the main
failure mode this order prevents (source: draft plan §4).

| # | Epic | Goal (one line) | Depends on |
|---|---|---|---|
| 0 | Project scaffold & governance | Working project skeleton + rules | — |
| 1 | Machine-readable contracts | All schemas/vocabularies exist | 0 |
| 2 | Controlled data backbone | SQLite spine with enforced integrity | 1 |
| 3 | Raw intake & document registry | Immutable, registered, checksummed sources | 2 |
| 4 | Chunking pipeline (ingestion 1) | Reviewable source units in DB | 3 |
| 5 | Sieving pipeline (ingestion 2) | Valid APP_B crumbs in DB | 3 |
| 6 | Chunk↔crumb traceability | Every crumb provably rooted in a chunk | 4, 5 |
| 7 | Requirement registry | 18 criteria decomposed into requirement records | 5 |
| 8 | Evaluation engine | Evidence-gated scores + one evaluation package | 6, 7 |
| 9 | Evidence matrix & gap model | Coverage matrix + classified gaps | 8 |
| 10 | Findings & auditor actions | Approval-controlled findings/actions | 9 |
| 11 | Evaluation Report generator | Report generated from the package | 8–10 |
| 12 | Dashboard generator | Standalone HTML generated from the package | 8–10 |
| 13 | Validation layer & runner | One command validates everything | 1–12 (incremental) |
| 14 | Audit state machine & gates | Enforced phases + recorded human decisions | 13 |
| 15 | Sieving subsystem integration | Vendored sieving code wired, pinned, drift-guarded | 5 |
| 16 | Reference benchmark fixtures | Regression anchors for scoring + rendering | 8, 12 |
| 17 | Claude Code commands | One slash command per pipeline stage | 14 |
| 18 | Sieving iteration & tuning harness | Measured, reversible sieving tuning loop | 5, 6 |

**Execution notes.**
- EPIC 13 is cross-cutting: every epic ships its own validator as one of its tasks; EPIC 13
  only aggregates them. This keeps each validator small (KISS).
- EPIC 16 fixtures may be written earlier (as soon as EPIC 8 / EPIC 12 interfaces exist) to
  drive test-first development; they are listed late only because they *gate* release.
- EPIC 15 can run in parallel after EPIC 5.
- **EPIC 18 is built immediately after EPIC 6** (its metrics need the chunk-link
  verification rate) and stays in continuous use for the rest of the project: sieving
  tuning is expected routine work, not an exception. Despite its number, it is early
  infrastructure — treat the order as 0 → 1 → 2 → 3 → 4 → 5 → 6 → **18** → 7 → 8 → …

---

# EPICS

---

## EPIC 0 — Project scaffold and governance

**Labels:** `epic`, `scaffold`, `governance`, `must-have`
**Goal:** A working, git-tracked project skeleton with control rules, continuity files, and
manifests — the frame every later epic hangs on.
**Why:** The repository currently contains only `docs/`. Without the scaffold, the
workspace-standard rules (immutable raw, wiki-first, log/index discipline) have nothing to
operate on.

### Task 0.1 — Create directory skeleton

**What:** Create every directory from Section 4 with `.gitkeep` placeholders.
**Why:** All later tasks reference fixed paths; creating them once prevents path drift.
**Deliverable:** directory tree per Section 4.

- [ ] All Section 4 directories exist.
- [ ] Empty directories contain `.gitkeep`.
- [ ] `git status` shows the tree tracked.

### Task 0.2 — Write project CLAUDE.md

**What:** Project control schema: identity, mission, directory layout, core rules, session
start/end protocol, command reference, commit convention.
**Why:** This file is what future sessions load first; it encodes the non-negotiables
(evidence-bounded evaluation, raw immutability, gate discipline) at the point of use.
**Deliverable:** `Enconet/CLAUDE.md`, extending the shared
`03_PKE_SA_NQA1/CLAUDE.md` workspace contract.

- [ ] Extends workspace commons (`../CLAUDE.md`); project rules may specialize but may not weaken
      workspace evidence, safety, record-integrity, or validation rules.
- [ ] Core rules include: raw immutable, wiki-first, index+log after every write,
      evidence constraint, no phase advance without gate, generated files never hand-edited.
- [ ] Skills rule: reusable skills live at `../.claude/skills/`; Enconet-specific skills live at
      `.claude/skills/`. The matching skill is mandatory reading before its activity (Task 18.7).
- [ ] Session start protocol: CLAUDE.md → wiki/current-status.md → wiki/index.md →
      project-state.yml → one-paragraph state summary.
- [ ] Session end protocol: run validations and invoke the shared `/handoff` skill (Task 0.7),
      which updates continuity records through the controlled publication flow.

### Task 0.3 — Create wiki continuity triad

**What:** `wiki/index.md`, `wiki/log.md` (append-only), `wiki/current-status.md`.
**Why:** These three files are the project's memory between sessions; every workspace
project uses the same triad, so tooling and habits transfer.
**Deliverable:** three seed files.

- [ ] index.md lists page sections (criteria / evidence / findings / actions / dashboards).
- [ ] log.md seeded with a creation entry and marked append-only.
- [ ] current-status.md contains phase, last action, next action.

### Task 0.4 — Seed manifests

**What:** Create empty CSV manifests with headers: `raw_sources.csv`, `ingest_runs.csv`,
`validation_runs.csv`, `approvals.csv`, `link_exceptions.csv`.
**Why:** Manifests are the human-scannable control ledgers; fixing their headers now defines
the audit trail format before any data flows.
**Deliverable:** `manifests/*.csv`.

- [ ] Each CSV exists with documented header row.
- [ ] `approvals.csv` header: object_id, decision, date, reviewer, notes.
- [ ] Headers documented in CLAUDE.md command reference.

### Task 0.5 — Create project-state.yml

**What:** Machine-readable project state: `phase`, `supplier`, `gates` (G1–G7 with
status/date/decision-ref), `benchmarks_locked`.
**Why:** Validator strictness and slash commands key off one authoritative state file
(Project02 pattern); it prevents "which phase are we in?" ambiguity.
**Deliverable:** `project-state.yml`.

- [ ] Contains phase enum value from EPIC 14 state list (initial: `registered` pre-state `setup`).
- [ ] Gates G1–G7 present, all `pending`.
- [ ] YAML parses; schema documented inline as comments.

### Task 0.6 — Git hygiene

**What:** `.gitignore` (DB journals, __pycache__, .obsidian workspace noise), commit
message convention (`[scaffold] …`, `[schema] …`, `[ingest] …`, `[eval] …`, `[report] …`,
`[dashboard] …`, `[gate] …`, `[fix] …`).
**Why:** A predictable commit vocabulary makes the git log a readable audit trail — same
convention family as Project01/02.
**Deliverable:** `.gitignore`, convention section in CLAUDE.md.

- [ ] `.gitignore` present; `db/*.sqlite-journal`, caches, workspace files ignored.
- [ ] Commit convention documented with one example per tag.

### Task 0.7 — Implement and integrate the shared `/handoff` skill

**What:** Create `03_PKE_SA_NQA1/.claude/skills/handoff/SKILL.md` as the shared,
project-neutral session bridge. It creates an immutable timestamped handoff record under the
active project and refreshes a validated `HANDOFF.md` convenience pointer. Enconet configuration
may extend the shared skill but must not fork its record contract.

**Why:** `current-status.md`, `index.md`, `log.md`, and `project-state.yml` are necessary but can
drift when updated manually. A handoff must capture one coherent, evidence-backed snapshot so a
new session can resume without rereading historical context or assuming that unrun tests passed.

**Required handoff content:**

- workspace/project roots, project ID, UTC timestamp, and agent/author;
- Git repository root, branch, HEAD, upstream, and worktree status;
- objective, phase, completed work, decisions/ADR links, blockers, and risks;
- validation commands, exit codes, and explicit `passed` / `failed` / `not-run` / `unknown` states;
- jmunch code/doc index identities, source roots, timestamps, and integrity/staleness state;
- exact next action and ordered follow-up tasks;
- uncommitted and generated artifacts that the next session must review.

**Implementation and integration:**

- [ ] Define a machine-validatable frontmatter or sidecar schema and Markdown template.
- [ ] Publish first to `handoffs/YYYY-MM-DDTHHMMSSZ-<short-sha>.md`; historical records are
      immutable. Replace `HANDOFF.md` atomically only after schema/consistency checks pass.
- [ ] Append one `handoff-created` event to `wiki/log.md`; never rewrite earlier log entries.
- [ ] Read Git, project state, current status, recent logs, open decisions, validation results,
      and jmunch metadata through read-only probes. Missing Git/indexes are explicit failures or unknowns.
- [ ] Add `/handoff` to shared/project CLAUDE session-end protocols, `/audit-close`, and the
      aggregate runner. Session start compares the latest immutable record, `HANDOFF.md`, Git HEAD,
      current status, and project state and reports drift.
- [ ] Add golden-file, dirty-worktree, detached-HEAD, no-Git, stale-index, failed-test,
      Unicode-path, repeat-run, and interrupted-write tests.
- [ ] Prohibit secrets, full environment dumps, raw controlled evidence, and unsupported claims.

**Acceptance criteria:**

- [ ] A new session can state phase, completed work, failed/not-run checks, blockers, and next
      action from the handoff without reading the complete context archive.
- [ ] Re-running `/handoff` creates a new immutable record and never edits an earlier record.
- [ ] Partial collection/validation failure cannot publish a record that appears complete; the
      command returns non-zero with actionable diagnostics.
- [ ] The same shared skill passes against Enconet and a fixture second project without source edits.
- [ ] Git history plus optional manifest hashes makes prior handoff/log tampering detectable.

---

## EPIC 1 — Machine-readable contracts (schemas and vocabularies)

**Labels:** `epic`, `schema`, `contracts`, `must-have`
**Goal:** Every enum, ID pattern, field list, and threshold the system uses exists as a
versioned YAML contract before any code consumes it.
**Why:** Prompt discipline alone cannot protect audit data. When contracts are files, every
validator, generator, and prompt reads the *same* definition, and drift becomes detectable.

### Task 1.1 — APP_B taxonomy contract

**What:** `schemas/app_b_taxonomy.yml` — the 18 Appendix B criteria as canonical
`criterion_id` / `criterion_name` pairs (APP_B_I Organization … APP_B_XVIII Audits).
**Why:** The taxonomy is fixed by regulation; hard-coding it once prevents classification
drift across prompts, DB, evaluations, and dashboard (source: docs/context/31).

- [ ] Exactly 18 entries; IDs `APP_B_I` … `APP_B_XVIII`.
- [ ] Names verified against the official public text of Appendix B (eCFR / NRC).
- [ ] Names match the sieving prompt exactly.
- [ ] Each entry has a short English description.
- [ ] File is the single source: no other file re-declares the pairs.
- [ ] Taxonomy is fixed by regulation; applicability is a per-supplier ruling (EPIC 8),
      never an edit to this file.

### Task 1.2 — ID grammar contract

**What:** `schemas/id_patterns.yml` — one anchored regex per object type.
**Why:** Traceability requires predictable IDs; regex validation makes malformed IDs a
hard failure instead of silent corruption.

```text
DOC-0001
CHUNK-DOC-0001-0001
QUOTE-DOC-0001-0001-01
CRUMB-DOC-0001-APP_B_IV-0001
REQ-APP_B_IV-01
EVAL-APP_B_IV
GAP-APP_B_IV-01
FIND-0001
ACT-0001
RUN-20260704-01
DASH-20260704-0001
```

- [ ] One anchored regex per pattern above.
- [ ] Duplicate ID = validation failure (checked in EPIC 2 DB and EPIC 13 validators).
- [ ] Invalid format = validation failure with the offending ID reported.

### Task 1.3 — Controlled vocabularies

**What:** `schemas/vocabularies.yml` — every enum in one file:
ratings (`fully, substantially, partially, minimally, unmet, undetermined, na`),
gap statuses (`covered, mostly-covered, partially-covered, minimally-covered, not-covered,
not-applicable, undetermined, missing-evidence`),
action types (`verification, document_request, sample_test, interview`),
translation statuses (`original, machine, reviewed, meaning-flagged`),
document sides (`RULE, DOCUMENT`), source rules (`10CFR50_APPB, 10CFR21`),
audit states (EPIC 14 list).
**Why:** Enums scattered across scripts rot independently; one vocabulary file keeps
validators, prompts, and generators in lock-step.

- [ ] All seven vocabularies present, values exactly as listed.
- [ ] Each vocabulary has a one-line usage note.
- [ ] Validators load enums from this file, never inline.

### Task 1.4 — APP_B crumb JSON contract

**What:** `schemas/app_b_json_schema.yml` — required document fields, required item fields,
allowed item_types, RULE-object fields, DOCUMENT-side rule-reference rules, evidence-quote
requirements, and multilingual fields (`quote_original`, `quote_language`, `statement_en`,
`translation_status`).
**Why:** The sieving prompt distinguishes repo-enforced from template-required fields; for
audit data every audit-critical field must become code-enforced, and the schema is where
that promotion happens (source: docs/context/31).

- [ ] Required document fields defined (name, date, side, source_rules).
- [ ] Required item fields defined (item_id, criterion, statement, evidence_quotes, source).
- [ ] RULE runs: `SOURCE_RULES` required, one of the source-rules vocabulary.
- [ ] DOCUMENT runs: `SOURCE_RULES` must be null; RULE-only objects forbidden.
- [ ] Multilingual fields defined with translation-status enum.
- [ ] `strict` and `warning` enforcement tiers marked per field.

### Task 1.5 — Canonical scoring model

**What:** `schemas/scoring_model.yml` — rating weights, score formula, rounding rules,
classification thresholds, consolidated-score definition.
**Why:** The context examples show that a scoring result and a dashboard rendering can
legitimately carry different values when their bases differ. Every supplier run needs
exactly one canonical score logic, chosen once, versioned, and approved by the human
(source: docs/context/37, 38).

- [ ] Weight per rating value defined.
- [ ] Consolidated score formula and rounding rule defined.
- [ ] N/A handling defined: not-applicable criteria are excluded from the consolidated
      score; the denominator is the applicable-criteria count.
- [ ] Classification thresholds defined (score → rating class).
- [ ] Version field + change note section present.
- [ ] Marked `pending human calibration approval` until Gate G3 first passes.

### Task 1.6 — Dashboard data contract

**What:** `schemas/dashboard_schema.yml` — required criterion object (`n, order, title,
rating, score, refs, aff, con, judge, verify`), required top-level metrics, forbidden
patterns (`login.microsoftonline.com`, `oauth`, `signin`, CDN/external references).
**Why:** The dashboard is generated audit software; its input contract must be machine-
checkable so a rendering never silently diverges from evaluation data (source: docs/context/40).

- [ ] Criterion object fields defined exactly as v2 contract.
- [ ] Rating values reference vocabularies.yml.
- [ ] Top-level metrics defined (weighted score, classification counts, supplier, date).
- [ ] Forbidden-pattern list present.

### Task 1.7 — Wiki page contract

**What:** `schemas/page_types.yml` + `schemas/required_fields.yml` — frontmatter contract
for page types: criterion-evaluation, evidence, finding, action, gate-decision.
**Why:** Wiki pages are the human-readable projection of DB records; a frontmatter contract
lets validators check pages the same way they check rows (Project02 pattern, adapted).

- [ ] Five page types defined with required frontmatter fields.
- [ ] Every page type requires: id, type, status, content_origin, source citation.
- [ ] `n-a` accepted for structurally-required but semantically-empty fields.

---

## EPIC 2 — Controlled data backbone (SQLite)

**Labels:** `epic`, `database`, `traceability`, `must-have`
**Goal:** One SQLite database whose schema enforces the data spine's integrity (unique IDs,
foreign keys, no orphan evidence).
**Why:** Ad-hoc JSON and CSV drift is how traceability dies. A declared schema with enforced
foreign keys makes broken links a write-time error instead of a review-time surprise.

### Task 2.1 — Write DDL schema

**What:** `db/schema.sql` with tables: `documents`, `document_chunks`, `crumbs`,
`crumb_sources`, `crumb_quotes`, `crumb_chunk_links`, `requirements`,
`criterion_applicability`, `criterion_evaluations`, `gaps`, `findings`, `auditor_actions`,
`sieve_runs`, `evaluation_runs`, `dashboard_runs`, `validation_runs`.
**Why:** The draft's `rule_items`/`document_items` split is folded into `crumbs.document_side`
(one table, one enum column) — simpler, and side-leakage is checkable by constraint.
`crumb_sources` and `crumb_quotes` are separate tables so **all** sources and quotes survive
flattening, not just the first.

- [ ] All 16 tables defined with typed columns and PKs.
- [ ] FKs: chunks→documents, crumbs→documents, crumbs→sieve_runs,
      quotes/sources→crumbs, links→(crumbs, chunks),
      applicability→(criteria, evaluation run), evaluations→criteria, gaps→evaluations,
      findings→(criteria, evidence), actions→findings-or-gaps.
- [ ] UNIQUE on `documents.doc_id`, `document_chunks.chunk_id`, `crumbs.item_id`.
- [ ] CHECK constraints use vocabulary enums (rating, side, gap status, action type).

### Task 2.2 — Database initializer

**What:** `scripts/init_db.py` — creates `db/nqa_audit.sqlite` from `schema.sql`,
enables foreign keys, idempotent (refuses to clobber an existing non-empty DB).
**Why:** Reproducible initialization means the DB can always be rebuilt from raw + scripts —
the DB is a derived artifact, never the only copy of anything.

- [ ] Creates DB with `PRAGMA foreign_keys = ON` verified.
- [ ] Running twice does not destroy data (explicit `--reset` flag required).
- [ ] Exit code non-zero on failure.

### Task 2.3 — DB access helper

**What:** `scripts/db_util.py` — single connection helper (FK pragma, row factory),
insert-with-ID-validation, exists/lookup helpers.
**Why:** Every pipeline script uses the same 5 operations; one helper prevents ten slightly
different SQLite dialects (KISS + single source of truth).

- [ ] `connect()` always enables FK enforcement.
- [ ] `insert()` validates IDs against `id_patterns.yml` before writing.
- [ ] Duplicate-ID insert raises a clear error naming the ID.

---

## EPIC 3 — Raw intake and document registry

**Labels:** `epic`, `ingestion`, `provenance`, `must-have`
**Goal:** Every source document is immutable, checksummed, registered in DB + manifest, and
has extracted text in `derived/`.
**Why:** The spine starts here: if raw provenance is weak, everything downstream inherits
the weakness. Checksums let any later stage prove it worked on the exact registered bytes.

### Task 3.1 — Intake and promotion procedure

**What:** Documented flow: file lands in `incoming/` → human reviews → promote to `raw/`
(move + write-lock via chmod) — procedure written in CLAUDE.md, executed manually or via
`scripts/promote_source.py`.
**Why:** A single controlled doorway into `raw/` is what makes the immutability rule real.

- [ ] `promote_source.py` moves file, strips write permission, appends `manifests/raw_sources.csv`.
- [ ] Promotion of a duplicate filename fails.
- [ ] Procedure documented (incl. re-lock command) in CLAUDE.md.

### Task 3.2 — Document registration

**What:** `scripts/register_document.py` — assigns `DOC-nnnn`, computes SHA-256, records
metadata (filename, title, supplier, doc_date, language, side hint) into `documents` + manifest.
**Why:** `doc_id` + checksum is the anchor every chunk, crumb, and quote points back to.

- [ ] `doc_id` allocated sequentially, matches ID grammar.
- [ ] SHA-256 stored; re-registration of same checksum is rejected.
- [ ] Row appears in both DB and `raw_sources.csv` (values identical).

### Task 3.3 — Text extraction to derived/

**What:** `scripts/extract_text.py` — extracts plain text (per document type) into
`derived/DOC-nnnn.txt`, records extraction method + date.
**Why:** Chunking and sieving need clean text; freezing it in `derived/` makes extraction a
reproducible, inspectable step instead of an invisible preprocessing detail.

- [ ] Output file named by doc_id.
- [ ] Extraction method recorded in DB.
- [ ] Empty extraction output fails with a clear error.

### Task 3.4 — Raw immutability validator

**What:** `scripts/validate_raw_sources.py` — verifies `raw/` file checksums against the
registry and confirms write-locks.
**Why:** Immutability is a claim; this validator is the proof, run on every validation pass.

- [ ] Checksum mismatch → FAIL naming the file.
- [ ] Unregistered file in `raw/` → FAIL.
- [ ] Registered file missing from `raw/` → FAIL.

---

## EPIC 4 — Chunking pipeline (ingestion 1)

**Labels:** `epic`, `ingestion`, `chunks`, `must-have`
**Goal:** Every registered document is split into chapter / sub-chapter chunks stored in the
DB with heading path, text, and metadata.
**Why:** Audit review needs paragraph-level source access ("show me where the supplier says
that"). Chunks are the reviewable source units the evidence layer links back to
(source: docs/context/30).

### Task 4.1 — Heading parser

**What:** `scripts/chunk_document.py` (parser part) — detects chapter (`1.`) and
sub-chapter (`1.1`) boundaries; third-level (`1.1.1`) stays inside its parent chunk.
**Why:** Chapter/sub-chapter granularity is the agreed size balance: small enough to review,
large enough to preserve context (source: docs/context/30).

- [ ] Level-1 and level-2 headings produce chunks; level-3+ does not (unless configured).
- [ ] Heading path recorded (e.g. `3 > 3.2`).
- [ ] Documents without numeric headings fall back to a documented rule (whole-doc chunk + warning).

### Task 4.2 — Chunk writer

**What:** Writer part of `chunk_document.py` — inserts chunks with `chunk_id`
(`CHUNK-DOC-nnnn-mmmm`), text, char offsets, source checksum reference.
**Why:** Offsets + checksum make every chunk independently verifiable against `derived/` text.

- [ ] `chunk_id` matches grammar; sequential per document.
- [ ] Char start/end stored; slicing `derived/` text by offsets reproduces chunk text.
- [ ] Re-chunking a document replaces its chunks atomically (no mixed generations).

### Task 4.3 — Chunk quality rules

**What:** Rejection rules inside the pipeline: empty chunks rejected; over-size chunks
flagged for manual split; duplicate heading paths flagged.
**Why:** Bad chunks poison sieving and review downstream; cheap rules here save expensive
confusion later.

- [ ] Empty chunk → pipeline error (not silent skip).
- [ ] Chunk size bounds configurable; violations logged as warnings.
- [ ] Summary printed per run: chunks created / warnings / rejections.

### Task 4.4 — Chunk validator

**What:** `scripts/validate_chunks.py` — every chunk belongs to a registered document,
IDs valid, offsets consistent, no empty text.
**Why:** The pipeline checks at write time; the validator re-proves it at any later time
(defense in depth, same pattern as all spine validators).

- [ ] Orphan chunk (no document) → FAIL.
- [ ] Offset slice mismatch → FAIL.
- [ ] PASS/FAIL summary row appended to `validation_runs.csv`.

---

## EPIC 5 — Sieving pipeline (ingestion 2 — APP_B crumbs)

**Labels:** `epic`, `ingestion`, `crumbs`, `app-b`, `must-have`
**Goal:** Versioned RULE / DOCUMENT prompts produce APP_B crumb JSON that is validated
against the contract and imported into the DB with all sources, quotes, and language fields.
**Why:** Crumbs are the structured evidence layer the whole evaluation stands on
(source: docs/context/31). The import path — not the prompt — is where quality is enforced.

### Task 5.1 — Versioned sieving prompts

**What:** `sieving/prompts/appb_rule_v1.md` and `sieving/prompts/appb_document_v1.md` — the transformation
prompts from docs/context/31, cleaned and versioned; DOCUMENT prompt uses
`DOCUMENT_SIDE: "DOCUMENT"` and `SOURCE_RULES: null` (correcting the known placeholder defect).
**Why:** Prompts are production artifacts; versioning + fixtures make prompt changes as
controlled as code changes.

- [ ] Both prompts stored, version-suffixed, referencing schemas by name.
- [ ] DOCUMENT prompt placeholder block is correct (side enum exact, SOURCE_RULES null).
- [ ] Prompt header states which schema version it targets.

### Task 5.2 — Run-context guard

**What:** `scripts/sieve_run.py` (context part) — run setup requires `DOCUMENT_SIDE` enum;
RULE runs require valid `SOURCE_RULES`; DOCUMENT runs forbid it.
**Why:** Side mixing (RULE material processed as DOCUMENT or vice versa) silently corrupts
the evidence base; the guard makes it impossible to start a mislabeled run.

- [ ] Invalid side → refuse to run.
- [ ] RULE without SOURCE_RULES → refuse; DOCUMENT with SOURCE_RULES → refuse.
- [ ] Run recorded in `sieve_runs` with RUN-id, prompt version, side, source doc.

### Task 5.3 — Crumb JSON validator

**What:** `scripts/validate_app_b_json.py` — validates sieving output against
`app_b_json_schema.yml` before import.
**Why:** Invalid JSON must be blocked at the door; once inside the DB it becomes "evidence".

- [ ] Missing document block / items → FAIL.
- [ ] Empty statement, empty evidence_quotes, empty source → FAIL.
- [ ] Unknown criterion pair → FAIL (against taxonomy contract).
- [ ] RULE/DOCUMENT side leakage → FAIL.
- [ ] Warning-tier fields report warnings without blocking (strict mode flag flips them to FAIL).

### Task 5.4 — Crumb importer

**What:** `scripts/import_crumbs.py` — imports validated JSON: crumbs + **all** sources into
`crumb_sources` + **all** quotes into `crumb_quotes`; assigns `CRUMB-…` IDs.
**Why:** First-source-only flattening loses secondary evidence; the importer preserves
everything, and scalar projections remain available for tables (source: docs/context/32).

- [ ] Every source object lands in `crumb_sources` (count matches input).
- [ ] Every quote lands in `crumb_quotes` (count matches input).
- [ ] Every crumb records the sieve RUN-id (and thus the prompt version) that produced it.
- [ ] Import is transactional: any failure rolls back the whole file.
- [ ] Import refuses files that did not pass Task 5.3 validation.

### Task 5.5 — Multilingual evidence fields

**What:** Importer + schema support for `quote_original`, `quote_language`, `statement_en`,
`translation_status`, `meaning_flag`.
**Why:** Evidence is Slovenian/English mixed; the original quote is the legal fact, the
English statement is the working text — both must exist, with translation risk flagged
for human review.

- [ ] Original quote always stored verbatim.
- [ ] `translation_status` from vocabulary; `meaning-flagged` rows listed for review.
- [ ] No English-only storage of a non-English quote is possible.

### Task 5.6 — Prompt fixture tests

**What:** `sieving/prompts/fixtures/` — one valid RULE fixture, one valid DOCUMENT fixture, one
malformed-placeholder fixture; a small runner asserts pass/pass/fail through Task 5.3.
**Why:** The placeholder defect class must never recur; fixtures turn that lesson into a
permanent regression test.

- [ ] RULE fixture passes validation.
- [ ] DOCUMENT fixture passes (side DOCUMENT, SOURCE_RULES null).
- [ ] Malformed fixture fails with the expected error.

---

## EPIC 6 — Chunk↔crumb traceability

**Labels:** `epic`, `traceability`, `must-have`
**Goal:** Every crumb is provably rooted in at least one chunk, or carries an approved,
documented exception.
**Why:** This is the join the whole system was missing a precise model for: a crumb citing
only a filename or page is weak evidence. `doc_id + chunk_id + quote-in-chunk verification`
makes source review strong (source: docs/context/30, draft plan).

### Task 6.1 — Link model and linking pass

**What:** `scripts/link_crumbs.py` — for each crumb quote, locate the containing chunk
(normalized text search within the same document); write `crumb_chunk_links`.
**Why:** Automatic linking does the bulk work; humans only handle the exceptions.

- [ ] Each crumb ends with ≥1 chunk link or an exception candidate.
- [ ] Link rows store crumb_id, chunk_id, quote_id, match method.
- [ ] Unmatched quotes exported as an exception-candidate list.

### Task 6.2 — Exception register

**What:** `manifests/link_exceptions.csv` — human-approved exceptions (quote not literally
in chunk text: e.g. table extraction, OCR variance) with reason and approval.
**Why:** Real documents produce legitimate mismatches; an explicit register keeps them
visible and bounded instead of silently tolerated.

- [ ] Each exception: crumb_id, quote_id, reason, approved_by, date.
- [ ] Unapproved exceptions count as broken links in validation.

### Task 6.3 — Traceability validator

**What:** `scripts/validate_traceability.py` — the spine check: crumb→chunk links resolve,
quote text appears in linked chunk (or approved exception), chunk→document→checksum chain
intact, no orphans anywhere.
**Why:** This validator *is* the traceability invariant; if it passes, every quote in every
deliverable can be walked back to immutable bytes.

- [ ] Crumb without link/exception → FAIL.
- [ ] Quote not found in linked chunk and not excepted → FAIL.
- [ ] Orphan links (dangling crumb_id/chunk_id) → FAIL.
- [ ] PASS/FAIL appended to `validation_runs.csv`.

---

## EPIC 7 — Requirement registry (RULE side)

**Labels:** `epic`, `requirements`, `rule-side`, `must-have`
**Goal:** All 18 Appendix B criteria decomposed into stable requirement records, each linked
to its RULE crumbs.
**Why:** The evaluation method demands requirement-by-requirement comparison; that needs a
controlled requirement list, not ad-hoc re-reading of the regulation each run
(source: docs/context/36).

### Task 7.1 — Ingest Appendix B as RULE run

**What:** Run the RULE pipeline (EPICs 3–5) over the Appendix B text (from
docs/context/36) as the first RULE document.
**Why:** The regulation goes through the same controlled spine as supplier documents —
one pipeline, no special cases, and it doubles as the pipeline's first integration test.

- [ ] Appendix B registered as DOC with side RULE, SOURCE_RULES `10CFR50_APPB`.
- [ ] The etalon is a permanent raw source in every project instance: full public text in
      `raw/`, public source URL and retrieval date recorded in the document registry.
- [ ] Chunked by criterion sections; sieved into RULE crumbs.
- [ ] All 18 criteria have ≥1 RULE crumb.

### Task 7.2 — Requirement records

**What:** `scripts/build_requirements.py` — decompose each criterion into requirement rows
(`REQ-APP_B_IV-01` …) with statement, parent criterion, sub-requirement flag.
**Why:** Stable REQ IDs let evaluations, gaps, and findings point at the exact clause they
concern, not just "criterion IV somewhere".

- [ ] Every criterion has ≥1 requirement row.
- [ ] REQ IDs match grammar; statements carry source RULE crumb references.
- [ ] Sub-requirements linked to parent requirement.

### Task 7.3 — Requirement validator

**What:** `scripts/validate_requirements.py` — 18/18 criteria covered, IDs valid, every
requirement traceable to a RULE crumb.
**Why:** An incomplete requirement registry silently narrows the audit's scope; this makes
completeness a checked property.

- [ ] Criterion with zero requirements → FAIL.
- [ ] Requirement without RULE-crumb link → FAIL.
- [ ] Result appended to `validation_runs.csv`.

---

## EPIC 8 — Evaluation engine

**Labels:** `epic`, `evaluation`, `scoring`, `applicability`, `must-have`
**Goal:** One human-approved applicability ruling and one evidence-gated evaluation record
per criterion, one canonical score over the applicable set, and one evaluation data package
that feeds both deliverables.
**Why:** This is the system's judgment core. The axiom: maximize conformance score subject
to coverage, completeness, accuracy, clarity, alignment — and evidence support. No crumb,
no positive classification. And no evaluation at all before applicability is ruled
(source: docs/context/36).

### Task 8.1 — Criterion applicability ruling

**What:** `scripts/rule_applicability.py` + `criterion_applicability` rows — per supplier
run, each of the 18 criteria is ruled `applicable` or `not-applicable` based on the
supplier's documented scope of activity, with written justification citing the scope
source; the ruling set requires human approval (Gate G2) before evaluation may start.
**Why:** The etalon mandates 18 criteria, but not every criterion applies to every company
(an installation-only supplier performs no design work → Criterion III Design Control is
not applicable). Evaluating inapplicable criteria produces noise; skipping them silently
destroys defensibility. An explicit, justified, approved ruling is the audit-correct path.

- [ ] Every criterion gets exactly one ruling per supplier run: applicable / not-applicable
      + justification.
- [ ] Not-applicable justification cites the supplier scope source (document or crumb ID).
- [ ] Ruling set requires an approvals.csv row (Gate G2) before evaluation may run.
- [ ] Changing a ruling after evaluation invalidates affected evaluations (forced re-run).

### Task 8.2 — Evaluation record model

**What:** Implement `criterion_evaluations` writes with the 15-field record: criterion_id,
criterion_name, classification, score, coverage, completeness, accuracy, clarity, alignment,
evidence_supported, affirmative_summary, contrary_summary, judge_ruling, gaps,
verification_actions.
**Why:** Structured storage before generation: the report and dashboard are projections of
these rows, so the rows must carry everything both outputs need.

- [ ] One record per criterion: full evaluation for applicable criteria; a minimal `na`
      record (classification `na`, reference to the applicability ruling) for
      not-applicable criteria.
- [ ] All 15 fields present; enums from vocabularies.
- [ ] Affirmative/contrary/judge structure preserved (debate pattern from the example audit session).

### Task 8.3 — Evidence gate rule

**What:** Enforcement in the evaluation writer: classification `fully`/`substantially`
requires ≥1 linked DOCUMENT crumb; missing evidence forces downgrade and records why.
**Why:** This single rule is what makes the audit defensible — it converts the evidence
constraint from prompt guidance into a hard write-time invariant.

- [ ] Positive classification without evidence link → write refused.
- [ ] Full evaluation write for a not-applicable criterion → write refused.
- [ ] Downgrade path recorded (`evidence_supported: false` + gap row).
- [ ] Every evaluation lists its supporting crumb IDs.

### Task 8.4 — Scoring calculator

**What:** `scripts/score_evaluation.py` — computes per-criterion score and consolidated
conformance score strictly from `scoring_model.yml`.
**Why:** One score logic, zero improvisation: the same evaluation rows always produce the
same numbers, and model changes are versioned schema changes, not silent code edits.

- [ ] Reads weights/thresholds/rounding only from `scoring_model.yml`.
- [ ] Not-applicable criteria excluded from the consolidated score; denominator =
      applicable-criteria count.
- [ ] Emits per-criterion scores + consolidated score + classification counts
      (including the `na` count).
- [ ] Deterministic: identical inputs → identical outputs.

### Task 8.5 — Evaluation data package builder

**What:** `scripts/build_evaluation_package.py` — emits
`outputs/<supplier>_appendix_b_evaluation_data.json`: all evaluation records, scores,
counts, gaps, actions, run metadata.
**Why:** The package is the single source both the report and dashboard consume — the
architectural answer to score divergence.

- [ ] Package contains all 18 records (evaluated + `na`), the applicability matrix,
      consolidated metrics, RUN-id, and schema versions.
- [ ] Package validates against its own declared schema.
- [ ] Rebuild from unchanged DB is byte-identical (stable ordering).

### Task 8.6 — Evaluation validator

**What:** `scripts/validate_evaluation.py` — record completeness, enum validity, evidence
gate compliance, score recomputation match.
**Why:** Re-derives the scores independently and compares — catching both data corruption
and calculator regressions.

- [ ] Missing criterion record → FAIL.
- [ ] Positive classification without evidence → FAIL.
- [ ] `na` record without an approved applicability ruling → FAIL.
- [ ] Scored record for a not-applicable criterion → FAIL.
- [ ] Recomputed score ≠ stored score → FAIL.
- [ ] Result appended to `validation_runs.csv`.

---

## EPIC 9 — Evidence matrix and gap model

**Labels:** `epic`, `matrix`, `gaps`, `must-have`
**Goal:** A per-criterion coverage matrix and a classified gap register that automatically
spawns auditor actions for missing evidence.
**Why:** Gap detection is a first-class audit output: the matrix shows coverage at a glance,
and gaps are where audit value concentrates (source: docs/context/36).

### Task 9.1 — Evidence matrix builder

**What:** `scripts/build_matrix.py` — per criterion: RULE evidence count, DOCUMENT evidence
count, gap count, finding count, action count; emitted as `wiki/evidence/matrix.md` + JSON.
**Why:** The matrix is the auditor's situational display — one table answering "where are
we thin?" before any narrative is written.

- [ ] All 18 criteria listed with the five counts and their applicability status.
- [ ] Counts computed from DB only (no manual entry).
- [ ] Markdown and JSON emissions agree.

### Task 9.2 — Gap register

**What:** Gap rows (`GAP-APP_B_IV-01` …) with status from the gap vocabulary, criterion
link, and a pointer to missing or weak evidence.
**Why:** "There is a gap" is not actionable; a classified gap linked to the exact missing
evidence is.

- [ ] Each gap: one status, one criterion, one evidence pointer (missing/weak).
- [ ] Gap IDs match grammar.
- [ ] Gaps referenced by the criterion's evaluation record.

### Task 9.3 — Missing-evidence → auditor action rule

**What:** Automatic creation of an `auditor_actions` row (type from vocabulary) for every
`missing-evidence` gap.
**Why:** A missing-evidence gap without a follow-up action is a dropped audit thread; the
rule guarantees every hole gets a hook.

- [ ] Every `missing-evidence` gap has ≥1 linked action.
- [ ] Action type defaults to `verification` or `document_request` per documented rule.
- [ ] Validator (EPIC 13) fails on unhooked missing-evidence gaps.

---

## EPIC 10 — Findings and auditor actions

**Labels:** `epic`, `findings`, `approval`, `must-have`
**Goal:** Findings and auditor actions exist as draft-until-approved records with a full
approval trail.
**Why:** Findings are formal audit statements; generated analysis must be separated from
approved conclusions until a human has ruled (source: draft plan; Project02 gate lesson).

### Task 10.1 — Finding template and pages

**What:** `templates/finding-template.md` + `wiki/findings/FIND-nnnn.md` pages: criterion
link, evidence links (crumb IDs) or missing-evidence link, severity, confidence, basis,
gap link, verification status, approval status.
**Why:** The template forces every finding to carry its own defense: what, where seen,
how serious, how confident, what basis.

- [ ] Template exists; frontmatter matches page contract (EPIC 1.7).
- [ ] Every finding links criterion + evidence-or-gap.
- [ ] Status starts `draft`; only approvals manifest moves it.

### Task 10.2 — Auditor action records

**What:** Action pages/rows (`ACT-nnnn`) typed `verification / document_request /
sample_test / interview`, linked to finding or gap, with open/closed state.
**Why:** Actions are the audit's forward motion — what the auditor will actually do next;
typing them makes the follow-up plan sortable and reportable.

- [ ] Every action: type from vocabulary, link to finding or gap, state.
- [ ] Open actions listed in current-status.md at session end.
- [ ] Priority actions flagged for report/dashboard surfacing.

### Task 10.3 — Approval workflow

**What:** `draft → approved` transition recorded in `manifests/approvals.csv` (object_id,
decision, date, reviewer, notes); script `scripts/approve.py` applies it.
**Why:** Approval must be an explicit recorded human act, not an implicit state drift —
this is what Gate G4 audits.

- [ ] Approval requires an approvals.csv row; page status follows the manifest.
- [ ] Un-approved findings are excluded from report/dashboard generation.
- [ ] Approval of a finding with broken links is refused.

### Task 10.4 — Findings validator

**What:** `scripts/validate_findings.py` — link integrity, enum validity, approval
consistency (page status vs manifest).
**Why:** Findings feed formal outputs; their integrity gets its own dedicated check.

- [ ] Finding without evidence-or-gap link → FAIL.
- [ ] Page status ≠ manifest status → FAIL.
- [ ] Result appended to `validation_runs.csv`.

---

## EPIC 11 — Evaluation Report generator

**Labels:** `epic`, `report`, `deliverable`, `must-have`
**Goal:** The Evaluation Report generates from the evaluation package alone and cannot
disagree with it.
**Why:** The report is formal audit output; generating it (instead of writing it) removes
transcription error as a failure class (source: docs/context/35, 40).

### Task 11.1 — Report template

**What:** `templates/evaluation-report-template.md` with the fixed section set:
Executive Summary; Scope and Source Documents; Method; Coverage Summary;
Criterion-by-Criterion Evaluation; Gap Analysis; Priority Verification Actions;
Recommendations; Consolidated Conformance Score; Limitations; Appendix: Evidence Matrix.
**Why:** A fixed structure makes supplier reports comparable across engagements.

- [ ] All 11 sections present in template order.
- [ ] Not-applicable criteria reported with their justification (never silently omitted);
      the consolidated score states the applicable-criteria basis (e.g. "over N applicable
      criteria").
- [ ] Every factual slot maps to a package field or crumb citation.
- [ ] Template documents which fields are generated vs human-reviewed.

### Task 11.2 — Report generator

**What:** `scripts/generate_report.py` — renders
`outputs/<supplier>_appendix_b_evaluation_report.md` from the package + template.
**Why:** Same inputs, same report — reproducibility is the point.

- [ ] Report score equals package score; counts equal package counts.
- [ ] Criterion sections carry crumb-ID citations.
- [ ] Only approved findings/actions appear.
- [ ] Regeneration from unchanged package is idempotent.

### Task 11.3 — Report consistency validator

**What:** `scripts/validate_report.py` — parses the generated report and cross-checks
scores, counts, gaps, actions against the package.
**Why:** Belt and braces: even a generated file gets independently re-checked, so a manual
edit or generator bug cannot ship silently.

- [ ] Any score/count divergence → FAIL.
- [ ] Missing required section → FAIL.
- [ ] Unsupported (citation-less) conclusion sentence patterns → FAIL.

---

## EPIC 12 — Dashboard generator

**Labels:** `epic`, `dashboard`, `html`, `deliverable`, `must-have`
**Goal:** A standalone, offline, self-contained HTML dashboard generated from the same
evaluation package, validated for data, structure, and behavior.
**Why:** The dashboard is generated audit software, not a hand-crafted artifact; the
illustrative dashboard example defines the rendering bar (source: docs/context/38, 40).

### Task 12.1 — Dashboard data builder

**What:** `scripts/build_dashboard_data.py` — produces
`outputs/<supplier>_appendix_b_dashboard_data.json` per `dashboard_schema.yml`
(18 criterion objects, counts, weighted score, priority actions).
**Why:** A separate, validated data step means the renderer is dumb — all audit logic stays
upstream where it is testable.

- [ ] Exactly 18 criterion objects; not-applicable criteria carry rating `na` and
      reference their applicability justification.
- [ ] Validates against `dashboard_schema.yml`.
- [ ] All values derived from the evaluation package (no independent computation).

### Task 12.2 — Dashboard HTML template

**What:** `templates/dashboard-template.html` — embedded CSS + JS, no external references;
sections: header, metric bar, executive summary, distribution, controls, criterion cards,
matrix, actions, footer; implementing the contract in `schemas/dashboard_schema.yml`
(the illustrative dashboard in docs/context/38 shows the intended look and behavior).
**Why:** Offline self-containment is a hard deliverable requirement (audit environments
have no internet, and external calls are a data-leak vector).

- [ ] Zero external CSS/JS/font/CDN references.
- [ ] All nine sections present.
- [ ] Filters, search, sorting, expand/collapse, print view implemented in embedded JS.

### Task 12.3 — Dashboard renderer

**What:** `scripts/generate_dashboard.py` — injects data JSON into the template; writes
`outputs/<supplier>_appendix_b_dashboard.html` + copy under `wiki/dashboards/`.
**Why:** Reproducible rendering closes the loop: data change → regenerate → identical
process every time; manual HTML edits become pointless.

- [ ] Opens and renders from `file://` with no network.
- [ ] All 18 cards and all matrix rows render from data.
- [ ] Regeneration is idempotent; DASH-id + generation date stamped in footer.

### Task 12.4 — Dashboard data/consistency validator

**What:** `scripts/validate_dashboard.py` (data part) — dashboard data vs evaluation
package: scores, ratings, counts, actions; forbidden-pattern scan on the HTML.
**Why:** The dashboard must be locked to the package; and login/OAuth/CDN artifacts in a
deliverable would be both a defect and a leak.

- [ ] Score or count mismatch vs package → FAIL.
- [ ] Missing criterion / wrong rating enum → FAIL.
- [ ] `login.microsoftonline.com`, `oauth`, `signin`, CDN/external URL patterns → FAIL.

### Task 12.5 — Dashboard JS smoke checks

**What:** Static functional checks in `validate_dashboard.py` (smoke part): required
function names, element IDs, data bindings, button hooks exist in the HTML.
**Why:** A dashboard that renders but cannot filter/search/sort is a silent functional
regression; static smoke checks catch it without needing a browser harness.

- [ ] Required JS function names present.
- [ ] Required element IDs / card containers present.
- [ ] Data-binding markers match the data JSON keys.
- [ ] Mandatory when `phase: dashboard_ready`.

---

## EPIC 13 — Validation layer and aggregate runner

**Labels:** `epic`, `validation`, `must-have`
**Goal:** One command — `python3 scripts/run_all_validations.py` — runs every validator,
phase-aware, and logs the aggregate result.
**Why:** Validation that isn't one command doesn't get run. The workspace commons already
mandates this entry point; this epic wires all spine validators into it.

### Task 13.1 — Aggregate runner

**What:** `scripts/run_all_validations.py` — runs, in order: raw_sources, chunks,
traceability, app_b_json (spot-check mode), requirements, evaluation, findings, structure,
frontmatter, report, dashboard; prints per-validator PASS/FAIL + aggregate.
**Why:** One exit code for "is the project healthy" — usable by humans, hooks, and gates.

- [ ] Runs all validators; continues past failures to report the full picture.
- [ ] Aggregate PASS only if all applicable validators PASS.
- [ ] Non-zero exit on aggregate FAIL.

### Task 13.2 — Phase-aware strictness

**What:** Runner reads `project-state.yml` phase; later phases activate more validators
(report/dashboard validators only from `report_ready` / `dashboard_ready` onward);
warning-tier schema fields flip to strict at `evaluated`.
**Why:** Early phases must not fail on artifacts that legitimately don't exist yet, but late
phases must not pass without them — strictness follows lifecycle.

- [ ] Validator applicability matrix (phase × validator) documented in the runner.
- [ ] Phase downgrade of strictness is impossible (later phase ⇒ superset of checks).
- [ ] Skipped validators reported as SKIPPED(phase), not PASS.

### Task 13.3 — Wiki hygiene validators

**What:** `scripts/validate_structure.py` + `scripts/validate_frontmatter.py` — directory
conformance, filename rules, frontmatter contract per `page_types.yml` /
`required_fields.yml` (ported from Project02 pattern).
**Why:** The wiki is a deliverable surface too; page hygiene keeps Obsidian navigation and
validators working as the page count grows.

- [ ] Misplaced/misnamed files → FAIL.
- [ ] Missing/invalid frontmatter per page type → FAIL.
- [ ] Every run appends a row per validator to `validation_runs.csv`.

---

## EPIC 14 — Audit state machine and human gates

**Labels:** `epic`, `workflow`, `gates`, `must-have`
**Goal:** Phase transitions are code-enforced, human gate decisions are recorded artifacts,
and sessions always know where they stand.
**Why:** The audit lifecycle must be un-skippable: no report from unapproved findings, no
dashboard from an unvalidated package. Humans decide; the machine remembers and enforces.

### Task 14.1 — State machine implementation

**What:** `scripts/audit_state.py` — states `registered, chunked, sieved,
evidence_reviewed, evaluated, findings_drafted, findings_approved, report_ready,
dashboard_ready, closed, failed`; legal transitions only; `failed` reachable from any state.
**Why:** A typed state machine converts process discipline from convention into mechanism.

- [ ] Illegal transition → error naming current state and legal successors.
- [ ] Transitions write to project-state.yml + log entry.
- [ ] `--status` prints current state, pending gate, open exceptions.

### Task 14.2 — Gate decision protocol

**What:** Gate packet template (`templates/gate-packet-template.md`) + procedure: at each
gate G1–G7, Claude assembles a standalone packet (what was done, what the human must check,
concrete decision options with plain-language ELI5 explanations) and stops.
**Why:** Gates only work if the human can decide quickly and confidently; packets carry the
decision to the human instead of making the human dig.

- [ ] Packet template: summary, evidence pointers, validation results, options + ELI5, decision record slot.
- [ ] One packet per gate per supplier; packets are standalone documents.
- [ ] Decision recorded in approvals.csv + project-state.yml before phase advances.

### Task 14.3 — Session continuity enforcement

**What:** Session start: read shared/project CLAUDE.md → latest immutable handoff/HANDOFF.md →
current-status.md → index.md → project-state.yml; detect drift, in-progress states, and unfinished
runs. Session end: run validations and invoke the shared `/handoff` skill from Task 0.7.
**Why:** The system must survive session boundaries without losing its place — continuity
is what makes the wiki "persistent and compounding".

- [ ] In-progress state at session start produces an explicit resume-or-rollback prompt.
- [ ] Session end checklist and `/handoff` are documented and referenced by `/audit-close`.
- [ ] Session start reports divergence among handoff, Git HEAD, current-status.md, and project-state.yml.
- [ ] current-status.md always names the next action.

---

## EPIC 15 — Sieving subsystem integration

**Labels:** `epic`, `sieving`, `tooling`, `should-have`
**Goal:** The vendored sieving code (`sieving/src/json_extractor`) is wired into the
project as the single crumb-processing library — reviewed, pinned, and drift-guarded.
**Why:** The sieving implementation is vendored into `sieving/` as an **integral,
locally-maintained part of this project** — one location where sieving is implemented,
maintained, modified, and interconnected with the wiki system (upstream origin recorded
in `sieving/PROVENANCE.md`). Code review (Sieving guide v1.1) confirmed the v0.1-era
risks (duplicate flattening, private pandas API) are already resolved; remaining work is
project wiring, dependency pinning, and drift visibility.
**Decision (2026-07-04, human):** sieving has **no separate GUI**. The vendored Streamlit
adapter was removed (see `sieving/PROVENANCE.md` divergence log); sieving is operated
through project scripts and slash commands, and reviewed through generated reports/wiki
pages, DB queries, and CSV/XLSX exports.

### Task 15.1 — Wire project scripts to the vendored library

**What:** Project pipeline scripts (`scripts/`) import crumb validation/flattening from
`sieving/src/json_extractor`; no copy of that logic exists anywhere else in the project.
**Why:** One implementation, one location — the point of vendoring sieving into the
project is that every consumer uses the same code.

- [ ] `scripts/` imports resolve against `sieving/src/json_extractor` (packaging/path documented).
- [ ] No duplicated flatten/validate logic anywhere in the project (grep-verified).
- [ ] `sieving/cli.py` remains a headless dev/debug entry only until `scripts/` wrappers
      cover its functions, then it is retired (no project process may depend on it).

### Task 15.2 — Dependency pinning and API guard

**What:** Pin `sieving/requirements.txt` versions; add a regression guard that fails if
private pandas APIs (e.g. `_append`) are reintroduced.
**Why:** The private-API defect is fixed upstream; a guard keeps it fixed through future
local modifications.

- [ ] Dependency versions pinned.
- [ ] Guard test fails on any private pandas API usage (currently zero, verified).
- [ ] Export regression passes on pinned versions.

### Task 15.3 — Schema drift detection

**What:** Warning mode logs missing/unexpected fields on load; `--strict` fails on drift.
**Why:** Auto-creating missing columns hides upstream contract changes — drift must be
visible in warning mode and blocking in strict mode.

- [ ] Missing expected field → logged warning.
- [ ] Unexpected field → logged warning.
- [ ] `--strict` converts both to failures.

### Task 15.4 — Export regression fixtures

**What:** Small fixture JSON + expected CSV/XLSX outputs; test compares actual exports.
**Why:** Export format is a consumer contract (spreadsheet review); fixtures freeze it.

- [ ] Fixture input + expected outputs stored under `sieving/tests/fixtures/`.
- [ ] Test fails on any column/order/value change.

---

## EPIC 16 — Reference benchmark fixtures and regression

**Labels:** `epic`, `benchmark`, `regression`, `must-have`
**Goal:** Two supplier-independent reference fixtures — one for scoring, one for dashboard
rendering — that the evaluation engine and renderer are permanently tested against, in this
project and in every future company evaluation that reuses the engine.
**Why:** Regression protection must not depend on any real supplier's data. A synthetic
evaluation set with hand-verified expected results anchors the scoring logic; a synthetic
data package covering every rating value anchors the renderer. The two benchmark classes
stay strictly separate: a scoring fixture never tests rendering, and vice versa.

### Task 16.1 — Scoring benchmark fixture

**What:** `benchmarks/scoring/` — a synthetic evaluation input set (all 18 criteria, mixed
ratings) plus expected outputs: per-criterion scores, classification counts, and the
consolidated score — computed once via `scoring_model.yml`, hand-verified, then locked.
**Why:** Anchors the evaluation engine: if scoring logic or the scoring model drifts, this
fixture fails first.

- [ ] Fixture covers every rating value at least once.
- [ ] Expected values computed via the EPIC 8 calculator and hand-verified at creation.
- [ ] Used only for scoring regression (never rendering).
- [ ] Any change to `scoring_model.yml` requires re-approval + version bump of the fixture.

### Task 16.2 — Dashboard rendering benchmark fixture

**What:** `benchmarks/dashboard_rendering/` — a synthetic dashboard data package (18
criterion objects, every rating value represented) plus expected structural properties
(card count, matrix rows, metric values, functional hooks).
**Why:** Anchors the renderer and validators: structure, counts, and behavior are proven
against a known-good input independent of any real audit.

- [ ] Fixture data validates against `dashboard_schema.yml`.
- [ ] Renderer output over fixture data passes all EPIC 12 validators.
- [ ] Used only for rendering/validation tests (never scoring).

### Task 16.3 — Benchmark policy note

**What:** `benchmarks/BENCHMARK_POLICY.md` — records the separation rule: scoring and
rendering fixtures are independent benchmark classes; their values must never be forced to
agree; each is updated only through its own approval.
**Why:** Configuration control: a future maintainer must not "unify" the two fixtures and
thereby weaken both regression anchors.

- [ ] Both fixture classes, their purposes, and the separation rule documented.
- [ ] Update/approval procedure per fixture documented.

### Task 16.4 — Benchmark hook in aggregate runner

**What:** `run_all_validations.py` gains a `--benchmarks` mode running both fixture tests.
**Why:** Benchmarks that require a separate invocation stop being run; hooking them into
the standard runner keeps them alive.

- [ ] `--benchmarks` runs both fixtures and reports PASS/FAIL.
- [ ] Mandatory before G5 (report release) and G6 (dashboard release).

---

## EPIC 17 — Claude Code commands

**Labels:** `epic`, `commands`, `automation`, `should-have`
**Goal:** One slash command per pipeline stage so operating the system is discoverable and
repeatable.
**Why:** The pipeline is many small scripts (by design); commands package them into the
few verbs a session actually needs (source: docs/context/40 EPIC 16).

### Task 17.1 — Pipeline commands

**What:** `.claude/commands/`: `/audit-status`, `/audit-register`, `/audit-chunk`,
`/audit-sieve`, `/audit-resieve` (new generation + metrics + diff), `/audit-link`,
`/audit-eval`, `/audit-report`, `/audit-dashboard`, `/audit-validate`, `/audit-gate`,
`/audit-close`.
**Why:** Each command wraps exactly one stage (KISS); `/audit-gate` assembles the gate
packet and stops for the human.

- [ ] Each command documents: purpose, script(s) invoked, preconditions (phase), outputs.
- [ ] Commands refuse to run in a wrong phase (state machine check first).
- [ ] `/audit-status` shows phase, gate states, open actions, last validation result.

### Task 17.2 — Command reference in CLAUDE.md

**What:** Command table in project CLAUDE.md (name → stage → phase → artifacts).
**Why:** The control schema is the one place future sessions look first; commands must be
listed where they will be found.

- [ ] All commands listed with phase preconditions.
- [ ] Session start/end protocol references `/audit-status` and `/audit-close`.

---

## EPIC 18 — Sieving iteration and tuning harness

**Labels:** `epic`, `sieving`, `tuning`, `iteration`, `must-have`
**Goal:** Sieving can be re-run, measured, compared, and rolled back cheaply — so the
prompts can be tuned as many times as it takes without ever corrupting audit data.
**Why:** Sieving (crumb formation) is the crown activity of this project: crumb quality
bounds everything downstream — evaluations, scores, findings, both deliverables. Its
effectiveness will not be pinpointed on the first attempt. This harness turns prompt
tuning from a risky manual exercise into a routine measured loop:
**re-sieve → measure → diff → score against golden set → promote or roll back →
deposit the lesson (skills).**

### Task 18.1 — Sieving playbook

**What:** `sieving/SIEVING_PLAYBOOK.md` — the single entry point for all sieving work:
where prompts live, how to create a new version, how to run a generation, how to read the
metrics report, how to diff runs, how to promote or roll back a generation.
**Why:** "Easily accessible and maintainable" means one document that a future session (or
the human) reads first; without it, tuning knowledge scatters across scripts and memory.

- [ ] Playbook covers: file map, versioning rule, the tuning loop, promotion/rollback,
      golden-set scoring.
- [ ] Every sieving script's CLI documented with one example invocation.
- [ ] CLAUDE.md marks the playbook as mandatory reading before any sieving change.

### Task 18.2 — Generational re-sieving

**What:** Re-running sieving on a document creates a new generation in `sieve_runs` (new
RUN-id, prompt version); previous generations are superseded, never deleted; exactly one
generation per document is `active`; rollback = repointing `active`.
**Why:** Frequent prompt modification is only safe when a bad run can never destroy a good
one — generations make every tuning experiment reversible.

- [ ] A new run never modifies or deletes prior crumbs (supersede flag only).
- [ ] Exactly one active generation per document; downstream stages read only active crumbs.
- [ ] Rollback to a previous generation is a single recorded operation.
- [ ] Re-running with an unchanged prompt version produces a warning (no-op tuning).

### Task 18.3 — Sieving metrics report

**What:** `scripts/sieve_metrics.py` — per-run report (md + JSON): crumbs per criterion,
criteria with zero crumbs, field-completeness rates, quote-verification rate (from EPIC 6
linking), rejected/failed item counts, and comparison to the previous active generation.
**Why:** Tuning needs a number to move: the report makes each prompt change's effect
visible in minutes and gives Gate G2 an objective basis for accepting sieving quality.

- [ ] Report generated automatically at the end of every sieve run.
- [ ] All listed metrics present; zero-crumb criteria prominently flagged.
- [ ] Report stored per RUN-id; the active generation's report is part of the G2 gate packet.

### Task 18.4 — Run diff tool

**What:** `scripts/sieve_diff.py` — compares two generations of the same document:
crumbs added / removed / changed per criterion, quote overlaps, side-by-side samples.
**Why:** "Is the new prompt better?" is answered by seeing exactly what changed — not by
re-reading hundreds of crumbs.

- [ ] Diff by criterion: added / removed / changed counts + item lists.
- [ ] Changed-crumb view shows old vs new statement and quotes side by side.
- [ ] Output readable as markdown (human) and JSON (tooling).

### Task 18.5 — Golden calibration set

**What:** `benchmarks/sieving_golden/` — one small reference document (or excerpt) with a
human-approved expected crumb list ("golden crumbs"); `scripts/score_sieving.py` scores any
prompt version against it: found / missed / spurious per criterion.
**Why:** Metrics say how *much* a prompt extracts; the golden set says how *correctly* it
extracts. It is the fixed target that makes successive prompt versions comparable — the
direct answer to "we will not pinpoint sieving effectiveness on the first attempt."

- [ ] Golden document + expected crumbs stored and human-approved (approvals.csv row).
- [ ] Scoring reports found / missed / spurious per criterion.
- [ ] Every new prompt version is scored against the golden set before promotion.
- [ ] Golden-set changes require re-approval (version bump).

### Task 18.6 — Prompt version registry

**What:** `sieving/prompts/CHANGELOG.md` — one entry per prompt version: date, version, what
changed, why, golden-set score, decision (promoted / rejected).
**Why:** Frequent modification without a registry produces "which prompt made these
crumbs?" archaeology; the registry plus per-crumb RUN-id makes every crumb's provenance
one lookup away.

- [ ] Every prompt version has a changelog entry before first use.
- [ ] Entry records golden-set score and the promotion decision.
- [ ] Every promotion/rejection entry links the skill update that deposited its lesson
      (Task 18.7 growth rule).
- [ ] The active prompt version per side (RULE / DOCUMENT) is unambiguous at all times.

### Task 18.7 — Sieving skill set

**What:** Three Claude Code skills seeded in `.claude/skills/`:
`sieving-run` (operating discipline: side selection, run context, active prompt version,
import + validation, failure handling — thin, points to the PLAYBOOK for mechanics),
`crumb-quality` (extraction craft: statement quality, verbatim quote fidelity,
borderline-criterion decision rules, item_type selection, multilingual rules),
`sieving-tuning` (loop judgment: reading metrics, interpreting diffs, golden-set scores,
promote/rollback criteria, CHANGELOG entries).
**Why:** Sieving quality depends on judgment, not just mechanics. Commands run the
mechanics, the PLAYBOOK maps the system, the spec guide states the contract — skills
encode *how to decide*, and they are where accumulated tuning lessons compound across
sessions (Project02's proven mandatory-reading pattern, made Claude Code-native).

- [ ] Three SKILL.md seeds exist in `.claude/skills/` with the `sieving-` prefix,
      cross-linked to `sieving/` artifacts (PLAYBOOK, spec guide, CHANGELOG).
- [ ] CLAUDE.md rule: the matching skill is read before the corresponding sieving
      activity (run / crumb review / prompt change).
- [ ] Growth rule enforced: every prompt promotion or rejection deposits its lesson into
      the matching skill (checklist item in the promotion procedure).
- [ ] `crumb-quality` contains a borderline-criterion decision table (seeded with known
      confusion pairs, e.g. V/VI/XVII document-vs-records, IV/VII procurement,
      X/XI inspection-vs-test; grown from real tuning experience).

---

# 7. Definition of Done (project level)

- [ ] All epics' acceptance criteria checked.
- [ ] `run_all_validations.py` → aggregate PASS at phase `dashboard_ready`.
- [ ] `run_all_validations.py --benchmarks` → both reference benchmark fixtures PASS.
- [ ] Sieving tuning loop demonstrated on the pilot document: new prompt version →
      re-sieve → metrics → diff → golden-set score → promote or roll back.
- [ ] End-to-end dry run on a small test document: raw → report + dashboard with zero manual edits.
- [ ] All seven gates decided and recorded in approvals.csv.
- [ ] wiki/index.md, log.md, current-status.md current; project-state.yml at `closed` for the pilot run.

# 8. Open decisions (human input requested — not blockers for EPICs 0–2)

1. **Supplier code for first production run.** Output files are named
   `<supplier>_appendix_b_*`. Proposed: `enconet` (per project name). Confirm or correct.
2. **Scoring model calibration.** Task 1.5 creates the structure; the actual weights /
   thresholds need your approval before the first real evaluation (Gate G3 prerequisite).
   A calibration proposal with concrete options (ELI5-explained) will be presented when
   Task 1.5 is executed.
3. **Working language of evidence quotes.** Plan assumes: quotes preserved in original
   language (Slovenian/English/other), all analysis text in English. Confirm.
4. **DB engine.** Plan fixes SQLite (context doc 30 says "for example sqlite"). Confirm
   SQLite is acceptable as the committed choice.
5. **Wiki page granularity for evidence.** Plan generates evidence pages per criterion
   (18 pages) rather than per crumb (hundreds). Confirm or request per-crumb pages.
6. **Supplier scope-of-activity source.** Applicability rulings (Task 8.1) need a
   documented statement of what Enconet actually does (scope of supply / services).
   Which document defines it — a contract, purchase order scope, the supplier's QA
   manual scope section, or a statement you will provide?

---

*End of Master Development Plan v1.0 — generated 2026-07-04. Review, decide Section 8, and
approve to begin EPIC 0.*
