# Support system — portable software-development operating framework

## Document control

| Field | Value |
|---|---|
| Status | Draft for cross-agent review and owner agreement |
| Date | 2026-07-16 |
| Scope | Workspace-wide reference; intended for adaptation across heterogeneous projects |
| Origin | Support practices proven or implemented in `03_PKE_SA_NQA1/Enconet` |
| Target consumers | Wiki projects, `CC_FIN`, `CC_Loto`, and future projects |
| Authority | Informative draft until Claude review and explicit owner agreement; it does not supersede current ADRs, project plans, or guidance |
| Update trigger | Review disposition, owner agreement, or evidence that changes a support principle or module |

## 1. Purpose and boundary

The support system is the project's operating framework. It governs how work is planned,
decided, coordinated, validated, reviewed, recorded, transferred, and improved. It is
separate from the product or domain process: Wiki ingestion and sieving, FIN forecasting,
and Loto statistical evaluation are domain workflows and are not part of the reusable core.

The goal is harmonized engineering behavior without forcing unlike projects into one
directory layout, test runner, lifecycle, or architecture. Transfer therefore means:

1. preserve the target project's product authority and working mechanisms;
2. adopt common semantics and evidence standards;
3. instantiate support mechanisms locally from reviewed templates;
4. configure project policy, commands, paths, and risk controls locally; and
5. validate intentional differences rather than hiding them.

## 2. Design principles

1. **Simplicity first.** When alternatives satisfy the same requirements, choose fewer
   concepts, dependencies, runtime layers, and failure modes. Prefer explicit control flow
   and familiar technology over hidden magic.
2. **Cohesive modularity.** Organize code around one clear responsibility, a narrow public
   interface, explicit inputs and outputs, and independently testable behavior. Small means
   cohesive, not an arbitrary line count.
3. **No God components.** A module, service, script, class, or UI component must not become
   the default owner of unrelated responsibilities. Size and complexity thresholds are
   warning signals; multiple independent reasons to change are the decisive signal.
4. **Explicit contracts.** Reusable boundaries document inputs, outputs, errors, ownership,
   compatibility, and versioning expectations.
5. **Reuse by evidence.** Extract shared abstractions for demonstrated consumers or an
   explicitly approved transfer requirement, not hypothetical future reuse. The support
   system has three identified consumers, so a reusable reference is justified.
6. **Mechanism over policy.** Shared support assets provide mechanisms; project-specific
   commands, gates, paths, risk thresholds, and workflow policies remain local.
7. **Evolutionary scalability.** Record foreseeable users, data volume, execution frequency,
   concurrency, retention, runtime, and growth horizon. Avoid structural dead ends, but
   implement only capacity supported by current evidence.
8. **Composition over hidden coupling.** Assemble workflows from explicit, replaceable
   components; prevent circular dependencies and implicit shared state.
9. **Extract on touch.** When changing a hotspot, do not add another responsibility or
   materially worsen complexity without an explicit, evidence-backed disposition.
10. **No abstraction without a deletion story.** A new abstraction must remove duplication,
    isolate volatility, or simplify consumers; adding a layer is not itself progress.
11. **Contracts before automation.** Define record schemas, ownership, state, failure modes,
    and acceptance criteria before building helpers.
12. **Evidence or it did not happen.** Passed, failed, not-run, unknown, skipped, blocked,
    and not-configured are distinct states. Only recorded evidence supports completion.

“Reusable” does not mean making every function generic. “Scalable” does not mean introducing
distributed services, queues, caches, plugins, or concurrency before a measured need exists.

## 3. Complete support-element inventory

### 3.1 Project identity, authority, and guidance

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Workspace/project hierarchy | Separate shared policy from project policy | Workspace and nested project guidance | Core |
| Project boundary | Fix repository root, project root, ownership, and active paths | Root/project guidance and ADR-0001 | Core |
| Agent guidance | Give each agent read order, commands, guardrails, and completion rules | `AGENTS.md` / `CLAUDE.md` pairs | Core when agents are used |
| Nested no-weakening rule | Prevent local guidance from weakening evidence or safety | Workspace guidance contract | Core |
| Authority hierarchy | Resolve conflicts among current decisions, evidence, plans, status, and history | Guidance, recordkeeping, ADRs | Core |
| Human/agent roles | Separate execution and review from approval authority | Master plan roles and gate policy | Core |
| Infrastructure ownership | Prevent one agent from editing the other's discovery/configuration surfaces | ADR-0016 | Dual-agent module |
| Shared-neutral artifacts | Identify records either agent may query or update under coordination | ADR-0017/0019 | Dual-agent module |
| Guidance drift manifest | Machine-check equivalent semantics and documented differences | `GUIDANCE_PAIRS.json` | Dual-agent module |

### 3.2 Project definition and planning

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Architecture document | Describe boundaries, components, flows, and constraints | `doc/ARCHITECTURE.md` | Core |
| Functional analysis | Define required capabilities independently of implementation | `doc/FUNCTIONAL-ANALYSIS.md` | Core |
| Evidence-backed AS-IS | Distinguish implemented reality from intentions | `doc/AS-IS.md` | Core |
| Canonical master plan | Define mission, principles, epics, tasks, dependencies, and DoD | `MASTER_DEVELOPMENT_PLAN.md` | Core |
| GitHub-Issues-style tasks | Make work claimable and acceptance-testable | Epic/task/criteria plan structure | Core |
| Alignment/execution plan | Order foundation, containment, delivery, and closeout work | `docs/ALIGNMENT_PLAN.md` | Optional for complex upgrades |
| Canonical-plan control | Prevent competing active plans | ADR-0006 and archived variants | Core |
| Frozen baseline/amendments | Require visible approval for material plan changes | Document control and ADRs | Core |
| Definition of Done | State task, epic, milestone, and project completion evidence | Plans and validators | Core |
| Current-status snapshot | Give a replaceable, readable current view | `wiki/current-status.md` | Core |
| Exact next action | Make continuation deterministic | Current status and handoff | Core |
| Event log | Preserve append-only milestones and transitions | `wiki/log.md` | Core |
| Navigation indexes | Make current authorities and records discoverable | Workspace/project/wiki indexes | Core |

### 3.3 Decisions and change control

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| One-decision-per-file ADRs | Preserve context, decision, and consequences | `decisions/` | Core |
| ADR register | Provide stable navigation and status | `decisions/README.md` | Core |
| Immutable accepted decisions | Prevent retrospective rewriting | Supersede rather than edit | Core |
| Decision implementation evidence | Separate agreement from completed implementation | Tasks, commits, tests, messages | Core |
| Owner-decision capture | Promote material chat decisions to durable records | ADRs, log, approvals | Core |
| Historical/context classification | Keep inputs accessible without granting current authority | `docs/context/`, `_archive/` | Core |
| Reconciliation record | Resolve competing analyses without losing either input | `CX_CC_RECONCILIATION.md` | Optional |
| Generated-vs-controlled policy | Prevent manual editing of derived artifacts | Recordkeeping and validators | Core |

### 3.4 Recordkeeping

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Record taxonomy | Classify immutable, append-only, replaceable, curated, generated, controlled, and historical records | `doc/RECORD-KEEPING.md` | Core |
| Stable identifiers | Make records linkable across tools and time | ADR/AFI/LL/GP/task/message IDs | Core |
| UTC timestamps | Establish ordering without local-time ambiguity | Messages, claims, handoffs | Core |
| Mutability rules | Define whether correction means edit, append, supersede, or replace | Record taxonomy | Core |
| Cross-reference validation | Prevent dangling evidence and reply chains | Validators | Core |
| Truthful state vocabulary | Prevent missing checks from becoming implied success | Handoff and validation schemas | Core |
| Provenance/divergence log | Record origin and local changes to vendored assets | `sieving/PROVENANCE.md` | Conditional |
| Checksummed untracked-data manifest | Protect controlled data that Git must not contain | `DATA_MANIFEST.json` | Conditional |

### 3.5 Communication, claims, and review

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Repository message channel | Retain communication with the work | `coordination/messages/` | Dual-agent module |
| Typed immutable messages | Distinguish note, question, blocker, review, acknowledgement, claim, and status | ADR-0017 schema | Dual-agent module |
| Reply-to chains | Correct or acknowledge without rewriting history | Message frontmatter | Dual-agent module |
| Active/resolved/confirmed/archive lifecycle | Keep the active queue actionable and history durable | ADR-0018 | Dual-agent module |
| Resolution manifests | Record outcome and confirmation before archival | `coordination/archive/` | Dual-agent module |
| Blocker disposition | Require resolved, owner-accepted, or deferred-until | ADR-0018 | Dual-agent module |
| Task claims | Reserve work and anticipated files | `coordination/claims/` | Multi-writer module |
| Claim expiry/release | Avoid permanent locks without implying completion | Claim schema | Multi-writer module |
| Generated board | Summarize active claims and messages without becoming history | `BOARD.md` | Multi-writer module |
| Cross-review | Require independent reproduction proportional to risk | TEAM_PROTOCOL | Dual-agent module |
| Synchronization confirmation | Prevent one agent from claiming the other's side complete | TEAM_PROTOCOL | Dual-agent module |
| Conflict escalation | Preserve evidence and resolve through owner or ADR | TEAM_PROTOCOL | Core for multi-writer work |
| Parallel-work isolation | Require separate worktrees and non-overlapping claims | TEAM_PROTOCOL | Conditional |
| Coordination validator | Enforce schemas, uniqueness, claims, blockers, lifecycle, and board freshness | `agent_coord.py` | Dual-agent module |

### 3.6 Improvement and organizational knowledge

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| AFI ledger | Track confirmed improvement opportunities without silently making them blockers | `doc/AFI.md` | Core |
| AFI lifecycle | Open, planned, deferred-until, owner-accepted, resolved | ADR-0021 | Core |
| Lessons-learned ledger | Convert failures and unexpected outcomes into reusable rules | `doc/LESSONS-LEARNED.md` | Core |
| Good-practices ledger | Retain patterns proven effective by project evidence | `doc/GOOD-PRACTICES.md` | Core |
| Knowledge transitions | Link observation → AFI → resolution → lesson → proven practice | ADR-0021 | Core |
| Deprecation/supersession | Preserve failed or replaced knowledge visibly | ADR-0021 | Core |
| Knowledge-to-work links | Connect observations to tasks, decisions, tests, and commits | Ledgers and event log | Core |

### 3.7 Session continuity and handoff

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Shared handoff skill | Define evidence collection and truthful transfer semantics | User-global `/handoff` | Core |
| Immutable handoff records | Preserve objective, work, decisions, checks, state, risks, artifacts, and next work | `handoffs/` | Core |
| Mutable current pointer | Make the latest validated record easy to find | `HANDOFF.md` | Core |
| Handoff schema | Enforce required metadata, headings, status, and check evidence | `handoff_schema.yml` | Core |
| Deterministic publisher | Validate and atomically publish record, pointer, and log event | `make_handoff.py` | Core |
| Staleness check | Detect Git divergence from the recorded continuation state | Publisher helper | Core |
| Session-start read order | Read guidance, handoff, status, navigation, state, messages, and claims | Guidance and continuity tool | Core |
| Continuity comparison | Compare Git, narrative status, machine state, and unfinished work | `session_continuity.py` | Conditional |
| Resume-or-rollback decision | Prevent silent restart of interrupted operations | Audit lifecycle | Conditional |
| Validated closeout | Run required checks before publication | `audit-close` | Core mechanism, local commands |

### 3.8 Workflow state and human control

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Machine-readable project state | Make lifecycle state authoritative and inspectable | `project-state.yml` | Conditional |
| Fail-closed transitions | Prevent illegal or unapproved advancement | `audit_state.py` | Conditional |
| Human approval boundaries | Keep material decisions with the owner | Master plan and gates | Core principle |
| Standalone decision packets | Present evidence, checks, options, and plain-language impact | Gate packets | Milestone-gate module |
| Signed approval register | Give decisions stable evidence references | `approvals.csv` | Milestone-gate module |
| Rejection/deferral semantics | Stop advancement while preserving the decision | Audit lifecycle | Milestone-gate module |
| Canonical command registry | Define command, phase, implementation, outputs, and purpose once | `audit_commands.yml` | Workflow-interface module |
| Shared dispatcher | Prevent adapters from weakening checks or routing differently | `audit_command.py` | Workflow-interface module |

### 3.9 Quality, validation, and reproducibility

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Machine-readable contracts | Replace ambiguous prose at critical boundaries | Schemas and vocabularies | Core |
| Test/validator first | Demonstrate the gap before implementation | Alignment-plan convention | Core |
| Negative-path tests | Prove refusal, tamper, drift, duplicate, and partial-failure behavior | Test suites | Core |
| Aggregate validation | Provide one reliable health verdict | Validation runners | Core |
| Phase-aware applicability | Require artifacts only when the lifecycle says they should exist | Enconet aggregate runner | Conditional |
| SKIPPED ≠ PASS | Preserve truthful applicability and availability states | Validation policy | Core |
| No-record mode | Verify without mutating operational history | Aggregate runner | Recommended |
| Validation-run evidence | Record command, exit code, result, and context | Handoff/manifests | Core |
| Golden/reference benchmarks | Lock behavior whose correctness can be independently established | `benchmarks/` | Conditional |
| Independent generated-output validation | Re-read outputs instead of trusting generator success | Report/dashboard validators | Core principle |
| Drift checks | Detect divergence in guidance, skills, schemas, commands, docs, or indexes | Workspace validators | Conditional by artifact |
| Advisory versus blocking checks | State enforcement level explicitly | AFI/gate/validator contracts | Core |

### 3.10 Git, environment, tooling, and recovery

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Git workflow policy | Define branch, commit, review, and push expectations | `GIT_CONVENTIONS.md`, guidance | Core |
| Commit vocabulary | Make history scannable | Tagged commit purposes | Optional |
| Repository/identity verification | Avoid acting on copied or wrong-root state | Session protocol | Core |
| Ignore/line-ending policy | Stabilize generated and cross-platform behavior | `.gitignore`, `.gitattributes` | Core |
| Dependency pinning | Make runtime and tests reproducible | Requirements and lock files | Core |
| Environment inventory | Record actual interpreter/tools and missing isolation | AS-IS | Core |
| Safe repair/migration policy | Require target review, dry-run, backup, rollback, and verification | Guidance and lessons | Core when mutations exist |
| Backup verification | Prove recoverability with checksums and recorded targets | DATA backup records | Conditional |
| Reusable templates | Standardize records without duplicating runtime policy | Templates | Core mechanism |
| Support-tool tests | Test coordination, handoff, drift, structure, and validation tooling | Workspace tests | Core for automated support |

### 3.11 Indexing, navigation, skills, and interfaces

| Element | Purpose | Wiki implementation | Portability |
|---|---|---|---|
| Canonical code/docs indexes | Improve retrieval without duplicating repository views | ADR-0019 profiles | Index module |
| Corpus/exclusion profiles | Prevent raw, generated, historical, or agent-owned data leakage | `INDEXING.md` | Index module |
| Committed-state refresh | Give an index a reproducible Git identity | ADR-0019 | Index module |
| Single-writer refresh claim | Prevent concurrent corruption | `INDEX-REFRESH` | Index module |
| Index integrity verification | Detect drift, missing content, and errors | jdocmunch/jcodemunch checks | Index module |
| Skill placement model | Separate cross-project, workspace, and project workflows | `SKILLS.md` | Skills module |
| Duplicate-scope prevention | Avoid conflicting skill authorities | `check_skill_structure.py` | Skills module |
| Paired-skill semantics | Allow agent-specific implementations with one contract | Drift validation | Dual-agent skills module |
| Thin workflow skills | Keep mechanics in scripts/playbooks and judgment in skills | Enconet sieving skills | Skills module |
| Simple command vs workflow distinction | Avoid manufacturing a skill for every CLI | EPIC17 contract | Skills module |
| Interface registry and adapters | Give multiple agents/tools one canonical command behavior | EPIC17 | Workflow-interface module |

## 4. Framework model: core plus modules

### 4.1 Mandatory core

Every adopting project must define and validate:

- project identity, authority hierarchy, roles, and ownership;
- architecture, functional analysis, evidence-backed AS-IS, and one canonical plan;
- ADR register and supersession rules;
- record taxonomy, current status, event log, navigation, and stable identifiers;
- AFI, lesson, and good-practice lifecycle;
- Git/environment/recovery expectations;
- project-native validation commands and truthful result states;
- immutable handoffs, a validated pointer, and exact next action; and
- the design principles in section 2.

### 4.2 Selectable modules

| Module | Enable when | FIN/Loto draft selection |
|---|---|---|
| Dual-agent coordination | Codex and Claude both work in the repository | Enabled for both |
| Claims/board | Multiple writers can overlap | Enabled for both |
| Milestone gates | Baseline, migration, adoption, or release needs human approval | Lightweight gates for both |
| Formal state machine | Operations have ordered, unskippable phases | Not selected by default |
| Shared indexes | Repository scale and tooling justify indexed retrieval | Assess per target |
| Skills | A complex reusable workflow needs context and judgment | Assess per workflow |
| Golden benchmarks | Expected behavior can be independently fixed | Assess per product contract |
| Controlled-input provenance | Inputs require immutable origin and custody | Assess per project data risk |
| Workflow command registry | Multiple adapters need identical stage behavior | Assess after target inventory |

## 5. Project support profile

Before transfer implementation, each project must approve a profile containing:

| Profile field | Required decision |
|---|---|
| Identity | Repository root, project name, remote, active branch |
| Authorities | Guidance, master plan, ADR register, architecture, AS-IS |
| Roles | Owner, implementers, reviewers, external approvers |
| Agents | Enabled agents and ownership boundaries |
| Planning | Canonical backlog and amendment procedure |
| Records | Locations, IDs, mutability, navigation, retention |
| Git | Commit/push/PR/release policy |
| Validation | Install, unit, integration, lint, type, benchmark, and aggregate commands |
| Lifecycle | Status source, milestone gates, optional state machine |
| Coordination | Message, claim, review, and archive behavior |
| Handoff | Publisher, required evidence, pointer, staleness behavior |
| Modules | Enabled support modules and explicit omissions |
| Scale assumptions | Users, volume, frequency, concurrency, retention, runtime, growth horizon |
| Recovery | Backup, migration, rollback, and verification expectations |
| Indexes/skills | Approved profiles, owners, exclusions, and refresh/drift rules |

## 6. Reuse and deployment model

The reference specification, schemas, templates, and validators are reusable. Each target
receives a reviewed repo-local instance with local configuration and tests. Target projects
must not depend at runtime on the Wiki repository, and a transfer must not create a hidden
cross-repository path dependency.

Reuse follows these rules:

- reuse mechanisms; configure policies;
- keep product/domain imports out of the reusable support core;
- record template origin and local divergence;
- preserve existing target records and migrate by explicit mapping;
- do not create a second plan, ADR register, status source, or validation authority when a
  compatible one already exists; and
- prefer a little explicit duplication over a premature framework with unstable semantics.

## 7. Non-portable Wiki values

The following are examples or adapters, not framework requirements:

- `Enconet`, supplier, NQA, Appendix B, audit, crumb, and sieving terminology;
- the Wiki project's 18 epics and G1–G7 meanings;
- `setup → registered → ... → closed` phases;
- `incoming/`, `raw/`, `derived/`, and the current SQLite/data-spine layout;
- current audit command names, schemas, report/dashboard gates, and scoring rules;
- current index names and exclusion lists;
- Slovenian/English/Croatian and supplier-specific metadata policies;
- current benchmarks and project-local sieving skills; and
- CC/CX prefixes if a future project selects a different team model.

## 8. Agreement and promotion

This draft becomes an agreed support-system specification only after:

1. an independent Claude review checks completeness, portability, simplicity, modularity,
   reuse discipline, scalability qualification, and FIN/Loto compatibility;
2. findings receive explicit disposition;
3. the owner accepts the resulting specification; and
4. the decision is recorded before a final transfer Master Plan is published.

Until then, this document is planning input and does not authorize changes in `CC_FIN` or
`CC_Loto`.
