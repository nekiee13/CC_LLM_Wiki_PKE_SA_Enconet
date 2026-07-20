---
record_type: disposable_dry_run_evidence
target: CC_Loto
slice: claude-guidance-alignment
step: 2
recorded_at_utc: 2026-07-20T03:36:40Z
target_parent: a4ccbe144a2027745e74215e2136dbe6fe610497
---

# CC_Loto Claude-owned minimal alignment — disposable dry-run evidence

## Result

The exact one-path candidate overlays cleanly on the published step-1 tree under a short disposable
`%TEMP%\lca-*` root. `CLAUDE.md` is the sole modification and there is no create. CC_Loto stayed
clean, unchanged, and synchronized at `a4ccbe14` throughout.

| Check | Result | Disposition |
|---|---:|---|
| Exact candidate paths | 1 | passed |
| Parent-blob derivation (pure append proven structurally) | enforced | passed |
| Diff against reviewed parent blob | 55 added / 0 removed | passed |
| Installed schema check vocabulary read and pinned | 7 states, no `blocked` | passed |
| Section enumerates check states in prose | 0 | passed |
| Defective enumerations present | 0 | passed |
| Blocked-state boundary stated | yes | passed |
| Synchronization overclaim | 0 | passed |
| Synchronization precondition stated | yes | passed |
| Pre-existing product anchors retained | 7/7 | passed |
| Codex-owned `AGENTS.md` in overlay | byte-identical to published object | passed |
| Installed coordination validation on overlay | exit `0`, 0 errors, 0 warnings | passed |
| Generated board after overlay | byte-identical | passed |
| Section links resolve in target | all; none escape | passed |
| Placeholder/sensitivity/foreign-token checks | 0 findings | passed |
| Fixed rerender differences | 0 | passed |
| Target HEAD/origin divergence | `0 0` | passed |
| Target porcelain after checks | empty | passed |

## Native short layers in the disposable overlay

The isolated target-requirements interpreter ran the native runner with output and model-cache paths
redirected inside the disposable root:

| Layer | Tests | Exit | Result |
|---|---:|---:|---|
| `core-unit` | 42 | 0 | passed |
| `contract` | 30 | 0 | passed |
| `state-integrity` | 3 | 0 | passed |
| Required short-layer total | 75 | 0 | passed |

Optional, optimization-core, integration, webapp, and hosted CI were **not run**: a
documentation-only guidance change makes no integration applicable. That is a not-run state, never a
pass, and it is not evidence about product-suite health.

## Failed and corrected attempts

Two, both disclosed rather than omitted:

1. The first renderer invocation exited `1` with `KeyError: 'properties'` while reading the check
   vocabulary. The schema expresses `checks[].items` as a `$ref` to `#/$defs/check` rather than an
   inline object, and my accessor assumed the inline shape. No candidate was produced and no pass was
   claimed. The renderer was corrected to assert the `$ref` target explicitly and resolve it, which
   is stricter than the original guess.
2. An initial `git diff --numstat` measurement reported `56 1` because it compared the candidate
   against a PowerShell-redirected copy of the parent rather than the Git blob; the redirection
   altered the file. The corrected comparison against the blob returns `55 0`. The incorrect figure
   is disclosed here rather than silently replaced.

Neither attempt wrote the live target.

## Stop conditions

Stop before any CC_Loto write on target drift, dirty status, a second changed path, any non-append
change to the parent bytes, byte mismatch, a prose enumeration of check states, a defective
enumeration, an unauthorized synchronization claim, loss of a pre-existing product anchor, any
modification of Codex-owned or shared-neutral content, non-zero coordination validation, board
change, native regression, sensitive or product data, dangling/escaping link, or reviewer finding.
