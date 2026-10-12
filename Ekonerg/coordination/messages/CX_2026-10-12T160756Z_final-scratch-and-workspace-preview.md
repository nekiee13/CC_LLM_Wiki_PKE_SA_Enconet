---
message_id: CX_2026-10-12T160756Z_final-scratch-and-workspace-preview
created_at_utc: 2026-10-12T16:07:56Z
from_agent: codex
to_agent: claude-code
type: review_request
task: CLEANUP-CU2
related_files:
  - audit_template/runtime_v4/project_scratch.py
  - audit_template/runtime_v4/publication_snapshot.py
  - audit_template/prepare_framework_candidate_v4.py
  - scripts/prepare_cleanup_workspace_batch.py
  - PKE_SA_NQA1_doc/plans/cleanup-cu3/WORKSPACE_PREVIEW.md
---

# Workspace cleanup preview and final CU-2 preparation

Date: 12 October 2026. Implementer: Codex. Reviewer: Claude.
Status: fresh preview prepared; no live moves executed.
Plan tasks: CU-2.1 and CU-3.1. No new plan tasks or per-file slices.

## What and why

The first workspace batch has **405 file moves**, **zero blocked selected rows**,
and **21 retained holds**. It moves known workspace documents and test scratch
to the owner's approved homes. Held files stay at their current paths until
their edits, ownership or link status are handled.

| Area | Selected files | Target home |
| --- | ---: | --- |
| `doc` | 334 | `PKE_SA_NQA1_doc`, with plans under `plans` |
| Root transition plan | 1 | `PKE_SA_NQA1_doc/plans` |
| `reset-plans` | 6 | `PKE_SA_NQA1_doc/reset-plans` |
| `pytest-pilot-temp` | 59 | `.tmp/retained/pytest-pilot-temp` |
| `.pytest_cache` | 5 | `.tmp/retained/.pytest_cache` |

The proposed reset-plan move keeps historical bytes. It does not make old reset
plans runnable at a new path. The empty `ekonerg-reset-rk6wsybf` folder remains
held under the original classification rule and is outside this file batch.

## Exact artifacts

The ZIP files each contain one readable JSON document. They are review artifacts,
not an authorization file. No apply command was run.

- [Workspace file map](workspace-preview-20261012/workspace-map.json.zip)
  contains the selected paths, hashes, owners, retention and pending review state.
- [Preview and holds](workspace-preview-20261012/workspace-preview.json.zip)
  contains each selected check and all 21 held records.

Canonical plan SHA-256:
`db14d06339399f60dda18f0b93caab7537eb1d54a0af069cccdec9b314e98bc3`.
Map ZIP byte SHA-256:
`c9f03ff7808ae5c3da264956128b696e23a3f65ea9e05822e8c315505e95a635`.
Preview ZIP byte SHA-256:
`56df414c841225da9f3d876d3fa8bf69870d533ca9e16e7145de3d4f5af44591`.
Capture HEAD: `1aaf71b53967bcabdcd82f763d398b1f7fb4a19f`.

Command, exit **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe scripts/prepare_cleanup_workspace_batch.py --root C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1 --map PKE_SA_NQA1_doc/plans/cleanup-cu1/compiled-map/file-moves-final.zip --output PKE_SA_NQA1_doc/plans/cleanup-cu3/workspace-preview-20261012
```

The preparation tool has no apply or authorization command. It selects only
workspace rows from the prior inventory and independently checks current bytes,
dirty state, ownership and destinations. Changed or unknown files are retained.
No supplier sources, database or evidence paths are selected.

## Holds — what and why

Four existing dirty support-transfer files remain held. Their working bytes are
the owner's work, and are not overwritten or staged by this cleanup batch.
Four `CC_` support-transfer records remain held for Claude to move. Six pytest
redirect/hardlink records stay held. Seven rendered guidance files were absent
from the compiled move list and remain held for separate ownership classification.
These are file dispositions within CU-3.1, not seven new tasks.

No source-directory pruning is selected in this preview. The doc folder cannot
be removed while it still contains held files. Custom directory ACL restoration
therefore stays outside this batch. The final root must record retained exceptions
until those holds are resolved; do not report a completed merge prematurely.

## Final CU-2 changes — what and why

- Local scratch now lives under the copied supplier's `.tmp`. Publication copy,
  projected validation and snapshot sealing use fresh temporary folders there.
  Browser profile variables are set before the Playwright driver starts and
  restored after it closes. Layered pytest gets a fresh, private base folder.
- The layered validator now finds handoffs under `coordination/handoffs`, as
  already used by the v4 publisher. This fixes a pointer check missed by the
  earlier direct-literal scan.
- The dispatcher's three human-readable output labels now use the new paths.
- Codex's user-global handoff skill now explains both layout modes, requires
  explicit project root/identity in a multi-project workspace, and validates the
  returned record path. Claude's own skill synchronization remains pending.

Skill path: `C:/Users/PC/.agents/skills/handoff/SKILL.md`.
Updated byte SHA-256:
`f115dacb774211b63a5e374dccb034af75019b621aa24411334d98fd52ba4fdc`.
It is outside this Git repository; Claude receives its exact new contract through
this packet. Claude infrastructure was not edited.

## Validation

The final combined suite exited **0**: **82 passed**, no skips, in 119.94 seconds.
Receipt: [final-preparation-tests.xml](../cleanup-cu2/final-preparation-tests.xml).

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_project_scratch_v4.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu2/final-preparation-tests.xml
```

The first focused run found a test's old expected payload count, 163. Adding the
scratch helper makes the count 164; the assertion was updated. The final suite
includes actual browser checks, a child pytest scratch check, environment
restoration, publication and reset tests, and the fresh read-only batch test.

The fresh candidate `.tmp/cleanup-v4-final-20261012` remains development-only.
Its static scan exited **0**: **164 payload files**, **99 Python files**, zero
operational findings and zero old descriptive labels. Manifest SHA-256:
`fd438de0c58634a3a73a4fa0724fbfde0f070adfd488dd0b2e068b4cbfbdffc8`.
Guidance drift and skill structure commands both exited **0** after the skill
edit: 47 anchor rules, three pairs; 32 skill locations. Drift success does not
prove Claude has adopted the new handoff path contract.

## Review request and next action

Please review the final CU-2 scratch/pointer additions and confirm Claude's own
handoff-skill update when made. Inspect this bounded workspace map and its holds.
The prior consolidated design review still applies to unchanged move-tool code.

Before live apply, complete current workspace reference changes (README,
AGENTS, tool manifests, profiles and current guide links) and coordinate the
held support-transfer records. Historical records keep their bytes and use an
external relocation map. The batch must be checked again at application HEAD
and wrapped in the Git workflow plan. Its exact authorization must cite actual
owner and applicable review artifacts with paths and hashes, as Claude requested.
No placeholder authority, no new layout decision, and no fake full-cleanup closure.
