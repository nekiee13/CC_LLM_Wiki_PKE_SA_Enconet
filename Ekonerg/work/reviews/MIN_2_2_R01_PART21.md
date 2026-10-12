# MIN-2.2 R-01 — 10 CFR Part 21

## What and why

This batch sieves the approved 10 CFR Part 21 source (`DOC-0001`). Part 21 is
kept separate from 10 CFR 50 Appendix B and ASME NQA-1. It is used here for
the nonconformance, defect-reporting, corrective-action, procurement, and
records context that may affect the Ekonerg audit.

This is a source-processing result. It is not a finding that Ekonerg complies
or fails to comply.

## Source and scope

- Source: `DOC-0001` (owner-approved G1 source snapshot).
- Authority role: `GOVERNING`.
- Prompt: `appb_rule_v1`.
- Source hash: `74e8cf5d62f05a87879f602cb1abdaee745af875fc6eeab5420df70dc3e84248`.
- Main sections used: §§ 21.1, 21.2, 21.21, 21.31, and 21.51.
- Supplier boundary: Ekonerg remains the only audit target. Any supplier
  material is used only as evidence of Ekonerg's supplier controls.

## Results

The batch produced eight crumbs. They cover:

1. the 60-day evaluation rule;
2. interim reporting;
3. reporting to the responsible director or officer;
4. initial and written notifications;
5. the person responsible for corrective action and reports;
6. Part 21 wording in applicable procurement documents;
7. five-year and ten-year record retention; and
8. posting current regulations and procedures.

The corrected candidate is `RUN-20261003-24` (generation 2):

- 8 crumbs;
- 13/13 evidence quotes linked (100%);
- 0 rejected items;
- 0 failed items;
- all required fields complete;
- candidate remains inactive pending the generation decision.

The first run, `RUN-20261003-23` (generation 1), remains active for audit
trail purposes. Its initial link preview was 11/13. It is not the result to
use because two quotes were shortened and did not match the source exactly.

## Appendix B mapping note

The eight crumbs point to candidate interpretation areas `APP_B_I`,
`APP_B_IV`, `APP_B_VI`, `APP_B_XVI`, and `APP_B_XVII`. This mapping helps the
later audit look in the right places; it does not decide that every Part 21
rule is an Appendix B requirement. Part 21 applicability and any final
criterion applicability decision remain audit decisions supported by Ekonerg
evidence.

## Evidence and validation

- Candidate metrics: `out/2026-10-03/R01-RUN-20261003-24/metrics.json`.
- Candidate metrics (readable): `out/2026-10-03/R01-RUN-20261003-24/metrics.md`.
- Generation diff: `sieving/runs/RUN-20261003-24/` (local run evidence).
- The schema now treats `DOC-0001` and `DOC-0002` as the two approved
  canonical source codes for the regulatory and Appendix B streams.
- No source file was edited.

## Decision needed

Claude review is requested for the corrected candidate. Do not promote
`RUN-20261003-24` to an accepted generation until the generation decision is
recorded. Until then, use this batch as a review candidate only.
