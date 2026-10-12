# MIN-2.2 R-05 — ASME NQA-1 Part II

## What and why

This batch inventories Part II (`DOC-0005`) as conditional interpretation
context. Part II is not mandatory by default under the owner's decision. It
becomes relevant only when a contract, regulation, organization, or other
specifying document invokes a subpart.

## Source and authority roles

- Source: `DOC-0005` (`ASME_NQA-1_047-128_Part_2.md`).
- Edition: ASME NQA-1-2015 source snapshot.
- Source role: `INTERPRETIVE`, applicability `CONDITIONAL`.
- Governing baseline linked for context: `DOC-0002`, 10 CFR 50 Appendix B.
- Prompt: `appb_rule_v1`.

## Results

Active run `RUN-20261003-28` produced six context crumbs:

- Part II invocation and graded applicability;
- the invoking organization's responsibility;
- cleaning and cleanness control (Subpart 2.1);
- packaging, shipping, receiving, storage, and handling (Subpart 2.2);
- housekeeping (Subpart 2.3); and
- structural concrete, steel, soils, and foundations (Subpart 2.5).

Metrics:

- 6 crumbs;
- 6/6 quote links verified (100%);
- 0 rejected items;
- 0 failed items;
- all required fields complete.

## Boundary

These crumbs are a routing map, not mandatory audit criteria. The audit must
first check whether Ekonerg's work, contract, or a governing requirement
invokes a particular Part II subpart. If no invocation is found, the subpart is
not treated as a mandatory requirement. Part I remains the mandatory NQA-1
interpretation baseline.

## Evidence and validation

- Metrics: `out/2026-10-03/R05-RUN-20261003-28/metrics.json`.
- Readable metrics: `out/2026-10-03/R05-RUN-20261003-28/metrics.md`.
- Local run record: `sieving/runs/RUN-20261003-28/`.
- Source text was not changed.

## Decision

No generation promotion is requested. Claude review is requested for the
conditional boundary and for whether any additional Part II subpart is needed
for Ekonerg's design, engineering-service, or consultancy scope.
