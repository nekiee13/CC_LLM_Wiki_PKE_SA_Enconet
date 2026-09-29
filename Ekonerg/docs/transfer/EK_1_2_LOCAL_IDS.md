# EK-1.2: local ID contract

Date: 2026-09-29. Codex implements; Claude reviews later. EK-1.2 is still open.

## What & Why

The copied `db_util.py` needs `schemas/id_patterns.yml` before it can
write even a test row. Ekonerg had the helper but not that contract.
This batch adds the local ID shapes. The `APP_B` text in some ID shapes
is a record format, not a decision that any source applies to Ekonerg.
No company name or source edition is baked into the pattern file.

The handoff proposed the generation tool and harness next. Inspection
showed that they also need a database schema, approval records, more
scripts, and a golden-set record that are not local yet. I did not
pretend that generation works. The local ID contract is a prerequisite.

## Tests first

Before the contract existed, the direct contract test failed as expected.
The other three could not reach their assertions because pytest's
default temp folder was denied by the sandbox. All four pass now.
They copy only Ekonerg's own helper and contract into two fake projects:
one with spaces and no sibling project, and one with Croatian text and
a fake sibling Enconet. They check valid and invalid IDs, local database
creation, a blocked foreign database path, and unchanged sibling bytes,
file time, and file list. No real audit data is used.

The first pytest run also hit a sandbox denial in its default temp
folder. A second run with a temp folder inside this Git checkout made
an unrelated no-Git handoff test fail. The full suite passed when run
with an external temp folder. The generated in-project pytest folder
was then removed; it was test output, not audit evidence.

## Source and limits

`EK_1_2_LOCAL_IDS_ADAPTATIONS.json` records the pinned source blob and
hash, the local file hash, and the test hash. After this batch, 186
adapt rows and 45 recreate rows remain. This batch did not initialize
a database, activate a prompt, ingest a document, or grant approval.

The pinned database SQL still hardcodes regulatory source codes. The
owner has not chosen Ekonerg's source editions or scope. A future
database batch must make that contract neutral and test it before
generation tools can be called ready. Claude review is queued, not
assumed complete.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m pytest Ekonerg\scripts\tests\test_db_identity.py -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-id-tests-20260929` | 0 | Four new tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-id-tests-20260929` | 0 | All 27 support tests passed after the two-name test refinement. |
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 75 tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 pinned rows and 275 dependency-scan files verified. |

The full audit aggregate, real corpus, browser, and benchmark checks
were **not run**. Ekonerg's guidance-pair check remains blocked by the
planned EK-3.3 file. Claude: inspect the pinned-to-local map and rerun
the isolated tests. Please review this batch without closing EK-1.2.
