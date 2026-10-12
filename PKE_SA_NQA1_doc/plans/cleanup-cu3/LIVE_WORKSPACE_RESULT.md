# Live workspace cleanup result

Date: 12 October 2026. Plan task: CU-3.1.
Status: reviewed 405-file batch applied and verified; retained holds remain.
Owner authority: [OWNER_LIVE_AUTHORIZATION.md](OWNER_LIVE_AUTHORIZATION.md).

## What changed

All **405 selected files moved** to the reviewed homes. Git tracks **299 renames**;
the other 106 files retain their untracked/ignored status. The repeat apply passed
without duplicate moves. The durable move journal ends with complete records.

Workspace documentation now uses `PKE_SA_NQA1_doc`. The reviewed activation patch
updated seven current-reference files, including the config, navigation, Codex
guidance and index profile. Claude guidance remains pending for Claude to update.
No active supplier runtime has adopted v4 in this workspace batch.
Two Codex-owned Enconet guide pointers now name the relocated workspace indexing
and skills guides. No Claude-owned counterpart was edited.

## Exact execution records

Records are under [live-workspace-20261012](live-workspace-20261012/).

- `workflow-plan.json.zip`: exact map, application HEAD/index and tracked sources.
- `authorization.json`: owner and actual Claude review paths with raw-byte hashes.
- `before-receipt.json`: original dirty/held hashes and patch identity.
- `patch-before.json.zip`: original bytes for the seven reference files.
- `move-journal.jsonl`: sealed start, file identities, every move and completion.
- `move-verify-before-activation.json`: all 405 moved with original bytes/identities.
- `post-activation-receipt.json`: final exact-patch, retained-file and baseline checks.
- `post-activation-tests.xml`: 11 related tests passed, no skips.

Application HEAD: `597cbd7c5bb780ce0e9100038f763aeaa996a6ca`.
Exact workflow plan canonical SHA-256:
`e996c26fc8d29737c6b1be7129cdb6c0745f6f55306a2be24870d8975a10dc61`.
The workflow augments the reviewed file map with Git state; its file rows remain
the same 405 reviewed rows. Authorization is bound to that full workflow hash.

## Validation

Initial apply and repeat apply both exited **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe scripts/cleanup_workflow.py --root C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1 --plan PKE_SA_NQA1_doc/plans/cleanup-cu3/live-workspace-20261012/workflow-plan.json.zip --mode apply --journal PKE_SA_NQA1_doc/plans/cleanup-cu3/live-workspace-20261012/move-journal.jsonl --authorization PKE_SA_NQA1_doc/plans/cleanup-cu3/live-workspace-20261012/authorization.json
```

Move-only verification exited **0** with elevated read access:

```text
C:/xPY/vEnv/WikiEnconet/python.exe scripts/cleanup_migration.py --root C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1 --plan PKE_SA_NQA1_doc/plans/cleanup-cu3/live-workspace-20261012/workflow-plan.json.zip --mode verify --journal PKE_SA_NQA1_doc/plans/cleanup-cu3/live-workspace-20261012/move-journal.jsonl
```

The first sandbox verify exited **1** because it could not read a retained cache
file. Elevated verification passed. Permissions were not changed to bypass it.

After verification, the pinned activation patch was applied through the patch
engine. Final checks independently replayed that patch in a disposable copy of
the saved original bytes and compared all seven resulting files to live hashes.
Results: **402 moved files retain original bytes and identities**; **3 moved
guides exactly match their authorized edits**. All 405 original paths are absent.
The move-only receipt precedes these three edits and is not a claim that the
old-content verifier still passes after activation.

Final checks: **1,976 protected files unchanged**, **7 original dirty files
unchanged**, **8 safe regular held-file hashes unchanged**, **21 holds retained**.
Unsafe/agent-owned held paths remain in place; they were not moved by the tool.
The check precedes the normal append-only session-handoff log event.

The related suite exited **0**, **11 passed** in 12.72 seconds:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_workspace_activation_patch.py scripts/tests/test_workspace_paths.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/live-workspace-20261012/post-activation-tests.xml
```

The patch rehearsal now reads the saved before-bytes after migration, instead of
requiring the old doc files to remain live. Guidance drift also exited **0**:
47 anchors, three pairs, nine documented differences, including pending Claude
docs-home synchronization. Skill structure exited **0**: 32 locations.

## Retained work and recovery

The 21 holds remain: four existing edits, four Claude-owned records, six pytest
redirect/hardlink entries and seven rendered guidance files requiring ownership
classification. Old directories, including empty `reset-plans`, were not pruned
by this batch. The old `doc` tree is retained holds, not a second active docs home.
The reset scratch folder remains held. Do not report CU-3.1 fully closed yet.

Before activation, the tested undo command could restore the file layout and Git
index at the captured HEAD. After activation, restore and verify the captured
reference bytes/identity metadata before using the move-only undo; after commit,
recovery needs a new reviewed plan for that HEAD. Never run stale undo against
changed current files. The original bytes, journal witnesses and Git history are
retained for recovery; no live undo was attempted.

The external reviewed map records history relocation. Frozen records were not
rewritten. Shared indexes remain stale; a full refresh after structural changes
and commit remains under CU-4 and an `INDEX-REFRESH` claim.

## Next action

Claude can now update its own workspace and nested guidance, handoff skill and
held records, preserving bytes where required. Codex then completes retained
workspace dispositions and proceeds with Ekonerg's bounded live batch under the
existing owner cleanup authorization. Supplier evidence, gates and results stay
separate. No repeat approval of the overall layout is needed.
