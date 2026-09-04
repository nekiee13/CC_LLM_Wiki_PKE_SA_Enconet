# EA5.4 Owner usability acceptance

UAT ID: `EA5.4-RUN-20260728-01`

Run: `RUN-20260728-01`

Owner decision: **AWAITING OWNER**

This is the final human usability check for the evidence-access workflow. No command line is needed. Start with the portable package in `outputs/candidates/evidence_access/portable_package`; it may also be copied as one complete folder to another location before testing.

For every step, tick Pass or Fail and briefly record anything surprising. A failure is useful evidence: record it rather than working around it.

### 1. Open the report

Open `RUN-20260728-01/evaluation_report.md` from the portable package.

Expected: the production evaluation report opens and its evidence links are visible.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

### 2. Open a crumb with multiple quotes

In criterion **APP_B_I**, click `CRUMB-DOC-0021-APP_B_I-0003`.

Expected: Evidence Explorer opens the matching crumb and shows exactly these three quote cards: `QUOTE-DOC-0021-0003-01`, `QUOTE-DOC-0021-0003-02`, and `QUOTE-DOC-0021-0003-03`.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

### 3. Confirm the source identity

Read the focused evidence card.

Expected: it shows the statement about Quality Assurance being a separate unit linked to company management; document `DOC-0021`; title *Pravilnik o radu društva ENCONET d.o.o., Revizija 2*; chapter `OPIS RADNIH MJESTA`; chunk `CHUNK-DOC-0021-0105`; all three exact quotes; and source hash beginning `a2c31625`.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

### 4. Navigate adjacent context

Use the Previous and Next context controls around the focused chunk.

Expected: Previous opens `CHUNK-DOC-0021-0104`; Next opens `CHUNK-DOC-0021-0106`; returning to the crumb restores `CHUNK-DOC-0021-0105`.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

### 5. Copy a traceable citation

Return to `CRUMB-DOC-0021-APP_B_I-0003` and use **Copy citation**.

Expected: the copied text identifies the run, document, crumb, quote(s), chunk, and source hash clearly enough for another reviewer to reopen the same evidence.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

### 6. Print or save the evidence card

Use **Print evidence**, then inspect the print preview. Saving a PDF is optional; cancelling after inspection is acceptable.

Expected: the preview contains the focused evidence card and its traceability information, without unrelated application controls obscuring it.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

### 7. Open another criterion

Return to the report. In criterion **APP_B_II**, click `CRUMB-DOC-0021-APP_B_II-0002`.

Expected: the viewer opens the QA manager responsibility statement in `CHUNK-DOC-0021-0119` and shows its two exact quotes, `QUOTE-DOC-0021-0006-01` and `QUOTE-DOC-0021-0006-02`.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

### 8. Select the run from the landing page

Open `review_workspace.html`, find `RUN-20260728-01`, and select it.

Expected: the registered production run is identifiable and its matching report and Evidence Explorer links open the same run artifacts tested above.

Pass: [ ]  Fail: [ ]  Observation: ______________________________

## Controlled artifact fingerprints

Use these only to identify the exact candidate under acceptance; you do not need to calculate them manually.

| Artifact | SHA-256 |
| --- | --- |
| Package manifest | `efcbada9b59862f8f0ba00c739147a2a5e4076d0009f87b3af539a5cb60a0012` |
| Review workspace | `a795aa0dc288de40c9114bb1841395a9f45314c124e07a96a89b0e631fff82df` |
| Portable report | `04cec818cc8f80a999851148e3ac3c80b4c5e1fdcb25dbe25dceaa19feb374b3` |
| Evidence Explorer | `cf4e9f6ed3dae44948ca7af6e0e177a0f7b84e5ca345fac2d55f701f755ebde6` |

## Owner decision — human gate

Codex must not complete this section or infer acceptance from automated tests.

- Decision: **APPROVE** / **REJECT**
- Decided at (date and time, preferably UTC): ______________________________
- Decision reference (message, signed record, or other durable reference): ______________________________
- Observed defects, including the failed step number(s): ______________________________

Approval means all eight steps are usable without repository knowledge or a command line. Rejection sends each observed defect back to development with a regression test before correction.
