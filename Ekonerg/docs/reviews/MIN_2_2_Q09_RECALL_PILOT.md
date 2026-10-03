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
