# CC_Loto Slice 1 pre-job briefing

## Authorization and boundary

M3 accepts CC_FIN and authorizes CC_Loto support publication from exact baseline
`b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`, conditional on a Loto-specific exact
render, disposable dry run, pre-job briefing, target-native checks, and independent review.
Codex is implementer and Claude Code is reviewer. This briefing authorizes no target write by
itself; CC_Loto remains untouched until Claude accepts the complete package and the native
baseline receives a truthful disposition.

## Proposed first slice

Create exactly eight neutral records, with no existing-file modification:

- `support/PROFILE.md`
- `support/current-status.md`
- `support/log.md`
- `support/RECORD-KEEPING.md`
- `support/decisions/README.md`
- `support/AFI.md`
- `support/LESSONS-LEARNED.md`
- `support/GOOD-PRACTICES.md`

`support/README.md` is deliberately deferred until coordination and handoff destinations exist.
Codex-owned `AGENTS.md`, Claude-owned guidance, `docs` navigation, validators, tests, and tools are
not part of Slice 1.

Exact review inputs:

- [`LOTO_EXACT_RENDER_MANIFEST.md`](LOTO_EXACT_RENDER_MANIFEST.md)
- [`LOTO_DRY_RUN_EVIDENCE.md`](LOTO_DRY_RUN_EVIDENCE.md)
- [`rendered/loto/`](rendered/loto/)

## Native baseline truth

- The shared interpreter lacked declared dependencies. A disposable isolated environment outside
  CC_Loto installed the target's `requirements.txt`; no repository or shared-environment dependency
  state changed.
- With output/model-cache paths redirected to short disposable roots and explicit
  `--pattern test*.py`, native individual layers passed: `core-unit` 42/42, `contract` 25/25,
  and `state-integrity` 3/3 (70/70 total). Contract and state-integrity were rerun outside the
  filesystem sandbox after sandbox-only Windows temp-directory permission errors.
- `webapp` exceeded 120 seconds without a result and was terminated. The default full run also
  produced no final result within its limit. Both are recorded as unavailable, not passed or failed;
  neither is required by this documentation-only first slice.
- CC_Loto remained clean. No product code, data, output, dependency, or configuration was changed.

Claude must independently review the exact render, disposable overlay, and literal native evidence
before any target write. Silence cannot authorize publication.

## Publication and recovery protocol

After acceptance, content commit A contains only the eight reviewed blobs. Validation evidence is
recorded in commit B by appending to `support/log.md` and replacing `support/current-status.md`.
Both commits are independently reviewed before push. Recovery is a new revert limited to the Slice
1 commits; no reset, force push, broad cleanup, product-data change, or unrelated-file restoration.
