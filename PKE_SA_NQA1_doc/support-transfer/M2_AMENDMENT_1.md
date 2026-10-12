---
record_type: milestone_decision_amendment
gate: M2
amendment: 1
decision: approved
decided_by: human project owner
recorded_at_utc: 2026-07-18T05:08:35Z
recorded_by: claude-code
trigger: CX_2026-07-18T050508Z_slice1-prepush-review-findings (S1-F1..F4)
---

# M2 amendment 1 — T3 reconciliation of the publication sequence (immutable record)

Codex's slice-1 pre-push review found that the M2 slice inventory conflicted with the
controlling, accepted `T3_TARGET_TEMPLATE_CONTRACT.md` publication rule 5 (records,
coordination, and handoff destinations must exist before `support/README.md` renders, so
no committed slice contains dangling links) and returned three further findings on
profile authority, evidence locality, and index completeness. The owner approved the
following amendment in-session on 2026-07-18:

## 1. Resequenced inventory (S1-F1)

- **Slice 1 (amended, 9 creates, no modification):** `support/PROFILE.md` (new, see §2),
  `support/current-status.md`, `support/log.md`, `support/RECORD-KEEPING.md`,
  `support/decisions/README.md`, `support/decisions/adr.template.md`, `support/AFI.md`,
  `support/LESSONS-LEARNED.md`, `support/GOOD-PRACTICES.md`. It no longer contains
  `support/README.md` or the `docs/README.md` link.
- Slices 2 (coordination core) and 3 (handoff core): unchanged.
- **Slice 3c (new, index closure, 1 create + 1 modification):** `support/README.md` and
  the one-line `docs/README.md` link, rendered only after `coordination/BOARD.md` and
  `HANDOFF.md` exist. The index must carry the full accepted FIN rendering list,
  including explicit architecture/AS-IS and release/package-status entries with their
  authority and state labeled (S1-F4). It still precedes every agent-owned addition
  (slice 5) per T3.

## 2. Target-local profile authority (S1-F2)

`support/PROFILE.md` joins the manifest as a controlled record: a clone-complete,
Wiki-independent rendering of the M1-approved CC_FIN support profile v1.0 (identity and
ownership, enabled/disabled modules, native-validation contract, product preservation,
sensitivity and indexing, scale assumptions, recovery rules). `support/RECORD-KEEPING.md`
and the future index cite it as the target-local sensitivity/module authority instead of
a prose label. Provenance (M1 approval) is cited as history, not as a runtime reference.

## 3. Target-local validation evidence (S1-F3)

Every slice's post-slice verification is recorded target-locally: an appended
`support/log.md` validation event carrying the exact command, integer exit code, and
the tuple-comparison result (for slice 1: 54/54, 0 new / 0 gone / 0 mutated), and
`support/current-status.md` links that event as its evidence. A clone must not depend
on any Wiki record to know the slice's validation truth.

## 4. Truthfulness cleanups

Log event types distinguish `support-committed-local` (unreviewed, unpushed) from
`support-published` (reviewed and pushed); the current-status exact-next-action names
its command or file entry point.

## 5. Rebuild procedure for the unpushed commit

Local CC_FIN commit `80f8730` (never pushed) is replaced after this amendment passes
Codex review: reset the local branch to the recovery anchor `238c207`, re-render the
amended slice 1, and commit. Replacing an unpushed, reviewer-rejected local commit is
not history rewriting of published history; this procedure is authorized for this case
only and never after a push.

## Boundary

Authorization scope is otherwise unchanged: slices 1-3, 3c, 5, 6 within the amended
manifest; slice 4 deferred; CC_Loto blocked (M3); no other new path. This amendment is
submitted to Codex for independent review before any FIN change is made.
