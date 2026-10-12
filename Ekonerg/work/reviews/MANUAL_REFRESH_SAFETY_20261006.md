# Approved manual switch and audit refresh

## What and why

The complete manual replaces the incomplete copy as current evidence. Both
copies remain in history. The owner approved the source, golden fixture and
generation switch. No new owner decision is needed.

The old score was 52.8%. The reviewed assessment is 66.7%: twelve substantial
and six partial ratings. This change comes from control content, not counts.
VIII, IX, XI, XIII and XIV no longer lack evidence. IV gains clearer purchase
controls. VI and XVII lose full-match status due to inconsistent procedure
references in the complete source. The other ratings retain their level but
receive more precise reasons. All 18 are official documentation-audit results
under the owner's instruction, not claims of field-verified performance.

The 279 manual crumbs include 68 leads. Those leads stay in the evidence pool
but are excluded from the score-support links. The remaining 211 describe
policy or supporting controls; they are not 211 completed work records.
Prior reviewed links from other sources are retained unless tagged as leads.

## Safety review before apply — Codex

- The root and every input/output path are resolved inside the selected project.
  Junctions, symlinks and hard links are refused. Runtime uses no sibling project.
- Preview reads only. Its separate saved file binds the database, assessment,
  raw sources, golden fixture, prompt, approval ledger and scoring model by hash.
- All raw files must match their registered hashes. Replacement chapter text
  must match source offsets. Every candidate quote must match its chapter.
- The database candidate must match the approved golden set. Source intake,
  golden and promotion decisions must be recorded. All 18 scope rulings and
  the G2/G3 model approvals must be valid.
- Apply reruns the preview, takes a database write lock and rechecks hashes.
  One transaction switches active sources and replaces all 18 assessments and
  their links. No source text, crumb, quote or chapter is edited.
- Before replacing evaluations, the tool stores their exact prior rows and
  links in an immutable database history table and in `before.json`. The plan
  records the complete new rows and links. Foreign keys and active links are
  checked before commit. No gaps, findings or actions exist in this database;
  the tool refuses them instead of silently leaving stale downstream records.
- A database trigger prevents activating a retired source. The harness permits
  its zero-active state only through a verified replacement chain. Old inactive
  candidates remain inactive and are not silently rejected or deleted.
- A caught failure rolls back SQL. An incomplete journal stops retry for review.
  If a crash occurs after commit but before the receipt, inspect the stored
  activation and evaluation history; do not rerun or restore blindly.
- The receipt records before/after database hashes and journal hashes. A repeat
  call verifies the stored history and returns `already_applied`, without writes.
- The owner keeps original-document backups and waived duplicate local backups.
  All old sources/evidence and prior evaluation snapshots remain recoverable.
  A reverse migration would require a reviewed plan, not direct history edits.

Claude review is pending under the owner's unavailable-reviewer instruction.

## Dashboard defect and bounded fix

The source HTML calls `renderCards(); renderMatrix(); renderRadar();` on one
line. The old generator removed every line containing `radar`, so it also
removed startup for the cards and matrix. A failing regression test reproduced
this. Remove only the radar call before removing radar-only lines.

The refreshed page uses real affirmative/contrary assessment text, prioritizes
gaps by rating rather than crumb count, and removes the fixed old list of five
unmet criteria. It keeps the light layout, filters, sorting, print and chapter
links. The separate dark-mode design trial is not part of this change.

## Coverage limit

All 31 source files have had the keyword sweep. The new full semantic review
is complete for the manual only. The other 23 vendor files retain their prior
reviewed generations; their new full semantic pass is the next audit work.
