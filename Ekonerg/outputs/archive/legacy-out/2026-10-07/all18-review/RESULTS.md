# Ekonerg: all-18 documentation audit results

Result: **77.8% — Substantially Matched (1400 / 1800 points)**.
Run: RUN-20261003-32. Revision: ALL18-REVIEW-20261007-01.
Owner decision: ALL18-REASSESSMENT-20261007-OWNER.

[Open the light dashboard](EKONERG_DASHBOARD.html).
[Evidence matrix](evidence-matrix.md).
[Full assessment](../../../docs/reviews/ALL18_ASSESSMENT_20261007.json).
[Rubric and scope](../../../docs/reviews/ALL18_RUBRIC_20261007.md).

## Read this first

This is the official documentation pre-flight result, not proof of field execution.
Three criteria are fully matched; fourteen are substantially matched; one is partially
matched. All 18 have a rating. No score is withheld and no human rating-entry form is added.

Part 21 remains applicable and its reporting path remains unresolved. By the owner's
explicit decision, it is outside XVI and the overall Appendix B score. Full XVI does
not imply full Part 21 compliance. The real audit should verify the reporting route
beyond customer notification in PQ10.2-1 section 3.11.

The same five-level weights and 18-criterion denominator are used. No new category,
weight, applicability rule, source edition or framework slice is introduced.
Read for the purpose of a requirement. Credit real controls spread across documents;
do not count crumbs as points or deduct points just because completed work samples
are not in the documentation pack.

## Rating summary and history

The baseline was 68.1% (1225/1800). Seven ratings improve on this recheck.
The other eleven ratings are unchanged, but all 18 explanations now describe current
controls and limits. History is preserved in the immutable revision journal.

| Criterion | Earlier points | Current rating | Current points |
|---|---:|---|---:|
| I — Organization | 75 | substantially | 75 |
| II — Quality Assurance Program | 75 | substantially | 75 |
| III — Design Control | 75 | substantially | 75 |
| IV — Procurement Document Control | 75 | fully | 100 |
| V — Instructions, Procedures, and Drawings | 75 | fully | 100 |
| VI — Document Control | 75 | substantially | 75 |
| VII — Control of Purchased Material, Equipment, and Services | 75 | substantially | 75 |
| VIII — Identification and Control of Materials, Parts, and Components | 50 | substantially | 75 |
| IX — Control of Special Processes | 50 | partially | 50 |
| X — Inspection | 75 | substantially | 75 |
| XI — Test Control | 50 | substantially | 75 |
| XII — Control of Measuring and Test Equipment | 50 | substantially | 75 |
| XIII — Handling, Storage and Shipping | 75 | substantially | 75 |
| XIV — Inspection, Test, and Operating Status | 50 | substantially | 75 |
| XV — Nonconforming Materials, Parts, or Components | 50 | substantially | 75 |
| XVI — Corrective Action | 100 | fully | 100 |
| XVII — Quality Assurance Records | 75 | substantially | 75 |
| XVIII — Audits | 75 | substantially | 75 |

## Current findings by criterion

These are documentation judgments. Each evidence anchor below is an existing,
active, same-criterion vendor crumb already linked to the score. The named procedure
paragraphs add source detail; they are not new fabricated crumbs. The dashboard's
expanded cards retain the quote and source chapter links.

### I. Organization

Substantially matched, 4/5. The organization has defined authority and reporting routes; the safety-over-cost/schedule safeguard needs clarification under Appendix B I and NQA-1 Requirement 1 §201(d).

Manual 5.3 and Prilog 2 §§1.2-1.3 assign duties, preserve responsibility after delegation, give QA personnel organizational freedom, and provide direct management access. PQ10.2-1 §2.9 gives management a stop-work duty on significant nonconformances.

Limit and real-audit focus: The written organization rules do not clearly protect QA decisions when cost or schedule conflicts with nuclear safety. Management access and a stop-work route support independence, but do not fully settle that conflict.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_I-0017`, `CRUMB-DOC-0032-APP_B_I-0018`, `CRUMB-DOC-0032-APP_B_I-0022`.

### II. Quality Assurance Program

Substantially matched, 4/5. The written program meets the main planning, resource, training and review duties. Nuclear inspection/test qualification maintenance needs clearer rules. An absent completed project plan is not treated as a missing generic planning process.

Manual 7.1-7.3, 8.1 and 9.3 define resources, competence, work conditions, project quality plans and annual management review. Dodatak 1 §2 places NS/AQ work at level I. PQ7.1-1 §§2-3 requires planned training and competence records; PQ9.2 §3.8 defines nuclear auditor qualifications.

Limit and real-audit focus: The program has a meaningful graded planning process. Its written nuclear inspection/test personnel qualification rules do not clearly set the periodic re-evaluation and inactivity checks in NQA-1 Requirement 2 §203. General training and certificate renewal do not fully define those checks.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_II-0017`, `CRUMB-DOC-0032-APP_B_II-0027`, `CRUMB-DOC-0032-APP_B_II-0028`, `CRUMB-DOC-0032-APP_B_II-0032`, `CRUMB-DOC-0032-APP_B_II-0038`.

### III. Design Control

Substantially matched, 4/5. The main design-control process is substantive. The software verification/reference chain needs clarification for NQA-1 Requirement 3 §§401 and 500. No blanket Part II compliance is assumed.

Manual 8.3 and PQ8.3-1 §§3.1-3.5 control design inputs, interfaces, independent checks, release, records and changes. Software verification is triggered by configuration and use changes in Dodatak 1's flow notes.

Limit and real-audit focus: The nuclear addendum and Prilog 5 use inconsistent RSP and ROS identifiers. The actual design-software verification method is not supplied, so the written chain to a proven calculation tool or independently verified result is incomplete.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_III-0010`, `CRUMB-DOC-0032-APP_B_III-0013`, `CRUMB-DOC-0032-APP_B_III-0015`, `CRUMB-DOC-0032-APP_B_III-0019`, `CRUMB-DOC-0032-APP_B_III-0027`.

### IV. Procurement Document Control

Fully matched for documentation, 5/5. PQ8.4-2 §3.2 and Manual 8.4 cover the procurement-document intent of Appendix B IV and NQA-1 Requirement 4 §§200-400. This is not a finding that every issued order has been checked.

Manual 8.4 and PQ8.4-2 §3.2 require technical and QA requirements, acceptance methods, access rights, record controls, nonconformance reporting, lower-tier flow-down and document delivery times. Named staff prepare, review and approve the purchase documents; Manual 8.4.4 applies contract-document change controls.

Limit and real-audit focus: No specific missing written procurement-document duty is identified in the reviewed scope. Real-audit sampling must confirm that nuclear purchase documents use the required clauses, including lower-tier flow-down and record/submittal terms.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_IV-0003`, `CRUMB-DOC-0032-APP_B_IV-0004`, `CRUMB-DOC-0032-APP_B_IV-0005`, `CRUMB-DOC-0024-APP_B_IV-0001`.

### V. Instructions, Procedures, and Drawings

Fully matched for documentation, 5/5. The written instruction framework covers Appendix B V and NQA-1 Requirement 5 §100, including acceptance criteria and detail suited to the task. This does not approve every listed technical method.

Manual 7.5.1 and 8.5.1 require detailed work instructions with prerequisites, people, equipment, responsibilities, acceptance criteria and reporting. PQ7.5-4 §3.1 specifies those contents and §3.3 requires competent preparation, independent review and approval.

Limit and real-audit focus: No specific missing general instruction-content duty is identified. Task-specific RVT/RPT/RMT/RUT and RSP/ROS methods still need real-audit checks in their own technical areas; a title alone is not proof that a special method is qualified.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_V-0005`, `CRUMB-DOC-0032-APP_B_V-0006`, `CRUMB-DOC-0032-APP_B_V-0007`, `CRUMB-DOC-0032-APP_B_V-0008`.

### VI. Document Control

Substantially matched, 4/5. Document-control duties are written and assigned. Conflicting controlled references prevent an unqualified full match under NQA-1 Requirement 6 §§100-300.

Manual 7.5.3 and PQ7.5-5 §§3-4 assign preparation, review, approval, changes and controlled distribution. They require current copies at use, revision status, controlled external documents and withdrawal or marking of obsolete copies.

Limit and real-audit focus: The supplied manual has conflicting references: Dodatak 1 §11 cites ROS-02 for software control while Prilog 5 lists ROS-03; §17 cites RSP-03 for backup while the register lists ROS-04. These are live navigation ambiguities, not merely absent work samples.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_VI-0008`, `CRUMB-DOC-0032-APP_B_VI-0010`, `CRUMB-DOC-0032-APP_B_VI-0011`, `CRUMB-DOC-0032-APP_B_VI-0012`, `CRUMB-DOC-0032-APP_B_VI-0013`.

### VII. Control of Purchased Material, Equipment, and Services

Substantially matched, 4/5. The service procurement and supplier-control process is substantive. The safety-related hardware acceptance timing and detailed commercial-product route need confirmation under Appendix B VII and NQA-1 Requirement 7 §501. No blanket Part II obligation is added.

Manual 8.4, PQ8.4-2 §§3.1-3.4 and PQ8.4-3 §§3.2-3.9 define supplier selection, nuclear qualification, graded surveillance, acceptance and performance review. Supplier evidence is checked against requirements and retained; Dodatak 1 §7 defines safety significance, critical characteristics and verification selection for commercial products.

Limit and real-audit focus: Commercial-product dedication is described at a high level, without the detailed acceptance route. Manual 8.4.3 describes conformity evidence before/after installation, which does not clearly secure required evidence before installation or use for safety-related hardware.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_VII-0005`, `CRUMB-DOC-0032-APP_B_VII-0006`, `CRUMB-DOC-0032-APP_B_VII-0007`, `CRUMB-DOC-0032-APP_B_VII-0008`, `CRUMB-DOC-0032-APP_B_VII-0009`, `CRUMB-DOC-0032-APP_B_VII-0011`.

### VIII. Identification and Control of Materials, Parts, and Components

Substantially matched, 4/5. The stated engineering-service scope has a meaningful identity and traceability process. The remaining gap concerns the generic hardware safeguards, not the absence of a completed job-specific marking record.

Manual 8.5.3 maintains project and study identity through work-order and document identifiers. Sections 8.5.4-8.5.5 control customer property and preservation. Dodatak 1 §8 requires a nuclear document defining traceability methods, special requirements and marking authority.

Limit and real-audit focus: The process is clear for engineering deliverables. The generic nuclear hardware rules do not clearly cover identity transfer on subdivision, replacement of damaged storage marks, or limited-life item expiry under NQA-1 Requirement 8 §§202 and 302-303.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_VIII-0002`, `CRUMB-DOC-0032-APP_B_VIII-0003`, `CRUMB-DOC-0032-APP_B_VIII-0004`, `CRUMB-DOC-0032-APP_B_VIII-0006`.

### IX. Control of Special Processes

Partially matched, 3/5. The policy and procedural framework are present, but method-specific qualification controls remain weakly evidenced against NQA-1 Requirement 9 §§201-203 and 400. Coatings, concrete, epoxy and non-metal testing are scope questions, not assumed Ekonerg activities.

Manual 3 defines qualified procedures and special processes; 8.5.2 commits to validation and supervision of such work. PQ7.5-4 §3.1 requires personnel/equipment qualifications and technical criteria in work procedures. Prilog 5 lists RVT, RPT, RMT and RUT methods.

Limit and real-audit focus: The generic template and procedure titles do not establish the actual special-process qualification method. The supplied set does not show how a specific NDT method is demonstrated fit for purpose, how its parameters/acceptance limits are approved, and how current process, equipment and personnel qualifications are maintained.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_IX-0001`, `CRUMB-DOC-0032-APP_B_IX-0002`, `CRUMB-DOC-0032-APP_B_IX-0003`.

### X. Inspection

Substantially matched, 4/5. Inspection planning, independence, records and reinspection are defined. The written hold-point waiver safeguard needs clarification; lack of a completed inspection report alone is not the reason for the rating.

Manual 8.6 and 9.1.4 require documented checks, acceptance, witness/hold points and indirect monitoring when inspection is unsuitable. PQ8.6 §§3.2-3.7 assigns competent independent checking and record duties; repaired work is verified again.

Limit and real-audit focus: The hold-point planning rule does not clearly require recorded consent before a hold point is waived, as NQA-1 Requirement 10 §300 requires. The real audit should also confirm exclusion of both the performer and direct supervisor from acceptance inspections.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_X-0004`, `CRUMB-DOC-0032-APP_B_X-0006`, `CRUMB-DOC-0032-APP_B_X-0007`, `CRUMB-DOC-0032-APP_B_X-0010`, `CRUMB-DOC-0032-APP_B_X-0011`, `CRUMB-DOC-0032-APP_B_X-0012`.

### XI. Test Control

Substantially matched, 4/5. The written customer-testing process has the core test-control duties. Software-method identification and test-record detail need clarification. The manual's no-own-product-testing statement is preserved and does not cancel customer-testing duties.

Manual 9.1.4 requires customer testing to have a program, written requirements, acceptance criteria, suitable conditions, records and result evaluation. Manual 7.5.1, PQ7.5-4 §3.1 and 7.1.5 provide prerequisites, qualified staff/equipment and calibration controls. Software verification is tied to defined change/use triggers.

Limit and real-audit focus: The software-control procedure reference conflicts with Prilog 5, and the full verification method is not supplied. The nuclear test-record content is not clearly specified to the detail of NQA-1 Requirement 11 §601, including deviations and the person evaluating results.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XI-0003`, `CRUMB-DOC-0032-APP_B_XI-0004`, `CRUMB-DOC-0032-APP_B_XI-0005`, `CRUMB-DOC-0032-APP_B_XI-0012`.

### XII. Control of Measuring and Test Equipment

Substantially matched, 4/5. Calibration, ownership, status and exclusion duties are substantive. Use traceability and the look-back check need clearer instructions. The qualified commercial-device exception is consistent in intent with Requirement 12 §304 and is not treated as a failure.

Manual 7.1.5 and PQ7.1-2 §§2-3 require equipment identification, periodic checks/calibration, assigned owners, status evidence and records. Overdue equipment is marked and removed from use; repeatedly faulty equipment is repaired or replaced. Commercial devices may be exempt only when they give the required precision.

Limit and real-audit focus: The supplied procedure does not clearly require tracing equipment to its use and evaluating prior results back to the last acceptable calibration when equipment is lost, damaged or out of calibration. These are written-control gaps under NQA-1 Requirement 12 §§303.1-303.2.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XII-0002`, `CRUMB-DOC-0032-APP_B_XII-0004`.

### XIII. Handling, Storage and Shipping

Substantially matched, 4/5. Written preservation and special-condition controls cover the main duty. The special handling-tool check needs clarification only where that equipment is used; no unsupported claim about Ekonerg operating a warehouse or crane is made.

Manual 8.5.5 requires controlled handling, storage, cleaning, packaging, preservation and shipment to prevent damage, loss and deterioration. Sensitive items are marked and their conditions checked; project plans define special protection and handler competence.

Limit and real-audit focus: The general preservation process is substantive. For special handling tools, the supplied rule does not clearly prescribe inspection/testing before use or at defined intervals, as NQA-1 Requirement 13 §400 requires when such tools are needed.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XIII-0002`, `CRUMB-DOC-0032-APP_B_XIII-0003`, `CRUMB-DOC-0032-APP_B_XIII-0004`, `CRUMB-DOC-0032-APP_B_XIII-0005`.

### XIV. Inspection, Test, and Operating Status

Substantially matched, 4/5. Written service acceptance and release controls are present, along with nuclear status planning. The remaining concern is the generic status-removal/operating safeguard, not a demand for completed plant tag records from an engineering-service supplier.

Manual 8.6 and 9.1.4 require acceptance evidence and an authorized release before delivery; nonconforming release requires special approval. Calibration status is marked and overdue equipment excluded. Dodatak 1 §14 requires a nuclear status document with a method, traceability and marking authority.

Limit and real-audit focus: The service-release process is clear. The generic nuclear status rule does not clearly prescribe who may remove status marks and how an unsafe operating status or bypass is prevented under NQA-1 Requirement 14 §100.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XIV-0001`, `CRUMB-DOC-0032-APP_B_XIV-0002`, `CRUMB-DOC-0032-APP_B_XIV-0003`, `CRUMB-DOC-0032-APP_B_XIV-0004`.

### XV. Nonconforming Materials, Parts, or Components

Substantially matched, 4/5. The written prevention, disposition and re-verification process is substantial. Technical justification and as-built treatment for repair/use-as-is need clarification. This rating covers Appendix B XV, not a finding of full Part 21 compliance.

Manual 8.7 and PQ10.2-1 §§2-3 define immediate reporting, marking/segregation or other safeguards, evaluation, approved disposition, prevention of use and verified completion. PQ8.3-1 §3.5 applies original design controls to changes caused by a nonconformance.

Limit and real-audit focus: Use-as-is or repair decisions do not clearly require a documented technical justification and matching as-built records as specified by NQA-1 Requirement 15 §404. Customer consent and QA approval are meaningful, but do not by themselves supply that technical basis. Part 21 reporting remains a separate unresolved follow-up.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XV-0005`, `CRUMB-DOC-0032-APP_B_XV-0006`, `CRUMB-DOC-0032-APP_B_XV-0007`, `CRUMB-DOC-0032-APP_B_XV-0008`.

### XVI. Corrective Action

Fully matched for documentation, 5/5. The written controls cover Appendix B XVI and NQA-1 Requirement 16 §100. Part 21 reporting is outside this criterion's score and remains unresolved; full here does not mean full Part 21 compliance or verified execution.

Manual 8.7, 9.2, 10.2 and Prilog 2 require prompt action, significant/repeated cause review, recurrence prevention, records, management reports and verified completion/effectiveness. PQ10.2-2 §§2.2, 2.5, 2.7 and 3.1-3.8 assign approval, follow-up, reopening and reporting duties.

Limit and real-audit focus: No missing Appendix B XVI written corrective-action duty is identified. The real audit must sample timely and effective completion. Part 21 remains applicable: the reporting route beyond the customer notification described in PQ10.2-1 §3.11 remains unresolved, and is not included in XVI's Appendix B score.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XVI-0004`, `CRUMB-DOC-0032-APP_B_XVI-0007`, `CRUMB-DOC-0032-APP_B_XVI-0008`, `CRUMB-DOC-0032-APP_B_XVI-0010`.

### XVII. Quality Assurance Records

Substantially matched, 4/5. Identification, retention, responsibility and physical/electronic preservation are substantive. The backup reference and long-term access/retrieval safeguards need clearer controlled instructions.

Manual 7.5.4, PQ7.5-7 §§3.1-3.8 and Prilog B define record identity, review, responsibility, retention and lifetime nuclear records. Electronic media are checked/copied within five years; Dodatak 1 §17 describes a central archive, a server and a remote parallel server.

Limit and real-audit focus: The backup method is cited as RSP-03 while Prilog 5 lists ROS-04. The supplied storage rules do not fully define protection/access and continued retrieval through hardware/software changes under NQA-1 Requirement 17 §§601 and 800. Five-year copying and remote storage are credited, not ignored.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XVII-0007`, `CRUMB-DOC-0032-APP_B_XVII-0010`, `CRUMB-DOC-0032-APP_B_XVII-0012`, `CRUMB-DOC-0032-APP_B_XVII-0015`, `CRUMB-DOC-0032-APP_B_XVII-0018`.

### XVIII. Audits

Substantially matched, 4/5. The audit process and nuclear auditor qualification duties are substantive. The supplier performance-review interval needs clarification. Completed audit records are real-audit samples, not a prerequisite for crediting this written process.

Manual 9.2 and PQ9.2 §§3.2-3.8 require planned and extra audits, independent trained auditors, checklists, reports to management, responses and verified follow-up. Nuclear lead-auditor qualification includes five audits in three years with a recent nuclear audit, continuing participation and an annual-evaluation form.

Limit and real-audit focus: PQ8.4-3 §3.8 reviews supplier performance after engagements and PQ9.2 §3.2 prescribes triennial nuclear supplier audits. A required annual evaluation, or a formally reviewed ongoing alternative, between supplier audits is not clearly set out for all approved nuclear suppliers under NQA-1 Requirement 18 §202.

Score evidence anchors: `CRUMB-DOC-0032-APP_B_XVIII-0003`, `CRUMB-DOC-0032-APP_B_XVIII-0004`, `CRUMB-DOC-0032-APP_B_XVIII-0005`, `CRUMB-DOC-0032-APP_B_XVIII-0007`, `CRUMB-DOC-0032-APP_B_XVIII-0010`.

## Safety and validation

- 475 active vendor crumbs, 379 score-support links and all active generation
  identities are unchanged. Sources, chapters, quotes and applicability are unchanged.
- All 558 active vendor quote/chapter rows are exact. All 32 registered raw-source
  hashes match. The live rows match the applied plan and the published 18-card payload.
- The apply receipt records the old/new DB hashes and journal hashes. A repeat apply
  returns `already_applied`, with no second history write.
- Old reports and the 68.1% baseline are retained. The DB remains local/ignored;
  the committed assessment, preview and journal preserve the change evidence.

Commands run from the workspace root:

| Check | Exit | Result |
|---|---:|---|
| `python Ekonerg/scripts/evaluation_refresh.py --assessment docs/reviews/ALL18_ASSESSMENT_20261007.json --output out/2026-10-07/all18-review/preview.json` | 0 | Read-only preview; 77.8% |
| `python Ekonerg/scripts/evaluation_refresh.py --apply-plan out/2026-10-07/all18-review/preview.json --output out/2026-10-07/all18-review/transition` | 0 | Applied; repeated with exit 0 and already_applied |
| `python Ekonerg/scripts/validate_evaluation.py --run-id RUN-20261003-32` | 0 | 18/18 structurally valid; not independent audit approval |
| `python Ekonerg/scripts/build_matrix.py --run-id RUN-20261003-32 --json out/2026-10-07/all18-review/evidence-matrix.json --markdown out/2026-10-07/all18-review/evidence-matrix.md` | 0 | 18 criteria |
| `python Ekonerg/scripts/build_umbra_conformance_dashboard.py --matrix Ekonerg/out/2026-10-07/all18-review/evidence-matrix.json --date 2026-10-07 --output Ekonerg/out/2026-10-07/all18-review/EKONERG_DASHBOARD.html` | 0 | Ekonerg-only light dashboard |
| `python Ekonerg/scripts/run_all_validations.py --no-record` | 0 | 8 phase-active checks pass; later report/dashboard checks skipped |
| `git diff --check` | 0 | No whitespace errors |

Final regression command, exit 0: **91 passed**.

```powershell
python -m pytest Ekonerg/scripts/tests/test_evaluation_refresh.py Ekonerg/scripts/tests/test_source_revision_promote.py Ekonerg/scripts/tests/test_source_revision_intake.py Ekonerg/scripts/tests/test_build_reviewed_candidate.py Ekonerg/scripts/tests/test_full_keyword_sweep.py Ekonerg/scripts/tests/test_sieve_generation_local.py Ekonerg/scripts/tests/test_validate_traceability.py Ekonerg/scripts/tests/test_umbra_conformance_dashboard.py Ekonerg/scripts/tests/test_evaluation_scope_source.py -q -p no:cacheprovider --basetemp Ekonerg/.tmp/all18-post-regression-20261007 --tb=short
```

TDD: the new Part 21 visibility test first failed as expected. A synthetic all-18
fixture initially lacked evidence for 17 criteria; it was corrected before apply.
Focused tests then passed (24), followed by pre-apply regression (90) and the final
post-publication regression (91). The extra final test checks all 18 published
ratings, summaries, basis IDs and 379 support links against this assessment.

Limit: the phase file remains `evidence_reviewed`; the aggregate does not activate
later report, browser, dashboard or review-package gates. The explicit evaluation,
source/trace and static dashboard checks above are not a replacement for a live
browser/mobile/print trial. Those trials and Claude's independent semantic/presentation
review remain pending. Dark GUI work is paused. No field-performance claim is made.

