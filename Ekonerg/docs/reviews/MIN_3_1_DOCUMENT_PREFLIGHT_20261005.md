# MIN-3.1 Ekonerg document pre-flight assessment

**Run:** `RUN-20261003-32`  
**Scope:** Ekonerg QA documentation against 10 CFR 50 Appendix B, using
ASME NQA-1 Part 1 as the required interpretation baseline.  
**Purpose:** identify likely weak areas before the real audit.

This is the same criterion classification vocabulary used by the Enconet
workflow. It is a document assessment, not a claim that the controls operated
in practice. The real audit should test the listed gaps with objective records,
work samples, interviews, and observation.

## Result at a glance

| Classification | Count | Meaning in this pre-flight |
|---|---:|---|
| `substantially` | 13 | The supplied QMS documents describe the required control, but implementation proof is still needed. |
| `partially` | 0 | No criterion is placed here in this first document pass. |
| `minimally` | 0 | No criterion is placed here in this first document pass. |
| `unmet` | 0 | Document review alone does not support this conclusion. |
| `undetermined` | 5 | No direct Ekonerg vendor crumb was mapped for the criterion; test the scope and obtain records. |
| `na` | 0 | No final N/A decision was made. |

No consolidated score is reported. The existing scoring model treats
`undetermined` as zero, which would make an evidence gap look like a failed
control. This report is for audit planning, not final scoring.

## Criterion assessment

| Criterion | Document classification | Vendor evidence used | Main real-audit focus |
|---|---|---|---|
| APP_B_I Organization | `substantially` | `CRUMB-DOC-0011-APP_B_I-0009`, `CRUMB-DOC-0011-APP_B_I-0011`, `CRUMB-DOC-0031-APP_B_I-0001` | Confirm appointments, authority, independence, and interviews. |
| APP_B_II Quality Assurance Program | `substantially` | `CRUMB-DOC-0018-APP_B_II-0002`, `CRUMB-DOC-0031-APP_B_II-0001`, `CRUMB-DOC-0031-APP_B_II-0006` | Sample quality plans, grading, training, risk work, and management review. |
| APP_B_III Design Control | `substantially` | `CRUMB-DOC-0022-APP_B_III-0002`, `CRUMB-DOC-0022-APP_B_III-0003`, `CRUMB-DOC-0022-APP_B_III-0005` | Trace one design from input through independent verification and change control. |
| APP_B_IV Procurement Document Control | `substantially` | `CRUMB-DOC-0021-APP_B_IV-0004`, `CRUMB-DOC-0021-APP_B_IV-0006`, `CRUMB-DOC-0024-APP_B_IV-0001` | Check procurement packages, flow-down clauses, and supplier records. |
| APP_B_V Instructions, Procedures, and Drawings | `substantially` | `CRUMB-DOC-0011-APP_B_V-0007`, `CRUMB-DOC-0013-APP_B_V-0002`, `CRUMB-DOC-0018-APP_B_V-0001` | Check approved work instructions, acceptance criteria, and completed use. |
| APP_B_VI Document Control | `substantially` | `CRUMB-DOC-0011-APP_B_VI-0007`, `CRUMB-DOC-0012-APP_B_VI-0003`, `CRUMB-DOC-0031-APP_B_VI-0002` | Test revision history, distribution, current copies, and withdrawal of obsolete copies. |
| APP_B_VII Purchased Material, Equipment, and Services | `substantially` | `CRUMB-DOC-0024-APP_B_VII-0002`, `CRUMB-DOC-0024-APP_B_VII-0003`, `CRUMB-DOC-0025-APP_B_VII-0003` | Confirm supplier boundary, qualification, acceptance, and reassessment. |
| APP_B_VIII Identification and Control of Materials, Parts, and Components | `undetermined` | No direct vendor crumb mapped. | Decide whether physical or traceable items are in Ekonerg scope; obtain identification records if yes. |
| APP_B_IX Control of Special Processes | `undetermined` | No direct vendor crumb mapped. | Confirm whether Ekonerg performs or controls special processes; obtain qualifications and procedures if yes. |
| APP_B_X Inspection | `substantially` | `CRUMB-DOC-0022-APP_B_X-0001`, `CRUMB-DOC-0022-APP_B_X-0002`, `CRUMB-DOC-0026-APP_B_X-0002` | Trace independent checks, hold points, inspector competence, and completed results. |
| APP_B_XI Test Control | `undetermined` | No direct vendor crumb mapped. | Confirm whether Ekonerg performs or accepts tests; obtain procedures, prerequisites, instruments, and results if yes. |
| APP_B_XII Measuring and Test Equipment | `substantially` | `CRUMB-DOC-0010-APP_B_XII-0001`, `CRUMB-DOC-0010-APP_B_XII-0002`, `CRUMB-DOC-0010-APP_B_XII-0003` | Check equipment list, calibration certificates, status, overdue actions, and impact reviews. |
| APP_B_XIII Handling, Storage, and Shipping | `undetermined` | No direct vendor crumb mapped. | Confirm whether physical items or preservation-sensitive deliverables are handled; sample controls if yes. |
| APP_B_XIV Inspection, Test, and Operating Status | `undetermined` | No direct vendor crumb mapped. | Confirm where status identification is needed and test prevention of unintended use or release. |
| APP_B_XV Nonconforming Materials, Parts, or Components | `substantially` | `CRUMB-DOC-0029-APP_B_XV-0001`, `CRUMB-DOC-0029-APP_B_XV-0002`, `CRUMB-DOC-0020-APP_B_XV-0001` | Trace a nonconformance, disposition, segregation, reinspection, and Part 21 decision. |
| APP_B_XVI Corrective Action | `substantially` | `CRUMB-DOC-0029-APP_B_XVI-0004`, `CRUMB-DOC-0030-APP_B_XVI-0004`, `CRUMB-DOC-0030-APP_B_XVI-0006` | Trace cause, action approval, effectiveness, closure, reopening, and reporting. |
| APP_B_XVII Quality Assurance Records | `substantially` | `CRUMB-DOC-0016-APP_B_XVII-0026`, `CRUMB-DOC-0016-APP_B_XVII-0030`, `CRUMB-DOC-0027-APP_B_XVII-0001` | Test retrieval, access, retention, disposition, and record integrity. |
| APP_B_XVIII Audits | `substantially` | `CRUMB-DOC-0027-APP_B_XVIII-0001`, `CRUMB-DOC-0027-APP_B_XVIII-0002`, `CRUMB-DOC-0028-APP_B_XVIII-0001` | Sample audit plans, auditor qualification, reports, follow-up, and management review. |

## Priority route for the real audit

1. Confirm the five `undetermined` scopes first: identification, special
   processes, testing, handling, and status.
2. Trace one complete design or engineering project through APP_B_III, V, X,
   XVII, and XVIII.
3. Trace one supplier or subcontractor package through APP_B_IV and VII.
4. Trace one nonconformance and corrective action under APP_B_XV and XVI,
   including the Part 21 decision path.
5. Recheck every `substantially` result against objective implementation
   evidence before issuing any final audit rating or score.

## Provenance

- Evidence matrix: `out/2026-10-05/MIN-3.1-evidence-matrix-v4.json`
- Active vendor evidence: `db/nqa_audit.sqlite`
- Scope and applicability decision: `docs/reviews/EF_3_1_OWNER_SCOPE_DECISION.md`
- Existing workflow example: Enconet Appendix B evaluation report
