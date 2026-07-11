# ADR-0009 — Language policy: sl/en/hr, no translation, verbatim quotes, per-run deliverable language

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet), pattern applies to future entries |
| Register | Master plan §8 decision 3 (assumption replaced) |

## Context

The master plan assumed: quotes preserved in original language, **all analysis text in
English**, with translation-status flags (Task 5.5: `statement_en`, `translation_status`,
`meaning_flag`). The owner replaced that assumption.

## Decision

1. Exactly three languages can occur: **Slovenian, English, Croatian**. Unavoidable; no
   translation layer is built.
2. Raw documents are ingested **as-is**.
3. Evidence quotes are always **verbatim as they exist in the raw documents**, whatever
   the language.
4. Deliverables (Evaluation Report, Dashboard) are generated in **one of the three
   languages, selected per run by the user**.

## Consequences

- **Master plan amendment required (goes into the canonical v1.3 plan as part of A4):**
  Task 5.5 is redefined — mandatory English normalization (`statement_en`) and
  translation-status machinery are dropped; `quote_language` (sl|en|hr) is retained as a
  recorded fact per quote.
- EPIC 11 (report) and EPIC 12 (dashboard) templates and generators take a
  `deliverable_language ∈ {sl, en, hr}` parameter; the chosen language is recorded in run
  metadata and shown on the deliverable.
- `schemas/vocabularies.yml` gains the language enum; validators check it.
- Open implementation detail (to settle at the plan amendment, not a new decision):
  whether internal evaluation records keep one fixed working language or are authored
  directly in the selected deliverable language. The binding constraints are (2)–(4) above.
