# T4 paired-agent coordination bootstrap contract v1.0

## Scope and sequencing

This planning-only contract defines the target-ready T4 coordination package. It does not publish
to CC_FIN or CC_Loto. Neutral coordination must be installed and validated before either agent
publishes owned guidance or claims paired synchronization. M2 still gates every FIN write; Loto
writes remain blocked until M3.

## Target-local structure

```text
coordination/
  TEAM_PROTOCOL.md
  BOARD.md
  schemas/
    message.schema.json
    claim.schema.json
    resolution-manifest.schema.json
  templates/
    message.template.md
    claim.template.yml
    resolution-manifest.template.md
    guidance-semantics.template.md
  messages/
  archive/
  claims/
```

`BOARD.md` is generated and never authoritative history. Empty `messages/`, `archive/`, and
`claims/` directories receive tracked README placeholders until their first record. Validators and
status generation later use FIN `scripts/` and Loto `tools/` under D-13.

## Ownership

| Surface | Owner | Cross-agent rule |
|---|---|---|
| `AGENTS.md`, `.agents/`, `CX_` records | Codex | Claude may read/validate, not edit/archive/re-index |
| `CLAUDE.md`, `.claude/`, `CC_` records | Claude | Codex may read/validate, not edit/archive/re-index |
| `coordination/TEAM_PROTOCOL.md`, schemas, templates, validators | Shared-neutral | Change under non-overlapping claim and review |
| `coordination/BOARD.md` | Generated shared-neutral | Regenerate; never hand-edit as history |
| Claims | Owned by claiming agent | Other agent may validate and report collision, not rewrite |

An owner may archive only its own prefix after resolution is confirmed. One agent cannot declare
the other agent's guidance, adapters, index, messages, or synchronization complete.

## Message contract

Messages are immutable Markdown records with validated frontmatter. IDs and filenames are
`<PREFIX>_<UTC compact timestamp>_<kebab-topic>.md`; `PREFIX` is `CX` or `CC`. Required metadata is
defined by `message.schema.json`. Corrections and acknowledgements create a new message with
`reply_to`; no record is rewritten.

Types are `note`, `question`, `blocker`, `review_request`, `acknowledgement`, `claim`, and `status`.
Every related path is repository-relative and cannot traverse outside the target. Message content
must exclude secrets, credentials, personal data, private path values, and prohibited product data.

## Lifecycle

| State | Meaning | Required evidence |
|---|---|---|
| Active | Action, answer, review, or confirmation remains | Record is in `messages/` |
| Resolved | Proposed outcome exists | Reply/evidence names the outcome |
| Confirmed | Recipient, owner, or independent evidence confirms resolution | Immutable acknowledgement, owner decision, or reproduced validation |
| Archived | Terminal, confirmed, and removed from active queue | Original intact plus immutable resolution manifest in `archive/` |

Moving a record does not change its content or ID. The resolution manifest names every archived
record, outcome, and confirmation evidence. Active directories contain unresolved work only.

### Blockers

A blocker leaves the active queue only with one explicit disposition:

- `resolved`, with validation evidence;
- `owner-accepted`, with the durable owner decision and residual risk; or
- `deferred-until`, with an objective condition/date and owner.

Silence, expiry, a commit, or an agent's confidence is not a blocker disposition.

## Claim contract

Claims reserve a task and anticipated paths for one agent until release or expiry. An active claim
fails if any anticipated path overlaps another active claim by exact path or ancestor/descendant
scope. Claim expiry removes exclusivity but does not imply completion, rollback, or safe takeover.
Before takeover, the next agent checks Git, status, handoff, messages, and unfinished artifacts.

Claim files are immutable as historical facts except for schema-defined lifecycle fields added by
the owning coordination tool (`last_renewed_at_utc`, `released_at_utc`, status). Manual rewriting is
forbidden.

## Board contract

The generated board lists active/released claims, active messages, current handoff pointer, archive
count, and generation timestamp. Validation recomputes the expected board and fails on staleness.
The board cannot approve a gate, resolve a blocker, prove a check passed, or replace source records.

## Guidance pairing

The common semantic anchors are: read order, authority hierarchy, ownership, message lifecycle,
claims, review/reproduction, truthful validation states, safe recovery, session start/close, and
target-write gates. Tool-specific command syntax may differ if a drift manifest names the semantic
anchor, both implementations, rationale, owner, verification, and reconsideration trigger.

- Claude alone authors the new CC_FIN Claude-owned payload during the gated FIN publication.
- Codex alone authors the new CC_Loto Codex-owned payload during the gated Loto publication.
- Existing CC_FIN Codex and CC_Loto Claude guidance remain unchanged unless their owner changes it.
- Planning templates describe shared semantics only and are not agent discovery infrastructure.

No side may claim synchronization until neutral validation passes and the counterpart explicitly
confirms its own side.

## Template placeholders

The coordination templates allow exactly these placeholders:

- target configuration: `{{PROJECT_NAME}}`, `{{AGENT_OWNERSHIP_SUMMARY}}`,
  `{{SUPPORT_PROFILE_PATH}}`;
- Codex/Claude anchor text: `{{CODEX_READ_ORDER}}`, `{{CLAUDE_READ_ORDER}}`,
  `{{CODEX_OWNERSHIP_TEXT}}`, `{{CLAUDE_OWNERSHIP_TEXT}}`, `{{CODEX_VALIDATION_TEXT}}`,
  `{{CLAUDE_VALIDATION_TEXT}}`, `{{CODEX_RECOVERY_TEXT}}`, `{{CLAUDE_RECOVERY_TEXT}}`,
  `{{CODEX_GATE_TEXT}}`, `{{CLAUDE_GATE_TEXT}}`;
- documented differences: `{{READ_ORDER_DIFFERENCE}}`, `{{OWNERSHIP_DIFFERENCE}}`,
  `{{VALIDATION_DIFFERENCE}}`, `{{RECOVERY_DIFFERENCE}}`, `{{GATE_DIFFERENCE}}`;
- verification: `{{READ_ORDER_CHECK}}`, `{{OWNERSHIP_CHECK}}`, `{{VALIDATION_CHECK}}`,
  `{{RECOVERY_CHECK}}`, `{{GATE_CHECK}}`.

Rendering fails on an unresolved or unknown placeholder. Each agent authors only its owned text;
the renderer cannot synthesize counterpart guidance.

## Validator and test contract

The target-local validator must fail non-zero for:

- malformed/duplicate IDs, filenames, timestamps, prefixes, types, paths, or unknown fields;
- unresolved `reply_to`, self-reply, or reply cycles;
- cross-agent archival or record-prefix ownership violations;
- blockers archived without an allowed disposition and confirmation evidence;
- missing/malformed resolution manifests or manifests referencing active/missing records;
- overlapping active claims, invalid renewal/release order, or inconsistent expiry;
- stale/generated-board differences;
- one-sided synchronization claims;
- prohibited sensitive content patterns.

Tests include positive lifecycles and negative fixtures for every failure above. A no-record status
and validation mode must not create messages, claims, board history, caches in tracked paths, or
other evidence records.

## Planning acceptance

- Structure, ownership, lifecycle, blockers, claims, board, guidance pairing, and validator behavior
  are explicit and target-local.
- Templates/schemas contain no target secrets, Wiki-domain workflow, or runtime Wiki dependency.
- Agent-owned payload creation remains assigned to its owner and gated target publication.
- No target repository was modified.
