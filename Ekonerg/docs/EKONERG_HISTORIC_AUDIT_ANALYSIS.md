# Historic Ekonerg Audit Analysis and Framework Pivot

**Status:** analysis complete; no current-audit score or finding was changed

**Sources reviewed:**

- [`SA20-1.md`](audit_report_examples/SA20-1.md), audit performed 8-10 July 2020
- [`SA23-1.md`](audit_report_examples/SA23-1.md), audit performed 18-19 October 2023

## 1. What these examples teach us

The two reports are not simple pass/fail checklists. They combine five views:

1. the supplier boundary and the type of work Ekonerg performed;
2. the QA activities that were examined;
3. the project records used as objective evidence;
4. findings, recommendations, and repeated findings; and
5. the operating limits imposed on supplier approval.

The current framework has a strong criterion and crumb view. It must add these
five views so that it can produce an audit report that a human auditor can use.

These reports are historical context. They are not current Ekonerg evidence,
current applicability decisions, or proof that a present-day control works.

## 2. Side-by-side facts

| Topic | SA20-1 (2020) | SA23-1 (2023) | Design lesson |
|---|---|---|---|
| Audit purpose | Check Ekonerg for continued approved-supplier status | Same purpose | The final decision is more than a score: it can include conditions and limits. |
| Supplier work | Design and engineering services; SR and AQ work | Design, engineering, and project/subcontractor oversight | Scope must describe the work Ekonerg performs and the work it controls through others. |
| Main QMS edition | Management System Manual rev. 4 | Management System Manual rev. 5 | Every claim needs the source document and revision used. |
| External references | Appendix B, Part 21, QS-610 rev. 1, NQA-1 2008/2009 | Appendix B, Part 21, QS-610 rev. 2, NQA-1 2008/2009 | Regulatory requirements, customer requirements, and interpretation references need separate provenance. |
| Activity sections | 17 | 17 | Preserve an activity view even though the controlling taxonomy has 18 Appendix B criteria. |
| Commercial dedication | N/A, not audited | N/A, not audited | “Not audited” must not be confused with “proved compliant.” |
| Supplier findings | 8 | 5 | Fewer findings does not mean every sub-control is proven. |
| Activity result | 9 Z, 7 NZ, 1 N/A | 11 Z, 5 NZ, 1 N/A | Historic Z/NZ is a section summary, not a numeric conformance score. |
| Recommendations | 3 | 3 | Recommendations are useful improvement actions, but are not the same as findings. |
| Decision | Conditional approved supplier status with limits | Conditional approved supplier status with limits | The report needs a decision-and-conditions record separate from criterion ratings. |

## 3. The strongest evidence pattern

Both reports use a repeatable narrative pattern for each activity:

1. list the governing Ekonerg procedures and manual revisions;
2. name a real project, contract, supplier, or record sample;
3. describe what was observed in that sample;
4. compare the observation with a requirement or procedure;
5. record a status, finding, or recommendation; and
6. link the result to a follow-up action or supplier limitation when needed.

For example, SA23-1 does not only say that testing is controlled. It describes
the quality-control plan, the FAT procedure, the required test pressure, the
missed test condition, the later pump failure, and the replacement test. That
chain is the type of objective evidence the sieve must preserve.

## 4. Recurring risk themes

### 4.1 Procurement flow-down and supplier control

SA20-1 reports missing approved procurement specifications, quality requirements,
QA participation, and supplier evaluation. SA23-1 reports that service purchase
requests still lacked quality requirements, and that planned audits of SR
suppliers were not performed or clearly scoped.

**Framework consequence:** procurement crumbs must capture the whole chain:
need or design input -> technical and quality requirements -> supplier selection
or audit -> purchase document -> acceptance evidence -> supplier performance.
A single sentence saying “procurement is controlled” is not enough.

### 4.2 Design control and authorised personnel

SA20-1 identifies unverified design inputs, the use of assumptions, and people
working outside the project plan. SA23-1 identifies gaps in designer
qualification and safety classification.

**Framework consequence:** design evidence needs explicit fields for design
inputs, verification, responsible people, qualifications, safety classification,
changes, and the project plan or DMP revision.

### 4.3 Testing, inspection, and field execution

SA20-1 describes missed Hold/Witness notifications and incomplete QA/QC plans.
SA23-1 again finds an incompletely filled quality-control plan and an FAT
procedure that was not approved before testing. The pump example shows why the
test condition matters: the first test missed the required operating point and
the problem appeared after installation.

**Framework consequence:** test evidence must preserve acceptance criteria,
approval-before-use, actual test conditions, results, exceptions, and the
relationship to the item or project. A test-plan title alone is weak evidence.

### 4.4 Nonconformance, Part 21, and corrective action

SA20-1 says project PDRs were not consistently treated as Ekonerg
nonconformances, and a customer warning was not processed as a corrective action.
It also notes repeated actions from the previous audit. SA23-1 says the quality
significance test was still missing from the corrective-action procedure and the
pump problem was not fully analysed as a prevention action.

**Framework consequence:** the model needs separate links for:

- condition or defect;
- nonconformance/PDR/FDCR/NCR record;
- Part 21 screening or report decision;
- root-cause and extent-of-condition review;
- corrective and preventive action;
- management reporting; and
- effectiveness check and closure.

### 4.5 Special processes and boundary limits

SA20-1 recommends adding anti-corrosion protection, concrete work, and visual
testing to the special-process programme. SA23-1 still limits Ekonerg's scope
because those activities were not fully defined as special processes.

**Framework consequence:** applicability must support a reasoned scope boundary,
not only a yes/no flag. The record should say which activity is absent,
conditional, performed by a subcontractor, or outside the supplier's approved
scope.

### 4.6 Internal audits and management oversight

SA20-1 recommends focused project audits because earlier deviations recurred.
SA23-1 records a larger internal-audit programme but still recommends explicit
independence between auditor and evaluator.

**Framework consequence:** audit evidence needs planned scope, auditor
qualification, independence, completed checklist/report, identified actions,
and follow-up effectiveness. A plan without a completed report is only a plan.

## 5. Important reporting nuances

### 5.1 A section status is not a blanket conclusion

The historic reports explicitly warn that `NZ` means one or more attributes in
the section were unacceptable; it does not mean every attribute failed. The
same logic applies to `Z`: a section may be marked satisfactory while its text
contains an unresolved limitation or a recommendation. SA23-1 is a clear
example: the Part 21 section is marked satisfactory while the report says there
has been no actual Part 21 implementation example.

The new framework must therefore report both:

- criterion-level judgment with evidence and uncertainty; and
- activity-level summary with findings, recommendations, and limitations.

It must not derive a numeric score from historic Z/NZ labels.

### 5.2 Recommendations are not findings

Both reports contain three recommendations alongside formal Supplier Findings.
Recommendations identify useful improvement work. A finding states an
unacceptable condition against a requirement. These must remain different
record types in the database and report.

### 5.3 Historical recurrence matters

SA23-1 compares itself with SA20-1 and says that parts of earlier actions were
repeated. This is a high-value audit signal: a closed action is not proof that
the corrective action was effective.

The framework should retain a historical reference link such as
`prior_finding_ref`, while keeping historical reports outside current evidence.
The current audit may use that link to focus review, but a current conclusion
still needs current Ekonerg evidence.

## 6. Proposed framework pivot

The pivot is a dual view, not a replacement of the 18-criterion model.

### View A: Appendix B criterion view

Keep the current 18 criteria, applicability gates, vendor crumbs, evidence
links, evaluation records, gaps, and scoring rules. This answers:

> Does Ekonerg's QA system meet each applicable Appendix B criterion?

### View B: Historic audit activity view

Add a stable activity catalogue based on the 17 sections used in both reports:

1. contracting;
2. design;
3. commercial dedication;
4. software QA;
5. procurement;
6. production, installation, product control, handling, storage, and transport;
7. special processes;
8. testing, inspection, and measuring equipment;
9. document control;
10. organization and QA programme;
11. nonconforming products and Part 21;
12. internal audits;
13. corrective action;
14. training and certification;
15. field services;
16. records; and
17. ISO 14001/ISO 45001 context.

An activity can map to several Appendix B criteria. For example, testing maps
to Inspection (X), Test Control (XI), Measuring and Test Equipment (XII), and
Operating Status (XIV). This many-to-many map is the missing bridge between the
historic reports and the current criterion database.

## 7. Minimum data additions

The following additions are the smallest useful change set:

| Addition | What it stores | Why it matters |
|---|---|---|
| `activity_catalog.yml` | The 17 activity IDs, names, and criterion mappings | Recreates the familiar report structure without weakening Appendix B control. |
| Evidence type vocabulary | Procedure, approval, project plan, design input, calculation, test, inspection, calibration, supplier audit, training, NCR/PDR/FDCR, management review, and record | Lets the sieve seek objective evidence instead of only policy text. |
| Project/sample anchor | Contract, project, modification, supplier, document revision, and date | Keeps evidence tied to a real implementation example. |
| Finding record extension | Condition, requirement, impact, activity, criteria, evidence, prior finding, and status | Makes a finding auditable and supports recurrence analysis. |
| Recommendation record | Improvement text, affected activity, owner, due date, and optional evidence | Keeps recommendations separate from nonconformances. |
| Decision conditions | Approved scope, restrictions, increased oversight, and release conditions | Represents the conditional supplier decisions shown in both examples. |
| Historical reference record | Report ID, finding ID, and recurrence note | Focuses review without treating old reports as current proof. |

## 8. Sieve changes

The sieve should collect two layers of vendor crumbs:

1. **Control crumbs:** what the QMS says should happen; and
2. **Implementation crumbs:** records or examples showing that it happened.

For each important control, the prompt should ask for the strongest available
implementation evidence. Examples include:

- a signed or approved project plan and its revision history;
- a design-input review and independent verification record;
- a purchase request showing quality requirements flowed down;
- a supplier audit or evaluation and its scope;
- an approved FAT procedure and actual test results;
- a calibration or independent check record;
- an NCR/PDR/FDCR with disposition and closure;
- a corrective-action cause analysis and effectiveness check;
- a qualified-person list linked to the work performed; and
- an internal audit report with auditor independence and follow-up.

If only a high-level policy statement exists, keep it as a lead and label the
implementation evidence as missing or unconfirmed. Fuzzy logic should broaden
the search for related evidence; it must not turn a policy promise into proof.

## 9. Report output to target

The next report should be able to render these sections:

1. audit identity, dates, team, supplier boundary, and source editions;
2. scope of Ekonerg work and controlled subcontractor work;
3. executive conclusion and conditional approval limits;
4. Appendix B applicability and criterion score table;
5. 17-activity status table with `Z`, `NZ`, `N/A`, or `not audited` explained;
6. objective evidence narrative grouped by project and activity;
7. Supplier Findings, each with requirement, condition, evidence, impact, and action;
8. recommendations and positive practices;
9. previous-audit actions and recurrence analysis;
10. Part 21 and corrective-action review;
11. technical specialist summary and capability boundary; and
12. appendices with source manifest, evidence links, approvals, and validation.

## 10. Recommended implementation order

1. **Crosswalk first:** add the activity catalogue and many-to-many mapping to
   the existing 18 criteria. This is configuration, not a new scoring model.
2. **Evidence anchors second:** add project, contract, supplier, revision, and
   evidence-type fields to the generated matrix and review records.
3. **Finding and recommendation records third:** keep the two outcomes separate
   and add prior-finding references.
4. **Decision conditions fourth:** represent supplier restrictions and increased
   oversight outside the numeric score.
5. **Report renderer fifth:** produce the historic-style activity report from
   the same evidence package used for the criterion report.
6. **Golden tests last:** use small, clearly marked historical fixtures to test
   recurrence, N/A versus not audited, recommendation separation, and a
   policy-only crumb that must not receive a positive implementation judgment.

This order keeps the current audit evidence safe. It improves the framework at
the reusable source instead of adding one-off patches for these two reports.

