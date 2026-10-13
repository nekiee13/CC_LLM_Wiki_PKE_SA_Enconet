# ADR-0021 — AFI, lessons-learned, and good-practice lifecycle

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-15 |
| Decided by | Human (project owner) |
| Scope | Workspace and all project entries |
| Register | Governs `doc/AFI.md`, `doc/LESSONS-LEARNED.md`, and `doc/GOOD-PRACTICES.md` |
| Authored by | Codex (`CX_` prefix) |

## Context

The workspace already maintains three connected knowledge ledgers: areas for
improvement (AFIs), lessons learned, and good practices. Their introductory text states
useful intent, but no ADR defines their authority, identifiers, evidence threshold,
status vocabulary, transition rules, or relationship to audit gates and blockers.

That gap became visible after EPIC12. An independently accepted implementation carried
a worthwhile but non-blocking validator-hardening observation. The owner directed that
it be recorded as an AFI, then confirmed that the AFI lifecycle itself was not governed
by an ADR. Without a common lifecycle, an improvement suggestion can be mistaken for a
release blocker, a resolved AFI can disappear without a durable lesson, or an attractive
idea can be promoted to “good practice” before it has worked in this workspace.

## Decision

1. The canonical workspace ledgers are:
   - `doc/AFI.md` for confirmed, unresolved improvement opportunities;
   - `doc/LESSONS-LEARNED.md` for evidence-backed knowledge derived from failures,
     defects, unexpected outcomes, or closed AFIs; and
   - `doc/GOOD-PRACTICES.md` for patterns proven effective in this workspace.
2. Current controlled documents, approved ADRs, source evidence, audit state, and gate
   decisions outrank all three ledgers. A ledger entry records knowledge; it does not
   silently change a controlled requirement or approval.
3. Every new entry created after this ADR uses a stable identifier:
   - `AFI-<AREA>-NNN` for an area for improvement;
   - `LL-<AREA>-NNN` for a lesson learned; and
   - `GP-<AREA>-NNN` for a good practice.
   Existing historical entries need not be renumbered retroactively. Identifiers are
   never reused, even after closure or supersession.
4. Every new entry records at least: status, date recorded, scope/area, observation or
   proposition, evidence, consequence or value, owner/next action when open, and links
   to related AFI/lesson/practice, ADR, task, validation, or commit records.
5. AFI statuses are `open`, `planned`, `deferred-until <condition/date>`,
   `owner-accepted`, and `resolved`:
   - `open` means confirmed but not yet scheduled;
   - `planned` names an authorized task or gate that will address it;
   - `deferred-until` records an explicit reconsideration condition;
   - `owner-accepted` records the owner's decision to retain the limitation; and
   - `resolved` requires implementation or disposition evidence and verification.
6. AFIs are non-blocking by default. An AFI becomes release-blocking only when a
   controlled requirement, validator, gate, active blocker record, or explicit owner
   decision independently makes it blocking. Severity and urgency must be stated rather
   than inferred from the AFI label.
7. Closing an AFI never deletes its history. The AFI entry is marked `resolved` or
   `owner-accepted`, dated, and linked to evidence. When the outcome yields reusable
   knowledge, a linked lesson-learned entry is created or updated. Git history alone is
   not a substitute for the visible closure link.
8. A lesson learned is added only when evidence demonstrates what happened and supports
   a reusable rule. Its status is `active` or `superseded`; supersession preserves the
   original text and links the newer lesson or ADR. A lesson may originate without an
   AFI when the underlying issue was fixed immediately.
9. A good practice is added only after the pattern has demonstrably prevented, detected,
   or reduced a real problem in this workspace. Its status is `active`, `deprecated`, or
   `superseded`, and its evidence must cite a command result, test, incident, review,
   commit, or ADR. Recommendation or popularity alone is insufficient.
10. Lifecycle transitions are evidence-linked:
    - confirmed observation → AFI;
    - resolved/accepted AFI → closure evidence and, when reusable, lesson learned;
    - lesson learned → good practice only after the resulting pattern is demonstrated;
    - failed good practice → `deprecated` plus a lesson describing the failure; and
    - replacement of a lesson or practice → `superseded` with a forward link.
11. Material additions and transitions use the shared coordination protocol: claim the
    affected ledger files, preserve cross-agent ownership boundaries, request review in
    proportion to risk, and append a concise event to `Enconet/wiki/log.md`. Validation
    results must include commands and exit codes; skipped or unavailable checks are not
    evidence of success.
12. The ledgers are mutable, curated views governed by this immutable ADR. Corrections
    and lifecycle changes are made visibly in place with dates and evidence; this ADR is
    changed only by a superseding ADR.

## Consequences

- AFIs have an explicit, non-blocking default and cannot accidentally become gates.
- Open improvement work remains visible while resolved items retain a durable closure
  trail and can seed evidence-backed lessons.
- Lessons and good practices become auditable knowledge rather than unqualified advice.
- The three ledgers use one transition model while remaining distinct in purpose.
- Existing historical entries remain valid; new entries follow the identifier and
  minimum-field contract, and historical entries may be normalized incrementally.
- `AFI-DASH-001` is the first identifier-governed AFI and remains open, non-blocking,
  with its closure criteria recorded in `doc/AFI.md`.
