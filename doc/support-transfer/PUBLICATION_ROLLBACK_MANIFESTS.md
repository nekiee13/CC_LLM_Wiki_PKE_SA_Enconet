# Publication and rollback manifests v1.0

These manifests are planning controls. They authorize no target write before M1 and no Loto write
before FIN acceptance at M3. At each implementation claim, the exact slice must be a subset of this
manifest.

## Common planned additions

| Path family | Classification | Purpose |
|---|---|---|
| `support/README.md`, `current-status.md`, `log.md` | Shared-neutral | Authority, live status, append-only events |
| `support/decisions/` | Shared-neutral | ADR template, register, immutable decisions |
| `support/AFI.md`, `LESSONS-LEARNED.md`, `GOOD-PRACTICES.md` | Shared-neutral | Improvement lifecycle |
| `support/handoffs/`, `support/schemas/`, `support/templates/` | Shared-neutral | Clone-complete handoff contract |
| `coordination/TEAM_PROTOCOL.md`, `BOARD.md`, schemas/templates | Shared-neutral | Communication and generated status contract |
| `coordination/messages/`, `archive/`, `claims/` | Ownership by record prefix | Immutable communication and claims |
| `HANDOFF.md` | Shared-neutral pointer | Current validated handoff navigation |
| FIN `scripts/agent_coord.py`, `scripts/make_handoff.py`, `scripts/validate_support.py`; Loto equivalents under `tools/` | Shared-neutral implementation | Small isolated utilities following each target's existing helper convention |

## CC_FIN manifest

Planned additions are the common paths plus focused support tests under existing `tests/` and,
after committed-state approval, Codex-owned index configuration with explicit source/test/docs
inclusions and data/vendor/generated exclusions.

| Existing path that may be modified | Owner/class | Allowed scope | Separate approval? |
|---|---|---|---|
| `AGENTS.md` | Codex-owned | Correct packaging fact; add support navigation/commands | Covered by approved profile |
| `docs/README.md` or existing docs index | Existing target authority | Link support index only | No, if link-only |
| `docs/governance-transition.md` | Existing target authority | Replace unsafe routine reset wording with evidence-first recovery | Explicit M1 disposition |
| `.github/workflows/followup-ml-gate.yml` | Hosted governance | Change push filter `master` to `main` only | Explicit M1 disposition and isolated diff |
| `.gitignore` | Existing target authority | Add only proven support runtime artifacts | Only if preflight proves necessary |

No product-plan, product-data, Cockpit, forecasting, package-version, feature-ADR, or runtime source
modification is permitted by this manifest.

## CC_Loto manifest

Planned additions are the common paths, support utilities under existing `tools/`, Codex-owned
`AGENTS.md`/`.agents/`, and focused support tests inside an existing `run_tests.py`-discovered
layer. No `scripts/` directory or index configuration is initially added.

| Existing path that may be modified | Owner/class | Allowed scope | Separate approval? |
|---|---|---|---|
| `CLAUDE.md` / `.claude/` | Claude-owned | Packaging/layer/support navigation correction by Claude only | Claude review/message lifecycle |
| `docs/README.md` or U7-selected index | Existing target authority | Link support index and integrate U7 navigation | Confirm at Loto implementation gate |
| `run_tests.py` | Existing target authority | None planned; modify only if no existing layer can discover support tests | New owner decision required |
| `.gitignore` | Existing target authority | Add only proven support runtime artifacts | Only if preflight proves necessary |

No enhanced plan, prior progress, `DATA.csv`, architecture, roadmap, package version, runtime source,
workflow, or model/test-fixture modification is permitted by this manifest.

## Preflight and dry run

For each target and slice:

1. record absolute root, remote, branch, HEAD, upstream HEAD, and porcelain status;
2. require the accepted baseline or stop for drift disposition;
3. verify every planned path against ownership and existing-file classification;
4. search the proposed content for credentials, private path values, product data, and forbidden
   cross-agent paths;
5. render the proposed file/diff list without writing the target;
6. run support schema/reference tests against a disposable copy or temporary fixture;
7. require a non-overlapping target claim and reviewer availability.

## Recovery point and commit shape

The recovery point is the recorded clean baseline SHA. Publication uses small commits grouped by
one concern: neutral skeleton, records/ADR, coordination, handoff, validators/tests, agent-owned
guidance, and optional integration. No commit mixes support transfer with product work. Push occurs
only after local validation and review required by the active gate.

## Abort triggers

Stop without further writes on baseline drift, dirty or unowned paths, secret/data exposure,
unexpected generated artifacts, inability to prove test discovery, failed required checks,
product-output changes, cross-agent ownership violation, unreviewed workflow mutation, or rollback
scope larger than the named support commits.

## Scoped rollback

- Before commit: remove or restore only paths created/changed by the active slice after checking
  the rendered path list; preserve all pre-existing and concurrent work.
- After local commit: obtain owner approval and use `git revert <named-commit>`; do not rewrite
  history or reset the tree.
- After push: revert through new commits, validate, independently review, then push normally.
- Never use recursive cleanup, broad checkout, `reset --hard`, or force push as routine recovery.

Post-rollback verification rechecks exact status, support navigation/references, native focused
tests, and target behavior relevant to the reverted slice. The rollback record names commands,
exit codes, remaining changes, and the exact next action.
