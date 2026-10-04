# PIVOT-5 — DOC-0016 context-anchor pilot

**Status:** blocked pending an approved rejection decision for the first pilot candidate

## What this pilot tests

The pilot checks whether the updated concept-recall prompt can carry small evidence
anchors with each vendor crumb. It uses DOC-0016 (`PQ07.5-7_r10_Kontrola_zapisa.md`)
and keeps the active audit generation unchanged.

## First candidate and why it is not usable

`RUN-20261004-43` was created from the earlier Q09 v2 fixture. The candidate imported
12 crumbs and 11 quote links. One quote did not match the raw document because the
fixture contains the stale text `Zapise s provjera generira tim za provjeru`; the
source says `Zapise s provjere generira tim za provjeru`.

The candidate is therefore **not promoted**. It remains an inactive, immutable
candidate in the database. The active run `RUN-20261003-40` is unchanged.

The normal generation tool requires an approved decision reference before it can
reject a candidate. No approval record for rejecting `RUN-20261004-43` exists yet.
This is a safety gate: it prevents a candidate from being removed without a traceable
human decision.

## Corrected input prepared

The corrected pilot input is:

`sieving/DATA/production/2026-10-04/q09_doc0016_context_pilot_corrected.json`

It is based on the already corrected golden fixture and adds only these anchors:

- 10 items: `evidence_type=policy_or_procedure`;
- 2 items: `evidence_type=candidate_lead`;
- all 12 items: `context.source_revision=10`;
- no project, contract, supplier, or evidence date is inferred.

The corrected input is ready for the next candidate run after the stale candidate is
rejected through the normal approval gate.

## Requested decision

Please approve a new decision reference for rejecting `RUN-20261004-43` because it
contains one stale quote and cannot satisfy the zero-unmatched-quote gate. After that
decision is recorded, Codex will run the corrected candidate as `RUN-20261004-44`,
verify all 12 links and context rows, and request the normal review. No audit score or
finding changes are made by this pilot.

