# M3 decision packet — accept CC_FIN pilot / authorize CC_Loto publication

## Decision requested

Approve, partially approve, defer, or reject M3. Approval accepts the completed CC_FIN support
pilot at its exact published tip and authorizes CC_Loto support publication under the M1-accepted
Loto profile and rollback manifest, beginning from the exact untouched Loto baseline. It does not
accept Loto (M4), authorize any product behavior/data/model change, or waive Loto-specific exact
rendering, dry-run, preflight, claims, independent pre-push review, and revert-only recovery.

| Target | Exact candidate baseline | Evidence version | What approval authorizes |
|---|---|---|---|
| CC_FIN | `88f2c51cf54599a1f58cdadb5a6dfd31dd4f59ac` | M3 evidence index v1; T7 + Slice 4 final closure | Accept the FIN support pilot as complete evidence for the sequential transfer |
| CC_Loto | `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481` | M1-accepted Loto profile v1.0; shared rollback manifest | Start Loto support publication in small reviewed slices after a Loto-specific exact dry run and pre-job briefing |

Read-only verification on 2026-07-18 found both repositories on `main`, clean, synchronized with
their live `origin/main`, and at the exact SHAs above. CC_Loto remains untouched by the transfer.

## Evidence bundle

- M3 evidence map and captured pilot lessons: [`M3_FIN_EVIDENCE_INDEX.md`](M3_FIN_EVIDENCE_INDEX.md)
- FIN T7 governance/product-preservation evidence and independent acceptance:
  [`T7_FIN_ACCEPTANCE_EVIDENCE.md`](T7_FIN_ACCEPTANCE_EVIDENCE.md),
  [`CC_2026-07-18T202106Z_t7-fin-verification-accepted.md`](../../Enconet/coordination/archive/CC_2026-07-18T202106Z_t7-fin-verification-accepted.md)
- FIN aggregate A/B/C publication and final correction closure:
  [`SLICE4_PUBLICATION_EVIDENCE.md`](SLICE4_PUBLICATION_EVIDENCE.md),
  [`CX_2026-07-18T211153Z_resolved-slice4-publication-thread-manifest.md`](../../Enconet/coordination/archive/CX_2026-07-18T211153Z_resolved-slice4-publication-thread-manifest.md)
- Disposable scoped-rollback proof and recovery contract:
  [`T6_STAGED_EXECUTABLE_CHECKPOINT.md`](T6_STAGED_EXECUTABLE_CHECKPOINT.md),
  [`PUBLICATION_ROLLBACK_MANIFESTS.md`](PUBLICATION_ROLLBACK_MANIFESTS.md)
- Accepted Loto target contract and cross-target differences:
  [`CC_LOTO_SUPPORT_PROFILE.md`](CC_LOTO_SUPPORT_PROFILE.md),
  [`DIFFERENCE_REGISTER.md`](DIFFERENCE_REGISTER.md), [`M1_APPROVAL.md`](M1_APPROVAL.md)

## Recommended decision set

1. Accept CC_FIN at `88f2c51cf54599a1f58cdadb5a6dfd31dd4f59ac` as the completed sequential pilot:
   support publication, target-local baseline migration, aggregate, governed evidence, and all
   independent-review findings are closed.
2. Accept the FIN native state truthfully, not as green: the 54-tuple target-local fingerprint is
   unchanged with 0 new/gone/mutated outcomes; resolving missing optional dependencies and existing
   assertions remains product/environment work outside this transfer.
3. Accept the disposable T6.4 rehearsal as M3 rollback evidence: it proves scoped revert-only
   recovery while preserving unrelated and concurrent work; every real Loto slice must still record
   its own parent and recovery scope.
4. Accept the seven pilot lessons in `M3_FIN_EVIDENCE_INDEX.md` as the captured cross-target lesson
   set for Loto preparation, while recording that FIN's target-local curated ledgers remain empty.
5. Authorize Loto publication from exact baseline
   `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481` under its M1 profile and the shared rollback manifest,
   conditional on a Loto-specific exact render/dry run and pre-job briefing before the first write.
6. Require Loto-native composition: `python run_tests.py` and its existing optional-layer semantics;
   no pytest dependency, FIN script paths, Wiki runtime dependency, index refresh, hosted mutation,
   product/data/model change, tag, or release is authorized.
7. Keep Codex as implementer and Claude as independent reviewer for this session. Agent-owned files
   remain authored only by their owning agent; every shared-neutral slice requires independent
   pre-push review, exact committed-byte checks, and clean live-remote closure evidence.
8. Keep M4 closed: this decision starts Loto publication but does not accept Loto. M4 requires the
   Loto aggregate, independent review, rollback evidence, and an owner decision.

## Risks and controls

| Risk | Control | Residual owner choice |
|---|---|---|
| FIN full native suite remains expected red | Immutable 54-tuple fingerprint; 0 new/gone/mutated; states never relabeled green | Accept FIN as non-regressed, or defer for product/environment remediation |
| FIN process lessons are not rows in target-local curated ledgers | Durable M3 evidence index captures demonstrated lessons and links immutable review history | Accept packet-level capture, or require a separately reviewed FIN ledger update before M3 |
| Loto differs materially from FIN | Loto profile, difference register, `run_tests.py`-native layering, no pytest assumption | Authorize only conditional Loto preparation/publication |
| Stale status or undiscoverable evidence recurs | Pre-push review covers log/index/class/status as one governed closure set | Accept mandatory governed-record closure check |
| Partial Loto publication leaves inconsistent state | Small concern-separated commits, exact parent per slice, revert-only recovery, clean validation | Accept scoped recovery or require an additional Loto rehearsal before first push |
| Transfer expands into product/data/hosted/release work | Explicit path/authority exclusions and stop conditions | Keep exclusions, or authorize a named exception separately |

## Alternatives

- **Approve recommended set:** FIN is accepted and Loto may begin exact-render/dry-run preparation
  and then small reviewed publication slices from `b469afc6`, with M4 still closed.
- **Partially approve:** accept FIN but continue to block Loto writes; preparation may remain
  read-only until a later owner decision.
- **Defer:** neither FIN acceptance nor Loto authorization is recorded; preserve evidence and
  reverify both exact tips before returning to M3.
- **Reject:** do not accept FIN and do not authorize Loto; release the M3 claim and record the
  specific evidence or design deficiency that must be addressed.

## Recovery impact in plain language

M3 acceptance does not merge the repositories or copy FIN behavior into Loto. Each Loto slice
starts from a named clean parent, changes only its reviewed support paths, and is independently
checked before push. If a slice fails, a new revert commit removes only that slice while preserving
earlier accepted slices, product work, concurrent changes, and Git history. The disposable rehearsal
proved this pattern under an injected mid-publication failure. Destructive reset and force push are
not routine recovery options.

## Owner decision record

Pending human owner decision. Silence, elapsed time, agent review, or this recommendation authorizes
nothing. Record the selected numbered items, any conditions, the exact FIN/Loto SHAs, and decision
time only after the owner responds.
