# T6 validation, recovery, and milestone-gate contract v1.0

## Scope and sequencing

This planning-only contract defines the target-ready T6 package: target-native support
aggregates (T6.1), architecture guardrails (T6.2), the M2-M5 milestone-packet contract (T6.3),
and scoped-recovery proof (T6.4). It does not publish to CC_FIN or CC_Loto and authorizes no
target write. M2 continues to gate every FIN write; M3 continues to gate Loto publication. The
staged executable prototypes and their disposable-root tests that back T4.1-artifact, T4.3,
T5.2, and T6.4 live under `doc/support-transfer/staged/` and are recorded separately in
`T6_STAGED_EXECUTABLE_CHECKPOINT.md`; this document is the design contract they implement
against.

## Task T6.1 — target-native support aggregates

Each target composes support checks with its own native contract; neither target adopts the
other's tool assumptions and neither adopts a Wiki assumption.

| Target | Native contract composed | Support checks added |
|---|---|---|
| CC_FIN | pytest, optional CPI, targeted ruff, existing CI | coordination validator, handoff-record validator, support-schema validator |
| CC_Loto | layered `run_tests.py`, optional-dependency semantics | coordination validator, handoff-record validator, support-schema validator |

Requirements:

- The aggregate runner is one small script per target (`scripts/validate_support.py` for FIN,
  `tools/validate_support.py` for Loto per D-13) that calls the target's existing native command(s)
  unmodified and then the shared-neutral support validators; it does not reimplement native test
  discovery or add a second test framework.
- Output is deterministic: identical repository state produces identical pass/fail per check: no
  network calls, no timestamps in comparison logic, no unordered set iteration in reported output.
- The aggregate returns non-zero if any applicable check fails; `not-configured` and `skipped`
  checks never cause a non-zero exit by themselves and never render as `passed`.
- A `--no-record` (or equivalent) mode exists for every check that otherwise mutates history
  (event log, validation-run manifest); this mode changes no tracked file.
- The truthful check vocabulary is exactly the T5 table (`passed`, `failed`, `skipped`,
  `not-run`, `unknown`, `not-configured`, `unavailable`); `blocked` remains a handoff/blocker
  state, never a check result.

## Task T6.2 — architecture guardrails

Guardrails are advisory signals that trigger review, not blind mechanical action.

- **God-component signal:** a support module accumulates more than one reason to change (for
  example a validator that also renders Markdown and also shells out to Git porcelain parsing)
  triggers a decomposition review; the review may keep the module if splitting would create a
  premature abstraction with only one caller.
- **New-abstraction rule:** a shared helper is justified only by naming its demonstrated
  consumers (this contract requires exactly two: CC_FIN and CC_Loto) and the concrete
  duplication or layer it removes; a helper with one consumer stays local to that target.
- **Scale-triggered change:** any change motivated by record volume, concurrency, or retention
  cites the approved scale assumption from `GAP_COLLISION_SENSITIVITY_MATRIX.md` or a newly
  measured bottleneck with evidence; it is never added speculatively.
- **Coupling/complexity checks are advisory by default.** A target's M1-approved profile may
  promote a specific check to blocking; until then a guardrail finding is recorded (AFI or
  review note) and does not by itself fail the aggregate.
- Guardrail findings use the T3 AFI/lesson taxonomy; a guardrail is never a silent veto with no
  durable record.

## Task T6.3 — milestone packets M2-M5

Every milestone packet (`templates/milestone-packet.template.md`) is a Claude/Codex-prepared,
owner-decided record; neither agent may record its own approval.

Required packet sections, mirroring the accepted M1 packet shape:

1. **Decision requested** — exact gate, exact target/baseline SHA(s), and what the decision
   does and does not authorize.
2. **Evidence bundle** — links to every upstream record the decision depends on (no evidence is
   restated only summarized-and-linked).
3. **Recommended decision set** — a numbered, individually approvable/deferrable list.
4. **Risks and controls** — risk, control, and the residual owner choice, one row per risk.
5. **Alternatives** — approve, partially approve, defer, and reject, each naming the concrete
   consequence.
6. **Recovery impact in plain language** — what a failed publication slice costs and how it is
   undone, without jargon.
7. **Owner decision record** — left blank in the candidate packet; filled in only by the owner's
   actual decision, never inferred from silence or elapsed time.

Gate-specific evidence requirements:

| Gate | Minimum evidence before packet preparation |
|---|---|
| M2 (authorize FIN publication) | FIN support profile (already M1-accepted), a dry run against the exact publication manifest, a recorded recovery point, target-native baseline checks, and the staged-executable evidence in `T6_STAGED_EXECUTABLE_CHECKPOINT.md` |
| M3 (accept FIN / authorize Loto) | FIN aggregate evidence (T6.1 runner, all applicable states truthful), independent Claude review, a rollback test/evidence from a real or disposable rehearsal, and captured lessons |
| M4 (accept Loto) | Loto aggregate evidence, independent review, rollback test/evidence |
| M5 (close transfer) | T9 conformance/difference reports and both targets' final handoffs |

Agents prepare and may recommend; only the human owner approves, rejects, or defers a gate. A
packet without an owner decision record authorizes nothing.

### Template placeholders

`templates/milestone-packet.template.md` allows exactly: `{{GATE_ID}}`, `{{DECISION_SCOPE}}`,
`{{TARGET_NAME}}`, `{{TARGET_BASELINE_SHA}}`, `{{EVIDENCE_VERSION}}`, `{{AUTHORIZATION_SCOPE}}`,
`{{BASELINE_VERIFICATION_STATEMENT}}`, `{{EVIDENCE_BUNDLE_LINKS}}`,
`{{RECOMMENDED_DECISION_ITEMS}}`, `{{RISK_CONTROL_ROWS}}`, `{{APPROVE_CONSEQUENCE}}`,
`{{PARTIAL_CONSEQUENCE}}`, `{{DEFER_CONSEQUENCE}}`, `{{REJECT_CONSEQUENCE}}`,
`{{RECOVERY_IMPACT_STATEMENT}}`, and `{{OWNER_DECISION_RECORD}}`. Rendering fails on an unresolved
or unknown placeholder; multi-target gates (M2/M3 span FIN only, M4 spans Loto only) repeat the
target row rather than inventing new placeholders.

## Task T6.4 — scoped recovery rehearsal

`PUBLICATION_ROLLBACK_MANIFESTS.md` (T2.4) already defines the preflight, recovery point, commit
shape, abort triggers, and scoped-rollback procedure. T6.4 requires proof, not restatement:

- The rehearsal runs in a disposable root: a temporary Git repository seeded with a
  target-shaped fixture tree (unrelated pre-existing files plus a placeholder native check),
  never CC_FIN or CC_Loto.
- The rehearsal publishes a multi-commit support slice (neutral skeleton, then coordination,
  then handoff) grouped exactly as `PUBLICATION_ROLLBACK_MANIFESTS.md` specifies, injects a
  failure partway through the slice, and aborts.
- Scoped rollback then removes or reverts only the slice's own commits/paths; the rehearsal
  asserts that pre-existing and concurrent unrelated files, and their content, are byte-identical
  before and after.
- Post-rollback verification re-runs the placeholder native check and the coordination/handoff
  validators against the recovered tree and records their literal states.
- Evidence is the rehearsal's exact commands, exit codes, and the before/after file-hash
  comparison; a narrative description alone does not satisfy T6.4.

## T6 semantic acceptance

- T6.1-T6.4 are specified target-locally, with no Wiki-repository runtime dependency and no
  shared code/doc index requirement.
- The truthful check vocabulary, guardrail-as-signal-not-veto rule, packet structure, and
  rehearsal proof requirement are unambiguous and testable.
- Milestone-packet approval remains exclusively an owner action; no agent records its own
  approval.
- No target repository was modified in the preparation of this contract.
