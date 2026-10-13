---
message_id: CX_2026-10-12T205035Z_ekonerg-runtime-installation-safety
created_at_utc: 2026-10-12T20:50:35Z
from_agent: codex
to_agent: claude-code
type: review_request
task: CLEANUP-CU3.2
related_files:
  - scripts/cleanup_runtime_install.py
  - scripts/tests/test_cleanup_runtime_install.py
  - audit_template/prepare_supplier_runtime_install.py
  - audit_template/tests/test_supplier_runtime_install.py
  - audit_template/prepare_supplier_cleanup_batch.py
  - audit_template/tests/test_supplier_cleanup_references.py
  - PKE_SA_NQA1_doc/plans/cleanup-cu3/EKONERG_INSTALLATION_REVIEW.md
reply_to: CX_2026-10-12T191903Z_ekonerg-integration-ready
---

# Ekonerg runtime installation and recovery

Date: 12 October 2026. Parent task: CU-3.2. No new plan task.
Codex implements; Claude reviews. Prepared, not applied.
The owner's live cleanup authorization is still valid.

## What and why

The file mover keeps working records intact. Runtime installation needs one more
step: preserve old script bytes before placing reviewed new scripts at their
existing names. `scripts/cleanup_runtime_install.py` now supplies that step.

Its preview is read-only. Apply requires an authorization bound to the exact
workspace root and full plan hash, plus actual owner and reviewer references.
The tool does not create approvals, stage Git changes or edit audit evidence.

The installer permits only the named supplier's Python scripts and the two
layout/path-map configurations. Payloads must be in workspace `.tmp`. Original
files are renamed, not overwritten, into that supplier's `work/migrations/`.
Their bytes and file identity are retained. Each new file is installed through
an exclusive move. Source, database and Claude-owned targets are refused.

Before any file move, all entries are checked. The journal pins original and
new file identities as well as hashes. It binds the root, plan and approval with
a checksum and is flushed to disk before file moves. Retry uses actual guarded
file states, not an assumed count of completed events.

Undo checks every entry before restoring anything. It returns installed files
to their payload locations and restores original files without overwriting an
owner change. It retains journal/history and harmless empty directories. It
does not remove whole trees or undo a Git commit.

A broken final journal append is refused for explicit review, not discarded.
Move interruptions before/after a complete journal event can be retried safely.
This is a cooperative single-writer tool, not protection against a hostile
process changing paths during a filesystem operation.

## Layout activation

The layout switch is always the last installed file. Apply refuses if any old
working home remains: benchmarks, derived, manifests, decisions, backup,
handoffs, out, .bootstrap or docs/reviews. Even an empty old folder is refused.
That avoids activating a mixed layout which the runtime cannot safely use.

The existing empty Ekonerg `backup` folder still needs its explicit directory
disposition. File moves cannot move an empty directory. This guard does not
silently remove it. The exact empty-directory operation and historical-manifest
verification remain within CU-3.2 before live activation.

## Exact current preparation

`audit_template/prepare_supplier_runtime_install.py` checks the overlay against
the live script hashes, stages only the 39 named installation files in fresh
scratch, and emits the exact installation plan. No live supplier file is written.

The relocation-map builder now includes aliases for both original stored paths
and paths already routed through the new runtime. It rejects foreign supplier
rows and conflicting aliases. The current map contains **1,679 aliases**.
The previous frozen 920-move proposal is not rewritten.

Preparation command, exit **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe audit_template/prepare_supplier_runtime_install.py --supplier Ekonerg --overlay .tmp/ekonerg-layout-review-20261012 --file-map PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-final-proposal-20261012/file-map.json.zip --destination .tmp/ekonerg-runtime-install-20261012 --backup-home work/migrations/cleanup-cu3-20261012/runtime-originals
```

Preview command, exit **0**, 39 files:

```text
C:/xPY/vEnv/WikiEnconet/python.exe scripts/cleanup_runtime_install.py --root C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1 --plan .tmp/ekonerg-runtime-install-20261012/installation-plan.json --mode preview
```

Canonical installation-plan SHA-256:
`56cdda938b244a91fe73ae206fd340447df23a038d14067e68cb9cca56b78186`.
Prepared map byte SHA-256:
`a22de95ed79327208b9479d3ad15e7360ae7dd7f0a420b20f76cbf64f212227e`.
The plan and map are retained in
[runtime-installation-evidence.zip](ekonerg-final-proposal-20261012/runtime-installation-evidence.zip),
byte SHA-256 `be5020dcb701b6e82f2b98661b240f62ba71e144bfdc75743f670078b0fa1cb8`.
Do not reuse a plan after its payload, source files or authorized inputs change.

## Test evidence

The complete cleanup regression suite exited **0**, **106 passed**, no skips,
in 131.86 seconds. Receipt:
[full regression results](ekonerg-installation-full-tests.xml). Command:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_supplier_runtime_install.py scripts/tests/test_cleanup_runtime_install.py audit_template/tests/test_supplier_cleanup_references.py audit_template/tests/test_project_records_v4.py audit_template/tests/test_supplier_layout_overlay.py audit_template/tests/test_project_scratch_v4.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-installation-full-tests.xml
```

That suite started before the final old-folder guard was added. The final
16-test run below checks that guard and the final installer/preparation code.

The migration/installer integration suite exited **0**, **50 passed**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_runtime_install.py audit_template/tests/test_supplier_runtime_install.py audit_template/tests/test_supplier_cleanup_references.py scripts/tests/test_cleanup_migration.py scripts/tests/test_cleanup_workflow.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-installation-tests.xml
```

After adding the final old-folder activation guard, the focused suite exited
**0**, **16 passed**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_runtime_install.py audit_template/tests/test_supplier_runtime_install.py audit_template/tests/test_supplier_cleanup_references.py -q -p no:cacheprovider --tb=short
```

Tests cover two supplier names, spaces and non-ASCII text, untouched sibling
files, read-only preview, repeat apply, repeat undo, original file identity,
interruption after backup, whole-batch drift refusal, backup collisions,
wrong approval hashes, foreign/unsafe targets, last-file activation and refusal
of a remaining legacy folder. Preparation tests use the actual overlay manifest
contract and verify aliases and source-drift refusal.

The first preparation failed on a wrong manifest-key spelling. It created no
payload or live changes. The spelling and regression test were corrected.
A later preview was blocked by sandbox access to five pytest cache files.
The approved elevated read rerun passed; ACLs were not changed. Neither failure
is reported as a passed check.

The live database still has SHA-256
`161c56ff5d457348ec6809c5e6dcc41e2dd09854d4e71cde11d12a2064d387c0`.
No script installation, evidence edit, source edit, reset or scoring took place.

## Review and next action

Please review the target guards, plan binding, backup strategy, journal states,
retry/undo and exact payload preparation. This supplements the open preserve-
edits and runtime-integration reviews, not a new per-file review workflow.

After safety review, finish the current move-map refresh and empty-directory
disposition, report-edition installation and historical-manifest checks. Then
apply the reviewed working-file batch and install these exact runtime changes
under existing owner authority. Validate live integrity and dashboard/print
behavior before proceeding to Enconet and the common release. Claude-owned
guidance and record synchronization remains Claude's responsibility.
