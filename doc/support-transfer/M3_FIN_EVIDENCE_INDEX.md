# M3 CC_FIN evidence index and captured pilot lessons

## Gate evidence identity

- FIN comparison baseline: `238c207c73970f3d3c6dc00c2db5932ebeca7be4`
- FIN accepted-candidate tip: `88f2c51cf54599a1f58cdadb5a6dfd31dd4f59ac`
- FIN live `origin/main`, local HEAD, and `origin/main`: equal at the accepted-candidate tip
- FIN divergence/worktree: `0 0`, clean
- Loto M1-accepted candidate baseline: `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`
- Loto live `origin/main`, local HEAD, and `origin/main`: equal at that baseline
- Loto divergence/worktree: `0 0`, clean; no support-transfer write has occurred

## Required M3 evidence

| Requirement | Evidence | Result |
|---|---|---|
| FIN aggregate and truthful applicable states | [`SLICE4_PUBLICATION_EVIDENCE.md`](SLICE4_PUBLICATION_EVIDENCE.md), target `support/SLICE4-PUBLICATION-EVIDENCE.md` | Published aggregate exit 0; coordination/schema/native focused pytest passed; bootstrap handoff and optional CPI/Ruff truthfully `not-configured`; hosted CI truthfully `not-run`; injected applicable failure exit 1 |
| Independent Claude review | [`CX_2026-07-18T211153Z_resolved-slice4-publication-thread-manifest.md`](../../Enconet/coordination/archive/CX_2026-07-18T211153Z_resolved-slice4-publication-thread-manifest.md), [`CC_2026-07-18T202106Z_t7-fin-verification-accepted.md`](../../Enconet/coordination/archive/CC_2026-07-18T202106Z_t7-fin-verification-accepted.md) | T7.1/T7.3 and Slice 4 independently reproduced and accepted; all findings closed |
| Rollback test/evidence | [`T6_STAGED_EXECUTABLE_CHECKPOINT.md`](T6_STAGED_EXECUTABLE_CHECKPOINT.md), [`PUBLICATION_ROLLBACK_MANIFESTS.md`](PUBLICATION_ROLLBACK_MANIFESTS.md) | Disposable Git rehearsal injected a failed third step, reverted only two slice commits, preserved unrelated/concurrent files byte-for-byte, retained history, and revalidated the recovered state |
| FIN governance/product preservation | [`T7_FIN_ACCEPTANCE_EVIDENCE.md`](T7_FIN_ACCEPTANCE_EVIDENCE.md) and Claude acceptance above | 25/25 current support-index links resolve; no product runtime/test/data path changed; chart/Cockpit/product-plan objects preserved; no Wiki runtime dependency |
| Baseline truthfulness | Target `support/BASELINE-FINGERPRINT.md`, [`BASELINE_FINGERPRINT_RENDER_EVIDENCE.md`](BASELINE_FINGERPRINT_RENDER_EVIDENCE.md) | Full native run remains expected red with stable 54/54 tuples: 24 torch, 11 matplotlib, 19 assertion; 0 new/gone/mutated |
| Publication history and recovery points | FIN Git ancestry `238c207..88f2c51`, target `support/log.md`, per-slice archived reviews | Small concern-separated commits, reviewed evidence commits, recorded parents, clean fast-forward publication; no reset/force push |

## Captured pilot lessons for Loto

The target FIN lesson/practice/AFI ledgers remain structurally installed but have no curated rows.
That absence is stated plainly. The demonstrated cross-target lessons required for M3 are captured
here so Loto planning can use them without inventing FIN-side history:

1. **Review the whole publication record, not only pinned executable bytes.** Slice 4 executable
   content was byte-correct, but post-publication review found missing log/index/classification and
   stale status. Loto pre-push review must include every governed record changed by a slice.
2. **Write replaceable status from its containing commit's perspective.** A status file that names
   its parent as current becomes false when committed. Render the local-unpushed state first, then
   record live-remote verification through the append-only log or a successor status.
3. **Make evidence discoverable through all governed paths.** An immutable evidence file alone is
   insufficient; the support index, record-class map, append-only event log, and current status must
   agree before closure.
4. **Correct immutable communication by successor, never rewrite.** A transcribed hash error was
   preserved and corrected by a linked immutable message; the reviewer reproduced the corrected
   hash before acceptance.
5. **Use short disposable roots on Windows.** Deep vendor paths can exceed legacy path limits and
   create a fixture-copy failure unrelated to the reviewed code. Loto dry runs should use a short
   `%TEMP%` root and report environmental failures literally.
6. **Truthful non-pass states are useful evidence.** `not-configured`, `not-run`, and `unavailable`
   must remain visible and must not be relabeled `passed`; only an applicable `failed` state drives
   the support aggregate nonzero.
7. **Keep target assumptions local.** FIN uses focused pytest; Loto must compose its existing
   `python run_tests.py` layers and must not acquire pytest or FIN path conventions by transfer.

## Known residual conditions

- FIN's full native suite is not green in this interpreter. The stable target-local fingerprint is
  evidence of non-regression, not a claim that dependency or product failures are resolved.
- FIN's initial handoff pointer remains the truthful `not-configured` bootstrap state; this does not
  fail the aggregate but the first operational handoff remains future work.
- Optional CPI and targeted Ruff have no configured FIN command; hosted CI is not executed locally.
- M3 acceptance authorizes no product-code/data/chart/Cockpit change, hosted-setting mutation,
  release, tag, force push, or cross-agent infrastructure edit in either target.
