# MIN-2.2 traceability candidate repairs

Status: inactive candidates; owner generation decision required.

Claude's strict review found two active quote records whose stored text is not a
verbatim raw-source substring. No matcher relaxation was used. The candidates
below preserve the existing crumb meaning and replace only the quote text with
source text that links exactly.

| Document | Candidate | Result | Decision needed |
|---|---|---:|---|
| DOC-0019 | `RUN-20261003-16` | 5 items, 5/5 exact links | Owner promotion decision |
| DOC-0011 | `RUN-20261005-52` | 12 items, 14/14 exact links | Owner golden/promotion decision |

The DOC-0019 candidate already existed as an inactive corrected generation. The
DOC-0011 candidate was created from `RUN-20261005-51` with the chapter-list
quote preserved with its source line breaks. Both candidates remain inactive;
the active generations were not changed.

## Checks

```text
RUN-20261003-16: 5 linked quotes; 5 raw-source substrings
RUN-20261005-52: 14 linked quotes; 14 raw-source substrings
```

Promotion must wait for explicit owner decision references and approved golden
fixtures. Until then, the live active generation and dashboard remain unchanged.
