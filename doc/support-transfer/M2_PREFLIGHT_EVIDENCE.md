# M2 preflight evidence — CC_FIN

Collected read-only on 2026-07-18 by claude-code under claim
`SUPPORT-TRANSFER-M2-PREFLIGHT`. No CC_FIN file was created, modified, or deleted; the
worktree was verified clean (`git status --porcelain` empty, exit 0) before and after
every step, including after the native test runs (bytecode and cache writes suppressed
with `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`; the JUnit report was written
outside the repository).

## 1. Target identity and recovery point

| Fact | Value | Command (exit 0) |
|---|---|---|
| HEAD | `238c207c73970f3d3c6dc00c2db5932ebeca7be4` | `git -C C:/xPY/xPrj/CC_FIN rev-parse HEAD` |
| Baseline drift | None — HEAD equals the M1-accepted baseline exactly | comparison with `M1_APPROVAL.md` baseline |
| Branch / upstream | `main` / `origin/main`, `0 0` ahead-behind | `git branch --show-current`; `git rev-list --left-right --count HEAD...@{u}` |
| Remote | `https://github.com/nekiee13/CC_FIN.git` | `git remote get-url origin` |
| Worktree | clean | `git status --porcelain` (empty) |

**Recovery anchor for the M2 publication: `238c207c73970f3d3c6dc00c2db5932ebeca7be4`**
(the M1-accepted baseline; slice 1 starts here). Each later slice records and verifies
its own clean pre-slice parent HEAD and reverts only its named commits back to that
parent (M2-F4); rollback is revert-only per `PUBLICATION_ROLLBACK_MANIFESTS.md`, and the
staged rehearsal proving this procedure is accepted T6.4 evidence.

## 2. Target-native baseline checks

Command: `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider
--continue-on-collection-errors -q` from `C:/xPY/xPrj/CC_FIN`; exit code `1`.

Result: **343 tests: 276 passed, 51 failed, 3 collection errors, 13 skipped** (14.5 s).

Machine-verified classification of the 54 failure/error outcomes (corrected per M2-F1;
full node-level fingerprint in `M2_BASELINE_FAILURE_SET.md`):

| Class | Count | Detail |
|---|---|---|
| `import-unavailable: torch` | 24 (21 failures + 3 collection errors) | `torch==2.6.0` is **pinned in `requirements.txt`** — a declared project dependency, not an optional test extra — but is not installed in this machine's interpreter |
| `import-unavailable: matplotlib` | 11 | `matplotlib==3.7.5` likewise pinned in `requirements.txt` and not installed |
| Assertion failures | 19 | observed set spans date-comparison assertions (e.g. `'2026-03-27' == '2026-03-26'`), QA status-code assertions, and sign/value assertions; all 19 are proven pre-existing at the untouched baseline, but **no common root cause is established** — some may be date-sensitive, others are not (M2-F5) |

Truthful state for M2 purposes: the baseline is **not green in this environment**, and
the 35 import outcomes reflect an interpreter that does not satisfy the project's own
declared dependencies. The 19 assertion failures are pre-existing at the untouched
baseline (`238c207`, no support file present); their causes are recorded as observed,
not attributed. The owner's explicit choice between establishing the declared dependency
environment first and accepting the fingerprinted red baseline is put in the packet.

## 3. Publication-manifest dry run (no writes)

Every planned **new** path from the CC_FIN manifest is collision-free (does not exist):
`support/`, `coordination/`, `HANDOFF.md`, `scripts/agent_coord.py`,
`scripts/make_handoff.py`, `scripts/validate_support.py`.

Every manifest-listed **existing modifiable** path is present: `AGENTS.md`,
`docs/README.md`, `docs/governance-transition.md`,
`.github/workflows/followup-ml-gate.yml`, `.gitignore`.

The known workflow defect is confirmed still present: `followup-ml-gate.yml` line 6
filters on `master` while the repository branch is `main` (M1 item 8 authorized the
isolated correction).

The exact per-slice create/modify inventory, ownership classification, rendered diffs
for existing files, and the disposable-copy render/validation evidence are in
`M2_DRY_RUN_MANIFEST.md` (M2-F3).

## 4. Staged-executable evidence

Accepted at `852d9e4`: `T6_STAGED_EXECUTABLE_CHECKPOINT.md`, 67/67 disposable-root
tests, Codex acceptance `CX_2026-07-17T222326Z` (archived). The publisher/validator
files are copy-ready for `scripts/` per the T4/T5 contracts.
