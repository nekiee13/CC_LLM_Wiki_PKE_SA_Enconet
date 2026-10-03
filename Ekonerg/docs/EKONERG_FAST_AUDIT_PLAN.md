# Ekonerg: process the documents and build the audit

Version: 1.0. Date: 2026-10-01.

Status: Plan written. The file list was checked. Audit tasks are not yet done.

Codex carries out each task. Claude reviews each task when available. The owner makes all gate and release decisions. These roles apply to every epic and task below.

## Goal and change of course

Assess whether Ekonerg's QA system meets 10 CFR 50 Appendix B, using ASME NQA-1 to interpret the rules. QA means quality assurance. QMS means the firm's quality management system.

We will read the supplied files, keep exact source links, and build a working audit report. Think of the evidence table as a notebook. Each claim must have an address that takes the reader back to its source.

The owner has stopped the long framework transfer route. This plan sets the next work order. EK-1.2 stays unfinished, with its code and review records kept. Further transfer slices are deferred. The older [framework plan](EKONERG_AUDIT_TDD_PLAN.md) remains the record of the full software scope.

The first useful output is a draft evidence table and a cited audit section. It can be shared with the owner while review is pending. Full framework release is no longer the start condition for this draft desk review. Formal source intake, scored results, approved findings, and final release still need their own gates.

## What is ready

The owner has supplied the files and asked that they be processed. The owner also stated that the supplied Appendix B and NQA-1 versions are valid. Record these choices once; do not ask for the files again.

The folder check found 31 Markdown files, with a total size of 1,851,547 bytes. File names suggest seven rule or standard files and 24 QMS files. Those groups are a starting list. Read the file contents to confirm each role.

- One file is named for Appendix B.
- Five files cover the NQA-1 preface and Parts 1 through 4.
- One file is named for 10 CFR Part 21.
- The QMS set has 23 procedure files and one manual, based on their names.

All files are already in a text format. Reading them does not need a new PDF or OCR tool. OCR means turning an image of a page into text.

The [earlier source note](transfer/EK_REGULATORY_INCOMING_IDENTITY.md) found a 2015 edition label in the NQA-1 preface. It did not prove the edition of each split file. It also found no capture date for the Appendix B file. Carry those checks into the source register. Do not guess a missing date.

Part 21 will get a source record and a scope note. Its presence does not add a new audit objective. Ask the owner only if its role affects a finding. The same rule applies to any disputed clause or QMS revision.

## Fixed scope and time limit

There are four epics and ten tasks. A batch is a unit of document work within a task. It does not create a new software slice or a new epic.

Technical setup has a total budget of 60 minutes of active work. This is a limit on setup, not an estimate for the whole audit. After that, use the safe direct-reading route for any readable file whose tool path is blocked. Record a genuine source or access problem and work on the other files.

The target for the first work session is a source register and the first cited criterion section. After that section, use the measured pace to estimate the rest. Do not promise a finish date from file count alone.

Only fix code if a defect blocks reading a file, keeping its evidence, or writing a traceable result. Explain the defect and its cost in the task record. All other software work goes to the deferred list. No new tools, services, or packages are required by this plan.

Deferred work includes full code transfer, broad code cleanup, a live audit database, dashboards, browser tests, score automation, and a release of the reusable framework. These items stay visible in the old plan. They are not marked done or dropped from a later release by this plan.

## Working rules

- Work in Ekonerg. Keep Enconet's sources, state, and approvals separate.
- Keep the owner's incoming files unchanged. Make new work copies with matching hashes when needed.
- A hash is a file fingerprint. Check it before and after a batch to detect changes.
- Use local scripts only when their paths and effects are known. The existing Python environment may be used.
- Read Markdown directly if a script needs a database or an unfinished workflow. Record exact file, heading, and line references.
- A search hit is a lead. Read the full relevant section and its context before using it as evidence.
- Keep original quotes in their source language. Write the report in Croatian. Label translations and link them to the original quote.
- Keep draft facts, draft judgments, reviewed results, and owner approvals distinct.
- A policy describes what should happen. Records, samples, and interviews may be needed to show what does happen.
- Treat missing evidence as an open issue. It is not proof that a control failed or passed.
- Ask only for missing facts or choices that affect the work. Keep unrelated document work moving.
- Use one result record per task, with its batches listed inside it. Keep exact checks, results, file paths, and open points.
- Aim for 30–50 pages of reading per sieving batch. Small documents of about
  10 pages are batched as triplets; medium documents of about 15–30 pages are
  batched as pairs; large documents over 40 pages are single-document batches,
  including user-prepared documents over 100 pages. Page count is a planning
  estimate only, not a document key or evidence locator.
- Codex decides boundary cases near 30–40 pages, pairs above 50 pages, or
  files without a reliable page estimate, and records a short sizing reason.
- Keep source text and evidence-bearing outputs local unless the owner permits their distribution. A code commit is not permission to upload the documents.

For any necessary code fix, use test-driven development, or TDD. First write a test that shows the defect. Then make the smallest fix, run the test, and run the required checks for that change. Test path changes with fake companies, including spaces and Croatian letters. Do not use real source text as test data.

For document tasks, define checks first, then create the records and check them. A skipped or blocked check stays visible. No check may be reported as passed without evidence.

Claude's pending software reviews remain pending. Codex can prepare draft work for review. No result is marked reviewed on Claude's behalf. A required review or owner gate still blocks formal release.

## Epic EF-1: Set up the source record

**What & Why:** List what the owner supplied and give each file a stable name in the audit. This keeps us from losing a file or citing the wrong version.

**Owner:** Codex. **Reviewer:** Claude. **Depends on:** The supplied incoming folder.

**Acceptance criteria:**

- [ ] All 31 files are in the register, or a new count is explained.
- [ ] Each work copy matches the source hash.
- [ ] Source choices, open facts, and G1 status are clear.
- [ ] A safe reading route is ready within the setup time limit, or its specific blocker is logged.

### Task EF-1.1: List and identify the supplied files

**What & Why:** Give each source an ID, version, and fingerprint. This is like putting a label on each book before we take notes from it.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** None.

**Work:**

1. List every file, byte count, and SHA-256 hash. Detect duplicate files by hash.
2. Read each title and version statement. Record language, document type, and any missing facts.
3. Check the NQA-1 split files for edition, order, missing sections, and overlap. Record the exact Appendix B snapshot supplied.
4. Record the owner's source statements and request to process this set. Link them to the dated file list.
5. Put genuine scope, revision, storage, or source questions in one short owner packet. Prepare the G1 record without inventing an approval.

**Acceptance criteria:**

- [ ] Each file has one stable source ID and its full relative path.
- [ ] Duplicate, empty, unreadable, or conflicting files have a stated disposition.
- [ ] A missing fact is marked unknown and linked to the affected file.
- [ ] Part 21 has an explicit scope status; no new audit duty is inferred.
- [ ] G1 names the source set and owner decision actually recorded.

### Task EF-1.2: Prove the small reading workflow

**What & Why:** Test the few steps needed to read and cite a source. This prevents another long setup phase before useful audit work starts.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** EF-1.1.

**Work:**

1. Choose a new local work folder. Keep original files and all prior Ekonerg work intact.
2. Make byte-identical work copies and link them to the source register. Record the chosen storage and access rules.
3. Test direct reading with a small fake Markdown file. Prove that a quote can be found again by heading and line range.
4. Test source-change detection and safe retry. A repeat run must preserve matching work and refuse a conflict.
5. Use a local extraction tool only if it adds value and passes its checks. At the setup limit, use direct reading for readable files.

**Acceptance criteria:**

- [ ] Original and work-copy hashes match; originals are unchanged.
- [ ] A sample quote resolves to the exact text and source ID.
- [ ] No script reads code or data from a sibling company.
- [ ] The setup log states elapsed time and any blocked tool.
- [ ] A local work copy is not described as a tested backup.

## Epic EF-2: Turn all supplied files into cited evidence

**What & Why:** Build two linked sets of notes: what the rules ask for, and what Ekonerg's documents show. This is the core audit work.

**Owner:** Codex. **Reviewer:** Claude. **Depends on:** EF-1 for the files in use.

**Acceptance criteria:**

- [ ] All 18 Appendix B criteria appear in the matrix.
- [ ] Every supplied file has a processing outcome.
- [ ] Each accepted claim has an exact source reference.
- [ ] Unread sections and source gaps remain visible.

### Task EF-2.1: Map the rules to the 18 criteria

**What & Why:** Make a checklist from the supplied rule text. NQA-1 clauses help explain the checks; their role and scope must be stated.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** EF-1.2 for the rule files.

**Work:**

1. Read the Appendix B text and identify each required element under all 18 criteria.
2. Map relevant NQA-1 clauses to those elements. Do not assume that matching chapter numbers prove a match.
3. Screen every supplied NQA-1 part. Record relevant clauses, guidance, and sections outside the stated scope, with reasons.
4. Keep binding source text, explanatory guidance, and the auditor's own reading in separate fields.
5. Start with the program and organization criteria for the first working section. Continue through all 18.

**Acceptance criteria:**

- [ ] Each requirement has a stable row ID and a cited Appendix B basis.
- [ ] Each NQA-1 link has a clause, source ID, and reason for the link.
- [ ] Conflicting or unclear scope is recorded for review.
- [ ] All five NQA-1 files and the Part 21 file have a documented outcome.
- [ ] Draft mappings are clearly marked until the required scope review is complete.

### Task EF-2.2: Read the QMS files and capture evidence

**What & Why:** Find the words and records that support each check. This turns the supplied procedures into usable audit evidence.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** EF-1.2 and the relevant draft rule rows from EF-2.1.

**Work:**

1. Read the QMS manual first for the stated scope. Then read the related procedures in small batches.
2. Use three small files, two medium files, or one large file according to the
   batch-sizing table in the local sieving playbook. Codex records a short
   sizing reason for boundary cases and preserves batch order.
3. Read full relevant sections, tables, notes, and references. Record both support and contrary evidence.
4. Give each quote a stable ID. Save its exact text, source ID, revision, heading, and line range. Add the printed page if the file has one.
5. Note referenced documents that were not supplied. Separate a stated policy from records that prove it was used.
6. Publish the first cited working section as soon as its source checks pass. Continue the same task for the remaining QMS files.

**Acceptance criteria:**

- [ ] Each of the 24 named QMS files is read or has an explicit blocker.
- [ ] Every quote matches the frozen text exactly.
- [ ] No page number is invented from a filename or a guess.
- [ ] Missing cited records and conflicting revisions have open issue IDs.
- [ ] Each batch states which files and sections were read and which remain open.
- [ ] The first working section is a draft and carries its review status.

### Task EF-2.3: Check coverage and prepare the evidence gate

**What & Why:** Check for holes before we judge the QA system. A full-looking table can still hide a missed file or a broken quote.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** EF-2.1 and EF-2.2.

**Work:**

1. Reconcile the file list, batch log, requirement rows, and evidence rows.
2. Check every accepted quote and source link. Keep failed rows out of the accepted evidence set.
3. Give each requirement a factual evidence status: found, partial, absent, or unclear. These are coverage notes, not compliance ratings.
4. Prepare a reasoned scope entry for each criterion. Unclear scope stays open; it does not become N/A.
5. Prepare the G2 packet with the coverage matrix, source checks, and open issues. Record Claude's review and the owner's actual decision.

**Acceptance criteria:**

- [ ] The register accounts for all 31 files and any approved later additions.
- [ ] All accepted quotes and IDs pass the link checks.
- [ ] All 18 criteria have evidence coverage and a scope status.
- [ ] No unsupported N/A entry hides a gap.
- [ ] G2 stays pending until the required review and owner decision exist.

## Epic EF-3: Draft judgments and useful follow-up work

**What & Why:** Explain what the evidence means and what still needs checking. The owner should see the reason for each draft finding.

**Owner:** Codex. **Reviewer:** Claude. **Depends on:** EF-2 and the gates named below.

**Acceptance criteria:**

- [ ] Each judgment has a rule basis, evidence, and stated limits.
- [ ] Missing proof leads to a clear follow-up action.
- [ ] Scores and approvals are used only when the required owner decision exists.
- [ ] A desk review is not presented as proof of all work done in practice.

### Task EF-3.1: Write a reasoned assessment for each criterion

**What & Why:** Explain where the QA system is supported by the documents and where proof is weak. This gives the owner useful answers before software is complete.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** EF-2.3; G2 before formal evaluation.

**Work:**

1. For each criterion, state the rule, support, contrary evidence, gaps, and limits.
2. Write early observations as draft desk-review notes while gates are pending.
3. Distinguish design of a control from proof that staff follow it. List records, samples, or interviews needed to close that gap.
4. Prepare G3 with the assessment basis. Use no numeric score or formal rating until the owner approves the method and any model version needed.
5. Leave scoring deferred if the owner has not approved it. Do not treat missing calibration as permission to pick weights.

**Acceptance criteria:**

- [ ] There is one section for each of the 18 criteria.
- [ ] Positive conclusions have relevant company evidence and the required review.
- [ ] An absence of proof is stated without guessing pass or fail.
- [ ] Every formal rating or score has its required G3 basis.
- [ ] The report states the limits of the document review.

### Task EF-3.2: Draft findings and next actions

**What & Why:** Turn each supported concern into a clear next step. A useful finding tells the owner what was seen, why it matters, and what needs proof.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** EF-3.1; required G2 and G3 decisions for formal findings.

**Work:**

1. Give each draft finding an ID, rule link, evidence or gap link, and plain description.
2. Keep missing evidence separate from a proven failure to meet a rule.
3. Add a linked document request, sample check, interview, or follow-up action.
4. Use an approved severity method if one exists. Otherwise leave severity pending and explain the concern in words.
5. Prepare the G4 packet. Record the owner's decisions and any unresolved reviewer findings.

**Acceptance criteria:**

- [ ] Each finding traces to a requirement and evidence or a named gap.
- [ ] Every missing-evidence gap has a linked action.
- [ ] Action owners and dates are agreed or clearly marked pending.
- [ ] Draft findings are not called approved findings.
- [ ] G4 approval is recorded before findings enter an approved report.

## Epic EF-4: Deliver a readable report and a clear handoff

**What & Why:** Give the owner useful audit work in simple files. Keep the review trail and remaining work clear so progress survives the next session.

**Owner:** Codex. **Reviewer:** Claude. **Depends on:** Checked outputs from EF-2 and EF-3.

**Acceptance criteria:**

- [ ] The owner has a Croatian working report and its linked evidence table.
- [ ] The files show their exact source set and review status.
- [ ] Final release and closeout are claimed only with the required gates.
- [ ] Deferred software work does not disappear from the record.

### Task EF-4.1: Build the working report and evidence table

**What & Why:** Put the work in files the owner can read now. Markdown is plain text with headings; CSV is a table that a spreadsheet can open.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** The first checked section from EF-2; then EF-3 as it completes.

**Work:**

1. Build a Croatian report with scope, source versions, method, 18 criterion sections, gaps, and limits.
2. Keep one main CSV evidence matrix. Use stable IDs in the report to link back to it.
3. Issue partial drafts as sections become ready. Name unread files and unfinished criteria in each draft.
4. Check that every report claim agrees with the matrix and the cited source.
5. Mark each version as draft, reviewed, or approved only when that status is supported.

**Acceptance criteria:**

- [ ] A partial draft lists what is complete and what is still open.
- [ ] The full draft accounts for all 18 criteria and all supplied files.
- [ ] Original quotes are exact; any translation is clearly labeled.
- [ ] Source links work from the local work package.
- [ ] The report and table contain the same judgments and open issues.

### Task EF-4.2: Review the package and record release decisions

**What & Why:** Let Claude check the work and let the owner choose what can be issued. A draft can help the owner while formal release is still pending.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** EF-4.1; G4 for an approved findings report.

**Work:**

1. Gather the task results into one review packet. Preserve each task's checks and open points.
2. Resolve Claude's findings when review is available. Record pending review honestly in the meantime.
3. Prepare G5 for the exact report candidate. Record file hashes so a later edit cannot reuse approval for old bytes.
4. Confirm the accepted delivery scope under G6. The planned dashboard and full framework tests remain deferred unless the owner explicitly changes that scope.
5. Release only the accepted package through an agreed local path. Check its files after release.

**Acceptance criteria:**

- [ ] Technical review and owner approval have separate records.
- [ ] Open required reviews block formal release, while draft work remains available.
- [ ] G5 and G6 refer to the exact accepted files and delivery scope.
- [ ] A report-only delivery has an explicit owner decision if it changes the old release scope.
- [ ] A changed candidate gets the required new checks and approval.

### Task EF-4.3: Record closeout and the exact next step

**What & Why:** Keep the next session from restarting old framework work. A short handoff should show the latest draft, open gates, and next audit action.

**Assignee:** Codex. **Reviewer:** Claude. **Depends on:** Latest EF-4 output; G5 and G6 for formal closeout.

**Work:**

1. Record which files and criteria were processed, the source hashes, and the latest artifact paths.
2. Keep open findings, missing records, and owner decisions in the next-action list.
3. Verify backup and restore before formal G7 closeout, using the owner's agreed storage plan.
4. Publish the session handoff with actual check results. Leave the audit open until the owner records G7.
5. Keep deferred transfer work in the old plan. Restart it only on an owner instruction.

**Acceptance criteria:**

- [ ] The handoff names one exact next audit action.
- [ ] It points to the latest report, matrix, and gate record.
- [ ] No failed, skipped, or blocked check is called a pass.
- [ ] A session handoff is not called full audit closeout.
- [ ] G7 is recorded only after required gates and backup checks are complete.

## Planned work files

All paths below are proposed outputs under Ekonerg. A listed path is not proof that the file exists. Use one dated work set and preserve earlier versions.

| Planned item | Purpose |
|---|---|
| `work/fast_audit/<work-id>/source_register.csv` | File IDs, versions, paths, hashes, and source status. |
| `work/fast_audit/<work-id>/sources/` | Unchanged local work copies tied to the register. |
| `work/fast_audit/<work-id>/basis.md` | The scope, source roles, edition checks, and open choices. |
| `work/fast_audit/<work-id>/batch_log.csv` | Files read, checks run, and each batch result. |
| `work/fast_audit/<work-id>/requirements.csv` | Rule elements, clause links, and scope notes. |
| `work/fast_audit/<work-id>/evidence.csv` | Exact quotes, their IDs, and source locations. |
| `work/fast_audit/<work-id>/matrix.csv` | Requirement-to-evidence links and draft assessments. |
| `work/fast_audit/<work-id>/issues.csv` | Missing facts, findings, and follow-up actions. |
| `work/fast_audit/<work-id>/report_hr.md` | The Croatian working report. |
| `work/fast_audit/<work-id>/decisions.md` | Actual owner decisions and the G1 through G7 status. |
| `work/fast_audit/<work-id>/checks.md` | Commands, exit codes, source checks, and reviewer results. |

The CSV files hold the main fast-audit records. The report draws from those rows. A later database import must keep their IDs and hashes; it must not force a second review of unchanged source text.

## Gate map and delivery order

| Gate | Evidence and decision to keep | Task |
|---|---|---|
| G1 | The selected sources, versions, scope, and actual owner intake decision. | EF-1.1 |
| G2 | Checked evidence, all 18 scope rulings, and owner acceptance. | EF-2.3 |
| G3 | The approved evaluation method, model version if used, and assessment decision. | EF-3.1 |
| G4 | Accepted findings and actions. | EF-3.2 |
| G5 | Acceptance of the exact report candidate. | EF-4.2 |
| G6 | Acceptance of the delivery package and any change to release scope. | EF-4.2 |
| G7 | Accepted closeout, backup evidence, and open-action handoff. | EF-4.3 |

Start with EF-1.1 and EF-1.2. Then map the rules and read QMS files in small batches. Publish the first checked section through EF-4.1 as soon as it is ready. Complete coverage, prepare judgments and findings under their gates, then seek release.

Owner approval of source validity and the request to process files support preparatory reading. They do not mean that all seven gates have passed. Draft work may continue while a formal gate is pending; a step that requires that gate must wait.

Missing software is logged against its affected route. The plan does not require a live database or a passing full-framework test suite to write a draft. It also does not claim that the existing full-framework checks have passed. Each release still needs the checks required for its agreed scope.

## Plan checks and next action

The prose must pass the existing Flesch-Kincaid check at grade nine or below. That is a reading-level check. The task structure must also pass a count check: four epics, ten tasks, and a What & Why note plus acceptance criteria for each.

See the [plan check record](reviews/EK_FAST_PLAN_CHECKS.md) for measured results, scope, and known limits. No real audit conclusion is made in this plan.

Next action: start EF-1.1 by hashing and identifying the 31 supplied files. Then prove the direct-reading route and begin the first rule and QMS evidence notes.
