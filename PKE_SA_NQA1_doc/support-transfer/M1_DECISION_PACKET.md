# M1 target-profile decision packet

## Decision requested

Approve, revise, defer, or reject support profiles v1.0 for CC_FIN and CC_Loto at the exact
baselines below. Approval opens FIN planning/implementation EPIC T3; it does not itself publish
files, modify Loto, change hosted settings, create a release, or approve product-plan work.

| Target | Exact candidate baseline | Profile | Publication order |
|---|---|---|---|
| CC_FIN | `238c207c73970f3d3c6dc00c2db5932ebeca7be4` | `CC_FIN_SUPPORT_PROFILE.md` v1.0 | First pilot |
| CC_Loto | `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481` | `CC_LOTO_SUPPORT_PROFILE.md` v1.0 | After FIN acceptance at M3 only |

Both baselines were reverified clean and unchanged during T1. No target write has occurred.

## Evidence bundle

- M0 activation: `M0_ACTIVATION.md`
- target inventories: `CC_FIN_EVIDENCE_INVENTORY.md` and
  `CC_LOTO_EVIDENCE_INVENTORY.md`
- gap/collision/sensitivity/scale evidence: `GAP_COLLISION_SENSITIVITY_MATRIX.md`
- target profiles: `CC_FIN_SUPPORT_PROFILE.md` and `CC_LOTO_SUPPORT_PROFILE.md`
- semantic adaptations: `DIFFERENCE_REGISTER.md`
- exact allowed path families and recovery: `PUBLICATION_ROLLBACK_MANIFESTS.md`

## Recommended decision set

1. Accept the owner-designated enhanced plan in each target as product authority despite its
   `Proposed` header; do not edit either product plan in support scope.
2. Accept profiles v1.0 and exact baseline SHAs above.
3. Keep CC_FIN as the sequential pilot; prohibit Loto publication until FIN acceptance at M3.
4. Enable the FIN index module with strict exclusions; defer Loto indexing.
5. Disable formal workflow state machines and repo-local target skills initially.
6. Exclude tracked product data, generated outputs, vendor assets, secrets, and private path values
   from support records/indexes without changing product Git tracking.
7. Authorize Codex to correct FIN-owned packaging guidance and replace unsafe routine reset wording
   within the manifest; Claude must correct Claude-owned Loto guidance on its side.
8. Authorize the isolated FIN workflow branch-filter correction from `master` to `main`, subject to
   exact diff review and native/hosted validation. No other hosted mutation is authorized.
9. Keep hosted branch protection `unknown` until independently verified; do not infer enforcement.
10. Keep tags, releases, product versions, product data, runtime behavior, and FIN Cockpit A-F out
    of transfer scope.

## Risks and controls

| Risk | Control | Residual owner choice |
|---|---|---|
| Support framework shadows product authority | Link-only index and explicit scope taxonomy | Accept plan disposition |
| Cross-agent file collision | Owned paths, immutable messages, active claims | Retain dual-agent model |
| Two-repo blast radius | Sequential FIN pilot and M3 gate | Accept sequence |
| Sensitive/product data enters records | Explicit exclusions and pre-publication scan | Accept classifications |
| Native validation is distorted | FIN and Loto retain different native contracts | Accept intentional differences |
| Recovery removes unrelated work | Clean recovery point, path manifest, revert-only policy | Accept recovery contract |
| CI branch correction changes hosted behavior | Isolated approval, review, and hosted evidence | Authorize or defer item 8 |
| Excess framework complexity | Core plus modules; state machine/skills deferred | Accept disabled modules |

## Alternatives

- **Approve recommended set:** FIN implementation can begin in small reviewed slices; Loto remains
  blocked until FIN proves the approach.
- **Approve but defer CI correction:** support publication proceeds, but the known FIN push-filter
  mismatch remains explicitly unresolved.
- **Revise:** no target write; requested profile/manifest changes return to T2.
- **Defer:** preserve the evidence package and reverify baseline drift before a later decision.
- **Reject:** release transfer claims and make no target changes.

## Recovery impact in plain language

Each publication slice starts from a recorded clean commit and touches only named paths. If a slice
fails, it is undone with a new revert commit limited to that slice; unrelated work and repository
history are preserved. Loto provides a second containment boundary because it stays unchanged until
the FIN pilot is accepted.

## Owner decision record

Approved on 2026-07-16T23:31:30Z with recommended items 1-10, including item 8. The durable
decision is `M1_APPROVAL.md`. It names both accepted profile versions and exact SHAs. T3 planning is
authorized; target writes remain blocked pending M2.
