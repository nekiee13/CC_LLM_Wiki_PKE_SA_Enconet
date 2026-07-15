---
id: {{DECISION_REF}}
type: gate-decision
status: draft
content_origin: mixed
source: project-state.yml; manifests/approvals.csv
gate: {{GATE}}
decision: pending
decision_date: n-a
reviewer: n-a
supplier: {{SUPPLIER}}
---

# {{GATE}} decision packet — {{SUPPLIER}}

## Summary

{{SUMMARY}}

## Evidence pointers

{{EVIDENCE_POINTERS}}

## Validation results

{{VALIDATION_RESULTS}}

## What the human must check

- Open every evidence pointer and confirm it identifies the reviewed supplier and gate.
- Confirm validation commands, integer exit codes, and any skipped or failed checks are explicit.
- Confirm the proposed choice is supported by the packet; do not infer missing evidence.

## Options and ELI5 explanation

- **Approve** — the evidence is sufficient, so the state machine may perform the gated transition.
- **Reject** — the evidence is insufficient or incorrect; fix the stated problem before trying again.
- **Defer** — no decision yet; gather the missing information and keep the current state unchanged.

ELI5: this packet is a stop sign. A human chooses an option and signs
`manifests/approvals.csv`; software records that choice but never chooses or advances by itself.

## Decision record

<!-- DECISION_RECORD_START -->
Pending human decision. Add one signed row to `manifests/approvals.csv` with
`object_id={{DECISION_REF}}`, then run `gate_packet.py record`.
<!-- DECISION_RECORD_END -->
