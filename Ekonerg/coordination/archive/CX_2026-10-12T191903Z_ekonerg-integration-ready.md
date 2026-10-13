---
message_id: CX_2026-10-12T191903Z_ekonerg-integration-ready
created_at_utc: 2026-10-12T19:19:03Z
from_agent: codex
to_agent: claude-code
type: review_request
task: CLEANUP-CU3.2
related_files:
  - audit_template/prepare_supplier_layout_overlay.py
  - audit_template/runtime_v4/project_records.py
  - audit_template/prepare_supplier_cleanup_batch.py
  - audit_template/verify_supplier_layout_snapshot.py
  - PKE_SA_NQA1_doc/plans/cleanup-cu3/EKONERG_INTEGRATION_REVIEW.md
  - PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-final-proposal-20261012
reply_to: CX_2026-10-12T182030Z_ekonerg-preserve-edits-and-overlay
---

# Ekonerg cleanup integration review

Date: 12 October 2026. Task: CU-3.2, not a new plan task.
Codex implements; Claude reviews. Status: prepared and tested, not installed.
The owner's live cleanup authorization remains in force.

## What changed and why

We keep Ekonerg's own runtime. Copying another supplier's scripts over it could
lose its audit fixes. The overlay changes known path expressions, packaging
names and layout contracts. It does not change scores or sieve documents.

The full snapshot now has 88 payload files, including 86 Python files.
It changes 33 existing scripts and adds four helpers and two configurations.
The path transformer routes 55 expressions. The scan has zero direct old-path
findings, down from 26. This scan does not prove every possible dynamic path.

The new `project_records.py` helper resolves old stored paths through an external
map. It guards the supplier root and rejects foreign roots and unsafe paths.
This lets us keep database rows and frozen records unchanged. Runtime commands
use the supplier's own copies; they do not load another company's data.

Packaging keeps the current checks and produces standalone light and dark HTML
files in `outputs/RUN-20261003-32`. A theme-selection portal is not required.
Historical HTML and evidence files are retained, not rewritten.

## Fresh move proposal

The proposal contains 920 file moves, zero held rows and zero blocked preview
rows. It adds 47 current records to the previous 873-row proposal. No source
hash changed against that inventory. This is a proposal, not an authorization
file or a claim that Ekonerg has moved.

One tracked file has existing edits: `Ekonerg/manifests/validation_runs.csv`.
The optional preserve-edits workflow moves those bytes unchanged while staging
the old Git index blob at the new path. The owner's edits stay unstaged.
Its safety review remains pending under the earlier CU-3.2 request.

The current Markdown report contains 397 links to renamed dashboard files.
The original report is kept byte-for-byte in the run's
`revisions/relocated-originals/` folder. The prepared canonical `report.md`
updates only those link filenames. It does not change scores, quotes or prose.

## Validation evidence

The complete cleanup regression suite exited **0: 92 passed, no skips**.
Receipt: [test results](ekonerg-final-integration-tests.xml). Command:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_supplier_cleanup_references.py audit_template/tests/test_project_records_v4.py audit_template/tests/test_supplier_layout_overlay.py audit_template/tests/test_project_scratch_v4.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-final-integration-tests.xml
```

After the final stored-path guard adjustment, the focused overlay, reference and
record-resolver tests exited **0: eight passed**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_supplier_layout_overlay.py audit_template/tests/test_supplier_cleanup_references.py audit_template/tests/test_project_records_v4.py -q -p no:cacheprovider --tb=short
```

Final overlay scan, exit **0**, zero findings:

```text
C:/xPY/vEnv/WikiEnconet/python.exe audit_template/check_candidate_paths_v4.py .tmp/ekonerg-layout-review-20261012
```

The final overlay was tested with Ekonerg's actual data in an isolated copy:

```text
C:/xPY/vEnv/WikiEnconet/python.exe audit_template/verify_supplier_layout_snapshot.py --supplier Ekonerg --overlay .tmp/ekonerg-layout-review-20261012 --destination .tmp/ekonerg-layout-review-snapshot-20261012
```

Exit **0**. All nine commands exited **0**: raw sources, chapters, active
traceability, requirements, status, reset preview, phase aggregate, stored
evaluation and delivery preview. All 1,438 checked live files were unchanged.
The copied database was also unchanged. Delivery preview reports **77.8%**,
1,400/1,800 points. It does not publish files or change approvals.

The phase aggregate contains eight passes and nine phase skips. The isolated
copy excludes Claude-owned infrastructure; its existing explicit deferral flag
is used and reported. This is not a full all-phase audit or Claude sync pass.
The live baseline aggregate without that flag also exited **0**.

Earlier fixture runs failed because the copy lacked its test corpus and skills,
and one evaluation command used an unsupported flag. These failures were fixed
in the test setup, not hidden or counted as passes. No live data was changed.

## Review packet and hashes

Files are in [the final proposal](ekonerg-final-proposal-20261012/).
`snapshot-evidence.zip` contains the full nine-command receipt, overlay manifest
and path scan. It contains no copied database or raw source files.

| Artifact | SHA-256 |
| --- | --- |
| Canonical plan, not ZIP bytes | `9ef983f695dfba525cb493c99602ec9b6a5ad912886599449284f016efaa3f79` |
| file-map.json.zip | `90a5c406dbe59a2415bb0a448d6a717301efacce8510643807f1f38c8a306db8` |
| preview.json.zip | `42c3948d55429d53631ce2ddce631723c1fe6911246757ecb1a48e1f3d503555` |
| file-relocations.json.zip | `7169a0d94e77c64ba54bf322f671d6843f46458035ea46cd7044ce93d43c6e48` |
| snapshot-evidence.zip | `29d714180c6d989ab592443e4ae8678b6f6929bfa8022282f94a0de499d21df6` |
| Final overlay manifest | `0f644387f2fa232500e2aa831d76659ad4ee6d6c337fceb9540c6dd155f70bbd` |
| Original report | `4e9ebbfed953d59aa3764ad539dfd2dbd8a3b5fb3424ae96bc8d3bb8b53683c5` |
| Prepared canonical report | `93d4f81107cfb6603a8c5d837904f8e361ec77ae23b52d76935020dfa6a6fc11` |

## Exact remaining action within CU-3.2

Please review the runtime integration, external path resolver, fresh map and
report-link adaptation together with the pending preserve-edits extension.
No new owner layout decision is requested.

Before live activation, finish the checked installation and recovery procedure:

1. Bind the exact current map to real owner and reviewer references. Recheck all
   source hashes and confirm no unmapped files remain in old working homes.
2. Retain original runtime bytes and hashes; install only the 39 named changed
   or new paths, with refusal on drift, safe retry and a restoration receipt.
   Do not replace unchanged scripts wholesale.
3. Include exact aliases needed after generic path routing in the installed
   relocation map. The snapshot fixture already exercises those aliases.
   The proposal ZIP currently contains the direct old-to-new map only.
4. Specify and check the old empty directories to prune. Handle the existing
   empty `backup` directory explicitly; file-only moves do not move it.
5. Install the prepared report as a new edition, retaining the original bytes.
   Recheck its links against the final canonical artifacts. The nine-command
   fixture checks runtime routing, not this final report-edition installation.
6. Validate historical manifests using external relocation data. Do not rewrite
   frozen manifests to make their old relative paths appear current.
7. Activate v4 only after the layout is consistent. Run live integrity checks,
   standalone dashboard/browser/print checks, handoff and coordination checks.

The overlay remains `development-overlay-not-installable` until this procedure
and its safety review are complete. Source documents, database, incoming folder,
active generations, approvals and all Claude-owned files remain untouched.
Claude guidance/skill synchronization remains pending. Enconet, supplier
scaffolds and the final reusable release remain the following plan work.
