# EA5.4 Owner usability acceptance

UAT ID: `EA5.4-RUN-20260728-01`

Run: `RUN-20260728-01`

Owner decision: **AWAITING OWNER**

The Owner approved the original eight-step candidate on 2026-09-04. Claude's subsequent
independent review found that document and package links displayed an arbitrary crumb. The
corrected candidate was approved on 2026-09-04. The Owner then requested an explicit corresponding
chapter reference for every quote. That presentation correction changes the viewer fingerprints,
so each earlier approval remains historical evidence and is not carried forward. Re-run the same
ten-step workflow, paying particular attention to steps 3 and 5.

This is the final human usability check for the evidence-access workflow. No command line is needed. Start with the portable package in `outputs/candidates/evidence_access/portable_package`; it may also be copied as one complete folder to another location before testing.

For every step, tick Pass or Fail and briefly record anything surprising. A failure is useful evidence: record it rather than working around it.

### 1. Open the report

Open `RUN-20260728-01/evaluation_report.md` from the portable package.

Expected: the production evaluation report opens and its evidence links are visible.

Pass: [ ]  Fail: [ ]  Observation:

### 2. Open a crumb with multiple quotes

In criterion **APP_B_I**, click `CRUMB-DOC-0021-APP_B_I-0003`.

Expected: Evidence Explorer opens the matching crumb and shows exactly these three quote cards: `QUOTE-DOC-0021-0003-01`, `QUOTE-DOC-0021-0003-02`, and `QUOTE-DOC-0021-0003-03`.

Pass: [ ]  Fail: [ ]  Observation:

### 3. Confirm the source identity

Read the focused evidence card.

Expected: it shows the statement about Quality Assurance being a separate unit linked to company management; document `DOC-0021`; title *Pravilnik o radu društva ENCONET d.o.o., Revizija 2*; and source hash beginning `a2c31625`. Each of the three quote cards explicitly shows the corresponding chapter path `1. PRILOG PRAVILNIKA O RADU > OPIS RADNIH MJESTA`, in addition to its line locator and chunk `CHUNK-DOC-0021-0105`.

Pass: [ ]  Fail: [ ]  Observation:

### 4. Navigate adjacent context

Use the Previous and Next context controls around the focused chunk.

Expected: Previous opens `CHUNK-DOC-0021-0104`; Next opens `CHUNK-DOC-0021-0106`; returning to the crumb restores `CHUNK-DOC-0021-0105`.

Pass: [ ]  Fail: [ ]  Observation:

### 5. Copy a traceable citation

Return to `CRUMB-DOC-0021-APP_B_I-0003` and use **Copy citation**.

Expected: the copied text identifies the run, document, crumb, quote(s), corresponding chapter path, chunk, and source hash clearly enough for another reviewer to reopen the same evidence.

Pass: [ ]  Fail: [ ]  Observation:

### 6. Print or save the evidence card

Use **Print evidence**, then inspect the print preview. Saving a PDF is optional; cancelling after inspection is acceptable.

Expected: the preview contains the focused evidence card and its traceability information, without unrelated application controls obscuring it.

Pass: [ ]  Fail: [ ]  Observation:

### 7. Open another criterion

Return to the report. In criterion **APP_B_II**, click `CRUMB-DOC-0021-APP_B_II-0002`.

Expected: the viewer opens the QA manager responsibility statement in `CHUNK-DOC-0021-0119` and shows its two exact quotes, `QUOTE-DOC-0021-0006-01` and `QUOTE-DOC-0021-0006-02`.

Pass: [ ]  Fail: [ ]  Observation:

### 8. Select the run from the landing page

Open `review_workspace.html`, find `RUN-20260728-01`, and select it.

Expected: the registered production run is identifiable and its matching report and Evidence Explorer links open the same run artifacts tested above.

Pass: [ ]  Fail: [ ]  Observation:

### 9. Open the document record

In any criterion's scope-justification line, click `document:DOC-0024`.

Expected: the drawer identifies `DOC-0024` and shows its document metadata. It does not show a
crumb statement, exact quotes, or a source chapter, because a document-wide citation does not
identify one exact crumb.

Pass: [ ]  Fail: [ ]  Observation:

### 10. Open the package record

Open `#evidence/source/package` in Evidence Explorer.

Expected: the drawer shows `RUN-20260728-01`, supplier, language, package hash, and evidence-bundle
hash. It does not show a crumb statement, exact quotes, or a source chapter.

Pass: [ ]  Fail: [ ]  Observation:

## Controlled artifact fingerprints

Use these only to identify the exact candidate under acceptance; you do not need to calculate them manually.

| Artifact | SHA-256 |
| --- | --- |
| Package manifest | `f3b72fdd381453af69b97e8d6e423c749fdbe045f3b0a55e8c7d43fc22faa95d` |
| Review workspace | `3b891a37a5ef4c96dbb42890e078ceb7f88f586c6f43e40b75cafc15a3aef1b0` |
| Portable report | `04cec818cc8f80a999851148e3ac3c80b4c5e1fdcb25dbe25dceaa19feb374b3` |
| Evidence Explorer | `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d` |

## Owner decision — human gate

The previous approval is historical because it identifies different viewer bytes. Record a new
decision only after checking the chapter-reference behavior above.

- Decision: **PENDING**
- Decided at: pending
- Decision reference: pending
- Observed defects: pending

Approval means all ten steps are usable without repository knowledge or a command line. Rejection sends each observed defect back to development with a regression test before correction.
