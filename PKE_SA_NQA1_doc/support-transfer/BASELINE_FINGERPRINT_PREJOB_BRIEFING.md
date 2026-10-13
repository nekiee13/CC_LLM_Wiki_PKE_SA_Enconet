---
record_type: support_transfer_prejob_briefing
task: SUPPORT-TRANSFER-BASELINE-FINGERPRINT
version: 1
recorded_at_utc: 2026-07-18T19:29:37Z
authorized_by: M2_APPROVAL.md item 1 and owner confirmation 2026-07-18
implementer: codex
reviewer: claude-code
target_parent: 1d61534b81771ae2cd0b8ca5ffa1dd9911712439
status: pre-write-review-required
---

# Baseline-fingerprint migration pre-job briefing — CC_FIN

## Authority, roles, and exact boundary

The owner selected the final M2 baseline-fingerprint migration, assigned Codex as
implementer, and assigned Claude Code as independent reviewer. No CC_FIN write begins
until Claude accepts this briefing and its exact rendered proposal.

Content commit A contains one target-local normative record plus the minimum navigation
and classification integrations needed to make that record governed and discoverable:

1. create `support/BASELINE-FINGERPRINT.md` with all 54 normative tuples and the complete
   comparison and normalization contracts;
2. modify `support/README.md` by adding exactly one Current records link to that record;
3. modify `support/RECORD-KEEPING.md` by classifying that path as immutable and requiring
   a reviewed successor for future change.

No product code, tests, dependencies, data, workflow, agent-owned infrastructure, generated
BOARD, `.gitignore`, CC_Loto path, or other target file enters A. Evidence commit B changes
only `support/log.md` and `support/current-status.md`. The reviewed clean target parent is
published Slice-6 evidence commit `1d61534b81771ae2cd0b8ca5ffa1dd9911712439`.
Rollback, if separately approved after failure, is a reviewed revert of the named A/B commits,
never reset, cleanup, deletion of unrelated work, force push, or history rewriting.

## Exact rendered proposal

`rendered/baseline-fingerprint/` is the byte authority. The preparation renderer reads
`support/README.md` and `support/RECORD-KEEPING.md` directly from the reviewed parent, inserts
one unique line into each, and renders the standalone record from the approved 54-tuple source.
The target record contains no Wiki or machine-path dependency. The renderer requires exactly
54 unique node IDs and the approved class split: 24 torch, 11 matplotlib, 19 assertion.

The immutable record preserves the no-new-tuple, exact-survivor, explained-disappearance, and
support-check rules. It explicitly states that the baseline is evidence—not permission to
weaken tests, install dependencies, change product behavior, or report expected native red as
passed. Any future baseline change requires a reviewed successor that preserves this record.

## BOARD and product non-impact

The three A paths are not coordination-board inputs. A disposable archive of the reviewed
parent, overlaid with the three candidate blobs, passed the installed target coordination
validator with 0 errors and 0 warnings; `coordination/BOARD.md` remained byte-identical.
The record and its navigation/classification lines do not change product execution, tests,
dependencies, workflows, hosted governance, or release state.

## Reproduction and immediate preflight

From the Wiki root run:

`$env:PYTHONDONTWRITEBYTECODE='1'; python doc/support-transfer/rendered/render_baseline_fingerprint.py`

Expected exit 0: exact three-file inventory, 54 unique tuples with the 24/11/19 split,
sensitivity and forbidden-reference scans clean, target validation 0/0, and BOARD unchanged.
Two consecutive renders must reproduce all three SHA-256 values recorded in
`BASELINE_FINGERPRINT_RENDER_EVIDENCE.md`.

Immediately before any target write, require live remote, `origin/main`, and local HEAD all
equal the reviewed parent; divergence `0 0`; empty porcelain; candidate create-path absent;
both modified parent blobs unchanged; and a fresh two-run deterministic render. Stop on drift,
collision, missing tuple, signature or count change, broken link, class mismatch, sensitive
content, forbidden origin dependency, runtime artifact, BOARD change, or scope expansion.

## Two-commit target protocol

1. **Content commit A:** copy exactly the three reviewed blobs; stage only those paths; require
   3/3 staged-object byte identity and a cached diff showing one create and exactly one inserted
   line in each modified file; commit locally.
2. At clean A run `$env:PYTHONDONTWRITEBYTECODE='1'; python scripts/agent_coord.py .`;
   require exit 0, 0 errors/0 warnings, and BOARD byte-identical to the parent.
3. At clean A run
   `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --continue-on-collection-errors -q --tb=no --junitxml="$env:TEMP\fin_baseline_fingerprint_A.xml"`.
   Expected exit 1 only for the normative set: exactly 54 actual tuples, 0 new, 0 gone,
   0 mutated, and the recorded 24/11/19 class split. Parse and compare against the new
   target-local record, not the Wiki source.
4. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md`.
   Record A's full SHA and committer UTC, literal commands and integer exits, validator 0/0,
   native tuple result, BOARD identity, target-local comparison source, and reviewer-gate state.
5. At clean B rerun the target and native commands with
   `fin_baseline_fingerprint_B.xml`; require target 0/0, the same 54 tuples, A-to-B identity,
   and comparison exclusively against `support/BASELINE-FINGERPRINT.md`.
6. Confirm A is exactly the reviewed three blobs, `B^ == A`, and `A..B` changes exactly the
   two evidence files. Submit A/B to Claude for independent pre-push review. Push only after
   reviewer acceptance and only as a fast-forward of the accepted commits.

Any byte, tuple, scope, authority, ownership, validation, BOARD, remote, or reviewer defect is
a stop. Failed, skipped, unavailable, pending, and expected-red states remain literal.
