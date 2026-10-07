# Enconet document, record and training procedures

Batch: ING-20261007-004. Same approved DOCUMENT v3; no new code or prompt changes.
All 624 content blocks across these three sources were read in direct-control
and quality-intent passes, including forms, tables and non-keyword blocks.

| Source | Run | Crumbs | Exact quote links | Direct / supporting / leads |
|---|---|---:|---:|---|
| DOC-0004, PP-42-01 rev. 6 | RUN-20261007-03 | 148 | 292 | 112 / 31 / 5 |
| DOC-0005, PP-42-02 rev. 5 | RUN-20261007-04 | 72 | 96 | 41 / 25 / 6 |
| DOC-0006, PP-62-01 rev. 4 | RUN-20261007-05 | 74 | 120 | 45 / 25 / 4 |
| New batch total | | 294 | 508 | |

**Live total: 886 vendor crumbs, 1,372 exact quote links, five of 26 documents
fully sieved. Twenty-one vendor documents remain.** No ratings or applicability
decisions were written. Multiple quotes can supply one control's context; their
count is not a score multiplier.

## Actual collected evidence

- [Document-control crumbs](../sieving/runs/RUN-20261007-03/REVIEW.md)
- [Quality-record crumbs](../sieving/runs/RUN-20261007-04/REVIEW.md)
- [Training crumbs](../sieving/runs/RUN-20261007-05/REVIEW.md)

Each run also has generated.json, semantic-review.json and metrics.json/md.
Empty form fields are retained as workflow clues where useful, never as
completed events, actual trained people or proof of signed acceptance.

## Useful controls and review clues

- Document approval, distribution acknowledgments, revision/withdrawal and
  time-limited temporary documents; project identity and retention controls.
- Records classified as permanent, five-year or until-revision, with specific
  contract/regulatory exceptions. Part 21 purchase records have a stated
  ten-year minimum despite the general ZK2 class; retain the specific wording.
- The records procedure still requires GPD, while the document-control GPD
  section says obsolete/canceled. Retain the inconsistency for audit review,
  without automatically deciding nonconformance.
- Training deadlines: notice at least one week before training and make-up
  within a month; retraining on significant revisions and induction before work.
- Qualification records kept permanently, and the unified qualification table
  assigned named custodians with twice-yearly control updates.
- Training provider evaluation and audit qualification requirements.

## Integrity and validation

Strict JSON, canonical run creation, strict import, exact-link preview/apply,
metrics and direct traceability validation returned exit 0 for each run.
Previous two runs' crumb, quote, link and context data hashes are unchanged.
All 36 incoming files still match their reset-time hashes.

Independent SQL checked all 1,372 links: EXACT method, same document ownership
and literal quote containment. The aggregate command
`python Enconet/scripts/run_all_validations.py --no-record` returned exit 0:
four applicable checks passed at chunked, later-phase checks skipped. Therefore
strict JSON and traceability were also run directly, not claimed as aggregate
passes. Commands are the same tested pipeline used for the earlier full runs.

The ingestion ledger records each document separately. No old generation was
rewritten, no source changed and no new framework feature was introduced.

## Next

Continue contract/marketing DOC-0007, design DOC-0008 and audit DOC-0009 as the
next bounded vendor batch. Fresh runs will keep the same approved prompt and
prior evidence intact. Regulatory requirement extraction and G2-G7 remain open.
