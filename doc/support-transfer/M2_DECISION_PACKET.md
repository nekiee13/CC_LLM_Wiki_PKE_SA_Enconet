# M2 decision packet — authorize CC_FIN support publication

## Decision requested

Approve, revise, defer, or reject the first CC_FIN support-publication slices under the
M1-approved profile and manifest. Approval authorizes writing the manifest's named
support paths to CC_FIN in small isolated commits with the recorded recovery point; it
does not touch CC_Loto (M3), any product code, data, charts, or the Cockpit, and does
not itself approve the workflow branch-filter edit beyond M1 item 8's existing isolated
authorization.

| Target | Exact candidate baseline | Evidence version | What approval authorizes |
|---|---|---|---|
| CC_FIN | `238c207c73970f3d3c6dc00c2db5932ebeca7be4` | Profile v1.0 (M1); staged executables at `852d9e4` | Publication of manifest-listed support paths only, revert-only recovery |

Baseline reverified read-only on 2026-07-18: HEAD equals the M1-accepted SHA exactly,
worktree clean, synchronized with `origin/main`. No drift disposition is required.

## Evidence bundle

- Preflight facts, native baseline run, and dry-run collision check:
  `M2_PREFLIGHT_EVIDENCE.md`
- M1-accepted profile and manifest: `CC_FIN_SUPPORT_PROFILE.md`,
  `PUBLICATION_ROLLBACK_MANIFESTS.md`, `M1_APPROVAL.md`
- Accepted staged executables and rehearsal: `T6_STAGED_EXECUTABLE_CHECKPOINT.md`
  (Codex acceptance `CX_2026-07-17T222326Z`, 67/67 tests)
- Design contracts the publication implements: `T3_*`, `T4_*`, `T5_*`,
  `T6_VALIDATION_RECOVERY_GATE_CONTRACT.md`

## Recommended decision set

1. Accept the recovery point `238c207` and revert-only rollback for every slice.
2. Authorize publication of the neutral support skeleton (support index, status, log,
   decisions/ledgers) as slice 1, exactly per the manifest path list.
3. Authorize the coordination core (protocol, schemas, templates, empty queues,
   generated board, validator under `scripts/`) as slice 2.
4. Authorize the handoff core (schema, templates, `make_handoff`-equivalent publisher
   under `scripts/`, `HANDOFF.md` pointer) as slice 3.
5. Authorize focused support tests under existing `tests/` as slice 4, discovered by
   FIN's native pytest.
6. Record the native-baseline disposition: treat the 32 environment-caused
   failures/errors (torch, matplotlib) as `unavailable` on this machine, and accept
   the 22 pre-existing date-sensitive assertion failures as the recorded product
   baseline for support purposes — support slices must not change any of these counts
   in either direction; T7.3 verifies against this exact recorded set.
7. Keep the Codex-owned `AGENTS.md` support-navigation addition with Codex as author
   (agent-owned payloads stay with their owner), sequenced after the neutral slices.
8. Defer the `followup-ml-gate.yml` `master`→`main` correction to its own isolated
   commit under M1 item 8's existing authorization, with the exact one-line diff
   reviewed at publication time.
9. Claude implements the slices this cycle (session role reversal stands); Codex
   independently reviews each slice; neither marks T7 criteria without the other's
   review.

## Risks and controls

| Risk | Control | Residual owner choice |
|---|---|---|
| Baseline is not green in this environment | Truthful recorded baseline (item 6); support slices assert unchanged counts, never "fix" product tests | Accept recorded-baseline approach or require a green environment first |
| Support slice touches product behavior | Manifest path allowlist; per-slice preflight diff; T7.3 product-preservation check | Accept slice sequencing |
| Partial publication leaves inconsistent state | Small isolated commits; staged no-clobber/atomic tooling; accepted T6.4 rollback rehearsal | Accept revert-only recovery |
| Cross-agent ownership violation | Slices 1-4 are shared-neutral; agent-owned payloads authored only by their owner (items 7, 9) | Retain role assignments |
| Hosted behavior changes unnoticed | Workflow edit isolated to its own reviewed commit (item 8) | Authorize, defer, or reject item 8 timing |
| Date-sensitive product tests drift during publication window | Baseline set recorded at exact date/HEAD; T7.3 compares like-for-like | Accept comparison method |

## Alternatives

- **Approve recommended set:** slice publication begins immediately after this decision,
  each slice preflighted and independently reviewed.
- **Approve slices 1-4 only, defer 7-8:** neutral core lands; agent-owned guidance and
  the workflow fix wait for a later decision.
- **Defer:** nothing is written; evidence is preserved and the baseline reverified
  before a future decision.
- **Reject:** claims are released and CC_FIN remains untouched.

## Recovery impact in plain language

Every slice starts from the recorded clean commit `238c207` and adds only named support
files. If anything goes wrong, the slice is undone with a revert commit limited to that
slice; product files, history, and any concurrent work are untouched — this exact
procedure was rehearsed and independently accepted as T6.4 evidence. CC_Loto is not
touched at all until the separate M3 decision.

## Owner decision record

Pending. No approval, rejection, or deferral has been recorded. This packet authorizes
nothing until the owner's explicit decision is recorded here with a UTC timestamp.
