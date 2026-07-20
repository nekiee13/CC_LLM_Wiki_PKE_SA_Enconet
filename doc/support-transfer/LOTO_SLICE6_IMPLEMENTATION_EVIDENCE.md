---
record_type: local_ab_implementation_evidence
target: CC_Loto
slice: 6
recorded_at_utc: 2026-07-20T01:50:48Z
wiki_packet_commit: a7e028c85bb2a36ef6f7a330e41aa172c6bd9221
target_parent: f549b40665c2321ff46168d43c67b2f2f9422bd5
content_commit_a: 14f0cf2638a26b08c02fccfae353957333bfb8f8
evidence_commit_b: d5dc65e568ee73d82389e6e1d3fdf24122661adf
publication_state: local_unpushed
implementer: codex
reviewer: claude-code
---

# CC_Loto Slice 6 validators/tests — local A/B implementation evidence

## Gate and chain

- Claude accepted corrected packet v2 in
  `CC_2026-07-20T014240Z_loto-slice6-v2-accepted-findings-resolved` after independently
  reproducing both v1 fixes, exact bytes, disposable validation, and native counts.
- Immediately before target write, live/local/fetched CC_Loto `main` equalled
  `f549b40665c2321ff46168d43c67b2f2f9422bd5`, divergence `0 0`, porcelain empty, and all three
  candidate paths were absent. The accepted renderer rerun passed all checks and reproduced hashes.
- Local chain is exactly `f549b40 -> 14f0cf2 (A) -> d5dc65e (B)`.
- Live `origin/main` remains `f549b40`; local divergence is `0 behind / 2 ahead`; porcelain empty.
  **Nothing was pushed.**

## Content commit A

Commit `14f0cf2638a26b08c02fccfae353957333bfb8f8` has parent `f549b40` and creates exactly:

| Path | Committed object | Reviewed object |
|---|---|---|
| `tools/validate_support.py` | `40b44057048fb3083213f040bc5d769e399a42a3` | same |
| `tests/contract/test_support_coordination.py` | `75bf30a8a1cbc857bda86bd0ac85111857e38f8f` | same |
| `tests/contract/test_support_handoff.py` | `0fc854e085f19a0d2367bd5290d7e8e4b398bc98` | same |

The staged path set and all three staged objects were verified before commit; `git diff --cached
--check` exited `0`. No product, dependency, workflow, data/model/output, agent-owned guidance,
coordination, tag, release, or index path changed.

## Findings and durable dispositions

Claude's v1 review found that applicable `unknown`/`unavailable` checks could exit `0` and that the
tracked-digest test assumed the correct Git worktree. Codex accepted both findings before any target
write. Published v2:

- returns nonzero for applicable `failed`, `unknown`, and `unavailable` states;
- keeps deliberate `passed`, `skipped`, `not-run`, and `not-configured` states non-failing;
- skips the tracked-digest invariant outside Git;
- requires Git top-level to equal the candidate root before `git ls-files`, loudly rejecting an
  enclosing repository rather than silently hashing the wrong tree.

The non-blocking `--no-record` observation was accepted without scope expansion: no current check
writes history and focused coverage pins the tracked-content invariant.

## Clean-A validation

- Support aggregate `--no-record`: exit `0`; coordination `passed` with 0 errors/0 warnings;
  bootstrap handoff `not-configured`; one schema `passed`; focused contract support 5/5 `passed`;
  native optional and hosted CI `not-run`.
- Direct installed coordination validation: exit `0`, 0 errors, 0 warnings; BOARD byte-identical.
- Missing-native executable probe: applicable native check `unavailable`, aggregate exit `1`.
- Product interpreter as support operator: coordination `unavailable`, aggregate exit `1`.
- Native layers with external output/cache roots: core-unit 42/42, contract 30/30,
  state-integrity 3/3, all exit `0`.
- Final porcelain: empty.

## Evidence commit B

Commit `d5dc65e568ee73d82389e6e1d3fdf24122661adf` has parent A and modifies exactly:

| Path | SHA-256 | Committed object |
|---|---|---|
| `support/log.md` | `6E014AF466240E3CE3297E21E1CB8C1F02EF9149E3DA0818837C09D5970FA4D0` | `e4e771ef9045dc7d0b8e956081603cb104598cc3` |
| `support/current-status.md` | `F1C2919349ADF00D1FA8F36D9ECFAB96B16CBB881A6C59745F53933E428DC3BE` | `5279b928b44fdf0cfd0c89110afb081e01b62b8e` |

The exact authority is [`rendered/loto-slice6-evidence-b/`](rendered/loto-slice6-evidence-b/),
produced by [`rendered/render_loto_slice6_evidence_b.py`](rendered/render_loto_slice6_evidence_b.py),
SHA-256 `E57400486991BF51F7C96EED69346C1EC18ED73CF81B4C6C36C6485EC393A4AF`.
The renderer derives `support/log.md` from committed A, proves the published prefix is intact, and
adds exactly two canonical events (2 additions, 0 deletions). Both staged objects matched the
authority before commit; staged diff check exited `0`.

## Clean-B validation

The complete clean-A matrix was repeated at B with the same literal results: aggregate exit `0`,
coordination 0/0, bootstrap handoff `not-configured`, schema/focused checks passed, optional/hosted
not-run, both unavailable operator probes exit `1`, native 42/30/3 all exit `0`, board byte-identical,
and porcelain empty. `B^ == A`; A has exactly three paths; B has exactly two.

Optimizer-core, integration, webapp, and optional layers were not made applicable and were **not
run**; they are not reported as passed. Every command in the target implementation phase succeeded
on its first invocation; the earlier packet sandbox denial and v1 review findings remain recorded in
the pre-write evidence and target log rather than being excluded.

## Reviewer handoff and recovery

No push is authorized by this record. Claude must independently review commit identities, parent
chain, exact path sets, committed objects against Wiki authorities, append-only log behavior,
fail-closed semantics, validation truth, and clean `0/2` state. On acceptance, Codex may push exactly
A followed by B as one normal fast-forward and report live state. Recovery, only on reviewer/owner
direction, is a new revert of B followed by A. Aggregate milestone validation, rollback evidence,
guidance alignment, and M4 remain closed.
