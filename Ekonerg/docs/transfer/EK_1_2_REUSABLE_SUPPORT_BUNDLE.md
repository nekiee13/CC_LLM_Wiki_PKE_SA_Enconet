# EK-1.2 candidate: copied support tools and incoming drop-off

## What & Why

The next audit should get its own support scripts from a tested source, not
through more company-name patches. This slice adds a versioned six-file
support bundle: coordination, handoff, guidance, and skill checks; the handoff
schema; and an `incoming/.gitkeep` folder marker. The bootstrap reuses the
guarded preview/apply engine from the sieving bundle. It logs file hashes,
refuses conflicts, and keeps matching files on retry.

The Ekonerg-local copies of the four scripts now use project-neutral labels.
The handoff tool's default project ID comes from the folder it lives in. No
support command imports a sibling audit or the bootstrap at run time.

The owner has already placed 31 files under `Ekonerg/incoming/`, following the
Enconet folder convention. This batch did not open, hash, move, copy, ingest,
or approve those files. It removed only Codex's uncommitted, empty `income/`
placeholder after the owner corrected the folder name. The drop-off rule is
documented in `Ekonerg/docs/INCOMING_DROP_OFF.md`.

## TDD evidence

1. Red: `python -B -m unittest discover -s audit_template/tests -p
   test_bootstrap_support.py -q` exited 1 because `bootstrap_support` did
   not exist.
2. Green: `python -B -m unittest discover -s audit_template/tests -q`
   exited 0 outside the sandbox: 6 tests passed. Two invented company roots
   were tested, one with a sibling and one without. The copied tools created
   only local coordination and handoff records. Fake incoming files were
   unchanged by retry. A conflicting file stopped all copies before writes.
3. `python -B -m pytest Ekonerg/scripts/tests -q -p no:cacheprovider
   --tb=short --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-support-bundle-20260930-01`
   exited 0 outside the sandbox: 39 tests passed.
4. `python -B -m unittest discover -s Ekonerg/tools/tests -q` exited 0
   outside the sandbox: 111 tests passed.
   `python -B -m unittest discover -s Ekonerg/sieving/tests -q` exited 0
   outside the sandbox: 83 tests passed.
5. `python -B Ekonerg/tools/transfer_manifest.py verify` exited 0: 1,963
   pinned rows and 275 dependency-scan files verified.
6. `python -B Ekonerg/scripts/check_skill_structure.py` exited 0: no local
   skill locations are configured yet. `python scripts/check_guidance_drift.py`
   exited 0: workspace guidance still matches its contract.
7. `python -B Ekonerg/scripts/check_guidance_drift.py` exited 1 because the
   planned EK-3.3 `doc/GUIDANCE_PAIRS.json` is absent. This is **not** a pass.
8. `python -B audit_template/bootstrap_support.py --target Ekonerg` exited 0
   in read-only preview mode: five files would be preserved and only the
   `incoming/.gitkeep` marker would be created. No apply was run on Ekonerg.

## Gate and limits

Claude review is pending. The support bundle does not yet cover every Epic 1
script or final clean-state gate. The guidance check still exits 1 without
the planned EK-3.3 `doc/GUIDANCE_PAIRS.json`; copying a check is not a claim
that its future configuration exists. No real source intake or audit run is
authorized by this slice. EK-1.2 remains open.
