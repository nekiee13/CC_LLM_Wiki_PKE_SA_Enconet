# Safety review: document rating correction

Codex reviewed the whole `scripts/evaluation_refresh.py` implementation before
live apply. Owner authorization: `DOCUMENT-SCORING-20261007-OWNER`. Claude review
is pending; do not call this a joint code approval.

## Exact target

Only `Ekonerg/db/nqa_audit.sqlite`, the selected evaluation run and a new journal
under `Ekonerg/out/2026-10-07/document-scoring/transition` are written. Paths are
checked for root escape, reparse points, symlinks and hard links. The script uses
only project-local imports, with an explicit project root for synthetic tests.
It never opens a sibling company's database.

The change is one rating and its explanation, not a new source or generation.
Other evaluation rows are written with their existing values. The run metadata,
applicability, crumb rows, quotes, chapter text, active generation flags and all
379 score-support links stay unchanged.

## Preview and guards

Preview is read-only. It binds the database, assessment, prior assessment,
rubric, approval ledger, model and all registered raw sources by SHA256. It
requires all 18 current assessments to match the prior assessment, an approved
G2/G3 model, confirmed applicability and an approved reassessment decision.

Every linked crumb must be an active vendor control of the same criterion.
Every linked quote must occur verbatim in its chapter. Each chapter must match
its registered raw source range and source hash. Changed ratings must cite
existing score-support crumbs and use one of the five existing ratings, with
all four explanation fields. Non-empty downstream gap/finding/action tables
block the change until reconciled.

Apply repeats the preview before writing. It checks all input hashes again
inside an immediate transaction. A modified preview or stale database fails.

## History and recovery

Existing no-local-original-backup authorization remains in place. No original
document is edited, deleted or copied to a backup folder.

Before a rating changes, an exclusive-create journal captures intent and the
complete old evaluation rows, evidence links and run metadata. An append-only
`evaluation_revisions` row stores before and after states in the transaction.
The existing 66.7% report is retained at its old path. A receipt binds the
before/after database hashes, plan, journal and resulting metrics.

An injected failure rolls the transaction back, writes a failed receipt and
blocks blind retry. If a process fails after commit but before its final
receipt, inspect the immutable history and intent journal; do not rerun or
delete them automatically. A completed retry verifies history, current rows,
active generations and journal hashes, then reports `already_applied`.

Tests cover a successful preview/apply/retry, preservation of evidence and
history, refused input/approval/source/quote/basis/model defects, rollback and
two synthetic company names with and without a sibling. The first run was
blocked by sandbox temporary-directory access. The first escalated run exposed
a Windows test-fixture connection left open before a directory rename; that
handle was closed. Neither failed test run modified the live audit database.
