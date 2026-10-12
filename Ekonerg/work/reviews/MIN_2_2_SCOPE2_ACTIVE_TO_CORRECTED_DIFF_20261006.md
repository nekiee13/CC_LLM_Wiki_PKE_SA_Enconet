# MIN-2.2: active-to-corrected scope-two diff

This is the owner-facing comparison requested by Claude. It compares each
active 12-crumb generation with the corrected 28/21-item JSON candidate. The
existing database diff files provide the stable item IDs; the corrected JSON
files provide the exact replacement quotes.

## DOC-0016

- Active generation: `RUN-20261004-49` (12 crumbs)
- Corrected candidate: `sieving/candidates/repairs-20261005/DOC-0016.json`
  (28 crumbs)
- Net change: 16 new crumbs and one replacement of an older equivalent crumb.
- Added IDs are listed in the generated diff:
  `sieving/runs/RUN-20261005-61/diff-RUN-20261004-49-to-RUN-20261005-61.md`
- Added groups: four APP_B_VIII, four APP_B_XI, four APP_B_XIII, four
  APP_B_XIV, plus replacement `CRUMB-DOC-0016-APP_B_XVII-0034` for the older
  equivalent `CRUMB-DOC-0016-APP_B_XVII-0028`.
- Corrected replacement quote: `Q09-DOC0016-007` uses the exact source wording
  (`provjere`). The corrected candidate hash is
  `937c86a47601d9886df970901ed0681dd0d1fa7c9eebf48d783e6aaa904a03b7`.

## DOC-0021

- Active generation: `RUN-20261004-42` (12 crumbs)
- Corrected candidate: `sieving/candidates/repairs-20261005/DOC-0021.json`
  (21 crumbs)
- Net change: nine new crumbs and one replacement of an older equivalent
  crumb.
- Added IDs are listed in the generated diff:
  `sieving/runs/RUN-20261005-66/diff-RUN-20261004-42-to-RUN-20261005-66.md`
- Added groups: replacement `CRUMB-DOC-0021-APP_B_IV-0009` for
  `CRUMB-DOC-0021-APP_B_IV-0006`, one APP_B_XI crumb, four APP_B_XIII crumbs,
  and four APP_B_XIV crumbs.
- Corrected replacement quote: `Q12-DOC0021-006` cites the exact clause 3.3.5
  text. The corrected candidate hash is
  `9f8ba03c524b3c145b86ea9df4acd6e94a9d69c1842b9dc87bcac4f142c5a7ba`.

The database diff files still belong to the stale candidates and therefore
must not be promoted. They are used here only for stable item-ID comparison.
Fresh database generations will be created only after the owner authorizes
rejection of the stale candidates.
