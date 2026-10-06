# Complete manual: source intake and audit continuation

## Owner decision

The owner requested audit processing, then replied **proceed** to this question:

> To activate the new manual evidence, do you approve the 279-item candidate as
> the golden reference and approve replacing its old 18-crumb generation,
> provided all source, chapter-link, and validation checks pass?

The question also said that the 68 leads stay leads, not proof of compliance.
The reply approves both choices. Three ledger entries record source intake,
golden approval, and conditional promotion. There is no new owner gate here.

## Why a source transition is needed

The old manual has 318 lines. The new copy has 3,180 lines. Both state revision 5.
The new copy is a fuller extraction, not a newly issued revision 6. Old evidence
must keep its original source and chapter links. The new copy therefore gets a
new source ID and a hash-tagged raw filename. The owner's incoming file stays put.

The old importer assumes one unchanged source per document. It would make a
first run on a new source active at once. That would count both copies. The new
intake path instead creates an inactive candidate and records its predecessor.

## Safety review before live use — Codex

- **Targets:** only the selected project root, resolved with path, junction,
  symlink, and hard-link checks. Source inputs and planned output hashes are bound
  to the preview. No runtime reads a sibling project.
- **Preview:** reads the source, registry, database, prompt, approvals, and
  candidate without changing them. Saving the preview writes only its new output.
- **Source:** the old raw file, chunks, crumbs, quotes, and runs stay unchanged.
  The full source uses its own ID, full chapter text, exact offsets, and hash.
- **Import:** strict schema checks run first. Every quote must fit verbatim in
  a replacement chapter. The new run is inactive from its first database row.
- **Transaction:** the new document, chapters, candidate, quotes, and links are
  written in one SQLite transaction. The existing source registry is append-only
  on success. The old active generation and all ratings remain unchanged.
- **Recovery:** the owner keeps original backups and waived local original-doc
  backups. This step keeps all old raw and evidence in place. Its intent journal
  stores the exact prior registry text and planned paths. On a caught failure,
  SQL rolls back, the old registry bytes are restored, and only files created by
  this operation are removed. No prior evidence is deleted.
- **Interruption:** if the process dies between file writes and receipt creation,
  retry stops for journal inspection. It does not guess whether SQL committed or
  delete leftovers blindly. A completed retry verifies recorded artifacts and
  database identity before returning `already_applied`.
- **Validation:** an inactive first run is allowed only for an explicit source
  revision whose predecessor still has its completed active generation. This is
  not a blanket waiver of the one-active-generation rule.

Claude review remains pending. Under the owner's temporary-unavailability
instruction, Codex performs and records the safety review and leaves a message.

## Audit continuation

The source intake is not promotion. After intake, score the unchanged candidate
against the approved golden set and retain a source-aware diff. Then pair the
source switch with refreshed criterion summaries, evidence links, and five-point
scores. Preserve the old evaluation as a dated snapshot. Do not present stale
zero-evidence conclusions as the updated audit.

The source-intake code has no command that activates the candidate or changes
ratings. The next action is the controlled source switch plus evaluation refresh,
using the approval already given. The other 23 vendor files still need their new
full semantic pass. The all-31-file keyword pass is complete. The GUI trial stays
paused; the evidence-matrix repair remains in the processing queue.

## Tests before live use

`python -m pytest Ekonerg/scripts/tests/test_source_revision_intake.py Ekonerg/scripts/tests/test_build_reviewed_candidate.py Ekonerg/scripts/tests/test_full_keyword_sweep.py -q -p no:cacheprovider`
exited 0: **40 tests passed**. This includes two synthetic company names, one with
Croatian letters, with and without sibling folders. The tests used approved
access to pytest temporary folders.

TDD red exited 1 before the new intake module existed. The first implementation
run had six failed tests: two test-path separators and four open test-database
handles on Windows. Those test issues were corrected; the full rerun passed.

## Live result

- Source: **DOC-0032**, linked to predecessor DOC-0031. This is an internal
  identity change, not a claim that Ekonerg issued a new document revision.
- Candidate: **RUN-20261006-77**, inactive, with **279 crumbs**.
- Chapter records: **55**. All **279 quotes** have exact links; **298 link rows**
  arise because some quoted text is repeated in more than one chapter. Do not
  count those links as extra crumbs.
- Golden score: **279 found, 0 missed, 0 spurious**, approved and promotion-ready.
  This measures fidelity to the owner's approved fixture, not independent proof
  that every regulatory duty is met.
- Current active vendor total: **214**, unchanged. The approved source switch
  will replace 18 old manual crumbs with 279, yielding **475**.
- No rating, evaluation-evidence link, or old generation changed in this intake.
  No further owner approval is needed for the already-approved replacement.

Artifacts:

- [Exact candidate and metadata](../../sieving/runs/RUN-20261006-77/candidate.json)
- [Metrics](../../sieving/runs/RUN-20261006-77/metrics.md)
- [Source-aware generation diff](../../sieving/runs/RUN-20261006-77/diff-RUN-20261003-39-to-RUN-20261006-77.md)
- [Golden score](../../sieving/runs/RUN-20261006-77/golden-score.json)
- [Preview](../../out/2026-10-06/manual-source-intake-preview.json)
- [Completed intake receipt](../../out/2026-10-06/manual-source-intake/completed.json)

Database before:
`2aba6d844bb609da85eef77aac2b5155d2bc5ccee02a5059af70c50f5e5b231f`

Database after:
`22851271caa3c80658caa9dc24ed80cf3a8bc772a1258e2354403783be8c759b`

The final regression command adds
`Ekonerg/scripts/tests/test_sieve_generation_local.py` and
`Ekonerg/scripts/tests/test_validate_traceability.py` to the command above. It
exited 0: **44 tests passed**. The added cases verify the source-aware diff and
that a future keyword sweep reads the replacement incoming file exactly once.
Unrelated source pairs are still refused by the diff.

The preview, apply, safe repeat apply (`already_applied`), strict candidate JSON,
link preview, metrics generation, golden creation, golden scoring, and generation
diff commands each exited 0. An independent SQL check confirmed all 298 links
are exact and point only to DOC-0032 with its registered hash. Foreign keys are
clean. The old raw hash and old active run are unchanged.

`python Ekonerg/scripts/run_all_validations.py --no-record` exited 0 with eight
phase-applicable passes. Later report/dashboard checks were skipped, not passed.
`python Ekonerg/scripts/validate_evaluation.py --run-id RUN-20261003-32` also
exited 0: the **old** 18-criterion evaluation remains structurally valid. This
does not certify an updated evaluation.

## Specific note for reassessment

The supplied NQA-1 Part I Requirement 12, paragraph 304, itself permits an
exception for commercial devices such as rulers, tapes, and levels when they
provide the required accuracy. The manual's commercial-device exception is
therefore **not automatically a nonconformance**. Assess its scope and limits
against that clause. Requirements 8–16 were reread for the pending reassessment;
do not turn missing lower-level detail into an assertion that no control exists.

Keep the source-switch and evaluation refresh together. A simple call to the
old `sieve_generation.py promote` is not sufficient for this cross-source case:
it expects an active generation on the same source identity. Update the guarded
transition path and tests; do not bypass its decision or golden checks with SQL.
The diff's quote-overlap pairings are review aids, not permission to remap old
evaluation links automatically. No audit score is derived from the crumb count.
