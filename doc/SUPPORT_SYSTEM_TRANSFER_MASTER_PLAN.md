# SUPPORT SYSTEM TRANSFER MASTER PLAN v1.0 — CC_FIN and CC_Loto

## 0. Document control

| Field | Value |
|---|---|
| Plan ID | `SUPPORT-SYSTEM-TRANSFER` |
| Version | 1.0 — controlled candidate |
| Date | 2026-07-17 |
| Status | M1 approved on 2026-07-16T23:31:30Z for corrected profiles v1.0; T3 planning is authorized, target publication remains blocked pending M2 |
| Owner | Human project owner |
| Implementers | Codex and Claude Code within their ownership boundaries |
| Source contract | `doc/Support_system.md`, accepted by the owner on 2026-07-17 |
| Review evidence | `Enconet/coordination/archive/CC_2026-07-16T221019Z_support-system-review-findings.md`; resolution manifest `CC_2026-07-16T222855Z_resolved-support-system-review-findings-manifest.md` |
| Supersedes | `doc/Support_system_transfer_draft.md` after this plan is independently accepted and owner-activated |
| Target 1 | CC_FIN — `C:\xPY\xPrj\CC_FIN`; `https://github.com/nekiee13/CC_FIN` |
| Target 2 | CC_Loto — `C:\xPY\xPrj\CC_Loto`; `https://github.com/nekiee13/CC_Loto` |
| Format | GitHub-Issues style: epics, claimable tasks, dependencies, and acceptance criteria |

M0 is recorded in `doc/support-transfer/M0_ACTIVATION.md`. M1 is recorded in
`doc/support-transfer/M1_APPROVAL.md`; it accepts the corrected target profiles and authorizes T3
planning. No checklist state, agent statement, or passage of time substitutes for M2-M5.

## 1. Mission and end state

Transfer the agreed software-development support system into CC_FIN and CC_Loto as two
repository-local implementations with common semantics and project-specific adapters. The
transfer harmonizes development practice without copying Wiki domain policy, weakening either
project's native validation, or replacing either project's product-upgrade Master Plan.

The end state is:

- each target has a clone-complete governance, recordkeeping, coordination, handoff, validation,
  and improvement-knowledge core;
- both agents have separate owned infrastructure and one shared neutral coordination protocol;
- project-native plans, tests, CI, product behavior, and historical evidence remain authoritative;
- common semantics are demonstrably consistent while local commands and paths remain local;
- support assets have no runtime dependency on this Wiki repository or on machine-global skills;
- every mutation has preflight, scoped rollback, and post-change verification evidence; and
- each target has an accepted handoff returning work to its product-upgrade backlog.

## 2. Authority boundaries and non-goals

### 2.1 Authorities preserved

| Concern | CC_FIN authority | CC_Loto authority |
|---|---|---|
| Product upgrades | `docs/project/CC_FIN_project_upgrade_plan_enhanced.md` | `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md` |
| Existing agent side | `AGENTS.md` (Codex-owned) | `CLAUDE.md` (Claude-owned) |
| Native validation | pytest, guardrail suites, optional CPI, targeted ruff, existing CI | layered `run_tests.py`, optional dependency layer, existing CI |
| Existing status/governance | GitHub workflows/templates, documentation freshness ledger, feature ADRs | `PROGRESS.md`, `ROADMAP.md`, CI, documentation-governance EPIC U7 |
| Product behavior | Existing application and chart/report behavior | Existing lottery/scientific behavior and package contracts |

The support plan governs only the support-system transfer. Where it conflicts with a current
target authority, work stops and the collision is resolved through the target's decision process.

### 2.2 Explicit non-goals

- Do not merge the support backlog into either product-upgrade Master Plan.
- Do not replace native tests with Wiki commands or assume pytest in CC_Loto.
- Do not install the Wiki G1–G7 audit lifecycle or supplier-document ingestion workflow.
- Do not copy Wiki raw-document rules into a target unless its approved data profile requires
  equivalent controls.
- Do not create a shared runtime library or cross-repository path dependency.
- Do not refactor product code, alter outputs, or close product-plan tasks as a side effect.
- Do not create GitHub issues, change branch protection, or mutate hosted settings until their
  target task is separately authorized.

### 2.3 CC_FIN chart preservation constraint

The verified CC_FIN baseline contains two existing charts plus the implemented third **Forecast
Decision Cockpit**, composed of panels A–F and available through the opt-in
`scripts/render_cockpit.py` command. Automatic cockpit emission from the main analysis pipeline
remains pending product-plan Task 23.12. Support transfer must preserve both facts: it must not
remove or change the cockpit, and it must not falsely mark pipeline integration complete.

## 3. Verified planning baselines

Read-only verification on 2026-07-17 established:

| Target | Branch / HEAD | Worktree | Key facts |
|---|---|---|---|
| CC_FIN | `main` / `238c207c73970f3d3c6dc00c2db5932ebeca7be4`; synchronized with `origin/main` | Clean | Enhanced upgrade plan; Codex guidance; pytest/CPI/ruff; hosted governance; feature ADRs; A–F cockpit implemented through an opt-in CLI |
| CC_Loto | `main` / `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`; synchronized with `origin/main` | Clean | Enhanced upgrade plan; Claude guidance; layered unittest runner; optional dependency semantics; CI; progress/roadmap; U7 documentation governance |

These SHAs are planning evidence, not permanent implementation pins. Task T1 re-verifies the
actual target state before any write and records all drift since these baselines.

## 4. Governing principles

1. **Prefer the simplest architecture that satisfies the verified requirements.**
2. **Build small cohesive modules.** Small means one reason to change, not an arbitrary line count.
3. **Prevent God modules, components, and services.** Multiple independent responsibilities
   trigger review and decomposition.
4. **Reuse proven semantics, not copied assumptions.** Common assets name real consumers and
   project-specific policy stays in target configuration.
5. **Design for evolutionary scale.** Record volume, users, concurrency, retention, and growth
   assumptions now; add infrastructure only for measured or approved needs.
6. **Contracts before adapters.** Shared record semantics and validators precede agent-specific
   guidance or command wrappers.
7. **Preserve before extending.** Existing authorities and history are mapped before new paths
   are created.
8. **Fail closed and report truthfully.** `passed`, `failed`, `not-run`, `unknown`, `skipped`, and
   `not-configured` remain distinct.
9. **Clone-complete core.** Machine-global skills may assist agents but are never required for
   repository correctness.
10. **Reversible publication.** Each target mutation has a recovery point, owned-path manifest,
    abort rule, rollback procedure, and verification.

## 5. Framework selection

The final selection is approved per target in EPIC T2. The planning default is:

| Capability | CC_FIN | CC_Loto | Planning disposition |
|---|---|---|---|
| Mandatory support core | Enabled | Enabled | Required |
| Dual-agent coordination | Enabled | Enabled | Required because both agents will work in each repository |
| Claims and generated board | Enabled | Enabled | Required for concurrent writers |
| Lightweight milestone gates | Enabled | Enabled | Four owner decisions; no Wiki state-machine transplant |
| Formal workflow state machine | Not selected | Not selected | Add only if target evidence justifies ordered, unskippable phases |
| Shared code/docs indexes | Assess | Assess | Conditional on repository scale, exclusions, and ownership |
| Workflow skills | Assess per workflow | Assess per workflow | Use only for complex reusable judgment workflows |
| Golden benchmarks | Preserve existing / assess support additions | Preserve existing / assess support additions | Product benchmarks remain product-owned |
| Controlled-input provenance | Assess external market-data and credential risk | Assess `DATA.csv` and scientific-data sensitivity | Defined by each target data profile |
| Hosted-platform governance | Integrate existing controls | Integrate existing CI | Never silently change hosted settings |
| Release/version/tag policy | Map existing behavior | Map existing behavior | Conditional on target release practice |

## 6. Execution model and issue conventions

### 6.1 Status vocabulary

- `[x]` means completed with durable evidence.
- `[ ]` means planned and not yet complete.
- A task is claimable only when all dependencies and its authorization gate are satisfied.
- Acceptance requires evidence in the target repository; a plan checkbox alone is not evidence.

### 6.2 Ownership vocabulary

- **Shared-neutral:** either agent may edit under an active non-overlapping claim.
- **Codex-owned:** `AGENTS.md`, `.agents/`, Codex guidance/indexes, and `CX_` records.
- **Claude-owned:** `CLAUDE.md`, `.claude/`, Claude guidance/indexes, and `CC_` records.
- **Owner-only:** milestone acceptance, material policy choice, risk acceptance, and plan activation.

### 6.3 Deployment order

CC_FIN is the first implementation pilot because it already has Codex guidance and the broader
hosted-governance surface. CC_Loto begins publication only after the FIN release review records
lessons and confirms that the shared semantics are viable. Planning and read-only profiling may
proceed for both targets before then. The owner may authorize parallel publication through an
explicit plan amendment if isolation and reviewer capacity are demonstrated.

### 6.4 Milestones

| Gate | Decision | Blocking evidence |
|---|---|---|
| M0 | Activate this Master Plan | Independent final-plan review; finding dispositions; owner accept/revise |
| M1 | Accept target profiles | Fresh inventories, collision matrices, data/secrets policy, enabled modules, rollback design |
| M2 | Authorize FIN publication | FIN support profile, dry run, recovery point, target-native baseline checks |
| M3 | Accept FIN / authorize Loto | FIN aggregate evidence, independent review, rollback test/evidence, lessons captured |
| M4 | Accept Loto | Loto aggregate evidence, independent review, rollback test/evidence |
| M5 | Close transfer | Cross-project conformance report, difference register, final handoffs |

## 7. Epic dependency map

| Epic | Goal | Depends on |
|---|---|---|
| T0 | Approve and activate the transfer plan | — |
| T1 | Re-verify targets and build evidence inventories | T0 |
| T2 | Approve project support profiles and differences | T1 |
| T3 | Define repo-local governance and recordkeeping core | T2 |
| T4 | Bootstrap paired-agent coordination | T2, T3 |
| T5 | Implement handoff and continuity contracts | T3, T4 |
| T6 | Compose validation, recovery, and owner gates | T2–T5 |
| T7 | Publish and accept CC_FIN pilot | T3–T6, M2 |
| T8 | Publish and accept CC_Loto | T7, M3 |
| T9 | Prove conformance and close the transfer | T7, T8 |

## EPIC T0 — Approve and activate the transfer plan

**Labels:** `support-system`, `planning`, `gate`  
**Owner:** human owner; Codex prepares; Claude independently reviews

### Task T0.1 — Publish the support-system specification

**Status:** completed.

- [x] Inventory covers governance, records, coordination, handoff, validation, tooling,
  recovery, hosted controls, release policy, indexing, and skills.
- [x] Every inventory item uses the normative portability taxonomy.
- [x] Qualified simplicity, modularity, reuse, God-component prevention, and scalability
  principles are explicit.

### Task T0.2 — Resolve independent specification review

**Status:** completed.

- [x] Claude independently reviewed the specification and both target baselines.
- [x] Findings M1–M4 and L1–L3 were corrected in commit `6dd1c41`.
- [x] Codex and Claude confirmations are retained through immutable coordination records.

### Task T0.3 — Record owner specification acceptance

**Status:** completed on 2026-07-17.

- [x] Owner accepted the corrected support-system specification.
- [x] Claude's resolution manifest records the owner disposition without claiming it by silence.

### Task T0.4 — Independently review this final Master Plan

**Status:** completed.

- [x] Claude verifies authority preservation, task completeness, dependencies, ownership,
  target-native validation, failure recovery, and the FIN-first sequencing assumption.
- [x] Every finding has an explicit Codex and owner disposition.
- [x] Review confirms no target repository was mutated during planning.

### Task T0.5 — Owner activation gate M0

**Status:** completed at 2026-07-16T23:00:25Z; durable record `doc/support-transfer/M0_ACTIVATION.md`.

- [x] Owner records accept, revise, or reject for this Master Plan.
- [x] Activation states whether FIN publication remains the pilot and whether any target tasks
  may run in parallel.
- [x] The decision records the owner statement, plan version and exact Git SHA, UTC timestamp,
  and sequencing choice in the plan status, append-only event log, and immutable coordination evidence.
- [x] No implementation claim starts before those activation records are committed and pushed.

## EPIC T1 — Re-verify targets and build evidence inventories

**Depends on:** T0.5  
**Labels:** `support-system`, `discovery`, `read-only`

### Task T1.1 — Inventory CC_FIN support evidence

- [x] Verify repository identity, HEAD/upstream, worktree, guidance, enhanced product plan,
  architecture/AS-IS records, tests, CI, templates, feature ADRs, status records, release
  behavior, secrets/data handling, and indexes.
- [x] Compare current HEAD with planning baseline `238c207`; classify every material drift as
  accepted/no-impact, profile-update-required, or replan/block, with owner disposition where needed.
- [x] Record each support-like artifact as retain, integrate, migrate, supersede, or product-local.
- [x] Record the A–F cockpit as implemented opt-in behavior and Task 23.12 pipeline wiring as
  pending product work.
- [x] Report plans as plans and implemented capability as implemented evidence.

### Task T1.2 — Inventory CC_Loto support evidence

- [x] Verify repository identity, HEAD/upstream, worktree, Claude guidance, enhanced product
  plan, `PROGRESS.md`, `ROADMAP.md`, U7, CI, package boundaries, data files, and release behavior.
- [x] Compare current HEAD with planning baseline `b469afc`; classify every material drift as
  accepted/no-impact, profile-update-required, or replan/block, with owner disposition where needed.
- [x] Preserve the layered `run_tests.py` contract and optional-dependency semantics.
- [x] Record each support-like artifact with the same disposition vocabulary as CC_FIN.
- [x] Identify all sensitive or non-indexable data classes, including the disposition of `DATA.csv`.

### Task T1.3 — Publish gap, collision, and sensitivity matrices

- [x] Distinguish missing capability from differently implemented capability.
- [x] Identify path, naming, authority, ownership, test, CI, secret, data, and release collisions.
- [x] Record scale assumptions: users, data volume, run frequency, concurrency, retention,
  expected growth, and acceptable support-tool runtime.
- [x] Produce no target writes beyond explicitly authorized neutral planning records.

## EPIC T2 — Approve project support profiles

**Depends on:** T1  
**Labels:** `support-system`, `profile`, `gate`

### Task T2.1 — Prepare the CC_FIN support profile

- [x] Name authorities, record paths, roles, agent boundaries, Git/hosted workflow, native checks,
  status, handoff, modules, scale assumptions, secret storage, sensitive-data exclusions,
  recovery, release policy, indexes, and skills.
- [x] Integrate existing GitHub governance and feature ADRs without shadow authorities.
- [x] Define truthful applicability for pytest, CPI, ruff, and CI checks.
- [x] Profile is evidence-complete and ready for the consolidated M1 decision.

### Task T2.2 — Prepare the CC_Loto support profile

- [x] Specify the same profile fields using Loto terminology and native commands.
- [x] Introduce no pytest assumption and preserve optional-layer reporting.
- [x] Integrate U7 instead of duplicating documentation governance.
- [x] Profile is evidence-complete and ready for the consolidated M1 decision.

### Task T2.3 — Approve the difference register

- [x] Every intentional difference names rationale, owner, verification, and reconsideration trigger.
- [x] Common record/status semantics are not weakened by target wording.
- [x] Wiki-specific adapters and deliberately omitted modules are explicit.

### Task T2.4 — Prepare publication and rollback manifests

- [x] List every path the transfer may create or modify in each target.
- [x] Classify paths as shared-neutral, Codex-owned, Claude-owned, or existing target authority.
- [x] Define preflight, dry run, recovery point, abort triggers, scoped rollback, and post-rollback checks.
- [x] Prohibit history rewriting, broad resets, and removal of unrelated user work.

### Task T2.5 — Prepare and decide target-profile gate M1

- [x] Compile the fresh inventories, collision/sensitivity matrices, both support profiles,
  difference register, enabled modules, and publication/rollback manifests into the M1 packet.
- [x] Packet states evidence, risks, alternatives, recovery, and plain-language impact.
- [x] Owner records approve, reject, or defer before any T3 implementation claim begins.
- [x] The decision identifies the accepted profile versions and exact target baseline SHAs.

## EPIC T3 — Define governance and recordkeeping core

**Depends on:** T2  
**Labels:** `support-system`, `governance`, `records`

### Task T3.1 — Define authority and navigation skeletons

- [ ] Each target has one support index linking—not copying—its product plan and existing authorities.
- [ ] Replaceable, append-only, immutable, generated, controlled, and historical records are distinct.
- [ ] Current status, event log, and exact-next-action semantics are specified.

### Task T3.2 — Define ADR lifecycle and registers

- [ ] One discoverable ADR register exists per target.
- [ ] Accepted ADRs are immutable and changed by supersession.
- [ ] CC_FIN feature ADRs receive an explicit integration/reference strategy.
- [ ] Decision acceptance and implementation completion remain distinct.

### Task T3.3 — Define AFI, lesson, and good-practice ledgers

- [ ] AFIs remain non-blocking unless another authority makes them blocking.
- [ ] Resolution preserves evidence and may create a reusable lesson.
- [ ] Good practices require demonstrated target evidence and can be deprecated/superseded.

### Task T3.4 — Build the target-local template contract

- [ ] Templates express common semantics without Wiki project names, supplier policy, or paths.
- [ ] Configuration points are explicit; policy is not hidden in copied scripts.
- [ ] Each target receives repository-local assets; no runtime reference to this workspace exists.
- [ ] Shared extraction is justified only by the two demonstrated target consumers.

## EPIC T4 — Bootstrap paired-agent coordination

**Depends on:** T2, T3  
**Labels:** `support-system`, `coordination`, `dual-agent`

### Task T4.1 — Bootstrap neutral coordination records

- [ ] Protocol, messages/archive/claims structure, board contract, and validator exist before
  either agent claims complete synchronization.
- [ ] Active, resolved, confirmed, and archived states match the agreed contract.
- [ ] Blockers require resolved, owner-accepted, or deferred-until disposition.

### Task T4.2 — Publish each agent's owned guidance

- [ ] Claude creates CC_FIN's Claude-owned side; Codex does not edit it.
- [ ] Codex creates CC_Loto's Codex-owned side; Claude does not edit it.
- [ ] Existing CC_FIN Codex and CC_Loto Claude guidance are preserved unless their owner changes them.
- [ ] Drift checks permit documented tool-specific differences without weakening shared semantics.

### Task T4.3 — Validate claims, review, and archive behavior

- [ ] Overlapping active claims fail.
- [ ] Message schemas, reply chains, blockers, resolution manifests, and board freshness are tested.
- [ ] Each agent archives only its own resolved and confirmed messages.
- [ ] One agent cannot declare the other agent's infrastructure synchronized.

## EPIC T5 — Implement handoff and session continuity

**Depends on:** T3, T4  
**Labels:** `support-system`, `handoff`, `continuity`

### Task T5.1 — Define target handoff profiles

- [ ] Required facts include objective, work, decisions, checks, Git/index state, blockers,
  artifacts, exact next action, and follow-up queue.
- [ ] Passed checks require commands and integer exit codes.
- [ ] Failed, not-run, unknown, skipped, and not-configured remain distinct.
- [ ] Records exclude secrets, credentials, personal data, and prohibited project data.

### Task T5.2 — Publish deterministic repo-local handoff tooling

- [ ] Immutable record validates before mutable pointer publication.
- [ ] Publication is atomic or fails without advancing the pointer.
- [ ] Complete, partial, and blocked statuses are supported.
- [ ] Staleness, absent Git, malformed evidence, and interrupted publication are tested.

### Task T5.3 — Integrate start and close continuity

- [ ] Session start compares guidance, handoff, status, messages, claims, Git, and unfinished work.
- [ ] Divergence is reported rather than silently resolved.
- [ ] Session close validates before publication.
- [ ] Interrupted risky work requires an explicit resume-or-rollback decision.

## EPIC T6 — Compose validation, recovery, and milestone gates

**Depends on:** T2–T5  
**Labels:** `support-system`, `validation`, `recovery`, `gate`

### Task T6.1 — Build target-native support aggregates

- [ ] CC_FIN composes support checks with its pytest/CPI/ruff/CI contracts.
- [ ] CC_Loto composes support checks with `run_tests.py` and preserves optional-layer semantics.
- [ ] Output is deterministic and returns non-zero for every applicable failure.
- [ ] A no-record verification mode exists wherever validation otherwise mutates history.

### Task T6.2 — Implement architecture guardrails

- [ ] God-component signals trigger review, not blind splitting.
- [ ] New abstractions name demonstrated consumers and the duplication or layer removed.
- [ ] Scale-related changes cite an approved assumption or measured bottleneck.
- [ ] Coupling and complexity checks remain advisory unless the profile makes them blocking.

### Task T6.3 — Prepare milestone packets M2–M5

- [ ] Packets state evidence, commands/results, risks, alternatives, rollback, and plain-language impact.
- [ ] Approve, reject, and defer are durable decisions.
- [ ] Agents prepare evidence but cannot approve a gate.

### Task T6.4 — Prove scoped recovery

- [ ] A disposable or otherwise safe rehearsal demonstrates partial-publication abort and rollback.
- [ ] Rollback touches only transfer-owned paths and preserves target history and unrelated changes.
- [ ] Native product checks and Git diff verify the recovered state.

## EPIC T7 — Publish and accept the CC_FIN pilot

**Depends on:** T3–T6 and M2  
**Labels:** `support-system`, `cc-fin`, `implementation`

### Task T7.1 — Integrate existing CC_FIN governance

- [ ] Support navigation references the enhanced product plan, feature ADRs, workflows, issue forms,
  freshness records, and release controls without creating competitors.
- [ ] Hosted changes, if any, have separate explicit authorization and recovery instructions.
- [ ] Product backlog and chart behavior remain unchanged.

### Task T7.2 — Publish CC_FIN support infrastructure in small isolated changes

- [ ] Preflight confirms HEAD, worktree, native baseline checks, target paths, recovery point, and claim.
- [ ] Neutral core precedes agent-owned additions.
- [ ] Paired guidance, coordination, handoff, ledgers, status/log, and validators pass.
- [ ] Partial failure stops; scoped rollback and post-rollback verification are available.

### Task T7.3 — Verify product preservation

- [ ] Existing native tests retain their semantics and applicable baseline behavior.
- [ ] The two existing charts and A–F cockpit remain present and unchanged by support work.
- [ ] Cockpit pipeline Task 23.12 remains in the product plan unless separately completed with evidence.
- [ ] No support asset imports or calls the Wiki repository at runtime.

### Task T7.4 — Independent review and M3 acceptance

- [ ] Claude independently reproduces support and product-preservation checks.
- [ ] Findings have explicit dispositions and all blockers are resolved/accepted/deferred.
- [ ] Owner accepts CC_FIN and explicitly authorizes CC_Loto publication.
- [ ] Pilot lessons and proven practices are recorded before T8 starts.

## EPIC T8 — Publish and accept CC_Loto

**Depends on:** T7.4 and M3  
**Labels:** `support-system`, `cc-loto`, `implementation`

### Task T8.1 — Integrate Loto planning and documentation governance

- [ ] Support navigation connects the enhanced product plan, U7, progress, roadmap, CI, and release policy.
- [ ] No competing product/scientific backlog or duplicate documentation-governance authority is created.
- [ ] Lessons from the FIN pilot are applied only when they fit the approved Loto profile.

### Task T8.2 — Publish CC_Loto support infrastructure in small isolated changes

- [ ] Preflight confirms HEAD, worktree, layered baseline checks, paths, recovery point, and claim.
- [ ] Neutral core precedes Codex-owned additions; Claude-owned guidance remains Claude-owned.
- [ ] Paired guidance, coordination, handoff, ledgers, status/log, and validators pass.
- [ ] No Wiki audit phases or pytest assumptions enter Loto.

### Task T8.3 — Verify data, test, and product preservation

- [ ] Required and optional test layers retain their existing meaning.
- [ ] Sensitive-data/index exclusions match the approved Loto profile.
- [ ] Scientific/product behavior and existing backlog remain unchanged.
- [ ] Partial failure can be rolled back without product-history or data loss.

### Task T8.4 — Independent review and M4 acceptance

- [ ] Claude and Codex reproduce evidence within their respective review responsibilities.
- [ ] Findings receive explicit dispositions.
- [ ] Owner accepts or rejects the Loto support implementation.

## EPIC T9 — Prove conformance and close the transfer

**Depends on:** T7, T8  
**Labels:** `support-system`, `conformance`, `closeout`

### Task T9.1 — Publish semantic conformance report

- [ ] Mandatory core semantics match even where paths, tools, and terminology differ.
- [ ] Every enabled module has an owner, tests, and target-local documentation.
- [ ] Every omission and deviation appears in the difference register.
- [ ] Neither target has a runtime dependency on the Wiki repository or global skill state.

### Task T9.2 — Publish reuse and difference report

- [ ] Reusable assets name both demonstrated consumers and their local adapters.
- [ ] Target policy remains local and no lowest-common-denominator semantics are introduced.
- [ ] Premature abstractions stay local with a reconsideration trigger.
- [ ] Future extraction candidates are recommendations, not silently created dependencies.

### Task T9.3 — Publish final target handoffs

- [ ] CC_FIN and CC_Loto handoffs contain verified Git, validation, index, blocker, and artifact state.
- [ ] Each handoff returns to the exact next action in its product-upgrade plan.
- [ ] Coordination queues contain unresolved work only; resolved records have manifests.

### Task T9.4 — Owner closeout gate M5

- [ ] Owner accepts, rejects, or defers transfer closeout.
- [ ] Remaining risks and follow-up work have owners and reconsideration dates.
- [ ] This plan's final status and completion evidence are recorded without rewriting its baseline history.

## 8. Risk register

| Risk | Prevention | Detection | Recovery |
|---|---|---|---|
| Existing authority is shadowed | Inventory and disposition before new paths | Navigation/authority validator and review | Remove only new shadow artifact; restore links to original authority |
| One agent edits the other's infrastructure | Ownership manifest and guidance | Git diff plus drift/coordination validation | Owner agent restores its side; immutable incident record |
| Product behavior changes during support work | Isolated commits and native baseline checks | Product tests, artifact comparison, Git diff | Revert only transfer-owned change; never broad reset |
| Partial publication leaves inconsistent support state | Atomic publishers, staged bootstrap, abort rules | Aggregate validator and pointer/board freshness | Scoped rollback to recorded recovery point |
| Secrets or sensitive data enter records/indexes | Approved sensitivity profile and exclusions | Secret scan, corpus inspection, index verification | Remove through reviewed history-safe procedure; rotate exposed secret |
| Wiki-specific policy leaks into targets | Contract/template review | Difference and forbidden-term checks | Replace adapter/configuration; preserve evidence of correction |
| Premature shared abstraction couples projects | Two-consumer evidence and repo-local deployment | Dependency/path scan | Inline/localize implementation and remove cross-repo dependency |
| FIN cockpit state is misrepresented | Explicit baseline constraint | Plan/status and product-preservation review | Correct record; product implementation remains untouched |
| Loto test semantics are replaced by pytest assumptions | Profile and native aggregate contract | Command/config review and layered runner | Remove foreign assumption and re-run native layers |

## 9. Definition of Done

The transfer is complete only when:

- [ ] T0–T9 acceptance criteria are satisfied with durable evidence;
- [ ] M0–M5 have explicit owner decisions;
- [ ] both product-upgrade Master Plans remain authoritative and navigable;
- [ ] both targets have validated repo-local support cores and paired-agent coordination;
- [ ] native product tests and behavior are preserved;
- [ ] rollback and partial-failure behavior have been demonstrated safely;
- [ ] secrets/data exclusions and index profiles are approved and verified;
- [ ] cross-project conformance and intentional differences are recorded;
- [ ] final handoffs name exact product-plan continuation actions; and
- [ ] all active claims are released and coordination validation passes.

Preparation of this document satisfies none of the implementation criteria by itself.
