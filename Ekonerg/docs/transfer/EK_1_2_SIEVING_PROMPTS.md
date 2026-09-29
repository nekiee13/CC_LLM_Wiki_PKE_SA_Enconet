# EK-1.2: fresh, inactive prompt bundle

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
coherent EK-1.2 batch, not the end of that task or Epic 1.

## What & Why

The prompt text, registry, fresh history, and invented examples belong
together. Copying only one would leave a broken or misleading bundle.
The two candidate prompts point to Ekonerg's local crumb schema. They
say to use only an owner-approved source and run context. They do not
embed a company name or source edition, so the text can serve a later
company without another rewrite.

`active.yml` has an empty `active` map. This is deliberate: template
files do not grant permission to process documents. The history is new;
it carries no prior score, promotion, or approval. The three JSON files
are invented parser examples, not source evidence. One is deliberately
invalid so tests can prove the format gate rejects it.

## Tests first

Five tests failed before the bundle existed. All five now pass. They
copy only the local prompt bundle, schema, and validator into a fake
project with spaces and Croatian text. They check the empty registry,
local schema links, no company-specific prompt text, new history, valid
invented examples, and the rejected invalid example. A fake sibling
Enconet marker keeps the same bytes and file time. No real corpus is
read. The full synthetic sieving suite has 75 tests.

## Source identity and limits

The three adapted files and four recreated files are mapped to pinned
Git commit `9f20430` in `EK_1_2_SIEVING_PROMPTS_ADAPTATIONS.json`. That
map records each source blob and hash, plus each destination LF hash.
After this batch, 187 adapt and 45 recreate rows remain. The empty
source `.gitkeep` is not needed while the local fixtures folder has
files; its manifest row remains for final disposition. Ten earlier
Claude reviews are queued, not approved.

No prompt was activated, scored, or used on a real document. Owner
approval of source editions, scope, and storage is still needed before
intake. Other transfer files, full corpus checks, installation checks,
and release checks remain. The framework is not audit-ready.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 75 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and 275 dependency files match. |
| `python -B scripts\check_guidance_drift.py` | 0 | Workspace guidance has no drift errors. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | EK-3.3 guidance pair file is absent. |

The full audit aggregate, real corpus, browser, and benchmark checks
were **not run**. Claude: inspect the empty activation gate, compare
source and destination maps, rerun the synthetic tests, and send
findings or batch-only approval through neutral coordination. Keep
EK-1.2 open.
