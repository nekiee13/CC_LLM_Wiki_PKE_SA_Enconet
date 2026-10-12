# Ekonerg live cleanup sprint result

Date: 12 October 2026. Task: CU-3.2. Existing bundle executed.
Status: live layout activated and verified; one empty-directory hold remains.
No new tool or plan task was added in this sprint.

## Owner authority

The owner explicitly said:

> Proceed with the existing cleanup bundle; defer Claude's pre-execution safety review.

Decision: [OWNER-CLEANUP-SPRINT-20261012-REVIEW-DEFERRED](OWNER_SPRINT_REVIEW_DEFERRAL.md).
This is a timing exception, not a claim that Claude reviewed the changes.
Claude's post-execution review and owned-guidance synchronization remain pending.

## What actually moved

- **924 files**, all verified against their sealed hashes and file identities.
- **592 tracked renames**, with their original Git blobs retained.
- **Nine of ten original directory trees**, retaining identity, owners and DACLs.
- **39 runtime/configuration files** installed from the checked Ekonerg overlay.
- Current handoffs now use `coordination/handoffs`.
- Working records use `work`; plans use `docs/plans`.
- Results use `outputs/RUN-20261003-32`; both HTML dashboards are standalone.

The canonical `report.md` is a new, checked edition with 397 dashboard filename
links updated. Its original report remains byte-for-byte in the run's revision
history. No source document, database row, evidence quote, score, gate or active
generation changed. No audit reset, resieving or new audit assessment took place.

## Current entry files

- Light: `Ekonerg/outputs/RUN-20261003-32/dashboard_light.html`
- Dark: `Ekonerg/outputs/RUN-20261003-32/dashboard_dark.html`
- Report: `Ekonerg/outputs/RUN-20261003-32/report.md`
- Stored evaluation: `Ekonerg/outputs/RUN-20261003-32/evaluation_package.json`

The score remains **77.8%, 1,400/1,800 points**. Delivery preview confirms
475 active DOCUMENT crumbs and 55 active RULE crumbs; the displayed evaluation
links 379 crumbs, 442 quotes, 118 chapters and 24 documents. These numbers are
unchanged, not new sieving results.

## Integrity and functional checks

[Sealed packet](ekonerg-live-sprint-20261012/) contains the exact file/directory
plans, authorizations, original Git index, protected baseline, post-live proof,
runtime installation plan, validation output and regression receipt.
Live journals and original runtime files are retained under
`Ekonerg/work/migrations/cleanup-cu3-live-20261012/`.

The post-live proof verifies:

- All **821 protected files** in the baseline are unchanged. This includes
  incoming/raw/database/DATA and the captured Claude-owned records/infrastructure.
- Six pre-existing dirty files keep identical bytes. The owner's original
  `wiki/log.md` bytes remain an exact prefix before normal publisher appends.
- The validation-ledger edit stays unstaged at `work/manifests/validation_runs.csv`.
- All 924 file moves and 39 runtime installations match their journals.
- All **397 local report links** resolve.

Checks completed:

| Check | Exit | Result |
| --- | ---: | --- |
| Retried file workflow | 0 | 924 moved, 592 tracked; index verified |
| Runtime installation | 0 | 39 installed |
| Current-phase aggregate | 0 | Eight passes, nine phase skips; no Claude deferral flag needed |
| Raw source verification | 0 | Passed |
| Active traceability | 0 | Passed |
| Stored evaluation | 0 | 18/18 structurally valid; no new audit approval |
| Frozen delivery manifest | 0 | 16 member references verified after relocation |
| Frozen portable manifest | 0 | Eight member references verified after relocation |
| Light live browser/PDF | 0 | 29 checks passed |
| Dark live browser/PDF | 0 | 29 checks passed |
| Full cleanup regression | 0 | **125 passed**, no skips, in 128.58 seconds |
| Delivery preview | 0 | Existing score and evidence counts preserved; no publication writes |

Exact core commands/stdout are in `live-validation-commands.json`.
Frozen-manifest receipts are `release-verification.json` and
`portable-verification.json`. Full regression receipt is `regression-tests.xml`.
Browser checks, desktop/mobile images and real PDFs are under
`Ekonerg/work/validation/cleanup-live-20261012/{light,dark}`.
Each browser check verifies filters, search, keyboard shortcuts, sorting, card
expansion, source-chapter access, mobile overflow, white print, PDF text and an
unchanged HTML hash.

Browser commands, each exit 0, use the existing shared interpreter:

```text
python Ekonerg/scripts/verify_dashboard_browser.py --html Ekonerg/outputs/RUN-20261003-32/dashboard_light.html --output Ekonerg/work/validation/cleanup-live-20261012/light
python Ekonerg/scripts/verify_dashboard_browser.py --html Ekonerg/outputs/RUN-20261003-32/dashboard_dark.html --output Ekonerg/work/validation/cleanup-live-20261012/dark
```

Complete regression command, exit 0:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_empty_homes.py scripts/tests/test_release_relocations.py audit_template/tests/test_supplier_runtime_install.py scripts/tests/test_cleanup_runtime_install.py audit_template/tests/test_supplier_cleanup_references.py audit_template/tests/test_project_records_v4.py audit_template/tests/test_supplier_layout_overlay.py audit_template/tests/test_project_scratch_v4.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-live-sprint-20261012/regression-tests.xml
```

## Stops and recovery during the sprint

The first file apply moved the files but stopped its Git check: 64 frozen
CRLF files lost their old path-specific `-text` policy at the new names.
Independent verification proved every working file unchanged and all 64 staged
differences were line-ending-only. Their exact original Git blobs were restored,
and the old byte policies were added at the new homes. Safe retry then passed.
No evidence content was normalized or edited. Recovery originals/journals are
also marked byte-stable for future checkout.

The initial browser calls used the pinned test environment, which lacks PyMuPDF,
and exited 1. Reruns with the already-installed shared Miniconda environment
passed; no package was installed or upgraded.

The first whole-integrity assertion flagged the expected handoff log append.
The corrected proof explicitly hashes the preserved original log prefix rather
than falsely claiming the entire append-only log was unchanged.

## One remaining filesystem hold

Windows refused the native rename of the empty `Ekonerg/outputs/candidates`
tree, including a safe retry: **WinError 5 / access denied**, exit 1.
Its original identity, owner/DACL and empty tree remain intact. No permission
was changed, no tree was deleted, and its journal is honestly partial: nine
trees moved, one original. The cause is not established as a lock or an ACL defect.

No active output uses that old tree. The operational v4 homes are consistent and
all live data/dashboard checks pass. Do not mark the ten-tree batch complete.
Retain this hold for a later safe retry or owner-directed filesystem resolution.

## Next original-plan work

CU-3.2's operational layout is active; the empty-tree hold and Claude review
remain open. Next sprint task is CU-3.3: apply the existing tools to Enconet's own
runtime and files, retaining its separate sources and scores. Then complete the
existing CU-4 common release, six supplier scaffolds, holds and index checks.
No extra preparation epics or per-file slices are authorized by this result.
