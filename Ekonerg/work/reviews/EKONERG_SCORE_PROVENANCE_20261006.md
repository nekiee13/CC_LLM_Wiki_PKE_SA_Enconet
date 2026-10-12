# Ekonerg score provenance - RUN-20261003-32

## Owner decision used for display

On 2026-10-06 the owner decided that the documented Ekonerg pre-flight ratings
may be treated as official audit-tool results and do not require human
re-entry or human review. The decision is recorded as
`OWNER-DECISION-20261006-SCORING-PROVENANCE-OFFICIAL` in `manifests/approvals.csv`.
The owner also decided that no judgment-entry form is needed; see
`OWNER-DECISION-20261006-JUDGMENT-FORM-NO`.

This result is official for the documentation-based pre-flight tool. It is not
a claim that controls operated in practice; a later real audit may test
implementation and objective records.

### Earlier display instruction

The earlier owner instruction was supplied in the project conversation. It was:

> You cant withold conformance score. Each criteria must be evaluated and final
> conformace score must be provided. Each criteriam must be subjected to 5 point
> scale. Check Enconets methodology.

This is a presentation instruction. It is not a recorded human approval of the
18 database evaluation rows.

## Database and model facts

- Run: `RUN-20261003-32`
- Database: `db/nqa_audit.sqlite`
- Evaluation rows: 18 in `criterion_evaluations`
- Human reviewer fields: none; the `criterion_evaluations` table has no reviewer
  column, and every `judge_ruling` says `Codex evidence evaluation`.
- Approved model: `1.0-ekonerg-20261004`, approval `G3-RUN-20261003-32`.
- Approved weights: fully 1.00, substantially 0.75, partially 0.50, minimally
  0.25, unmet 0.00.
- Recomputed result with the approved model: `52.8%`, `partially`, from
  `2 fully + 8 substantially + 3 partially + 0 minimally + 5 unmet` over 18.
- Quarantine: **not performed**. Rows are not marked provisional and still feed
  `score_evaluation.py` and the current dashboard.

The dashboard code uses the same weights as the approved Ekonerg model. The
phrase "Enconet five-level scale" describes the inherited five-level vocabulary;
the live evaluation run checks and records the approved Ekonerg model version.
The published 52.8% therefore does not change when recomputed with the approved
model. Under the dated owner decision above, the generated dashboard is the
completion artifact for this owner-operated pre-flight run; the absence of a
database reviewer column does not block this tool result.

## Criterion-by-criterion record

All ratings below were written by Codex from the active Ekonerg vendor-document
snapshot using `scripts/evaluate_ekonerg_run.py`. The owner has decided that
human re-entry or human review is not required for this documentation-based
pre-flight result. `Policy only` means the evidence is procedure or QMS text; it is not
an implementation record, operating sample, completed audit file, certificate,
or other proof that the control operated.

| Criterion | Rating / scale | Rating source | Human reviewer | Evidence type |
|---|---|---|---|---|
| I Organization | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; implementation records absent |
| II QA Program | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; lower-level implementation records absent |
| III Design Control | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; project design records absent |
| IV Procurement Document Control | partially / 3 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; complete flow-down evidence absent |
| V Instructions, Procedures, and Drawings | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; representative job instructions absent |
| VI Document Control | fully / 5 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Document-control procedure text; executed records absent |
| VII Control of Purchased Items and Services | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; supplier implementation records absent |
| VIII Identification and Control of Items | unmet / 1 of 5 | No direct DOCUMENT crumb; Codex absence rationale | none | No vendor evidence in active snapshot |
| IX Control of Special Processes | unmet / 1 of 5 | No direct DOCUMENT crumb; Codex absence rationale | none | No vendor evidence in active snapshot |
| X Inspection | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; completed inspection records absent |
| XI Test Control | unmet / 1 of 5 | No direct DOCUMENT crumb; Codex absence rationale | none | No vendor evidence in active snapshot |
| XII Control of Measuring and Test Equipment | partially / 3 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; certificates and use records absent |
| XIII Handling, Storage, and Shipping | unmet / 1 of 5 | No direct DOCUMENT crumb; Codex absence rationale | none | No vendor evidence in active snapshot |
| XIV Inspection, Test, and Operating Status | unmet / 1 of 5 | No direct DOCUMENT crumb; Codex absence rationale | none | No vendor evidence in active snapshot |
| XV Nonconforming Items | partially / 3 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; completed nonconformance records absent |
| XVI Corrective Action | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Policy/QMS text; executed corrective-action records absent |
| XVII Quality Assurance Records | fully / 5 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Records procedure text; sampled records absent |
| XVIII Audits | substantially / 4 of 5 | Codex rationale and linked DOCUMENT crumbs | none | Audit procedure text; completed audit files absent |

## Status requested by Claude

The 18 rows are **Codex-generated documentation evaluations**, not human-entered
judgments. The owner has approved their use as the official result of this
pre-flight tool, so they remain in the score command and dashboard and are not
quarantined. This record does not claim that the score proves operating
performance or replaces a later real audit.
