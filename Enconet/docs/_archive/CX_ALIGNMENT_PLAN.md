# PKE SA NQA1 Structure and Continuity Alignment Plan

## Issue metadata

| Field | Value |
|---|---|
| Scope | `03_PKE_SA_NQA1` workspace and first project entry, `Enconet` |
| Status | Proposed |
| Prepared | 2026-07-11 |
| Execution style | GitHub issues: epics, tasks, dependencies, acceptance criteria |
| Workspace root | `C:\xPY\xPrj\LLM_Wiki\03_PKE_SA_NQA1` |
| Project root | `C:\xPY\xPrj\LLM_Wiki\03_PKE_SA_NQA1\Enconet` |

## Baseline

This plan aligns the current checkout. Paths and status copied from the original machine are
historical evidence until verified against this tree.

Confirmed CC/CX differences and the implementation start gate are recorded in
`docs/CX_CC_RECONCILIATION.md`; that document controls the corrections applied here.

- Initial jdocmunch snapshot `local/PKE_SA_NQA1_Enconet_docs` at 2026-07-11T00:01:
  17 files, 949 sections. Counts are snapshot evidence and change after legitimate edits.
- Initial jcodemunch snapshot `local/Enconet-0a063bd7` at 2026-07-11T00:01:
  31 Python files, 186 symbols.
- Initial documentation snapshot: no syntactically broken internal links, 933/949 sections without
  inbound cross-document references, and three structural warnings. Most orphans belong to the
  historical context corpus; controlled-doc navigation is the quality gate.
- Code: health grade C (78.4), average complexity 8.24, two unstable modules, and no dependency
  cycles. The reported 20.5% likely-dead figure is a heuristic snapshot with known false positives
  through package `__init__` re-exports; it is not deletion evidence.
- Tests cannot start in the active environment because `pytest`, `pandas`, and `openpyxl` are absent.
- No `.git` directory is visible at `LLM_Wiki`, `03_PKE_SA_NQA1`, or `Enconet`, so the checkout
  cannot currently prove its remote, branch, commit, or clean state.

## Target ownership model

```text
03_PKE_SA_NQA1/
|-- .git/                         # one verified repository boundary
|-- .gitignore
|-- AGENTS.md                     # shared Codex rules for every project entry
|-- CLAUDE.md                     # shared Claude Code rules for every project entry
|-- README.md                     # workspace map and project registry
|-- doc/                          # global engineering knowledge
|   |-- README.md
|   |-- ARCHITECTURE.md
|   |-- FUNCTIONAL-ANALYSIS.md
|   |-- AS-IS.md
|   |-- AFI.md
|   |-- GOOD-PRACTICES.md
|   |-- LESSONS-LEARNED.md
|   |-- RECORD-KEEPING.md
|   `-- SKILLS.md
|-- .agents/skills/               # repo-local Codex skills
|   `-- handoff/SKILL.md
|-- .claude/skills/               # repo-local Claude Code skills
|   `-- handoff/SKILL.md          # equivalent workflow, validated for drift
|-- scripts/                      # workspace validators/index wrappers
|-- tests/                        # workspace contract tests
|-- Enconet/
|   |-- AGENTS.md                 # Enconet Codex additions; inherits ../AGENTS.md
|   |-- CLAUDE.md                 # Enconet Claude additions; inherits ../CLAUDE.md
|   |-- MASTER_DEVELOPMENT_PLAN.md
|   |-- project-state.yml
|   |-- docs/                     # approved plans, decisions, context catalog
|   |   `-- context/              # historical/source material, non-authoritative by default
|   |-- .agents/skills/           # Enconet-only Codex skills
|   |-- .claude/skills/           # Enconet-only Claude Code skills
|   |-- decisions/                # immutable ADR records
|   |-- handoffs/                 # immutable generated handoffs
|   |-- wiki/                     # index, append-only log, current status
|   |-- manifests/ schemas/ scripts/ tests/
|   `-- sieving/                  # existing working subsystem
|-- Ekonerg/
`-- TEKOL/
```

Ownership rules:

1. Workspace-wide concepts live once under `doc`, root agent guidance, root skill directories,
   root `scripts`, or root `tests`. `AGENTS.md`/`.agents` are Codex discovery surfaces;
   `CLAUDE.md`/`.claude` are Claude Code discovery surfaces.
2. Enconet implementation details live under Enconet and reference, but do not duplicate,
   workspace policy.
3. `Enconet/docs/context` is an input archive. Content becomes normative only through an
   approved current document or decision.
4. Runtime paths are repository-relative or supplied by CLI/configuration. Code must not depend
   on a user name, drive letter, current working directory, or legacy root name.

## EPIC A0 - Recover a verifiable repository baseline

**Goal:** Establish a trustworthy Git identity before changing controlled records.

**Dependencies:** None.

### A0-T1 - Locate or restore the repository boundary

- [ ] Determine whether `.git` was omitted during copy/download or whether the actual clone is elsewhere.
- [ ] Prefer one repository rooted at `03_PKE_SA_NQA1`; document a narrower boundary only if the
  GitHub repository intentionally contains Enconet alone.
- [ ] Record remote URL, default branch, current SHA, upstream, and worktree state.
- [ ] Compare a local file manifest with the last GitHub backup before overwriting anything.

**Acceptance criteria**

- `git rev-parse --show-toplevel` succeeds from Enconet.
- Remote, branch, HEAD, and upstream are recorded in `doc/AS-IS.md` and the first handoff.
- Local/remote differences are reviewed and classified; no local file is silently discarded.

### A0-T2 - Install root Git hygiene

- [ ] Add a root `.gitignore` for Python/test caches, environments, databases/journals, secrets,
  local settings, indexes, and temporary/generated exports.
- [ ] Decide whether `sieving/DATA` is tracked regression data, Git LFS data, or external controlled data.
- [ ] Adopt commit tags such as `[align]`, `[docs]`, `[test]`, `[fix]`, and `[handoff]`.

**Acceptance criteria**

- `git status --short` shows only intended preparation changes.
- Secret and large-file checks pass before the first push from this machine.
- The repository root, not only `Enconet/sieving`, owns effective ignore policy.

## EPIC A1 - Establish documentation authority and path contracts

**Goal:** Prevent historical exports and obsolete paths from controlling implementation.

**Dependencies:** A0.

### A1-T1 - Create an authority/context catalog

- [ ] Add `Enconet/docs/README.md` with owner, status, authority, supersession, and review fields.
- [ ] Classify every context file as `source`, `historical-session-export`, `example`, or
  `candidate-requirement`.
- [ ] Mark `23 FINAL PROJECT FILL-IN.md` as mixed historical material and catalog its unrelated
  Travel Guide, procedure-revision, finance, Linux, and obsolete-path content.
- [ ] Mark `30 Ingestion phase.md` and `35 Wiki output.md` as stubs pending controlled requirements.
- [ ] Mark context 37 and 38 as examples, not verified output or executable contracts.

**Acceptance criteria**

- Every context file has one authority classification and a replacement/extraction action.
- Current docs do not cite an example as proof that a feature is implemented.
- Obsolete `/home/nekiee/...`, `F:\xPy\Json`, and `PKE_SA_Enconet` paths are labeled historical
  or replaced with tokens such as `<WORKSPACE_ROOT>`.

### A1-T2 - Define the path-resolution contract

- [ ] Define `WORKSPACE_ROOT`, `PROJECT_ROOT`, `SIEVING_ROOT`, `DATA_ROOT`, and `OUTPUT_ROOT` in
  global architecture and expose one code helper.
- [ ] Resolve defaults from package/repository location, not process current directory.
- [ ] Support CLI/environment overrides and normalize with `pathlib.Path`.
- [ ] Reject active code/docs containing legacy machine-specific absolute paths.

**Acceptance criteria**

- The CLI works from Enconet, `Enconet/sieving`, and another CWD with equivalent explicit inputs.
- A validator rejects new legacy paths outside explicitly marked historical content.
- Tests cover spaces, non-ASCII names, Windows separators, and repository relocation.

### A1-T3 - Reconcile the master plan

- [ ] Replace the standalone `PKE_SA_Enconet` assumption with workspace/project ownership.
- [ ] Add global `doc`, shared/project `AGENTS.md` and `CLAUDE.md`, both agents' skill discovery
  directories, and root validators.
- [ ] Clearly separate verified baseline, target state, and deferred architecture.
- [ ] Link the master plan to this alignment plan and `CX_PREPARATION_CRITIQUE.md`.

**Acceptance criteria**

- Every master-plan path has one owner in the target model.
- `doc/AS-IS.md` reports no planned component as implemented.
- Approved deviations from the target hierarchy are captured in ADRs.

## EPIC A2 - Create shared governance and global documentation

**Goal:** Give Enconet, Ekonerg, TEKOL, and future entries one reusable baseline.

**Dependencies:** A1.

### A2-T1 - Add shared dual-agent guidance

- [x] Add shared and Enconet `AGENTS.md` files for Codex.
- [x] Add shared and Enconet `CLAUDE.md` files for Claude Code.
- [ ] Define equivalent document authority, evidence constraints, immutable-source policy,
  validation gates, record updates, and jmunch use in both agent surfaces.
- [ ] Require a session-start state summary and `/handoff` before session close.
- [ ] Define precedence: safety/evidence rules, workspace rules, then project additions.
- [ ] Add a drift validator for equivalent cross-agent rules while allowing documented
  tool-specific differences.

**Acceptance criteria**

- Short project `AGENTS.md` and `CLAUDE.md` files inherit their matching shared rules.
- Shared rules contain no Enconet-only schema or supplier assumptions.
- Rules link to canonical global docs rather than duplicating them.
- Codex and Claude Code can each discover their own guidance without relying on the other tool's filename.

### A2-T2 - Scaffold `03_PKE_SA_NQA1/doc`

- [ ] Create `README.md`, `ARCHITECTURE.md`, `FUNCTIONAL-ANALYSIS.md`, `AS-IS.md`, `AFI.md`,
  `GOOD-PRACTICES.md`, `LESSONS-LEARNED.md`, `RECORD-KEEPING.md`, and `SKILLS.md`.
- [ ] Give each file a scope statement, owner, and update trigger.
- [ ] Keep global docs independent of a single supplier run.

**Acceptance criteria**

- `doc/README.md` links all global docs and project entries.
- AS-IS lists verified current capabilities; AFI lists missing/deferred work.
- Architecture and functional analysis link requirements to code and validation evidence.

### A2-T3 - Define skill boundaries

- [x] Put reusable Codex skills under `03_PKE_SA_NQA1/.agents/skills/<skill>/SKILL.md`.
- [x] Put reusable Claude Code skills under `03_PKE_SA_NQA1/.claude/skills/<skill>/SKILL.md`.
- [ ] Put Enconet-only skills under the matching `.agents/skills` or `.claude/skills` directory.
- [ ] Define owner, trigger, inputs, outputs, failure behavior, and tests for each skill.
- [ ] Maintain the inventory in `doc/SKILLS.md`.
- [ ] Validate equivalent dual-agent workflows for semantic drift; do not assume one agent
  discovers the other agent's skill directory.

**Acceptance criteria**

- Shared skills import no Enconet-only path.
- Project skills depend on shared skills only through documented contracts.
- A structure test detects duplicate skill names with conflicting ownership.

## EPIC A3 - Implement shared `/handoff`

**Goal:** Produce a deterministic, reviewable bridge between sessions.

**Dependencies:** A0, A2.

### A3-T1 - Specify the handoff record

The skill writes an immutable record to
`<PROJECT_ROOT>/handoffs/YYYY-MM-DDTHHMMSSZ-<short-sha>.md` and atomically refreshes
`<PROJECT_ROOT>/HANDOFF.md`. The timestamped record is authoritative; the pointer identifies
the record it mirrors.

Required fields:

- workspace/project roots, project ID, UTC timestamp, and agent/author;
- Git root, branch, HEAD, upstream, and worktree status;
- objective, phase, completed work, and referenced files/issues;
- decisions and open decisions with ADR links;
- validation commands, exit codes, and concise results;
- blockers, risks, and uncommitted/generated artifacts;
- exact next action and ordered follow-up queue;
- jmunch index names, source roots, timestamps, and integrity/staleness state.

**Acceptance criteria**

- The schema distinguishes `unknown`, `not-run`, `failed`, and `passed`.
- Secrets, full environment dumps, raw evidence, and unsupported claims are prohibited.
- Frontmatter or a sidecar makes mandatory fields machine-validatable.

### A3-T2 - Implement `/handoff`

- [ ] Collect Git facts read-only and fail clearly when no repository exists.
- [ ] Read status, project state, latest log entries, open ADRs, and validation results.
- [ ] Query jmunch metadata and flag stale/mismatched source roots.
- [ ] Render temporarily, validate, then atomically publish the record and pointer.
- [ ] Append one `handoff-created` event; never rewrite prior log entries.

**Acceptance criteria**

- Repeat runs create new records and never mutate history.
- Partial failure cannot publish a record that appears complete.
- Paths are repository-relative where possible; absolute roots are recorded once.
- The same implementation works for Enconet and a second-project fixture.

### A3-T3 - Integrate and test `/handoff`

- [ ] Reference it from shared/project `AGENTS.md` and `CLAUDE.md`, session close, master plan,
  and validation runner.
- [ ] Test dirty worktree, detached HEAD, no Git, stale index, failed tests, Unicode paths,
  repeat runs, and interrupted writes.
- [ ] At session start compare HANDOFF, latest immutable record, Git HEAD, project state, and status.

**Acceptance criteria**

- A fresh session identifies state, failed/not-run checks, and next action without reading all context.
- Git plus optional manifest hashes makes old-record tampering detectable.
- `/handoff` returns non-zero when mandatory collection, validation, or publication fails.

## EPIC A4 - Align Enconet code and scripts

**Goal:** Make sieving portable, non-destructive, and audit-safe.

**Dependencies:** A1, A2.

### A4-T1 - Repair path-sensitive utilities

- [ ] Quarantine `check_files.py`, `fix_files.py`, `fix_structure.py`, `fix_init_files.py`, and
  `print_run_pipeline_sig.py`; preserve a tombstone explaining their drift history.
- [ ] Replace `check_files.py` with a read-only validator driven by an explicit versioned manifest.
- [ ] Rewrite `verify_install.py` to check dependencies before imports, use encoding-safe output,
  distinguish dependency/structure errors, and never recommend mutating repair scripts.
- [ ] Quarantine remaining data-repair scripts after their migrations are captured.
- [ ] Require `--dry-run`, explicit root, backup/transaction behavior, and tests for retained mutators.

**Acceptance criteria**

- Checks target `sieving`, not `sieving/tools`.
- No utility deletes/moves data based only on CWD or inferred unchecked roots.
- Active output contains no instruction to download files from an unspecified prior session.

### A4-T2 - Align documentation with the retired GUI decision

- [ ] Treat the 2026-07-04 human decision as closed: sieving has no standalone Streamlit GUI.
- [ ] Remove active `streamlit run app.py` and GUI claims from README, QUICKSTART, PROJECT_INFO,
  pipeline comments, and active tools; cite the provenance decision.
- [ ] Do not re-open the GUI without a superseding ADR.

**Acceptance criteria**

- README, QUICKSTART, verifier, dependencies, and actual entry points agree.
- Every advertised interface has a smoke test.

### A4-T3 - Make filtering fail closed

- [ ] Prevent invalid filters from silently widening audit results.
- [ ] Make strict behavior default; permit fail-open preview only through an explicit dev option.
- [ ] Block export whenever a filter error exists unless that override is recorded.

**Acceptance criteria**

- Invalid filters return non-zero and create no output by default.
- Tests cover parse errors, execution errors, preview override, and export blocking.
- Handoff records any fail-open override use.

### A4-T4 - Eliminate duplicated canonical contracts

- [ ] Move criteria, codes, query fields, exporter columns, and crumb schema to one versioned owner.
- [ ] Load/generate runtime objects, prompt checks, and docs from that owner.
- [ ] Add schema-version and fixture migration rules.

**Acceptance criteria**

- One canonical edit updates validation, runtime, and generated documentation.
- Drift tests compare schemas, prompts, query fields, exporter columns, and fixtures.
- Existing DATA files validate or appear in an explicit migration manifest.

### A4-T5 - Add a blocking crumb-validation gate

- [ ] Validate `record_side` as a hard enum before side-specific validation.
- [ ] Make export paths reject a complete input file when any item has an ERROR-severity
  `ValidationError`; preserve transactional per-file behavior.
- [ ] Keep advisory exploration available only through an explicit, recorded option that cannot
  feed export without a separate explicit override.
- [ ] Write failing regression tests before implementation.

**Acceptance criteria**

- ERROR-flagged records cannot enter normal CSV/XLSX/Markdown exports.
- Missing or invalid `record_side` is an ERROR, not a silent validation bypass.
- Run summaries identify rejected files/items and advisory overrides.

### A4-T6 - Correct specification and test coverage

- [ ] Correct `Sieving_method_specification_Guide.md` section 10.1: `config.py` does not derive
  criteria/codes through `AppBTemplate`; link the single-owner task A4-T4.
- [ ] Replace the empty `test_export_sync.py` with export contract tests.
- [ ] Add tests for A4-T1 through A4-T5, path resolution, bad-file handling, and CLI exit codes.
- [ ] Report measured coverage; treat jmunch reachability/dead-code output as heuristic.

## EPIC A5 - Establish records and test-first validation

**Goal:** Make changes reviewable through append-only records, Git, and layered tests.

**Dependencies:** A0-A4.

### A5-T1 - Create the record taxonomy

- [ ] Use immutable ADR files for decisions/trade-offs.
- [ ] Use append-only `wiki/log.md` for events.
- [ ] Use current-status/project-state for replaceable current state.
- [ ] Curate practices, lessons, and AFI with links to logs, ADRs, issues, tests, or commits.
- [ ] Use manifests for sources, artifacts, runs, validations, and handoffs.

**Acceptance criteria**

- Every record type has one purpose, owner, schema/template, and trigger.
- Corrections supersede append-only records instead of rewriting them.
- Commits link task IDs and relevant ADRs.

### A5-T2 - Implement layered validation

- [ ] Layer 0: syntax, formatting, encoding, schema parsing.
- [ ] Layer 1: structure, path policy, authority, links, manifests.
- [ ] Layer 2: unit tests for paths, schema, extraction, query, export.
- [ ] Layer 3: integration tests over small RULE/DOCUMENT fixtures.
- [ ] Layer 4: golden audit package, report, dashboard regression.
- [ ] Layer 5: state-transition and handoff recovery tests.
- [ ] Add one aggregate runner with machine/human output.

**Acceptance criteria**

- Every implementation task starts with a failing test/validator demonstrating the gap.
- Mandatory failure returns non-zero and identifies the failed layer.
- Generated outputs are reproducible or normalize documented nondeterministic fields.

### A5-T3 - Bootstrap a reproducible environment

- [ ] Document Python versions and constrain/lock dependencies.
- [ ] Separate runtime and development/test dependencies where useful.
- [ ] Add clean-machine bootstrap and verification commands.
- [ ] Make console output portable to standard Windows terminals.

**Acceptance criteria**

- A new environment installs and runs the documented full suite.
- Verifier reports dependency failures before dependent import failures and does not crash on CP1252.
- No package is assumed merely because it existed on the original machine.

## EPIC A6 - Rebuild navigation and indexes

**Goal:** Make current information discoverable and prove indexes match the aligned tree.

**Dependencies:** A1-A5.

### A6-T1 - Build navigable indexes

- [ ] Add workspace, global-doc, Enconet-doc, and wiki indexes.
- [ ] Link controlled docs by requirement, architecture, implementation, test, decision, and workflow.
- [ ] Normalize documents reported as swallowed single-heading blocks.

**Acceptance criteria**

- Intentional historical/context orphans are classified and excluded from the controlled-doc gate.
- No current controlled document is reachable only through filesystem browsing.
- Internal-link and heading-structure validation pass.

### A6-T2 - Define repeatable jmunch profiles

- [ ] Document stable names, roots, excludes, and full/incremental refresh rules.
- [ ] Separate global docs, controlled Enconet docs, historical context, code, and data-fixture profiles.
- [ ] Add index integrity/source-root checks to `/handoff` and aggregate validation.
- [ ] Record `(repo id, indexed_at, counts)` whenever metrics are cited; never use fixed counts as
  acceptance thresholds.
- [ ] Document caveats: dead-code false positives through re-exports and intentional context orphans.

**Acceptance criteria**

- Reindexing on another machine produces the same profile names and expected file sets.
- `verify_index` reports no drift immediately after full refresh.
- Handoff identifies stale, dirty, missing, or mismatched indexes.

### A6-T3 - Close alignment with evidence

- [ ] Run all validation layers, full index refreshes, integrity checks, and health snapshots.
- [ ] Update AS-IS, AFI, lessons, practices, status, and append-only logs.
- [ ] Generate `/handoff` and commit the evidence packet.

**Acceptance criteria**

- Every epic criterion links to a command result, test, file, or approved decision.
- Final tree matches the ownership model or documents approved deviations.
- The next session continues from handoff without depending on unclassified session exports.

## Recommended order

1. A0-T1 repository recovery and baseline proof.
2. A1 authority/path contracts.
3. A2 shared governance and global-doc scaffold.
4. A3 `/handoff` contract, implementation, and tests.
5. A4 code alignment, starting with unsafe utilities and fail-open filtering.
6. A5 record taxonomy, environment bootstrap, and validation runner.
7. A1-T3 master-plan reconciliation and A6 documentation/index closure.

## Decisions required

- Repository boundary: all `03_PKE_SA_NQA1` entries or Enconet only.
- DATA policy: tracked fixtures, Git LFS, or external controlled storage.
- Schema owner: workspace-level NQA contract or Enconet-owned contract.
- Context disposition: retain in place with metadata or move to an archive.
- Master-plan candidate: merge accepted CC structural changes and dual-agent additions, then publish
  one canonical plan.

The GUI is not an open decision; retirement was recorded on 2026-07-04.
