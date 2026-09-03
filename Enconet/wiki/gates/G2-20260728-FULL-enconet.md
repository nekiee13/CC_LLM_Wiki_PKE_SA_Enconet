---
id: G2-20260728-FULL
type: gate-decision
status: approved
content_origin: mixed
source: project-state.yml; manifests/approvals.csv
gate: G2
decision: approved
decision_date: '2026-07-28'
reviewer: project-owner
supplier: enconet
scope_id: FULL-20260728
---

# G2 decision packet — enconet

## Summary

Review the complete Enconet DOCUMENT evidence set: 26 active documents, 234 active crumbs, and 337/337 source quotations linked across all 18 Appendix B criteria. The evidence matrix has DOCUMENT coverage for 18/18 criteria. RUN-20260723-01 remains the active generation for DOC-0021; corrected RUN-20260723-02 remains an inactive candidate and must receive an explicit reject or approved-promotion disposition before this G2 transition. G2 approval also requires selection of the controlled deliverable language.

## Evidence pointers

- wiki/evidence/matrix.md
- wiki/evidence/matrix.json
- manifests/ingest_runs.csv
- sieving/runs/RUN-20260723-01/metrics.json
- sieving/runs/RUN-20260728-01/metrics.json
- sieving/runs/RUN-20260728-02/metrics.json
- sieving/runs/RUN-20260728-03/metrics.json
- sieving/runs/RUN-20260728-04/metrics.json
- sieving/runs/RUN-20260728-05/metrics.json
- sieving/runs/RUN-20260728-06/metrics.json
- sieving/runs/RUN-20260728-07/metrics.json
- sieving/runs/RUN-20260728-08/metrics.json
- sieving/runs/RUN-20260728-09/metrics.json
- sieving/runs/RUN-20260728-10/metrics.json
- sieving/runs/RUN-20260728-11/metrics.json
- sieving/runs/RUN-20260728-12/metrics.json
- sieving/runs/RUN-20260728-13/metrics.json
- sieving/runs/RUN-20260728-14/metrics.json
- sieving/runs/RUN-20260728-15/metrics.json
- sieving/runs/RUN-20260728-16/metrics.json
- sieving/runs/RUN-20260728-17/metrics.json
- sieving/runs/RUN-20260728-18/metrics.json
- sieving/runs/RUN-20260728-19/metrics.json
- sieving/runs/RUN-20260728-20/metrics.json
- sieving/runs/RUN-20260728-21/metrics.json
- sieving/runs/RUN-20260728-22/metrics.json
- sieving/runs/RUN-20260728-23/metrics.json
- sieving/runs/RUN-20260728-24/metrics.json
- sieving/runs/RUN-20260728-25/metrics.json
- sieving/runs/RUN-20260723-02/metrics.json (inactive candidate; disposition required)
- sieving/runs/RUN-20260723-02/diff-RUN-20260723-01-to-RUN-20260723-02.json
- sieving/runs/RUN-20260723-02/golden-score.json

## Validation results

- PASS: python scripts/build_matrix.py --json wiki/evidence/matrix.json --markdown wiki/evidence/matrix.md (exit 0)
- PASS: python scripts/run_all_validations.py --no-record (exit 0)
- PASS: validate_traceability, 337/337 active DOCUMENT quotes linked
- PASS: evidence matrix contains 18/18 RULE and 18/18 DOCUMENT criterion coverage

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
Decision: **approved**

Date: 2026-07-28

Reviewer: project-owner

Approval reference: `G2-20260728-FULL`
<!-- DECISION_RECORD_END -->
