# T5 handoff and session-continuity contract v1.0

## Scope

This planning-only contract defines clone-complete target handoffs and continuity behavior. It does
not publish tooling to either target. The repository-local schema, template, publisher, pointer,
tests, and guidance integration are published later under the target gates; no user-global skill or
Wiki path is required at runtime.

## Target-local structure

```text
HANDOFF.md                         # replaceable pointer
support/handoffs/                  # immutable validated records
support/schemas/handoff.schema.json
support/templates/handoff-record.template.md
support/templates/handoff-pointer.template.md
support/templates/continuity-checklist.template.md
scripts/ or tools/ make_handoff.py # target convention from D-13
```

The templates allow exactly `{{PROJECT_NAME}}`, `{{HANDOFF_RECORD_ID}}`,
`{{HANDOFF_RECORD_RELATIVE_PATH}}`, `{{HANDOFF_PUBLISHED_AT_UTC}}`,
`{{HANDOFF_SOURCE_AGENT}}`, `{{HANDOFF_STATUS}}`, and `{{HANDOFF_GIT_HEAD}}`. Rendering fails on an
unknown or unresolved placeholder. The record template uses structured values supplied to the
schema validator rather than free-form substitution.

## Handoff profile

Every immutable handoff records:

- target identity, record ID, UTC creation time, source agent, status, objective, and scope;
- work completed and remaining, decisions, artifacts, blockers, and follow-up queue;
- exact Git root/branch/HEAD/upstream/worktree and index state (`current`, `stale`, `absent`,
  `unknown`, or `not-configured`);
- validation checks with literal state, command when run, integer exit code when available, and
  evidence/notes;
- exact next action with owner, prerequisites, operation/entry point, and stop condition;
- active claims/messages and interrupted-risk disposition.

Handoff status is `complete`, `partial`, or `blocked`. It describes continuity completeness, not
product completion or gate approval.

The publisher parses frontmatter and required Markdown headings into the normalized object validated
by `handoff.schema.json`; the schema is not limited to frontmatter alone. Rendered Markdown and the
normalized object must agree on ID, time, source agent, status, checks, and next action.

## Truthful check vocabulary

| State | Meaning | Command/exit-code rule |
|---|---|---|
| `passed` | Applicable command ran and succeeded | non-empty command and integer exit code `0` required |
| `failed` | Applicable command ran and failed | non-empty command and non-zero integer exit code required |
| `skipped` | Applicable but deliberately not run | reason required; no passed implication |
| `not-run` | No execution occurred | reason/next action required |
| `unknown` | State could not be established | limitation required |
| `not-configured` | Capability does not exist for target | evidence/rationale required |
| `unavailable` | Capability exists but environment/service/dependency unavailable | limitation required |

`blocked` is a handoff/blocker state, not a substitute check result. Optional checks retain the same
truthful vocabulary.

## Sensitive-data boundary

Before publication, content scanning fails on credentials, secret values, personal data, private
absolute paths, and target-prohibited product data. Records may cite approved repository-relative
paths, identifiers, hashes/checksums, or environment-variable names without private values. FIN and
Loto exclusions come from their M1 profiles.

## Deterministic publication protocol

1. Resolve the repository root; collect Git/index/coordination state without mutation.
2. Render a uniquely named record in the target handoff directory.
3. Validate schema, headings, IDs, check semantics, paths, sensitive content, and exact next action.
4. Write and fsync a temporary record in the destination filesystem.
5. Atomically replace the final immutable record path; fail if that ID already exists.
6. Render and validate a temporary `HANDOFF.md` pointer to the final record.
7. Atomically replace the pointer only after the immutable record is durable.
8. Append/log the publication through the target's validated event mechanism.
9. Re-open and validate record/pointer identity and report paths plus integer result code.

Failure before step 5 leaves no final record or pointer change. Failure after step 5 but before
pointer replacement leaves a valid orphan record and the previous pointer intact; retry may adopt
that exact validated record but cannot overwrite it. Failure after pointer replacement is reported
as partial and cannot be called success until post-publication validation/logging completes.

## Staleness and absent Git

A staleness check compares recorded root, branch, HEAD, upstream relation, and worktree observation
with current state. Divergence is reported field-by-field and never silently normalized. A
non-Git/disconnected environment is supported only with explicit `git_state: absent` or `unknown`,
status `partial`/`blocked` as appropriate, and an exact next action; it cannot fabricate a SHA.

## Session-start continuity

Read and compare, in order:

1. agent-owned guidance and shared authority/navigation;
2. `HANDOFF.md` and its immutable record;
3. current support status and product-plan reference;
4. active messages, claims, and generated board freshness;
5. Git/upstream/worktree and index state;
6. unfinished artifacts, temporary files, backups, migrations, or risky operations.

Any divergence becomes a visible status/blocker with evidence. The session does not repair, reset,
delete, migrate, or resume risky work merely to match the handoff.

## Session close

Closeout runs required target-native/support checks, records literal outcomes, validates the complete
handoff, and publishes using the deterministic protocol. A failed required check may produce
`partial` or `blocked`, never `complete` with an implied pass. Publication does not approve a gate.

Interrupted risky work requires a durable `resume` or `rollback` decision naming owner, scope,
recovery point, backups, validation, and stop conditions. If neither is authorized, the handoff is
blocked and the next action is escalation—not automatic continuation.

## Test contract

Positive tests cover complete, partial, and blocked records. Negative/fault-injection tests cover:

- passed/failed state without valid command/exit code and malformed evidence;
- stale Git/index state, absent Git, dirty worktree, and upstream divergence;
- duplicate IDs, malformed record/pointer identity, missing headings, and path traversal;
- sensitive/prohibited content;
- interruption before record publish, between record/pointer, and after pointer/before log;
- retry/adoption of an orphan immutable record without overwrite;
- session-start divergence and risky-work resume-or-rollback enforcement.

Tests run in disposable roots and assert the previous pointer and unrelated files are preserved.

## Planning acceptance

- Required facts, statuses, truthful result vocabulary, and sensitive exclusions are explicit.
- Record-before-pointer atomicity and every interruption outcome are defined.
- Session start reports divergence; close validates before publication.
- Risky interrupted work cannot silently resume.
- No target repository was modified.
