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
- Node-level baseline failure fingerprint (normative T7.3 comparison set):
  `M2_BASELINE_FAILURE_SET.md`
- Exact per-slice file inventory, existing-file dispositions, and disposable-copy
  render/validation evidence: `M2_DRY_RUN_MANIFEST.md`
- M1-accepted profile and manifest: `CC_FIN_SUPPORT_PROFILE.md`,
  `PUBLICATION_ROLLBACK_MANIFESTS.md`, `M1_APPROVAL.md`
- Accepted staged executables and rehearsal: `T6_STAGED_EXECUTABLE_CHECKPOINT.md`
  (Codex acceptance `CX_2026-07-17T222326Z`, 67/67 tests)
- Design contracts the publication implements: `T3_*`, `T4_*`, `T5_*`,
  `T6_VALIDATION_RECOVERY_GATE_CONTRACT.md`

## Recommended decision set

1. Accept `238c207` as the M2 recovery anchor: slice 1 starts there; each later slice
   records and verifies its own clean pre-slice parent HEAD and rolls back by reverting
   only its named commits to that parent — never a broad reset across accepted slices.
2. Authorize publication of the neutral support skeleton (9 files) as slice 1, plus the
   one-line link in `docs/README.md`, exactly per `M2_DRY_RUN_MANIFEST.md`.
3. Authorize the coordination core (14 files including `scripts/agent_coord.py` and
   `scripts/_support_shared.py`) as slice 2, per the manifest inventory.
4. Authorize the handoff core (7 files including `scripts/make_handoff.py` and the
   initial `HANDOFF.md` pointer) as slice 3, per the manifest inventory.
5. **Defer slice 4** (the `scripts/validate_support.py` T6.1 aggregate and the two
   focused support test modules): these artifacts are designed but not yet rendered
   (M2-RR2), so nothing is authorized for them here. They return as a separate
   authorization once rendered content, disposable-copy tests (truthful states,
   `--no-record`, non-zero composition), native pytest discovery evidence, and
   independent review exist.
6. **Baseline disposition (owner choice required).** The recorded baseline is not
   green: 24 torch and 11 matplotlib outcomes stem from an interpreter missing the
   project's own pinned dependencies, and 19 assertion failures are pre-existing at
   `238c207` with no common root cause established. Choose one:
   **(a)** establish the declared dependency environment (install pinned
   torch/matplotlib), re-run, and re-record the fingerprint before slice 1; or
   **(b)** accept the exact node-level fingerprint in `M2_BASELINE_FAILURE_SET.md` as
   the T7.3 comparison set. Under either choice the acceptance rule is the tuple
   contract in `M2_BASELINE_FAILURE_SET.md` (M2-RR1): the comparison unit is
   `(node_id, outcome, class, normalized_signature)` under its documented
   deterministic normalization rule; a like-for-like re-run after each slice must show
   no new tuple, exact tuple stability for every surviving node (a changed failure
   reason on the same node requires an explicit reviewed disposition — silent same-node
   replacement is a stop condition even at equal counts), explained disappearance only,
   all support-specific checks passing, and date-dependent drift in listed nodes
   recorded and dispositioned.
7. Authorize the Codex-authored slice 5 for Codex-owned/assigned edits per M1 item 7:
   the `AGENTS.md` packaging fact and support navigation, and the
   `docs/governance-transition.md` unsafe-reset wording replacement. Claude authors
   neither file's content.
8. Authorize the `followup-ml-gate.yml` `master`→`main` correction as its own isolated
   slice 6 under M1 item 8, with the exact one-line diff
   (`-      - master` / `+      - main`) reviewed at publication time. No `.gitignore`
   edit is planned; a proven need would require a new owner decision.
9. Claude implements the shared-neutral slices this cycle (session role reversal
   stands); Codex authors slice 5 and independently reviews every slice; neither agent
   marks a T7 criterion without the other's review.

## Risks and controls

| Risk | Control | Residual owner choice |
|---|---|---|
| Baseline is not green in this environment | Node-level fingerprint (item 6): no-new-failing-node rule, explained resolutions only, silent replacement is a stop condition | Item 6(a) dependency environment first, or 6(b) fingerprinted red baseline |
| Support slice touches product behavior | Manifest path allowlist; per-slice preflight diff; T7.3 product-preservation check | Accept slice sequencing |
| Partial publication leaves inconsistent state | Small isolated commits; staged no-clobber/atomic tooling; accepted T6.4 rollback rehearsal | Accept revert-only recovery |
| Cross-agent ownership violation | Slices 1-4 are shared-neutral; agent-owned payloads authored only by their owner (items 7, 9) | Retain role assignments |
| Hosted behavior changes unnoticed | Workflow edit isolated to its own reviewed commit (item 8) | Authorize, defer, or reject item 8 timing |
| Listed baseline nodes drift during the publication window | Node-level set recorded at exact date/HEAD; like-for-like re-runs; drift recorded and dispositioned, never averaged away | Accept comparison method |

## Alternatives

- **Approve recommended set:** slice publication begins immediately after this decision,
  each slice preflighted and independently reviewed.
- **Approve slices 1-3 only, defer 7-8:** neutral core lands; agent-owned guidance and
  the workflow fix wait for a later decision.
- **Defer:** nothing is written; evidence is preserved and the baseline reverified
  before a future decision.
- **Reject:** claims are released and CC_FIN remains untouched.

## Recovery impact in plain language

Slice 1 starts from the recorded clean commit `238c207`; each later slice starts from
the verified clean result of the previous accepted slice and records that parent commit
before writing anything. Every slice adds only its named support files. If anything goes
wrong, the slice is undone with a revert commit limited to exactly that slice's commits,
back to its recorded parent; product files, earlier accepted slices, history, and any
concurrent work are untouched — this exact procedure was rehearsed and independently
accepted as T6.4 evidence. CC_Loto is not touched at all until the separate M3 decision.

## Owner decision record

Pending. No approval, rejection, or deferral has been recorded. This packet authorizes
nothing until the owner's explicit decision is recorded here with a UTC timestamp.
