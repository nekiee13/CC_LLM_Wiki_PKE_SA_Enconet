# MIN-0.1 owner gate packet

**Status:** pending owner G1 decision; no source promotion or audit conclusion.

## What this packet covers

This packet freezes the current Ekonerg source set and records the choices that
must be approved before real processing. It does not copy, edit, or ingest the
files in `Ekonerg/incoming/`.

## Source set fingerprint

- Folder: `Ekonerg/incoming/`
- Files: **31 Markdown files**
- Total bytes: **1,851,547**
- Register: `Ekonerg/work/fast_audit/EF-20261001-01/source_register.csv`
- Register SHA-256: `f0b62b19a989ec9960d39df56181c34d6821be3d050ffd4c37b0beb64c516662`
- Last independent register check: 31 rows, 31 files, no changed hashes,
  no duplicate IDs or hashes, and strict UTF-8 decoding passed.

The register is a local ignored work record. It is not itself an approval.
The incoming files remain the owner-controlled source drop.

## Proposed source roles

| Role | Files | Use in this audit |
|---|---|---|
| Governing rule | 10 CFR 50 Appendix B | Main audit benchmark; 18 criteria |
| Supplemental rule | 10 CFR Part 21 | Mainly nonconformance and corrective-action controls |
| Interpretation | ASME NQA-1 Parts 1–4 files | Part 1 mandatory baseline; Part 2 only if explicitly invoked; Parts 3–4 guidance unless separately invoked |
| Company evidence | 23 QMS procedures and one QMS manual | Ekonerg QA-system evidence |

## Owner decisions already recorded

- Audit question: assess Ekonerg's QA system against Appendix B, using ASME
  NQA-1 as the interpretation baseline.
- Supplier scope: Ekonerg is the only supplier in this audit scope.
- Work activities: design, engineering services, and consultancy.
- Part 21: applicable mainly to nonconformances and corrective actions.
- Preliminary screen: 12 applicable, 6 conditional, 0 final N/A.

These statements are recorded owner direction. They do not by themselves
approve source editions or close the conditional applicability questions.

## Open G1 decisions for the owner

Please record one decision for each item:

1. **Source snapshot/effective date:** what date or controlled snapshot should
   identify these exact 31 files?
2. **Source approval:** approve this exact register for G1, or list changes.
3. **NQA-1 edition:** confirm that the supplied preface and split files are the
   intended interpretation set. The preface states 2015; the split files do
   not prove edition completeness by themselves.
4. **NRC dates:** the Appendix B and Part 21 files do not state a capture or
   effective date in the checked headings. Confirm how that uncertainty should
   be recorded.
5. **Missing images:** 26 Markdown files link to image assets not present in
   `incoming/`. Confirm that affected claims stay unverified unless the
   original assets are supplied.
6. **Controlled backup:** name the approved backup location outside Ekonerg.
7. **Supplier boundary:** provide the supplier/subcontractor list and one
   flow-down sample if covered work is outsourced.

## MIN-0.2 reset preview

A read-only reset preview was run before any real intake:

- Command: `python -B Ekonerg/scripts/reset_audit.py --plan reset-plans/ekonerg-reset-min0-2.json`
- Exit code: **0**
- Plan SHA-256: `15c441c652ffc287c92cf266205a460e3ec8c35f7de42b8e44aa074b5434b571`
- Candidates: **49 files** — 46 delete, 3 truncate.
- Incoming snapshot: 31 files; hashes match the source register.
- Apply: **not run**. No backup was created and no project file was removed.

The reset apply needs the owner-selected external backup directory and the
exact confirmation token `RESET-EKONERG`. It must wait for that confirmation.

## Gate result

**G1 is pending.** Real ingestion must not start until the owner records the
source snapshot, source approval, backup location, and any corrections above.
