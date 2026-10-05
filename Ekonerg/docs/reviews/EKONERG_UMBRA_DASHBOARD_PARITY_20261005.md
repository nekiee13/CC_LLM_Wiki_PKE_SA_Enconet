# UMBRA dashboard parity review — 2026-10-05

## Output

[EKONERG_UMBRA_DASHBOARD_2026-10-05.html](../../out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.html)

The page uses the TEKOL example as its functional source and applies a dark
UMBRA skin. The source content was intentionally kept unchanged, including the
TEKOL name, scores, evidence text, 18 criteria, matrix, gaps, and auditor
actions. This follows the supplied preservation rules.

## Preserved

- 18 criterion records and their original data values.
- Total score: `1499 / 1800` (`83.3%`).
- Rating counts: `3` fully matched, `11` substantially matched, `4` partially matched.
- Header, six metrics, executive summary, classification distribution, cards,
  matrix, remediation gaps, verification actions, and footer.
- Rating filters, search, sorting, expand/collapse, matrix sorting, keyboard
  shortcuts, responsive layout, and print/PDF action.
- Existing IDs, data attributes, JavaScript data, and rendering bindings.

## Changed

- Light surfaces were mapped to UMBRA dark semantic tokens.
- Inputs, buttons, badges, tables, cards, focus states, and muted text were
  adjusted for dark-mode contrast.
- Print rules restore a light paper-friendly theme.
- The radar chart was removed, as explicitly requested. Its data values were
  not changed.

## Validation

The standalone parity check passed:

```text
18 criteria; score total 1499; rating counts 3/11/4;
UMBRA tokens, controls, and print rules present; radar discarded.
```

The original HTML file in `docs/dashboard_example` was not modified.
