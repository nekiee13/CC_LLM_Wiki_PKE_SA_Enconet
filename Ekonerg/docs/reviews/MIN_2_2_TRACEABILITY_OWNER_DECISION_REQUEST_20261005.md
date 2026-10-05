# MIN-2.2 owner decision request — strict raw-source repairs

Status: owner-approved on 2026-10-06. The two approved repairs were applied
as quote-only migrations because downstream evaluation evidence prevented a
generation swap.

## What is being asked

Claude's strict review found two active quote records that are readable and
meaningful, but are not exact verbatim substrings of the linked source chunk.
The repair candidates keep the same criterion and meaning. They replace only
the stored quote text with the source text, so the quote link is exact.

Please provide one explicit owner decision reference for each promotion. The
reference must say that the traceability repair is approved; it must not be
treated as an audit conformity judgment.

Suggested reference IDs (owner may choose different IDs):

- `REPAIR-DOC0019-GEN2-20261005-OWNER` — promote `RUN-20261003-16` over
  `RUN-20261003-14`.
- `REPAIR-DOC0011-GEN3-20261005-OWNER` — promote `RUN-20261005-52` over
  `RUN-20261005-51`.

## Quote-level diff A — DOC-0019, Appendix B III

- Old active item: `CRUMB-DOC-0019-APP_B_III-0003` in `RUN-20261003-14`.
- Replacement item: `CRUMB-DOC-0019-APP_B_III-0006` in `RUN-20261003-16`.
- Change: the candidate preserves the same verification-sequence statement,
  but stores the source's numbered chapter lines (`6. 6.`, `7. 7.`, …) rather
  than the flattened list without the duplicated source numbering.
- Result: 5/5 linked quotes are exact raw-source substrings.
- Full machine diff: [`diff-RUN-20261003-14-to-RUN-20261003-16.json`](../../sieving/runs/RUN-20261003-16/diff-RUN-20261003-14-to-RUN-20261003-16.json)

## Quote-level diff B — DOC-0011, Appendix B VI

- Old active item: `CRUMB-DOC-0011-APP_B_VI-0008` in `RUN-20261005-51`.
- Replacement item: `CRUMB-DOC-0011-APP_B_VI-0011` in `RUN-20261005-52`.
- Change: the candidate preserves the same objective-control statement, but
  stores the source's chapter line breaks and sections 3.3.1–3.3.2 instead of
  a flattened one-line list.
- Result: 14/14 linked quotes are exact raw-source substrings.
- Full machine diff: [`diff-RUN-20261005-51-to-RUN-20261005-52.json`](../../sieving/runs/RUN-20261005-52/diff-RUN-20261005-51-to-RUN-20261005-52.json)

## Safety and next step

The owner decisions are recorded in `manifests/approvals.csv`. The controlled
promotion command was attempted for both candidates and refused by its
downstream-evidence safety gate. The approved source-exact quote text was then
applied to the two existing active quote records without changing generation,
crumb ID, source document, or audit rating. Historical generations remain
retained. See `MIN_2_2_STRICT_QUOTE_MIGRATION_20261006.md` for hashes and
validation.

Claude's review: `CC_2026-10-05T011103Z_strict-candidates-review`.
