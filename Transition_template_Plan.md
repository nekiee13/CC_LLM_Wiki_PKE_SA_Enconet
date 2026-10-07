# Transition Template Plan

Date: 7 October 2026  
Implementer: Codex  
Reviewer: Claude  
Owner: approves deployment, sources, scope and required audit gates

## Goal

Start the next company audit from one tested framework. Copy tools and methods,
not another company's documents, crumbs, decisions or scores.

Target vendors: **IBE, TEKOL, IGH, IMK, KCPG and MOR**.

This plan uses the prepared v2 release. It does not approve a new audit or reopen
Enconet's closed audit. Work stays in a few clear tasks, not endless file slices.

## Current status

- [x] Detailed Ekonerg improvement summary saved.
- [x] Additive Enconet tool upgrade installed; existing audit evidence preserved.
- [x] Separate Enconet light and dark dashboard candidates built and tested.
- [x] Clean v2 package prepared: 123 framework files plus six setup records.
- [x] Read-only copy previews prepared for all six vendors.
- [x] Owner authorized clean framework folders for all six named vendors.
- [x] Clean framework installed in IBE, TEKOL, IGH, IMK, KCPG and MOR.
- [ ] Owner confirms that vendor's sources, editions and audit scope.
- [ ] New vendor deployment, intake and audit run completed.

The six vendor frameworks are installed; their audits have not started. No
database or company documents were copied. Claude review and Claude-owned
guidance synchronization remain pending. Future vendors use the same installer;
see [release usage](audit_template/README.md).

## Epic 1 - Keep one safe, reusable template

**What & why:** Use one versioned package so each new company does not need a
fresh round of script patches. Each company gets its own local script copies.

### Task 1.1 - Maintain the clean release

**What & why:** Keep code, common Appendix B criterion names, prompts and display
tools. Leave all company evidence and approvals out of the package.

Status: prepared and tested.

Acceptance criteria:

- [x] Release is stored in `audit_template/framework/v2/` with file hashes.
- [x] No raw sources, database, audit results or company golden fixtures copied.
- [x] Approvals start empty; no prompt is active by default.
- [x] Runtime uses local scripts, not sibling-company code or data.
- [x] Tests cover safe retry, conflicts and two synthetic company names.
- [ ] Claude completes the release review; changes, if needed, use a new version.

### Task 1.2 - Preserve existing audits

**What & why:** A software upgrade must not change a past audit's conclusion.
Enconet receives added tools, not Ekonerg's evidence or score.

Status: additive upgrade completed; future re-audit work not started.

Acceptance criteria:

- [x] Enconet's existing sources, database and approved outputs stay intact.
- [x] New dashboard candidates use Enconet's own stored results.
- [x] Candidate prompt is installed but not activated.
- [ ] Before an Enconet re-audit, check runtime compatibility and calibrate the
  prompt on Enconet documents. Do not inherit Ekonerg's calibration approval.

## Epic 2 - Start one selected vendor

**What & why:** Set up one clean project, check it, then use the same steps for
the other vendors. Do not copy a full populated company directory.

### Task 2.1 - Preview and apply setup

**What & why:** Show the owner what will be copied before writing files.
Conflicting files must stop setup rather than be overwritten.

Acceptance criteria:

- [x] Current previews exist for all six vendors in `doc/framework-reuse/`.
- [x] Owner authorized clean deployment for all six named vendors.
- [x] Fresh previews passed against the actual target trees.
- [x] Applies recorded separate run IDs and file-copy journals.
- [x] Each apply targeted only its selected company folder.
- [x] TEKOL was empty; no existing audit files needed removal.
- [ ] Local database is initialized separately; no company evidence is seeded.

### Task 2.2 - Record local choices and accept sources

**What & why:** The tools are shared, but each company's audit fence and valid
documents must be clear. Another company's approvals do not count here.

Acceptance criteria:

- [ ] Owner confirms supplier scope, output language and regulatory editions.
- [ ] Part 21 and criterion applicability are recorded for this company.
- [ ] ASME NQA-1 parts and roles are explicit; not every provision is treated
  as mandatory just because it appears in a source document.
- [ ] Current company and approved regulatory documents are in `incoming/`.
- [ ] Sources are inventoried, hash-registered and checked for missing content.
- [ ] Original incoming files remain intact.
- [ ] Required source and scope gates are recorded before dependent work starts.

## Epic 3 - Run the audit and show the result

**What & why:** Move quickly from setup to useful findings. Keep broad evidence
search, exact source links and clear explanations of each score.

### Task 3.1 - Ingest and sieve the full document set

**What & why:** Search every document for both words and the intent behind a
requirement. A control may be useful evidence even when it uses different terms.

Acceptance criteria:

- [ ] Documents are extracted and stored by chapter, with source identity intact.
- [ ] Full keyword and concept sweep covers the registered document set.
- [ ] Representative golden examples are reviewed and approved locally.
- [ ] Approved prompt is activated with recorded version and provenance.
- [ ] Sieving collects vendor crumbs with exact quotations and chapter links.
- [ ] High-level references remain leads; they are not automatic proof of a
  detailed control. Formal FAHP is not introduced by this plan.
- [ ] Coverage, exclusions and crumb counts are checked before evaluation.
- [ ] Required generation decisions are recorded before promotion.

Batch size is chosen by Codex to protect reading quality. Aim for about 30-50
pages: small documents may form triplets, medium documents pairs, and large
documents stand alone. These are guides, not hard limits.

### Task 3.2 - Evaluate, report and validate

**What & why:** Explain how vendor evidence supports each criterion, and show
weak areas that the owner can investigate during the real audit.

Acceptance criteria:

- [ ] All 18 Appendix B criteria have a recorded applicability decision.
- [ ] Each applicable criterion uses the existing five-point scoring method.
- [ ] Each rating has a short reason and linked vendor crumbs, not a count-only
  judgment. Missing proof and contrary evidence remain visible.
- [ ] Overall conformance uses the recorded applicable scope and scoring model.
- [ ] Report and light/dark dashboards use only this company's data.
- [ ] Cards show summaries, score support and real-audit verification actions.
- [ ] Clicking a crumb opens its related source chapter.
- [ ] Filters, search, sorting, expansion, mobile layout and print behavior work.
- [ ] Required validations run; skipped or failed checks are stated plainly.
- [ ] Output snapshots are stored under `out/yyyy-mm-dd/` with run provenance.

### Task 3.3 - Close the transition and repeat

**What & why:** Leave a short, verified record so the next vendor can follow the
same process without another framework repair cycle.

Acceptance criteria:

- [ ] Codex leaves task evidence and a review request in project coordination.
- [ ] Claude reviews when available; no review is claimed before it happens.
- [ ] Resolved messages follow the agent-owned archive rules.
- [ ] A verified handoff records results, failed checks and the exact next action.
- [ ] Repeat Epics 2 and 3 for each remaining vendor with fresh local decisions.

## Usage - setup commands

Run from the workspace root. Replace `IBE` with the chosen vendor.

### 1. Preview only

```powershell
python audit_template/prepare_vendor.py --target IBE --supplier IBE
```

This reads the target and reports the file plan. It does not deploy the project.
Use the actual supplier name in `--supplier`; quote names that contain spaces.

### 2. Apply after owner authorization

```powershell
python audit_template/prepare_vendor.py --target IBE --supplier IBE --apply --run-id ibe-setup-20261007
python IBE/scripts/init_db.py
```

Use a unique run ID for a new setup operation. The installer refuses differing
files. If it reports a conflict, inspect it; do not delete files to force setup.
The initializer creates a local database with the common criterion names only.

### 3. Begin local intake

Place documents in `IBE/incoming/`. Read that project's `AGENTS.md`,
`docs/FRAMEWORK_METHOD_V2.md`, `sieving/SIEVING_PLAYBOOK.md` and current state.
Record the local choices before using the phase workflow. A successful copy is
not a successful ingestion, approved calibration or completed audit.

## Reset and re-audit

Reset is for an authorized new cycle of the **same** vendor, not normal setup.
Preview the local reset plan and review its targets and backup policy first.
Keep incoming documents, framework code and required history. Generated audit
data can then be cleared through the tested reset path. A no-backup waiver must
be approved for that vendor; Ekonerg's waiver does not transfer.

## Scope limits

No new rating categories, formal FAHP, workflow redesign or per-file review
slices are added. Never modify controlled evidence in place without explicit
approval and a tested migration. Codex changes its own guidance; Claude owns
`CLAUDE.md`, `.claude/` and `CC_` records.

## Supporting records

- [Detailed Ekonerg summary](Ekonerg/docs/EKONERG_IMPROVEMENTS_SUMMARY_20261007.md)
- [Release status and validation evidence](doc/framework-reuse/ROLLOUT_20261007.md)
- [Enconet upgrade scope](Enconet/docs/FRAMEWORK_UPGRADE_20261007.md)

The prepared release passed 13 regression tests and 42 dashboard browser
checks. Enconet's aggregate passed all 19 checks. These validate the tools, not
a new company's compliance. The existing Claude-owned skill-structure defect
remains pending; it was not silently repaired or reported as passed.
