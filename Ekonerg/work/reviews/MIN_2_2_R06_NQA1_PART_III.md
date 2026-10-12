# MIN-2.2 R-06 — ASME NQA-1 Part III

## What and why

This batch inventories Part III (`DOC-0006`) as non-mandatory guidance. Part
III can explain practical ways to implement Part I (and an invoked Part II
subpart), but it cannot add a new mandatory audit rule.

## Source and authority roles

- Source: `DOC-0006` (`ASME_NQA-1_129-206_Part_3.md`).
- Edition: ASME NQA-1-2015 source snapshot.
- Source role: `INTERPRETIVE`, applicability `CONDITIONAL`.
- Governing baseline linked for context: `DOC-0002`, 10 CFR 50 Appendix B.
- Prompt: `appb_rule_v1`.

## Results

The first run `RUN-20261003-29` is retained as the active trace. A corrected
candidate `RUN-20261003-30` was then made to shorten one quote that crossed an
extraction line break.

Candidate metrics:

- 6 guidance crumbs;
- 6/7 quote links verified (85.7%);
- 0 rejected items;
- 0 failed items;
- all required fields complete.

The crumbs cover the non-mandatory boundary, where guidance may be stored,
process embedding and graded control, training and qualification, and
performance assessment.

## Link exception

One quote contains the source extractor's `� Part III �` marker in the phrase
“Application of this Part's … guidance.” The linker refused to claim a match
for a cleaned version without that marker. The source was not edited. This is
recorded for reviewer choice rather than silently normalizing the source.

## Boundary

Part III remains guidance only. Ekonerg is not judged against it as a separate
mandatory rule. It may help explain how an Ekonerg process works when the same
topic is required by Appendix B and interpreted through NQA-1 Part I.

## Evidence and validation

- Metrics: `out/2026-10-03/R06-RUN-20261003-30/metrics.json`.
- Readable metrics: `out/2026-10-03/R06-RUN-20261003-30/metrics.md`.
- Local run record: `sieving/runs/RUN-20261003-30/`.
- Source text was not changed.
- Candidate is inactive and has not been promoted.

## Decision needed

Claude review is requested for the guidance boundary and the one source-marker
exception. A generation decision is needed before any further candidate is
made.
