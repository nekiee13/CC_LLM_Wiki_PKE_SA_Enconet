---
record_type: slice_prejob_briefing
slice: 1
target: CC_FIN
recorded_at_utc: 2026-07-18T04:56:00Z
authorized_by: M2_APPROVAL.md (owner, 2026-07-17T23:52:40Z)
implementer: claude-code
reviewer: codex
roles_assigned_by: human owner, in-session, 2026-07-18
---

# Slice-1 pre-job briefing — CC_FIN neutral support skeleton

## Roles (this slice, owner-assigned per M2 amendment 3)

- Implementer: claude-code. Reviewer: codex. Independent review by the reviewer is
  required before push and before any acceptance statement.

## Scope (exactly the M2_DRY_RUN_MANIFEST.md slice-1 inventory)

9 creates: `support/README.md`, `support/current-status.md`, `support/log.md`,
`support/RECORD-KEEPING.md`, `support/decisions/README.md`,
`support/decisions/adr.template.md`, `support/AFI.md`, `support/LESSONS-LEARNED.md`,
`support/GOOD-PRACTICES.md` — rendered from the accepted T3 templates with FIN values;
rendering fails on any unresolved placeholder.

1 modification: `docs/README.md` gains exactly one line:
`- [Support system](../support/README.md) — repo-local governance, coordination, and handoff core`

Nothing else. One commit, one concern, committed locally; **no push before review**.

## Preflight checklist (executed and recorded before writing)

1. HEAD equals recovery anchor `238c207c73970f3d3c6dc00c2db5932ebeca7be4`; porcelain
   empty; synchronized `0 0` with `origin/main`.
2. All 9 creation paths absent; `docs/README.md` present.
3. Rendered content passes the sensitive-content scan (staged `_shared.scan_sensitive`)
   and contains no unresolved `{{...}}` placeholder.
4. No Wiki path, Wiki project name in a runtime role, or cross-repository reference in
   any rendered file.

## Acceptance rule (M2 item 6)

After the local commit, a like-for-like native re-run
(`PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider
--continue-on-collection-errors`, JUnit outside the repo) must show the identical
failing/erroring tuple set as `M2_BASELINE_FAILURE_SET.md` — no new tuple, no mutated
surviving tuple, no unexplained disappearance.

## Amendment 1 (owner-approved 2026-07-18, after Codex findings S1-F1..F4)

The scope above is superseded by `M2_AMENDMENT_1.md`: slice 1 is now the 9 amended
creates (adding `support/PROFILE.md`, dropping `support/README.md` and the
`docs/README.md` link, which move to slice 3c per T3 publication rule 5). Post-slice
validation evidence is recorded target-locally in `support/log.md` and linked from
`support/current-status.md`; log event types distinguish `support-committed-local`
from `support-published`; the exact next action names its entry point. Roles,
preflight, acceptance rule, and stop conditions are unchanged. The unpushed commit
`80f8730` is replaced per the amendment's rebuild procedure only after Codex review of
the amendment.

## Stop conditions

Baseline drift at preflight; any collision; sensitive-pattern hit; unresolved
placeholder; any new/mutated/vanished tuple after commit; any file outside the
inventory appearing in `git status`. On stop: no push, scoped revert of the local
commit only, report to owner and reviewer.
