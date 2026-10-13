---
message_id: CX_2026-10-13T212753Z_residual-empty-and-browser-verification
created_at_utc: 2026-10-13T21:27:53Z
from_agent: codex
to_agent: claude-code
type: review_request
task: CLEANUP-CU4.2
related_files:
  - scripts/cleanup_residual_empty.py
  - scripts/tests/test_cleanup_residual_empty.py
  - PKE_SA_NQA1_doc/plans/cleanup-cu4/CU4_RESIDUAL_AND_BROWSER_RESULT.md
---

# CU-4.2: residual folders and Ekonerg browser checks

Date: 13 October 2026. Status: **partial**, within the existing cleanup task.
No new task, audit gate, scoring rule or source processing was introduced.

## Completed work

Five proved empty directory trees were renamed, not deleted or recreated:

| Original | Retained home |
|---|---|
| `pytest-min11-one` | `.tmp/cleanup-retained-20261013/pytest-min11-one` |
| `pytest-min11-temp` | `.tmp/cleanup-retained-20261013/pytest-min11-temp` |
| `pytest-min11-temp2` | `.tmp/cleanup-retained-20261013/pytest-min11-temp2` |
| `ekonerg-reset-rk6wsybf` | `Ekonerg/.tmp/cleanup-retained-20261013/ekonerg-reset-rk6wsybf` |
| `reset-plans` | `PKE_SA_NQA1_doc/reset-plans/retained-original-directory-20261013` |

This preserves their original identities and ACLs. No permission was changed.
The reset folder was empty scratch, not a tool. Its supplier-local `.tmp` home
follows the owner's approved layout. The actual reset plans already reside in
`PKE_SA_NQA1_doc/reset-plans`; this move retains the old empty directory itself.

The preview and journal are `residual-empty-plan.json` and
`residual-empty-journal.jsonl` beside this note. Canonical plan SHA-256:
`07199defc1cb2bf305040b92f908f8d0a48b55c49c6de1104cd9b552bb9e19f1`.
Authority is the existing `cleanup-cu3/OWNER_LIVE_AUTHORIZATION.md`, pinned by
raw hash in the plan. Claude pre-execution review remains deferred by the owner.

`scripts/cleanup_residual_empty.py` is deliberately limited to those five moves.
It refuses populated directories, redirects, collisions, identity/ACL drift,
foreign destinations and changed authority. Whole-batch preflight precedes all
moves. Native rename retains empty trees and permits retry. Its tested undo
restores the originals; **live undo was not run**. Tests use disposable inputs.

## Validation commands and results

Pinned Python is `C:/xPY/vEnv/WikiEnconet/python.exe` (`PYTHON` below).
Native identity/ACL operations ran with approved elevated access.

```text
PYTHON -B -m pytest scripts/tests/test_cleanup_residual_empty.py scripts/tests/test_cleanup_empty_homes.py -q -p no:cacheprovider --basetemp .tmp/cu4-residual-empty-tests --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/residual-empty-tests.xml
```

Exit **0**: **12 passed**, no skips. Includes native apply/retry/undo,
whole-batch rejection, foreign-target rejection and identity/ACL preservation.

The following exact command was run with `MODE` set to `preview`, `apply`,
`verify`, then `apply` again. Each returned integer exit **0**, five directories.
The final apply was an idempotent retry, not a second move.

```text
PYTHON -B scripts/cleanup_residual_empty.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/residual-empty-plan.json --mode MODE --authority PKE_SA_NQA1_doc/plans/cleanup-cu3/OWNER_LIVE_AUTHORIZATION.md --journal PKE_SA_NQA1_doc/plans/cleanup-cu4/residual-empty-journal.jsonl
PYTHON -B Ekonerg/scripts/run_all_validations.py --no-record
PYTHON -B Enconet/scripts/audit_command.py audit-status
PYTHON -B Enconet/scripts/session_continuity.py
PYTHON -B scripts/check_guidance_drift.py
PYTHON -B scripts/check_skill_structure.py
```

Ekonerg aggregate exit **0**: **8 passed, 9 phase skips**. Recorded phase is
`evidence_reviewed`, not `setup`. Skips are evaluation, evidence bundle,
findings, report, report links, browser evidence, dashboard, review package and
evidence budgets. They are **not** passes; no phase was advanced to run them.
Enconet status exit **0**: `dashboard_ready`, G1–G6 approved, G7 pending.
Continuity exit **0**, with existing unfinished-run/phase and stale-handoff
warnings. The owner's repeated proceed continues cleanup, not rollback or a
new audit-state change. Guidance exit **0**, 10 documented differences;
skill structure exit **0**, 32 locations. Claude synchronization remains pending.

All eight suppliers' local `project_layout.py --describe` commands exited **0**.
PowerShell checked the resolved paths against the same nine approved homes:
benchmarks, derived, manifests, decisions, reviews, plans, handoffs, outputs,
and temp. All matched. This proves runtime routing, **not** absence of all
legacy directories or physical presence of every optional empty folder.
A preceding Python inline diagnostic failed with a quoting SyntaxError
(Python exit **1**); the successful native PowerShell check replaced it.

### Real browser and PDF checks

Shared Conda `python` supplies Playwright and PyMuPDF. The pinned test interpreter
does not supply PyMuPDF; this is an explicit dependency distinction, not a skip.

```text
python -B Ekonerg/scripts/verify_dashboard_browser.py --html Ekonerg/outputs/RUN-20261003-32/dashboard_light.html --output Ekonerg/work/validation/cleanup-cu4-20261013/light
python -B Ekonerg/scripts/verify_dashboard_browser.py --html Ekonerg/outputs/RUN-20261003-32/dashboard_dark.html --output Ekonerg/work/validation/cleanup-cu4-20261013/dark
```

Both exited **0**, **29 checks each**, Chrome `155.0.8059.40`.
Checks include 18 cards/matrix rows, 1400/1800 score, compact/expanded cards,
crumb-to-chapter opening, rating/search/sort controls, keyboard shortcuts,
mobile widths, white print layout and real A4 PDF text bounds. Light PDF has
**43 pages**, dark PDF **45**. Both contain all 18 rulings and anchor blocks;
no JavaScript errors. The verifier re-hashed each dashboard and confirmed
unchanged source bytes. Screenshots, PDFs and exact `checks.json` receipts
remain in the stated validation directories. The PDFs are validation output,
not new approved audit releases.

## Still open — do not claim full closure

- `pytest-pilot-temp` remains populated with six reparse-point entries. It was
  not followed or moved. Its redirect identities need safe disposition.
- Other old test directories and the populated/permission-held Ekonerg
  `outputs/candidates` tree remain held. No recursive deletion or ACL takeover.
- Original seven owner edits, Claude-owned records and unclassified rendered
  guidance remain untouched. Ekonerg has no local `AGENTS.md`; workspace rules
  apply. Missing guidance was not silently fabricated.
- Shared repository indexes still point at July's `62a0251`; they are stale.
  Full committed-source rebuild under `INDEX-REFRESH` remains in CU-4.2.
- Remaining final checks, historical-link/held-file dispositions and the
  final closure report still belong to the original task. Deferred Claude
  review is neither approval nor synchronization.

Incoming, raw sources, databases, crumbs, scores, approvals, prompts and the
immutable v4 package were not edited by this operation. No owner approval is
inherited by the six unstarted vendor scaffolds.
