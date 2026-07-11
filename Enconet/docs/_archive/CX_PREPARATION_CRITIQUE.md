# Enconet Preparation Critique

## Scope and method

This critique covers the current `03_PKE_SA_NQA1/Enconet` checkout, the complete indexed
documentation corpus, and the Python sieving subsystem. A finding is included only when it
identifies a concrete problem and proposes a resolution.

Follow-up review, accepted corrections, five additional findings, and the agreed implementation
start gate are recorded in `CX_CC_RECONCILIATION.md`. Where the documents differ, the
reconciliation controls the current CX position.

Evidence collected on 2026-07-11:

- jdocmunch: `local/PKE_SA_NQA1_Enconet_docs` (17 documents, 949 sections).
- jcodemunch: `local/Enconet-0a063bd7` (31 Python files, 186 symbols).
- Local structure and Git probes.
- `python -m pytest -q -p no:cacheprovider` and `python verify_install.py` probes.

## Findings

### P0-1 - The working tree has no verifiable Git identity

**Problem.** No `.git` boundary is visible from `LLM_Wiki`, `03_PKE_SA_NQA1`, or `Enconet`.
The preparation therefore cannot establish the remote URL, current branch, HEAD SHA, upstream,
dirty state, or whether the files came from the cited backup. This conflicts with the requested
append-only/Git-backed records and Master Plan Task 0.6.

**Resolution.** Recover the actual clone or repository metadata before implementation. Record
remote, branch, SHA, and a local-versus-remote manifest. Do not initialize unrelated history until
it is confirmed that the original metadata cannot be recovered.

### P0-2 - Invalid audit filters fail open and can export widened results

**Problem.** `sieving/src/json_extractor/pipeline.py` catches filter parse/execution failures and
returns the unfiltered DataFrame. `sieving/cli.py` exits only when the user supplies
`--strict-filter`; otherwise it can preview or export all records. An invalid audit restriction
must not silently become a broader evidence set.

**Resolution.** Fail closed by default. Return a typed failure or raise a domain error, block
export whenever `filter_error` exists, and reserve fail-open preview for an explicit development
option. Add tests proving invalid filters create no output.

### P0-3 - Moved repair utilities resolve the wrong root and include destructive behavior

**Problem.** `sieving/tools/check_files.py`, `fix_files.py`, and `fix_structure.py` set
`project_root = Path(__file__).parent`, which resolves to `sieving/tools`, while their path tables
assume `sieving`. `fix_structure.py` recursively deletes directories and creates package files
under this incorrect root. Comments claim the scripts run from project root, but CWD is ignored.

**Resolution.** Do not run these utilities. Replace parent assumptions with a tested root resolver
or explicit `--project-root`. Convert checks to read-only manifest validation. Retained mutators
require dry-run, explicit targets, transactional backup, and fixture tests; otherwise archive them.

### P1-1 - Active documentation advertises a GUI that does not exist

**Problem.** `sieving/README.md`, `QUICKSTART.md`, `PROJECT_INFO.md`, and `tools/check_files.py`
describe `streamlit run app.py`, but no `app.py` exists and requirements declare no Streamlit
dependency. This appears in active quick-start and verification instructions, not only future plans.

**Resolution.** Make a scope decision. Implement/test the GUI with a declared dependency, or mark
it deferred and remove active commands/checks. Keep planned interfaces in AFI/master planning.

### P1-2 - The master-plan hierarchy does not match the approved workspace hierarchy

**Problem.** The target root is `PKE_SA_Enconet/` and its CLAUDE/skill model assumes a standalone
project. The approved structure is `03_PKE_SA_NQA1/Enconet`, with global docs, shared `CLAUDE.md`,
and reusable skills at `03_PKE_SA_NQA1`. The plan omits the requested global `doc` ownership model.

**Resolution.** Recast the plan around workspace/project ownership. Put general architecture,
functional analysis, AS-IS, AFI, practices, lessons, record policy, and shared skill inventory in
`03_PKE_SA_NQA1/doc`; keep Enconet specifics under Enconet. Use a short project CLAUDE file that
inherits the root contract.

### P1-3 - Session continuity is a checklist, not an atomic handoff mechanism

**Problem.** Master Plan Tasks 0.3 and 14.3 require status, index, log, and project-state files,
but specify no executable `/handoff` skill, immutable records, required fields, atomic publication,
validation evidence, or drift detection. Four manual state surfaces can disagree while each looks valid.

**Resolution.** Implement the shared `/handoff` contract in `CX_ALIGNMENT_PLAN.md`. Generate an
immutable timestamped record plus a validated pointer, append one log event, and compare handoff,
Git, project state, and current status at session start. Incomplete publication must fail visibly.

### P1-4 - Historical context is mixed with unrelated projects and treated as grounding input

**Problem.** `docs/context/23 FINAL PROJECT FILL-IN.md` contains Travel Guide, internal procedure,
finance, Linux VM, Git recovery, and supplier-audit sessions, including obsolete `/home/...` roots.
Context 32 contains `F:\xPy\Json`. The master plan lists these exports as grounding inputs without
an authority classification, encouraging path and domain leakage.

**Resolution.** Catalog files as historical evidence, examples, stubs, or candidate requirements.
Extract accepted requirements into controlled docs with provenance links. Reject legacy paths in
active docs/code while permitting explicitly marked historical blocks.

### P1-5 - Canonical audit contracts are duplicated across code, prompts, and plans

**Problem.** Appendix B criteria/codes are hard-coded in `config.py`, overlap with
`templates/app_b.py`, and recur in prompts/plans. Query fields and exporter columns add more
copies. Future YAML schemas are planned, but current code has no single owner or migration rule.

**Resolution.** Establish one versioned machine-readable owner for taxonomy, codes, crumb schema,
query fields, and export columns. Runtime code, prompt validation, docs, and fixture checks should
load or generate from it. Add drift and schema-migration tests before modifying DATA.

### P1-6 - The codebase cannot currently be validated on the second machine

**Problem.** Pytest cannot start because `pytest` is absent. `verify_install.py` confirms that
`pandas` and `openpyxl` are absent. Only lower-bound dependencies are supplied, with no clean-machine
bootstrap/lock evidence or successful test record.

**Resolution.** Document a virtual-environment bootstrap, supported Python versions, and constrained
or locked runtime/test dependencies. Run the complete suite in a clean environment and add CI after
the Git boundary is restored.

### P1-7 - Windows portability fails in the installation verifier

**Problem.** On the default CP1252 console, `python verify_install.py` crashes on its first Unicode
checkmark. With `PYTHONUTF8=1`, it proceeds to dependency diagnostics. This hides the useful result
and contradicts the cross-machine objective.

**Resolution.** Use ASCII markers or an output abstraction with encoding detection and fallback.
Add a non-UTF-8 subprocess test so the verifier returns diagnostics rather than crashing.

### P1-8 - Default paths depend on CWD and configuration creates directories eagerly

**Problem.** `Config.data_dir` defaults to `Path("./DATA")`; `Config.__post_init__` immediately
creates data and user-config directories. Launching from another directory changes input roots and
mutates that directory merely by obtaining configuration. This is unsuitable for controlled inputs.

**Resolution.** Resolve default DATA from the project/package root, allow explicit overrides, and
separate path calculation from directory creation. Input discovery must not create missing input
directories. Test multiple launch directories.

### P2-1 - The documentation corpus is indexed but not navigable

**Problem.** jdocmunch reports no broken links but 933/949 sections have no inbound cross-document
reference. Lack of links is being mistaken for link health. Three structural warnings indicate
swallowed headings, and there is no Enconet/global docs index.

**Resolution.** Add workspace, global-doc, Enconet-doc, and wiki indexes. Link current docs by
requirement, architecture, implementation, test, and decision. Exclude classified historical
context from the controlled-doc orphan gate while keeping it cataloged.

### P2-2 - Test evidence is narrow and one advertised test file is empty

**Problem.** `tests/test_export_sync.py` contains only a header. jcodemunch heuristics identify
50/99 non-test functions/methods as untested (49.5% reached), including configuration, I/O,
flattening, CLI, and exports. Existing OR tests do not cover relocation, failure atomicity,
invalid-filter export, repair tools, or Windows behavior.

**Resolution.** Replace the empty test with export contract tests and prioritize filter failure,
path resolution, schema drift, mutating utilities, bad files, and CLI exit codes. Treat jmunch
reachability as heuristic and add measured coverage in CI.

### P2-3 - Verification reports cascaded imports as separate installation errors

**Problem.** `src/json_extractor/__init__.py` eagerly imports `pipeline`, which imports pandas.
The verifier then reports six module/attribute import failures when pandas is absent, obscuring one
dependency problem as structural failures and recommending a structure repair script.

**Resolution.** Check dependencies before package imports, distinguish dependency from structure
errors, and remove misleading repair advice. Consider lazy public imports if lightweight submodule
use is intended.

### P2-4 - The stated baseline both underclaims and overclaims implementation

**Problem.** The preparation premise says only the master plan exists, but the tree contains a
substantial sieving subsystem, 60+ JSON examples, CLI, query DSL, exporters, tests, and repair tools.
Conversely, planned DB, wiki, report, dashboard, state machine, and validators do not exist.

**Resolution.** Build `doc/AS-IS.md` from verified files and executable checks. Distinguish
working, present-but-unverified, planned, deferred, and retired states. Link working claims to code
and tests; put missing capabilities in AFI and the master plan.

## Verified positives and residual risk

- The code index found no Python import dependency cycles.
- DATA discovery is recursive and deterministically sorted.
- The docs index has no syntactically broken internal Markdown links.
- The master plan already contains evidence constraints, human gates, a continuity triad, and
  incremental validation intent. The defect is incomplete integration and workspace mismatch.

These are static observations. Runtime behavior remains unverified until dependencies are installed
and tests pass on this machine.
