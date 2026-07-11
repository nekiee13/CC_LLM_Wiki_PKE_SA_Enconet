# Alignment Plan — 03_PKE_SA_NQA1 workspace and Enconet project

## 0. Document control

| Field | Value |
|---|---|
| Document | docs/ALIGNMENT_PLAN.md — canonical execution backlog |
| Published | 2026-07-11 |
| Status | approved — consolidated from the CX/CC preparation per `docs/CX_CC_RECONCILIATION.md` |
| Supersedes | `docs/_archive/CX_ALIGNMENT_PLAN.md` (A0–A6) and `docs/_archive/CC_ALIGNMENT_PLAN.md` (C0–C6) — content merged here, structure C0–C6 retained, waves G0–G5 from the reconciliation |
| Evidence base | `docs/_archive/CC_PREPARATION_CRITIQUE.md`, `docs/_archive/CX_PREPARATION_CRITIQUE.md` (verified findings), `decisions/ADR-0001…0013` (all preparation decisions) |
| Companion | `MASTER_DEVELOPMENT_PLAN.md` v1.4 (canonical, amendment A4 applied) |
| Format | GitHub-issues style: epics → tasks → acceptance criteria, with dependencies |

### Baseline (verified 2026-07-11)

- Master plan **v1.4 canonical** published; all preparation decisions recorded as
  ADR-0001…0013 in `decisions/`; prefixed plan/preparation variants archived in
  `docs/_archive/` (never deleted, per ADR-0004).
- Indexes: jcodemunch `local/Enconet-0a063bd7`; jdocmunch `local/PKE_SA_NQA1_Enconet_docs`
  (root `Enconet/`, ignore `sieving/DATA/` + `*.json`). Counts are snapshots, never
  acceptance thresholds.
- No `.git` yet (recovery = C0); Python 3.13.9 with pandas/openpyxl/pytest absent;
  verified code defects per the archived critiques (fail-open filters, advisory
  validation, hazardous tools, duplicated contracts, CWD-dependent config).
- Dual-agent governance live: workspace + project `CLAUDE.md`/`AGENTS.md`; `/handoff`
  skill for Codex **user-global** at `~/.agents/skills/handoff/` (CX_ADR-0015), for Claude Code **user-global** at
  `~/.claude/skills/handoff/` (ADR-0014) — one contract; deterministic helper, schema
  validator, and tests still open.

## 1. Target structure and ownership

The canonical target tree is **master plan §4 (v1.4)** — one owner, not repeated here.
Ownership rules:

1. Workspace-wide concepts live once at `03_PKE_SA_NQA1/`: shared `CLAUDE.md`/`AGENTS.md`,
   global `doc/`, workspace-shared skills, workspace scripts/tests. The cross-project Codex
   `/handoff` skill is the user-global exception at `~/.agents/skills/handoff/`.
2. Enconet implementation lives under `Enconet/` and references, never duplicates,
   workspace policy.
3. `docs/_archive/` is preserved history (ADR-0004): cataloged, indexed, exempt from
   controlled-doc gates, never authoritative.
4. Runtime paths are repository-relative or configured; never machine-specific.
5. Recorded human decisions are closed; re-opening one requires a superseding ADR.
6. Index metrics cited in controlled docs carry (repo, indexed_at, count).

## 2. Wave map (reconciliation §5 ↔ epics)

| Wave | Content | Epics/tasks |
|---|---|---|
| G0 | Baseline identity | C0 |
| G1 | Governance: dual-agent guidance, global doc/, authority catalog, path contract, one canonical plan | C1, C2 *(canonical-plan publication: done 2026-07-11)* |
| G2 | Integrity containment: quarantine tools, fix verifier, fail-closed filters, blocking validation | C4.1–C4.3 |
| G3 | Reproducibility: dependency bootstrap, risk-focused tests | C5.3, C4.6 |
| G4 | Contract consolidation: one schema owner + spec-guide correction | C4.4, C1.4, C4.5 |
| G5 | Continuity/indexing: handoff completion, record taxonomy, navigation, index profiles | C3, C5.1–C5.2, C6 |

**Rule:** no database/report/dashboard implementation (master plan EPICs 2+) until G0–G3
pass — polished outputs must not be generated from unverifiable or invalid evidence.

---

## EPIC C0 — Recover a verifiable repository baseline *(wave G0 — NEXT)*

**Depends on:** — · **Decisions:** ADR-0001 (root at `03_PKE_SA_NQA1`), ADR-0002 (DATA policy)

### Task C0.1 — Locate or restore the repository boundary
Find the `.git` belonging to `github.com/nekiee13/CC_LLM_Wiki_PKE_SA_Enconet` or re-clone
and reconcile file-by-file; never overwrite local work unreviewed.

- [ ] `git rev-parse --show-toplevel` succeeds from `Enconet/` and returns the `03_PKE_SA_NQA1` root.
- [ ] Remote URL, branch, HEAD SHA, upstream recorded in `doc/AS-IS.md` and the first handoff.
- [ ] Local-vs-remote manifest diff exists; every difference classified (keep-local / take-remote / merge) before any overwrite.
- [ ] The 2026-07-11 sanitized state (canonical plan, ADRs, archive) is committed as the first clean commits with `[align]` tags.

### Task C0.2 — Root git hygiene

- [ ] Root `.gitignore` covers: caches, venvs, DB journals, `.obsidian/workspace*`, local settings, **`Enconet/sieving/DATA/` (ADR-0002)**.
- [ ] DATA checksum manifest (filename, size, SHA-256, source note) created and tracked; validator verifies corpus ↔ manifest.
- [ ] **Open action (ADR-0002 risk):** owner designates the external backup location for DATA; until then every handoff flags single-copy risk.
- [ ] Commit tag vocabulary documented in shared guidance: `[align] [docs] [schema] [ingest] [eval] [report] [dashboard] [gate] [fix] [test] [handoff]`.

---

## EPIC C1 — Documentation authority and path contract *(waves G1/G4)*

**Depends on:** C0 (except C1.3, executed 2026-07-11 pre-git by owner instruction)

### Task C1.1 — Context authority catalog
Classify every `docs/_archive/` and remaining context file (`source` /
`historical-session-export` / `example` / `candidate-requirement`) in `docs/README.md`,
with disposition per file.

- [ ] Every archived/context file has one classification and a disposition.
- [ ] No controlled doc cites an example (37/38) as proof of implementation.
- [ ] Legacy paths (`/home/nekiee/...`, `F:\xPy\Json`, `LLL_Wiki`) appear only inside content classified historical.
- [ ] `docs/context/` relocation to `docs/_archive/context/` executed as a reviewed post-G0 migration (ADR-0004).

### Task C1.2 — Path-resolution contract
`WORKSPACE_ROOT` / `PROJECT_ROOT` / `SIEVING_ROOT` / `DATA_ROOT` / `OUTPUT_ROOT` defined in
`doc/ARCHITECTURE.md`; one code helper; package-anchored defaults; CLI/env overrides.

- [ ] CLI produces identical results from three different CWDs given equivalent explicit inputs.
- [ ] Workspace validator rejects new machine-specific absolute paths outside historical content.
- [ ] Tests cover relocation, spaces, non-ASCII names, Windows separators.

### Task C1.3 — Canonical master plan publication — **DONE 2026-07-11**

- [x] v1.4 published as `MASTER_DEVELOPMENT_PLAN.md` (ADR-0006): workspace re-root, unified version strings, amendment log A1–A4, preparation inputs linked.
- [x] Amendment A4 applied: language policy (ADR-0009 → principle 10, Tasks 1.3/1.4/5.5, EPICs 11–12) and scope rule (ADR-0012 → Tasks 8.1/8.6); §8 closed to the ADR register.
- [x] Variants archived to `docs/_archive/` (OG_ v1.1, CC_ v1.2-CC, CX_ v1.3-CX) — retained, never deleted.
- [ ] Residual: first git commit captures the publication (C0.1).

### Task C1.4 — Correct the spec guide misstatement

- [ ] `Sieving_method_specification_Guide.md` §10.1 corrected (config.py does **not** derive criteria via AppBTemplate); change note appended (v1.1 → v1.2); same change or explicit cross-ref as C4.4.

---

## EPIC C2 — Shared governance and the global doc section *(wave G1)*

**Depends on:** C1 · **Decisions:** ADR-0005 (dual-agent)

### Task C2.1 — Shared guidance pair
Workspace `CLAUDE.md` + `AGENTS.md` carry equivalent authority/evidence/validation/session
rules (both exist — refine as rules evolve); project pair inherits.

- [ ] Semantic drift validator compares the pairs (and skill pairs); documented tool-specific differences allowed, silent divergence fails.
- [ ] Session-end names `/handoff` mandatory; session-start reads `HANDOFF.md` first, then verifies against reality.
- [ ] Read-first lists point at canonical docs (`MASTER_DEVELOPMENT_PLAN.md`, `docs/ALIGNMENT_PLAN.md`, `docs/CX_CC_RECONCILIATION.md`, `decisions/README.md`).

### Task C2.2 — Scaffold `03_PKE_SA_NQA1/doc/`
Files: `README.md`, `ARCHITECTURE.md`, `FUNCTIONAL-ANALYSIS.md`, `AS-IS.md`, `AFI.md`,
`GOOD-PRACTICES.md`, `LESSONS-LEARNED.md`, `RECORD-KEEPING.md`, `SKILLS.md`, `INDEXING.md`.
Seeds: master plan §2–§4 + spec guide (architecture); verified inventory (AS-IS); spec
guide §11 + unremediated findings (AFI); PROVENANCE/divergence-log and code-verification
patterns (good practices); DOC-prompt defect, tools drift history, index false-positive
lesson (lessons learned).

- [ ] Every file has scope, owner, update trigger; `doc/README.md` links all.
- [ ] AS-IS contains zero claims without a file/command/test reference.

### Task C2.3 — Skill boundaries

- [ ] Workspace-shared Codex skills at `.agents/skills/`; cross-project Codex skills at
      `~/.agents/skills/`; Enconet-only Codex skills at project level; inventory in `doc/SKILLS.md`.
- [ ] Structure test fails on duplicate skill names with conflicting ownership.
- [ ] Master plan Task 18.7 sieving skills are Enconet-level.

### Task C2.4 — Inter-agent coordination protocol *(ADR-0017; implement AFTER C0.1)*

Stand up `Enconet/coordination/` — the repository as the agents' communication channel:
`TEAM_PROTOCOL.md` + `BOARD.md` (agent-neutral shared authorities, exempt from the
CC_/CX_ prefix rule), `messages/` (immutable, author-prefixed
`CC_/CX_<timestamp>_<topic>.md`, schema per ADR-0017), `claims/<task-id>.yml`
(task owner + anticipated files + expiry).

- [ ] **Blocked by C0.1** — no coordination files before the Git boundary exists.
- [ ] `TEAM_PROTOCOL.md` carries working rules 1–10 (claim before edit; no edits under
      another agent's active claim; cross-review as the norm; "synchronized" only after
      each agent confirms its own side; one active writer per shared tree; parallel work
      = separate worktrees + non-overlapping claims) and a concrete claim-expiry default.
- [ ] Message immutability: acknowledgement is a new message with `reply_to`; existing
      messages are never rewritten; blockers require acknowledgement.
- [ ] Session-start reading order extended in both agents' own guidance (each edits only
      its side, ADR-0016): HANDOFF.md → BOARD.md → unread messages → active claims.
- [ ] `agent_coord.py` (workspace scripts/): `status | claim | release | message |
      acknowledge | validate`; validation rejects malformed messages, duplicate IDs,
      overlapping active claims, unacknowledged blockers, stale BOARD.md, and
      unsupported synchronization claims.
- [ ] BOARD.md is generated output (by `agent_coord.py status`), never hand-authoritative.

---

## EPIC C3 — Complete the `/handoff` implementation *(wave G5; usable earlier in degraded mode)*

**Depends on:** C0, C2 · **Master plan anchor:** Task 0.7 · **Status:** the Codex contract
carrier exists at `~/.agents/skills/handoff/SKILL.md`; Claude-side synchronization is owned
by Claude Code and is outside this Codex relocation (CX_ADR-0015).

Record contract (per Task 0.7 and the shared SKILL.md): immutable
`handoffs/YYYY-MM-DDTHHMMSSZ-<short-sha|nogit>.md` + atomic `HANDOFF.md` pointer;
frontmatter `record_type/schema_version/project/created_at_utc/status/git_head/source_agent`;
overall status `complete|partial|blocked`; per-check states `passed|failed|not-run|unknown`;
fixed body headings; one `handoff-created` log event; no implied success, ever.

### Task C3.1 — Machine schema + validator

- [ ] `handoff_schema.yml` (workspace) + `make_handoff.py --validate`; malformed record → non-zero.
- [ ] Per-check `passed` without command + exit code → validation error (closes the prose-only gap).

### Task C3.2 — Deterministic helper

- [ ] `03_PKE_SA_NQA1/scripts/make_handoff.py`: read-only fact collection (git, state, status, log tail, ADRs, validation results, jmunch metadata + staleness), render → validate → atomic publish → single log append.
- [ ] Repeat runs never mutate history; interrupted publication leaves prior `HANDOFF.md` intact; no-git mode produces `nogit` records with visible warning.

### Task C3.3 — Integration + test matrix

- [ ] Both agents' session protocols invoke it; `/audit-close` (master plan EPIC 17) calls it; aggregate runner warns on handoff staleness (HEAD moved since last record).
- [ ] Tests: no git, dirty worktree, detached HEAD, stale index, failed validation, repeat runs, interrupted write, Unicode paths, CP1252 console.
- [ ] Demonstrated once: a fresh session states phase, failed/not-run checks, and next action from `HANDOFF.md` + reading list alone.

---

## EPIC C4 — Sieving code and tooling alignment *(waves G2/G3/G4)*

**Depends on:** C1

### Task C4.1 — Fail-closed filtering *(G2)*

- [ ] Invalid filter ⇒ non-zero exit and **no output file** by default; `--allow-unfiltered-preview` is the explicit dev escape (preview only; export stays blocked while `filter_error` is set).
- [ ] Tests: parse error, execution error, preview override, export blocking; override use visible in run summary and handoff.

### Task C4.2 — Blocking validation gate *(G2)*

- [ ] `strict_validation` default for any export path: a file with ≥1 ERROR-severity `ValidationError` is rejected whole; `record_side` validated as hard enum **before** side-specific checks.
- [ ] Advisory mode cannot feed an export without an explicit recorded override.
- [ ] Regression tests written first and failing before the fix (C5.2 rule).

### Task C4.3 — Quarantine the hazard chain *(G2)*

- [ ] `tools/check_files.py`, `fix_files.py`, `fix_structure.py`, `fix_init_files.py`, `print_run_pipeline_sig.py` → `sieving/tools/_archive/` with a README tombstone; `fix_mor_*`/`fix_nqa1_*`/`fix_rule_refs_*` follow once their migrations are captured in LESSONS-LEARNED.
- [ ] `verify_install.py` rewritten: dependency checks before imports; dependency vs structure errors distinguished; ASCII-safe output; never recommends a mutating script.
- [ ] No active script resolves project root as `Path(__file__).parent` pointing at `tools/`.

### Task C4.4 — Single-owner contracts *(G4)* · **Decision:** ADR-0003

- [ ] `Enconet/schemas/*.yml` owns taxonomy, codes, item_type enum, column schema, query fields; `config.py`/`app_b.py` load from it.
- [ ] Drift test compares owner ↔ runtime tables ↔ prompt text ↔ exporter columns.
- [ ] Existing DATA files re-validate unchanged, or differences land in an explicit migration manifest.
- [ ] Spec guide §10.1 corrected in the same change (C1.4).

### Task C4.5 — GUI documentation cleanup *(G4)* · **Decision:** ADR-0007 (closed 2026-07-04)

- [ ] `README.md`, `QUICKSTART.md`, `PROJECT_INFO.md` no longer advertise Streamlit/`app.py`; each edit cites ADR-0007.
- [ ] Docs-vs-reality smoke check: every command quoted in README/QUICKSTART executes (at least `--help`) in the bootstrapped environment.

### Task C4.6 — Test breadth *(G3)*

- [ ] Empty `test_export_sync.py` replaced with real export contract tests (columns, encoding utf-8-sig, sheet name, format/suffix precedence).
- [ ] New tests for C4.1/C4.2 behavior, path contract, bad files, CLI exit codes; measured coverage reported by the aggregate runner.

---

## EPIC C5 — Record keeping and test-first validation *(waves G3/G5)*

**Depends on:** C0

Record taxonomy (in `doc/RECORD-KEEPING.md`): immutable ADRs (`decisions/`) · append-only
`wiki/log.md` · replaceable `current-status.md`/`project-state.yml` · immutable handoffs +
pointer · curated lessons/practices with evidence links · append-only provenance logs ·
append-only manifests.

### Task C5.1 — Instantiate the taxonomy — **partially DONE**

- [x] `decisions/` seeded with ADR-0001…0013 including the GUI backfill (2026-07-11).
- [ ] `wiki/log.md` + `wiki/current-status.md` + `wiki/index.md` created (master plan Task 0.3); the 2026-07-11 preparation events backfilled as the first log entries.
- [ ] Commits reference task IDs and ADRs where applicable.

### Task C5.2 — Layered, test-first validation

Layers 0–5 (syntax → structure/paths/authority → unit → integration fixtures → golden
regression → state/handoff recovery), one aggregate runner.

- [ ] Every implementation task starts from a failing test/validator demonstrating the gap.
- [ ] Aggregate runner: non-zero on failure naming the layer; SKIPPED ≠ PASS.
- [ ] Generated outputs reproducible, or nondeterministic fields documented and normalized.

### Task C5.3 — Reproducible environment *(G3)*

- [ ] Supported Python versions declared; runtime vs dev/test deps separated; constraints/lock added (floor-pins insufficient; verify the `pytest>=9.0.2` bound against reality).
- [ ] Clean bootstrap executed on this machine; full suite green; result recorded in AS-IS and the next handoff.
- [ ] Console output portable to CP1252 terminals.

---

## EPIC C6 — Reindexing, navigation, and closure *(wave G5)*

**Depends on:** C1–C5

### Task C6.1 — Navigable indexes

- [ ] Workspace README, `doc/README.md`, `Enconet/docs/README.md`, wiki index exist and interlink; no controlled doc reachable only by filesystem browsing.
- [ ] Orphan gate applies to controlled docs only; archived history cataloged but exempt.
- [ ] Swallowed-heading warnings resolved or waived with a note.

### Task C6.2 — jmunch profiles and caveats (in `doc/INDEXING.md`)

| Profile | Tool | Root | Notes |
|---|---|---|---|
| `enconet-code` | jcodemunch | `Enconet/` | Python only |
| `enconet-docs` | jdocmunch | `Enconet/` | **ignore `sieving/DATA/`, `*.json`** |
| `nqa1-global-docs` | jdocmunch | `03_PKE_SA_NQA1/doc/` | when C2.2 lands |

- [ ] Stable names, roots, excludes, full-vs-incremental refresh rules documented; refresh after batch changes and before `/handoff`.
- [ ] Caveat registry: `find_dead_code` false positives via `__init__` re-exports (confirm with find_importers/grep before deletion); orphan counts include archives by construction; **wrong-root incremental refresh silently re-roots a profile — always pass the documented root + excludes** (observed live 2026-07-11).
- [ ] `verify_index` clean after each full refresh; `/handoff` flags stale roots.

### Task C6.3 — Close with evidence

- [ ] All validation layers green; indexes refreshed and verified; health snapshots recorded.
- [ ] AS-IS / AFI / LESSONS / GOOD-PRACTICES updated from the preparation findings.
- [ ] `/handoff` generated; evidence packet committed; every epic's criteria link to a command result, test, file, or ADR.

---

## Decision register — ALL DECIDED 2026-07-11 (records in `decisions/`)

| # | Decision | Outcome | ADR |
|---|---|---|---|
| D-1 | Repository boundary | One repo rooted at `03_PKE_SA_NQA1` | ADR-0001 |
| D-2 | `sieving/DATA` policy | Out of git; checksum manifest tracked; external backup location **still to be designated** (open action) | ADR-0002 |
| D-3 | Canonical schema owner | `Enconet/schemas/*.yml` | ADR-0003 |
| D-4 | Context disposition | `docs/_archive/`, post-G0 migration, never delete | ADR-0004 |
| D-5 | Dual-agent policy | Both agents + drift validation | ADR-0005 |
| D-6 | Master plan candidate | v1.3-CX merged → published as canonical v1.4 (done) | ADR-0006 |
| §8-1…6 | Domain decisions | naming / scoring deferral to G3 / language sl-en-hr / SQLite / 18 pages / scope-or-nonconformance | ADR-0008…0013 |

GUI disposition: closed 2026-07-04, backfilled as ADR-0007.

**Next action: EPIC C0 (wave G0) — git recovery and first clean commits.**

*End of Alignment Plan — canonical, published 2026-07-11.*
