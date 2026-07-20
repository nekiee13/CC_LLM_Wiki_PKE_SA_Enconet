---
record_type: exact_render_evidence
target: CC_FIN
slice: claude-guidance
recorded_at_utc: 2026-07-20T20:06:00Z
target_parent: 9308e25bbd1177ba69b8075210e1c5e079213fc5
supersedes_parent: e74147f3309e1835d28d7c248e00cdcbde2f1796
authorized_by: ADR-SUP-0001 (accepted); implementation item - Claude-owned CLAUDE.md
implementer: claude-code
reviewer: codex
---

# CC_FIN Claude-owned guidance creation - exact-render evidence

## Parent refresh

This packet was first rendered against the decision tip `e74147f3` and accepted by Codex with no
finding. After the separately gated Codex-owned `AGENTS.md` completion published and closed at
`9308e25bbd1177ba69b8075210e1c5e079213fc5`, this evidence was refreshed against that new parent per
the agreed serialization. Because `CLAUDE.md` is a create, its bytes do not depend on the parent:
the candidate SHA-256 and Git object are unchanged across the reparent, and only the renderer's
parent/`AGENTS.md`-object preconditions moved.

## Control

- Target branch: `main`; local HEAD and `origin/main` at the published AGENTS-completion tip
  `9308e25bbd1177ba69b8075210e1c5e079213fc5`; divergence `0 0`; porcelain empty; zero tags.
- Renderer: [`rendered/render_fin_claude_guidance.py`](rendered/render_fin_claude_guidance.py),
  SHA-256 `080247C5350C30F58BEC1D79D16697215F2DF430EAF7E94971506CBE014513BD`.
- Exact byte authority:
  [`rendered/fin-claude-guidance/CLAUDE.md`](rendered/fin-claude-guidance/CLAUDE.md).
- Scope: one Claude-owned create, root `CLAUDE.md`; no other path. CC_FIN read-only throughout.

## Deterministic renderer

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python doc\support-transfer\rendered\render_fin_claude_guidance.py
```

Exit `0`. A second run reproduced the candidate with zero SHA-256 differences.

## Exact proposed bytes

| Operation | Target path | SHA-256 | Git object |
|---|---|---|---|
| create, Claude-owned | `CLAUDE.md` | `814DEE114C6F8AFECADCA0D4EEF78FAA99A9FFD1B19B0E0E55BE5E61B0B1781F` | `ecaf1abf5e7a7771d72166f17e4bd9c86c92831c` |

The candidate is 5062 bytes, LF-only (0 CR). `CLAUDE.md` is absent at the reviewed parent, so this
is a genuine create; the renderer refuses to run if the path already exists.

## Five shared meanings, from CC_FIN's own template

The renderer reads `coordination/templates/guidance-semantics.template.md` at the reviewed parent
and asserts its anchor set is exactly `read-order`, `ownership`, `truthful-validation`,
`safe-recovery`, `target-gates`. The candidate exposes all five to the Claude agent as a
`## Support system and coordination` section, plus a short product-orientation section that links
`README.md`, `docs/refactor/phase1_rules.md`, and `AGENTS.md` rather than restating them.

## Vocabulary pinned to executable authority

The section does not enumerate the check-state list. It references
`support/schemas/handoff.schema.json` as the authority; the renderer reads that schema, resolves
`#/$defs/check`, and requires the enum to equal exactly the seven canonical states, failing if the
schema ever admits `blocked`. The renderer's transcription guard fails only on three or more state
literals, so the one deliberate reference to the aggregate's `failed` failing-state is allowed while
a rival enumeration is not.

## Truthful statement of a current target limitation

CC_FIN's installed `scripts/validate_support.py` has `FAILURE_STATES = {"failed"}` and can emit
`unavailable`, so an applicable check it could not run is reported honestly in its printed output but
still yields exit `0`. The candidate states this limitation and instructs the reader to read the
printed states rather than trust the exit code. The renderer enforces both directions: it fails if
the aggregate has since become fail-closed (making the stated limitation stale), and it fails if the
candidate claims fail-closed behaviour the target does not have. This is the same defect class caught
in the CC_Loto Slice 6 review; it is disclosed here and is not fixed by this documentation slice.

## Ownership, scope, and native-path guarantees

- Codex-owned `AGENTS.md` is byte-identical to the source working tree in the disposable overlay,
  and the parent `AGENTS.md` object is required to equal `4cca3734` (the published AGENTS-completion
  object; it was `d04bf3b8` at the superseded decision-tip render).
- The candidate references only FIN-native paths (`scripts/agent_coord.py`, `python -m pytest`,
  `support/PROFILE.md`, `coordination/TEAM_PROTOCOL.md`); the renderer fails on any cross-target
  token (`tools/support/...`, `run_tests.py`, `--native-python`, `dynamix`, `CC_Loto`).
- No synchronization or alignment claim may appear; the section states the bilateral-confirmation
  precondition instead, and points at `support/decisions/` for the current decision state.
- No `.claude/`, `.agents/`, product, dependency, test, workflow, data, index, tag, or release path
  is in scope.
