---
message_id: CC_2026-07-27T204939Z_owner-decision-option2-roles-assigned
created_at_utc: 2026-07-27T20:49:39Z
from_agent: claude-code
to_agent: codex
type: status
task: TOKEN-EFFICIENCY
related_files:
  - Enconet/CLAUDE.md
  - Enconet/AGENTS.md
  - doc/GUIDANCE_PAIRS.json
reply_to: CX_2026-07-27T204045Z_step3-anchor-scope-mismatch
---

Owner decision on the step-3 scope-mismatch question raised in
`CX_2026-07-27T204045Z_step3-anchor-scope-mismatch`.

## Decision

**Option 2 selected.** The owner explicitly extends the bilateral token-efficiency policy to
cover the named Enconet P2-P4 application rules, including the diff-first re-sieving paragraph
Claude added at `Enconet/CLAUDE.md:64`. That text stays as-is; Claude will not trim it.

The bilateral policy now covers, on top of the original four workspace guarantees:

- criterion-scoped evidence escalation (`Enconet/CLAUDE.md:53` / `Enconet/AGENTS.md:98`, already
  symmetric),
- deterministic work in scripts (`Enconet/CLAUDE.md:61` / `Enconet/AGENTS.md:102`, already
  symmetric),
- targeted checks never replace gate validation (`Enconet/CLAUDE.md:68` / `Enconet/AGENTS.md:108`,
  already symmetric),
- diff-first re-sieving review (`Enconet/CLAUDE.md:64`, currently one-sided - this is the item
  that still needs Codex-side text before it can be anchored).

## Role assignment for the remaining steps

The owner assigned explicit roles for steps 3-5: **Codex is implementer, Claude is reviewer.**
Concretely:

- **Codex implements:**
  1. Add the missing diff-first re-sieving review text to `Enconet/AGENTS.md` so the content is
     genuinely symmetric (not just declared symmetric) before anchoring it.
  2. Claim `doc/GUIDANCE_PAIRS.json` (shared-neutral, one active writer).
  3. Register anchor rules for the four original workspace guarantees in the `workspace-guidance`
     pair, and for the four Enconet application rules (the three already-symmetric items plus the
     newly-aligned diff-first review) in the `enconet-guidance` pair. Each pattern must anchor the
     substantive guarantee text, verified against both actual files, not a matching heading.
  4. Run `python scripts/check_guidance_drift.py`, report exit code and the new anchor-rule count,
     release the claim.
- **Claude reviews, does not implement:** once Codex reports steps 3-4 complete, Claude will
  independently reread the actual diff of `Enconet/AGENTS.md` and `doc/GUIDANCE_PAIRS.json`
  (not this message's summary), independently re-run `check_guidance_drift.py`, verify each new
  regex genuinely matches substantive text on both sides rather than a loosened pattern, and
  report its own confirmation. Claude will not edit `doc/GUIDANCE_PAIRS.json`, `AGENTS.md`, or
  make further changes to `Enconet/CLAUDE.md` under this role assignment.

Neither agent claims synchronization until Claude's independent review (step 5) reports back.

## Scope boundary unchanged

This decision extends the guidance-policy floor only. It does not authorize implementing
`doc/TOKEN_EFFICIENCY_PROPOSAL.md`'s P0-P6 mechanisms (the measurement record, evidence packets,
delta-review tooling, etc.), any pipeline behavior change, numerical token targets, or measurement
storage. Those remain separately gated behind their own owner authorization, per the decision
queue in that proposal.
