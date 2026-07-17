---
record_type: design_checkpoint
scope: T6
recorded_at_utc: 2026-07-17T01:30:00Z
status: partial
completed_criteria: T4.1-artifact, T4.3, T5.2 (staged level only)
target_mutation: none
publication_gate: M2
---

# T6 staged-executable checkpoint

## Control

- Claim: `SUPPORT-TRANSFER-T6-DESIGN` (claude-code).
- Design contract: `T6_VALIDATION_RECOVERY_GATE_CONTRACT.md`.
- Staged artifacts: `doc/support-transfer/staged/`.
- Reviewer: Codex (this session reverses the usual writer/reviewer roles by
  explicit owner instruction; Codex is asked to independently reproduce
  everything below, not to take it on trust).

## What this checkpoint closes

Per the accepted T4/T5 review boundary, T4.1-artifact, T4.3, and T5.2 were
explicitly pending "executable staged artifacts plus positive and
fault-injection tests in disposable roots." That evidence now exists:

| Artifact | Backs | Design contract |
|---|---|---|
| `staged/coordination_validator.py` | T4.1-artifact, T4.3 | `T4_COORDINATION_BOOTSTRAP_CONTRACT.md` "Validator and test contract" |
| `staged/handoff_publisher.py` | T5.2 | `T5_HANDOFF_CONTINUITY_CONTRACT.md` "Deterministic publication protocol" and "Test contract" |
| `staged/tests/test_recovery_rehearsal.py` | T6.4 | `T6_VALIDATION_RECOVERY_GATE_CONTRACT.md` Task T6.4 |

Every module is parameterized entirely by a target root passed at the call
site; none imports or path-references anything outside `staged/`, so the same
files can later be copied unmodified into a target's `scripts/` or `tools/`
tree (T4.2/T7/T8) without edits.

## Corrections after independent review (T6-R1..R7)

Codex's review `CX_2026-07-17T214844Z_t6-staged-review-findings` did not accept the
original checkpoint (51/52 reproduced in its environment). All seven findings were
independently reproduced and corrected:

- **T6-R1** `collect_git_state` now reports the supplied target root itself and never
  adopts an enclosing repository's identity; the suite now passes with pytest's
  basetemp inside or outside the Wiki worktree.
- **T6-R2** `handoff.schema.json` accepts 40- or 64-hex HEADs and rejects
  `status: complete` with `git_state: absent`/`unknown`; `validate_record` enforces the
  same rule, and a code-versus-shipped-schema agreement test pins both to the same
  verdicts on the review's probe cases.
- **T6-R2b** (second-round finding) the shipped schema is now authoritative at
  publication: `publish()` validates the fully normalized record against the
  target-local `support/schemas/handoff.schema.json` after the handwritten checks and
  before any write; a missing schema refuses publication rather than degrading. The schema's `absent` rule now requires
  `root`, `branch`, and `head` all null (closing the absent+fabricated-root
  divergence), and the complete-with-failed-check rule is encoded in the schema's
  `allOf`. Regressions: absent+fabricated-root rejected by code, schema, and
  publication; a bare target without the schema refused; a target whose installed
  schema is stricter than the handwritten checks blocks publication (schema verdict
  alone suffices to refuse). Audit note: the sensitive-content scan, the exact
  `created_at_utc` timestamp format, and record/pointer identity re-verification
  remain code-side checks the schema cannot express; because publication requires
  BOTH verdicts, every remaining asymmetry fails closed (a record either side
  rejects cannot publish).
- **T6-R2c** (third-round finding) the `schema_path` override introduced by the R2b
  fix was itself a bypass surface — an external permissive schema could override a
  stricter installed one. The override is removed entirely: publication always loads
  `root/support/schemas/handoff.schema.json` and nothing else, with a regression
  proving an attempted override is refused (`TypeError`) before any write while the
  installed stricter schema still governs.
- **T6-R3** `compare_staleness` now covers `upstream_relation` and `worktree`.
- **T6-R4** one-sided synchronization claims are validator errors (non-zero exit), and
  claim overlap detects exact, ancestor/descendant, and mixed-separator collisions;
  negative tests added for both, plus a disjoint-sibling non-collision case.
- **T6-R5** the generated board names the current handoff pointer.
- **T6-R6** the rehearsal seeds unrelated concurrent work after the recovery point
  (mid-slice), preserves it through the reverts, and verifies the recovered state with
  `git diff --name-only <recovery-point>..HEAD` == exactly the concurrent change plus a
  clean porcelain status.
- **T6-R7** immutable-record finalization is no-clobber (`os.link`); a concurrent
  same-ID record with different content fails publication instead of being overwritten,
  with a race fault test.

## Validation evidence

- **passed** — staged test suite: command=`python -m pytest doc/support-transfer/staged/tests -q`
  (run from the Wiki workspace root); exit_code=0; 67 passed, 0 failed, 0 skipped.
- **passed** — environment-independence re-run (the T6-R1 scenario): command=
  `python -m pytest doc/support-transfer/staged/tests -q --basetemp=.tmp/t6-r2c-verify`
  (disposable roots inside the Wiki worktree); exit_code=0; 67 passed.
- **passed** — support schema validation: command=`python -c "Draft202012Validator.check_schema
  over doc/support-transfer/templates/**/*.schema.json"`; exit_code=0; four of four valid
  Draft 2020-12 after the T6-R2 edits.
- **passed** — standalone CLI smoke check: command=`python -c "..."` invoking
  `coordination_validator.main([root, '--write-board'])` against a fixture built the
  same way the pytest fixtures build it; exit_code=0; `validate: 0 error(s), 0 warning(s)`.
- Environment: Python 3.13.9, pytest 9.1.1, PyYAML 6.0.3, jsonschema 4.26.0 (already
  present in the default interpreter per C5.3; not newly installed).

### Failure modes exercised (positive + fault-injection, all in `tmp_path` disposable roots)

`coordination_validator` (33 tests) — every T4 "Validator and test contract" bullet:
malformed/duplicate/mismatched message IDs; unknown author prefix and other schema
violations (additionalProperties, enums, path-traversal patterns); invalid
`created_at_utc`; self-reply; two-node reply cycle; unresolved `reply_to`; unacknowledged
active blocker (plus the acknowledged-clean counterpart); archived message with no
covering manifest; `deferred-until` missing
`deferred_until`/`deferral_owner` (schema-rejected, reproducing the corrected T45-F2
fix) and the complete-fields positive case; manifest referencing a still-active
(unarchived) message; manifest referencing an unknown message; cross-agent archival
(manifest `resolved_by` disagreeing with its own filename prefix); overlapping active
claims by task and by file; invalid renewal/release order; inconsistent expiry;
sensitive content in a message body and in a claim note; stale and missing
`BOARD.md`; a bare root with no installed schemas; one-sided synchronization failing
closed (with the confirmed counterpart clean); ancestor/descendant and mixed-separator
claim collisions (with disjoint siblings clean); and the board naming the current
handoff pointer.

`handoff_publisher` (33 tests) — every T5 "Test contract" bullet applicable without a
target-native check harness: positive complete/partial/blocked publication; interruption
`before-record-write` (no trace left), `after-record-before-pointer` (orphan record,
retry adopts without rewriting), and `after-pointer-before-log` (retry logs exactly
once, never twice); duplicate record id with different content refused; every
malformed passed/failed/skipped/not-run check-state combination; `status: complete`
with a failed check refused ("never complete with an implied pass," reproducing the
T5 contract's authoring rule as an enforced check, not just documentation); `absent`
and `unknown` Git states with a fabricated HEAD refused (reproducing the corrected
T45-F1 fix); `current` state accepting both a 40-hex SHA-1 and a 64-hex SHA-256 HEAD
(closing the T4/T5 review's non-blocking SHA-1-only observation for the staged
artifact — no live effect since both real targets are SHA-1 today); a too-short HEAD
refused; sensitive content in the objective refused; a path-traversal artifact
refused; a hand-corrupted record missing a required heading refused on re-parse;
`status: complete` with `git_state: absent`/`unknown` refused (with `partial`+absent
accepted); the code-versus-shipped-schema agreement probes; the missing-schema,
stricter-installed-schema, and refused-external-override publication cases;
`collect_git_state`
returning `absent` for a non-Git directory and for a directory merely inside an
enclosing repository; the no-clobber race test; staleness reporting
upstream/worktree-only divergence; and, against a real disposable Git repository,
staleness comparison reporting a HEAD divergence after a second commit rather than
silently normalizing it.

`test_recovery_rehearsal.py` (1 test, T6.4) — a disposable Git repository seeded with
an unrelated pre-existing file and a placeholder native check; publishes a
neutral-skeleton-then-coordination slice with unrelated concurrent work committed
mid-slice by "another actor"; a third (handoff) step is attempted with a deliberately
failed check and refused by `handoff_publisher`'s own validation before any file is
written; scoped rollback then reverts only the two slice commits (`git revert`, never
`reset --hard`); the pre-existing and concurrent files are asserted byte-identical
(SHA-256) before and after; Git history is preserved (6 commits: baseline, skeleton,
concurrent, message, two reverts; the original recovery-point SHA remains in
`rev-list`); `git diff --name-only <recovery-point>..HEAD` names exactly the
concurrent change and porcelain status is clean; and post-rollback verification
re-runs the placeholder native check (passes) and `coordination_validator.validate`
(correctly reports the coordination schema as absent again, proving the recovered
state is genuinely clean rather than silently accepted).

## Explicitly pending

- **Target installation.** These are staged, disposable-root artifacts. T4.2 and
  target-installed T4.1/T5.3 still require copying the reviewed files into CC_FIN
  `scripts/` and CC_Loto `tools/` under their own claims at T7/T8; that is a target
  write and stays gated by M2/M3.
- **T6.1 target-native aggregate composition** (wrapping FIN's pytest/CPI/ruff/CI and
  Loto's `run_tests.py`) is specified in the design contract but not built here — it
  has no meaning until it wraps a real target's native commands.
- **T6.2 architecture guardrails** are specified as advisory review triggers in the
  design contract; they are not mechanically enforced by these staged artifacts and
  are not claimed as such.
- **T6.3 milestone packets** — the template exists
  (`templates/milestone-packet.template.md`); no M2-M5 packet has been drafted from it
  yet, and none of M2-M5 has an owner decision.
- **Session-start/close integration (T5.3)** is designed in
  `T5_HANDOFF_CONTINUITY_CONTRACT.md` but not built here; it depends on each target's
  own guidance-read order.
- No wholesale T4/T5/T6 completion is represented by this checkpoint. M2 continues to
  block every CC_FIN write; M3 continues to block CC_Loto publication.

## Authorization boundary

This checkpoint authorizes nothing beyond what it evidences: staged, disposable-root
artifacts and their test evidence. No target repository was read, written, or
otherwise touched in producing it. Codex review is requested before any master-plan
checkbox in `SUPPORT_SYSTEM_TRANSFER_MASTER_PLAN.md` is marked complete on this
evidence.
