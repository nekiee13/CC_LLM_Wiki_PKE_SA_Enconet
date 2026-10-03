# MIN-0.1 owner gate packet

**Status:** G1 approved by owner; no-local-backup reset completed; intake is ready.

## What this packet covers

This packet freezes the current Ekonerg source set and records the choices that
must be approved before real processing. It does not copy, edit, or ingest the
files in `Ekonerg/incoming/`.

## Source set fingerprint

- Folder: `Ekonerg/incoming/`
- Files: **31 Markdown files**
- Total bytes: **1,851,547**
- Register: `Ekonerg/manifests/raw_sources.csv`
- Register SHA-256: `19de710132a8a3eb98e4f8b5f3d2709ac0c55a4dc28996b365a67cc032af8e14`
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

## G1 decision update

The owner approved this exact 31-file source set. The approval reference used
for the dated snapshot is `G1-EKONERG-2026-10-02`.

The owner will protect the original documents outside this audit project. The
owner therefore waived a second local backup of generated audit state. The
`Ekonerg/backup` folder is not used. If a local generated-state backup is ever
wanted, it must still be outside the project because a backup inside the
project could be deleted by reset.

## Supplier boundary — ELI5

Think of the boundary as a fence around the audit. The fence contains
Ekonerg's own QA system and the work Ekonerg delivers. It does not automatically
make every company that Ekonerg buys from a second audit target.

If an outside supplier or subcontractor can affect Ekonerg's quality result,
we check how Ekonerg controls that work: supplier selection, contract flow-down,
acceptance, and follow-up. We record the outside company as evidence about
Ekonerg's control, not as a new audited supplier. The owner said Ekonerg is the
only supplier in this audit scope; the supplier list and one flow-down sample
are still needed to test that boundary.

## Remaining G1 clarifications

Please record one decision for each item:

1. **Source snapshot/effective date:** what date or controlled snapshot should
   identify these exact 31 files?
2. **NQA-1 edition:** confirm that the supplied preface and split files are the
   intended interpretation set. The preface states 2015; the split files do
   not prove edition completeness by themselves.
3. **NRC dates:** the Appendix B and Part 21 files do not state a capture or
   effective date in the checked headings. Confirm how that uncertainty should
   be recorded.
5. **Missing images:** 26 Markdown files link to image assets not present in
   `incoming/`. Confirm that affected claims stay unverified unless the
   original assets are supplied.
6. **Reset backup choice:** owner waived the local generated-state backup;
   original-document protection remains the owner's responsibility.
7. **Supplier boundary evidence:** provide the supplier/subcontractor list and one
   flow-down sample if covered work is outsourced.

## Dated source snapshot

Created without copying source text:

- Path: `Ekonerg/out/2026-10-02/source_snapshot.json`
- Command: `python -B Ekonerg/scripts/source_snapshot.py --date 2026-10-02 --g1-ref G1-EKONERG-2026-10-02`
- Exit code: **0**
- Contents: 31 relative paths, byte counts, and SHA-256 hashes; no document text.

The `out/YYYY-MM-DD/` folder is for immutable result snapshots. Each audit run
should write its package, report, dashboard, validation record, and source hash
manifest under its date/run folder. Do not overwrite an existing snapshot.

A post-reset source snapshot was also recorded at
`Ekonerg/out/2026-10-03/source_snapshot.json`. It contains the same 31 incoming
files and hashes, proving that reset did not change the owner-provided sources.

## MIN-0.2 reset preview and apply

A read-only reset preview was run before any real intake:

- Command: `python -B Ekonerg/scripts/reset_audit.py --plan reset-plans/ekonerg-reset-2026-10-02-g1.json`
- Exit code: **0**
- Plan SHA-256: `15c441c652ffc287c92cf266205a460e3ec8c35f7de42b8e44aa074b5434b571`
- Candidates: **49 files** — 46 delete, 3 truncate.
- Incoming snapshot: 31 files; hashes match the source register.
- Apply: completed on 2026-10-03 with `--no-backup` and
  `RESET-EKONERG-NO-BACKUP`; 46 files deleted and 3 manifests reset to headers.
- Backup result: `owner-waived`; no local archive was created, per owner decision.
- Post-apply verification: all 49 planned targets matched the requested result;
  incoming and framework files remained present.

The reset command now has two explicit modes. Normal apply creates an external
generated-state backup and requires `RESET-EKONERG`. The owner-approved
no-local-backup mode requires `--no-backup` plus the separate token
`RESET-EKONERG-NO-BACKUP`. The owner authorized and completed the no-local-backup
apply on 2026-10-03.

## Gate result

**G1 is approved and reset is complete.** Real ingestion may now start.
The remaining source-edition,
NRC-date, missing-image, and supplier-boundary items stay visible as audit
limitations or evidence requests; they do not get silently filled in.
