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
