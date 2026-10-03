# Prompt history

This is a fresh history for the new company audit. Both prompt candidates were
activated by explicit owner instruction on 2026-10-03. Claude review and
golden-set approval remain pending; no source-edition decision was carried over.

| Candidate | Side | State | Test score | Decision |
|---|---|---|---|---|
| `appb_rule_v1` | RULE | active, owner-authorized | draft calibration pending | `PROMPT-RULE-20261003-V1`; Claude review pending |
| `appb_document_v1` | DOCUMENT | active, owner-authorized | draft calibration pending | `PROMPT-DOCUMENT-20261003-V1`; Claude review pending |

Before promotion or tuning, record the local golden-set result, reviewer
decision, decision reference, and lesson in the relevant local skill. Rejection
or promotion requires a fresh human decision; activation alone does not make a
draft golden set approved.

## Recall-first collection rule (owner instruction, 2026-10-03)

During sieving, prefer high recall. Keep plausible and borderline crumbs when
the source supports them, preserve the exact quote and chapter locator, and mark
uncertain criterion mapping in the statement for later review. Do not invent
source facts or treat a fuzzy candidate as a confirmed audit conclusion.

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
