# UMBRA dashboard parity review — 2026-10-05

## Output

[EKONERG_UMBRA_DASHBOARD_2026-10-05.html](../../out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.html)

The page copies the supplied TEKOL page's light layout and interaction model.
It keeps the header, six metrics, executive summary, classification
distribution, filters, expandable criterion cards, sortable matrix, gaps,
actions, responsive behavior, and print behavior. The visible data is Ekonerg
only.

## Evaluation result

The dashboard reads the approved local run `RUN-20261003-32`, which contains
one ruling for each of the 18 applicable Appendix B criteria.

- Overall conformance: **52.8% (950 / 1800 points)** — **Partially Matched**.
- Five-level scale: fully 5/5 = 100, substantially 4/5 = 75, partially 3/5
  = 50, minimally 2/5 = 25, unmet 1/5 = 0.
- Distribution: 2 fully, 8 substantially, 3 partially, 0 minimally, 5 unmet.
- Unmet criteria are VIII, IX, XI, XIII, and XIV because the active Ekonerg
  vendor snapshot has no direct vendor crumb for them.

The canonical evaluation package is
[EKONERG_EVALUATION_20261005.json](../../out/2026-10-05/EKONERG_EVALUATION_20261005.json).

## Preserved

- 18 Appendix B criterion rows from `MIN-3.1-evidence-matrix-v4.json`, shown
  in expandable evidence-review cards and the sortable matrix.
- Ekonerg evidence metrics: 24 QMS files, 189 vendor crumbs, 55 rule crumbs,
  321 quote records, 13 criteria with vendor coverage, and 5 without direct
  vendor crumbs.
- Ekonerg source boundary, run ID, gate references, and source provenance.
- Evidence gaps, auditor verification actions, responsive layout, and
  printer-friendly output.

## Changed

- Removed the dark override. The generated page now uses the TEKOL light
  presentation tokens and controls.
- Replaced the withheld state with the recorded five-level criterion ratings
  and final conformance score.
- Kept the radar chart excluded as previously directed; no new workflow or
  supplier data was introduced.

## Criterion traceability

Each expandable criterion card now includes:

- a short criterion summary and the full affirmative, contrary, and ruling
  explanation;
- the score in both percentage and five-level form (for example, `75% · 4/5`);
- a score trace showing the rating, points, and number of linked vendor crumbs;
- a collapsible list of the exact crumb IDs linked to that criterion's
  evaluation record.

The matrix also reports the number of linked score crumbs for each criterion.
This follows the Enconet dashboard contract: `refs` are supporting crumb IDs,
while `aff`, `con`, `judge`, and `verify` explain the criterion decision.

## Validation

The generator passed and the output contains no `TEKOL`, `Withheld`, dark
theme, radar, or historic score text. The source HTML in
`docs/dashboard_example` was not modified.

The evaluation run was independently checked with:

```text
validate_evaluation.py: PASS - 18/18 structurally valid
score_evaluation.py: 52.8; classification=partially; counts=2/8/3/0/5
```
