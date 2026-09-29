# EK-1.2: reusable sieving CLI labels

Date: 2026-09-30. Codex implements; Claude reviews later. EK-1.2
remains open.

## What & Why

The copied CLI worked from another project folder, but its help and
`info` command still said “Ekonerg.” A later company would need a
name patch. The CLI now gets the display name from its own project
folder. The pipeline and export descriptions also use neutral words.
No audit rule, source, prompt, or output path was changed.

## Tests first

The new test runs the copied CLI in two fake projects, `Čista Tvrtka`
and `Žuti Pogon`. Both names have spaces and non-ASCII letters. One
fake project has a sibling audit and one does not. Each CLI shows its
own name, reads an invented document, and exports only into its own
`sieving/outputs/` folder. The sibling file list, bytes, and file times
stay unchanged. A source scan also bars the first company's name from
the reusable CLI, pipeline, and export modules.

Before the fix, the focused test failed on fixed “Ekonerg” labels and
source text. A later assertion failed only because the help renderer
wrapped one line; that assertion now checks the two stable parts.
The focused test then passed, followed by all 83 sieving tests.

## Source and limits

`EK_1_2_NEUTRAL_CLI_ADAPTATIONS.json` ties the three adapted files to
the pinned `9f20430` source manifest and records their new SHA-256
values. It also records the new test hash. These files were already
counted as adapted, so 183 adapt and 45 recreate rows remain. The
new hashes supersede older destination hashes but do not erase earlier
review requests.

The real source-code list and active prompt list are still empty. No
document was ingested and no real audit run was made. Owner decisions
on editions, scope, storage, and intake remain pending. Claude review
is queued, not approved. The full audit aggregate was not run.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -p test_company_neutral_cli.py -q` | 0 | Two fake project cases and the source scan passed. |
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 83 tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-neutral-cli-20260930` | 0 | 39 support tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 transfer-tool tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 pinned rows and 275 dependency files verified. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | Planned EK-3.3 guidance-pair file remains absent. |

Claude: please review the folder-derived labels, two-company CLI test,
unchanged sibling evidence, and hashes. Please do not close EK-1.2 yet.
