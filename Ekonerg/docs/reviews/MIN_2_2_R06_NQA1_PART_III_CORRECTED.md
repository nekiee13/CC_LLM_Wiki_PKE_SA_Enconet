# MIN-2.2 R-06 — Part III corrected candidate

## Correction

Claude found that `RUN-20261003-30` shortened one source quote. The raw
source contains the marker `— Part III —` and the corrected candidate restores
it exactly:

`Application of this Part's — Part III — guidance may be achieved by either or both of the following approaches when implementing Parts I and II requirements:`

The raw source is unchanged.

## Prepared candidate

- Source: `DOC-0006`, `ASME_NQA-1_129-206_Part_3.md`.
- Prompt: `appb_rule_v1`.
- Candidate input: `sieving/runs/r06_doc0006_corrected.json`.
- Candidate quotes: 7/7 exact source matches.
- Applied candidate: `RUN-20261003-41` (generation 3, inactive).
- Metrics: 6 crumbs, 7/7 quote links (100%), 0 rejected, 0 failed.
- Diff: only the corrected quote and its regenerated crumb identity changed;
  crumb count stayed at 6.

## Safety gate

The owner approved rejection of `RUN-20261003-30` with decision reference
`R06-GEN2-REJECT-20261003-OWNER`. The rejected generation remains in the
database for traceability. The corrected generation is now an inactive review
candidate; it is not promoted and does not replace the active generation until
the required review decision is recorded.
