# EK-1.2: sieving path and contract foundation

Date: 2026-09-29. Codex builds; Claude reviews. Status: slice ready for
review. The whole EK-1.2 task is still open.

## What & Why

The sieving tool needs its own data and settings paths. It also needs a local
copy of its input contract and the 18 Appendix B names. The old default
settings path used the worker's home folder. That could mix two companies.
This slice moves that default under Ekonerg and rejects a caller path that
leaves the Ekonerg project. A resolved path check also catches an existing
link to an outside folder. The default DATA path was already correct; it
remains under `Ekonerg/sieving/DATA`.

The four approved manifest rows come from Git commit `9f20430`. Exact source
blob IDs and byte hashes, plus destination LF hashes, are in
`EK_1_2_SIEVING_FOUNDATION_ADAPTATIONS.json`. The JSON-compatible contract is
byte-for-byte equal to its source. The taxonomy parses to the same data; only
its header note changed. The two Python files keep the source contract logic
and adapt local paths and wording. Four adapt rows are submitted here, so
207 adapt rows and 49 recreate rows remain. This count includes the prior
continuity slice while its review remains pending.

## Tests first

The new tests use made-up Ekonerg and Enconet folders in Windows Temp. The
first run failed because the four local files did not exist. After adding
them, five tests passed. They check a path with spaces and Croatian text,
both local defaults, rejected outside and nested Enconet paths, a link to an outside folder,
unchanged sibling Enconet bytes and timestamp, and local contract loading.
The tests do not read a real audit document or run an old repair tool.

## Checks and limits

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -p test_foundation.py -q` | 0 | Five synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 manifest rows and the 275-file scan match. |
| Read-only hash and Git-blob comparison of the adaptation JSON | 0 | All four source blobs and five destination hashes match. |

The focused test command first failed inside the filesystem sandbox because
Windows Temp was not writable there. It passed with the approved Temp access.
The full audit aggregate, old sieving corpus tests, browser and benchmark
checks were **not run**. Their runtime and fresh inputs are not ready.

## Limits and review

This is **not** a runnable sieving pipeline. The remaining package files,
CLI, tests, prompts, corpus setup and export paths are still missing. The
path check is a normal-workflow guard, not a defense against a race where
another process changes a link after the check. Other entry points may still
accept an outside path until they are adapted and tested.

The carried template names 10 CFR 50 Appendix B, 10 CFR 21 and ASME NQA-1.
That is a framework template, not an Ekonerg source-edition approval or an
applicability ruling. No Ekonerg document or regulation was ingested. The
owner's intake gate must supply and approve exact editions and scope before
real intake. Do not treat these template codes as that decision.

Claude: verify the pinned source blobs and destination hashes, compare both
parsed schemas to the source, read the adapted path logic and tests, and run
the focused synthetic tests and manifest verification. Report findings or
**slice-only** approval through neutral coordination. Keep EK-1.2 open.
