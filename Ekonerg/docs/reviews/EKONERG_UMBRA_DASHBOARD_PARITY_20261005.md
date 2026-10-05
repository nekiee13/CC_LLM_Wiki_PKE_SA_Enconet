# UMBRA dashboard parity review — 2026-10-05

## Output

[EKONERG_UMBRA_DASHBOARD_2026-10-05.html](../../out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.html)

The page uses the TEKOL file only as a visual reference. The production output
is generated from the Ekonerg evidence snapshot and uses the dark UMBRA skin.
It contains Ekonerg as the supplier, Ekonerg run and gate references, the
Ekonerg matrix counts, and a withheld score because no human judgments exist.

## Preserved

- 18 Appendix B criterion rows from `MIN-3.1-evidence-matrix-v4.json`.
- Ekonerg metrics: 24 QMS files, 189 vendor crumbs, 55 rule crumbs, 321 quote
  records, 13 criteria with vendor coverage, and 5 without direct vendor crumbs.
- Ekonerg run `RUN-20261003-32`, gate references, and source provenance.
- Withheld score and `0 / 18 judgments recorded`; no rating is inferred.
- Ekonerg evidence queue, reading batches, gates, judgment form, responsive
  layout, and printer-friendly output.

## Changed

- Light surfaces were mapped to UMBRA dark semantic tokens.
- Inputs, buttons, badges, tables, cards, focus states, and muted text were
  adjusted for dark-mode contrast.
- Print rules restore a light paper-friendly theme.
- The TEKOL content, score, and rating counts were removed from production
  output. They remain only in the supplied design reference.
- The radar chart is not present in the production UMBRA evidence view.

## Validation

The dashboard generation and focused tests passed:

```text
`build_evidence_dashboard.py`: PASS; `pytest` focused dashboard/context tests:
4 passed; output contains `Ekonerg`, `Withheld`, and no `TEKOL` text.
```

The original HTML file in `docs/dashboard_example` was not modified.
