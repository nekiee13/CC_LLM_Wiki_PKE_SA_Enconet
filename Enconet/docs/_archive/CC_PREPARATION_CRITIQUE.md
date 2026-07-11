# CC Preparation Critique — 03_PKE_SA_NQA1 / Enconet

## 0. Document control

| Field | Value |
|---|---|
| Document | CC_PREPARATION_CRITIQUE.md |
| Prepared | 2026-07-11 |
| Author | Claude Code (CC) |
| Scope | `03_PKE_SA_NQA1/Enconet` checkout: documentation corpus, sieving subsystem, jmunch indexes, and the CX preparation documents |
| Companion | `CC_ALIGNMENT_PLAN.md` (remediation plan for every finding below) |
| Evaluates | `CX_ALIGNMENT_PLAN.md`, `CX_PREPARATION_CRITIQUE.md` (2026-07-11) |
| Validity rule | A finding is included only when it names a concrete problem **and** proposes a resolution |

## 1. Method and evidence base

Independent verification performed on 2026-07-11 (not a re-statement of CX evidence):

- **Full reads:** `MASTER_DEVELOPMENT_PLAN.md` (all 1474 lines), `Sieving_method_specification_Guide.md` v1.1, `docs/context/30/31/35/36/40`, sieving docs (`README.md`, `QUICKSTART.md`, `PROJECT_INFO.md`, `PROVENANCE.md`), CX documents.
- **Code reads:** `pipeline.py`, `config.py`, `cli.py`, `templates/app_b.py`, `query/schema.py` (excerpts), `extract/load_and_flatten.py` (validation core, via targeted search), `tools/check_files.py`, `tools/fix_files.py`, `tools/fix_structure.py`, `verify_install.py`, `src/json_extractor/__init__.py`, `tests/test_export_sync.py`, `requirements.txt`, `pytest.ini`.
- **Runtime probes:** Python 3.13.9; import probes for pandas / openpyxl / pytest / typer / rich; live execution of `verify_install.py`.
- **Index queries:** jcodemunch `local/Enconet-0a063bd7` (get_repo_health, find_dead_code), jdocmunch `local/PKE_SA_NQA1_Enconet_docs` (get_doc_health, get_index_overview).
- **Sweeps:** grep for legacy paths (`/home/nekiee`, `F:\xPy\Json`, `LLL_Wiki`, `PKE_SA_Enconet`), GUI references (`streamlit`, `app.py`), and contract duplication (`APP_B_I` tables).

## 2. Verdict on the CX documents

**Overall: the CX critique is substantially correct and the CX plan structure is sound.**
Of the 15 CX findings, 13 are independently confirmed, 2 require correction, and the CX
documents have five material gaps (CC-1…CC-5, Section 4). `CC_ALIGNMENT_PLAN.md` adopts
the CX epic skeleton with amendments rather than replacing it.
*(Correction 2026-07-11: this sentence originally said "4 material gaps" against five
enumerated findings — the count inconsistency was caught by `docs/CX_CC_RECONCILIATION.md`
§2.3 and is fixed here.)*

### 2.0 Concurrency note — master plan v1.1 landed during this preparation

While this critique was being prepared, `MASTER_DEVELOPMENT_PLAN.md` was amended to
**v1.1** (2026-07-11, +49 lines): Task 0.7 adds the shared `/handoff` skill at
`03_PKE_SA_NQA1/.claude/skills/handoff/`; Task 0.2 now extends `../CLAUDE.md` instead of
`/home/nekiee/LLL_Wiki/CLAUDE.md`; Task 14.3 integrates handoff into session protocol.
Verdicts P1-2 and P1-3 below were verified against the v1.0 baseline; **v1.1 resolves the
P1-3 mechanism gap and the Task 0.2 path defect**. The amendment itself, however,
demonstrates the drift class this preparation exists to prevent:

- the H1 title and closing footer still read "v1.0" while document control reads 1.1 —
  the same document now carries two version claims;
- §4 target layout is still rooted at `PKE_SA_Enconet/`;
- document control has no amendment-log row stating what changed and why;
- a **byte-identical duplicate** `CX_MASTER_DEVELOPMENT_PLAN.md` was left at the Enconet
  root beside the amended original (verified: diff clean, same size/mtime). Two copies of
  the authority document guarantee drift the moment either is edited — and the
  pre-amendment v1.0 text was preserved in *neither* (no git history exists to recover it).

**Resolution.** Folded into `CC_ALIGNMENT_PLAN.md` Task C1.3 (version-string consistency,
§4 re-root, amendment log, duplicate removal). Task 0.7's contract is adopted as canonical
by CC EPIC C3.

### 2.1 Per-finding verdict table

| CX finding | Verdict | Independent evidence |
|---|---|---|
| P0-1 No verifiable Git identity | **Confirmed** | Only `.git` under `02_PKE_Procedure_revision`; `git status` fails at `LLM_Wiki` root. Consequence: `sieving/PROVENANCE.md` claims GUI "recoverable from git history (commit b315f05)" — that history is not on this machine. |
| P0-2 Filters fail open, export widened results | **Confirmed, with framing correction (4.1)** | `pipeline.py:207–214`: on `DSLParseError` **or any exception**, `df` remains unfiltered. `cli.py:181–186`: exit 2 only with `--strict-filter`; otherwise execution continues to preview **and export** of the unfiltered frame. |
| P0-3 Tools resolve wrong root; destructive behavior | **Confirmed and worse (4.3)** | `check_files.py:39`, `fix_files.py:18`, `fix_structure.py:18` all set `project_root = Path(__file__).parent` → `sieving/tools`. `fix_structure.py` uses `shutil.rmtree` and silently **creates** a phantom `src/json_extractor/...` skeleton under `tools/` (lines 84–85). |
| P1-1 Docs advertise a GUI that does not exist | **Confirmed, with correction (3.1)** | `README.md` ("Dual interfaces", `streamlit run app.py`), `QUICKSTART.md:23/159/230`, `PROJECT_INFO.md:268`, `check_files.py:44`. But the GUI question is **not open** — see 3.1. |
| P1-2 Master plan hierarchy mismatch | **Confirmed vs v1.0; partially resolved by v1.1 (see 2.0)** | v1.0 §4 roots the tree at `PKE_SA_Enconet/` (still true in v1.1); v1.0 Task 0.2 required extending `/home/nekiee/LLL_Wiki/CLAUDE.md` (fixed in v1.1). |
| P1-3 Continuity is a checklist, not a handoff mechanism | **Confirmed vs v1.0; resolved in v1.1 by Task 0.7 (see 2.0)** | v1.0 Tasks 0.3/14.3 defined four manual state surfaces with no executable `/handoff`, no atomicity, no drift detection. v1.1 Task 0.7 supplies the mechanism; implementation remains open. |
| P1-4 Historical context treated as grounding input | **Confirmed** | `context/23` carries `/home/nekiee/LLL_Wiki/...` trees, Travel Guide / finance / Linux material; `context/32` carries `F:\xPy\Json` and the superseded v0.1 tool description. Master plan §0 lists both as grounding inputs without authority classification. |
| P1-5 Canonical contracts duplicated | **Confirmed and worse (4.2)** | The 18-pair criteria table is hard-coded twice in code (`config.py:144–163`, `app_b.py:29–48`) plus twice in the prompts (context/31). The two code copies are not even shape-identical: `config.get_canonical_codes()` carries `allowed_locators`/`locator_pattern`; `AppBTemplate.CANONICAL_CODES` does not. Validation (`load_and_flatten.py:326`) reads the **config** copy; `AppBTemplate` exposes its own competing `validate_criterion_*` methods. |
| P1-6 Codebase cannot be validated on this machine | **Confirmed by probe** | Python 3.13.9 present; `pandas`, `openpyxl`, `pytest` all absent (typer/rich present). `requirements.txt` is floor-pins only; the only test dependency is `pytest>=9.0.2`. |
| P1-7 Windows portability failure in verifier | **Reproduced** | `python verify_install.py` crashes with `UnicodeEncodeError: 'charmap' codec can't encode character '✓'` (`cp1252.py`) on its first structure check. |
| P1-8 CWD-dependent paths; eager directory creation | **Confirmed** | `config.py:25` `data_dir = Path("./DATA")`; `__post_init__` (lines 83–86) `mkdir`s both `./DATA` and `~/.json_extractor` merely on `get_config()`. Running the CLI from any other directory silently reads a different (freshly created, empty) DATA root. |
| P2-1 Corpus indexed but not navigable | **Confirmed, with metric caveat** | jdocmunch: 0 broken links, 987/1005 sections without inbound cross-doc reference, 3 swallowed-heading warnings. Caveat: most orphans are the historical `context/` corpus, which will never be linked — the gate must apply to controlled docs only (CX A6-T1 already says this; the baseline bullet should too). |
| P2-2 Narrow tests; advertised test file empty | **Confirmed** | `test_export_sync.py` = 3 comment lines. Total test corpus 286 lines, all OR-group focused (`test_pipeline_or`, `test_query_dsl_or`, `test_query_engine_or`). Nothing covers export contract, invalid-filter export blocking, path resolution, or the tools. |
| P2-3 Verifier cascades one missing dependency into six errors | **Confirmed and worse (4.3)** | `__init__.py:21` eagerly imports `pipeline` → pandas. All six `verify_install.py` import checks then fail, and the summary advises `python fix_structure.py` — the wrongly-rooted mutating script. A missing dependency is thus converted into advice to run a destructive tool. |
| P2-4 Baseline both underclaims and overclaims | **Confirmed** | The preparation premise ("only Master development plan is prepared") ignores ~31 Python files, 60+ DATA crumb files, tests, and two authority documents; conversely nothing of the planned DB/wiki/report/dashboard layer exists. `doc/AS-IS.md` must be built from verified files. |

### 2.2 CX_ALIGNMENT_PLAN verdict

The epic structure (A0 git baseline → A1 authority/paths → A2 governance → A3 handoff →
A4 code → A5 records/tests → A6 indexes) is correct and is adopted in
`CC_ALIGNMENT_PLAN.md` with the amendments below. Two baseline bullets need correction
(3.1, 3.2); the "Decisions required" list carries one item that is not actually open (3.1);
and the plan text cites index statistics that were already stale the same day (4.4).

## 3. Corrections to CX (points of disagreement)

### 3.1 The GUI disposition is not an open decision

**Problem.** CX A4-T2 asks to "Decide whether `app.py`/Streamlit is implemented now,
deferred, or retired" and lists "GUI disposition" under *Decisions required*. That decision
was already made and recorded by the human on **2026-07-04** in three places:
`sieving/PROVENANCE.md` (divergence log: Streamlit adapter removed), master plan EPIC 15
("Decision (2026-07-04, human): sieving has **no separate GUI**"), and
`Sieving_method_specification_Guide.md` §10.1. Re-opening a recorded human decision as a
pending decision undermines the record-keeping system this preparation is building.

**Resolution.** Reclassify the task as pure documentation alignment: purge
`streamlit run app.py` and GUI claims from `README.md`, `QUICKSTART.md`, `PROJECT_INFO.md`
and the tools; cite the 2026-07-04 decision in each edit. Remove "GUI disposition" from the
open-decision list (done in `CC_ALIGNMENT_PLAN.md` §5).

### 3.2 The dead-code metric is mostly false positives — acting on it would delete the pipeline core

**Problem.** The CX baseline states "20.5% likely dead functions" as a health fact.
jcodemunch `find_dead_code` flags **56 symbols at confidence 1.0**, including
`flatten_multiple_files`, `export_dataframe`, `discover_json_files`, `QueryEngine`, and
the whole of `load_and_flatten.py` / `io/` / `query/engine.py` / `app_b.py`. These are
demonstrably live: `pipeline.py:31–33` imports them **through subpackage `__init__`
re-exports** (`from .extract import ...`, `from .io import ...`, `from .query import ...`),
which the import-graph heuristic does not resolve to the defining modules. The only
provably dead file is `tools/print_run_pipeline_sig.py`. A cleanup driven by this report
would delete the working evidence pipeline.

**Resolution.** Treat `find_dead_code` output as untrusted for this package shape. Before
any deletion, confirm with `find_importers`/`check_references` **and** a plain grep for the
symbol. Record this caveat in the index-profile documentation (CC_ALIGNMENT_PLAN Task C6.2)
so future sessions do not rediscover it. Real dead-code candidates remain: the `tools/`
repair scripts (quarantine per P0-3) and `print_run_pipeline_sig.py`.

## 4. Findings the CX documents missed

### CC-1 — Validation is advisory: ERROR-flagged crumbs still flow into exports (highest-consequence integrity gap)

**Problem.** CX P0-2 covers the *filter* fail-open path but not the deeper one:
`validate_item` only **collects** `ValidationError` objects; `flatten_item_to_record`
still emits the record, and `run_pipeline` puts every row — including rows carrying
VAL-TAX/VAL-EVID/VAL-JOIN **ERROR**s — into the DataFrame and thence into CSV/XLSX
exports. Nothing in the current toolchain can refuse an invalid crumb. For an audit
evidence system this is the single most consequential gap: "REPO-ENFORCED" means
*flagged*, not *rejected*. Additionally, `record_side` itself is never validated — a
missing or misspelled side silently skips **all** side-leak and join checks
(spec guide §2.1). The spec guide records both honestly (§2, §11 items 1–2); the CX
critique, which proposes fail-closed behavior for filters, never mentions that the
validation layer itself fails open.

**Resolution.** Extend the fail-closed epic beyond filters: add a blocking mode to the
pipeline (reject file on any ERROR; `--advisory` opt-out for exploration), validate
`record_side` as a hard enum before side-specific checks, and land the regression tests
first (test-first rule). This is the interim measure until the master plan's import gate
(Tasks 5.3/5.4) exists. Tracked as CC_ALIGNMENT_PLAN Task C4.2.

### CC-2 — The authority document itself misstates the code (spec guide §10.1)

**Problem.** `Sieving_method_specification_Guide.md` §10.1 annotates
`config.py ← Config (canonical criteria/codes via AppBTemplate)`. This is false:
`config.py` imports nothing from `templates/` (its imports are `json`, `pathlib`,
`typing`, `dataclasses`) and hard-codes its own criteria/codes tables. The guide is
otherwise the project's most reliable document ("enforcement details verified against
pipeline source code"), which makes this one wrong claim more damaging: a future session
deduplicating the contracts (P1-5) would reasonably delete the config tables believing
AppBTemplate already feeds them — and break `validate_item`, which reads the **config**
copy (`load_and_flatten.py:326`).

**Resolution.** Correct §10.1 when the single-owner contract lands (one edit, same
commit as the dedup — CC_ALIGNMENT_PLAN Task C4.4), and add the drift test CX proposed so
documentation claims about enforcement are machine-checked against code.

### CC-3 — The broken tools form a self-reinforcing hazard chain

**Problem.** CX reports P0-3 (wrong root, destructive) and P2-3 (import cascade) as
separate findings. The compounding failure is the chain between them: on this machine,
running the advertised verifier (`verify_install.py`) crashes on encoding; run with
`PYTHONUTF8=1` it reports six phantom "structure" errors (pandas cascade) and then
**recommends running `fix_structure.py`** — the wrongly-rooted script that mutates
`sieving/tools/` and would `rmtree` matching directories. A new session following the
documented instructions in order is steered from a missing dependency toward a
destructive repair.

**Resolution.** Break the chain at all three links in one task: verifier checks
dependencies **before** imports and never recommends repair scripts; repair scripts
quarantined to `sieving/tools/_archive/` with a README tombstone; ASCII output.
CC_ALIGNMENT_PLAN Task C4.3.

### CC-4 — `check_files.py` verifies a manifest of a project that no longer exists

**Problem.** Beyond the wrong root, the tool's manifest itself is stale: it requires
`app.py` (removed 2026-07-04), `DATA/example_document.json` and
`DATA/example_regulation.json` (actual layout: `DATA/DOCUMENT/*.json`, `DATA/RULE/*.json`),
and instructs the operator to extract files to `F:\xPy\Json\` — the previous machine's
path — inside an *active* tool, not a historical context file. Even run from the correct
root it would fail and mis-instruct.

**Resolution.** Archive it with the other repair tools. The replacement is a read-only
structure validator driven by a versioned manifest file (CX A4-T1 direction, refined in
CC_ALIGNMENT_PLAN Task C4.3) — not a hand-maintained table inside a script.

### CC-5 — Index statistics quoted without snapshot identity go stale within hours

**Problem.** The CX baseline cites "17 files, 949 sections". By the time the CX documents
were themselves indexed (2026-07-11 00:18), the same index reported **19 docs / 1005
sections** — the CX documents changed the numbers they quote. Any plan that hard-codes
index counts as acceptance evidence will "fail" spuriously after every legitimate doc
addition.

**Resolution.** When citing index metrics in controlled documents, always record the
tuple (repo id, `indexed_at`, doc/symbol count) and treat counts as snapshot evidence,
not acceptance thresholds. Acceptance criteria should test *properties* (0 broken links
among controlled docs; verify_index drift = 0) rather than absolute counts.
Adopted throughout CC_ALIGNMENT_PLAN.

## 5. Verified positives (kept from CX, extended)

- **No dependency cycles** (jcodemunch: 0), and the package layering
  (extract / query / io / templates under one pipeline facade) is clean.
- **The OR-group DSL work is real and tested** (`test_pipeline_or.py`,
  `test_query_dsl_or.py`, `test_query_engine_or.py` — 271 lines of live tests).
- **`Sieving_method_specification_Guide.md` is exemplary**: code-verified enforcement
  tables, an honest known-gaps registry (§11) that anticipated several CX findings, and
  explicit change control. One misstatement (CC-2) does not change that.
- **`PROVENANCE.md` divergence log** is exactly the record-keeping pattern the project
  wants everywhere: date, change, rationale, recovery path.
- **The master plan's design core is sound** — evidence-bounded evaluation, one data
  spine, generational sieving, human gates. Every structural CX/CC finding is about
  *alignment and enforcement*, none required overturning a design principle.

## 6. Priority view

| Priority | Findings | Why first |
|---|---|---|
| P0 | Git identity (P0-1); hazard chain (CC-3, P0-3); fail-closed filters + blocking validation (P0-2 + CC-1) | Irreversibility: destructive tools and unverifiable provenance can silently corrupt the evidence base other work builds on |
| P1 | Master plan / structure reconciliation (P1-2), contract dedup (P1-5 + CC-2), environment bootstrap (P1-6, P1-7), path contract (P1-8), context authority (P1-4), handoff (P1-3) | Everything downstream (EPIC 0+ of the master plan) assumes these |
| P2 | Navigation/indexes (P2-1, CC-5), test breadth (P2-2), doc cleanup (P1-1 as reframed in 3.1), AS-IS baseline (P2-4) | Quality and continuity, not integrity |

Remediation for every finding above is scheduled, with acceptance criteria, in
`CC_ALIGNMENT_PLAN.md`.

*End of CC Preparation Critique — 2026-07-11.*
