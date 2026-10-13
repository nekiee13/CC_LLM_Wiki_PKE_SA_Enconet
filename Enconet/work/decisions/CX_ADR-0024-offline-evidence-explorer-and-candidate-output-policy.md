# ADR-0024 — Offline Evidence Explorer and candidate-output policy

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-09-03 |
| Decided by | Human (project owner) |
| Scope | Evidence-access architecture and controlled report/dashboard outputs |
| Register | Owner approval of `EVIDENCE-ACCESS-TDD` and instruction to proceed with EA0.2 |
| Authored by | Codex (`CX_` prefix) |

## Context

The approved Appendix B report contains evidence labels but cannot open their supporting database
records. The Owner considered a live Streamlit interface, then approved the reviewed
`EVIDENCE-ACCESS-TDD` work queue and directed Codex to proceed with EA0.2. The existing dashboard
is already a self-contained offline browser artifact. ADR-0007 prohibits restoring the retired
standalone sieving GUI without a superseding owner decision, while ADR-0008 fixes published output
names and ADR-0011 keeps the Obsidian projection at criterion granularity.

The report and dashboard currently in `outputs/` have passed their human gates. Development must
not silently replace those approved bytes.

## Decision

1. The first evidence-access delivery is an **offline static Evidence Explorer**, implemented by
   enhancing the generated self-contained dashboard and connecting the generated report to it. It
   is not a restoration of the retired sieving GUI.
2. Browser-visible evidence is a deterministic, read-only projection from the approved evaluation
   package and SQLite data. The browser artifact has no database write path, upload path, login,
   network dependency, or mutation endpoint.
3. All ordinary development and production-candidate writes go beneath
   `outputs/candidates/evidence_access/<run_id>/`. Candidate generation must not write to a
   published path, including a wiki dashboard copy.
4. After approval and controlled promotion, the report and dashboard retain the canonical
   ADR-0008 names. Links must therefore work from both the candidate directory and final published
   directory without renaming the canonical deliverables.
5. Promotion to a protected report path requires the applicable G5 owner approval. Promotion to a
   protected dashboard, dashboard-data, or wiki-dashboard path requires the applicable G6 owner
   approval. Both also require completed independent review, passing validations, and an atomic
   promotion operation. EA6.4 will bind these requirements to the dispatcher and immutable
   approval records; a caller-provided string alone is not final gate evidence.
6. The current approved artifact hashes below are the pre-development recovery baseline. They must
   remain unchanged through candidate development. A later approved promotion records new hashes
   without rewriting this ADR; the old bytes remain recoverable from their commit/hash.
7. A future Streamlit, local HTTP, or other live evidence service remains outside this decision.
   Starting that work requires a new owner ADR that explicitly supersedes ADR-0007. This ADR does
   not supersede ADR-0007.
8. Browser-test dependencies are not added by this decision. Their selection and installation
   remain the separate EA5.1 owner-approval boundary.

<!-- evidence-access-policy
policy_version: "1.0"
delivery_mode: offline_static
candidate_root: outputs/candidates/evidence_access/<run_id>/
preserve_canonical_names_after_promotion: true
read_only_evidence: true
future_live_service_requires_superseding_adr: ADR-0007
browser_test_dependencies: deferred_to_EA5.1_owner_approval
approved_artifacts:
  outputs/enconet_appendix_b_evaluation_report.md: 0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175
  outputs/enconet_appendix_b_evaluation_report_hr.md: 0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175
  outputs/enconet_appendix_b_dashboard.html: 15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07
  outputs/enconet_appendix_b_dashboard_hr.html: 15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07
  outputs/enconet_appendix_b_dashboard_data.json: 528cbe51dc8711f1e93d55f431518eba68425d470bd2df9d32a624ec1abe5b71
  outputs/enconet_dashboard_data_hr.json: 528cbe51dc8711f1e93d55f431518eba68425d470bd2df9d32a624ec1abe5b71
  wiki/dashboards/enconet_appendix_b_dashboard.html: 15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07
-->

## Consequences

- Obsidian remains unchanged; the report opens exact evidence in the portable offline browser
  package once later tasks implement the links and bundle.
- Candidate and published artifacts have separate locations and lifecycle states.
- Current approved outputs are protected by both recorded hashes and executable policy tests.
- EA7 may evaluate a live service only after demonstrated need and a separate owner decision.
- Browser automation dependencies remain deferred to the separately controlled EA5.1 task.
- Independent Claude review of this implementation remains deferred, not waived, under ADR-0023.
