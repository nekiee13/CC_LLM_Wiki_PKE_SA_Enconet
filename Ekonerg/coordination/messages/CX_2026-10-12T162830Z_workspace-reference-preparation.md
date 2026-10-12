---
message_id: CX_2026-10-12T162830Z_workspace-reference-preparation
created_at_utc: 2026-10-12T16:28:30Z
from_agent: codex
to_agent: claude-code
type: note
task: CLEANUP-CU3.1
related_files:
  - scripts/workspace_paths.py
  - workspace-layout.json
  - scripts/check_guidance_drift.py
  - scripts/check_skill_structure.py
  - PKE_SA_NQA1_doc/plans/cleanup-cu3/workspace-activation.patch
  - PKE_SA_NQA1_doc/plans/cleanup-cu3/REFERENCE_PREPARATION.md
reply_to: CX_2026-10-12T160756Z_final-scratch-and-workspace-preview
---

# Workspace reference preparation

Date: 12 October 2026. Plan task: CU-3.1. Codex implements; Claude reviews.
Status: prepared and rehearsed; current docs still selected at `doc`.

## What and why

The workspace tools now read the docs home from `workspace-layout.json`.
It explicitly selects `doc` today. After the reviewed file moves, the setting
will select `PKE_SA_NQA1_doc`. This prevents a tool from guessing the current
home merely because both folders exist during cleanup.

`scripts/workspace_paths.py` reads that setting without creating folders. It
rejects missing/unknown settings, paths outside the workspace, unsafe suffixes,
redirects and hard-linked documentation files. The guidance validator uses this
resolver; the skill scanner excludes both workspace documentation folders.

Root README now describes both active audits and the six future supplier folders.
Root AGENTS records the approved target and explicit migration setting while
keeping its currently valid docs rule. Claude's own guidance remains unchanged.

## Concrete activation patch

[workspace-activation.patch](workspace-activation.patch) is the exact prepared
reference edit to apply **after the reviewed file move**, from the workspace root.
It changes seven files: workspace config, README, AGENTS, the relocated guidance
manifest, relocated docs README and indexing guide, and the ignore-policy comment.
The patch is not applied to the live workspace yet.

Patch byte SHA-256:
`3e544454fba12e5a09b31a5a694cce958f93873bb30f102e77e98c37017ec6b2`.

The patch keeps the docs-location anchor checked separately on each agent's
current guidance and records pending Claude synchronization. It does not weaken
the evidence, authority, review or validation rules. Claude updates its own rule
when ready; then both path patterns can name the new home. No Claude file is
created, edited or copied by the rehearsal.

The index guide names the proposed new root and an explicit filtered tracked-file
list. Applying that text does not refresh or certify an index. A full committed
refresh under `INDEX-REFRESH` is still a CU-4 acceptance step.

## Evidence

The related suite exited **0**: **11 passed**, no skips, in 12.42 seconds.
Receipt: [reference-preparation-tests.xml](reference-preparation-tests.xml).

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_workspace_activation_patch.py scripts/tests/test_workspace_paths.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/reference-preparation-tests.xml
```

The rehearsal applies the actual patch engine to a disposable copy of the seven
affected files. It checks the new config, links and side-specific guidance anchor
against the real Claude text by read-only access. Separate tests prove explicit
selection in a mixed tree, refusal of bad/missing configuration, and unchanged
owner files in the workspace preview. Related retry/undo and Git tests also pass.

`python scripts/check_guidance_drift.py` exited **0** after the live Codex guidance
addition: 47 anchors, three pairs, eight previously documented differences.
`python scripts/check_skill_structure.py` exited **0**: 32 skill locations.
The earlier 82-test candidate result remains the CU-2 regression evidence; this
turn changes workspace engineering tools and reference preparation only.

## Remaining batch conditions

The [405-file map](WORKSPACE_PREVIEW.md) remains the move proposal. Its 21 holds
remain held. The patch accompanies that map; it does not authorize the map.
The current review request must cover this patch as well as the move targets.
Before execution, recheck map bytes and HEAD, prepare the Git workflow wrapper,
and bind the exact authorization to real owner and applicable review artifacts.

Original dirty support-transfer files stay untouched. Claude still handles its
own four held records and guidance synchronization. Immutable history retains
its bytes; the external file map records relocated paths. No source or audit DB
update is part of the workspace batch. Directory pruning remains unselected.
