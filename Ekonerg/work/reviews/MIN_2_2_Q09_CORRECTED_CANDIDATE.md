# MIN-2.2 Q09 — corrected candidate for DOC-0016

## Purpose

Claude found one evidence-quote spelling error in the first concept-recall
generation for `DOC-0016` (`PQ07.5-7_r10_Kontrola_zapisa.md`). The source says
`Zapise s provjere generira tim za provjeru`; the earlier candidate used
`provjera`. The source document was not changed.

## Candidate

- Previous active generation: `RUN-20261003-33`.
- Corrected candidate: `RUN-20261003-40` (generation 2, now active).
- Prompt: `appb_document_v2_concept_recall` (unchanged).
- Candidate input: `sieving/runs/q09_doc0016_v2_corrected.json`.
- Candidate input SHA-256: `6A781A7C9021E6B3783A79F8286EBFEB2458EF18A4B6B59FB28D4886860DBD5B`.

## Results

- 12 crumbs imported.
- 12/12 evidence quotes linked (100%).
- 0 unmatched quotes, rejected items, or failed items.
- The only diff is replacement of the typo-bearing crumb with the exact-source quote.
- The candidate is inactive and must not be promoted without a recorded generation decision.

Evidence files:

- `sieving/runs/RUN-20261003-40/metrics.json`
- `sieving/runs/RUN-20261003-40/metrics.md`
- `sieving/runs/RUN-20261003-40/diff-RUN-20261003-33-to-RUN-20261003-40.json`
- `sieving/runs/RUN-20261003-40/diff-RUN-20261003-33-to-RUN-20261003-40.md`

This is a source-processing correction only. It does not create an audit
conclusion or change criterion applicability.

## Promotion record

- Golden fixture approval: `GOLDEN-DOC0016-V2-20261004-OWNER`.
- Generation promotion approval: `DOC0016-GEN2-PROMOTE-20261004-OWNER`.
- The database now records `RUN-20261003-40` as the active generation for
  `DOC-0016`; the prior generation `RUN-20261003-33` is superseded.
