# CLAUDE.md

Guidance for Claude Code working in this repository. Codex has its own instructions in
`AGENTS.md`; neither file replaces the other, and neither is a product requirements authority.

## Product orientation

Forecasting and Scenario Engine, currently in Path Stabilization (Phase-1). Canonical
implementation lives in `src/`; `compat/` is a delegation-only adapter layer; runnable entrypoints
live in `scripts/`. The public forecast boundary is `src.models.facade.ForecastArtifact`.

Authorities to read rather than restate: [README.md](README.md),
[docs/refactor/phase1_rules.md](docs/refactor/phase1_rules.md), and the detailed layout, style, and
completion rules already recorded in [AGENTS.md](AGENTS.md). This file does not duplicate them and
must not become a second backlog.

Native commands: `python -m pip install -r requirements.txt`, `python -m pytest`, and
`python -m ruff check src compat scripts tests tools`. Keep Phase-1 edits minimal and localized;
do not run repo-wide formatting sweeps.

## Support system and coordination

The repository-local support core is navigation and evidence. Controlling detail lives in
[support/README.md](support/README.md), [support/PROFILE.md](support/PROFILE.md), and
[coordination/TEAM_PROTOCOL.md](coordination/TEAM_PROTOCOL.md); where this summary and those
authorities disagree, the authorities win.

- **Ownership.** Claude Code owns `CLAUDE.md`, `.claude/`, and `CC_` coordination records. Codex
  owns `AGENTS.md`, `.agents/`, and `CX_` records. Read the other agent's files for context, but
  never edit, move, delete, archive, or re-index them; request changes through a coordination
  message. Coordination records without an agent prefix, schemas, templates, validators, the
  generated board, support records, and handoffs are shared-neutral: claim them before editing and
  take independent review.

- **Session start.** For support-oriented work read, in order: this file; `support/README.md` and
  `support/PROFILE.md`; `HANDOFF.md` and its immutable record once one is published;
  `support/current-status.md` and the append-only `support/log.md`; `coordination/BOARD.md`,
  unresolved `coordination/messages/`, and active `coordination/claims/`; then live Git state -
  branch, HEAD, upstream, divergence, worktree, and any unfinished or risky artifact. Verify that
  state against the records rather than trusting the records.

- **Coordination lifecycle.** Messages are immutable: correct or answer with a new `reply_to`
  record, never by rewriting a sent one. Claims reserve anticipated paths and must not overlap.
  Archive a message only once it is resolved **and** the counterpart has confirmed - silence is not
  confirmation - moving only `CC_` records under an immutable resolution manifest. Use
  `python scripts/agent_coord.py .` to validate, and regenerate the board through the installed CLI
  rather than hand-editing `coordination/BOARD.md`, which is generated state and never authority.
  When asked to check messages, inspect and independently verify actionable Claude-addressed
  messages in the same turn; never acknowledge acceptance without evidence.

- **Validation truth.** Report every check with its literal state from the vocabulary defined in
  [support/schemas/handoff.schema.json](support/schemas/handoff.schema.json) - that schema is the
  authority, not any prose copy of the list. `blocked` is a handoff and blocker state, never a
  check result. Never relabel a skipped, unavailable, not-run, or excluded check as passed, and
  never let an exit code stand in for a check that did not execute. Note a current limitation
  rather than assuming otherwise: `scripts/validate_support.py` treats only `failed` as a failing
  state, so an applicable check it could not run is reported honestly in its output but still
  yields exit `0`. Read its printed states; do not treat its exit code alone as proof that
  everything ran. Support checks compose with, and never replace, `python -m pytest`.

- **Safe recovery.** Capture parent, upstream, divergence, clean state, and allowed paths before
  any reviewed change. Recovery is a new `git revert` of the named commits after reviewer or owner
  direction; reset, force push, history rewriting, and broad cleanup are prohibited. Preserve
  unrelated and concurrent work, then re-run the support and applicable native checks and record
  literal commands and exit codes. A revert that conflicts with later work on the same append-only
  records requires owner-directed resolution.

- **Owner gates.** Milestone gates are the owner's decision and are never inferred from completed
  work, elapsed time, or independent review. Publishing files is not milestone acceptance, and a
  passing support check is evidence about the support system, not about the product test suite. Do
  not describe this repository's two agent guidance files as aligned or synchronized unless both
  are published and each agent has confirmed its own side at the live tip; `support/decisions/`
  records the current decision state.
