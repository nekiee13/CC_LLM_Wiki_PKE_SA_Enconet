# T3 target-local template contract v1.0

## Purpose

The templates under `doc/support-transfer/templates/` are neutral design sources for later
publication. T7/T8 copy and render the accepted content into each target; target files must never
import, link to, or read this Wiki workspace at runtime. M1/M2/M3 and the publication manifest
remain the authorization controls.

## Configuration surface

Only the placeholders below are valid. Publication placeholders are resolved once when a template
is installed in a target. Snapshot placeholders are resolved every time the replaceable current
status is published.

| Publication placeholder | Meaning |
|---|---|
| `{{PROJECT_NAME}}` | Human-readable target name |
| `{{REPOSITORY_URL}}` | Canonical repository URL |
| `{{DEFAULT_BRANCH}}` | Accepted default branch |
| `{{PRODUCT_PLAN_PATH}}` | Owner-designated product Master Plan path |
| `{{PRODUCT_DOC_INDEX_PATH}}` | Existing target documentation navigation root |
| `{{NATIVE_VALIDATION_COMMAND}}` | Target-native validation entry point, not a universal runner |
| `{{SUPPORT_PROFILE_PATH}}` | Published target-local support profile/equivalent |
| `{{AGENT_OWNERSHIP_SUMMARY}}` | Target-specific Codex/Claude/shared-neutral boundary |
| `{{TARGET_DECISION_AUTHORITIES}}` | Links to existing target ADR/decision locations |
| `{{DATA_EXCLUSION_SUMMARY}}` | Approved target-specific secret/data/index exclusions |

| Snapshot placeholder | Meaning |
|---|---|
| `{{UTC_TIMESTAMP}}` | Observation time in UTC |
| `{{GIT_HEAD}}` | Observed full target commit SHA |
| `{{UPSTREAM_RELATION}}` | Ahead/behind/equal/unavailable relation and evidence |
| `{{WORKTREE_STATE}}` | Clean/dirty/unavailable state without normalization |
| `{{SUPPORT_MILESTONE}}` | Current support milestone and gate state |
| `{{ACTIVE_WORK_SUMMARY}}` | Active task and bounded scope |
| `{{COORDINATION_SUMMARY}}` | Claims, messages, and blockers |
| `{{VALIDATION_SUMMARY}}` | Commands, integer exit codes, and literal result states |
| `{{NEXT_ACTION_OWNER}}` | Responsible role or agent |
| `{{NEXT_ACTION_PREREQUISITES}}` | Required conditions before action |
| `{{NEXT_ACTION}}` | Deterministic next operation or entry point |
| `{{NEXT_ACTION_STOP_CONDITION}}` | Condition that stops/escalates instead of continuing |
| `{{STATUS_EVIDENCE_LINKS}}` | Links used to construct the snapshot |

A rendered asset contains no unresolved placeholder. Configuration is data in the rendering
manifest or explicit target text; scripts must not hide product policy in conditionals.

## Asset-to-target map

| Design template | Target-local destination | Class |
|---|---|---|
| `support-index.template.md` | `support/README.md` | controlled |
| `record-keeping.template.md` | `support/RECORD-KEEPING.md` | controlled |
| `current-status.template.md` | `support/current-status.md` | replaceable |
| `event-log.template.md` | `support/log.md` | append-only |
| `adr-register.template.md` | `support/decisions/README.md` | controlled register |
| `adr.template.md` | new `support/decisions/ADR-SUP-NNNN-slug.md` | immutable after acceptance |
| `afi-ledger.template.md` | `support/AFI.md` | curated ledger |
| `lessons-ledger.template.md` | `support/LESSONS-LEARNED.md` | curated ledger |
| `good-practices-ledger.template.md` | `support/GOOD-PRACTICES.md` | curated ledger |

## Target rendering profiles

### CC_FIN

- Uses existing `scripts/` for later support utilities.
- Support index links the enhanced plan, project docs, architecture/AS-IS, freshness ledger,
  feature ADRs, workflows/forms, and release/package status.
- Native command text describes pytest, applicable Ruff, and conditional CPI truthfully.
- Data exclusions name datasets, spreadsheets, vendor/archive trees, output/debug/cache classes.
- Existing feature ADRs appear only as referenced target decision authorities.

### CC_Loto

- Uses existing `tools/` for later support utilities; no new `scripts/` convention.
- Support index links the enhanced plan, separately scoped prior 21/21 progress, ROADMAP,
  architecture/AS-IS, U7, CI, and release/package status.
- Native command text uses `python run_tests.py` and preserves optional-layer reporting; it never
  assumes pytest.
- Data exclusions name `DATA.csv`, fixtures, DynaMix paths, model/output/cache/plot classes.
- Documentation governance links U7 instead of becoming a competing cleanup plan.

## Publication and validation rules

1. Render only into a disposable staging root during T3-T6 design/rehearsal.
2. Fail on an unknown or unresolved placeholder, absolute Wiki path, Wiki project name, supplier
   policy, sieve/raw/ingestion terminology, or runtime reference to this repository.
3. Compare staged output with the M1 path/ownership manifest before target writes.
4. Validate Markdown structure, stable IDs, relative links, record classes, and target commands.
5. Within the neutral-core publication, create and validate records, coordination, and handoff
   destinations before rendering `support/README.md`. The index closes the neutral core only after
   `HANDOFF.md` and `coordination/BOARD.md` exist, so no committed slice contains those dangling
   links. It still precedes every agent-owned addition.
6. Publish target-local copies only in T7/T8 after their applicable gates.
7. Target copies become independently maintained under their target authority and provenance.

## Reuse boundary

The templates demonstrate two consumers with common record semantics, so a shared design source is
justified. A shared runtime package, service, database, or cross-repository dependency is not
justified. Rendering/validation code remains target-local unless later evidence shows duplicated
behavior, two maintained consumers, and a safe version/rollback contract.

## T3.4 acceptance

- Templates contain common semantics and explicit target placeholders only.
- FIN and Loto configuration differences are visible in this contract.
- Target publication produces clone-complete repository-local assets.
- No template contains a runtime Wiki dependency or hidden project policy.
- Shared extraction is limited to the two demonstrated template consumers and does not create a
  shared runtime component.
