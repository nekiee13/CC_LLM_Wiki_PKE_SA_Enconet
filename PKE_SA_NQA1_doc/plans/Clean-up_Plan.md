# Clean-up Plan

Date: 11 October 2026  
Status: workspace, Ekonerg and Enconet live batches applied; remaining holds and CU-4 open
Review: owner authorized live execution and deferred Claude's pre-execution safety review; post-execution review remains pending.
Implementer: Codex. Reviewer: Claude. Owner: scope and approval decisions.  
Scope: workspace, Enconet, Ekonerg, IBE, TEKOL, IGH, IMK, KCPG, MOR, and future suppliers.

## Goal — ELI5

Put each kind of file in one clear home. The audit must work just as it does now.
Think of this as sorting a filing cabinet, not changing what its records say.
Enconet and Ekonerg will use the same layout. New suppliers will get that layout
from one tested release, not a fresh set of small fixes.

This plan does not reset an audit, run new sieving, change a score, or issue a
report. Moving a prepared report does not make it an approved release.

## Current facts and limits

- Live Git baseline for this plan: `7c85bbd`, branch `main`.
- Root has `doc/`, `reset-plans/`, several `pytest-*` folders, and
  `ekonerg-reset-rk6wsybf/`.
- Both active audits have `out/`, `outputs/`, `manifests/`, `derived/`,
  `benchmarks/`, and `handoffs/`. Ekonerg also has `backup/` and `work/`.
- Six future-supplier folders exist. They are clean v2 scaffolds. The default
  reusable release is v3. A layout change needs a new release, proposed as v4.
- Some paths are fixed in code. Examples are reset ledgers, package output,
  handoff publication, and the generated coordination board.
- Shared code/docs indexes are stale. Their July 2026 baseline is `62a0251`.
  This plan uses live paths instead. No index refresh is claimed.
- Several files already have owner or other-agent changes. These are not
  cleanup permission to overwrite them. Record them in the move preview.
- The reset scratch folder denied normal read access. An elevated read listed
  no children. Its name is not proof that it holds a real reset tool.
- This is a checked top-level inventory, not a claim that every file has been
  classified. Task CU-1.1 completes that check before any move.

## Proposed layout

`outputs` is the single result folder. `work` holds working records, including
records that must be kept. A file is not disposable just because it is in `work`.

```text
03_PKE_SA_NQA1/
  AGENTS.md, CLAUDE.md, README.md, Git/config files
  .agents/, .claude/            existing agent infrastructure; do not move
  PKE_SA_NQA1_doc/
    plans/Clean-up_Plan.md
    reset-plans/
    framework-reuse/
    support-transfer/
    ...existing workspace guides
  scripts/                     workspace tools
  audit_template/              versioned, tested release source
  audit_archives/              retained audit history
  .tmp/                        workspace test scratch; ignored by Git
  <Supplier>/
    .agents/, .claude/          where present; keep their current homes
    incoming/                  owner document drop-off; keep unchanged
    raw/                       registered source files; keep unchanged
    db/                        audit database; keep here
    docs/
      plans/                   plans and plan-status notes
      ...guides and examples
    work/
      benchmarks/              calibration and golden fixtures
      derived/                 source/chapter working artifacts
      manifests/               source, approval and validation ledgers
      decisions/               ADRs and audit decisions
      reviews/                 review reports, not message queues
      backup/                  existing backups only; no new backup mandate
      validation/              test logs and browser checks
      migrations/              previews, move maps and rollback journals
      bootstrap/               new install/upgrade receipts
      archive/                 older working artifacts needing retention
    coordination/
      messages/, archive/, claims/, BOARD.md, TEAM_PROTOCOL.md
      handoffs/                immutable session records
    outputs/
      RUN-<id>/
        dashboard_light.html
        dashboard_dark.html
        report.md
        ...report/PDF/data and release records, when present
        revisions/             only if this run has distinct saved editions
      archive/                 old outputs with no proved run assignment
    scripts/, schemas/, sieving/, templates/, tests/, tools/
    wiki/                      audit knowledge and small result pointers
    .tmp/                      supplier-local scratch; ignored by Git
    AGENTS.md, CLAUDE.md, HANDOFF.md, project-state.yml, config files
```

The runtime and evidence structure inside `sieving/` stays as-is in this phase.
Do not scatter its code, prompts or DATA into new folders just to reduce names.
Existing `vendor/` design assets stay in place unless the inventory proves a
better safe home. Empty scaffolds need the same path contract, not fake audit
records or a populated database.

### Move map

| Existing home | Proposed home | Rule |
| --- | --- | --- |
| Root `doc/` | `PKE_SA_NQA1_doc/` | Move tracked docs with history; merge with this new plans folder safely. |
| Root `reset-plans/` | `PKE_SA_NQA1_doc/reset-plans/` | Keep JSON bytes and approval history. Old plans may be history, not runnable plans. |
| Root `Transition_template_Plan.md` | `PKE_SA_NQA1_doc/plans/` | Move the plan; fix current references. |
| Root `pytest*`, reset/test scratch | Root `.tmp/` or supplier `.tmp/` | Classify first. Do not treat unknown files as trash. |
| `benchmarks/`, `derived/`, `manifests/`, `backup/` | Supplier `work/`, same subfolder name | Preserve bytes, hashes, source links and read-only flags. |
| `decisions/` | Supplier `work/decisions/` | Keep ADR identities and all decision history. |
| `docs/reviews/` | Supplier `work/reviews/` | Messages remain under `coordination/`. |
| `handoffs/` | Supplier `coordination/handoffs/` | Preserve record bytes; update publisher and pointer handling first. |
| Plans in root or supplier docs | Root or supplier `docs/plans/` as above | Identify plans by purpose, not filename alone. Do not move every guide. |
| `out/` and `outputs/` | Supplier `outputs/` | Results go under their real run; logs go under `work/validation/`. |
| `outputs/candidates/evidence_access/<run>/...` | `outputs/<run>/...` | Keep prepared/approved state in metadata, not extra folder names. |
| Required theme-choice landing page | No required landing page | Each dashboard opens on its own with all needed data embedded. |

`ekonerg-reset-rk6wsybf` is not assumed to be executable tooling. If it is
scratch, place retained content in `Ekonerg/.tmp/`. If it contains a real tool,
place that code in `Ekonerg/tools/`. Record the result before moving it.

## Ground rules

- No blanket delete, reset, global search-and-replace, or overwrite on collision.
- Do not change incoming/raw bytes, IDs, editions, crumbs, quotes, scores, run
  identities, findings, approval decisions, or gate states.
- A necessary stored-path change is a data migration. Preview it, review it,
  record before/after values, and apply it only with explicit authority.
- Keep immutable messages, handoffs, frozen plans and release records unchanged.
  Use a move map to resolve their old links. New records use new paths.
- Codex does not move or edit `CC_*`, `CLAUDE.md`, or `.claude/`. Claude handles
  its own records and adapters. A shared folder containing those files cannot
  be moved wholesale by Codex.
- Workspace and supplier `.agents/` and `.claude/` folders stay where they are.
  Both agents update their own internal path references when the new contract
  is ready. User-global skill folders also stay in their current homes.
- Keep v1/v2/v3 releases intact. Publish a new layout release instead.
- Existing no-local-backup choices stay in force. Git is not a backup of ignored
  databases or untracked files. Retain those files through reversible moves.
- Remove only proved scratch under an approved exact list. Otherwise relocate
  it and keep it. Do not change broad permissions to force cleanup.
- Test first, then implement, then move. One review per coherent batch is enough.

## Epic CU-1 — Agree on the homes and protect the records

**What:** Make an exact move list and record the current audit state.  
**Why:** We must know what each box holds before we move it.

### Task CU-1.1 — Inventory files, owners and path users

**What:** Scan all eight supplier folders and the workspace. Class each file as
source, code, result, working record, history, or scratch. Find code, tests,
configs, DB fields, JSON, ledgers, Markdown and browser links using old paths.  
**Why:** A tidy folder is not useful if its tools can no longer find it.

Acceptance criteria:

- [ ] Inventory includes tracked, ignored and untracked files, empty folders,
      access failures, nested Git stores, and both agents' ownership.
- [ ] A machine-readable map lists old path, new path, owner, byte hash,
      retention rule, path users and any collision.
- [ ] No unknown file is marked for deletion. No borrowed run ID is invented.
- [ ] Dirty or Claude-owned files have a clear hold or owner-coordinated move.
- [ ] No path under incoming/raw is scheduled for a content change.

### Task CU-1.2 — Freeze a baseline and approve one layout

**What:** Capture hashes, audit counts, scores, gates, links and release status.
Confirm the target layout and the few exceptions.  
**Why:** These facts show that cleanup did not change the audit.

Acceptance criteria:

- [ ] Both audits have baseline receipts from their live read-only data.
- [ ] Receipts cover full source/chapter hashes, active generations, evidence
      links, approval records, scores, outputs and immutable releases.
- [ ] Owner confirms `outputs`, the proposed `work` contents, and retention.
- [ ] Claude reviews the plan/path map and identifies its own required moves.
- [ ] Existing publication status and no-backup decisions remain separate.

Epic acceptance: every proposed move has a known owner and an undo path.

## Epic CU-2 — Make the tools ready before changing paths

**What:** Give all scripts one tested path contract and a safe move tool.  
**Why:** Changing one address book is safer than patching each supplier by hand.

### Task CU-2.1 — Add a local, shared layout contract with tests first

**What:** Add a company-neutral path resolver to the release source. Copy its
tested code and layout config into each supplier. Route intake, chunking,
sieving, approvals, reset, reports, exports, handoffs and tests through it.  
**Why:** A future supplier should need setup choices, not new path fixes.

Acceptance criteria:

- [ ] Write failing tests for the new homes before changing runtime paths.
- [ ] Normal commands work from project root and workspace root.
- [ ] Runtime reads only local supplier code/data; no sibling imports.
- [ ] Two synthetic suppliers, one with spaces and one with non-ASCII letters,
      pass with and without a sibling folder. The sibling stays unchanged.
- [ ] Missing or mixed layouts fail clearly; they do not select another audit.
- [ ] Reset preview uses the new paths and excludes incoming, code, plans and
      coordination history. Test reset apply only on disposable fixtures.
- [ ] Test and browser profile scratch always uses `.tmp/`, not root `pytest*`.
- [ ] When the handoff path contract changes, Codex updates its own handoff
      skill and Claude updates its own equivalent. Record both confirmations;
      until then, cross-agent skill synchronization remains pending.

### Task CU-2.2 — Build preview/apply/verify/undo migration tooling

**What:** Make a script that checks the move map, performs safe moves, and logs
what happened. It must support a safe rerun or undo after interruption.  
**Why:** A long list of manual moves is easy to get wrong.

Acceptance criteria:

- [ ] Default preview writes no project files; apply needs a reviewed map.
- [ ] Tests cover collisions, changed files, access denied, partial failure,
      interrupted runs, safe retry, undo and paths outside the chosen root.
- [ ] Block unsafe symlinks, junctions, reparse points and hardlinks.
- [ ] Resolve exact absolute paths inside the selected root before a move or
      delete. Use native PowerShell operations with literal paths where needed.
- [ ] Tracked moves preserve Git history. Untracked moves preserve file bytes
      and relevant permissions, with a durable hash journal.
- [ ] Never overwrite a destination or delete a file changed by someone else.
- [ ] Undo restores the captured layout without deleting unrelated new files.
- [ ] Old signed/immutable records remain unchanged. An external move map
      resolves their paths; it is not presented as their original manifest.

Epic acceptance: isolated migration and rollback tests pass before live use.

## Epic CU-3 — Clean the workspace and align both active audits

**What:** Carry out the reviewed map in three bounded batches.  
**Why:** This gives us clear stop points without endless per-file tasks.

### Task CU-3.1 — Clean workspace docs and scratch

**What:** Merge `doc` into `PKE_SA_NQA1_doc`, move reset plans and root plans,
and relocate known test scratch. Fix current guides, profiles and tool paths.  
**Why:** The root should show projects and tools, not past test runs.

Acceptance criteria:

- [ ] All workspace guides have one canonical home; no duplicate `doc` tree.
- [ ] `reset-plans` and root plans have the homes in the move map.
- [ ] Root `pytest*` and the reset scratch folder are gone from the root after
      safe relocation, or are named blocked exceptions with reasons.
- [ ] Existing dirty support-transfer files are preserved and coordinated,
      never reverted or silently swept into a broad commit.
- [ ] README, AGENTS, guidance-pair paths, ignore rules and index profiles use
      the new docs home. Claude updates its own guidance separately.
- [ ] No scratch is moved into `scripts` just to hide it from view.

### Task CU-3.2 — Move Ekonerg working records and simplify results

**What:** Apply the shared layout to Ekonerg. Put working records in `work`,
plans in `docs/plans`, handoffs in coordination, and results in run folders.  
**Why:** The owner can find audit results without walking through tool folders.

Acceptance criteria:

- [ ] All mapped folders move; `HANDOFF.md` and the board point to the new
      handoff home. New publication and validation work there.
- [ ] One `outputs` tree replaces `out` plus `outputs`. Test screenshots/logs
      go to `work/validation`; reports and dashboards go to their run folder.
- [ ] No active result requires `candidates/evidence_access` nesting.
- [ ] Colliding editions get explicit retained revisions, not overwrites.
- [ ] Each light/dark HTML includes its data, chapter text, CSS and scripts.
      It works offline after copying that single file into an empty folder.
- [ ] Crumb clicks open the full linked chapter; all 18 criteria, scores,
      explanations, matrix, filters, sort, expand, shortcuts and print remain.
- [ ] No required theme-selection page remains in the owner delivery.
      Optional JSON, PDF and Markdown files do not become HTML dependencies.
- [ ] Old prepared packages and review records are retained as history.
      Their status is not silently changed or their hash manifests rewritten.

### Task CU-3.3 — Apply the same layout to Enconet

**What:** Use the same tool and contract for Enconet, including
`work/decisions`. Keep its own source set and audit records separate.  
**Why:** The owner should not learn a different tree for each audit.

Acceptance criteria:

- [x] Enconet follows the same paths and output rules as Ekonerg.
- [x] Frozen plans and ADRs keep their content, identifiers and hash history.
- [x] Existing released packages remain verifiable at their original bytes;
      relocation is documented outside their frozen manifests.
- [x] Wiki result links, release verification, reset preview, handoffs and
      audit command routing work at the new paths.
- [x] Incoming/raw, active evidence, scores, gates and approved editions match
      the baseline. No Ekonerg evidence enters Enconet.

Epic acceptance: both audits work and their protected baseline facts match.

## Epic CU-4 — Make this the standard for every supplier

**What:** Release the layout once, update empty scaffolds, and prove completion.  
**Why:** Cleanup should solve the next audit too, not only these two folders.

### Task CU-4.1 — Publish a clean layout release and update six scaffolds

**What:** Build proposed v4 from the tested current tools, including the
standalone dashboard rule. Preview and apply the layout to IBE, TEKOL, IGH,
IMK, KCPG and MOR without starting their audits.  
**Why:** Every supplier needs the same shelves but its own future records.

Acceptance criteria:

- [ ] v1/v2/v3 and existing addon hashes stay intact. New release has its own
      version, manifest, tests, install instructions and upgrade receipts.
- [ ] Six per-supplier previews show all changes and preserve owner content.
- [ ] All six get local code copies and the shared layout; no audit database,
      source, crumb, score, active prompt or approval is copied from an audit.
- [ ] Unknown supplier names work without an allowlist or per-name patch.
- [ ] The complete synthetic intake-to-report test runs in the new layout.
- [ ] A second install or migration is safe and does not create duplicate trees.

### Task CU-4.2 — Run final checks and hand over a clean tree

**What:** Run the required suites, inspect both dashboards, check all path
links and update the docs/indexes. Deliver one short closure report.  
**Why:** A clean-looking tree must also be a working, safe framework.

Acceptance criteria:

- [ ] Each active audit passes its required aggregate checks. Record each
      exit code and every phase-based skip; do not report skips as passes.
- [ ] Enconet full isolated regression, the applicable Ekonerg regression,
      migration/undo tests and reusable-release suites pass.
- [ ] New-output tests prove standalone light/dark use, all crumb/chapter
      links, mobile layout, keyboard access, white print and real PDF output.
- [ ] Compare all evidence, approval, score and source baseline facts.
      Only reviewed stored-path changes may differ.
- [ ] Current docs/code contain no unapproved old-path dependencies.
      Historical old links resolve through the retained relocation map.
- [ ] Coordination and handoff validation pass. Guidance drift checks pass
      after Codex guidance updates; Claude sync is stated honestly.
- [ ] Refresh shared indexes from committed state under one `INDEX-REFRESH`
      claim. Structural rename needs full refresh and verification, not a
      blind incremental refresh. Never re-index Claude-owned guidance.
- [ ] Root has no stray test directories; all eight suppliers pass the same
      structural check. Unused optional folders need not contain dummy files.
- [ ] Closure report lists moves, retained history, exact hashes, test results,
      any approved exceptions and the new dashboard/report entry paths.

Epic acceptance: one versioned layout works for active, known and unknown audits.

## Execution order and stop rules

1. CU-1: finish inventory, baseline and one owner/reviewer layout decision.
2. CU-2: tests first, then path contract and migration tooling. Review once.
3. CU-3: workspace, Ekonerg, then Enconet. Verify each batch before the next.
4. CU-4: release, six scaffolds, full checks and one final handoff.

There are four epics and nine tasks. Do not add per-file slices. A failed test is
fixed within its task unless it reveals a real scope or authority issue.
No new audit scoring, UI redesign, data model redesign or sieving is included.

Stop if a hash differs, a destination collides, a record has an unknown owner,
or permissions block safe handling. Do not loosen the checks to keep moving.

## Layout decision and remaining live-move conditions

The owner has confirmed the proposed layout under
`OWNER-LAYOUT-20261012-CLEANUP`. The confirmed choices are:

1. Use `outputs` as the one result folder and the `work` homes shown here.
2. Keep unknown/history artifacts; remove only named, proved scratch if approved.
3. Claude handles its own records affected by folder moves. Immutable history
   gets an external path map rather than rewritten content.

See [owner decision](cleanup-cu1/OWNER_LAYOUT_APPROVAL.md). CU-2 code/tool
preparation is next. Reviewed targets, tool safety and held-file dispositions
remain required before live application. No existing project folder has been
renamed, reset or deleted.

## Review record

Claude's `CC_2026-10-11T221253Z_cleanup-plan-review` confirms the plan has no
safety conflict and no objection to CU-1 as scoped. Claude will update its
own workspace/supplier guidance, skill references and global handoff contract
when the new paths are ready. Codex confirms those agent folders stay put.
This is not approval of a file move map, migration code or live application.
The combined CU-1 packet review found no safety objection. Owner layout
confirmation is recorded. Later CU-2 tooling and reference preparation reviews
were accepted by Claude. The owner then authorized live cleanup execution.

## Live execution update — 12 October 2026

CU-3.1's first reviewed workspace batch moved 405 files and activated the seven
reference changes. Apply, repeat apply and pre-activation verification passed.
Post-activation checks prove 402 unchanged moved files and three exact authorized
guide edits, with all 1,976 protected baseline files unchanged. Eleven related
tests passed. See [live workspace result](cleanup-cu3/LIVE_WORKSPACE_RESULT.md).

The 21 held records and old directories remain explicit exceptions. Claude
guidance/skill synchronization and owned-record moves remain pending. CU-3.1 is
not fully closed; Ekonerg/Enconet live moves, six scaffolds, v4 release and final
index refresh remain under CU-3/CU-4. Owner authority is recorded at
[live authorization](cleanup-cu3/OWNER_LIVE_AUTHORIZATION.md).

CU-3.2's current-runtime integration now has zero direct old-path findings.
The cleanup regression suite passed 92 tests, and nine isolated Ekonerg checks
passed without changing checked live files or the database. The fresh proposal
has 920 moves. Ekonerg has not moved or activated v4. Runtime/tool safety review
and the checked installation/recovery procedure remain within CU-3.2; no new
task is added. See [integration review](cleanup-cu3/EKONERG_INTEGRATION_REVIEW.md).

CU-3.2 now also has a bound runtime installer with byte-preserving originals,
interruption retry and guarded undo. The exact 39-file preparation and read-only
preview pass. The common suite passed 106 tests; the final activation guard
passed its 16-test focused suite. No live Ekonerg installation has occurred.
See [installation review](cleanup-cu3/EKONERG_INSTALLATION_REVIEW.md).

CU-3.2's refreshed proposal covers 922 files with no unmapped working files.
Two frozen release manifests pass an isolated relocation rehearsal (16 and
eight references). The common suite passed 115 tests; final manifest/directory
guards passed 12 focused tests. Two empty-folder moves are explicitly proposed,
not applied. Directory permission recovery and pending safety reviews still
precede live Ekonerg activation. See
[final preflight](cleanup-cu3/EKONERG_FINAL_PREFLIGHT.md).

CU-3.2 now has tested native directory recovery: retain original empty trees
instead of pruning/recreating them. The exact proposal covers ten trees and
128 native identity/permission witnesses, bound to the refreshed 923-file map.
The common suite passed 124 tests; final directory tests passed nine. Live
directory preview correctly refuses to proceed while files remain. Safety review
still precedes live application. See
[native directory review](cleanup-cu3/EKONERG_NATIVE_DIRECTORY_REVIEW.md).

Owner explicitly deferred Claude's pre-execution safety review, and CU-3.2's
existing bundle was applied: 924 file moves, 592 original tracked blobs retained,
nine native directory trees and 39 runtime/configuration installations. The
live aggregate, integrity, frozen-manifest and both dashboard/PDF checks pass;
125 regression tests pass. One empty `outputs/candidates` tree remains unchanged
after Windows denied its rename. Post-execution Claude review remains pending.
See [actual live sprint result](cleanup-cu3/EKONERG_LIVE_SPRINT_RESULT.md).

CU-3.3's live Enconet batch is applied: 17,752 file moves, 463 original tracked
blobs retained, ten original empty directory trees archived with native permissions,
and the verified local runtime activated. All 19 live phase checks pass; all 486
protected hashes match. The score remains 80.6%. The frozen publication's twelve
artifacts pass relocation verification, and reset preview passes without applying a
reset. Local handoff routing and publication pass; the new immutable record is
under `coordination/handoffs`, with no old handoff home recreated. The full
historical regression and release/scaffold rollout remain
under the existing CU-4 final checks. No task was added. See
[Enconet live result](cleanup-cu3/ENCONET_LIVE_SPRINT_RESULT.md).
