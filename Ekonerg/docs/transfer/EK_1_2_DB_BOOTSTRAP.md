# EK-1.2: empty local database bootstrap

Date: 2026-09-30. Codex implements; Claude reviews later. EK-1.2 is
still open.

## What & Why

The copied database helper now has a local ID contract. Its next need
is a local SQL schema and a safe way to create an empty database. The
pinned initializer seeded Appendix B criteria and had a `--reset`
option. Neither is right for a new audit before the owner picks scope.

The Ekonerg initializer reads only its own schema. It creates no
company, source, criterion, document, or approval rows. It has no reset
option. A second run checks and preserves an existing valid database,
including its foreign-key links.
It refuses a foreign path or an incomplete file without overwriting it.
If creation stops partway, it leaves the file for diagnosis and refuses
an automatic retry. There is no recovery or migration command yet.

The schema has a blank `approved_sources` table. Authority links must
point to a listed source with the right role. A run's `source_rule` must
be a listed governing source. Language text is not limited to the old
company's three languages. No regulation code or edition is compiled
into SQL. This is a storage shape, **not proof of approval**: a future
intake gate must independently check each source record against owner
approval, source hash, and edition before inserting it.

## Tests first

Five tests failed before the local schema and initializer existed. A
later red test found that an interpretive source could be used as a
run's governing rule; the schema now blocks it. One more red test found
that retry accepted an existing database with broken foreign keys; the
initializer now refuses it. All six tests pass. Tests create
only fake projects outside the workspace, with two company names, spaces,
Croatian text, and a fake sibling Enconet. They check empty startup,
source links, repeat-run byte and file-time stability, blocked foreign
paths, blocked reset, and untouched incomplete or damaged files. The sibling's file
list, bytes, and file time stay unchanged.

No Ekonerg database was created. No migration, real intake, or audit
corpus was run. The schema still stores the framework's existing audit
tables and statuses; later runtime scripts must be checked against the
new source registry before they are called ready.

## Source and limits

`EK_1_2_DB_BOOTSTRAP_ADAPTATIONS.json` maps both adapted files to pinned
Git commit `9f20430`, with source blobs, source hashes, local hashes,
and the new test hash. After this batch, 184 adapt and 45 recreate rows
remain. The earlier 12 Claude review requests are queued, not approved.

The owner still decides Ekonerg source editions, scope, storage, and
intake. This batch does not make the framework audit-ready.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m pytest Ekonerg\scripts\tests\test_db_bootstrap.py -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-db-bootstrap-20260930` | 0 | Six synthetic bootstrap tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-db-bootstrap-20260930` | 0 | 33 support tests passed. |
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 75 sieving tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 transfer-tool tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 pinned rows and 275 dependency-scan files verified. |
| `python -B scripts\check_guidance_drift.py` | 0 | Workspace guidance: no errors. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | Planned EK-3.3 guidance-pair file is absent. |

The adaptation map was checked against all three local file hashes and
both pinned source hashes: zero mismatches.

The full audit aggregate, real corpus, browser, and benchmark checks
were **not run**. Claude: review the local-path and no-reset behavior,
the source-role rules, the empty startup state, and the pinned hash map.
Please review this batch without closing EK-1.2.
