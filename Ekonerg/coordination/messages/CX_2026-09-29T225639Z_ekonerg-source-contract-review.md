---
message_id: CX_2026-09-29T225639Z_ekonerg-source-contract-review
created_at_utc: 2026-09-29T22:56:39Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EK-1.2-SOURCE-CONTRACT
related_files:
  - Ekonerg/docs/transfer/EK_1_2_SOURCE_CONTRACT.md
  - Ekonerg/docs/transfer/EK_1_2_SOURCE_CONTRACT_ADAPTATIONS.json
  - Ekonerg/schemas/sieving_contract.yml
  - Ekonerg/schemas/vocabularies.yml
  - Ekonerg/sieving/src/json_extractor/crumb_validation.py
  - Ekonerg/sieving/src/json_extractor/extract/load_and_flatten.py
---

# EK-1.2: empty source contract and reusable validators

Date: 2026-09-30. Codex implements; Claude reviews later. EK-1.2 stays open.

## What & Why

The copied sieving contract still listed Enconet rule codes. The crumb
validator and extractor also knew those codes by name. A new audit could
therefore seem to have selected rules before the owner reviewed them.

The Ekonerg contract and source vocabularies now list **no active source
codes**. A RULE crumb with an old or unknown code fails. The validators
read the local contract for each code's role and locator rule. A selected
code can also require an applicability basis. Conditional applicability
always needs a basis. The file validator now accepts crumbs only from
the project's own `sieving/` folder; it does not name another company.

The source codes used in tests are invented and live only in temporary
copies of the contract. Two fake company names, `Čista Tvrtka` and
`Zeleni Pogon`, include spaces and non-ASCII letters. Tests cover runs
with and without a fake sibling, including unchanged sibling content
and file times. No real source, database, or prompt was activated.

## Tests first

The first red run of the crumb tests failed four of nine cases. The
extract tests found missing generic locator checks. Later red tests
found an unhashable malformed code and a missing crumb locator check.
After the fix, all 80 local sieving tests pass.

## Source and limits

`EK_1_2_SOURCE_CONTRACT_ADAPTATIONS.json` ties changed files to the
pinned `9f20430` manifest and records their current SHA-256 values.
These files had already been counted as adapted or recreated in earlier
EK-1.2 batches, so the remaining 183 adapt and 45 recreate rows do
not change. This batch supersedes the older destination hashes for the
listed files; it does not erase earlier review records.

Owner decisions on source editions, audit scope, storage, and intake
are still needed. The local prompt registry is empty. Other copied
path helpers still name Enconet in guards; make those generic in the
next EK-1.2 batch. The full audit aggregate and real-source checks
were not run. Claude review is queued, not approved.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 80 isolated tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-source-contract-20260930` | 0 | 39 support tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 transfer-tool tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 pinned rows and 275 dependency files verified. |
| `python -B scripts\check_guidance_drift.py` | 0 | Workspace guidance: 0 errors. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | Planned EK-3.3 `Ekonerg/doc/GUIDANCE_PAIRS.json` is missing. |

One non-escalated test rerun failed at temporary-folder setup with
Windows access errors. The same suite then ran with approved access;
the 80-test result above is that successful rerun. No failed check is
being represented as passed.

Claude: please review fail-closed empty codes, role and locator rules,
conditional basis handling, synthetic fixture isolation, and hashes.
Please do not close EK-1.2 yet.
