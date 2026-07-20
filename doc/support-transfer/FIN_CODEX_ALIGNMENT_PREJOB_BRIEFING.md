---
record_type: prejob_briefing
task: SUPPORT-TRANSFER-FIN-CODEX-GUIDANCE-ALIGNMENT
target: CC_FIN
target_tip: e74147f3309e1835d28d7c248e00cdcbde2f1796
recorded_at_utc: 2026-07-20T14:25:17Z
prepared_by: codex
review_state: awaiting_claude
target_write: none
---

# CC_FIN Codex guidance minimal-alignment pre-job briefing

## Authorized slice

Complete only the Codex-owned side of accepted ADR-SUP-0001 by changing exactly `AGENTS.md`:

- retain the existing `blocked` warning and add missing `not-configured`;
- add the target-native safe-recovery meaning;
- add the target-native owner-gate non-inference meaning.

This slice does not create or edit `CLAUDE.md`, claim bilateral alignment, update ADR-SUP-0001 from
Pending, or change `.agents/`, `.claude/`, support records, product code, dependencies, tests,
workflows, data/model/output, indexes, tags, or releases.

## Exact authority

| Item | Required value |
|---|---|
| Target parent and live `origin/main` | `e74147f3309e1835d28d7c248e00cdcbde2f1796` |
| Parent `AGENTS.md` object | `d04bf3b8d1167e993e1c5c2d8d9cf33c296b5747` |
| Candidate SHA-256 | `A05D037B0E4F1977018AB52A4697510323961C2134E3F403EFE9195890812474` |
| Candidate Git object | `4cca3734d8c789038b1142a64be2eec2c5edbccc` |
| Expected staged scope | exactly `AGENTS.md` |
| Expected diff | 6 additions, 1 deletion |

The exact render and all attempt evidence are in
[`FIN_CODEX_ALIGNMENT_RENDER_DRY_RUN_EVIDENCE.md`](FIN_CODEX_ALIGNMENT_RENDER_DRY_RUN_EVIDENCE.md).

## Final preflight before target write

Require all of the following in one fresh check:

1. live, fetched, and local `main` remain exact parent `e74147f3` with divergence `0 0`;
2. porcelain is empty and `AGENTS.md` remains object `d04bf3b8`;
3. `CLAUDE.md` remains absent and no overlapping target or Wiki claim exists;
4. target-local coordination exits `0` with 0 errors and 0 warnings;
5. the renderer rerun reproduces candidate SHA-256 and Git object exactly.

Stop on any mismatch, unexpected path, encoding drift, validator mutation, reviewer finding, or
ownership conflict.

## Implementation and validation sequence

Only after Claude accepts this packet:

1. apply the exact candidate bytes to `AGENTS.md`;
2. require the working file SHA-256 and Git object to equal the authority;
3. run target-local coordination and the installed support aggregate `--no-record`;
4. require BOARD byte identity and clean validation outputs;
5. stage exactly `AGENTS.md`, run cached diff check, and compare the staged object to
   `4cca3734d8c789038b1142a64be2eec2c5edbccc`;
6. commit locally and keep it unpushed for Claude's committed-object review;
7. push only on explicit authorization, then report live/local/fetched identity for closure review.

Recovery is a named revert of the single guidance commit after owner approval, followed by the same
support validation. Unrelated work is preserved; no reset, amend, rebase, force push, tag, release,
or second-path cleanup is authorized.

## Reviewer checklist

Claude should independently verify the parent and candidate objects, exact 6/1 one-path diff,
semantic coverage of the three missing items, preservation of the existing blocked warning, absence
of a synchronization claim, deterministic renderer guards, dry-run attempt accounting, and
proportional validation. Acceptance authorizes the final preflight and local commit only, not push.
