# CU-1 compiled file map — proposed, not applied

The draft inventory is now a file-level map. It proposes **19,067 file moves**,
with **zero destination collisions**. All rows still have `approval: pending`.
These are file records, not 19,067 new tasks. CU-2 should process them in the
coherent batches already set by the plan.

No source file, audit folder, database, score, approval or reset state changed.
Owner allowed work to continue while Claude reviews later. That changes review
timing, not authority to bypass safety checks or apply unreviewed live moves.

## Where things will go

- Ten current result files get direct run-root homes: light/dark dashboards,
  report, package JSON and dashboard-data JSON for each active audit.
- Their identity is checked against the existing manifest and inventory hash,
  plus current file bytes. Enconet dark uses its recorded dark/source hashes.
  This is selection for relocation, not approval of a new audit conclusion.
- Ninety-five other files have path run IDs verified against their own local
  database. They stay as saved revisions. A run ID does not prove that a
  generation is active, approved or fit to use.
- 606 files without a proved run stay in `outputs/archive/legacy-...`.
  Dates and guessed names are not turned into new run IDs.
- 41 sieving-quality metrics, 30 JUnit receipts, 32 logs and three JSON check
  receipts go to `work/validation/`, based on content or file type.
- Fourteen supplier framework plans and two workspace plans get plan homes.
  Vendor QA documents named “plan” stay untouched in incoming/raw.
  Review files remain under work/reviews, even if their name contains “PLAN”.
- Distinct revisions keep their old relative history path. An earlier compile
  found seven collisions when those paths were shortened; the corrected map
  preserves both versions and has zero collisions.

## Holds that remain

- Six proposed file moves contain pre-existing edits; do not overwrite them.
- Nine proposed moves belong to Claude, including historical plan records.
  Claude moves them itself. The prior packet identified six before plan
  classification; this refined map correctly adds three historic CC plans.
- 6,495 redirected paths/hardlinks remain outside the file move list.
- The empty reset scratch folder is still covered by the original inventory
  hold. This file-only map does not grant permission to move or delete it.
- Empty-directory cleanup, current references, old immutable-record paths,
  permissions and fresh source hashes must be handled by tested CU-2 tooling.

No directory is moved wholesale. This avoids moving Claude files by accident
and makes each retained version explicit. Removing old empty directories is
not a hidden part of this proposal.

## Packet

`file-moves-final.zip` contains the complete `file-moves-final.json`.
`current-artifacts.json` records the explicit per-audit selection choices.
Those names belong in configuration, not in reusable compiler code.

The older local compile attempts are diagnostic history, not published maps.
The original CU-1 inventory and baselines remain unchanged.

```powershell
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short
C:/xPY/vEnv/WikiEnconet/python.exe scripts/compile_cleanup_map.py --workspace C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1 --inventory PKE_SA_NQA1_doc/plans/cleanup-cu1/scan-20261012-verified/inventory.zip --selection PKE_SA_NQA1_doc/plans/cleanup-cu1/compiled-map/current-artifacts.json --output PKE_SA_NQA1_doc/plans/cleanup-cu1/compiled-map/NEW-MAP-NAME.json
```

Final focused tests: **exit 0, 17 passed**. Tests cover source/DB/sibling
preservation, two synthetic names, plan/source distinction, file-only moves,
version collisions, owner/dirty holds, path escape and manifest/hash selection.
Initial RED collection failed before the compiler existed; a test import path
was then corrected. One later Temp-ACL failure was resolved by elevated retry.
An initial archive safety assertion was too broad: it treated raw-named test
fixture copies as live supplier sources. The corrected scope check passed for
all eight actual supplier roots and all agent-home exclusions.

Compilation: **exit 0**. Both current DB hashes still match the CU-1 baseline.
No full audit/browser regression was run because no audit runtime, dashboard
or live layout changed. The compiler has no apply, delete or reset command.

## Next

CU-1 map and baselines are ready for deferred review. CU-2 can develop and test
the local path contract and migration tool without changing live layout. The
owner layout choice and map/tool safety review remain required before apply.
