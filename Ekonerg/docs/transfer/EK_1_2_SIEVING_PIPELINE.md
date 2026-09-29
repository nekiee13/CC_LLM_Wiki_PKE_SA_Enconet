# EK-1.2: local sieving pipeline

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
slice of EK-1.2, not the end of that task or Epic 1.

## What & Why

The pipeline joins local JSON reading, record flattening, query filters,
and export. An invalid item can still make a row for diagnosis. That row
must not quietly become an audit output. The two selected source files are
now local to Ekonerg. Normal export blocks a failed filter, a bad input
file, an empty result, or an ERROR validation issue.

The pinned source allowed an explicit validation override reason. This
slice keeps that route, requires non-blank text, and records the reason on
the result. A reason is **not** an owner approval or an audit finding.
Bad files and failed filters cannot use this route. The local I/O layer
also refuses paths outside Ekonerg before reading or writing.

## Tests first

Before the local package entry and pipeline existed, seven starting tests
failed in fake-project setup. Eight focused tests now pass. They make a
fake Ekonerg folder with spaces and Croatian text, plus a sibling Enconet
marker. They check a valid local CSV export; an evidence error; strict
schema drift; failed filters with and without preview; a mixed good/bad
file list; foreign input and output paths; an empty project; and the
explicit validation-reason route. The sibling marker's bytes and timestamp
stay unchanged. No live corpus, approval or audit output is used.

## Source identity and limits

The two adapt rows come from pinned Git commit `9f20430`. Their source
blobs, source hashes, destination LF hashes, and the test hash are in
`EK_1_2_SIEVING_PIPELINE_ADAPTATIONS.json`. After this slice, 196 adapt
rows and 49 recreate rows remain. Five earlier Claude reviews are queued,
not approved.

The package is still incomplete: crumb validation, CLI, templates,
prompts, full corpus tests, installation checks and release checks remain.
The pipeline's explicit validation reason is only a diagnostic exception;
it does not bypass later human gates. Source editions and applicability
still require owner-approved intake. The full framework is not ready.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 45 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and the 275-file dependency scan match. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured. |

The full audit aggregate, real sieving corpus, browser and benchmark checks
were **not run**. Claude: compare source and destination hashes, inspect
export gates and the local path behavior, rerun tests, and return findings
or slice-only approval through neutral coordination. Keep EK-1.2 open.
