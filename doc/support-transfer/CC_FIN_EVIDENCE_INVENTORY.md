# T1.1 — CC_FIN support evidence inventory

## Control and verification

| Field | Value |
|---|---|
| Inspected | 2026-07-17, read-only |
| Repository | `C:\xPY\xPrj\CC_FIN`; `https://github.com/nekiee13/CC_FIN` |
| Branch / HEAD | `main`; `238c207c73970f3d3c6dc00c2db5932ebeca7be4` |
| Upstream | `origin/main` at the identical SHA |
| Worktree | Clean |
| Planning baseline | `238c207` |
| Drift disposition | `accepted/no-impact`: current HEAD equals planning baseline; no replan required |
| Size snapshot | 1,052 tracked files; 229 tracked Python files; 111 tracked test-path files |
| Target writes | None |

Commands used included `git rev-parse`, `git status --short --branch`, `git ls-files`,
`git tag --list`, targeted `rg`, file reads, and Git history inspection. No test, build,
generator, formatter, migration, or repair command was run.

## Authority and disposition inventory

| Artifact/capability | Evidence | Disposition | Transfer consequence |
|---|---|---|---|
| Product upgrade plan | `docs/project/CC_FIN_project_upgrade_plan_enhanced.md` v2, header `Status: Proposed` | **Retain; owner-designated product authority** | M1 must explicitly accept the owner designation despite the stale `Proposed` label; support backlog stays separate |
| Architecture / functional analysis | `docs/project/Architectural_and_functional_analysis.md` | **Retain** | Link from support navigation; do not copy |
| AS-IS | `docs/project/AS-IS.md`, source commit `d69c59d` | **Retain as dated snapshot** | Support status must not treat it as live HEAD evidence |
| Project documentation index | `docs/project/README.md`; `docs/README.md` is existing authoritative docs entrypoint | **Integrate** | New support index links both without shadowing them |
| Codex guidance | root `AGENTS.md` | **Retain; Codex-owned** | Extend only in T4 under Codex claim |
| Claude guidance | No root `CLAUDE.md` | **Missing** | Claude creates its owned side in T4 |
| Agent skills | No project `.agents/` or `.claude/` support skill set | **Not configured** | Skills module disabled initially; global handoff skill is optional convenience only |
| Git workflow | `docs/governance-transition.md`: direct trunk work on `main` | **Integrate with safety correction** | Preserve single-developer direct-main flow; do not add default PR ceremony |
| Hosted governance | PR template, M5 exception issue form, three follow-up-ML workflows | **Retain/integrate** | No hosted mutation without separate approval |
| CI gate | `.github/workflows/followup-ml-gate.yml` | **Retain with collision** | Workflow push trigger names `master` while repository branch is `main`; M1 decides whether correction is separately authorized |
| Feature ADRs | `docs/integration-pilot/adr/` register and ADRs 0001–0004 | **Retain as subsystem/historical authority** | Future root ADR register references rather than renumbers or absorbs them |
| Refactor decisions | `docs/refactor/decisions/0001…0002` | **Retain as product-local decisions** | Register/reference strategy required; no silent migration |
| Documentation freshness | `docs/documentation_freshness_ledger.md` | **Integrate** | Preserve file-level owners/status; add support docs when publication begins |
| Product status | Project README and AS-IS snapshots; no unified root current-status record | **Differently implemented / gap** | Support status is added later without replacing product snapshots |
| Handoff | No root `HANDOFF.md`, schema, immutable handoffs, or publisher | **Missing** | Core T5 capability required |
| Coordination | No neutral messages/archive/claims/board/protocol | **Missing** | Dual-agent and multi-writer modules required |
| Improvement knowledge | Product plan has AFIs; no shared AFI/LL/GP lifecycle ledgers | **Partial** | Retain plan AFIs; add support ledgers without duplicating the product backlog |
| Validation | pytest plus CPI and targeted ruff commands in `AGENTS.md`; CI has focused follow-up gates | **Retain/compose** | Support aggregate calls native commands with truthful optional states |
| Release/versioning | Package version `2.1.0`; no Git tags; enhanced plan Epic 16 proposes release-tag convention | **Planned, not implemented** | Do not invent tags; profile records `not-configured` until product task lands |
| Indexing | Prior AS-IS mentions local jcodemunch; no repo-local index profile/ownership contract | **Conditional gap** | Recommend docs/code index module because vendor and generated corpora require strong exclusions |
| Record taxonomy/navigation | Fragmented across project, refactor, OC, pilot, freshness, and runbook docs | **Gap with rich inputs** | Create one support navigation layer; existing authorities stay in place |

## Native validation contract

| Check | Command | Applicability |
|---|---|---|
| Install | `python -m pip install -r requirements.txt` | Required for a fresh environment; mutating, not run during T1 |
| Full tests | `python -m pytest` | Required before support release |
| Focused import | `python -m pytest tests/test_infra.py::test_import_loading_module` | Required preflight smoke |
| CPI | `python -m pytest --run-cpi -m cpi` | Optional/configured only when CPI dependencies and runtime are available |
| Lint | `python -m ruff check src compat scripts tests tools` | Required for changed support Python; existing repo-wide debt must not be silently reclassified |
| Entrypoint smoke | `python scripts/app3G.py --help` | Required preservation smoke |

No result state is assigned here because these commands were not run during read-only T1.

## Data, secrets, and index sensitivity

- `.env` is ignored and the application loads it; records must never include its content.
- No credential/API-key variable was found in the targeted source scan. Environment variables are
  primarily paths, feature switches, and runtime controls (`FIN_DYNAMIX_REPO`,
  `FIN_DYNAMIX_PY_EXE`, `FIN_PCE_PY_EXE`, `FIN_DEBUG_DIR`, database paths, and related flags).
- Tracked operational/source datasets exist under `data/raw/`, `CSV_OUTPUT/`, `XL/`, and
  `config/followup_ml_value_assign.csv`. They are product evidence, not support records.
- Vendored trees and archives are large and contain their own generated/configuration examples.
- Support docs/code indexes must exclude `.env`, `data/raw/**`, `CSV_OUTPUT/**`, `XL/**`,
  `out/**`, `graphs/**`, `debug_artifacts/**`, `.tmp/**`, `vendor/**`, archive tarballs,
  caches, and generated documentation snapshots unless a separately approved profile includes them.
- Handoffs may name paths and committed SHAs but must not embed datasets, environment values,
  credentials, model artifacts, or generated market outputs.

## Verified product preservation facts

- Two original chart families remain implemented.
- The third Forecast Decision Cockpit A–F is implemented through
  `scripts/render_cockpit.py` and `src/charts/cockpit.py`.
- Product-plan Task 23.12 remains `SEEDED`: automatic `analysis_pipeline` wiring is pending.
- Support work must not change any of those states or claim product completion.

## Collisions and open dispositions for M1

1. **FIN-C01 — Product plan control label.** Owner designates the enhanced plan as the product
   authority, but its header says `Proposed`. Recommendation: accept authority now and leave any
   product-plan status edit to the product-plan owner/workflow.
2. **FIN-C02 — Guidance factual drift.** `AGENTS.md` says `pyproject.toml` is empty; it is a
   populated package stub. Recommendation: Codex corrects its owned guidance during T4.
3. **FIN-C03 — CI branch mismatch.** Focused gate triggers pushes to `master`, while active branch
   is `main`. Recommendation: authorize a separate one-line hosted-workflow correction with native
   CI review, or explicitly defer it as product governance debt.
4. **FIN-C04 — Destructive divergence example.** `docs/governance-transition.md` presents
   `git reset --hard origin/main`. Recommendation: replace with an approval-gated recovery
   procedure that inventories unpushed work and offers non-destructive alternatives first.
5. **FIN-C05 — Hosted protection unknown.** Branch-protection settings were not verified because
   GitHub CLI is unavailable. Recommendation: record `unknown`, do not infer protection, and verify
   through an authorized GitHub surface before hosted changes.

## T1.1 acceptance

- Existing support-like artifacts have explicit dispositions.
- Enhanced product plan remains separate and owner-designated.
- Planned capabilities are not reported as implemented.
- Baseline drift is zero and classified `accepted/no-impact`.
- No target file was created, edited, staged, or generated.

