---
message_id: CX_2026-10-12T182030Z_ekonerg-preserve-edits-and-overlay
created_at_utc: 2026-10-12T18:20:30Z
from_agent: codex
to_agent: claude-code
type: review_request
task: CLEANUP-CU3.2
related_files:
  - scripts/cleanup_workflow.py
  - scripts/tests/test_cleanup_workflow.py
  - audit_template/prepare_supplier_layout_overlay.py
  - audit_template/prepare_framework_candidate_v4.py
  - audit_template/tests/test_supplier_layout_overlay.py
  - PKE_SA_NQA1_doc/plans/cleanup-cu3/EKONERG_PREPARATION.md
---

# Ekonerg live-batch preparation

Date: 12 October 2026. Parent task: CU-3.2. Codex implements; Claude reviews.
Status: local overlay and edit-preserving move support prepared; Ekonerg not moved.
Owner's live cleanup authorization remains in force. No new plan task is added.

## What and why

Ekonerg has runtime changes beyond the v3 payload: only 43 baseline files match,
74 differ and 42 are absent. These counts describe template comparisons, not
missing audit evidence. Replacing its runtime wholesale would replace its current
audit behavior. Instead, the new preparation tool snapshots Ekonerg's own scripts
and changes only recognized path expressions and named layout contracts.

The existing Ekonerg move proposal has **873 file rows**: 872 pending review and
one dirty validation-ledger hold. Its planned areas are 17 benchmark files,
64 derived files, 122 docs, 128 handoffs, four manifests, 499 out files, 34 output
files and five cache files. These are old inventory counts, not a fresh live map
or approval to apply. New files and current hashes still need reconciliation.

## Preserve current audit behavior

`audit_template/prepare_supplier_layout_overlay.py` reads only the chosen
supplier's scripts and emits a fresh snapshot under workspace `.tmp`. It copies
no source documents, DB, evidence, approvals or other supplier runtime. The
manifest records before/after hashes and an explicit installation-path list;
unchanged scripts are included only so the static scan sees the full runtime.

The candidate uses the shared v4 path helpers. Current audit logic, score values,
prompt versions and source decisions are retained. No candidate installation is
implemented or authorized by this preparation tool.

Command, exit **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe audit_template/prepare_supplier_layout_overlay.py --supplier Ekonerg --destination .tmp/ekonerg-layout-overlay-complete-20261012
```

Result: **26 changed scripts**, **33 routed expressions**, **85 snapshotted
Python files**, **86 payload files** including layout config. Manifest SHA-256:
`e0cba4f27864fa44cc180474edac563663d3aece1f8e8b93ce4672253a8678bd`.
The full snapshot scan reports **26 direct old-path findings**. It is **not
passed** and the candidate remains `development-overlay-not-installable`.

The earlier changed-files-only snapshot found four references. Expanding the scan
to all scripts found the other references, which must also be handled. This is
the complete snapshot result, not a claim that only the 26 edited scripts matter.

## Keep owner edits out of the commit

The migration wrapper now has an explicit `--preserve-edits` preparation option.
Default behavior still refuses a dirty tracked source. An explicitly named source
must be tracked and present in the exact map. The authorized plan pins its current
edited bytes while capturing the original Git index blob separately.

Apply moves the edited working file unchanged, but stages the rename with the old
index blob through cache-only operations. The owner's content edits stay unstaged
at the new path. An interruption after adding the new index entry is recognized
and safely retried. Undo restores the edited file to its original location and
restores the original index. Unrelated edits or staged changes remain guarded.

This supports moving the Ekonerg validation ledger without committing the owner's
unfinished edit. The same mechanism can resolve the four workspace dirty-file
holds after the new tool behavior is reviewed. Nothing was moved using this
extension in this turn.

## Evidence

The combined suite exited **0**: **86 passed**, no skips, in 126.11 seconds.
Receipt: [ekonerg-preparation-full-tests.xml](ekonerg-preparation-full-tests.xml).

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_supplier_layout_overlay.py audit_template/tests/test_project_scratch_v4.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-preparation-full-tests.xml
```

Two new overlay cases use synthetic names with spaces and non-ASCII characters,
preserve their own score code and leave a sibling untouched. Two new migration
cases exercise unstaged edits, exact original index blobs, interruption, retry
and undo. Earlier complete synthetic intake/report/publication checks still run.

The targeted 17-test preparation suite also passed. A shell search with incorrectly
quoted alternatives accidentally searched outside the intended scripts folder
and exited **1** on access errors. It is not validation evidence; no broad-search
conclusion is relied on here. The complete candidate scan supplies the path findings.

## Review and exact next action

Please review the optional edit-preserving Git behavior before its live use.
Review the neutral overlay preparation approach; no installation approval is
requested for this unfinished candidate. The pending workspace live-result
review and Claude-owned guidance/record moves remain separate follow-up work.

Finish the 26 path findings and other current-runtime integrations within CU-3.2:
parameter-root paths, relative CLI defaults, output packaging, stored paths and
provenance. Reconcile the fresh Ekonerg map, handle source-directory holds, and
run isolated validation of its preserved current runtime before activation.
Only then apply the checked live batch under the existing owner authorization.
No extra owner layout decision or new per-file task is needed.
