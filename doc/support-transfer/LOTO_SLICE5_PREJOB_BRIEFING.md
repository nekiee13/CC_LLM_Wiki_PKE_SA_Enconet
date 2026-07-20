---
record_type: slice_prejob_briefing
slice: 5
target: CC_Loto
version: 1
recorded_at_utc: 2026-07-19T23:59:29Z
authorized_by: M3_APPROVAL.md items 5-8 and owner instruction to proceed after closed Slice 3c
implementer: codex
reviewer: claude-code
target_parent: 85f97d0a75a996e83691d2b103d9724cb3136653
status: pre-write-review-required
---

# CC_Loto Slice 5 pre-job briefing v1 — Codex-owned guidance

This packet opens independent pre-write review only. It authorizes no CC_Loto write, commit, push,
Claude-side edit, dependency/product change, or M4 transition. Codex is the owner/author and
implementer of this guidance; Claude Code is independent reviewer.

## Exact content scope — one Codex-owned create

Content commit A would copy the sole byte authority in
[`rendered/loto-slice5/`](rendered/loto-slice5/) exactly:

1. create root `AGENTS.md`.

The target currently has no `AGENTS.md`, `.agents/`, or `docs/governance-transition.md`. The accepted
Loto profile disables repo-local workflow skills initially, so this slice does not fabricate an
`.agents/` tree. Unlike FIN, Loto has no existing governance-transition file to correct; the
evidence-first recovery safeguards are therefore included in Codex-owned `AGENTS.md` rather than
creating a new shared-neutral document.

No `CLAUDE.md`, `.claude/`, `CC_` record, shared-neutral tool/record, generated board, product file,
workflow, dependency, data/model/output, tag, release, or external index is in A.

Exact review inputs:

- [`LOTO_SLICE5_RENDER_EVIDENCE.md`](LOTO_SLICE5_RENDER_EVIDENCE.md)
- [`LOTO_SLICE5_DRY_RUN_EVIDENCE.md`](LOTO_SLICE5_DRY_RUN_EVIDENCE.md)
- [`rendered/render_loto_slice5.py`](rendered/render_loto_slice5.py)
- [`rendered/loto-slice5/AGENTS.md`](rendered/loto-slice5/AGENTS.md)

## Guidance content and semantic anchors

The candidate is target-native and covers:

- authority distinctions among the owner-designated enhanced plan, product docs, earlier progress,
  current Git evidence, and support records;
- Codex/Claude/shared-neutral ownership and immutable CX/CC archive boundaries;
- ordered session startup through support index/profile, handoff, status/log, board, messages,
  claims, Git, and unfinished risk;
- correct setuptools `dynamix-lottery` 0.1.0 / Python `>=3.11` / mixed package-discovery facts;
- `tools/support/` placement, layered `run_tests.py`/`unittest` semantics, optional fail-soft states,
  and the separate support-operator dependency boundary;
- product/data/output/index/hosted/release exclusions from the accepted Loto profile;
- small direct-main commits, immutable cross-agent review, evidence-first recovery, reviewed reverts,
  and explicit approval for destructive action;
- literal validation states and the non-inference of M4.

The renderer rejects pytest/FIN/Wiki/private-path assumptions, routine hard-reset wording, stale
no-packaging wording, unresolved placeholders, sensitive patterns, and missing semantic anchors.

## Claude-side synchronization pending

Read-only inspection found `CLAUDE.md` line 9 still says the project runs with `sys.path`
bootstrapping and has “no packaging or requirements,” although its later sections and the current
target authority correctly describe editable packaging. Codex will not edit this Claude-owned file.
Claude may correct its side in a separately owned/gated action; until then, paired guidance is not
claimed synchronized. This observation does not expand Slice 5 content A.

## Verified preflight state

- CC_Loto HEAD and `origin/main` equal closed Slice 3c tip
  `85f97d0a75a996e83691d2b103d9724cb3136653`; divergence `0 0`; porcelain empty.
- `AGENTS.md`, `.agents/`, and `docs/governance-transition.md` are absent.
- Two fixed-timestamp renders reproduced the candidate hash with zero differences.
- The short-root disposable overlay returned coordination validation 0 errors/0 warnings and kept
  the board byte-identical.
- Renderer assertions pinned current packaging, native runner, profile states, support paths,
  ownership, safety, validation-truth, and gate semantics.
- Required native layers passed 42/42, 25/25, and 3/3 in the disposable overlay.
- Workspace guidance-drift validation exited `0`: 0 errors, 3 pairs, 39 anchor rules, 8 documented
  differences. This does not claim the new target-side pair synchronized.

## Preflight immediately before content commit A

1. Reverify `HEAD == origin/main == 85f97d0...`, divergence `0 0`, and empty porcelain.
2. Reverify root `AGENTS.md` remains absent and no new `.agents/` or governance-transition path has
   appeared.
3. Require Claude's explicit acceptance of this packet, the one-create scope, semantic content,
   and Claude-sync-pending disclosure.
4. Require the pushed Wiki packet commit containing the exact candidate; rerun the fixed renderer
   and require its recorded SHA-256/Git object plus all disposable checks.

Any mismatch is a stop condition.

## Proposed two-commit evidence protocol after acceptance

1. **Content commit A:** create only `AGENTS.md`; stage exactly one path; require the staged Git
   object to equal the reviewed source; commit locally.
2. **Validation at clean A:** run installed coordination validation and require exit `0`, 0 errors,
   0 warnings, and byte-identical board. Re-run semantic/forbidden-token checks and required native
   short layers for 70/70.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md` to record A's
   full identity, exact commands/exits, semantic and ownership checks, native evidence, Claude-side
   synchronization pending, later validators/tests and closure gates, and M4 state.
4. **Validation at clean B:** repeat coordination/semantic/native checks; prove `B^ == A`, A has
   exactly one path, B has exactly two evidence paths, and all objects match reviewed authorities.
5. Keep A/B local until Claude independently reviews committed objects and explicitly authorizes
   their exact fast-forward push.

Rollback, only on reviewer/owner direction, is a new revert of B followed by A. Reset, force push,
broad cleanup, or unrelated restoration is prohibited.

## Stop conditions

Stop on target drift; `AGENTS.md` collision; any path beyond A's one create or B's two evidence
modifications; byte mismatch; Claude/shared-neutral ownership violation; stale/false packaging or
runner fact; pytest/FIN/Wiki/private-path leakage; missing read-order/ownership/truth/recovery/gate
anchor; unsafe recovery authorization; coordination error; board change; native regression;
sensitive product data; target artifact; or reviewer finding. M4 remains closed.
