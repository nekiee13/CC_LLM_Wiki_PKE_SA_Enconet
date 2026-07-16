# Draft support-system transfer plan — FIN and Loto

## 0. Document control

| Field | Value |
|---|---|
| Status | Draft for Claude review and owner agreement; not implementation authorization |
| Date | 2026-07-16 |
| Source specification | `doc/Support_system.md` |
| Target 1 | FIN — `C:\xPY\xPrj\CC_FIN`; `https://github.com/nekiee13/CC_FIN` |
| Target 2 | Loto — `C:\xPY\xPrj\CC_Loto`; `https://github.com/nekiee13/CC_Loto` |
| Format | GitHub-Issues style: epics → tasks → acceptance criteria, with dependencies |
| Constraint | No target-repository mutation or GitHub issue creation during specification review |

## 1. Objective

Prepare a decision-complete path for harmonizing software-development support across FIN
and Loto without copying Wiki-specific domain policy or replacing either project's existing
upgrade plan. The future implementation will deploy reviewed repo-local support instances
from common templates, with a mandatory core and project-selected modules.

## 2. Verified target baseline

The following was inspected read-only on 2026-07-16.

| Area | FIN | Loto |
|---|---|---|
| Repository | `main`, remote `nekiee13/CC_FIN`; inspected HEAD `238c207` | `main`, remote `nekiee13/CC_Loto`; inspected HEAD `b469afc` |
| Upgrade authority | `docs/project/CC_FIN_project_upgrade_plan_enhanced.md` | `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md` |
| Agent guidance | `AGENTS.md`; no root `CLAUDE.md` | `CLAUDE.md`; no root `AGENTS.md` |
| Tests | pytest, guardrail suites, optional CPI checks, targeted ruff | custom layered `run_tests.py`; optional dependency layer |
| Existing governance | GitHub PR template, workflows, issue template; feature-specific ADRs and governance records | CI workflow, `PROGRESS.md`, roadmap, documentation-governance EPIC U7 |
| Missing unified layer | No root handoff, coordination, support record taxonomy, shared AFI/LL/GP ledgers, or project state | No root handoff, coordination, ADR register, support ledgers, project state, or Codex guidance |

“Missing unified layer” does not mean no governance exists. FIN's governance fragments and
Loto's plan/progress/CI mechanisms must be mapped, preserved, or deliberately superseded;
they must not be shadowed by a second authority.

## 3. Transfer principles

- Preserve both enhanced product-upgrade plans as authoritative.
- Apply the design principles and core/module model from `Support_system.md`.
- Enable the full Codex–Claude coordination module in both projects.
- Use lightweight owner milestone gates, not Wiki G1–G7 or the Wiki audit state machine.
- Deploy repo-local support assets with no runtime dependency on the Wiki workspace.
- Integrate with each project's native tests, GitHub controls, paths, terminology, and risk.
- Bootstrap neutral records first; each agent then creates only its owned infrastructure.
- Treat this draft as a hypothesis until Claude review and owner agreement.

## EPIC T0 — Agree the support-system contract

**Depends on:** —

### Task T0.1 — Inventory and classify the Wiki support system

Publish `doc/Support_system.md` with every support element classified as `Core`,
`Module: <name>`, `Conditional: <condition>`, or `Wiki-specific adapter`.

**Acceptance criteria**

- [ ] Governance, planning, decisions, records, coordination, knowledge, handoff, gates,
      validation, Git/environment, indexing, skills, templates, and recovery are covered.
- [ ] Simplicity, cohesive modularity, God-component prevention, evidence-based reuse, and
      evolutionary scalability are explicit and qualified.
- [ ] Non-portable Wiki values are listed.

### Task T0.2 — Independent cross-agent review

Claude reviews the specification and this transfer draft against the live Wiki framework and
the read-only FIN/Loto baselines.

**Acceptance criteria**

- [ ] Review addresses completeness, portability, missing dependencies, and target conflicts.
- [ ] Every finding receives a Codex and owner disposition.
- [ ] Neither side claims agreement by silence.

### Task T0.3 — Owner agreement gate

Record accept, revise, or reject for the support-system specification.

**Acceptance criteria**

- [ ] Material review findings are resolved or explicitly accepted/deferred.
- [ ] Owner agreement is recorded before a final transfer Master Plan is prepared.

## EPIC T1 — Build target support gap profiles

**Depends on:** T0.3

### Task T1.1 — FIN evidence inventory

Map FIN's plans, guidance, ADR fragments, GitHub workflows, issue forms, documentation
freshness ledger, test commands, release behavior, and repository ownership.

**Acceptance criteria**

- [ ] Every existing support-like artifact has an authority and disposition: retain,
      integrate, migrate, supersede, or leave product-local.
- [ ] The enhanced FIN plan remains canonical for product upgrades.
- [ ] No planned support artifact is reported as already implemented.

### Task T1.2 — Loto evidence inventory

Map Loto's enhanced plan, `CLAUDE.md`, CI, `PROGRESS.md`, roadmap, documentation-governance
EPIC U7, package layout, and layered test runner.

**Acceptance criteria**

- [ ] The custom runner and optional-dependency semantics are preserved.
- [ ] Existing progress and roadmap records receive explicit dispositions.
- [ ] The enhanced Loto plan remains canonical for product upgrades.

### Task T1.3 — Gap and collision matrices

Compare both targets with the mandatory core and candidate modules.

**Acceptance criteria**

- [ ] Missing capability is distinguished from differently implemented capability.
- [ ] Path, naming, ownership, Git, test, and authority collisions are explicit.
- [ ] Scale assumptions and recovery requirements are identified for owner input.

## EPIC T2 — Approve project support profiles

**Depends on:** T1

### Task T2.1 — FIN support profile

Specify FIN authorities, record locations, agents, Git workflow, validation commands,
milestone gates, modules, scale assumptions, and recovery controls.

**Acceptance criteria**

- [ ] Profile integrates existing GitHub governance rather than duplicating it.
- [ ] pytest/CPI/ruff commands have truthful applicability states.
- [ ] Claude-owned additions are assigned to Claude, not Codex.

### Task T2.2 — Loto support profile

Specify the equivalent profile using Loto's package, CI, and layered test semantics.

**Acceptance criteria**

- [ ] No pytest assumption is introduced.
- [ ] Codex-owned additions are assigned to Codex, not Claude.
- [ ] U7 documentation governance is integrated into the support backlog.

### Task T2.3 — Difference register

Record intentional FIN/Loto differences against common support semantics.

**Acceptance criteria**

- [ ] Every deviation names rationale, owner, verification, and reconsideration trigger.
- [ ] Common semantics are not weakened by local wording.

## EPIC T3 — Transfer governance and recordkeeping core

**Depends on:** T2

### Task T3.1 — Authority and navigation skeleton

Plan project-local support index, recordkeeping contract, current status, event log, and links
to the existing master plan, architecture, AS-IS, and guidance.

**Acceptance criteria**

- [ ] One authority exists for each record class.
- [ ] Replaceable, append-only, immutable, generated, and historical records are distinct.
- [ ] Existing authorities are linked or migrated, never silently shadowed.

### Task T3.2 — ADR lifecycle and register

Plan one decision register per target and migrate/reference existing decisions.

**Acceptance criteria**

- [ ] Accepted ADRs are immutable and changed by supersession.
- [ ] FIN feature-specific ADRs receive an explicit integration strategy.
- [ ] Decision acceptance and implementation completion remain distinct.

### Task T3.3 — AFI, lessons, and good practices

Plan project-local evidence ledgers and typed transitions.

**Acceptance criteria**

- [ ] AFIs are non-blocking unless another authority makes them blocking.
- [ ] Closure retains evidence and creates reusable lessons when appropriate.
- [ ] Good practices require demonstrated project evidence.

## EPIC T4 — Transfer paired-agent coordination

**Depends on:** T2, T3

### Task T4.1 — Bootstrap neutral coordination

Create the neutral protocol, message/archive/claim structure, generated board contract, and
validation rules before either agent claims full synchronization.

**Acceptance criteria**

- [ ] Bootstrap ownership is explicit and does not authorize editing the other agent's files.
- [ ] Active/resolved/confirmed/archive semantics match the agreed specification.
- [ ] Blockers require disposition; silence is not confirmation.

### Task T4.2 — Complete paired guidance

Claude creates/updates Claude-owned guidance and Codex creates/updates Codex-owned guidance in
each target.

**Acceptance criteria**

- [ ] FIN gains its Claude counterpart without weakening FIN's current Codex rules.
- [ ] Loto gains its Codex counterpart without weakening Loto's current Claude rules.
- [ ] Semantic drift checks allow documented tool-specific differences.

### Task T4.3 — Claims, review, and archive tooling

Adapt repo-local coordination helpers and tests.

**Acceptance criteria**

- [ ] Overlapping active claims fail.
- [ ] Messages, replies, blocker disposition, resolution manifests, and board freshness are tested.
- [ ] One agent cannot archive or declare completion for the other's owned infrastructure.

## EPIC T5 — Transfer handoff and session continuity

**Depends on:** T3, T4

### Task T5.1 — Project handoff profile

Define required facts, project-native checks, Git/index state, blockers, artifacts, exact next
action, and follow-up queue for each target.

**Acceptance criteria**

- [ ] Passed checks require commands and integer exit codes.
- [ ] Failed, not-run, unknown, skipped, and not-configured remain distinct.
- [ ] Records contain no secrets or uncontrolled data.

### Task T5.2 — Publisher and pointer

Adapt and test a repo-local deterministic publisher from the shared handoff contract.

**Acceptance criteria**

- [ ] Immutable record validates before pointer publication.
- [ ] Status values are complete, partial, and blocked.
- [ ] Staleness and absent-Git behavior are tested.

### Task T5.3 — Start/close continuity

Integrate guidance, handoff, status, messages, claims, tests, and unfinished-work checks.

**Acceptance criteria**

- [ ] Session start reports divergence rather than silently resolving it.
- [ ] Session close validates before publishing handoff.
- [ ] Interrupted risky work requires resume-or-rollback owner direction.

## EPIC T6 — Transfer validation and milestone gates

**Depends on:** T2, T3, T5

### Task T6.1 — Support aggregate validator

Compose each target's native checks with support-record, coordination, handoff, navigation,
and drift checks.

**Acceptance criteria**

- [ ] FIN uses its pytest/CPI/ruff/CI contracts without inventing success for optional checks.
- [ ] Loto uses `run_tests.py` layers and preserves optional-dependency behavior.
- [ ] Aggregate output is deterministic and non-zero on applicable failure.

### Task T6.2 — Lightweight milestone packets

Define four approval points: baseline confirmed, support plan adopted, risky migration approved,
and support release accepted.

**Acceptance criteria**

- [ ] Packets name evidence, checks, risks, alternatives, and plain-language impact.
- [ ] Approve, reject, and defer are recorded.
- [ ] Agents assemble evidence but cannot approve the milestone.

### Task T6.3 — Architecture guardrails

Add project-appropriate checks or review triggers for modularity, coupling, complexity,
abstraction, reuse, and scale assumptions.

**Acceptance criteria**

- [ ] God-component signals trigger review, not blind mechanical splitting.
- [ ] New shared abstractions name demonstrated consumers and what duplication/layer they remove.
- [ ] Scale-oriented changes cite an approved assumption or measured bottleneck.

## EPIC T7 — Implement FIN support profile

**Depends on:** T3–T6 and final transfer Master Plan authorization

### Task T7.1 — Integrate existing FIN governance

Map feature-specific ADRs, workflows, issue forms, freshness records, and enhanced-plan tasks
into one support navigation and authority model.

**Acceptance criteria**

- [ ] Existing evidence and history are preserved.
- [ ] No competing master plan, ADR register, or CI authority is created.

### Task T7.2 — Publish FIN paired-agent and continuity infrastructure

Each agent publishes its owned side; shared records follow claims and cross-review.

**Acceptance criteria**

- [ ] Paired guidance, coordination, handoff, ledgers, and status/log records validate.
- [ ] FIN application behavior and product backlog remain unchanged unless separately authorized.
- [ ] Preflight records target paths, Git state, recovery point, and the reviewed rollback procedure.
- [ ] Partial publication stops safely; rollback changes only transfer-owned artifacts, preserves
      product history and unrelated work, and is verified by native tests and Git diff.

### Task T7.3 — FIN milestone acceptance

Run the target-native aggregate and obtain owner acceptance.

**Acceptance criteria**

- [ ] All applicable support checks pass with evidence.
- [ ] Intentional deviations are recorded in the difference register.

## EPIC T8 — Implement Loto support profile

**Depends on:** T3–T6 and final transfer Master Plan authorization

### Task T8.1 — Integrate Loto plan and documentation governance

Connect U7, progress, roadmap, CI, and the enhanced plan to the support authority model.

**Acceptance criteria**

- [ ] Existing product and scientific backlog remains authoritative.
- [ ] Support work does not duplicate U7 or change test semantics.

### Task T8.2 — Publish Loto paired-agent and continuity infrastructure

Each agent publishes its owned side and target-native support records.

**Acceptance criteria**

- [ ] Paired guidance, coordination, handoff, ledgers, and status/log records validate.
- [ ] No Wiki audit phases or pytest assumptions enter Loto.
- [ ] Preflight records target paths, Git state, recovery point, and the reviewed rollback procedure.
- [ ] Partial publication stops safely; rollback changes only transfer-owned artifacts, preserves
      product history and unrelated work, and is verified by native tests and Git diff.

### Task T8.3 — Loto milestone acceptance

Run the layered tests plus support validation and obtain owner acceptance.

**Acceptance criteria**

- [ ] Required and optional layers are reported truthfully.
- [ ] Intentional deviations are recorded.

## EPIC T9 — Cross-project conformance and closeout

**Depends on:** T7, T8

### Task T9.1 — Semantic conformance review

Compare the two local implementations with the agreed core and their approved profiles.

**Acceptance criteria**

- [ ] Core semantics match even where paths and tools differ.
- [ ] Every enabled module has tests and an owner.
- [ ] No target has a runtime dependency on the Wiki repository.

### Task T9.2 — Difference and reuse report

Record common assets, local adapters, deliberate differences, evidence, and future extraction
candidates.

**Acceptance criteria**

- [ ] Reuse claims name real consumers.
- [ ] Premature abstraction candidates remain local until evidence justifies extraction.

### Task T9.3 — Final handoffs

Publish verified FIN and Loto handoffs and close the transfer claims.

**Acceptance criteria**

- [ ] Each handoff names the exact next product-development action.
- [ ] Coordination is validated and active queues contain unresolved work only.

## Draft Definition of Done

This draft-planning stage is complete when:

- [ ] `Support_system.md` and this plan are committed and indexed in the Wiki workspace;
- [ ] Claude has independently reviewed both documents;
- [ ] findings have explicit dispositions;
- [ ] the owner has accepted or revised the support-system specification; and
- [ ] preparation of the final transfer Master Plan is explicitly authorized.

Nothing in this draft authorizes changes to FIN or Loto before that point.
