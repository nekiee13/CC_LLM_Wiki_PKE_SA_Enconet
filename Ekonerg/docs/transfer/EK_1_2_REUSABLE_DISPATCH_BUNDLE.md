# EK-1.2 candidate: local dispatcher and preflight runner

## What & Why

A new audit needs local commands, not imports from another company. This
three-file bundle copies the command registry, the phase-aware dispatcher,
and the six-layer preflight runner. It uses the same guarded preview, hash
check, copy journal, and safe retry as the earlier bundles. It depends on
the state bundle's local path, database, and state helpers.

This is **not** the phase-aware aggregate validator. The separate
`run_all_validations.py` is still missing from Ekonerg and the template.
The dispatcher refuses `audit-validate` and `audit-close` while it is
missing. No audit pass or closeout is claimed.

## TDD evidence

1. Red: `python -B -m unittest discover -s audit_template/tests -p
   test_bootstrap_dispatch.py -q` exited 1 because `bootstrap_dispatch`
   did not exist.
2. Green: after adding the versioned bundle, the three new tests passed.
   They use two invented company names with spaces and Croatian characters.
   One has a sibling audit; one does not. Preview writes nothing. Apply and
   retry keep matching files. The copied commands work from another folder,
   foreign database paths are refused, missing phase-aware validation fails
   closed, and the sibling's bytes and file times stay unchanged.
3. A wider test found a real mistake: importing the local path helper from
   the preflight runner broke its stdlib-only contract in isolated copies.
   The UTF-8 console setup is now self-contained in that runner. The fixed
   code passed `python -B -m unittest discover -s audit_template/tests -q`
   (exit 0, 12 tests), `python -B -m unittest discover -s
   Ekonerg/tools/tests -q` (exit 0, 111 tests), and `python -B -m unittest
   discover -s Ekonerg/sieving/tests -q` (exit 0, 83 tests).
4. `python -B -m pytest Ekonerg/scripts/tests -q -p no:cacheprovider
   --tb=short --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-dispatch-bundle-20260930-02`
   exited 0 outside the sandbox: 39 tests passed. A prior sandbox run
   exited 1 because Windows denied access to its temporary test folder.
5. `python -B audit_template/bootstrap_dispatch.py --target Ekonerg`
   exited 0 in read-only mode: all three files would be preserved. No
   live apply ran. `python -B Ekonerg/tools/transfer_manifest.py verify`
   exited 0 against pinned Enconet commit `9f20430`, 1,963 rows, and 275
   dependency-scan files.
6. Workspace guidance check exited 0. Ekonerg guidance check exited 1
   because planned EK-3.3 `doc/GUIDANCE_PAIRS.json` is absent. That check
   did **not** pass.

## Gate and limits

Claude review is pending; EK-1.2 stays open. The phase-aware validator and
its own tests still need a separate transfer. A full audit aggregate was
not run. The 31 owner files in `Ekonerg/incoming/` were not read, hashed,
staged, or processed. Source scope, editions, storage, intake, and approval
remain for later owner gates.
