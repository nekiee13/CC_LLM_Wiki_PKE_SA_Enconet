# EK-1.2 candidate: neutral setup structure validation

## What & Why

A new audit needs its own empty wiki folders and a way to check their shape.
This ten-file bundle gives it a local structure checker, a neutral folder
contract, a header-only validation log, six empty wiki markers, and a Git
rule that keeps copied framework text at LF on each checkout. The rule leaves
incoming source documents alone. The bundle does not create a project state,
database, page, criterion, source rule, or approval.

The Enconet page-type schema was **not** copied: it names Appendix B and an
18-criterion set. Ekonerg's scope is not approved yet. The new schema checks
only folder locations and broad page-name shapes. A structure PASS does not
mean the audit or any document is approved.

## TDD and validation evidence

1. Red: `python -B -m unittest discover -s audit_template/tests -p
   test_bootstrap_setup_validation.py -q` exited 1 because the new bootstrap
   module did not exist. The same command later exposed a real log bug: an
   invalid phase added a bad CSV row. That red run exited 1 with two failed
   cases. The checker now refuses the invalid phase before logging.
2. Green: the focused tests exited 0 with four tests. They use two invented
   company names with spaces and Croatian letters. One has a fake sibling
   Enconet and one does not. Both include a fake nested Enconet folder. The
   tests cover preview, apply, safe retry, empty wiki PASS, bad page and
   schema FAIL, foreign paths, no-record mode, a valid recorded row, and
   unchanged sibling and nested-folder bytes and file times.
3. `python -B -m unittest discover -s audit_template/tests -q` exited 0:
   20 tests passed. `python -B -m pytest Ekonerg/scripts/tests -q -p
   no:cacheprovider --tb=short --basetemp
   C:\Users\PC\AppData\Local\Temp\ekonerg-setup-bundle-20260930-01` exited
   0 outside the sandbox: 39 tests passed. Ekonerg tools and sieving unittest
   suites exited 0 with 111 and 83 tests, respectively.
4. `python -B Ekonerg/tools/transfer_manifest.py verify` exited 0 against
   pinned Enconet source `9f20430`, 1,963 rows, and 275 dependency files.
5. Workspace `python scripts/check_guidance_drift.py` exited 0. Ekonerg
   `python -B Ekonerg/scripts/check_guidance_drift.py` exited 1 because
   planned EK-3.3 `Ekonerg/doc/GUIDANCE_PAIRS.json` is absent. That local
   check did **not** pass.

## Live empty-scaffold copy

The first read-only Ekonerg preview showed nine creates, no conflicts.
`python -B audit_template/bootstrap_setup_validation.py --target Ekonerg
--apply --run-id setup-validation-20260930-01` exited 0 and created exactly
those nine files. Its append-only journal is
`Ekonerg/.bootstrap/setup-validation-v1/setup-validation-20260930-01.jsonl`
(SHA-256 `45a8017c9e18aacd465bfbce8ad1be1d954c83c039116bd18e94abc1fafa1f0e`).

The invalid-phase test found a code defect before commit. The fix was made
in both the versioned source and its fresh Ekonerg copy. The old journal
remains unchanged as evidence of the first copy. A second preview showed
nine preserves, then run ID `setup-validation-20260930-02` exited 0 with
zero creates and nine preserves against the corrected manifest. Its journal
is `Ekonerg/.bootstrap/setup-validation-v1/setup-validation-20260930-02.jsonl`
(SHA-256 `48d1e84527e65daebc0f988700286193c6fb9fda07f1551579c56b18ea8f5340`).

A Windows checkout check then exposed a byte-stability gap: without a local
Git rule, copied text and journals would use CRLF after checkout, but the
manifest expects LF bytes. A new test first failed because the rule was
missing. The rule was added to the versioned bundle and tested. The third
preview showed one create and nine preserves. Run ID
`setup-validation-20260930-03` exited 0, created only `.gitattributes`, and
preserved the nine earlier files. Its journal is
`Ekonerg/.bootstrap/setup-validation-v1/setup-validation-20260930-03.jsonl`
(SHA-256 `3526ad8cd93aa51019ef8952ab576d1042e9474db8c65cb99a51a9f12f0dc784`).
Staging exposed one last gap: `.gitattributes` itself needed the LF rule.
A test failed first, then passed after the rule was added to the versioned
source and live copy. The old journals remain immutable. Run ID
`setup-validation-20260930-04` exited 0 with zero creates and ten preserves;
its journal SHA-256 is
`7e8c5a3f83b671ba6bd48e2c6e210e1ec820f0be86022b5b32bdc2c4807ddfa5`.
`git check-attr eol` now reports `lf` for the rule itself, copied script,
schema, log, marker, and journal; `incoming/` is not covered. The final
template manifest hash is
`b83509375a1e9fd0a7909dbba2e5aa72d49318ccde41b954fd1f266db7570f16`.

`python -B Ekonerg/scripts/validate_structure.py --no-record` exited 0 on
the empty folders only. The live validation log still has just its header.
No Ekonerg database or project-state file exists. The 31 owner files in
`Ekonerg/incoming/` were not read, hashed, moved, staged, or processed.

## Gate and limits

Claude review is pending. EK-1.2 stays open: later-phase child validators
are still missing, so the full aggregate, browser checks, and benchmarks
were not run. Ekonerg's current `schemas/id_patterns.yml` also still has
Appendix B-specific crumb, requirement, evaluation, and gap IDs. Those IDs
must be made company-neutral at the versioned source before criterion-bearing
work; this setup check does not use or approve them. Source scope, editions,
storage, intake, and approval remain owner decisions.
