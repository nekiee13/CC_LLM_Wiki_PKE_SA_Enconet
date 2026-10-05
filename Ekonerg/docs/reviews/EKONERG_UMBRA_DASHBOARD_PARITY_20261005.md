# UMBRA dashboard parity review — 2026-10-05

## Output

[EKONERG_UMBRA_DASHBOARD_2026-10-05.html](../../out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.html)

The page uses the TEKOL file as a layout and interaction reference only. The
production output keeps that page structure (header, six metrics, executive
summary, coverage distribution, filters, expandable criterion cards, matrix,
gaps, actions, and print behavior) and applies the UMBRA dark skin. Its
content is generated from the Ekonerg evidence snapshot.

## Preserved

- 18 Appendix B criterion rows from `MIN-3.1-evidence-matrix-v4.json`, shown in
  expandable evidence-review cards and the sortable matrix.
- Ekonerg metrics: 24 QMS files, 189 vendor crumbs, 55 rule crumbs, 321 quote
  records, 13 criteria with vendor coverage, and 5 without direct vendor crumbs.
- Ekonerg run `RUN-20261003-32`, gate references, and source provenance.
- Withheld score and `0 / 18 judgments recorded`; no rating is inferred.
- Ekonerg evidence gaps, auditor verification actions, responsive layout, and
  printer-friendly output.

## Changed

- Light surfaces were mapped to UMBRA dark semantic tokens.
- Inputs, buttons, badges, tables, cards, focus states, and muted text were
  adjusted for dark-mode contrast.
- Print rules restore a light paper-friendly theme.
- The TEKOL content, score, and rating counts were removed from production
  output. They remain only in the supplied design reference.
- The radar chart is not present in the production UMBRA evidence view.

## Validation

The dashboard generation and focused checks passed:

```text
`build_umbra_conformance_dashboard.py`: PASS; output contains `Ekonerg`,
`Withheld`, 18 criterion cards, filters, matrix, gaps, actions, and no `TEKOL`
or radar content. The evidence/context tests remain green (4 passed).
```

The original HTML file in `docs/dashboard_example` was not modified.
