# Ekonerg: fair documentation score

[Open the updated dashboard](EKONERG_DASHBOARD.html).

**68.1% — 1225 / 1800 points.** All 18 criteria are rated.
There are **1 full, 11 substantial and 6 partial** matches. None is unmet or
withheld. The approved overall label stays **partially matched**.

The vendor evidence set is unchanged: **475 crumbs**, with **379 score-support
links**. Quotes still open their source chapters. Leads stay out of score support.

## What changed, and why

The written corrective-action controls cover Criterion XVI. The earlier review
reduced it for a separate Part 21 reporting question. That was too harsh for
this criterion. Its rating is now fully matched for documentation.

Full here means that the written controls cover the duty. It does **not** say
that the real audit has already checked how staff follow those controls.
Missing work samples alone do not lower a documentation rating. Real gaps in
the written method still count.

The five-point scale is unchanged: 100, 75, 50, 25 and 0 points. We did not
inflate the weights, add categories or lower the regulatory duties.

| Criterion | Previous points | Current points |
|---|---:|---:|
| I — Organization | 75 | 75 |
| II — QA Program | 75 | 75 |
| III — Design Control | 75 | 75 |
| IV — Procurement Document Control | 75 | 75 |
| V — Instructions, Procedures and Drawings | 75 | 75 |
| VI — Document Control | 75 | 75 |
| VII — Purchased Items and Services | 75 | 75 |
| VIII — Item Identification and Control | 50 | 50 |
| IX — Special Processes | 50 | 50 |
| X — Inspection | 75 | 75 |
| XI — Test Control | 50 | 50 |
| XII — Measuring and Test Equipment | 50 | 50 |
| XIII — Handling, Storage and Shipping | 75 | 75 |
| XIV — Inspection, Test and Operating Status | 50 | 50 |
| XV — Nonconforming Items | 50 | 50 |
| XVI — Corrective Action | 75 | **100** |
| XVII — QA Records | 75 | 75 |
| XVIII — Audits | 75 | 75 |
| **Total** | **1200 / 1800 = 66.7%** | **1225 / 1800 = 68.1%** |

Part 21 remains applicable. Its reporting-path question stays visible in XVI's
contrary argument and ruling. This correction does not declare Part 21 fully
compliant. The other 17 ratings retain their specific written-gap explanations.

## Evidence and history

- [Scoring rubric and source clauses](../../../docs/reviews/DOCUMENT_SCORING_RUBRIC_20261007.md)
- [Exact assessment change and supporting crumb IDs](../../../docs/reviews/DOCUMENT_SCORING_ASSESSMENT_20261007.json)
- [Current evidence matrix](evidence-matrix.md)
- [Previous 66.7% result](../../2026-10-06/manual-refresh/RESULTS.md)
- [Applied preview](preview.json), [old evaluation](transition/before.json),
  and [transaction receipt](transition/completed.json)

Revision: `DOC-SCORING-20261007-01`; evaluation run: `RUN-20261003-32`.
Owner decision: `DOCUMENT-SCORING-20261007-OWNER`.

Database before SHA256:
`e5892a0f99faeed99a4af54de672f2910f2a918374c6c1f896422228e43c2073`.

Database after SHA256:
`43096c594b47fc9ab8593292b0d0ced66447b3052f8c5d8e005f01dc2df74977`.

The old ratings, links and run metadata are also stored in immutable database
history. No source, quote, chapter, generation, evidence link, applicability
ruling or numerical model changed.

## Checks and limits

- Preview/apply/repeat: exit 0; repeat returned `already_applied`.
- Evaluation validation: exit 0; all 18 rows structurally valid.
- Post-apply regression bundle: exit 0; **86 passed**.
- Phase aggregate: exit 0; **8 passes**. Later report/dashboard gate checks
  were skipped, not passed. Evaluation and dashboard structure were checked
  separately.
- Matrix build: exit 0; 18 rows. Dashboard build: exit 0.
- Browser interaction, mobile and print checks: **not run**. The prior browser
  profile failure is still a known limit; the failed method was not repeated.

The owner accepted the mapping and source-transition review items. Two Codex
messages were archived unchanged with a hash manifest. This is owner acceptance,
not a claim that Claude completed those independent reviews. Claude review of
the new scoring correction and paired-skill synchronization remains pending.

This is one completed correction, not a new chain of framework slices. The
other 23 vendor documents still use their previously reviewed generations;
this scoring pass did not repeat their full semantic sieving.
