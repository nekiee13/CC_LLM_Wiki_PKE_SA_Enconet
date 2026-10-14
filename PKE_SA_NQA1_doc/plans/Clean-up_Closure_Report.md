# Cleanup closure report

Date: 14 October 2026  
Status: **partial — CU-4.2 acceptance is still open**  
Implementer: Codex. Reviewer: Claude.  
Scope: the existing four epics and nine tasks; no new task or slice.

## In plain words

The filing-cabinet work is done. The old folders and scratch trees no longer
block the approved layout. The final checks caught one remaining routing bug,
which is fixed, and one older dashboard display defect, which is not changed.
The audit evidence and scores have not been changed to make checks pass.

## Plan status

| Task | Implementation status | Evidence |
|---|---|---|
| CU-1.1 Inventory | Delivered | `cleanup-cu1/CU1_STATUS.md` |
| CU-1.2 Baselines and layout | Delivered | `cleanup-cu1/OWNER_LAYOUT_APPROVAL.md` and baseline receipts |
| CU-2.1 Local path contract | Delivered; final routing correction tested | `cleanup-cu2/INTEGRATION_STATUS.md`; tests below |
| CU-2.2 Safe move tooling | Delivered | `cleanup-cu2/CU2_REVIEW_PACKET.md`; preview/apply/verify/undo evidence |
| CU-3.1 Workspace | Delivered; named holds resolved | `cleanup-cu3/LIVE_WORKSPACE_RESULT.md`; retention receipts below |
| CU-3.2 Ekonerg | Delivered | `cleanup-cu3/EKONERG_LIVE_SPRINT_RESULT.md` |
| CU-3.3 Enconet | Delivered | `cleanup-cu3/ENCONET_LIVE_SPRINT_RESULT.md` |
| CU-4.1 Release and six suppliers | Delivered | `cleanup-cu4/CU4_RELEASE_AND_SCAFFOLDS_RESULT.md` |
| CU-4.2 Final acceptance | Open | Mobile limitation, latest reviews and final index reconciliation |

Delivered does not mean that every later review has been accepted. Earlier
unchecked plan boxes are not new work orders; the dated receipts describe
what was actually run and reviewed.

## Moves and retained history

- Workspace batch: 405 file moves, including 299 tracked files.
- Ekonerg batch: 924 file moves, 39 runtime/configuration files and ten original
  empty directory trees. The last Windows access-denied hold is resolved.
- Enconet batch: 17,752 file moves, 45 runtime/configuration files and ten
  original empty directory trees.
- Eight retained workspace documents moved with exact hashes; four unfinished
  owner edits stayed unstaged. Claude moved its own seven documents.
- The 102 empty old-`doc` directory nodes are retained under
  `.tmp/cleanup-retained-20261014/old-doc-empty-shells`.
- Sixty-three safe scratch trees, plus five populated synthetic/cache trees
  containing 99 files, are retained under `.tmp`, not deleted.
- The separately owner-approved generated-Claude fixture parent is retained
  under `Enconet/.tmp/cleanup-retained-20261014/protected-test-fixtures`:
  195 files, 6,538 real directories and 2,653 internal shortcuts. No file
  content, ACL or shortcut target was changed. Shortcuts were not followed.
- Both audits now use `outputs/RUN-*`; historical colliding editions remain
  explicit retained revisions. Current dashboards are standalone files.

Detailed retention evidence:

- [Retry result](cleanup-cu4/CU4_HOLDS_RETRY_RESULT_20261014.md)
- [Non-protected retention](cleanup-cu4/CU4_FINAL_NONPROTECTED_RETENTION_20261014.md)
- [Approved fixture retention](cleanup-cu4/CU4_PROTECTED_FIXTURE_MOVE_RESULT_20261014.md)

This is relocation with retention, not deletion or an audit reset. Old absolute
shortcuts are historical records, not supported runtime launchers.

## Final path correction

Three current README links were repaired. A bounded check of nine selected
current documents found 67 local Markdown links with no missing targets.
All 19,871 recorded relocation targets exist: 18,184 Enconet and 1,687 Ekonerg.
These checks do not certify every link in immutable historical documents.

An initial direct-prefix Python scan missed split-component expressions such
as `ROOT / 'outputs' / 'candidates'`. A broader pass found the current Enconet
evidence-export and review defaults still selected old homes. The fix:

- Routes new v4 evidence exports only to local `outputs/RUN-ID/filename`.
- Routes current review defaults to `work/reviews`.
- Resolves valid moved local references through the recorded relocation map.
- Preserves the stricter offline/server-entrypoint ban and explicit legacy
  fixture behavior.
- Adds the same bridge to the reusable overlay generator, with neutral root
  names and idempotence tests. There is no sibling-company runtime dependency.

The new local `Enconet/scripts/evidence_access_policy_v4.py` is byte-identical
to the frozen v4 source. SHA-256:

`de767378cb7a6adff187d7ee35cf0ce2643796d82b4314090b639d0e8f3e15a7`

The immutable release itself is unchanged. Its manifest SHA-256 remains:

`2a18e0db61973b3702989de63ebcf9c1a26f6492b6a55cccba30c950c92b2cb4`

The July review-packet validator and old approval-bound schema records remain
historical contracts. Their old paths were not rewritten as fresh approvals.
Some registry entries refer to absent pre-reset evidence: those operations must
fail closed. Tests expressly forbid borrowing that evidence from history.
Descriptive output labels in `audit_commands.yml` are not runtime path choices.

## Validation

Commands below run from the workspace root. `PY` means
`C:/xPY/vEnv/WikiEnconet/python.exe`. `BROWSER_PY` means
`C:/xAppz/miniconda/python.exe`, which has Playwright and PyMuPDF.

| Check | Exit | Result |
|---|---:|---|
| `PY -B Enconet/scripts/run_regression_tests.py --output Enconet/work/validation/2026-10-14/cu4-closure-regression-01` | 0 | 489 passed: 188 current and 301 isolated historical; no failures/errors/skips; live audit unchanged |
| `PY -B -m pytest Enconet/tests/test_cleanup_final_paths.py audit_template/tests/test_supplier_layout_overlay.py -q -p no:cacheprovider --basetemp .tmp/cu4-path-close-tests-02 --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/path-close-tests-02.xml` | 0 | 16 passed |
| `PY -B -m pytest scripts/tests audit_template/tests/test_supplier_layout_overlay.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_project_records_v4.py -q -p no:cacheprovider --basetemp .tmp/cu4-closure-tooling-01 --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/closure-tooling-01.xml` | 0 | 153 passed |
| `PY -B Enconet/scripts/run_all_validations.py --no-record` | 0 | 19 passed |
| `PY -B Ekonerg/scripts/run_all_validations.py --no-record` | 0 | 8 passed; 9 phase-based skips, not passes |
| `PY scripts/check_guidance_drift.py` | 0 | 47 anchors; 8 documented differences |
| `PY scripts/check_skill_structure.py` | 0 | 32 locations |
| `git diff --check` | 0 | No whitespace errors; existing line-ending warnings noted |

The first focused path-test attempt failed: one test wrongly expected missing
pre-reset evidence to exist, and two test cases had a misplaced assertion.
Those tests were corrected without restoring data; the failed XML is retained.
Earlier browser attempts also exposed verifier selector/timing issues. The
final verifier uses each dashboard's actual preserved controls. Its print spy
is installed inside an explicit function to avoid Playwright invoking the
spy during assignment. Earlier failures are not counted as passes.

All eight local layout descriptors use the approved nine homes. Each future
supplier upgrade verifies 170 installed files and 129 retained originals.
IBE, TEKOL, IGH, IMK, KCPG and MOR remain clean setup projects, not active audits.

### Browser and real PDF receipts

The read-only verifier is `scripts/verify_cleanup_dashboards.py`. It checks
filters, search, ordering, expansion, source-chapter access, responsive widths,
print controls, white print output, PDF content and unchanged source HTML.
It does not claim that opening one representative crumb tests every link.
Full traceability checks remain part of the audit validators.

Final receipts are under each audit's
`work/validation/2026-10-14/cu4-closure-browser/{light,dark}-verified/checks.json`.
Each command uses `BROWSER_PY -B scripts/verify_cleanup_dashboards.py` with
the arguments below. A nonzero browser exit is not a pass.

| `--html` | `--output` | Remaining arguments | Exit/result |
|---|---|---|---|
| `Enconet/outputs/RUN-20261008-17/dashboard_light.html` | `Enconet/work/validation/2026-10-14/cu4-closure-browser/light-verified` | `--expected-points 1450 --expected-fully 6 --expected-percent 80.6% --supplier ENCONET` | 1: 24 passed, mobile overflow failed |
| `Enconet/outputs/RUN-20261008-17/dashboard_dark.html` | `Enconet/work/validation/2026-10-14/cu4-closure-browser/dark-verified` | `--expected-points 1450 --expected-fully 6 --expected-percent 80.6% --supplier ENCONET` | 0: 25 passed |
| `Ekonerg/outputs/RUN-20261003-32/dashboard_light.html` | `Ekonerg/work/validation/2026-10-14/cu4-closure-browser/light-verified` | `--expected-points 1400 --expected-fully 3 --expected-percent 77.8% --supplier EKONERG` | 0: 29 passed |
| `Ekonerg/outputs/RUN-20261003-32/dashboard_dark.html` | `Ekonerg/work/validation/2026-10-14/cu4-closure-browser/dark-verified` | `--expected-points 1400 --expected-fully 3 --expected-percent 77.8% --supplier EKONERG` | 0: 29 passed |

Both Enconet themes invoke print exactly once. The earlier duplicate-count
failure was verifier-only, not a published-dashboard print defect.

Confirmed display defect: Enconet's unchanged light dashboard has a 564-pixel
document width at a 390-pixel viewport. Its matrix escapes the page. The owner
has been asked whether to authorize separate corrected revisions or retain
this as a known limitation. Neither original dashboard has been edited.

## Protected audit facts

Current database SHA-256 values still match the cleanup baseline:

- Enconet: `f17c977f8c5ffec13a279bdb909dd17f38e056e5183812a92ae5810b03251ed1`
- Ekonerg: `161c56ff5d457348ec6809c5e6dcc41e2dd09854d4e71cde11d12a2064d387c0`

No incoming/raw document, active generation, evidence quote, score or gate was
changed in this final path pass. Enconet remains 1,450/1,800 (80.6%); Ekonerg
remains 1,400/1,800 (77.8%). Enconet's G7 remains pending.

## Owner entry points

- [Enconet light](../../Enconet/outputs/RUN-20261008-17/dashboard_light.html)
- [Enconet dark](../../Enconet/outputs/RUN-20261008-17/dashboard_dark.html)
- [Ekonerg light](../../Ekonerg/outputs/RUN-20261003-32/dashboard_light.html)
- [Ekonerg dark](../../Ekonerg/outputs/RUN-20261003-32/dashboard_dark.html)

## What remains — within CU-4.2

1. Record the owner's mobile-limit decision. If corrected revisions are
   authorized, retain originals, preserve data and use the existing revision
   and publication controls; do not silently replace released files.
2. Obtain Claude's latest retention and final path reviews. The two substantive
   retention requests are still open; no review acceptance is inferred.
3. Reconcile the final committed code/docs index snapshot. The last certified
   snapshot is `e4201491241e5d139c9b5d1ebafa4ca3ca210f72`, older than this
   correction. A current-tip refresh is not claimed in this report.
4. Update this report and the original acceptance checklist from actual
   outcomes. No further folder-move batch is planned.

The seven pre-existing owner-edited files remain outside this implementation
commit. No Claude-owned guidance, skill or message has been modified.
