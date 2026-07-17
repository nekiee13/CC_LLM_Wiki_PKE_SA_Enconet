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

**Recovery point for every M2 slice: `238c207c73970f3d3c6dc00c2db5932ebeca7be4`.**
Rollback is revert-only per `PUBLICATION_ROLLBACK_MANIFESTS.md`; the staged rehearsal
proving this procedure is accepted T6.4 evidence.

## 2. Target-native baseline checks

Command: `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider
--continue-on-collection-errors -q` from `C:/xPY/xPrj/CC_FIN`; exit code `1`.

Result: **343 tests: 276 passed, 51 failed, 3 collection errors, 13 skipped** (14.5 s).

Root-cause classification of the 54 failures/errors:

| Class | Count | Detail |
|---|---|---|
| `ModuleNotFoundError: torch` | 21 (18 failures + 3 collection errors) | ANN training/eval modules; torch is not installed in this machine's default interpreter |
| `ModuleNotFoundError: matplotlib` | 11 | chart/panel render tests |
| Assertion failures | 22 | predominantly date-comparison assertions (e.g. `'2026-03-27' == '2026-03-26'`, `'2025-08-01' == '2025-07-30'`) and `QA_FH3_MISSING` status assertions — consistent with date-sensitive tests evaluated on 2026-07-18, not with any repository change (HEAD is the untouched M1 baseline) |

Truthful state for M2 purposes: the baseline is **not green in this environment**. The
environment classes (torch, matplotlib) are machine limitations, `unavailable` in the T5
vocabulary. The 22 assertion failures are pre-existing at the untouched baseline and
owner disposition is required on how the M2 gate treats them (see packet). Support
transfer changed nothing: the identical failure set exists at `238c207` with no support
file present.

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

## 4. Staged-executable evidence

Accepted at `852d9e4`: `T6_STAGED_EXECUTABLE_CHECKPOINT.md`, 67/67 disposable-root
tests, Codex acceptance `CX_2026-07-17T222326Z` (archived). The publisher/validator
files are copy-ready for `scripts/` per the T4/T5 contracts.
