# EK-6.3 — Evidence-quality and G2 applicability packet

## Purpose

This packet prepares the next human review gate. It does not approve
applicability, promote sieve generations, score Ekonerg, or create findings.

The audit fence is Ekonerg's QA system. Other companies are not separate audit
targets. Supplier documents are used only to check Ekonerg's supplier controls.

## Evidence set checked

- 31 registered source documents.
- 411 validated document chunks.
- Eight QMS batches processed.
- Regulatory streams R-01 through R-07 processed.
- Diagnostic matrix: `out/2026-10-03/EK-6.3-G2/evidence_matrix.md`.
- Draft applicability screen: `out/2026-10-03/EK-6.3-G2/applicability_draft.json`.

The matrix currently shows all 18 criteria as `unruled`, because no G2
approval has been written to the database. It shows evidence counts only.

## Evidence coverage

| Criterion group | Current evidence picture |
|---|---|
| Organization, QA program, design, procurement | Direct QMS and NQA-1 evidence exists. |
| Procedures and document control | Direct Ekonerg procedures exist. |
| Supplier controls | Purchasing, supplier evaluation, and supplier design-work controls exist. |
| Inspection, corrective action, records, audits | Direct QMS evidence exists. |
| Physical-item and special-process controls | Evidence is conditional or not yet specific to Ekonerg's service scope. |

## Applicability screen

The draft recommends 12 criteria as likely applicable and six as conditional:

- Likely applicable: I, II, III, IV, V, VI, VII, X, XV, XVI, XVII, XVIII.
- Conditional: VIII, IX, XI, XII, XIII, XIV.
- Final `NOT_APPLICABLE` decisions: none yet.

The conditional group covers physical-item identification, special processes,
testing, measuring equipment, handling/storage/shipping, and operating status.
The current evidence does not prove that these controls are never needed. A
contract or project record may invoke them.

## Explicit exceptions

1. Appendix B generation 2 has one source-spelling mismatch (`alfunctions`).
2. Part III generation 2 has one extraction-marker mismatch (`� Part III �`).
3. These exceptions remain visible in their stream reports. They are not
   silently corrected and do not support a positive audit conclusion.

## Acceptance-gate status

- Written basis for each draft ruling: **prepared**.
- Evidence exceptions with dispositions: **prepared**.
- Metrics and source-link checks: **available**.
- Previous generations recoverable: **yes**.
- Owner G2 approval: **pending**.
- Database applicability rulings: **not written**.

## Required next action

Owner and Claude must review the draft. The owner must record G2 approval (or
requested changes). Only after that approval may `rule_applicability.py` write
the 18 applicability rulings and evaluation begin.
