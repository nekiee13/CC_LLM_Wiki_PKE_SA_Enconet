# Enconet — separate dark dashboard

[Open the dark dashboard](../outputs/candidates/evidence_access/RUN-20261008-17/dark/enconet_appendix_b_dashboard_dark.html).
[Open the unchanged light dashboard](../outputs/enconet_appendix_b_dashboard.html).

This is a separate screen presentation of the verified Enconet release, not a
new audit. The score remains **80.6%** across all 18 criteria. The light file,
report, database, sources, approval rows and published release manifest are
unchanged. No new gate or independent-review approval is claimed.

## Appearance

The local, company-neutral dark builder was already copied into this project.
Its UMBRA-inspired foundations are now adapted to the current dashboard's
native components. Runtime reads only Enconet's own scripts, CSS and light
dashboard; it does not read another company's files.

The dark copy uses teal background lighting, luminous score accents, a faint
geometric grid, dark layered panels, semantic rating colors and a decorative
mouse spotlight. Inputs, buttons, table cells, quotes, source chapters and the
evidence drawer use readable dark surfaces. Keyboard focus remains visible.
Motion is disabled when reduced motion is requested; touch does not enable
the cursor effect. Printing still uses the original light theme.

No chart, form, rating, evidence, criterion, control or navigation scheme was
added or removed. The original script and embedded audit data remain verbatim.
The reference-list observer now safely handles both supported card layouts.

## Verification

All successful commands returned exit **0**, using
`C:/xPY/vEnv/WikiEnconet/python.exe`:

- `-m pytest Enconet/tests/test_dark_dashboard.py -q -p no:cacheprovider`:
  five passed. RED first found two missing native-layout protections, exit 1.
  One subsequent non-escalated retry hit pytest's temporary-folder permissions;
  rerun outside the sandbox passed. No failed check is counted as success.
- `Enconet/scripts/build_dark_dashboard.py --source Enconet/outputs/enconet_appendix_b_dashboard.html --output Enconet/outputs/candidates/evidence_access/RUN-20261008-17/dark/enconet_appendix_b_dashboard_dark.html`:
  builds a fresh separate file; refuses source overwrite or repeated overlay.
- `Enconet/out/2026-10-10/dark-dashboard/check_dark.py`:
  dashboard/evidence validators pass; 18 criteria and 80.6 preserved. Tested
  rating filter, search and empty state, reverse sorting, card expand/collapse,
  all 134 referenced crumbs and source chapters, desktop/mobile layout and
  printing. Zero network requests and page errors. The first browser assertion
  assumed short Roman IDs; it was corrected to the actual APP_B identifiers,
  with no dashboard/data change, then all checks passed.
- `Enconet/scripts/run_regression_tests.py --output Enconet/out/2026-10-10/dark-dashboard/regression`:
  **478 passed**, 177 current and 301 historical; zero failures, errors or skips.
  Live audit hash guard passed. No concurrent output-writing validation ran.

The new file inherits ordinary Users read/execute permissions, independently
checked without escalation. It does not carry the private staging ACL defect.

Light SHA-256:
`bf62a3fe044e488a9659c0d74b03df04f40c519c608bfc5b7da81d792ec633f1`.

Dark SHA-256:
`7d6e17cb02270d02b09d73bece7b584bcec399532de8843ca8029ba7a9017063`.

## Artifacts

- [Build provenance](../outputs/candidates/evidence_access/RUN-20261008-17/dark/enconet_appendix_b_dashboard_dark.provenance.json)
- [Browser/data verification](../out/2026-10-10/dark-dashboard/verification.json)
- [Desktop screenshot](../out/2026-10-10/dark-dashboard/dark-desktop.png)
- [Mobile screenshot](../out/2026-10-10/dark-dashboard/dark-mobile.png)
- [Actual light-print PDF](../out/2026-10-10/dark-dashboard/dark-print.pdf)
- [Full-suite record](../out/2026-10-10/dark-dashboard/regression/summary.json)

The desktop/mobile screenshots were visually inspected. The PDF was exported
after checking that print-mode body background is white and decorative light
is hidden. Original print CSS remains unchanged.

Claude review remains deferred. Requested review: check the screen-only skin,
data/script parity, native reference observer safety, contrast, controls and
print/accessibility behavior. Canonical light publication remains unchanged;
this dark copy is available separately for owner visual review.
