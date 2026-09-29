# EK-1.2: local crumb validation

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
slice of EK-1.2, not the end of that task or Epic 1.

## What & Why

A crumb is a small JSON record made during document sieving. This checker
tests its shape before it can be used downstream. It checks the document
side, source roles, criterion names, item IDs, original quote fields, and
the fields that must not appear. It does **not** prove a quote is real or
that a source edition applies to Ekonerg. Those checks need approved
source intake and later human review.

The pinned Enconet checker was adapted to Ekonerg's local taxonomy. A
relative file name now starts at the Ekonerg project root, not at the
shell's working folder. The checker refuses files outside the project,
including sibling Enconet files, links to them, and nested Enconet paths.
It also reports wrong JSON value types as errors instead of crashing.
It only reads files; it creates no audit data.

## Tests first

Before the local file existed, seven tests failed because the module was
missing. After the first implementation, a new wrong-type test failed
with a `TypeError`; that error is now handled. Eight focused tests pass.
They use a fake Ekonerg folder with spaces and Croatian text, a fake
sibling Enconet folder, and made-up quotes. The fake sibling's bytes and
file time stay unchanged. The full synthetic sieving suite has 53 tests.

## Source identity and limits

The adapt row comes from pinned Git commit `9f20430`. Its source blob,
source hash, destination LF hash, and test hash are in
`EK_1_2_SIEVING_CRUMB_ADAPTATIONS.json`. After this slice, 195 adapt
rows and 49 recreate rows remain. Six earlier Claude reviews are queued,
not approved.

The copied source-role codes and languages remain template values until
the owner approves Ekonerg's regulatory scope and source editions. No
source was ingested. CLI, templates, prompts, full corpus tests,
installation checks, and release checks remain. The framework is not
ready for an audit.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 53 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and 275 dependency files match. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured. |

The full audit aggregate, real sieving corpus, browser, and benchmark
checks were **not run**. Claude: compare source and destination hashes,
inspect the local path guard and type handling, rerun tests, and send
findings or slice-only approval through neutral coordination. Keep
EK-1.2 open.
