# MIN-2.2 active quote repair decision

**Status:** prepared for owner decision
**Scope:** two active traceability blockers only
**Rule:** use exact source text; do not approve a fuzzy or invented link

## Why this note exists

The live audit validator checks the active generation for each document. Two
quotes do not match the stored chapter text exactly. The audit cannot move to
scoring until each quote is corrected in a new candidate generation or a
separate exception is explicitly approved.

## Repair A: DOC-0030

- Active run: `RUN-20261003-05`
- Blocked quote: `QUOTE-DOC-0030-0002-01`
- Crumb: `CRUMB-DOC-0030-APP_B_XVI-0002`
- Stored wording begins: `Uvjeti koji zahtijevaju korektivne akcije...`
- Chapter wording begins: `Uvjete koji zahtijevaju korektivne akcije...`
- Existing corrected candidate: `RUN-20261003-06`
- Candidate evidence: its metrics report 9/9 quote links (100%); it is still
  inactive and has not replaced the active generation.

**Required decision:** approve or reject promotion of `RUN-20261003-06` after
reviewing its diff and golden evidence. Promotion must use the controlled
`sieve_generation.py promote` command and an owner decision reference.

## Repair B: DOC-0011

- Active run: `RUN-20261003-35`
- Blocked quote: `QUOTE-DOC-0011-0011-01`
- Crumb: `CRUMB-DOC-0011-APP_B_VI-0003`
- Stored wording uses `imaju`.
- The source chapter `CHUNK-DOC-0011-0004`, section `3.8.3`, uses `imati`:
  `Revizije i promjene moraju na dnu svake stranice i naslovnoj stranici
  imati broj revizije.`

**Required action:** create a new inactive candidate from the source chapter
with the exact wording, run normal linking and metrics, and review the diff.
No active database row has been edited. Promotion requires a later owner
decision and a complete golden check.

## Acceptance criteria

1. The corrected quote is an exact substring of the registered chapter text.
2. The active run is never edited in place.
3. A candidate is inactive until its generation decision is recorded.
4. `validate_traceability.py --active-only --no-record` reports no active quote
   errors after approved promotion.
5. Full-history validation remains available and continues to report any
   unresolved historical records.

## Current gate

The aggregate remains red. No audit score, finding, or conclusion is produced
until both active records pass the controlled repair path.
