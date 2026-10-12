# MIN-2.2 DOC-0016 v2 golden calibration

## Purpose

This is a draft answer key for the corrected concept-recall generation of
`DOC-0016` (`PQ07.5-7_r10_Kontrola_zapisa.md`). It gives the reviewer a fixed
set of expected crumbs for this document and prompt version.

It is not an audit conclusion. It is not yet an approval to promote the
generation.

## Draft calibration

- Manifest: `benchmarks/sieving_golden/manifest_document_doc0016_v2.yml`.
- Prompt: `appb_document_v2_concept_recall`.
- Candidate: `RUN-20261003-40`.
- Expected crumbs: 12.
- Criteria represented: APP_B_I, APP_B_III, APP_B_VI, APP_B_X,
  APP_B_XVII, and APP_B_XVIII.
- Status: `pending_human_approval`.
- Approval reference: none.

Every expected quote was checked as an exact substring of the registered raw
document. The corrected Q09-007 quote uses `provjere`, matching source line
87. The two weak schedule-table items remain `candidate_lead` items; the
calibration does not turn them into confirmed audit evidence.

## Diagnostic score

The local scorer compared the draft with `RUN-20261003-40`:

- found: 12
- missed: 0
- spurious: 0
- quote links in the candidate: 12/12 (100%)
- promotion-ready: false, because the draft has no human approval reference

The diagnostic score was run with `--allow-draft` and is not a promotion
approval. A human approval record is still required before
`sieve_generation.py promote` can run.
