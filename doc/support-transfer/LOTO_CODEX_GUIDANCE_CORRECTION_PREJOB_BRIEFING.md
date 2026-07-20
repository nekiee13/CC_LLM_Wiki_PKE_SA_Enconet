---
record_type: slice_prejob_briefing
target: CC_Loto
slice: codex-guidance-vocabulary-correction
version: 1
recorded_at_utc: 2026-07-20T03:02:47Z
authorized_by: LOTO_GUIDANCE_ALIGNMENT_APPROVAL.md item 1
implementer: codex
reviewer: claude-code
target_parent: d5dc65e568ee73d82389e6e1d3fdf24122661adf
status: pre-write-review-required
---

# CC_Loto Codex guidance vocabulary correction — pre-job briefing

## Gate and ownership

This packet opens Claude's independent pre-write review only. It authorizes no CC_Loto write,
commit, push, Claude-owned edit, synchronization claim, or M4 transition. Codex owns and would edit
`AGENTS.md`; Claude Code reviews. The later Claude-owned alignment slice remains closed until this
slice is published and independently closed.

## Exact content scope

Content commit A would modify exactly root `AGENTS.md`, replacing parent object
`34b7eb93095022bea137e2a0c2313f356bfa0f28` with reviewed candidate object
`42571a2c5f67b5a11759f38d7d65f50f156087c3`.

The sole semantic correction is:

- replace the invalid check enumeration containing `blocked` and lacking `not-configured`;
- install the canonical states `passed`, `failed`, `skipped`, `not-run`, `unknown`,
  `not-configured`, and `unavailable`;
- state that `blocked` is a handoff/blocker state, never a check result;
- preserve the later warning about validation prevented by a real blocker.

Diffstat is exactly 3 additions, 2 deletions. No `CLAUDE.md`, `.claude/`, `.agents/`, product,
dependency, test, workflow, data/model/output, index, tag, or release path is in A.

## Review authorities

- [`LOTO_GUIDANCE_ALIGNMENT_APPROVAL.md`](LOTO_GUIDANCE_ALIGNMENT_APPROVAL.md)
- [`LOTO_CODEX_GUIDANCE_CORRECTION_RENDER_EVIDENCE.md`](LOTO_CODEX_GUIDANCE_CORRECTION_RENDER_EVIDENCE.md)
- [`LOTO_CODEX_GUIDANCE_CORRECTION_DRY_RUN_EVIDENCE.md`](LOTO_CODEX_GUIDANCE_CORRECTION_DRY_RUN_EVIDENCE.md)
- [`rendered/render_loto_codex_guidance_correction.py`](rendered/render_loto_codex_guidance_correction.py)
- [`rendered/loto-codex-guidance-correction/AGENTS.md`](rendered/loto-codex-guidance-correction/AGENTS.md)

## Immediate preflight before any target write

1. Require live/local/fetched `main == d5dc65e...`, divergence 0/0, empty porcelain, and zero tags.
2. Require `AGENTS.md == 34b7eb93` and `CLAUDE.md == 3edd8750`.
3. Require this complete packet commit on Wiki `origin/main` and Claude's explicit acceptance.
4. Rerun the reviewed renderer with the target-requirements interpreter; require candidate SHA-256
   `44E3AC42...AA2AC`, object `42571a2c`, 3/2 diffstat, one-path overlay, aggregate success,
   BOARD identity, and native 42/30/3.

Any mismatch stops the slice before write.

## Proposed A/B protocol after acceptance

1. Stage only `AGENTS.md`; compare the staged object to `42571a2c`; run staged diff check; commit A.
2. At clean A, repeat exact semantic checks, installed aggregate, direct coordination validation,
   BOARD identity, and native 42/30/3.
3. Render evidence B from committed A: append-only `support/log.md` plus replaceable
   `support/current-status.md`, recording literal commands/exits, exact objects, owner approval,
   Claude review, the still-pending Claude-owned alignment slice, and M4 closed.
4. Stage only those two shared-neutral evidence paths, prove the log prefix and exact objects, commit
   B, and repeat validation at clean B.
5. Keep A/B local until Claude independently accepts the committed objects and explicitly authorizes
   the exact normal fast-forward push. Report live state for Claude's closure review afterward.

Recovery, only on owner/reviewer direction, is a new revert of B followed by A. No reset, force push,
broad cleanup, or unrelated restoration is authorized.

## Stop conditions

Stop on target drift, any path beyond the exact A/B sets, candidate/object mismatch, alteration of
the preserved blocker warning, any Claude-owned edit, synchronization overclaim, failed aggregate or
native check, BOARD change, sensitive/product artifact, or reviewer finding. M4 remains closed.
