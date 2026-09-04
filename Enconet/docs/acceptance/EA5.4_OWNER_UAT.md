# EA5.4 Owner usability acceptance

UAT ID: `EA5.4-RUN-20260728-01`

Run: `RUN-20260728-01`

Owner decision: **APPROVED**

The Owner approved the original eight-step candidate on 2026-09-04. Claude's subsequent
independent review found that document and package links displayed an arbitrary crumb. The
corrected candidate has new fingerprints, so that earlier approval remains historical evidence
and is not carried forward. Re-run the workflow below, including the two new regression steps.

This is the final human usability check for the evidence-access workflow. No command line is needed. Start with the portable package in `outputs/candidates/evidence_access/portable_package`; it may also be copied as one complete folder to another location before testing.

For every step, tick Pass or Fail and briefly record anything surprising. A failure is useful evidence: record it rather than working around it.

### 1. Open the report

Open `RUN-20260728-01/evaluation_report.md` from the portable package.

Expected: the production evaluation report opens and its evidence links are visible.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 2. Open a crumb with multiple quotes

In criterion **APP_B_I**, click `CRUMB-DOC-0021-APP_B_I-0003`.

Expected: Evidence Explorer opens the matching crumb and shows exactly these three quote cards: `QUOTE-DOC-0021-0003-01`, `QUOTE-DOC-0021-0003-02`, and `QUOTE-DOC-0021-0003-03`.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 3. Confirm the source identity

Read the focused evidence card.

Expected: it shows the statement about Quality Assurance being a separate unit linked to company management; document `DOC-0021`; title *Pravilnik o radu društva ENCONET d.o.o., Revizija 2*; chapter `OPIS RADNIH MJESTA`; chunk `CHUNK-DOC-0021-0105`; all three exact quotes; and source hash beginning `a2c31625`.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 4. Navigate adjacent context

Use the Previous and Next context controls around the focused chunk.

Expected: Previous opens `CHUNK-DOC-0021-0104`; Next opens `CHUNK-DOC-0021-0106`; returning to the crumb restores `CHUNK-DOC-0021-0105`.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 5. Copy a traceable citation

Return to `CRUMB-DOC-0021-APP_B_I-0003` and use **Copy citation**.

Expected: the copied text identifies the run, document, crumb, quote(s), chunk, and source hash clearly enough for another reviewer to reopen the same evidence.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 6. Print or save the evidence card

Use **Print evidence**, then inspect the print preview. Saving a PDF is optional; cancelling after inspection is acceptable.

Expected: the preview contains the focused evidence card and its traceability information, without unrelated application controls obscuring it.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 7. Open another criterion

Return to the report. In criterion **APP_B_II**, click `CRUMB-DOC-0021-APP_B_II-0002`.

Expected: the viewer opens the QA manager responsibility statement in `CHUNK-DOC-0021-0119` and shows its two exact quotes, `QUOTE-DOC-0021-0006-01` and `QUOTE-DOC-0021-0006-02`.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 8. Select the run from the landing page

Open `review_workspace.html`, find `RUN-20260728-01`, and select it.

Expected: the registered production run is identifiable and its matching report and Evidence Explorer links open the same run artifacts tested above.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 9. Open the document record

In any criterion's scope-justification line, click `document:DOC-0024`.

Expected: the drawer identifies `DOC-0024` and shows its document metadata. It does not show a
crumb statement, exact quotes, or a source chapter, because a document-wide citation does not
identify one exact crumb.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

### 10. Open the package record

Open `#evidence/source/package` in Evidence Explorer.

Expected: the drawer shows `RUN-20260728-01`, supplier, language, package hash, and evidence-bundle
hash. It does not show a crumb statement, exact quotes, or a source chapter.

Pass: [x]  Fail: [ ]  Observation: Owner approved the corrected ten-step UAT.

## Controlled artifact fingerprints

Use these only to identify the exact candidate under acceptance; you do not need to calculate them manually.

| Artifact | SHA-256 |
| --- | --- |
| Package manifest | `89a55446e4fc0c36952d6020c9bd8baa8a7595d04814bf5f90d91165ea9a7217` |
| Review workspace | `37c8e0df1d01334031c538b5f7c45118f64122965c74194b827c2e78c26b17b8` |
| Portable report | `04cec818cc8f80a999851148e3ac3c80b4c5e1fdcb25dbe25dceaa19feb374b3` |
| Evidence Explorer | `74e54dfa2faf6e62f410febdc4d2e729fd6324d8de3edeb1d6d700e734ba04a2` |

## Owner decision — human gate

Recorded from the Owner's explicit decision; this section was not inferred from automated tests.

- Decision: **APPROVE**
- Decided at: `2026-09-04T19:34:59Z`
- Decision reference: Owner chat approval on 2026-09-04: “Owner approved corrected ten-step UAT”
- Observed defects: none

Approval means all ten steps are usable without repository knowledge or a command line. Rejection sends each observed defect back to development with a regression test before correction.
