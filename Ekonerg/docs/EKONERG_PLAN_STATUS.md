# Ekonerg Audit Framework — Plan Status

Snapshot date: 2026-10-03. Source plan: [`EKONERG_AUDIT_TDD_PLAN.md`](EKONERG_AUDIT_TDD_PLAN.md)
(v1.1). Implementer: Codex. Reviewer: Claude. Status reflects coordination records in
`Ekonerg/coordination/archive/` as of this snapshot; it is not a substitute for reading
the plan or the archived review records directly.

## Sprint update — 2026-10-05

MIN-2.2 remains open, but one blocker is reduced. The requirement validator now
passes: 18 criteria are covered by 55 deterministic rows seeded from active RULE
crumbs. Conservative quote matching added 25 safe links across the affected runs;
two active quotes still differ from the extracted source text and remain open.
Twelve more unmatched quotes belong to inactive generations. The aggregate gate
still fails on traceability and the missing Claude-owned `sieving-tuning` skill.
No scoring, findings, or audit conclusion were produced.

Evidence: `docs/reviews/MIN_2_2_TRACEABILITY_REPAIR_20261005.md`.

## Milestone M1 — Clean framework

| Epic | Task | Status |
|---|---|---|
| EK-0 — Agree on the transfer and review its scope | EK-0.1 — Publish the plan and request Claude's review | ✅ Approved (v1.1, no blocking findings) |
| EK-0 | EK-0.2 — Freeze the source and list every transfer item | ✅ Approved (transfer manifest, 1,963 rows) |
| EK-1 — Create local tools and a safe project boundary | EK-1.1 — Build a safe copy process | ✅ Closed (tool + live transfer both approved) |
| EK-1 | EK-1.2 — Make all runtime and support paths local | 🟡 In progress — support-tool foundation approved (9 of 225 adapt entries); dispatcher/registry closeout, runtime/sieving path adaptation, and remaining `DEPENDENCY_REVIEW.md` items still pending |
| EK-1 | EK-1.3 — Verify the shared environment | ⬜ Not started |
| EK-2 — Create fresh state and prove no old audit data remains | EK-2.1 — Create the Ekonerg skeleton and ledgers | ⬜ Not started |
| EK-2 | EK-2.2 — Build the database from schema | ⬜ Not started |
| EK-2 | EK-2.3 — Add the clean-state validator | ⬜ Not started |
| EK-3 — Adapt framework contracts, tests, and agent workflows | EK-3.1 — Separate reusable rules from run records | ⬜ Not started |
| EK-3 | EK-3.2 — Rebuild a fully synthetic test set | ⬜ Not started |
| EK-3 | EK-3.3 — Set up agent guidance and local coordination | ⬜ Not started |
| EK-4 — Prove the full workflow with invented data | EK-4.1 — Test intake, extraction, and evidence links | ⬜ Not started |
| EK-4 | EK-4.2 — Test scoring, reports, and offline evidence tools | ⬜ Not started |
| EK-4 | EK-4.3 — Test gates, interruption, and closeout | ⬜ Not started |
| EK-4 | EK-4.4 — Release the clean framework | ⬜ Not started (blocked on EK-1 through EK-4.3; owner acceptance required) |

## Milestone M2 — First Ekonerg audit

*In progress: the approved 31-file intake is registered, extracted, and
chunked. All eight QMS batches are processed. Regulatory batches R-01 through
R-07 are processed as separate Part 21, Appendix B, and NQA-1 streams. Active
and candidate runs remain subject to review; no audit conclusion has been
made.*

| Epic | Task | Status |
|---|---|---|
| EK-5 — Define and approve the real input set | EK-5.1 — Prepare the owner's source and scope checklist | ⬜ Not started |
| EK-5 | EK-5.2 — Approve the intake order and first batch | ⬜ Not started |
| EK-6 — Ingest fresh regulatory and QMS evidence | EK-6.1 — Register and process regulatory sources | 🟡 Registered, extracted, chunked; controlled RULE test passed; full sieving pending |
| EK-6 | EK-6.2 — Process Ekonerg QMS documents in bounded batches | 🟡 Registered, extracted, chunked; controlled objective-evidence test passed; full batches pending |
| EK-6 | EK-6.3 — Review evidence quality and approve G2 | ✅ G2 approved; 18 applicability rows applied for RUN-20261003-32 |
| EK-7 — Evaluate Ekonerg and approve findings | EK-7.1 — Record scoring approval and draft evaluations | ⬜ Not started |
| EK-7 | EK-7.2 — Draft findings and follow-up actions | ⬜ Not started |
| EK-8 — Generate, test, and release Croatian outputs | EK-8.1 — Build the report and evidence package | ⬜ Not started |
| EK-8 | EK-8.2 — Test the dashboard and complete owner UAT | ⬜ Not started |
| EK-8 | EK-8.3 — Release outputs under G5 and G6 | ⬜ Not started |
| EK-9 — Close the audit and hand over follow-up work | EK-9.1 — Reconcile records and prepare G7 | ⬜ Not started |
| EK-9 | EK-9.2 — Publish the final handoff and archive resolved work | ⬜ Not started |

## Legend

- ✅ Approved / closed — Claude has independently reviewed and approved with no blocking findings.
- 🟡 In progress — partially reviewed and approved; remaining sub-scope still pending.
- ⬜ Not started — no implementation or review activity recorded yet.

## Notes

- Current M2 processing update: R-01 through R-07 have reports and review
  requests. R-01 Part 21, R-02 Appendix B, and R-04 Part I are requirement
  streams. R-03, R-05, R-06, and R-07 are explicitly interpretive or guidance
  streams. The eight bounded QMS batches are also processed. Review and
  generation decisions remain open.
- EK-6.3 G2 is approved under `G2-RUN-20261003-32`. Twelve criteria are
  applicable and six remain conditional in scope; none is a final N/A. The
  18-row applicability matrix is written to the database. Formal evaluations
  and scoring now wait for G3 model approval and human judgments.
- EK-1.2 is the current open task: the local support-tool foundation (`agent_coord.py`,
  `run_validation.py`, `make_handoff.py`, `check_guidance_drift.py`,
  `check_skill_structure.py`, and their tests) is reviewed and approved, but the task as a
  whole stays open until the audit dispatcher/registry closeout, runtime/sieving path
  adaptation, and the remaining `DEPENDENCY_REVIEW.md` items are submitted and reviewed.
- Real Ekonerg intake is now present locally: 31 registered documents and 411
  validated chunks. Source copies and derived text remain local and are not
  committed; the hash register is committed.
- The local prompt registry now has owner-authorized active RULE and DOCUMENT
  prompts (`appb_rule_v1` and `appb_document_v1`). RULE and objective DOCUMENT
  golden calibrations are owner-approved. Claude review remains pending; the
  controlled test is not production evidence and creates no audit conclusion.
- The sieving harness now has every required local stage, including
  `sieve_generation.py`; readiness now passes with the intentional pending-
  golden note. The golden calibration set is still pending human approval.
- M1 cannot be accepted until EK-1 through EK-4 close and the owner explicitly accepts the
  M1 evidence packet (Task EK-4.4).

### Latest owner decisions — 2026-10-05

- The owner approved `RUN-20261003-24` as the corrected Part 21 generation.
  The approval is recorded as `R01-PART21-GEN2-PROMOTE-20261005-OWNER`.
- Fuzzy AHP is deferred. It is not part of the current audit scoring path.
- The Part 21 golden fixture is owner-approved and `RUN-20261003-24` is
  promoted. The aggregate remains blocked by historical traceability records.
