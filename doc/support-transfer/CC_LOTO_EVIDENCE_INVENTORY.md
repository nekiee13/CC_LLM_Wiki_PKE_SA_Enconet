# T1.2 — CC_Loto support evidence inventory

## Control and verification

| Field | Value |
|---|---|
| Inspected | 2026-07-17, read-only |
| Repository | `C:\xPY\xPrj\CC_Loto`; `https://github.com/nekiee13/CC_Loto` |
| Branch / HEAD | `main`; `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481` |
| Upstream | `origin/main` at the identical SHA |
| Worktree | Clean |
| Planning baseline | `b469afc` |
| Drift disposition | `accepted/no-impact`: current HEAD equals planning baseline; no replan required |
| Size snapshot | 131 tracked files; 108 tracked Python files; 65 tracked test-path files |
| Target writes | None |

Commands used included Git identity/state/history, tracked-file counts, targeted source/config
searches, `DATA.csv` hashing, and controlled-document reads. No test, install, build, generator,
formatter, model, optimizer, migration, or repair command was run.

## Authority and disposition inventory

| Artifact/capability | Evidence | Disposition | Transfer consequence |
|---|---|---|---|
| Product upgrade plan | `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`, header `Status: Proposed`, body v2.3 additions | **Retain; owner-designated product authority** | M1 explicitly accepts designation; support backlog remains separate |
| Architecture / functional analysis | `docs/architecture.md`; `docs/architectural_and_functional_analysis.md` | **Retain with dated-drift labels** | Link, do not copy; architecture intro contains known packaging drift |
| AS-IS | `docs/AS-IS.md`, snapshot at `c322e13` / Python 3.14 environment | **Retain as historical dated snapshot** | Never use as current test or HEAD evidence |
| Claude guidance | root `CLAUDE.md` | **Retain; Claude-owned** | Claude corrects its factual drift under T4/U0 ownership |
| Codex guidance | No root `AGENTS.md` | **Missing** | Codex creates its owned side in T4 |
| Packaging | `pyproject.toml`, requirements and lockfile | **Retain** | Support installation composes with editable install; no new package manager |
| Native tests | `run_tests.py` layered unittest runner | **Retain exactly** | No pytest assumption; optional layer stays non-blocking/explicit |
| CI | `.github/workflows/ci.yml`: core matrix, optional non-blocking, lockfile job | **Retain/integrate** | Support checks compose with jobs rather than duplicate them |
| Product progress | `docs/PROGRESS.md` tracks completed 21/21 TDD plan and later fixes | **Retain as product-status authority for that plan** | It does not imply enhanced-plan U0–U19 completion |
| Roadmap | `docs/ROADMAP.md` older critique/backlog | **Retain as historical/product input** | Enhanced plan supersedes its upgrade planning, but history remains |
| Documentation governance | Enhanced-plan U7 proposed; no `docs/INDEX.md` yet | **Planned, not implemented** | Integrate support navigation with U7; do not manufacture U7 completion |
| Handoff | No root handoff pointer/schema/publisher/records | **Missing** | Core T5 capability required |
| Coordination | No neutral messages/archive/claims/board/protocol | **Missing** | Dual-agent and multi-writer modules required |
| ADR lifecycle | No unified ADR register | **Missing** | Add target-local register later without rewriting product history |
| Improvement knowledge | Enhanced plan contains AFIs; no AFI/LL/GP lifecycle ledgers | **Partial** | Preserve plan AFIs; add support ledgers separately |
| Release/versioning | Package `0.1.0`; no Git tags or release governance evidence | **Not configured** | Profile records current absence; no invented release claim |
| Indexing | AS-IS references a local jcodemunch snapshot; no repo-local profile contract | **Conditional** | Defer index module initially due small repository; define data exclusion if enabled |
| Agent skills | No paired repo-local support skills | **Not configured** | Skills module disabled initially |

## Native validation contract

| Check | Command | Applicability |
|---|---|---|
| Install | `pip install -e .` | Required fresh-environment setup; mutating, not run in T1 |
| Core/default layers | `python run_tests.py` | Blocking native product validation |
| Optional layer | `python run_tests.py --include-optional` | Non-blocking/conditional; absence is not failure |
| Single layer | `python run_tests.py --layer <layer>` | Focused validation |
| Single pattern | `python run_tests.py --layer core-unit --pattern test_constants.py` | Focused validation |
| CI lockfile smoke | Existing workflow install/import step | Blocking hosted evidence when available |

The live runner includes `core-unit`, `contract`, `optimization-core`, `state-integrity`,
`integration`, `webapp`, and optional layers. Claude guidance omits `webapp`; that is existing
documented AFI-12/U0 drift and must not be copied into the support profile.

## Data, secrets, and index sensitivity

- `DATA.csv` is tracked operational source data with SHA-256
  `49EDC91E6F735C4DE1227AFAA3F2E56069671CA2202B3560586A8105F2773F39` at the inspected baseline.
- It contains draw history rather than credentials, but is product data and must not be embedded
  in handoffs, messages, support ledgers, or documentation indexes. Records may cite path, schema,
  row-count evidence, commit, and checksum.
- `Output/`, model cache, and runtime artifacts are ignored/generated and excluded from support indexes.
- Environment overrides (`DYNAMIX_DATA_FILE`, `DYNAMIX_OUTPUT_DIR`,
  `DYNAMIX_MODEL_CACHE_DIR`) contain paths; records must not expose private machine paths unless
  essential and approved.
- No credential/API-key variable was identified in the targeted product-source scan.
- Support index exclusions, if indexing is enabled later, include `DATA.csv`, `Output/**`, model
  caches, external `DynaMix-python/**`, generated plots/reports, environments, caches, and secrets.

## Collisions and open dispositions for M1

1. **LOTO-C01 — Product plan control label.** Owner designates the enhanced plan as product
   authority, while its header remains `Proposed`. Recommendation mirrors FIN: accept designation
   without editing product-plan status during support transfer.
2. **LOTO-C02 — Claude guidance drift.** Intro says no packaging/requirements and its layer list
   omits `webapp`; current files and runner contradict that. Recommendation: Claude corrects its
   owned guidance in U0/T4, with no Codex edit.
3. **LOTO-C03 — Architecture drift.** `docs/architecture.md` says no packaging and then describes
   an installable package. Recommendation: integrate with U7/U0, retain as dated until corrected.
4. **LOTO-C04 — Status separation.** `docs/PROGRESS.md` reports the earlier TDD plan 21/21 complete;
   the enhanced U0–U19 plan is proposed. Recommendation: preserve both scopes and never roll the
   21/21 claim into enhanced-plan status.
5. **LOTO-C05 — Tracked operational data.** `DATA.csv` is a legitimate product input but unsuitable
   for support records/indexes. Recommendation: classify `controlled product data, tracked by
   product choice`, exclude from support corpora, and leave tracking policy to U5/product authority.
6. **LOTO-C06 — Hosted protection unknown.** GitHub protection could not be queried because GitHub
   CLI is unavailable. Record `unknown`; do not infer or change it.

## T1.2 acceptance

- Custom layered runner and optional-dependency behavior are preserved.
- Progress, roadmap, U7, CI, packaging, data, and enhanced-plan authorities have dispositions.
- Enhanced product plan remains separate and owner-designated.
- Baseline drift is zero and classified `accepted/no-impact`.
- No target file was created, edited, staged, or generated.

