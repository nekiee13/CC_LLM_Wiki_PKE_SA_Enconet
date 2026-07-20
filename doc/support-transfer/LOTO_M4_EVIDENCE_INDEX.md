---
record_type: milestone_evidence_index
milestone: M4
target: CC_Loto
baseline: b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481
candidate_tip: bda0db3cf913207c254064b0681f7f309a536ec6
recorded_at_utc: 2026-07-20T07:10:00Z
prepared_by: codex
review_state: awaiting_claude
owner_decision: pending
target_write: none
---

# CC_Loto M4 evidence index

## Scope and conclusion boundary

This index assembles the evidence required for the owner-gated M4 decision at exact CC_Loto tip
`bda0db3cf913207c254064b0681f7f309a536ec6`. It establishes that the transferred support system is
healthy, the protected product baseline is unchanged, the scoped rollback rehearsal succeeded, and
the two agent guidance files share the eight approved support-workflow anchors.

It does **not** establish that CC_Loto's default product test suite is green. Optimization-core,
integration, webapp, optional, and hosted CI were not run. The accurate summary is: **support
validated; product baseline unchanged; product layers not run**. This index is evidence for review,
not M4 approval.

## Frozen identity

| Fact | Verified result |
|---|---|
| Authorized pre-transfer baseline | `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481` |
| Candidate local HEAD | `bda0db3cf913207c254064b0681f7f309a536ec6` |
| Fetched `origin/main` | same |
| Live `refs/heads/main` | same |
| Divergence | `0 0` |
| Porcelain | empty |
| Live tags | zero |
| Transfer commits | 18, with no extra commit between baseline and candidate |
| Baseline-to-candidate diff | 36 paths; 2,121 insertions; 2 deletions |
| M4 preparation writes to CC_Loto | none |

## Exact transfer chain

| # | Commit | Concern |
|---:|---|---|
| 1 | `8f030392` | Slice 1 support records |
| 2 | `496800dc` | Slice 1 evidence |
| 3 | `12ef3b78` | Slice 2 coordination core |
| 4 | `4ce96acb` | Slice 2 evidence |
| 5 | `fece718a` | Slice 3 handoff core |
| 6 | `71004697` | Slice 3 evidence |
| 7 | `c3d85a1a` | Slice 3c navigation index |
| 8 | `85f97d0a` | Slice 3c evidence |
| 9 | `6e050bfb` | Codex guidance |
| 10 | `fd7e96fd` | Codex-guidance evidence |
| 11 | `41669124` | Claude factual correction |
| 12 | `f549b406` | Claude-correction evidence |
| 13 | `14f0cf26` | Target-native aggregate, validators, and tests |
| 14 | `d5dc65e5` | Validator/test evidence |
| 15 | `2aebed6b` | Codex guidance vocabulary correction |
| 16 | `a4ccbe14` | Vocabulary-correction evidence |
| 17 | `843906eb` | Claude support-workflow guidance |
| 18 | `bda0db3c` | Guidance-alignment evidence |

## M4 criterion map

| Criterion | Evidence | Disposition |
|---|---|---|
| T8.1 navigation and authority | Root/support navigation and the accepted Slice 3c closure; links connect the enhanced plan, U7, progress, roadmap, CI, and release policy. The enhanced plan remains proposed, indexes remain deferred, and no competing backlog or authority was introduced. | Established |
| T8.2 target preflight and installed support system | Every slice used exact target preflight, rendered candidates, disposable dry runs, claims, committed-object review, and live-tip closure. Neutral support core preceded agent-owned guidance. Final aggregate and direct coordination validation pass. | Established |
| T8.3 semantics, exclusions, and recovery | Required/optional states remain distinct; sensitive/index exclusions match; protected product/science/backlog objects are unchanged; named-commit rollback preserves disjoint concurrent work and all baseline bytes. | Established with the rollback conflict limitation below |
| T8.4 independent reproduction and owner gate | Claude independently reviewed every publication slice, the aggregate, rollback evidence, and bilateral guidance synchronization. The final M4 packet still requires Claude review and an explicit owner accept/defer/reject decision. | Review pending; owner decision pending |

## Final-tip verification

The following read-only verification was repeated at the exact candidate tip during M4 packet
preparation. The generated `coordination/BOARD.md` hash remained
`A541294B50A11AE56E48DA5735C3BAF67D76264B4CA72BAD8A0F287F37E0A349` and the target remained clean.

| Check | Exit/result |
|---|---|
| Installed aggregate with explicit native Python | `0`; coordination passed; handoff `not-configured`; schema parsed `1`; focused support contract passed |
| Direct target coordination validation | `0`; 0 errors, 0 warnings |
| Missing native-Python fail-closed probe | `1`; native contract support unavailable |
| Wrong support-operator fail-closed probe | `1`; coordination unavailable |
| Native `core-unit` | `0`; 42/42 |
| Native `contract` | `0`; 30/30 |
| Native `state-integrity` | `0`; 3/3 |
| Optimization-core, integration, webapp | `not-run` |
| Optional and hosted CI | `not-run` |

The original aggregate execution and independent acceptance are recorded in
[`LOTO_AGGREGATE_VALIDATION_EVIDENCE.md`](LOTO_AGGREGATE_VALIDATION_EVIDENCE.md) and
[`CC_2026-07-20T022641Z_resolved-loto-aggregate-acceptance-manifest.md`](../../Enconet/coordination/archive/CC_2026-07-20T022641Z_resolved-loto-aggregate-acceptance-manifest.md).

## Product and data preservation

The baseline-to-candidate diff contains no change under `src/`, `opt/`, `.github/`, or `docs/`, and
no change to `DATA.csv`, `pyproject.toml`, `requirements.txt`, `requirements.lock`, or
`run_tests.py`. Object identity was verified directly:

| Protected path | Baseline and candidate object |
|---|---|
| `DATA.csv` | `6fb9ff4e` |
| `pyproject.toml` | `cb46e627` |
| `requirements.txt` | `db000f71` |
| `requirements.lock` | `38a5d577` |
| `run_tests.py` | `780887d4` |
| `.github/workflows/ci.yml` | `dd9516eb` |
| `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md` | `6c44ec25` |

The 36 changed paths are limited to support publication and its target-native contract surface:
`AGENTS.md`, `CLAUDE.md`, `HANDOFF.md`, `README.md`, `coordination/**`, `support/**`, two
support-contract test files, `tools/support/**`, and `tools/validate_support.py`.

## Rollback proof and limitation

The disposable rehearsal used real commits and literal named `git revert --no-edit` operations:

| Role | Commit |
|---|---|
| Support commit 1 | `d88f8588e8d9a7be1b8572d93aa2ffa28169dbf8` |
| Disjoint concurrent commit | `f30373bca9c335d0a2e8b2d76a5116a44f99ae1a` |
| Support commit 2 | `9e46f95d87cb49af48c79bb816849f61dd8d41f0` |
| Revert support 2 | `44123c047519faa77fd73d97bbe5ffa4556d64f1` |
| Revert support 1 | `b454e275561b1a5f215fb531da0c878fe89b75a2` |

All 165 baseline tracked hashes were restored, the concurrent file remained, and aggregate,
coordination, and proportional native validation passed after recovery. This proves recovery in the
tested disjoint-concurrent-work case. It does not prove an automatic conflict-free revert after later
edits to the same append-only records; such a conflict remains owner-directed. See
[`LOTO_ROLLBACK_REHEARSAL_EVIDENCE.md`](LOTO_ROLLBACK_REHEARSAL_EVIDENCE.md) and
[`CX_2026-07-20T024019Z_resolved-loto-rollback-rehearsal-manifest.md`](../../Enconet/coordination/archive/CX_2026-07-20T024019Z_resolved-loto-rollback-rehearsal-manifest.md).

## Guidance synchronization truth

At the candidate tip, `AGENTS.md` and `CLAUDE.md` share the eight owner-approved semantic anchors:
support read order, claim before work, immutable active/archive lifecycle, authoritative
`agent_coord.py`, validation truth, aggregate fail-closed behavior, revert-only recovery, and the M4
owner gate. The files are intentionally agent-native and are not byte-identical. Synchronization
does not establish product health or M4 acceptance. See
[`CC_2026-07-20T065813Z_resolved-loto-guidance-synchronization-manifest.md`](../../Enconet/coordination/archive/CC_2026-07-20T065813Z_resolved-loto-guidance-synchronization-manifest.md).

## Findings, lessons, and attempt accounting

- Anchor presence is not proof of anchor correctness. Guidance prose was cross-checked against the
  executable schema and tool authority.
- Adversarial negative-path review materially improved the installed validator. Slice 6 v1 could
  return exit `0` when an applicable check was `unknown` or `unavailable`, so a missing native
  executable or wrong support-operator environment could validate nothing without failing the
  aggregate. The finding was accepted before any target write; v2 fails closed, and the two final-tip
  probes now demonstrate exit `1`. This was a real fail-open defect caught by independent review,
  not by repeating the happy path.
- Semantic checks must validate meaning rather than incidental formatting. During the alignment
  cycle, a Claude-side schema `$ref` lookup assumption and a Codex-side multiline-regex assumption
  were disclosed, corrected, and independently rechecked.
- Aggregate success means support-system health only; it must never be relabeled as product health.
- Rollback proof is scoped to the demonstrated topology and does not erase the conflict limitation.
- During M4 packet preparation, the first protected-scope wrapper passed its object checks but its
  final two revision-range diff commands failed because PowerShell parsed the unbraced range
  incorrectly. The commands were rerun with an explicit `${baseline}..HEAD` range and both passed.
  No failed or unavailable check is omitted.

## Closure records by slice

- Slice 1: [`CC_2026-07-18T230607Z_loto-slice1-live-tip-verified-slice1-closed.md`](../../Enconet/coordination/archive/CC_2026-07-18T230607Z_loto-slice1-live-tip-verified-slice1-closed.md)
- Slice 2: [`CC_2026-07-19T215934Z_loto-slice2-live-tip-verified-slice2-closed.md`](../../Enconet/coordination/archive/CC_2026-07-19T215934Z_loto-slice2-live-tip-verified-slice2-closed.md)
- Slice 3: [`CC_2026-07-19T225159Z_loto-slice3-live-tip-verified-slice3-closed.md`](../../Enconet/coordination/archive/CC_2026-07-19T225159Z_loto-slice3-live-tip-verified-slice3-closed.md)
- Slice 3c: [`CC_2026-07-19T234604Z_loto-slice3c-live-tip-verified-slice3c-closed.md`](../../Enconet/coordination/archive/CC_2026-07-19T234604Z_loto-slice3c-live-tip-verified-slice3c-closed.md)
- Codex guidance: [`CC_2026-07-20T003427Z_loto-slice5-live-tip-verified-slice5-closed.md`](../../Enconet/coordination/archive/CC_2026-07-20T003427Z_loto-slice5-live-tip-verified-slice5-closed.md)
- Claude guidance correction: [`CC_2026-07-20T011219Z_resolved-loto-cc-guidance-slice-manifest.md`](../../Enconet/coordination/archive/CC_2026-07-20T011219Z_resolved-loto-cc-guidance-slice-manifest.md)
- Validators/tests: [`CC_2026-07-20T020442Z_loto-slice6-live-tip-verified-slice6-closed.md`](../../Enconet/coordination/archive/CC_2026-07-20T020442Z_loto-slice6-live-tip-verified-slice6-closed.md)

## Gate state

All implementation prerequisites offered for M4 are assembled. M4 remains closed until Claude
independently reviews this packet and the owner explicitly records a decision. Silence, packet
publication, or reviewer acceptance is not owner approval.
