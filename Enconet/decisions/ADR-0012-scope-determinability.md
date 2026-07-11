# ADR-0012 — Undeterminable supplier scope is a non-conformance, never a silent N/A

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet), rule applies to every supplier evaluation |
| Register | Master plan §8 decision 6 (reframed by the owner) |

## Context

Applicability rulings (master plan Task 8.1) need a documented statement of the supplier's
scope of activity. The plan asked *which* document supplies it (contract, PO scope, QA
manual). The owner reframed the question into a rule.

## Decision

1. The supplier's scope **must be clearly determinable from the raw documents** provided
   for the evaluation.
2. If the scope cannot be determined from the raw documents, that is itself treated as a
   **non-conformance to Appendix B requirements** — recorded as a finding — not as a
   reason to mark criteria "not applicable".

## Consequences

- **Master plan amendment required (part of A4 on the canonical plan):** Task 8.1 gains
  the rule — every `not-applicable` ruling must cite scope evidence by crumb/document ID
  from `raw/`; if no adequate scope statement exists, a finding is raised (scope
  documentation gap), N/A rulings are blocked, and the affected criteria are evaluated as
  applicable against the available evidence.
- The evaluation validator (Task 8.6) fails any applicability matrix whose N/A rulings
  lack raw-doc citations.
- No standing "scope source" question remains for the owner: the burden sits on the
  supplier's raw documentation, where an auditor expects it.
