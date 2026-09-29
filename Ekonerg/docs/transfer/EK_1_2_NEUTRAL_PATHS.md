# EK-1.2: company-neutral sieving paths

Date: 2026-09-30. Codex implements; Claude reviews later. EK-1.2
remains open.

## What & Why

The copied sieving tools refused a folder named `Enconet`, but allowed
the same wrong path under any other company name. A later audit would
need another name patch. The guards now use the local project layout:
normal sieving data, settings, reads, and exports must stay under that
project's `sieving/` tree. The project root can still serve as the
CLI's glob starting point. Paths outside the project, or through a
link to outside it, remain blocked. Existing hard-link checks remain.

This is a reusable rule, not an Ekonerg source or scope decision. The
real source-code list and active prompt list remain empty.

## Tests first

The new test copies only the needed local files into two fake projects:
`Čista Tvrtka` and `Zeleni Pogon`. One has a fake sibling audit and
one has no sibling. Both reject an unknown nested company folder and
an outside path. The fake sibling's file list, bytes, and file times
must stay unchanged. Before the fix, both cases failed because the old
guards accepted the unknown nested name. After the fix, the focused
test and all 81 sieving tests pass.

The first test attempt could not set up Windows temporary folders in
the sandbox. The same red test ran with approved temp access and failed
for the intended guard defect. That access was also used for the green
run; the setup error is not a pass.

## Source and limits

`EK_1_2_NEUTRAL_PATHS_ADAPTATIONS.json` ties the adapted config file
to pinned commit `9f20430` and records all three destination hashes.
The I/O guard was created in an earlier Ekonerg batch, so it has no
pinned source row. This record supersedes its earlier destination hash
without erasing that earlier review request. The remaining 183 adapt
and 45 recreate rows do not change.

This does not approve source editions, scope, storage, or intake. No
document was ingested and no real audit run was made. Claude review
is pending. The full audit aggregate was not run.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -p test_company_neutral_paths.py -q` | 0 | Two fake company cases passed. |
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 81 tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-neutral-paths-20260930` | 0 | 39 support tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 transfer-tool tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 pinned rows and 275 dependency files verified. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | Planned EK-3.3 guidance-pair file is still absent. |

Claude: please review the positive sieving boundary, CLI root case,
symlink and hard-link behavior, two-company test, and hash map. Please
do not close EK-1.2 yet.
