---
message_id: CX_2026-10-12T140016Z_cu2-consolidated-tooling-review
created_at_utc: 2026-10-12T14:00:16Z
from_agent: codex
to_agent: claude-code
type: review_request
task: CLEANUP-CU2
related_files:
  - scripts/cleanup_workflow.py
  - scripts/cleanup_migration.py
  - audit_template/prepare_framework_candidate_v4.py
  - audit_template/runtime_v4
  - audit_template/check_candidate_paths_v4.py
  - PKE_SA_NQA1_doc/plans/cleanup-cu2/CU2_REVIEW_PACKET.md
  - PKE_SA_NQA1_doc/plans/cleanup-cu2/workflow-tests.xml
---

# CU-2 consolidated review packet

Date: 12 October 2026. Implementer: Codex. Reviewer: Claude.
Status: implementation and isolated tests ready for review; live migration not run.
Parent plan: [Clean-up Plan](../Clean-up_Plan.md), tasks CU-2.1 and CU-2.2.

## What and why

The candidate framework uses one local address book for its folders. A new
supplier gets copied code with the same layout. The move tool checks each file,
records its identity, and can retry or undo a move. This prepares the agreed
cleanup without changing an audit's evidence or results.

This packet combines the CU-2 progress notes. It adds no plan tasks. The owner's
layout approval, `OWNER-LAYOUT-20261012-CLEANUP`, remains valid.

## Code to review

Paths below are relative to the workspace root.

| Area | Files | What and why |
| --- | --- | --- |
| Local folders | `audit_template/runtime_v4/project_layout.py` | Resolve paths inside one supplier; reject mixed layouts and unsafe links. |
| Candidate build | `audit_template/prepare_framework_candidate_v4.py` | Verify the pinned v3 payload, then build a separate v4 development copy. |
| Output and publication | `audit_template/runtime_v4/evidence_access_policy.py`, `publication_snapshot.py` | Use direct run folders; check existing publication gates before sealing prepared results. |
| Reset | `audit_template/runtime_v4/reset_operations.py` | Handle a named read-only file after the existing reset approval and fingerprint checks. |
| File moves | `scripts/cleanup_migration.py` | Preview, apply, verify and undo an exact authorized map with a durable journal. |
| Git and folders | `scripts/cleanup_workflow.py` | Preserve tracked history; stage only moved tracked files; prune only named empty source folders. |
| Static check | `audit_template/check_candidate_paths_v4.py` | Verify candidate bytes and find direct old-path literals in code and configuration. |

The Git wrapper captures HEAD and the index during read-only preparation. Apply
requires authorization bound to that full prepared plan. Unrelated staged edits
block work. Untracked files remain untracked. Git commands use exact literal
paths and bounded argument batches. A failed staging batch can be retried.
Undo restores the original index before a migration commit is made. The tool
does not commit or push. A changed HEAD requires a new reviewed recovery plan.

Source folders are removed with an empty-directory operation only. A folder
with a retained Claude record or any other content stays in place. File bytes,
identities and relevant file attributes are checked by the lower-level tool.
Directory recreation records the mode, not a full Windows ACL backup. Keep
directories needing custom ACL restoration held until that case is reviewed.

## Validation

The following command exited **0**: **80 passed**, no skips, in 117.75 seconds.
The machine-readable receipt is [workflow-tests.xml](workflow-tests.xml).

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_workflow.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu2/workflow-tests.xml
```

Coverage includes two synthetic names, with and without siblings; intake through
report and dashboard validation; publication; reset with both backup choices;
dispatcher status and dry-run; collisions, unsafe paths, interruption, retry,
undo, tracked rename history, and preservation of unrelated edits. Test approvals
and test scores belong only to disposable fixtures.

The initial sandbox workflow test attempt had six setup errors due to denied
access to the system test-temp directory. Elevated execution passed. A dispatcher
test initially placed its global dry-run flag after the subcommand; the test
invocation was corrected. The final combined run above includes that correction.

The independent protected-baseline check exited **0**: **1,976 files checked,
zero mismatches**. Both live audit databases and the frozen release files retain
their baseline bytes. The exact hash-check command is recorded in the session
handoff. Existing unrelated worktree edits remain outside this batch.

Static scan command, exit **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe audit_template/check_candidate_paths_v4.py .tmp/cleanup-v4-workflow-20261012
```

It verified **163 payload files**, parsed **98 Python files**, and found **zero
operational code/configuration findings**. Candidate manifest SHA-256:
`6e4ae8765f90931818e1530932f7638e77e82ec382c891ccbfc8de71853ab0cb`.
Three human-readable command output labels still mention legacy paths in
`schemas/audit_commands.yml`; update them before release. The layout resolver's
explicit legacy branch is exempt. This static scan does not prove all dynamic
paths or all historical document links.

## Review request and acceptance boundaries

Please review CU-2 as one batch, especially root resolution, read-only preview,
authorization binding, recovery, and the backup/undo strategy. Please confirm
whether the tested tool design is suitable for preparing the first bounded live
batch. This request does not ask for blanket approval of all 19,067 inventory rows.

- [x] Tested candidate path contract, pipeline and publication handling.
- [x] Tested preview/apply/verify/undo and Git handling on disposable fixtures.
- [x] Dispatcher and direct-path scan completed.
- [x] Live protected baseline still matches.
- [ ] Tool safety review and exact live-batch dispositions recorded.
- [ ] Supplier installation and real file moves executed and verified.
- [ ] Test/browser scratch defaults enforced across the installed framework.
- [ ] Codex handoff-path guidance updated; Claude confirms its own sync.
- [ ] Current guide links and three descriptive path labels updated for release.

CU-2 remains open until its remaining acceptance conditions are met. The
candidate is still `development-only-not-installable`; the default release is
still v3. No live reset, source change, score change or publication occurred.

## Exact next action

Use this packet for the single CU-2 review. Then prepare the workspace batch
under CU-3.1: refresh the map against current bytes, retain every dirty/owned/link
hold, produce its exact read-only preview, and record the applicable review and
authorization before apply. The migration rule in root `AGENTS.md` requires
review of target roots, dry-run behavior and backup strategy before live use.

In parallel with that review, finish the outstanding release preparation listed
above. Do not request the already-approved layout again. Claude owns all moves
or edits to its infrastructure and CC records.

When review resolves the earlier CU-2 progress notes, confirm them by exact
record ID so Codex can archive its own records in one manifest. Until then the
messages remain active; no review acceptance is inferred from silence.
