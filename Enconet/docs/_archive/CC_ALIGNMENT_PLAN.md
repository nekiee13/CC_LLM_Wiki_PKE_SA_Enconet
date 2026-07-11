# CC Alignment Plan — 03_PKE_SA_NQA1 workspace and Enconet project

## 0. Document control

| Field | Value |
|---|---|
| Document | CC_ALIGNMENT_PLAN.md |
| Prepared | 2026-07-11 |
| Author | Claude Code (CC) |
| Status | Proposed — awaiting human review |
| Scope | `C:\xPY\xPrj\LLM_Wiki\03_PKE_SA_NQA1` (workspace) and `...\03_PKE_SA_NQA1\Enconet` (first project entry) |
| Format | GitHub-issues style: epics → tasks → acceptance criteria, with dependencies |
| Companion | `CC_PREPARATION_CRITIQUE.md` (evidence for every problem this plan remediates) |
| Relationship to CX_ALIGNMENT_PLAN.md | **Adopted with amendments.** The CX epic skeleton (A0–A6) is endorsed; this plan renumbers it C0–C6, corrects two items (GUI decision, dead-code metric), and adds tasks for gaps CC-1…CC-5. Where a task is unchanged from CX, this plan says so instead of re-writing it. |

### Baseline (independently verified 2026-07-11 — see CC_PREPARATION_CRITIQUE §1)

- Indexes exist and are current for this preparation:
  jcodemunch `local/Enconet-0a063bd7` (indexed 2026-07-11T00:01, 31 py files / 186 symbols),
  jdocmunch `local/PKE_SA_NQA1_Enconet_docs` (indexed 2026-07-11T00:18, 19 docs / 1005 sections).
  Cited as snapshots, not acceptance thresholds (CC-5).
- No `.git` anywhere in `LLM_Wiki` except `02_PKE_Procedure_revision/.git`. The GitHub
  backup (`github.com/nekiee13/CC_LLM_Wiki_PKE_SA_Enconet`) is not verifiably connected
  to this tree.
- Environment: Python 3.13.9; `pandas`, `openpyxl`, `pytest` absent; `typer`, `rich` present.
- Authority documents present: `MASTER_DEVELOPMENT_PLAN.md` **v1.1** (draft; amended
  2026-07-11 concurrently with this preparation — Task 0.7 adds the shared `/handoff`
  skill, Tasks 0.2/14.3 integrate it and fix the workspace-commons path),
  `Sieving_method_specification_Guide.md` v1.1 (AS-IS), `sieving/PROVENANCE.md`.
- Recorded human decision 2026-07-04: sieving has **no separate GUI** (do not re-open).

## 1. Target structure and ownership model

Endorses the CX target tree with two additions (marked ←). Workspace level owns what is
reusable across Enconet / Ekonerg / TEKOL / future entries; project level owns everything
supplier-specific.

```text
03_PKE_SA_NQA1/                        ← workspace root (one git repository, pending D-1)
├── .gitignore
├── CLAUDE.md                          ← shared rules, inherited by every project entry
├── README.md                          ← workspace map + project registry
├── doc/                               ← GLOBAL doc section (user requirement #4)
│   ├── README.md                      ← index + scope/owner/update-trigger per file
│   ├── ARCHITECTURE.md                ← system architecture (engine, data spine, wiki)
│   ├── FUNCTIONAL-ANALYSIS.md         ← requirements ↔ implementation ↔ validation map
│   ├── AS-IS.md                       ← what verifiably exists (built from checks, not plans)
│   ├── AFI.md                         ← areas for improvement / missing / future upgrades
│   ├── GOOD-PRACTICES.md              ← confirmed working practices, with evidence links
│   ├── LESSONS-LEARNED.md             ← what went wrong and the rule it produced
│   ├── RECORD-KEEPING.md              ← the record system contract (EPIC C5)
│   ├── SKILLS.md                      ← inventory of all skills, both levels
│   └── INDEXING.md                    ← jmunch profiles, refresh rules, metric caveats  ← added (CC-5, §3.2 of critique)
├── .claude/skills/                    ← SHARED skills (user requirement #5)
│   └── handoff/SKILL.md               ← /handoff — shared across all entries (EPIC C3)
├── scripts/                           ← workspace-level validators (structure, path policy)
├── tests/                             ← workspace contract tests
├── Enconet/                           ← project entry #1 (this project)
│   ├── CLAUDE.md                      ← short; inherits ../CLAUDE.md, adds Enconet specifics
│   ├── MASTER_DEVELOPMENT_PLAN.md
│   ├── Sieving_method_specification_Guide.md
│   ├── project-state.yml
│   ├── HANDOFF.md                     ← pointer to latest handoff record (EPIC C3)
│   ├── handoffs/                      ← immutable timestamped handoff records
│   ├── decisions/                     ← immutable ADRs (EPIC C5)
│   ├── docs/                          ← project docs (this file) + context/ archive
│   ├── .claude/skills/                ← Enconet-only skills (sieving-* per master plan 18.7)
│   ├── wiki/  manifests/  schemas/  scripts/  tests/   (per master plan EPIC 0)
│   └── sieving/                       ← vendored subsystem (unchanged location)
├── Ekonerg/                           ← placeholder until its own kickoff
└── TEKOL/                             ← placeholder (benchmark heritage lives in Enconet/benchmarks until then)
```

Ownership rules (CX rules 1–4 endorsed verbatim), plus:

5. **Recorded human decisions are closed.** A task may implement or document a decision;
   re-opening one requires an explicit ADR that supersedes the old record.
6. **Index numbers are snapshots.** Controlled docs cite (repo id, indexed_at, count);
   acceptance criteria test properties, never absolute counts.

---

## EPIC C0 — Recover a verifiable repository baseline

**Labels:** `epic`, `git`, `must-have` · **Depends on:** — · **CX equivalent:** A0 (endorsed)

### Task C0.1 — Locate or restore the repository boundary
As CX A0-T1, unchanged: find the `.git` that belongs to
`CC_LLM_Wiki_PKE_SA_Enconet` or re-clone and reconcile file-by-file; never overwrite
local work unreviewed; record remote/branch/SHA/worktree state.

- [ ] `git rev-parse --show-toplevel` succeeds from `Enconet/`.
- [ ] Remote URL, branch, HEAD SHA, upstream recorded in `doc/AS-IS.md` and the first handoff.
- [ ] A local-vs-remote manifest diff exists; every difference classified (keep-local / take-remote / merge) before any overwrite.
- [ ] Decision D-1 (repository boundary) recorded as ADR-0001.

### Task C0.2 — Root git hygiene
As CX A0-T2, plus explicit DATA handling.

- [ ] Root `.gitignore` covers: `__pycache__/`, `.pytest_tmp/`, `*.sqlite-journal`, venvs, `.obsidian/workspace*`, local settings, export scratch.
- [ ] Decision D-2 (DATA policy: tracked fixtures vs LFS vs external) recorded as ADR-0002.
- [ ] Commit tag vocabulary adopted and documented in shared CLAUDE.md: `[align] [docs] [schema] [fix] [test] [handoff] [gate]` (superset of master plan Task 0.6 tags).

---

## EPIC C1 — Documentation authority and path contract

**Labels:** `epic`, `docs`, `authority`, `must-have` · **Depends on:** C0 · **CX equivalent:** A1 (endorsed with additions)

### Task C1.1 — Context authority catalog
As CX A1-T1, unchanged in substance: classify every `docs/context/*` file
(`source` / `historical-session-export` / `example` / `candidate-requirement`) in
`Enconet/docs/README.md`; mark 23 as mixed-historical, 30/35 as stubs, 37/38 as examples.

- [ ] Every context file has exactly one classification and a disposition (extract / retain-as-history / supersede).
- [ ] No current controlled doc cites an example (37/38) as proof of implementation.
- [ ] Legacy paths (`/home/nekiee/...`, `F:\xPy\Json`, `LLL_Wiki`) appear only inside content classified historical.

### Task C1.2 — Path-resolution contract
As CX A1-T2, unchanged: `WORKSPACE_ROOT` / `PROJECT_ROOT` / `SIEVING_ROOT` / `DATA_ROOT` /
`OUTPUT_ROOT` defined in `doc/ARCHITECTURE.md`, one code helper, package-anchored defaults,
CLI/env overrides, `pathlib` everywhere.

- [ ] CLI produces identical results from three different CWDs given equivalent explicit inputs.
- [ ] A workspace validator rejects new machine-specific absolute paths outside historical blocks.
- [ ] Tests cover relocation, spaces, non-ASCII, Windows separators.

### Task C1.3 — Master plan reconciliation (extends CX A1-T3)
Amend `MASTER_DEVELOPMENT_PLAN.md` in place (it is a draft awaiting review — amendments
are its normal life-cycle). **Status note:** the v1.1 amendment (2026-07-11) already
resolved the `/handoff` integration (Task 0.7) and the Task 0.2 commons path. Remaining:

- [ ] §4 target layout re-rooted at `03_PKE_SA_NQA1/Enconet/` (still reads `PKE_SA_Enconet/`; workspace items split out to workspace level).
- [ ] Version-string consistency: H1 title and footer still read "v1.0" while document control reads 1.1 — one version, everywhere.
- [ ] Document-control block gains an amendment log row per amendment (what changed, when, why); v1.1 backfilled.
- [ ] Plan links to `CC_ALIGNMENT_PLAN.md` + both critiques as preparation inputs.
- [ ] Verify Task 0.7 / EPIC C3 contracts are one contract (naming, statuses, flow) — C3 is the detailed design for 0.7, never a fork.
- [ ] Master plan exists exactly once after review. Current variants at Enconet root: `MASTER_DEVELOPMENT_PLAN.md` (v1.1, live), `CX_MASTER_DEVELOPMENT_PLAN.md` (byte-identical v1.1 duplicate), `CC_MASTER_DEVELOPMENT_PLAN.md` (v1.2-CC proposed revision: §4 re-rooted, version strings unified, amendment log, preparation inputs linked). On approval the accepted variant becomes `MASTER_DEVELOPMENT_PLAN.md` and both prefixed copies are removed (superseded content preserved by git once C0 lands).

### Task C1.4 — Correct the spec guide misstatement (new — critique CC-2)

- [ ] `Sieving_method_specification_Guide.md` §10.1 no longer claims `config.py` derives criteria "via AppBTemplate"; it states the actual duplication and links the dedup task C4.4.
- [ ] Change note appended to the guide's document control (v1.1 → v1.2).
- [ ] Same commit as C4.4 or explicitly cross-referenced if done earlier.

---

## EPIC C2 — Shared governance and the global doc section

**Labels:** `epic`, `governance`, `must-have` · **Depends on:** C1 · **CX equivalent:** A2 (endorsed)

### Task C2.1 — Shared `03_PKE_SA_NQA1/CLAUDE.md`
As CX A2-T1: authority rules, evidence constraints, immutable-source policy, validation
gates, jmunch usage, precedence (safety/evidence > workspace > project), session
start/end protocol requiring `/handoff` before close.

- [ ] `Enconet/CLAUDE.md` shrinks to Enconet-specific additions and one inherit line.
- [ ] No supplier-specific schema in the shared file.
- [ ] Session-end protocol names `/handoff` as mandatory; session-start names `HANDOFF.md` as first read.

### Task C2.2 — Scaffold `03_PKE_SA_NQA1/doc/`
As CX A2-T2 with the file set from §1 (including `INDEXING.md`). Seed content sources:

| File | Seeded from |
|---|---|
| ARCHITECTURE.md | master plan §2–§4 (data spine, layout) + sieving spec guide §1, §10 |
| FUNCTIONAL-ANALYSIS.md | master plan epic map ↔ code reality (what implements what) |
| AS-IS.md | verified inventory (critique P2-4): working / present-unverified / planned / retired |
| AFI.md | spec guide §11 limitations + critique findings not yet remediated |
| GOOD-PRACTICES.md | PROVENANCE divergence-log pattern, spec-guide code-verification pattern, two-tier enforcement documentation |
| LESSONS-LEARNED.md | DOC-prompt placeholder defect; tools/fix_* drift history; index false-positive lesson (critique §3.2) |
| RECORD-KEEPING.md | EPIC C5 contract |
| SKILLS.md | inventory: shared `handoff`; Enconet `sieving-run`, `crumb-quality`, `sieving-tuning` (master plan 18.7) |
| INDEXING.md | EPIC C6 profiles + caveats |

- [ ] Every file has scope, owner, update trigger.
- [ ] AS-IS contains zero claims without a file/command/test reference.
- [ ] `doc/README.md` links all files and both project entries.

### Task C2.3 — Skill boundaries
As CX A2-T3: shared skills at `03_PKE_SA_NQA1/.claude/skills/`, Enconet-only at
`Enconet/.claude/skills/`; each SKILL.md declares owner, trigger, inputs, outputs,
failure behavior; inventory in `doc/SKILLS.md`.

- [ ] Shared skills reference no Enconet-only paths.
- [ ] A structure test fails on duplicate skill names across levels.
- [ ] Master plan Task 18.7 skills are listed as Enconet-level (they encode supplier-corpus judgment).

---

## EPIC C3 — The `/handoff` skill (session bridge)

**Labels:** `epic`, `handoff`, `continuity`, `must-have` · **Depends on:** C0, C2 · **CX equivalent:** A3 (endorsed) · **Master plan anchor:** Task 0.7 (added in v1.1 — this epic is its detailed design, not a competing contract)

**Goal:** one command ends every session with an immutable, machine-validatable record
that lets the next session continue with minimal catch-up (user requirement #6).

### C3 Design — the handoff contract

**Storage** (naming per master plan Task 0.7).
- Immutable record: `<PROJECT_ROOT>/handoffs/YYYY-MM-DDTHHMMSSZ-<short-sha>.md`
  (`<short-sha>` present when a git HEAD exists; omitted with a visible warning in
  degraded no-git mode). Never edited after publication.
- Pointer: `<PROJECT_ROOT>/HANDOFF.md` — an exact copy of the latest record plus a
  one-line header naming the record it mirrors. Atomically replaced on each run.

**Record schema.** YAML frontmatter (machine-validatable) + fixed body sections:

```yaml
---
id: 2026-07-11T153000Z-abc1234        # equals the record filename stem
project: 03_PKE_SA_NQA1/Enconet
created_utc: 2026-07-11T15:30:00Z
author: claude-code            # or human name
git:
  root: <abs path or null>
  branch: <name | detached | null>
  head: <sha | null>
  upstream: <remote/branch | null>
  dirty: true|false|unknown
  untracked: <n | unknown>
phase: <project-state.yml phase | unknown>
validation:
  command: <exact invocation | not-run>
  exit_code: <int | not-run>
  status: passed|failed|not-run|unknown
indexes:
  - profile: enconet-code
    repo: local/Enconet-0a063bd7
    indexed_at: <ts>
    stale: true|false
  - profile: enconet-docs
    repo: local/PKE_SA_NQA1_Enconet_docs
    indexed_at: <ts>
    stale: true|false
---
```

Body sections, in order (every one present, `n/a` allowed only where stated):

1. **Objective and phase** — one paragraph: what the project is doing right now.
2. **Completed this session** — bullet list, each with file paths and commit SHAs (or "uncommitted").
3. **Decisions** — made (ADR links) and open (with the question stated precisely).
4. **Validation evidence** — commands, exit codes, one-line result each; `not-run` is a
   legal, visible value — never implied.
5. **Blockers and risks** — including uncommitted/generated artifacts.
6. **Next action** — exactly **one** concrete next step, then an ordered follow-up queue.
7. **Reading list** — the minimal file set the next session must read (target ≤ 5 files).

**Statuses** are four-valued everywhere: `passed | failed | not-run | unknown`.
Prohibited content: secrets, environment dumps, raw evidence bodies, claims without a
file/command reference.

**Generation flow (atomic).**
1. **Collect** (read-only): git facts (graceful `null`s when no repo — required until C0
   completes), `project-state.yml`, `wiki/current-status.md`, tail of `wiki/log.md`,
   open ADRs, last validation results, jmunch index metadata (staleness = source tree
   mtime newer than `indexed_at`).
2. **Render** to a temp file in the scratch area.
3. **Validate** frontmatter against the schema (all mandatory keys present, enums legal).
4. **Publish atomically**: move temp → `handoffs/<id>.md`; rewrite `HANDOFF.md`; a failure
   between the two steps must leave the previous `HANDOFF.md` intact (write-new + replace).
5. **Log**: append exactly one `handoff-created: <id>` event to `wiki/log.md`.
6. Any mandatory-step failure → non-zero exit, nothing published, partial temp retained
   for diagnosis.

**Implementation shape.** The skill (`03_PKE_SA_NQA1/.claude/skills/handoff/SKILL.md`)
instructs the agent and delegates fact collection to a deterministic helper
`03_PKE_SA_NQA1/scripts/make_handoff.py` (git/state/index probing, schema validation,
atomic publish), so the record's factual spine is script-generated and only the narrative
sections are authored by the agent. The helper is what makes "repeat runs never mutate
history" testable.

**Session-start counterpart** (integration, not a separate skill): shared CLAUDE.md
directs every session to read `HANDOFF.md` first, then verify it against reality —
git HEAD, `project-state.yml` phase, index staleness. Any mismatch is reported before
work starts.

### Task C3.1 — Specify and validate the record schema

- [ ] Schema above captured in `doc/RECORD-KEEPING.md` + a machine schema (`schemas/handoff_schema.yml` at workspace level).
- [ ] `make_handoff.py --validate <file>` checks any record; malformed frontmatter → non-zero.
- [ ] Four-valued status enforced; `passed` without a command+exit_code is a validation error.

### Task C3.2 — Implement skill + helper

- [ ] `SKILL.md` + `make_handoff.py` exist at workspace level; work for Enconet and for a second-project fixture directory.
- [ ] No-git environment produces a valid record with `git.*: null` and a visible warning (works before C0 completes).
- [ ] Repeat runs create new records; prior records byte-identical afterwards.
- [ ] Interrupted publication (simulated) leaves previous `HANDOFF.md` intact.

### Task C3.3 — Integrate

- [ ] Shared CLAUDE.md session-end protocol: `/handoff` mandatory; session-start: read + verify `HANDOFF.md`.
- [ ] Master plan integration already present in v1.1 (Tasks 0.2, 0.7, 14.3) — verify wording stays consistent with this contract during C1.3.
- [ ] Aggregate validation runner (when it exists, master plan EPIC 13) gains a handoff-freshness check: warn when HEAD has moved ≥ N commits since the last record.

### Task C3.4 — Test matrix

- [ ] Covered: no git; dirty worktree; detached HEAD; stale/missing index; failed validation run; repeat runs; interrupted write; Unicode paths; CP1252 console (ASCII-safe output).
- [ ] A fresh session using only `HANDOFF.md` + reading list can state phase, last validation status, and next action — demonstrated once as a recorded exercise.

---

## EPIC C4 — Sieving code and tooling alignment

**Labels:** `epic`, `code`, `audit-safety`, `must-have` · **Depends on:** C1 · **CX equivalent:** A4 (amended)

### Task C4.1 — Fail-closed filtering (CX A4-T3, endorsed)

- [ ] Invalid filter ⇒ non-zero exit and **no output file**, by default; `--allow-unfiltered-preview` is the explicit dev escape (preview only — export remains blocked while `filter_error` is set).
- [ ] Tests: parse error, execution error, preview override, export blocking.
- [ ] Any use of the override is visible in the run summary (and later, handoff).

### Task C4.2 — Blocking validation gate (new — critique CC-1)

- [ ] `run_pipeline(strict_validation=True)` (default for any export path): a file containing ≥1 ERROR-severity `ValidationError` is rejected whole (transactional-per-file), listed in the run summary.
- [ ] `record_side` validated as hard enum **before** side-specific checks; missing/invalid side is an ERROR, not a silent skip.
- [ ] Advisory mode remains available for exploration but cannot feed an export without an explicit recorded override.
- [ ] Regression tests written first and failing before the change (test-first rule, C5).

### Task C4.3 — Quarantine the hazard chain (extends CX A4-T1; critique CC-3, CC-4)

- [ ] `tools/check_files.py`, `fix_files.py`, `fix_structure.py`, `fix_init_files.py`, `print_run_pipeline_sig.py` moved to `sieving/tools/_archive/` with a README tombstone (what they were, why archived, drift history they evidence).
- [ ] `verify_install.py` rewritten: dependency checks **before** package imports; dependency vs structure errors distinguished; ASCII-only output (no cp1252 crash); never recommends a mutating script.
- [ ] Remaining `fix_mor_*` / `fix_nqa1_*` / `fix_rule_refs_*` data-repair scripts: archived likewise once their migrations are captured in LESSONS-LEARNED.md (they are evidence of drift history — do not silently delete).
- [ ] No active script resolves project root as `Path(__file__).parent` pointing at `tools/`.

### Task C4.4 — Single-owner contracts (CX A4-T4 + critique CC-2)

- [ ] One machine-readable owner for: 18-criteria taxonomy, canonical codes, item_type enum, canonical column schema, query field list. (Location per decision D-3; default: `Enconet/schemas/*.yml` per master plan EPIC 1, loaded by sieving code.)
- [ ] `config.py` and `templates/app_b.py` load from the owner (or one is reduced to a thin re-export of the other as an interim step).
- [ ] Drift test compares owner ↔ runtime tables ↔ prompt text ↔ exporter columns.
- [ ] Spec guide §10.1 corrected in the same change (Task C1.4).
- [ ] Existing DATA files re-validate unchanged, or differences land in an explicit migration manifest.

### Task C4.5 — GUI documentation cleanup (CX A4-T2 **reframed** — decision already recorded 2026-07-04)

- [ ] `README.md`, `QUICKSTART.md`, `PROJECT_INFO.md` no longer advertise Streamlit/`app.py`; each edit cites the 2026-07-04 decision (PROVENANCE.md).
- [ ] No open-decision entry for the GUI anywhere in current docs.
- [ ] A docs-vs-reality smoke check: every command quoted in README/QUICKSTART executes (at least `--help`) in the bootstrapped environment.

### Task C4.6 — Test breadth (CX P2-2 remediation)

- [ ] `test_export_sync.py` replaced with real export contract tests (column order, encoding utf-8-sig, xlsx sheet name, format/suffix precedence).
- [ ] New tests for: C4.1 filter behavior, C4.2 blocking gate, C1.2 path contract, bad-file handling, CLI exit codes.
- [ ] Measured coverage reported in the validation runner (jmunch reachability treated as heuristic only).

---

## EPIC C5 — Record keeping and test-first validation

**Labels:** `epic`, `records`, `validation`, `must-have` · **Depends on:** C0 · **CX equivalent:** A5 (endorsed)

**The record taxonomy (user requirement #7)** — captured in `doc/RECORD-KEEPING.md`:

| Record | Form | Mutability | Trigger |
|---|---|---|---|
| Design decisions / trade-offs | `Enconet/decisions/ADR-NNNN-<slug>.md` (context → options → decision → consequences) | Immutable; superseded, never edited | Any decision that constrains future work |
| Events | `wiki/log.md` | Append-only | Every session, every gate, every handoff |
| Current state | `wiki/current-status.md`, `project-state.yml` | Replaceable | Session end |
| Handoffs | `handoffs/*` + `HANDOFF.md` | Immutable + pointer | Session end (EPIC C3) |
| Lessons / practices | `doc/LESSONS-LEARNED.md`, `doc/GOOD-PRACTICES.md` | Curated, each entry linked to its evidence (log/ADR/commit/test) | When a lesson is confirmed, not when suspected |
| Provenance | `PROVENANCE.md`-style divergence logs | Append-only | Any vendored-code change |
| Manifests | `manifests/*.csv` | Append-only rows | Per master plan EPIC 0.4 |

### Task C5.1 — Instantiate the taxonomy

- [ ] `decisions/` seeded with ADR-0001 (repo boundary), ADR-0002 (DATA policy), ADR-0003 (schema owner), and a **backfill ADR recording the 2026-07-04 GUI decision** so the existing decision has a first-class record.
- [ ] `wiki/log.md` + `current-status.md` created (master plan Task 0.3 brought forward).
- [ ] Commit messages reference task IDs and ADRs where applicable.

### Task C5.2 — Layered, test-first validation (CX A5-T2 endorsed)

Layers 0–5 as CX (syntax → structure/paths/authority → unit → integration fixtures →
golden regression → state/handoff recovery), one aggregate runner, machine + human output.

- [ ] Every implementation task in EPICs C1–C4 starts from a failing test or validator demonstrating the gap (enforced by review checklist).
- [ ] Aggregate runner returns non-zero naming the failed layer; SKIPPED ≠ PASS.
- [ ] Generated outputs reproducible, or nondeterministic fields documented and normalized.

### Task C5.3 — Reproducible environment (CX A5-T3 endorsed)

- [ ] Supported Python versions declared; runtime vs dev/test dependencies separated; constraints or lock file added (current floor-pins are insufficient; `pytest>=9.0.2` bound verified against the actually-installed version).
- [ ] Clean-machine bootstrap documented and executed once on this machine; full suite green; result recorded in AS-IS.md and the first handoff.
- [ ] Console output portable to CP1252 terminals (verified via the C4.3 rewrite).

---

## EPIC C6 — Reindexing, navigation, and closure

**Labels:** `epic`, `indexes`, `navigation`, `must-have` · **Depends on:** C1–C5 · **CX equivalent:** A6 (amended)

### Task C6.1 — Navigable indexes (CX A6-T1 endorsed)

- [ ] Workspace README, `doc/README.md`, `Enconet/docs/README.md`, and wiki index exist and interlink.
- [ ] Orphan gate applies to **controlled docs only**; classified historical context is cataloged but exempt.
- [ ] The 3 swallowed-heading warnings resolved or waived with a note.

### Task C6.2 — jmunch profiles and metric caveats (CX A6-T2 + critique §3.2, CC-5)

Documented in `doc/INDEXING.md`:

| Profile | Tool | Root | Notes |
|---|---|---|---|
| `enconet-code` | jcodemunch | `Enconet/` | Python only; DATA excluded |
| `enconet-docs` | jdocmunch | `Enconet/` | Controlled docs + context (context tagged historical) |
| `nqa1-global-docs` | jdocmunch | `03_PKE_SA_NQA1/doc/` | Created when C2.2 lands |

- [ ] Stable names, roots, exclude patterns, and full-vs-incremental refresh rules documented; refresh required after any batch doc/code change and before `/handoff` reports index state.
- [ ] **Caveat registry** included: (a) `find_dead_code` produces false positives through `__init__` re-exports in this package shape — confirm with `find_importers`/grep before deletion; (b) orphan-section counts include the historical corpus by construction; (c) all cited counts carry (repo, indexed_at).
- [ ] `verify_index` clean immediately after each full refresh; `/handoff` flags stale roots.

### Task C6.3 — Close with evidence (CX A6-T3 endorsed)

- [ ] All validation layers green; indexes refreshed and verified; health snapshots recorded.
- [ ] AS-IS / AFI / LESSONS / GOOD-PRACTICES updated from this preparation's findings.
- [ ] `/handoff` generated; evidence packet committed; every epic's acceptance criteria link to a command result, test, file, or ADR.

---

## Recommended order

1. **C0** — git identity first; nothing controlled should change before provenance exists (exception: the two CC preparation docs and master-plan amendment, which are the preparation itself).
2. **C4.3** — quarantine the destructive tools (cheap, removes the standing hazard).
3. **C1** — authority catalog, path contract, master plan + spec guide reconciliation.
4. **C2** — shared CLAUDE.md, global doc/, skill boundaries.
5. **C3** — /handoff (usable in degraded no-git mode even earlier; full value after C0).
6. **C5** — records + environment + test-first runner (C5.3 environment can run parallel to C2).
7. **C4** (rest) — fail-closed filters, blocking validation, contract dedup, doc cleanup, tests.
8. **C6** — navigation, index profiles, closure evidence.

## Decision register — ALL DECIDED 2026-07-11 (records in `Enconet/decisions/`)

| # | Decision | Outcome | ADR |
|---|---|---|---|
| D-1 | Repository boundary | One repo rooted at `03_PKE_SA_NQA1` | ADR-0001 |
| D-2 | `sieving/DATA` policy | Not tracked in git; checksum manifest tracked; external backup location still to be designated (open action, flagged in handoffs) | ADR-0002 |
| D-3 | Canonical schema owner | `Enconet/schemas/*.yml`; workspace promotion only via superseding ADR | ADR-0003 |
| D-4 | Context disposition | Move to `docs/_archive/context/` after G0; never delete (2-year evolution history) | ADR-0004 |
| D-5 | Dual-agent policy | Keep both Claude Code and Codex + drift validation | ADR-0005 |
| D-6 | Master plan candidate | v1.3-CX becomes canonical in G1; variants archived | ADR-0006 |
| §8-1 | Supplier/framework label | `enconet` + `appendix_b`; scheme `<supplier>_<framework>_<artifact>` extensible (ISO 9001 future candidate) | ADR-0008 |
| §8-2 | Scoring calibration | Deferred by decision to Gate G3 | ADR-0013 |
| §8-3 | Language policy | sl/en/hr only; no translation; verbatim quotes; per-run deliverable language — **master plan Task 5.5 / EPIC 11–12 amendment required** | ADR-0009 |
| §8-4 | DB engine | SQLite confirmed | ADR-0010 |
| §8-5 | Evidence page granularity | 18 per-criterion pages | ADR-0011 |
| §8-6 | Supplier scope source | Scope must be determinable from raw docs; undeterminable scope = non-conformance finding, N/A blocked — **master plan Task 8.1 amendment required** | ADR-0012 |

GUI disposition: decided 2026-07-04, backfilled as ADR-0007.
The two required master-plan amendments (ADR-0009, ADR-0012) are applied to the canonical
v1.3 plan as amendment A4 during G1 (see ADR-0006). **The start gate is open: G0 begins.**

*End of CC Alignment Plan — 2026-07-11. Review the D-register and approve to begin EPIC C0.*
