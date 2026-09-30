# EK-1.2 candidate: taxonomy-neutral sieving runtime

## What & Why

The copied sieving code assumed every audit uses Appendix B. Its contract
loader fixed the taxonomy filename and the number of criteria at 18. Its
extractor required `APP_B`, and crumb checks opened the Appendix B file
directly. The runtime now reads one taxonomy file named in the local
contract. It checks that the file stays in the local schema folder, that
the taxonomy ID matches, and that criterion IDs are unique and non-empty.
Extracted items must match the local template ID, version, taxonomy ID, and
criterion name. Missing or bad config fails closed.

This change does **not** choose Ekonerg criteria or approve a source. The v1
bundle and the present Ekonerg config still carry an Appendix B taxonomy and
select it by default. They are **not** a clean company-neutral bootstrap.
The template README now says not to apply v1 to another company until a
separate neutral-config task resolves this. No Ekonerg document was ingested.

## TDD proof

1. Red: a new bootstrap test copied the runtime into two made-up company
   roots, configured a one-criterion `TEST_SET` there, and queried a made-up
   document. Before the fix, both queries exited 2: the extractor still
   required `APP_B` and rejected `AREA_2`. A new local-contract test exited
   1 because a foreign taxonomy path was not rejected. A template-identity
   test exited 1 because a wrong template ID and version were accepted.
2. Green: `python -B -m unittest discover -s audit_template/tests -q`
   exited 0 with 21 tests. `python -B -m unittest discover -s
   Ekonerg/sieving/tests -q` exited 0 with 86 tests. The two synthetic roots
   cover a company name with spaces and non-ASCII letters, with and without
   a sibling project; sibling bytes and file times stay unchanged. Contract
   tests reject missing, foreign, mismatched, duplicate, and empty taxonomy
   config. Crumb checks accept the invented criterion and reject an old
   Appendix B criterion under that invented config.
3. `python -B -m pytest Ekonerg/scripts/tests -q -p no:cacheprovider
   --tb=short --basetemp
   C:\Users\PC\AppData\Local\Temp\ekonerg-neutral-sieving-20260930-01`
   exited 0 with 40 tests. `python -B -m unittest discover -s
   Ekonerg/tools/tests -q` exited 0 with 111 tests. The tools suite printed
   an expected stop message from a negative case; the suite passed.
4. `python -B Ekonerg/tools/transfer_manifest.py verify` exited 0 against
   pinned source `9f20430`, 1,963 rows, and 275 dependency files. Workspace
   `python scripts/check_guidance_drift.py` exited 0 with zero errors.
   Ekonerg `python -B Ekonerg/scripts/check_guidance_drift.py` exited 1
   because planned EK-3.3 `doc/GUIDANCE_PAIRS.json` is missing. It did not
   pass. The full live audit aggregate, browser, and benchmark were not run.

## Live sync and limits

The versioned source and Ekonerg copy of the four changed bundle files
have matching hashes. The updated bundle manifest SHA-256 is
`18f46d85f411c69a7c2a3dc783edc03ed193936856eab7e9ac376e158a08154f`.
The live preview exited 0 and showed 21 preserves, no creates or conflicts.
Apply run ID `neutral-sieving-runtime-20260930-01` exited 0 with zero
creates and 21 preserves. Its immutable journal is
`Ekonerg/.bootstrap/sieving-v1/neutral-sieving-runtime-20260930-01.jsonl`
(SHA-256 `7aa54c7f4d164739bdd98f52a3197d5d6126521b325e940f498519ee56a83bb8`).

A fresh-checkout check found that Windows could change copied sieving code
to CRLF and break those hashes. A new setup-bundle test failed first, then
passed after a versioned local Git rule was extended. The rule covers only
`sieving/cli.py`, `sieving/src/**/*.py`, and the active prompt file; it
does not cover `sieving/DATA` or `incoming/`. The repaired setup manifest
SHA-256 is
`7bdad406671aa54f1c830b331bb8b8bfe65ab349faa45f15909d56dd0dfa3f29`.
Its Ekonerg preview showed ten preserves. Apply run ID
`neutral-sieving-lf-20260930-01` exited 0 with zero creates and ten
preserves; its immutable journal SHA-256 is
`e8637ee6ada984a5f94780017c3b9284b1132d235473cb5ac9055c17feaf8a58`.
`git check-attr eol` reports `lf` for copied sieving code and prompts, but
no forced ending for the two source-data folders.

The Ekonerg `sieving/DATA` folder, audit database, and project-state file
do not exist. All 31 owner files in `incoming/` are untouched. No live
intake, source approval, or criterion selection occurred. The Appendix B
facade, taxonomy file, and default template selection remain a separate
framework defect. Claude review is pending; this runtime slice does not
close EK-1.2.
