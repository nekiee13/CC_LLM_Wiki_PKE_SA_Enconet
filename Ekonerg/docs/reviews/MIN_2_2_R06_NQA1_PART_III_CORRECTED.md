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
- Intended next generation: `RUN-20261003-41`.

## Safety gate

The local resieve tool refused to create `RUN-20261003-41` because inactive
candidate `RUN-20261003-30` has no recorded generation decision. This is the
correct fail-closed behavior. No database row, active crumb, or prior
generation was changed.

To continue, an owner-approved decision must reject `RUN-20261003-30` with a
recorded decision reference. After that decision, the corrected candidate can
be previewed and applied as generation 3, then reviewed before promotion.
