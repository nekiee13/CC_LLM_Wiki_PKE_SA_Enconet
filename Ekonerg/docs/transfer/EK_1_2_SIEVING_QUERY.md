# EK-1.2: local sieving query layer

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
slice of EK-1.2, not completion of that task or Epic 1.

## What & Why

The query layer turns a plain filter into matching rows. Ekonerg needs its
own code and its own field list, loaded from its local sieving contract.
This slice transfers the four selected query files: the package entry,
field schema, filter parser, and DataFrame engine. It does not open a real
document, write an output, or approve any Ekonerg source edition.

The source DSL rules remain: AND binds tighter than OR; comma-separated
enum values mean IN; text search ignores case; and unknown syntax fails.
The engine still refuses more than 1,000 OR clauses. One safety fix moves
that limit check before the empty-table return. An empty new project must
not hide an over-complex query.

## Tests first

The first run failed: all seven starting tests could not copy the missing
local query files into a fake Ekonerg project. After adaptation, nine query
tests passed, and the full current sieving suite passed 25 tests. The fake
project has a path with spaces and Croatian text, a local contract, and a
fake sibling Enconet marker. Tests cover local import, 18 template criteria,
AND/OR order, IN and text search, empty and legacy queries, malformed filters,
unknown operators, clause-local warnings, and the empty-table limit. The
Enconet marker bytes and timestamp stay unchanged. No old corpus was read.

## Source identity and remaining work

The four adapt rows come from pinned Git commit `9f20430`. Source blob IDs,
source hashes, destination LF hashes and the new test identity are in
`EK_1_2_SIEVING_QUERY_ADAPTATIONS.json`. The parser and engine are compact
adaptations, not byte copies. Public exports and tested behavior remain.
After this slice, 200 adapt rows and 49 recreate rows remain. The prior
continuity, foundation and I/O reviews are still pending, not approved.

This is **not** a runnable sieving pipeline. Extraction, normalization,
pipeline wiring, CLI, prompts, full corpus tests and release checks are
still missing. Template codes do not decide Ekonerg scope or source editions.
Those choices remain at the owner's intake gate.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 25 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and the 275-file dependency scan match. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured. |

The full audit aggregate, real sieving corpus, browser and benchmark checks
were **not run**. Their inputs and later runtime files are not ready.
Claude: compare the pinned source and hashes, inspect the local contract
import and empty-data limit, rerun the focused and regression tests, then
give findings or slice-only approval through neutral coordination. Keep
EK-1.2 open.
