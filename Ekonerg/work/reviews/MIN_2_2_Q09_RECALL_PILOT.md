# MIN-2.2 Q-09 — Concept-recall pilot

## Purpose

This pilot tests the owner-authorized `appb_document_v2_concept_recall` prompt
on a vendor document that previously had no active sieve run. It uses the
quality-goal cards and two-pass collection rule. It is a sieve result, not a
conformance conclusion.

## Result

- Source: `DOC-0016` — `PQ07.5-7_r10_Kontrola_zapisa.md`.
- Run: `RUN-20261003-33`.
- Prompt: `appb_document_v2_concept_recall`.
- Crumbs collected: **12**.
- Quote links: **11/12 (91.7%)**.
- Rejected items: 0.
- Failed items: 0.
- Active vendor crumbs changed from **109 to 121**.

The pilot collected multiple separate record controls, organization roles,
document identifiers, review/approval controls, retention, audit-record leads,
and design-record leads from one document. This is broader than the old
five-to-eight-crumb pattern.

## Exception

One quote was shortened during preparation (`provjera` instead of the exact
source phrase `provjere`). The linker refused it. The item remains visible as
an unresolved pilot defect and must be corrected in a new candidate generation;
it must not be treated as linked evidence.

## Coverage still open

Five vendor documents still have no active sieve run: `DOC-0011`, `DOC-0020`,
`DOC-0021`, `DOC-0022`, and `DOC-0031`. The coverage guard therefore remains
red until those documents receive v2 runs.

## Q-10 continuation

The next uncovered document was processed with the same owner-authorized prompt:

- Source: `DOC-0011` — `PQ07.5-2_r8_Postupci_sustava_kvalitete,_sustava_za.md`.
- Run: `RUN-20261003-35`.
- Crumbs collected: **12**.
- Quote links: **12/13 (92.3%)**. One crumb contains two quotes; one of those
  quotes combined text across a formatting break and was correctly left
  unmatched by the linker.
- Rejected items: 0.
- Failed items: 0.

This continuation adds direct evidence for document control, responsibilities,
procedure content, objective-evidence requirements, revision distribution, and
record retention. The unmatched quote is an evidence-preparation defect, not a
conformance conclusion; it remains visible for later correction or candidate
regeneration.

After Q-10, active vendor coverage is **20 runs and 133 crumbs**. Four vendor
documents remain without an active run: `DOC-0020`, `DOC-0021`, `DOC-0022`, and
`DOC-0031`.

## Q-11 continuation

The following uncovered document was then processed:

- Source: `DOC-0020` — `PQ08.2-1_r6_Odnosi_s_Naručiteljima.md`.
- Run: `RUN-20261003-36`.
- Crumbs collected: **12**.
- Quote links: **14/14 (100%)**.
- Rejected items: 0.
- Failed items: 0.

The run captured customer-requirement communication, assigned roles, customer
feedback records, complaint handling, nonconformance/corrective-action triggers,
and retention of complaint evidence. This is supporting evidence to review
against Appendix B; it is not a conformance conclusion.

After Q-11, active vendor coverage is **21 runs and 145 crumbs**. Three vendor
documents remain without an active run: `DOC-0021`, `DOC-0022`, and `DOC-0031`.

## Q-12 continuation

The next uncovered document was processed:

- Source: `DOC-0021` — `PQ08.2-2_r5_Priprema_i_postupanje_s_ugovornom_doku.md`.
- Run: `RUN-20261003-37`.
- Crumbs collected: **12**.
- Quote links: **15/16 (93.8%)**. One quote omitted the source heading prefix
  and was left unmatched by the linker.
- Rejected items: 0.
- Failed items: 0.

The run captured contract and offer review, supplier controls, quality-plan
inputs, approval, document identification, closeout checks, and controlled
record retention. The unmatched quote remains an evidence-preparation defect,
not a conformance conclusion.

After Q-12, active vendor coverage is **22 runs and 157 crumbs**. Two vendor
documents remain without an active run: `DOC-0022` and `DOC-0031`.

## Q-13 continuation

The next uncovered document was processed:

- Source: `DOC-0022` — `PQ08.3-1_r4_Kontrola_studijskih_projektnih_radova_.md`.
- Run: `RUN-20261003-38`.
- Crumbs collected: **14**.
- Quote links: **21/21 (100%)**.
- Rejected items: 0.
- Failed items: 0.

The run captured design inputs, independent review and verification, quality
plans, oversight, collaboration controls, change approval, corrective-action
leads, and retention of design records. The `APP_B_XVI` entries are retained as
candidate leads until the underlying corrective-action records are checked.

After Q-13, active vendor coverage is **23 runs and 171 crumbs**. Only the
management manual `DOC-0031` remains without an active run.

## Q-14 continuation and coverage close

The final uncovered document was processed:

- Source: `DOC-0031` — `Priručnik_sustava_upravljanja_rev.5.md`.
- Run: `RUN-20261003-39`.
- Crumbs collected: **18**.
- Quote links: **24/24 (100%)**.
- Rejected items: 0.
- Failed items: 0.

The run captured the manual's Appendix B scope, document control, roles,
controlled copies, records, design/procurement/audit/corrective-action leads,
and its definitions of objective evidence and quality assurance. Heading-only
items are candidate leads until the referenced procedures and records are
checked.

The coverage guard now passes: **24 of 24** registered vendor documents have
active runs and non-zero crumbs, for **189 active crumbs** total. This closes
the recall-coverage pass; it does not create conformance findings or a score.
