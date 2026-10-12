---
record_type: guidance_alignment_comparison
target: CC_Loto
target_tip: d5dc65e568ee73d82389e6e1d3fdf24122661adf
recorded_at_utc: 2026-07-20T02:43:36Z
prepared_by: codex
target_write: none
---

# CC_Loto guidance-alignment comparison

## Frozen inputs

| File | Owner | Git object at target tip |
|---|---|---|
| `AGENTS.md` | Codex | `34b7eb93095022bea137e2a0c2313f356bfa0f28` |
| `CLAUDE.md` | Claude Code | `3edd87504e76a97d8ba46ecf40e81b8ad894299f` |

The target was read-only during comparison. Local HEAD and fetched `origin/main` were
`d5dc65e568ee73d82389e6e1d3fdf24122661adf`, divergence was `0 0`, and porcelain was empty.

## Meaning of synchronization

Synchronization does **not** mean byte-identical agent files. Each file retains agent-specific
commands and product guidance. For this decision, the pair is semantically synchronized only when
both files consistently expose the safety-critical shared support contract to their own agent.

## Shared-contract matrix

| Required semantic anchor | `AGENTS.md` | `CLAUDE.md` |
|---|---|---|
| Agent-owned versus shared-neutral path boundary | Present | Absent |
| Support-oriented session read order | Present | Absent |
| Immutable message/claim and owner-specific archive lifecycle | Present | Absent |
| “Check messages” requires evidence before acceptance | Present | Absent |
| Target-local coordination command and generated BOARD rule | Present | Absent |
| Literal validation-state reporting and support/native interpreter boundary | Present, but one vocabulary defect exists | Absent |
| Named-commit, revert-first recovery and unrelated-work preservation | Present | Absent |
| M4 cannot be inferred from completed work | Present | Absent |

`CLAUDE.md` remains useful and factually correct as product-development guidance: it describes the
package, entry points, layered test runner, configuration, optional dependencies, and product
invariants. The gap is limited to support-workflow safety and governance, not product knowledge.

## Existing durable disclosure

The published `support/current-status.md` explicitly states that the pair is not synchronized and
that adding support workflow to `CLAUDE.md` is an owner-scoped decision. The earlier Claude-owned
guidance correction changed only a false packaging statement and deliberately did not claim broader
alignment.

## Minimum alignment target

If approved, a concise Claude-owned section should cover these six groups without copying all of
`AGENTS.md`:

1. ownership and shared-neutral boundaries;
2. support-oriented read order and live-Git preflight;
3. immutable coordination lifecycle, including evidence-backed message handling;
4. target-local support validation and the exact check vocabulary: `passed`, `failed`, `skipped`,
   `not-run`, `unknown`, `not-configured`, and `unavailable`; `blocked` remains a handoff/blocker
   state and is never a check result;
5. named-commit, revert-first recovery with unrelated-work preservation;
6. explicit owner gates, including that M4 is never inferred.

Detailed mechanics should continue to live in `support/README.md`, `support/PROFILE.md`, and the
installed tools. This keeps the two guidance files semantically consistent while limiting duplicated
text and future drift.

## Codex-side factual defect found

`AGENTS.md` line 86 currently tells Codex to report checks as `passed`, `failed`, `skipped`,
`unavailable`, `blocked`, `unknown`, or `not run`. This conflicts with the accepted T6 contract, installed
aggregate, and handoff schema: it wrongly includes `blocked` as a check result and omits
`not-configured`. Alignment must not copy this defect. If the owner approves alignment, a separate
Codex-owned correction should first replace that sentence with the exact canonical vocabulary; Claude
reviews that slice independently.

The other `blocked` occurrence, line 129's warning never to report a validation as passed when it was
blocked, is not a check-vocabulary declaration. It correctly describes an execution prevented by a
real blocker and remains outside the correction. The later renderer must pin the exact corrected
enumeration rather than require the word `blocked` to disappear from the whole file.

## Other exclusions

- No `.agents/` or `.claude/` change is required by the minimum alignment target.
- No product, dependency, test, workflow, data/model/output, support record, tag, release, or index
  change is implied by this comparison.
- This comparison neither approves a Claude-owned edit nor establishes synchronization.
