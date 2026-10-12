# MIN-2.2 R-02 — 10 CFR 50 Appendix B

## What and why

This batch sieves the owner-approved Appendix B source (`DOC-0002`). Appendix
B is the governing audit baseline. It is kept separate from Part 21 and from
ASME NQA-1 interpretation material.

This is a rule-extraction result. It is not an assessment of Ekonerg.

## Source and scope

- Source: `DOC-0002` (`10CFR_Part 50_-_Appendix_B.md`).
- Authority role: `GOVERNING`.
- Prompt: `appb_rule_v1`.
- Main source sections: Introduction and Criteria I through XVIII.

## Results

Candidate `RUN-20261003-25` (generation 2) produced one crumb for every
Appendix B criterion:

- 18 crumbs;
- 17/18 quote links verified (94.4%);
- 0 rejected items;
- 0 failed items;
- all required fields complete;
- no criterion has zero crumbs.

The earlier controlled generation `RUN-20261003-01` remains active and is
retained for traceability. It had six broad crumbs. The new generation adds
focused coverage for all 18 criteria, including the mandatory Part 1-style
areas such as design control, procurement, inspection, records, corrective
action, and audits.

## Link exception

The only unmatched quote is in Criterion XVI (Corrective Action). The supplied
source text contains the word `alfunctions` where the normal word would be
`malfunctions`. The extracted quote used the normal spelling, so the linker
correctly refused to claim a source match. This is a source-fidelity issue, not
a reason to edit the incoming source. The candidate remains inactive until a
reviewer decides whether to quote the supplied spelling or record another
source-fidelity treatment.

## Applicability and interpretation

All 18 criteria are extracted as governing requirements. This does not mean
all 18 are applicable to every Ekonerg activity. Applicability must be decided
later from Ekonerg's design, engineering-service, and consultancy scope.
ASME NQA-1 Part 1 may interpret mandatory controls; Part 2 is not made
mandatory by this sieve.

## Evidence and validation

- Metrics: `out/2026-10-03/R02-RUN-20261003-25/metrics.json`.
- Readable metrics: `out/2026-10-03/R02-RUN-20261003-25/metrics.md`.
- Local run record: `sieving/runs/RUN-20261003-25/`.
- Source text was not changed.
- Candidate is inactive and has not been promoted.

## Decision needed

Claude review is requested. The reviewer should confirm the 18 statements,
the one-source-typo exception, and whether a corrected candidate may be made
after the generation decision. No audit conclusion or applicability decision
was made in this batch.
