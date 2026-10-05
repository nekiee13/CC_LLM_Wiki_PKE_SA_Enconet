# MIN-2.2 v3 candidate quote repairs — 2026-10-06

The two broader v3 candidates were corrected without touching the database or
the active 12-crumb generations.

| Document | Candidate scope | Corrected file | Changed quote |
|---|---:|---|---|
| DOC-0016 | 28 items | `sieving/candidates/repairs-20261005/DOC-0016.json` | `Q09-DOC0016-007`: `provjera` → `provjere` |
| DOC-0021 | 21 items | `sieving/candidates/repairs-20261005/DOC-0021.json` | `Q12-DOC0021-006`: exact clause `3.3.5.` text |

Each corrected file keeps the same item count as its v3 input. The only item
change is the quote text and its source locator. Strict JSON validation passed
for both files. The corrected file hashes are:

- DOC-0016: `937C86A47601D9886DF970901ED0681DD0D1FA7C9EEBF48D783E6AAA904A03B7`
- DOC-0021: `9F8BA03C524B3C145B86EA9DF4ACD6E94A9D69C1842B9DC87BCAC4F142C5A7BA`

These remain separate inactive candidates. They require their own diff review
and owner decision before any promotion. The active generations and dashboard
score are unchanged.
