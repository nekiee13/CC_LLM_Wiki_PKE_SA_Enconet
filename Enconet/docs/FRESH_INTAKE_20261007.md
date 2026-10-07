# Fresh Enconet intake - 7 October 2026

The owner authorized processing after the archived reset. Registration is not
approval of scope, editions, applicability, calibration or audit results.

## Inventory

The live inventory covers all 36 incoming files:

- 26 vendor Markdown documents.
- Seven regulatory Markdown documents: Appendix B, Part 21 and five ASME parts.
- Three exclusions: desktop.ini, .gitkeep and conversion instructions.

The supplied ASME preface identifies **NQA-1:2015**, issued 20 February 2015.
That is an observed source identity, not an approved scope decision. Parts 2-4
must not automatically be treated as mandatory requirements.

Machine record:
`out/2026-10-07/fresh-intake/incoming-inventory.json`.
It contains filenames, SHA-256, observed titles/publication dates, heading
counts, duplicate flags and exclusions. Unknown dates remain unknown.

## First source batch: SRC-20261007-001

- Source: `NP-SUK-001R8(Nuklearni QA plan).pdf.md`.
- Observed title: NUKLEARNI QA PLAN; identifier NP-SUK-001; revision 8.
- Publication date in source: 14 April 2023.
- Language: Croatian; side: DOCUMENT; supplier: Enconet.
- New-cycle registration: DOC-0001; no old DOC identity inherited.
- Incoming original retained; raw copy write-locked and hash-registered.
- UTF-8 text extraction completed in `derived/DOC-0001.txt`.
- Chapter parser preview: 57 sections, no warnings; joining sections preserves
  the full extracted text. No chapter database writes yet.
- All 36 incoming files still match their reset-time SHA-256 values.

One source was selected for this bounded batch. Twenty-five vendor documents
and seven regulatory files remain unregistered. No crumbs have been generated.

## Safe copy path

The canonical `audit-register` dispatcher now accepts `--preserve-incoming`.
Add `--preview` for a read-only preview; omit it to copy/register. This selects
the local, reusable exclusive-create helper `copy_incoming_source.py` rather
than the legacy move behavior. Existing raw files are never overwritten.
The immutable v2 package was not edited; updated reusable source is kept in
`audit_template/runtime_v2/promote_source.py` for a future release.

The synthetic test verifies preview does not copy, apply preserves incoming,
duplicate apply fails, foreign paths fail and metadata files are excluded.
An initial Windows Temp permission failure was not a pass; an escalated fresh
fixture run passed (`1 passed`, command exit 0).

## Next

Continue bounded source intake, then obtain source/scope decisions before
advancing G1. Confirm output language for this cycle rather than inheriting
the old run's Croatian selection. Prepare a local v3 golden calibration before
prompt activation. Old selectors and old approvals are not authorization for
this cycle. Do not write chaptering through a phase-check bypass.
