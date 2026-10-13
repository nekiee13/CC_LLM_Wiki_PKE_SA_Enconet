# ADR-0023 — Temporary Codex continuation with deferred Claude review

| Field | Value |
|---|---|
| Status | Accepted — temporary operating-mode exception |
| Date | 2026-09-03 |
| Decided by | Human (project owner) |
| Scope | `EVIDENCE-ACCESS-TDD` implementation and its coordination lifecycle |
| Register | Owner directive in the active 2026-09-03 session |
| Authored by | Codex (`CX_` prefix) |

## Context

The Owner approved the reviewed `docs/EVIDENCE_ACCESS_TDD_PLAN.md` as the work queue and
directed Codex to continue its planned corrections one task at a time. Claude Code, the
designated independent reviewer, is temporarily unavailable. Waiting for an immediate Claude
review after every task would stop otherwise authorized, bounded work, but removing review
evidence or silently treating review as complete would weaken the dual-agent contract.

The plan already separates implementation tasks from human-controlled architecture, artifact
promotion, and acceptance gates. The neutral coordination channel can preserve immutable review
requests until Claude becomes available.

## Decision

1. Codex is temporarily authorized to implement `EVIDENCE-ACCESS-TDD` tasks sequentially, one
   task at a time, while Claude Code is unavailable.
2. This is deferred review, not waived review. After each completed task Codex must create an
   immutable `CX_` coordination message containing at minimum:
   - task/issue ID and exact scope;
   - changed files;
   - RED test and demonstrated pre-fix failure;
   - GREEN/focused test results with integer exit codes;
   - regression and aggregate validation results;
   - known risks, deviations, and remaining gates; and
   - the exact review requested from Claude.
3. Deferred review messages remain unresolved in `coordination/messages/`. Codex must not archive
   them as resolved, claim Claude approval, or claim both sides synchronized before Claude reviews
   and confirms them.
4. When Claude returns, Claude reviews the queued completed tasks in implementation order. Codex
   addresses material findings with a new RED test and correction before the affected milestone or
   controlled artifact is accepted or promoted.
5. Owner authorizations already granted remain in force. This decision does not itself expand any
   task beyond the reviewed plan or pre-authorize a later human gate.
6. The one-task-at-a-time rule is mandatory. Codex completes, validates, records, and releases one
   task claim before claiming the next plan task. Work may not be bundled merely because review is
   deferred.
7. Existing ownership boundaries remain unchanged. Codex must not create, edit, move, delete, or
   archive Claude-owned infrastructure or `CC_` records.
8. The following controls are not relaxed:
   - frozen master/alignment plans;
   - raw-source immutability and provenance;
   - fail-closed filtering, generation, validation, and publication;
   - audit phase and human-gate requirements;
   - ADR-0007's prohibition on restoring a standalone GUI without a superseding owner decision;
   - controlled-output candidate and promotion rules; and
   - required use of `C:\xPY\vEnv\WikiEnconet` once EA0.6 makes it project-ready.
9. This temporary exception ends when the Owner declares it ended or Claude availability is
   restored and acknowledged through the neutral coordination channel. A later owner directive
   supersedes this operating-mode decision; this ADR remains immutable history.

## Consequences

- Codex can make bounded progress without representing absent review as approval.
- The inbox will intentionally contain unresolved Codex review requests until Claude returns.
- Automated tests and validations remain necessary but do not substitute for the deferred
  independent review.
- No controlled output may pass a required human gate solely because this temporary mode exists.
- Work remains easy to audit because each task has its own claim, test evidence, message, and
  commit boundary.
