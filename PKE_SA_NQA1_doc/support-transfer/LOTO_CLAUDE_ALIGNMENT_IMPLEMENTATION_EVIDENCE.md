---
record_type: local_ab_implementation_evidence
target: CC_Loto
slice: claude-guidance-alignment
step: 2
recorded_at_utc: 2026-07-20T03:45:10Z
wiki_packet_commit: 37099a1730b81923fa4d2500a9c250d3f228bb21
target_parent: a4ccbe144a2027745e74215e2136dbe6fe610497
content_commit_a: 843906eb3b01b4154110f089e29f553c7f8b1ca2
evidence_commit_b: bda0db3cf913207c254064b0681f7f309a536ec6
publication_state: local_unpushed
implementer: claude-code
reviewer: codex
---

# CC_Loto Claude-owned alignment — local A/B implementation evidence

## Gate and chain

- Codex accepted the pre-write packet with no findings in
  `CX_2026-07-20T034015Z_loto-claude-alignment-packet-accepted`, having independently reproduced the
  renderer and candidate identities, the pure-append proof, the schema `$ref` resolution, and the
  disposable checks.
- Preflight passed before any write: HEAD equalled `origin/main` at
  `a4ccbe144a2027745e74215e2136dbe6fe610497`, divergence `0 0`, porcelain empty, zero tags,
  `CLAUDE.md` at parent object `3edd87504e76a97d8ba46ecf40e81b8ad894299f`, and Codex-owned
  `AGENTS.md` at `42571a2c5f67b5a11759f38d7d65f50f156087c3`.
- The Wiki packet commit `37099a17` was confirmed on `origin/main` and the renderer was rerun,
  reproducing candidate SHA-256 `0DE42FEA...7A35`.
- Local chain is exactly `a4ccbe14 -> 843906eb (A) -> bda0db3c (B)`.
- CC_Loto is clean and two commits ahead of `origin/main` (`0 2`). **Nothing was pushed.**

## Content commit A

Commit `843906eb3b01b4154110f089e29f553c7f8b1ca2` (`support: add Claude guidance support-workflow
section`) has parent `a4ccbe14...` and modifies exactly one path:

| Operation | Path | Committed object |
|---|---|---|
| modify, Claude-owned | `CLAUDE.md` | `689a48b669c009baf79f1349e64f352532a5e444` |

- The staged object was compared to the reviewed authority before committing and matched.
- `git diff --cached --numstat` reported `55 0` — a pure append; no pre-existing byte changed.
- `git diff --cached --check` exited `0`.
- Codex-owned `AGENTS.md` remains `42571a2c` in A. No shared-neutral, coordination, product, data,
  dependency, workflow, test, index, tag, or release path is touched.

At clean A, the support-operator interpreter (PyYAML `6.0.3`, jsonschema `4.26.0`) ran the installed
aggregate (`--no-record`) to exit `0` and `python tools/support/agent_coord.py .` to exit `0` with 0
errors and 0 warnings; `coordination/BOARD.md` stayed byte-identical. Native layers, with output and
model-cache paths redirected outside the repository:

| A layer | Tests | Exit | Result |
|---|---:|---:|---|
| `core-unit` | 42 | 0 | passed |
| `contract` | 30 | 0 | passed |
| `state-integrity` | 3 | 0 | passed |

## Evidence commit B

Commit `bda0db3cf913207c254064b0681f7f309a536ec6` (`support: record Claude alignment validation
evidence`) has parent A and changes exactly:

- `support/log.md` — object `4fdd06f3ff7cb7dfef9f23396a56be6d9bea7008`
- `support/current-status.md` — object `9290c6a71806f57e924900bb0af98cca28906412`

The reviewed B byte authority is
[`rendered/loto-claude-alignment-evidence-b/`](rendered/loto-claude-alignment-evidence-b/), produced
by [`rendered/render_loto_claude_alignment_evidence_b.py`](rendered/render_loto_claude_alignment_evidence_b.py).
That renderer derives the log from the committed A blob and proves the append-only property rather
than asserting it: published prefix preserved, exactly two appended lines, each matching the
pipe-delimited event contract. It also refuses to emit any record containing a synchronization
overclaim and requires the explicit non-synchronization statement. Both staged objects were compared
to that authority before committing and matched.

At clean B:

- `B^ == A`; `A^ == a4ccbe14`.
- A changes exactly 1 path; B changes exactly 2 paths.
- `CLAUDE.md` is `689a48b6` and `AGENTS.md` is `42571a2c` at B.
- Installed aggregate exits `0`; coordination validation exits `0` with 0 errors and 0 warnings;
  `BOARD.md` byte-identical.
- Target is clean; divergence is `0 2`.
- Native layers again pass 42/42, 30/30, and 3/3, all exit `0`.

## Not-run and disclosed states

Optional, optimization-core, integration, webapp, and hosted-CI layers were **not run**: a
documentation-only guidance change makes no integration applicable. They are recorded as not-run,
never as passed, and are not evidence about product-suite health.

Two preparation failures were disclosed in the dry-run evidence and are retained here: a renderer
`KeyError` from assuming an inline schema shape instead of the `$defs` reference, and an incorrect
`56 1` numstat produced by diffing against a PowerShell-redirected copy of the parent instead of the
Git blob. Both were corrected before any target write; the correct diff is `55 0`. No
implementation-phase command failed.

## Standing non-synchronization

Neither A nor B claims the guidance pair is synchronized, and both renderers fail closed on such a
claim. Publication of this step is a precondition, not the conclusion: each agent must independently
confirm the shared anchors at the live tip for its own side first.

## Reviewer handoff and recovery

Codex must independently inspect A/B identities, the parent chain, exact path sets, committed
objects against their Wiki authorities, the append-only proof, status truth, ownership boundaries,
installed and native validation, and the clean `0 2` state. No push is authorized by this record. On
explicit acceptance, Claude Code may push exactly A followed by B as one normal fast-forward and
report live remote state for closure verification. Recovery, only on reviewer/owner direction, is a
new revert of B followed by A; reset, force push, and unrelated cleanup are prohibited. M4 remains
closed.
