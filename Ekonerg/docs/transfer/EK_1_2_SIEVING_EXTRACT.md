# EK-1.2: local parsed-JSON extraction

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
slice of EK-1.2, not completion of the task or Epic 1.

## What & Why

This code turns parsed sieving JSON into rows for later query and export.
Each row must keep its document ID, source location, evidence quote, rule or
document side, and join key. This slice transfers the two selected source
extraction files into Ekonerg. It uses only Ekonerg's local configuration
and contract. It does not read a real document or write an audit output.

The adapted module keeps the source row columns and validation IDs. It also
closes data-loss cases found in tests. A non-object root is refused. A list
of payloads must have the same number of provenance paths; the old `zip`
could silently drop a payload. Wrong quote, source and entity shapes now
produce errors instead of truncated text, missing location data, or a
crash. The primary evidence column uses the first non-empty quote.

## Tests first

Before the two local files existed, all seven starting tests failed in
fixture setup. After adaptation, 12 focused tests passed. Three more RED
checks found an empty primary quote, an unreported nested entity shape,
and a crash on a non-text entity member. A fourth RED check found an
unreported malformed source heading. Each passed after a small fix. The
current synthetic sieving suite has 37 passing tests.

The test project has a path with spaces and Croatian text, its own local
contract, and a fake sibling Enconet marker. Tests use made-up RULE and
DOCUMENT items, including a Croatian quote. They check side separation,
canonical names, schema drift in normal and strict modes, valid join keys,
source headings, entity order, malformed shapes, one path per payload, and
correct file labels on errors from multiple payloads.
The fake Enconet marker's bytes and timestamp stay unchanged.

## Source identity and limits

The two adapted rows come from pinned Git commit `9f20430`. Source blobs,
source hashes, destination LF hashes and the new test hash are in
`EK_1_2_SIEVING_EXTRACT_ADAPTATIONS.json`. The code is an adaptation, not a
byte copy. After this slice, 198 adapt rows and 49 recreate rows remain.
The prior continuity, foundation, I/O and query reviews are pending, not
approved.

The extractor can return rows alongside validation errors, as the source
design does. Those rows are **not approved output**. Pipeline and export
gates still need to block invalid results; neither is complete. The full
package, crumb validation, CLI, prompts, corpus and release checks are also
pending. Template source codes do not decide Ekonerg editions or scope.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 37 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and the 275-file dependency scan match. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured. |

The full audit aggregate, real sieving corpus, browser and benchmark checks
were **not run**. Their later runtime files and owner-approved inputs are
not ready. Claude: compare source and destination hashes, inspect the
shape/provenance changes, rerun synthetic and regression tests, and return
findings or slice-only approval through neutral coordination. Keep EK-1.2
open.
