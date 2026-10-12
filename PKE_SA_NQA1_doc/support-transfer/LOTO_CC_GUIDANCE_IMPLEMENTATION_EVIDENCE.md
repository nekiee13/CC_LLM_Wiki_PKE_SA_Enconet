---
record_type: local_ab_implementation_evidence
target: CC_Loto
slice: cc-guidance
recorded_at_utc: 2026-07-20T00:58:22Z
wiki_packet_commit: 5a50210af395d34341ef55022f57541e8b56c3f1
target_parent: fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e
content_commit_a: 416691248cb4f69586ddd483a942c56e5be60cf6
evidence_commit_b: f549b40665c2321ff46168d43c67b2f2f9422bd5
publication_state: local_unpushed
implementer: claude-code
reviewer: codex
---

# CC_Loto guidance correction — local A/B implementation evidence

## Gate and chain

- Codex accepted the pre-write packet with no findings in
  `CX_2026-07-20T005207Z_loto-cc-guidance-packet-accepted`, having independently reproduced the
  renderer and candidate hashes, the 3/2 diff, the parent facts, and the disposable checks.
- Preflight at the published Slice 5 tip passed before any write: HEAD equalled `origin/main` at
  `fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e`, divergence `0 0`, porcelain empty, `CLAUDE.md` at
  parent object `be29ac97bf0307bfc0128e9c2120010bb921993a`, and Codex-owned `AGENTS.md` at
  `34b7eb93095022bea137e2a0c2313f356bfa0f28`.
- The Wiki packet commit `5a50210a` was confirmed on `origin/main`, and the renderer was rerun,
  reproducing candidate SHA-256 `3D4DCF9F...42C9`.
- Local chain is exactly `fd7e96fd -> 4166912 (A) -> f549b40 (B)`.
- CC_Loto is clean and two commits ahead of `origin/main` (`0 2`). **Nothing was pushed.**

## Content commit A

Commit `416691248cb4f69586ddd483a942c56e5be60cf6` (`support: correct Claude guidance packaging
statement`) has parent `fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e` and modifies exactly one path:

| Operation | Path | Committed object |
|---|---|---|
| modify, Claude-owned | `CLAUDE.md` | `3edd87504e76a97d8ba46ecf40e81b8ad894299f` |

- The staged object was compared to the reviewed authority *before* committing and matched.
- `git diff --cached --check` exited `0`; `git diff-tree` reports one path; diffstat is 3 insertions
  and 2 deletions, confined to the opening paragraph.
- Codex-owned `AGENTS.md` remains at `34b7eb93` in A. No shared-neutral, coordination, product,
  data, dependency, workflow, tag, or release path is touched.

At clean A, the separate support-operator interpreter (PyYAML `6.0.3`, jsonschema `4.26.0`) ran
`python tools/support/agent_coord.py .`: exit `0`, 0 errors, 0 warnings, and `coordination/BOARD.md`
remained byte-identical. With output and model-cache paths redirected outside the repository, the
native runner produced:

| A layer | Tests | Exit | Result |
|---|---:|---:|---|
| `core-unit` | 42 | 0 | passed |
| `contract` | 25 | 0 | passed |
| `state-integrity` | 3 | 0 | passed |
| Total | 70 | 0 | passed |

## Evidence commit B

Commit `f549b40665c2321ff46168d43c67b2f2f9422bd5` (`support: record guidance-correction validation
evidence`) has parent A and changes exactly:

- `support/log.md` — SHA-256 `9E939A1C719E91037E48C7E712BA8687540360AA28B5914531FF3BC923948568`
- `support/current-status.md` — SHA-256
  `37BAC1AFD889B50D34EF160076F187AE5D58532341AFFEE616721F668CD32832`

The reviewed B byte authority is
[`rendered/loto-cc-guidance-evidence-b/`](rendered/loto-cc-guidance-evidence-b/), produced by
[`rendered/render_loto_cc_guidance_evidence_b.py`](rendered/render_loto_cc_guidance_evidence_b.py).
That renderer derives the log from the committed A blob and *proves* rather than asserts the
append-only property: it requires the published prefix to be preserved and exactly two appended
lines matching the pipe-delimited event contract. It also refuses to emit any record containing a
synchronization overclaim and requires the explicit non-synchronization statement to be present.
Both staged objects were compared to that authority before committing and matched.

At clean B:

- `B^ == A`; `A^ == fd7e96fd`.
- A changes exactly 1 path; B changes exactly 2 paths.
- `CLAUDE.md` is `3edd8750` and `AGENTS.md` is `34b7eb93` at B.
- Installed coordination validation exits `0` with 0 errors and 0 warnings; board byte-identical.
- Target is clean; divergence is `0 2`.
- Native layers again pass 42/42, 25/25, and 3/3 (70/70), all exit `0`.

## Not-run and excluded states

Optional, optimizer-core, integration, and webapp layers were not made applicable by a
documentation-only change and were **not run**; they are recorded as not-run, never as passed. No
command attempt is being excluded from this record: every renderer, validator, and native invocation
reported above succeeded on its first attempt in this implementation phase.

## Standing non-synchronization

Neither A nor B claims the CC_Loto guidance pair is synchronized, and both renderers fail closed on
such a claim. `AGENTS.md` carries support read-order, ownership, validation-truth, recovery, and
gate anchors that `CLAUDE.md` does not. Closing that asymmetry is an owner-scoped decision for a
separate briefed slice.

## Reviewer handoff and recovery

Codex must independently inspect A/B identities, parent chain, exact path sets, committed objects
against their Wiki authorities, append-only log behaviour, status truth, installed validation,
native results, and the clean `0 2` state. No push is authorized by this record. On explicit
acceptance, Claude Code may push exactly A followed by B as one normal fast-forward and report live
remote state for Codex's closure verification. Recovery, only on reviewer/owner direction, is a new
revert of B followed by A; reset, force push, and unrelated cleanup are prohibited. Validators/tests,
aggregate validation, rollback evidence, and M4 remain closed.
