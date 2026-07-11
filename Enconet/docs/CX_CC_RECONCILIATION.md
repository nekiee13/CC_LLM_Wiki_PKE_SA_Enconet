# CX/CC Reconciliation and Implementation Start Gate

## 0. Document control

| Field | Value |
|---|---|
| Prepared | 2026-07-11 |
| Status | Proposed agreement for human approval |
| Scope | All `CC_*` documents and their relationship to the `CX_*` preparation artifacts |
| Purpose | Establish one evidence-backed starting point before implementation |

## 1. Documents reviewed

1. `CC_MASTER_DEVELOPMENT_PLAN.md` - proposed v1.2-CC revision of the master plan.
2. `docs/CC_ALIGNMENT_PLAN.md` - amended A0-A6 alignment backlog, renumbered C0-C6.
3. `docs/CC_PREPARATION_CRITIQUE.md` - independent review of CX findings and plan.
4. `docs/CC_PKE_NQA_Supplier_Audit_Wiki_Enconet_Upgrade_Plan.md` - earlier design/upgrade input
   that predates the relocation preparation and current sieving baseline.

Review method: jdocmunch section reads and outlines, CC/CX no-index diffs, jcodemunch source and
reference queries, and direct verification of the provenance, master-plan, and active tool behavior.

## 2. Confirmed agreement

### 2.1 CX findings confirmed

The CC review independently confirms 13 CX findings: missing Git identity, fail-open filters,
wrong-root/destructive tools, stale GUI instructions, workspace hierarchy mismatch, historical
context contamination, duplicated contracts, missing dependencies, Windows encoding failure,
CWD-dependent paths/eager writes, weak documentation navigation, narrow tests, cascaded verifier
errors, and baseline status mismatch. The CC phrase "13 of 15" treats two findings as corrected
rather than rejected; the underlying defects remain mostly valid with the refinements below.

### 2.2 Corrections accepted

1. **GUI disposition is closed.** `sieving/PROVENANCE.md` records the 2026-07-04 human decision
   to remove the standalone Streamlit GUI. The implementation task is documentation/tool cleanup,
   not a new architecture decision.
2. **Dead-code counts are heuristic and materially false-positive.** jcodemunch reference checks
   prove `flatten_multiple_files`, `export_dataframe`, `discover_json_files`, and `QueryEngine`
   are live through `__init__` re-exports. No deletion may rely on the reported percentage alone.

### 2.3 Additional CC findings accepted

1. **Blocking validation is missing.** `validate_item` returns ERROR objects, but
   `flatten_item_to_record` still returns a record, `flatten_json_to_records` appends it, and
   `run_pipeline` exports it. Invalid/missing `record_side` also bypasses all side-specific checks.
2. **The specification guide contains one dangerous false statement.** Section 10.1 says
   `config.py` obtains canonical criteria/codes through `AppBTemplate`; the modules actually contain
   separate tables and `config.py` imports no template module.
3. **The verifier and repair scripts form one hazard chain.** Missing dependencies become multiple
   import/structure errors; the verifier recommends a wrongly rooted mutating script.
4. **`check_files.py` validates an obsolete project manifest.** It expects removed GUI/example
   files and prints the old-machine path even if its root calculation is repaired.
5. **Index counts need snapshot identity.** Counts changed as preparation docs were indexed.
   Controlled criteria must test properties such as zero drift, not fixed corpus counts.

The CC critique says the CX documents have "4 material gaps" but Section 4 enumerates CC-1 through
CC-5. The agreed count is **five additional findings**.

## 3. Differences that require qualification

### 3.1 Handoff status

Master-plan v1.1 resolves the *design omission* by adding Task 0.7; it does not complete the
implementation. A valid Codex skill now exists at `~/.agents/skills/handoff/SKILL.md`
(relocated user-globally by CX_ADR-0015),
but the deterministic helper, Claude Code counterpart, schema validator, atomic-write tests,
second-project fixture, and session-start drift validator remain open. Status: **partially implemented**.

### 3.2 Master-plan variants

The prefixed master plans are intentional review variants requested by the human, not accidental
duplicates to delete during preparation. They do become a drift risk after approval. Agreement:

- preserve `CX_MASTER_DEVELOPMENT_PLAN.md` and `CC_MASTER_DEVELOPMENT_PLAN.md` until reconciliation;
- approve one merged revision;
- then publish exactly one canonical `MASTER_DEVELOPMENT_PLAN.md` and retain superseded variants
  through Git history or a controlled archive, not as competing live authorities.

### 3.3 CC master and alignment omit Codex discovery surfaces

The CC target uses only `CLAUDE.md` and `.claude/skills`. The user runs both agents. The merged
target must include:

- Codex: `AGENTS.md`, repo-local `.agents/skills/`, and user-global `~/.agents/skills/` for
  cross-project workflows such as `/handoff`;
- Claude Code: `CLAUDE.md`, `.claude/skills/`;
- a drift validator for equivalent rules/workflows, with documented tool-specific differences.

### 3.4 Earlier CC upgrade plan is a historical design input

`CC_PKE_NQA_Supplier_Audit_Wiki_Enconet_Upgrade_Plan.md` correctly establishes the validated data
spine, dual ingestion, canonical scoring, shared report/dashboard package, gates, and benchmark
separation. It is not an AS-IS contract and is superseded as an execution plan because it still
assumes Streamlit, legacy `json_tool/core.py`, `df._append`, and a different implementation order.

## 4. Master-plan changes accepted from CC

Adopt these v1.2-CC changes into the merged candidate:

- re-root the plan at `03_PKE_SA_NQA1/Enconet` with a separate workspace layer;
- unify title, document-control, and footer version claims;
- add an amendment log;
- add global docs, handoffs, decisions, and preparation inputs;
- treat the detailed alignment handoff contract as Task 0.7 detail, not a competing design;
- add `doc/INDEXING.md` and snapshot/caveat rules;
- retain closed human decisions unless an ADR explicitly supersedes them.

Add the dual-agent surfaces from Section 3.3 before accepting the merged master plan.

## 5. Agreed implementation backlog

Use the CX A0-A6 structure with CC amendments. The first implementation wave is:

1. **G0 - Baseline identity:** recover/confirm Git boundary, remote, branch, HEAD, and DATA policy.
2. **G1 - Governance:** publish dual-agent guidance, global doc scaffold, authority catalog,
   path contract, and one canonical master plan.
3. **G2 - Integrity containment:** quarantine obsolete repair tools, fix the verifier, make filter
   errors export-blocking, and add blocking crumb validation with a hard `record_side` enum.
4. **G3 - Reproducibility:** bootstrap dependencies and run risk-focused tests before larger refactors.
5. **G4 - Contract consolidation:** establish one schema owner and correct the spec guide in the same change.
6. **G5 - Continuity/indexing:** complete both agents' handoff integration, deterministic helper/tests,
   record taxonomy, controlled-doc navigation, and repeatable jmunch profiles.

Do not begin database/report/dashboard implementation until G0-G3 pass. Those outputs otherwise
risk being generated from unverifiable or invalid evidence.

## 6. Human decisions and recommended defaults

| ID | Decision | Recommended default | Blocks |
|---|---|---|---|
| D-1 | Git repository boundary | one repository at `03_PKE_SA_NQA1` | G0 |
| D-2 | DATA policy | track a small sanitized golden fixture set; keep full supplier corpus in an approved controlled store or Git LFS | G0/G3 |
| D-3 | Canonical schema owner | `Enconet/schemas` initially; promote to workspace scope only when a second project reuses the exact contract | G4 |
| D-4 | Context disposition | retain in place with authority catalog metadata until Git history is restored; move only through a reviewed migration | G1 |
| D-5 | Dual-agent policy | maintain both discovery surfaces; validate shared semantics and permit documented tool-specific rules | G1 |
| D-6 | Master-plan candidate | merge CC v1.2 structural corrections and confirmed findings into the CX candidate, then publish one canonical plan | G1 |

The GUI is not in this register because the 2026-07-04 retirement decision is closed.
The six domain decisions in Master Plan Section 8 remain separate human decisions; they do not
block the relocation/integrity work unless a task explicitly depends on one.

## 7. Start-gate acceptance criteria

Implementation may start at G0 when this reconciliation and D-1/D-2 are approved. Work may advance
beyond preparation only when:

- the repository identity is verifiable;
- one canonical master plan and one canonical alignment backlog are named;
- current/historical document authority is explicit;
- unsafe repair tools cannot be invoked through active instructions;
- the development environment can run the mandatory tests;
- filter and validation failures block audit exports by default;
- handoff and index status report `passed`, `failed`, `not-run`, or `unknown` explicitly.
