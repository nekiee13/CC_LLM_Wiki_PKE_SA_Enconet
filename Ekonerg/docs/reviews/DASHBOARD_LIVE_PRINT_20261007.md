# Live dashboard and print verification

Owner requested completion of the final browser/print checks. No dashboard,
source, evidence, generation or score was changed.

## Result

29 live checks passed in installed Chrome 154.0.8037.98. The final command was:

```text
python Ekonerg/scripts/verify_dashboard_browser.py --html Ekonerg/out/2026-10-07/all18-review/EKONERG_DASHBOARD.html --output Ekonerg/out/2026-10-07/browser-print-final
```

Exit code: 0. The source hash and complete check list are in
`out/2026-10-07/browser-print-final/checks.json`.

- All 18 cards and matrix rows render without JavaScript errors.
- Card expansion, filters, search, sorting, keyboard shortcuts and chapter links work.
- Tablet (768px) and mobile (390px) checks show no page-level horizontal overflow.
- The print button calls print and expands all 18 criterion cards.
- Print uses white paper, hides controls and retains the matrix and criterion details.
- A real 43-page A4 PDF contains 18 rulings and 18 anchor-evidence blocks,
  the supplier name and the unchanged 1400/1800 (77.8%) result.
- Extracted text remains within A4 page boundaries. PDF pages 4 and 43 were
  visually inspected: readable text and no clipped columns were found.

The PDF is `out/2026-10-07/browser-print-final/EKONERG_AUDIT_REPORT.pdf`.
Nested crumb/chapter disclosures keep their existing click-to-open behavior;
the default PDF is a criterion report, not a dump of every full source chapter.
The matrix scrolls inside its wrapper on small screens. A physical printer and
the operating system print dialog were not tested; Chrome's actual PDF print
renderer was tested. No claim of physical-printer certification is made.

## Other validation and limits

```text
python -m pytest Ekonerg/scripts/tests/test_umbra_conformance_dashboard.py -q -p no:cacheprovider --tb=short
```

Exit code: 0; 5 tests passed. An earlier PDF assertion failed (exit 1) because
it searched mixed-case headings that CSS prints in uppercase. Case-insensitive
matching corrected the verifier, not the report or its contents; the final
29-check run passed. The earlier artifact directories are retained as history.

The prior scoring/source reviews were already confirmed. This supplies the last
missing live-UI evidence for CX_2026-10-06T203406Z. Claude confirmation remains
required before archival of that review request. Dark GUI remains paused until
the coordination backlog is cleared.
