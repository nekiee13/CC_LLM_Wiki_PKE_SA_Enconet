# T3 governance and recordkeeping contract v1.0

## Control and scope

This planning contract defines the common semantics required by EPIC T3 for CC_FIN and CC_Loto.
It does not create a new product authority, publish to either target, or authorize target writes.
The target-specific profile and manifest approved at M1 control later publication.

## Authority and navigation

Each target receives exactly one support navigation root at `support/README.md`. It links to current
product authorities and support records; it never copies product requirements, backlogs, progress,
architecture, feature decisions, CI policy, or release policy.

The conflict order is:

1. applicable law, explicit owner decisions, and controlled product requirements;
2. accepted product decisions and the owner-designated product Master Plan;
3. accepted support ADRs and the M1-approved project support profile;
4. current implemented evidence and validation results;
5. replaceable current status and active work records;
6. historical plans, superseded decisions, examples, and context.

The support index must label authority and state rather than rely on link order. A link cannot
promote a historical or proposed record. When authorities conflict, work stops and records the
conflict; an agent does not silently choose the most convenient source.

### Required target links

| Target | Product authorities linked from support index | Integration rule |
|---|---|---|
| CC_FIN | enhanced product Master Plan, project docs index, architecture/AS-IS, freshness ledger, feature ADR locations, GitHub workflow/issue governance, release/package status | Link existing records under their native names; preserve A-F Cockpit and product backlog status |
| CC_Loto | enhanced product Master Plan, prior-plan `PROGRESS.md`, ROADMAP, architecture/AS-IS, U7 documentation governance, CI, release/package status | Label prior 21/21 completion separately from enhanced U0-U19 status; integrate rather than duplicate U7 |

## Record taxonomy

| Class | Meaning | Change rule | Examples |
|---|---|---|---|
| Controlled | Current normative contract | Reviewed edit or superseding controlled version | support index, recordkeeping contract, profiles |
| Immutable | Evidence fixed after publication | New corrective/superseding record; never rewrite | accepted ADR, gate decision, handoff, resolution manifest |
| Append-only | Ordered event history | Append new entries only | support event log |
| Replaceable | Current readable snapshot | Replace after validation; history remains in Git/log | current status, HANDOFF pointer |
| Curated ledger | Structured current set with preserved transitions | Add or transition entries; never erase prior identity/evidence | AFI, lessons, good practices |
| Generated | Derived view, not authority | Regenerate from authoritative records | coordination board, reports |
| Historical | Retained non-current input | Do not edit to look current; link current successor | superseded plans/ADRs, context |

Every record declares or inherits one class. Generated and replaceable records cannot serve as the
sole evidence for an immutable decision. Historical records remain searchable but cannot override a
current authority.

## Current status, event log, and exact next action

`support/current-status.md` is replaceable and must state:

- timestamp, target HEAD, upstream relation, and whether the tree was clean when observed;
- current product-plan reference without copying its task state;
- active support milestone, claims/messages summary, blockers, and validation state;
- one exact next action with an owner, prerequisites, command or file entry point, and stop condition;
- the evidence records used to construct the snapshot.

Unknown, stale, or unavailable facts remain explicit. A dirty tree is described, not normalized.

`support/log.md` is append-only. Each event contains event type, UTC timestamp, stable subject ID,
concise evidence-based statement, and source/actor. Corrections append a new event referencing the
incorrect event. The log never substitutes for a gate record, ADR, test result, or product status.

The exact next action is deterministic enough that a new clone can start without reconstructing
intent from chat. If prerequisites fail, the action is to report/resolve the divergence, not to
continue optimistically.

## ADR lifecycle

### Identity and register

New portable-support decisions use `ADR-SUP-NNNN` and live under `support/decisions/`. Each target
has one discoverable `support/decisions/README.md` register. Existing product or feature ADRs keep
their paths, identifiers, and scopes; the support register references them in a separate
"Existing target decision authorities" section and never renumbers or copies them.

For CC_FIN this means its feature/subsystem ADR sets remain product-local decision authorities.
Support ADRs may depend on them by exact link and scope. For CC_Loto, the support register becomes
the support-decision root without claiming that no product decision exists elsewhere.

### States and transitions

| State | Meaning | Permitted transition |
|---|---|---|
| Proposed | Decision is under review and non-binding | accepted, rejected, withdrawn |
| Accepted | Owner/authorized authority approved it | superseded only |
| Rejected | Proposal was considered and declined | terminal; new proposal gets a new ID |
| Withdrawn | Author withdrew before acceptance | terminal; new proposal gets a new ID |
| Superseded | A newer accepted ADR replaces all or part | terminal, with successor link |

An accepted ADR is immutable. Corrections or changed decisions use a new ADR that links the old
one and states full or partial supersession. The register may update the state/link after the new
ADR is accepted, preserving Git evidence.

### Decision versus implementation

ADR acceptance means the decision is authorized; it does not mean code, configuration, guidance,
tests, migration, deployment, or hosted changes are complete. Each accepted ADR separately records
an implementation state (`not-started`, `in-progress`, `implemented`, `partially-implemented`,
`blocked`, or `not-applicable`) and links evidence. Only validated implementation evidence may move
that field to `implemented`.

## AFI lifecycle

AFIs are confirmed improvement opportunities, not defects or blockers by default. IDs use
`AFI-SUP-NNNN`. Required fields are observation, impact, evidence, scope, owner, state, related
authority/work, and next review/action.

States are `open`, `planned`, `deferred-until`, `owner-accepted`, `resolved`, and `superseded`.
Another named authority may make an AFI blocking; the AFI must link that authority. Resolution
records outcome and validation while preserving the original observation. A resolution may link a
lesson, ADR, test, or good-practice candidate; it never silently deletes the AFI.

## Lessons learned

Lessons use `LL-SUP-NNNN` and capture a surprising outcome, error, or constraint that should change
future behavior. Each entry records context, evidence, consequence, reusable rule, applicability,
counterexample/limit, related AFI/ADR/task, and state. States are `active`, `superseded`, and
`deprecated`. A lesson is not a good practice merely because it sounds reasonable.

## Good practices

Good practices use `GP-SUP-NNNN`. Promotion requires demonstrated target evidence: at least one
named outcome in the adopting target and a verification method. Two consumers are required only
when claiming a cross-project reusable abstraction. Each practice states problem, practice,
evidence, applicability, exceptions, owner, review trigger, and state.

States are `candidate`, `active`, `deprecated`, and `superseded`. `candidate` is non-normative.
Deprecation and supersession preserve the prior text and link the reason/successor. A Wiki-only
success cannot by itself prove a FIN or Loto good practice.

## Knowledge transitions

The normal evidence chain is observation → AFI → resolved outcome → lesson → candidate practice →
demonstrated active practice. Stages may be skipped only when the record supplies equivalent direct
evidence. Links remain stable in both directions where practical. None of these ledgers becomes a
parallel product backlog.

## T3 semantic acceptance

- Both targets have one link-only support navigation root.
- All record classes and correction rules are unambiguous.
- Status, log, and exact-next-action semantics are clone-complete.
- ADR acceptance remains distinct from implementation completion.
- Existing FIN decision authorities are referenced without renumbering.
- AFIs remain non-blocking unless another authority says otherwise.
- Lessons and practices preserve evidence and visible supersession.
- No target repository was modified.
