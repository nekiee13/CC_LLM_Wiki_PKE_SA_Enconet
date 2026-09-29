# EK-1.2: local sieving command

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
slice of EK-1.2, not the end of that task or Epic 1.

## What & Why

The CLI lets a user list, query, preview, and export JSON sieving rows.
The pinned command expanded file patterns from the shell's folder. That
could search the wrong project before the pipeline checked paths. The
Ekonerg command now starts relative paths at the Ekonerg project root.
It checks direct files, data folders, globs, and output paths before
reading or exporting. A recursive glob does not follow a linked folder.

The query, list-files, and info commands keep the pinned behavior.
Invalid filters exit with code 2. An explicit development preview can
show unfiltered rows, but cannot export them. Rows with ERROR validation
issues need both a development override flag and a nonblank reason to
export. That route is **not** an owner approval or an audit finding.

## Tests first

Seven tests failed before the local CLI file existed. The first run
after implementation exposed two test-fixture issues: Windows console
encoding and the pinned exporter's need for an existing output folder.
The fixture now sets UTF-8 and creates only its fake local output folder.
Two more safety tests were added. All nine focused tests pass.

The tests use a fake Ekonerg project with spaces and Croatian text, run
the command from a sibling Enconet folder, and use only made-up JSON.
They check local export, recursive glob and `--all`, missing files,
foreign direct and glob paths, linked paths, invalid-filter preview,
and validation-error override. The fake sibling marker keeps the same
bytes and file time. The full synthetic sieving suite has 66 tests.

## Source identity and limits

The adapt row comes from pinned Git commit `9f20430`. Its source blob,
source hash, destination LF hash, and the test hash are in
`EK_1_2_SIEVING_CLI_ADAPTATIONS.json`. After this slice, 192 adapt rows
and 49 recreate rows remain. Eight earlier Claude reviews are queued,
not approved.

The command still expects an output folder to exist, as the pinned
exporter does. Prompts, remaining transfer files, full corpus checks,
installation checks, and release checks remain. No real source was
ingested, and the owner must approve source editions and scope before
intake. The framework is not audit-ready.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 66 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and 275 dependency files match. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured. |
| `python -B Ekonerg\sieving\cli.py --help` | 0 | Three local commands listed. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | EK-3.3 guidance pair file is absent. |

The full audit aggregate, real corpus, browser, and benchmark checks
were **not run**. Claude: compare the source and destination hashes,
inspect the pre-scan path checks and export gates, rerun tests, and send
findings or slice-only approval through neutral coordination. Keep
EK-1.2 open.
