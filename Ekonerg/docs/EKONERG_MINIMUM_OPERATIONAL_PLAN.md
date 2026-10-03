# Ekonerg minimum operational audit plan

**Status:** proposed
**Goal:** run one controlled Ekonerg audit from document intake to a traceable
report.
**Assignee:** Codex implements. Claude reviews when available. The owner makes
the gate and release decisions.

## The shortest safe path

This plan has four epics and nine tasks. Each task is a batch. A batch may
contain many files, but it creates one result record and one review request.
We do not create a task for every file, quote, or script.

The plan stops if a gate fails. A failed gate creates one blocker record; it
does not create a new chain of small tasks. Code changes use TDD: write the
failing test, make the smallest fix, then run the required checks.

## Current starting facts

- `Ekonerg/incoming/` contains 31 source files.
- The draft route has 90 verified quotes, but no real sieving crumbs.
- Ekonerg's working activities are design, engineering services, and
  consultancy.
- Ekonerg is the only supplier in this audit scope; its supplier boundary is
  still vague.
- Part 21 is in scope mainly for nonconformances and corrective actions.
- ASME NQA-1 Part 1 is the mandatory interpretation baseline. Part 2 is not
  mandatory unless explicitly invoked. Parts 3 and 4 are guidance unless
  separately invoked.
- The preliminary Appendix B screen is 12 applicable, 6 conditional, and 0
  final N/A.

## Not part of this minimum plan

- A broad rewrite of the framework.
- A new task for each of the 225 transfer adaptations or 49 recreations.
- A browser, cloud, or live-service deployment.
- Automatic legal conclusions or automatic N/A decisions.
- A literal purge of immutable coordination and audit history.

---

## Epic MIN-0 — Freeze the run and prepare a clean workspace

**What & Why:** Agree on the small set of choices that can change the audit,
then make a safe empty run. This prevents old results or changed documents from
mixing with the new audit.

**Owner:** Owner for approvals; Codex for implementation.
**Depends on:** This plan and the 31-file incoming set.

### Task MIN-0.1 — Record the one-page owner gate packet

**What & Why:** Put the source, scope, and standard rules in one place. This is
like writing the rules on the cover of the audit notebook before taking notes.

**Work:**

1. Record the 31-file source register and its SHA-256 fingerprint.
2. Record the owner scope decisions already supplied.
3. Record the source snapshot/effective date and controlled backup location.
4. Record G1 approval for this exact source set, or record the blocker.

**Acceptance criteria:**

- [ ] The register lists every incoming file and its hash.
- [ ] The owner signs the source set, scope, Part 21 role, and backup choice.
- [ ] Part 1, Part 2, Part 3, and Part 4 roles are written as separate rules.
- [ ] No source is called approved when the owner has not approved it.

### Task MIN-0.2 — Reset and create a fresh run

**What & Why:** Remove old generated state without touching incoming documents
or the reusable framework. This gives the audit a clean starting line.

**Work:**

1. Run `reset_audit.py` in preview mode.
2. Check the plan and external backup destination.
3. Apply only after owner confirmation with `RESET-EKONERG`.
4. Create a new run ID and an empty project-local database.

**Acceptance criteria:**

- [ ] The reset plan is reviewed before apply.
- [ ] The backup ZIP is outside Ekonerg and can be opened.
- [ ] All 31 incoming hashes are unchanged.
- [ ] The database is empty and passes integrity and foreign-key checks.
- [ ] The run ID is new and does not reuse an old result.

---

## Epic MIN-1 — Prove the complete technical chain once

**What & Why:** Finish only the runtime wiring needed for one complete run.
Test it with fake data first, so real QMS files are not used to debug paths or
code.

**Owner:** Codex.
**Depends on:** MIN-0.2.
**Exit rule:** no new transfer slice is opened unless an acceptance test fails.

### Task MIN-1.1 — Wire the minimum local runtime as one batch

**What & Why:** Make ingestion, chunking, sieving, crumb import, validation,
evaluation, and reporting use only the Ekonerg tree. Also load the 18
company-neutral Appendix B criteria rows. The fresh database has the table but
no rows, so evaluation cannot start without this small seed step. This removes
the risk of silently reading Enconet or writing to the wrong project.

**Work:**

1. Create the empty database with `init_db.py`.
2. Run `seed_criteria.py` and verify the 18 rows.
3. Repeat the command and confirm that the first seed is preserved.

**Acceptance criteria:**

- [ ] Every command used by the test chain resolves paths under Ekonerg.
- [ ] No command imports code or data from Enconet.
- [ ] A synthetic company name with spaces and Croatian letters works.
- [ ] A synthetic sibling project remains byte-for-byte unchanged.
- [ ] A fresh database is seeded once with exactly the 18 criteria from the
  local taxonomy, using a deterministic test-covered command.
- [ ] The batch has one review record with exact test commands and exit codes.

### Task MIN-1.2 — Run one synthetic end-to-end rehearsal

**What & Why:** Run the whole conveyor belt with fake documents: ingest,
sieve, audit, and report. This proves the parts connect before real evidence is
used.

**Acceptance criteria:**

- [ ] A fresh synthetic run creates sources, chunks, crumbs, evidence links,
  one evaluation package, and one report.
- [ ] Every generated item has a run ID and source hash.
- [ ] A second run does not overwrite the first run.
- [ ] Missing evidence stays open; it is not silently scored as a pass.
- [ ] The complete rehearsal passes without reading Ekonerg or Enconet sources.

---

## Epic MIN-2 — Process the real Ekonerg documents

**What & Why:** Use the proven chain on the owner's 31 files. Keep source
intake, extracted text, crumbs, and audit judgments separate.

**Owner:** Codex.
**Depends on:** MIN-0.1, MIN-0.2, and MIN-1.2.

### Task MIN-2.1 — Ingest and chunk the approved source set

**What & Why:** Register the exact owner files and split them into reviewable
pieces. Hashes show that the audit uses the files the owner supplied.

**Acceptance criteria:**

- [ ] All 31 files are registered under the approved G1 record.
- [ ] All source hashes match before and after extraction.
- [ ] Extracted text and chunks link back to one source ID and hash.
- [ ] Missing images and missing chapters/sections are listed as open issues.
- [ ] No file outside `Ekonerg/incoming/` is treated as owner evidence.

### Task MIN-2.2 — Sieve, validate, and import crumbs as one batch

**What & Why:** Ask the approved prompts for rule and document crumbs, check
their shape, and import only valid crumbs. A crumb is a small, traceable piece
of evidence.

**Acceptance criteria:**

- [ ] The prompt version and source rule are recorded for every sieve run.
- [ ] Every imported crumb points to a source document and exact text.
- [ ] Invalid, duplicate, or unmatched crumbs are rejected and counted.
- [ ] The final crumb count is recorded by run ID; no count is guessed.
- [ ] Incoming documents remain unchanged.

### Task MIN-2.3 — Build the evidence and applicability matrix

**What & Why:** Connect each Appendix B criterion to Ekonerg evidence and the
owner's scope. This turns a pile of crumbs into an audit checklist.

**Acceptance criteria:**

- [ ] All 18 Appendix B criteria have one applicability record.
- [ ] The 12 applicable and 6 conditional preliminary decisions are checked
  against real work samples.
- [ ] Supplier/subcontractor scope is resolved or remains an explicit blocker.
- [ ] Part 21 nonconformance and corrective-action evidence is linked.
- [ ] Policy text is not treated as proof that staff used the control.

---

## Epic MIN-3 — Evaluate, report, and close the run

**What & Why:** Turn accepted evidence into reviewed judgments and a report.
Keep the report tied to the database and source hashes so it can be checked.

**Owner:** Codex prepares; owner approves.
**Depends on:** MIN-2.1 through MIN-2.3.

### Task MIN-3.1 — Pass the evidence gate and record evaluations

**What & Why:** A human must accept the evidence before the tool can grade it.
This prevents a polished report from hiding weak proof.

**Acceptance criteria:**

- [ ] G2 evidence acceptance is recorded for the run.
- [ ] G3 scoring method and calibration are approved before scoring.
- [ ] Each criterion has a traceable evaluation or an explicit open gap.
- [ ] Conditional criteria are not marked N/A without a recorded reason and
  owner approval.
- [ ] Part 2 material is used only where an explicit invocation is recorded.

### Task MIN-3.2 — Generate and validate the report and dashboard

**What & Why:** Build the report from the accepted run data. Do not copy
numbers by hand into a document or dashboard.

**Acceptance criteria:**

- [ ] Report and dashboard counts match the canonical run data.
- [ ] Every finding links to criteria, evidence, source hash, and status.
- [ ] Open evidence gaps are visible; missing proof is not called a pass.
- [ ] Aggregate validation, traceability, and schema checks pass.
- [ ] Claude review and owner release decision are recorded before publication.

### Task MIN-3.3 — Close out with backup and handoff

**What & Why:** Prove that the result can be recovered and tell the next
reviewer exactly what remains open.

**Acceptance criteria:**

- [ ] G7 closeout records the final approval and open actions.
- [ ] A restore test succeeds in an isolated location.
- [ ] The final run, report, backup, and validation hashes are recorded.
- [ ] The handoff names the next action and any unresolved issue.
- [ ] No source or result is deleted after closeout without a new approved
  reset plan.

## Minimum operational outcome

The framework is operational only when MIN-1.2 passes on synthetic data and
MIN-2.2 through MIN-3.3 pass on the real Ekonerg run. Until then, outputs are
draft work, not an audit conclusion.
