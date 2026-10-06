# Prompt history

This is a fresh history for the new company audit. Both prompt candidates were
activated by explicit owner instruction on 2026-10-03. Claude review and
golden-set approval remain pending; no source-edition decision was carried over.

| Candidate | Side | State | Test score | Decision |
|---|---|---|---|---|
| `appb_rule_v1` | RULE | active, owner-authorized | draft calibration pending | `PROMPT-RULE-20261003-V1`; Claude review pending |
| `appb_document_v1` | DOCUMENT | previous | draft calibration pending | `PROMPT-DOCUMENT-20261003-V1`; retained for comparison |
| `appb_document_v2_concept_recall` | DOCUMENT | active, owner-authorized | pilot pending | `PROMPT-DOCUMENT-20261003-V2`; Claude review pending |
| `appb_document_v3_context_anchors` | DOCUMENT | active, owner-approved | DOC-0016 v3 golden and generation approved | `DOC0016-V3-GEN5-PROMOTE-20261004-OWNER` |

Before promotion or tuning, record the local golden-set result, reviewer
decision, decision reference, and lesson in the relevant local skill. Rejection
or promotion requires a fresh human decision; activation alone does not make a
draft golden set approved.

## Recall-first collection rule (owner instruction, 2026-10-03)

During sieving, prefer high recall. Keep plausible and borderline crumbs when
the source supports them, preserve the exact quote and chapter locator, and mark
uncertain criterion mapping in the statement for later review. Do not invent
source facts or treat a fuzzy candidate as a confirmed audit conclusion.

## Evidence context anchors (framework pivot, 2026-10-04)

The active document prompt now requests optional evidence types and source-stated
project, contract, supplier, revision, and date anchors. Anchors are never
inferred. Existing crumbs and the v2 prompt version remain valid; the extension
only adds context when the source explicitly supports it.

## Versioned anchor calibration (owner decision, 2026-10-04)

The owner selected Option A after the anchor extension was identified as a
post-approval prompt change. The extension is carried in
`appb_document_v3_context_anchors`; it requires a fresh golden calibration and
owner approval before activation. The v2 approval remains tied to the exact v2
prompt text.

## Vendor evidence depth rule (owner clarification, 2026-10-03)

A vendor's high-level reference to a regulation, standard, or QMS process is a
lead, not objective proof. The DOCUMENT sieve should also seek deeper evidence:
roles, approvals, records, registers, forms, reports, outputs, acceptance
criteria, training, revision history, and implementation examples. If the
deeper evidence is absent, retain the reference as a candidate and flag that
objective evidence was not shown.

## Concept-recall candidate v2 (2026-10-03)

`appb_document_v2_concept_recall` adds a second pass over every chapter or
chunk. It uses criterion intent cards to collect direct controls, supporting
controls, and candidate leads without a fixed crumb cap. It remains a candidate
until its pilot and fresh owner/reviewer decision are recorded; activation is
not implied by creating the prompt.

## Generation rejection lesson

| Prompt | Side | Event | Generation | Date | Decision by | Scope | Lesson |
|---|---|---|---|---|---|---|---|
| `appb_rule_v1` | RULE | candidate rejected | `RUN-20261003-30` | 2026-10-03 | Owner | R-06 Part III source-marker correction | `sieving-tuning`: preserve em-dash-delimited source markers exactly before creating a replacement generation. |
| `appb_document_v2_concept_recall` | DOCUMENT | candidate promoted | `RUN-20261003-40` | 2026-10-04 | Owner | Q09 DOC-0016 exact-quote correction | `sieving-tuning`: preserve localized source spelling and verify every quote as an exact source substring before promotion. |
| `appb_document_v3_context_anchors` | DOCUMENT | candidate promoted | `RUN-20261004-49` | 2026-10-04 | Owner | PIVOT-4 source-context-anchor versioning | `sieving-tuning`: keep source-stated context anchors, never infer them, and retain candidate leads as leads. |
| `appb_document_v1` | DOCUMENT | repair promotion | `RUN-20261003-06` | 2026-10-05 | Owner | REPAIR-DOC0030-GEN2-20261005-OWNER | `sieving-tuning`: preserve exact source wording when correcting a traceability candidate; promote only after a complete approved repair score. |
| `appb_document_v2_concept_recall` | DOCUMENT | repair candidate | `RUN-20261005-50` | 2026-10-05 | Owner | REPAIR-DOC0011-GEN2-20261005-OWNER | `sieving-tuning`: retain the exact source wording when repairing one quote; do not alter unrelated crumbs. |
| `appb_document_v3_context_anchors` | DOCUMENT | full-source replacement promoted | `RUN-20261006-77` | 2026-10-06 | Owner, PROMOTE-MANUAL-FULL-20261006-OWNER | DOC-0032 replaces incomplete DOC-0031; 279 golden matches; assessment refreshed atomically | `sieving-tuning`: switch source and downstream assessments together; retain old evidence and scores; exclude candidate leads from score support. |
