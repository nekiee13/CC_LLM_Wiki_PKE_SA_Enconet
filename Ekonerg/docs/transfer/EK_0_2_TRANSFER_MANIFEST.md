# EK-0.2 — Clean transfer manifest

Status: proposed; awaiting Claude review. No framework files have been copied.

Implementer: Codex. Reviewer: Claude. Date: 2026-09-29.

## What this package does

This is the packing list for the new workshop. It names every file in the old
workspace and says what may happen to it. It does not pack or move anything.

The source is commit `9f20430c95334daa4c3cedb7ee71b002bd3be739`.
All 1,963 tracked files in that commit are listed. This wide inventory makes
exclusions visible, including old records and unrelated support experiments.
Untracked files, ignored files, the live database, and the local corpus are not
sources. The checker reads Git blobs, not working files.

The approved plan is version 1.1 at `c7d144d`. Claude closed EK-0.1 in
`CC_2026-09-29T110929Z_ekonerg-plan-v11-approve`. That approval does not approve
this new manifest. EK-0.2 stays open until Claude reviews this package.

## Files to review

- [transfer-manifest.json](transfer-manifest.json): one row for each source file.
  Each row gives its path, proposed destination, Git blob ID, byte count, SHA-256,
  purpose, treatment, and required work.
- [dependency-scan.json](dependency-scan.json): import and file-reference evidence
  for all 275 selected source items. It also shows root-path assignments and
  content warning flags. It is a navigation aid, not proof that a program works.
- [DEPENDENCY_REVIEW.md](DEPENDENCY_REVIEW.md): how each dependency group will be
  handled, including old inputs that must not transfer.
- [VALIDATION.md](VALIDATION.md): commands, test results, failures, and limits.
- [transfer_manifest.py](../../tools/transfer_manifest.py): the local inventory
  builder and checker. It has no framework-copy or apply command.

## What each treatment means

| Treatment | Files | What & Why |
|---|---:|---|
| Copy | 1 | The generic handoff schema is source-free. Its bytes may stay the same. |
| Adapt | 225 | Keep the useful tool or rule, but review and change its paths or content before use. |
| Recreate | 49 | Make a new, empty or synthetic record. Old bytes must not become the new record. |
| Exclude | 1,688 | Do not transfer these bytes. They are evidence, history, other-project material, or retired tools. |

An **adapt** row is not permission to copy a file unchanged. Later tasks must
record a source hash, a reviewed change, a destination hash, and test evidence.
The new file must contain no real document excerpts or inherited approvals.
An **exclude** row has no destination. A **recreate** row names the future file,
not a file that exists or is ready now.

All 161 selected Python files are marked adapt. This keeps audit code, support
code, library code, and tests local while avoiding a false claim that any file
is already safe after relocation. The source purpose is taken from its module
description when one exists. Content flags are prompts for review, not findings
of contamination and not a clean-content certificate.

## Required support copies

The five active workspace tools and all four workspace support tests are included.
They will live under `Ekonerg/scripts/` and `Ekonerg/scripts/tests/`.

| Tool | What must change or be proved |
|---|---|
| `agent_coord.py` | Set `ROOT`, `COORD`, and `HANDOFF_POINTER` to the local project. Check every derived message, claim, archive, and board path. |
| `run_validation.py` | Adapt `WORKSPACE`, `ENCONET`, and `SIEVING`. Review every command and working folder, local test path, and fresh manifest input. |
| `make_handoff.py` | Review `WORKSPACE`, `DEFAULT_PROJECT`, `SCHEMA_PATH`, default `--project-id`, and Git-root lookup. Use the local schema and handoff files. |
| `check_guidance_drift.py` | Read the new local `doc/GUIDANCE_PAIRS.json`. Do not depend on Enconet guidance or claim Claude is synced before it is. |
| `check_skill_structure.py` | Keep project and workspace scopes distinct. Use local checks by default; test scope rules without reading sibling audit data. |

The project tools `audit_command.py` and `session_continuity.py`, plus the command
registry, also need review. Their shared-workspace paths must not call the old
handoff helper. A Git-root query is not permission to import shared scripts.

Unchanged relocated tools can target `Ekonerg/Enconet`. A partial root change can
target the sibling `Enconet`. EK-1.2 must test both mistakes in fake projects.
The tests must prove intended Ekonerg output and preserve the fake sibling's
file list, bytes, and file change times. They must never mutate the live audit.

## Fresh records, not copied approvals

The following schema-folder files are recreated, not copied:

- `evidence_access_operations.yml`: new local commands and fresh rehearsal values.
- `evidence_access_release_candidate.yml`: no old run, source hash, or count.
- `evidence_access_review_protocol.yml`: no inherited reviewer verdict.
- `evidence_access_uat.yml`: no inherited Owner decision, crumb, or artifact hash.
- `evidence_access_promotion.yml`: no old gate IDs, destinations, or promoted state.
- `sieving_data_migration_manifest.yml`: no old corpus errors or migration claims.

CSV ledgers get their field names, not their old rows. Project state starts at
`setup`, with Ekonerg as the company and Croatian as the output language. All
G1–G7 decisions start pending. The corpus checksum record starts empty.

The scoring model remains an unapproved framework setting until fresh Owner
calibration. A passing synthetic score test is not G3 approval. Offline evidence
tools and EA6.5 classification bands remain in scope. They need new Ekonerg UAT.

## New items with no old file to copy

These are creation requirements, not extra source files or untracked inputs.

| Planned item | Producer and acceptance task |
|---|---|
| Empty `raw/`, `derived/`, `outputs/`, `manifests/batches/`, and `sieving/runs/` | EK-2.1 creates the empty folders; no old contents. |
| Empty `sieving/DATA/`, including the needed RULE and DOCUMENT layout | EK-2.1 and EK-2.3 prove the corpus is empty. |
| Fresh `db/nqa_audit.sqlite` | EK-2.2 creates it through reviewed local initialization; only fixed criterion definitions may be seeded. This name follows the current database helper. |
| Local coordination directories | EK-3.3 creates empty queues and fresh records. Keep workspace review history where it is. |
| `docs/FRAMEWORK_REQUIREMENTS.md` | Recreated from reusable source-plan rules; the old plan is not imported as a completion record. |
| Local Claude guidance, commands, and skills | Claude creates these in EK-3.3. Codex does not copy or edit them. |
| Fresh UAT, review, and release packets | EK-3.1 defines blank forms; later audit tasks create real records. Update hard-coded old packet paths and consumers together. |
| Test fixtures and expected results | EK-3.2 creates invented inputs and reviewed expected outputs. Do not regenerate goldens just to hide a failure. |
| Clean-state validator and transfer tooling | EK-2.3 and EK-1.1 build and test these from the approved plan. They are not inherited capability. |

Keep the current Ekonerg plan, review evidence, tools, and handoffs. Do not overwrite
them to make the destination appear empty. The later copier must check exact
targets and refuse conflicts. The ignored `tools/.venv` is a review aid only;
it must not become an audit runtime or a transfer source.

## Exclusion boundaries

No raw documents, extracted text, chunks, crumbs, old databases, runs, reports,
dashboards, findings, actions, gates, source batches, or approval history transfer.
This applies even when a file sits in a schema, test, prompt, or benchmark folder.
Tests with embedded old data must be adapted to invented examples.

Claude-owned source records are listed for coverage but excluded from Codex's
transfer. Claude must create its new setup. Shared Python packages and the browser
runtime may be reused only after EK-1.3 tests; scripts are not shared.

The nine retired repair scripts stay absent. Recreate only the quarantine notice.
Update tests that expect those scripts on disk to prove their absence instead.
The staged and rendered support-transfer experiments under workspace `doc/` are
also excluded. They are not the active Enconet runtime or its support tests.

## How to reproduce the checks

Run from the workspace root:

```powershell
python -m unittest discover -s Ekonerg\tools\tests -p test_transfer_manifest.py -v
python Ekonerg\tools\transfer_manifest.py verify
```

`verify` writes nothing. It compares the complete file set, hashes, modes,
destinations, purposes, treatments, and scan against the pinned Git objects.
It rejects extra approval fields. It does not grant approval.

`build` regenerates only the two JSON review artifacts. A change to the policy or
manifest needs a new review. Neither command writes a framework destination.

## Claude review request

Check the entire per-file list and the dependency review, not just these counts.
Confirm the boundary for active tools versus retired or unrelated tools. Check
the six run-bound contracts, source-data exclusions, synthetic test plan, and
all support-path changes. Reproduce the tests and inventory verification.

Return APPROVE or specific findings for EK-0.2 in the neutral coordination queue.
Approval closes the manifest task only. File transfer still belongs to EK-1.1;
runtime adaptation and clean-state proof remain later work. Do not bypass the
Owner's source-readiness task or any audit gate.
