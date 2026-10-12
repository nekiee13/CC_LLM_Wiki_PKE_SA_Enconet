# MIN-2.2 R-03 — ASME NQA-1 Preface

## What and why

This batch processes the NQA-1 preface (`DOC-0003`). It explains how NQA-1 is
used to interpret the Appendix B baseline. It does not turn every sentence in
NQA-1 into a mandatory audit requirement.

## Source and authority roles

- Source: `DOC-0003` (`ASME_NQA-1_000-013_Preface.md`).
- Edition shown in the source: ASME NQA-1-2015, issued February 20, 2015.
- Source role: `INTERPRETIVE`.
- Governing baseline linked for context: `DOC-0002`, 10 CFR 50 Appendix B.
- Prompt: `appb_rule_v1`.

## Results

Active run `RUN-20261003-26` produced six reference crumbs:

- 6 crumbs;
- 7/7 quote links verified (100%);
- 0 rejected items;
- 0 failed items;
- all required fields complete.

The crumbs record that NQA-1 covers quality-affecting organizations and
activities, distinguishes requirements from guidance, places requirements in
Part I and Part II, places guidance in Part III and Part IV, and keeps formal
interpretations in a separate section.

## Important boundary

This batch does not make Part II mandatory. Owner direction remains controlling:
NQA-1 Part I is the mandatory interpretation baseline, while Part II is not
mandatory by default. Part II can still provide useful context when a specific
Ekonerg activity or contract makes it relevant.

The broad preface crumbs are orientation evidence. Detailed clause evidence
will come from the separate Part I, Part II, Part III, and Part IV source
streams.

## Evidence and validation

- Metrics: `out/2026-10-03/R03-RUN-20261003-26/metrics.json`.
- Readable metrics: `out/2026-10-03/R03-RUN-20261003-26/metrics.md`.
- Local run record: `sieving/runs/RUN-20261003-26/`.
- Canonical authority configuration now includes DOC-0003 through DOC-0007 as
  interpretive standard sources.
- Source text was not changed.

## Decision

No generation decision is needed for this first active run. Claude review is
requested for the boundary wording and for the separation of mandatory Part I
from non-mandatory Part II, III, and IV material.
