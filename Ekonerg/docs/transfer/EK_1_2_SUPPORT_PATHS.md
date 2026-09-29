# EK-1.2: local support tools

Status: support package ready for Claude review. EK-1.2 is still open.
Codex implements. Claude reviews. Date: 2026-09-29.

## What & Why

Ekonerg now has its own copies of the five support tools and four support test
files. A script should find its project from its own location. It should not
depend on which folder the user opened first.

This review covers the support foundation. The other 216 adapt entries are
pending. It does not approve a complete audit runtime or close EK-1.2.

Source: pinned commit `9f20430c95334daa4c3cedb7ee71b002bd3be739`.
The [adaptation record](EK_1_2_SUPPORT_ADAPTATIONS.json) lists each source blob,
source hash, and new file hash. Hashes for new text use UTF-8 with LF endings.
The approved transfer manifest has not changed.

## Changes and reasons

| Tool | What changed | Why |
|---|---|---|
| `agent_coord.py` | `ROOT` is Ekonerg; `COORD` and `HANDOFF_POINTER` are directly under that root. IDs must be safe names. Redirected output folders are refused. | Claims, messages, and the board must land in the right project. An ID must not become a path. |
| `run_validation.py` | `PROJECT` replaces the old workspace and company roots. All generated commands and working folders are local. Handoff pointer traversal is refused. | Running a local test must not launch the old project's code or read its handoff. |
| `make_handoff.py` | Defaults, schema, project ID, and CLI root are Ekonerg. Record validation reads local paths. Publication refuses redirected folders. Git output decoding handles the Windows code page. | Notes and their pointer must stay local. The Git root may still be the parent workspace. |
| `check_guidance_drift.py` | It reads `Ekonerg/doc/GUIDANCE_PAIRS.json` from its own root. | A missing local contract must fail visibly, rather than use the old one. |
| `check_skill_structure.py` | The default scan covers Ekonerg only. Shared scopes need an explicit option. | The new project must not silently scan another company's skills. Explicit scope checks still test duplicate names and ownership. |

The four support test files use their local script copies. The Unicode handoff
test relocates the tool and schema into its fake project, matching the new CLI
boundary. Invented test fixtures hold no company source excerpts or approvals.

## How to use the tools

Scripts are under `Ekonerg/scripts/`. They may be called by absolute path from
Ekonerg, the workspace root, or another folder. None imports shared script code.

The local handoff CLI accepts only its own Ekonerg root. A relative `--validate`
record path is read from that root. A foreign record is refused. Its internal
Python functions support fake roots for tests; they are not a separate approval
or cross-project publication interface.

The local skill checker scans only the project by default. `--include-shared`
adds workspace and user-global infrastructure to a read-only check.
`--workspace-root`, `--claude-home`, and `--codex-home` allow explicit test scopes.
Those checks retain the original duplicate-scope and agent-ownership rules.

Actual development messages still use Enconet's neutral coordination channel,
as required by workspace guidance. Tests exercise the Ekonerg tool against fake
local queues. EK-3.3 will create Ekonerg's own guidance and coordination setup.

## Proof and limits

Fourteen new tests run copies of the tools in disposable workspaces. They check
the intended output, both wrong Enconet paths, foreign roots, traversal, real
Windows junctions, the shared Git root, and paths with spaces and Croatian
characters. Fake sibling snapshots include file names, hashes, and timestamps.
All support imports are checked against the Python standard library.

See [validation evidence](EK_1_2_VALIDATION.md) for commands, exits, and limits.
The local guidance contract is not present yet; its check fails as expected.
The full aggregate is not run, because its audit dependencies are still pending.
A printed command list is path evidence, not proof that every stage works.

The tools assume one cooperative writer. Preflight path checks do not claim
protection against a hostile process changing paths during a write.
No live audit, source intake, database migration, or shared environment change
was performed.

## Remaining EK-1.2 work

After this support review, continue within EK-1.2:

1. Adapt the audit dispatcher and command registry so closeout calls the local
   handoff tool. Preserve phase checks and validation before publication.
2. Adapt the runtime scripts and local sieving package. Check output options,
   nested and sibling paths, and imports without an editable Enconet install.
3. Complete the path changes identified in `DEPENDENCY_REVIEW.md`, including
   old packet paths and the corpus default. Keep later blank-state and fixture
   work linked to EK-2 and EK-3; do not import old records to fill gaps.
4. Run the full required checks once the dependencies exist. Claude must review
   that evidence before the whole task closes.
