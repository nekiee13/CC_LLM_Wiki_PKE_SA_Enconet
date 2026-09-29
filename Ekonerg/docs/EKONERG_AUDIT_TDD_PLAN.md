# Ekonerg Audit Framework — Clean Transfer and First Audit

| Document control | Value |
|---|---|
| Version | 1.0 — exported owner-discussed plan |
| Date | 2026-09-29 |
| Status | Draft for Claude review; not an implementation completion record |
| Implementer | Codex |
| Reviewer | Claude, after every task |
| Source baseline | `9f20430c95334daa4c3cedb7ee71b002bd3be739` |
| Publication scope | Plan export and review request only; no framework transfer or ingestion |

## 1. Goal, decisions, and working rules

Build a clean Ekonerg project from the Enconet alpha framework. Then run the first Ekonerg audit using newly supplied documents.

Think of this as copying an empty workshop. We keep the tools and work instructions. We bring in new materials and start a new job record.

### Confirmed owner decisions

| Topic | Decision |
|---|---|
| Delivery | Two milestones: clean framework, then first Ekonerg audit |
| Location | Existing empty `Ekonerg/` directory in the workspace repository |
| Scripts | Copy all needed audit and support scripts into Ekonerg |
| Shared environment | The existing Python environment and browser runtime may be shared |
| Audit rules | Keep the current Appendix B/NQA-1 framework rules and human gates |
| Source documents | Ingest all regulatory and QMS documents again |
| Test data | Invented examples are allowed in isolated test fixtures |
| Evidence Access | Include offline evidence tools and EA6.5 classification bands |
| Output language | Croatian; source quotes stay in their original language |
| Input formats | Prepared Markdown and text |
| Source readiness | Owner supplies and approves the source set before intake |
| Implementation | Codex |
| Independent review | Claude, after every task |
| Claude setup files | Claude creates and maintains its own files |
| Plan format | Markdown with epics, tasks, dependencies, and acceptance criteria |
| GitHub issues | Do not create actual issues |

The owner must still supply audit-specific facts: source editions, Ekonerg scope, document versions, and the approved storage and backup locations. These are explicit tasks below. They will not be guessed.

### What the inspection found

- Ekonerg was empty before this plan export.
- Framework code at the inspected HEAD matches `9f20430`. Later commits concern coordination.
- Some support scripts still point directly to Enconet.
- Some files under `schemas/` hold approved Enconet run details. They are not blank templates.
- The scoring model still marks calibration as pending.
- The current text reader supports the input formats selected by the owner.
- Enconet's continuity check reports an unfinished run despite its closed project state.
- Available Enconet indexes are stale. This plan relies on live files for these findings.
- The shared Python executable exists. Its full compatibility still needs testing.

### Two release milestones

**M1 — Clean framework ready**

Ekonerg has its own tested tools, fresh records, and an empty audit database. No real sources have been ingested.

**M2 — First audit complete**

Fresh sources have passed the full audit flow. The owner has approved G1–G7. Croatian outputs and their evidence links pass validation.

### Rules for every task

Every task below is assigned to **Codex**, with **Claude as reviewer**. Owner decisions remain owner decisions. Claude's own setup files are a named external dependency.

For code changes, use this TDD cycle:

1. **RED:** Add a test that fails for the intended missing behavior.
2. **GREEN:** Make the smallest change that passes it.
3. **REFACTOR:** Improve clarity while keeping tests green.
4. **VERIFY:** Run focused tests and the required checks for that boundary.
5. **REVIEW:** Send Claude the task ID, commit, changes, and test evidence.
6. **CLOSE:** Resolve findings and record Claude's verdict before dependent work starts.

Keep existing tests that already pass. Do not break working code just to manufacture a RED result.

For document and audit-operation tasks, define the checks first, then create the record or run the approved process. A failed input check is not permission to change the evidence.

Each task record must include exact commands, integer exit codes, results, and artifact links. A skipped test is never a passed test.

### Definition of a clean project

Allowed at M1:

- Local code, schemas, templates, prompts, tests, and operating guides.
- The 18 criterion definitions and other fixed framework settings.
- Invented test fixtures, clearly marked as tests.
- New Ekonerg setup, review, validation, and handoff records.

Not allowed at M1:

- Enconet or regulatory source documents, quotes, chunks, or crumbs.
- Imported requirement records or supplier applicability decisions.
- Old databases, run folders, reports, dashboards, or evidence packages.
- Old approvals, findings, actions, exceptions, or release decisions.
- Real document excerpts hidden in tests, benchmarks, prompts, or skills.
- Links or imports that make Ekonerg depend on Enconet's runtime files.

The clean database may contain fixed criterion definitions. All source-derived and audit-run tables must be empty.

## 2. Milestone M1 — Build and prove the clean framework

### EPIC EK-0 — Agree on the transfer and review its scope

**What & Why:** Define exactly what will move. This prevents a folder copy from bringing old evidence or approvals into the new audit.

**Depends on:** None.

**Labels:** `epic`, `planning`, `review`, `M1`

#### Task EK-0.1 — Publish the plan and request Claude's review

**What & Why:** Store one plan and send a clear review request. Both agents need the same task list and stop points.

**Work:**

- Publish this plan as `Ekonerg/docs/EKONERG_AUDIT_TDD_PLAN.md`.
- Use the existing neutral coordination channel for this initial review.
- Send the review brief in Section 4, with the plan's commit and content hash.
- Record findings, fixes, and Claude's final verdict.

**Acceptance criteria:**

- [ ] Every epic and task has a What & Why, dependencies, and acceptance criteria.
- [ ] Codex and Claude roles are explicit.
- [ ] Claude checks both clean transfer and first-audit coverage.
- [ ] All blocking findings are resolved before framework implementation.
- [ ] Plain-language prose is checked for Flesch–Kincaid grade ≤9.
- [ ] The readability check records its tool, version, result, and excluded code/path/table tokens.

**Review status:** Pending. Export and review delivery are authorized. Framework implementation has not started. Formal readability measurement remains an open acceptance check; it is not reported as passed.

#### Task EK-0.2 — Freeze the source and list every transfer item

**What & Why:** Select files from a known Git revision. Each copied tool must have a known origin.

**Tests/checks first:**

- An unlisted file must fail the transfer check.
- A changed source hash must fail.
- Files from the dirty worktree must not enter the transfer by accident.

**Work:**

- Use committed framework files from `9f20430` as the source baseline.
- Record source path, destination, hash, purpose, and treatment.
- Classify each item as copy, adapt, recreate, or exclude.
- Inspect dependencies reached through imports, subprocesses, templates, schemas, and tests.
- Review file contents, not just folder names.

**Acceptance criteria:**

- [ ] The manifest covers all required runtime and support files.
- [ ] Every transferred file has a recorded origin.
- [ ] Real data and old decisions are excluded, including those under `schemas/`.
- [ ] Local uncommitted changes are excluded.
- [ ] Claude approves the manifest before files are copied.

**Epic exit:** The plan and transfer manifest have passed review.

---

### EPIC EK-1 — Create local tools and a safe project boundary

**What & Why:** Give Ekonerg its own tools and clear paths. Running an Ekonerg command must never read or change Enconet's audit by mistake.

**Depends on:** EK-0.

**Labels:** `epic`, `transfer`, `isolation`, `M1`

#### Task EK-1.1 — Build a safe copy process

**What & Why:** Copy only approved files into the empty destination. A preview lets the reviewer see exactly what will happen.

**RED tests:**

- Reject a wrong destination, path traversal, or a link that escapes the target.
- Refuse to overwrite an existing file with different content.
- Reject a source file absent from the manifest.
- Confirm preview mode writes nothing.

**GREEN work:**

- Add a transfer tool with a default preview mode and explicit apply mode.
- Read source bytes from the pinned Git revision.
- Copy the reviewed allowlist.
- Record created paths and hashes.
- Preserve licenses and code-origin notes.
- Define recovery as removal of only recorded, unchanged files from a failed new transfer.

**Acceptance criteria:**

- [ ] Preview and apply use the same manifest.
- [ ] Source and destination hashes match for unchanged copies.
- [ ] Adapted files are listed separately.
- [ ] A second run preserves matching files and refuses conflicts.
- [ ] Enconet files are unchanged.
- [ ] Interrupted transfer can be diagnosed and safely resumed.

#### Task EK-1.2 — Make all runtime and support paths local

**What & Why:** Copy handoff, coordination, and guidance checks too. This meets the owner's rule that scripts are not shared.

**RED tests:**

- Invoke commands from Ekonerg, the workspace root, and another directory.
- Run an isolated copy with no Enconet directory beside it.
- Detect imports or subprocess calls into Enconet or workspace script folders.
- Reject output targets outside the chosen project during normal audit commands.

**GREEN work:**

- Adapt all copied tools to resolve paths from the Ekonerg project root.
- Route audit closeout to the local handoff helper.
- Route local coordination to Ekonerg's own records.
- Copy required support schemas and test helpers.
- Remove dependencies on an editable Python package installed from Enconet.

**Acceptance criteria:**

- [ ] Normal Ekonerg commands use only Ekonerg code and data.
- [ ] Shared access is limited to the approved Python packages and browser runtime.
- [ ] Paths with spaces and Croatian characters work.
- [ ] Approved provenance text may name Enconet; active runtime references may not.
- [ ] Local support-tool tests pass.

#### Task EK-1.3 — Verify the shared environment

**What & Why:** Reuse the existing environment only after proving it can run Ekonerg. A path that exists does not prove the tools work.

**RED tests:**

- Missing packages produce a clear failure.
- A wrong or absent browser runtime fails its preflight check.
- A package import that resolves into Enconet fails isolation checks.

**GREEN work:**

- Check the existing `WikiEnconet` Python environment.
- Record the interpreter, package versions, browser version, and paths.
- Add a local environment guide and dependency specification.
- Test the browser with an invented offline page.
- If a dependency change is required, record its effect on both projects before changing the shared environment.

**Acceptance criteria:**

- [ ] Required imports and browser startup pass.
- [ ] Browser checks make no external web requests.
- [ ] No environment copy is placed inside the project.
- [ ] No shared dependency is silently upgraded.
- [ ] Any required upgrade has compatibility evidence for both projects.

**Epic exit:** Ekonerg tools work from their own project boundary.

---

### EPIC EK-2 — Create fresh state and prove that no old audit data remains

**What & Why:** Start with empty notebooks as well as empty source folders. Old approvals or run IDs could make a new audit look finished when it has not begun.

**Depends on:** EK-1.

**Labels:** `epic`, `database`, `clean-state`, `M1`

#### Task EK-2.1 — Create the Ekonerg skeleton and ledgers

**What & Why:** Create fresh folders and records that clearly say “not started.”

**RED tests:**

- Reject an initial phase other than `setup`.
- Reject an approved G1–G7 gate or an inherited decision reference.
- Reject the wrong supplier or output language.
- Detect old audit rows in source, intake, approval, and exception ledgers.

**GREEN work:**

- Set supplier to `ekonerg`, phase to `setup`, and output language to `hr`.
- Set G1–G7 to pending, with no dates or decision references.
- Start audit ledgers with their required headers.
- Create a new index, event log, current-status record, and project guide.
- Keep new framework review records separate from real audit approvals.
- Add local ignore rules for data, caches, database journals, and local editor state.

**Acceptance criteria:**

- [ ] No old audit history is present.
- [ ] Audit intake and approval ledgers have no inherited rows.
- [ ] New validation records identify the checks actually run.
- [ ] Status names the next action: finish clean-framework acceptance before intake.
- [ ] Generated outputs are absent.

#### Task EK-2.2 — Build the database from schema

**What & Why:** Create a new database from table definitions. Never copy a used database and try to empty it.

**RED tests:**

- All source-derived and run tables start empty.
- Fixed criterion definitions contain the expected 18 entries.
- Invalid foreign keys and duplicate IDs fail.
- A second initialization preserves existing data.
- An incomplete or populated database is not silently reset.

**GREEN work:**

- Use the copied schema and initializer.
- Include required schema changes in the fresh build path.
- Review any migration tool before using it.
- Keep reset operations outside the normal setup workflow.

**Acceptance criteria:**

- [ ] No Enconet database is read or copied.
- [ ] Required tables, indexes, and views exist.
- [ ] Integrity and foreign-key checks pass.
- [ ] There are no sources, crumbs, requirements, evaluations, findings, actions, or audit runs.
- [ ] Repeated initialization is safe.

#### Task EK-2.3 — Add the clean-state validator

**What & Why:** Prove that the clean project contains no old evidence. A search for the word “Enconet” alone cannot prove this.

**RED tests:**

Plant test contamination in an isolated fixture:

- An old quote inside a prompt or benchmark.
- A source file under an unexpected folder.
- An inherited approval or populated database row.
- A UAT contract with an old run ID, artifact hash, or approval.
- An output package containing real source-derived records.

**GREEN work:**

- Validate the file allowlist, database contents, ledgers, and run-bound contracts.
- Inspect test fixtures for real document excerpts.
- Allow only narrow, documented provenance references.
- Produce a clean-state report with counts and inspected paths.

**Acceptance criteria:**

- [ ] Every planted contamination case fails.
- [ ] Valid invented fixtures pass.
- [ ] Common ID syntax alone is not treated as contamination.
- [ ] The validator reports the exact file, field, or table at fault.
- [ ] M1 cannot pass without this check.

**Epic exit:** The database, folders, and records are proven clean.

---

### EPIC EK-3 — Adapt framework contracts, tests, and agent workflows

**What & Why:** Keep the useful rules while removing details that belong to one finished audit. Both agents must follow the same tested workflow.

**Depends on:** EK-2.

**Labels:** `epic`, `contracts`, `tests`, `governance`, `M1`

#### Task EK-3.1 — Separate reusable rules from run records

**What & Why:** A schema describes a form. An approved Enconet form is already filled in. Ekonerg needs the form, not the old answers.

**RED tests:**

- Blank setup cannot pass a release or UAT approval check.
- A release contract bound to another project or run fails.
- Missing source evidence cannot be replaced by taxonomy definitions.
- An unapproved scoring calibration cannot satisfy the Ekonerg evaluation gate.

**GREEN work:**

- Keep reusable taxonomy, authority roles, ID rules, scoring logic, and command contracts.
- Turn run-bound UAT, release, and promotion records into unapproved templates.
- Remove old hashes, source pointers, decisions, and candidate identities.
- Preserve pending scoring calibration until the owner makes an Ekonerg decision.
- Apply the existing authority model without importing its source evidence.

**Acceptance criteria:**

- [ ] Ekonerg has its own canonical schema copies.
- [ ] Setup validates without pretending that release inputs exist.
- [ ] Later phases fail when required run records are missing.
- [ ] No copied approval can authorize an Ekonerg action.
- [ ] Appendix B, Part 21, and NQA-1 roles remain distinct.

#### Task EK-3.2 — Rebuild a fully synthetic test set

**What & Why:** Tests should prove how the tools behave without carrying a company's documents.

**RED tests:**

- Tests fail if they require Enconet's database, source folders, or outputs.
- The fixture scan detects real excerpts and source-derived records.
- Test runs that target the real Ekonerg audit folders fail isolation checks.

**GREEN work:**

- Keep reusable test logic.
- Replace real data dependencies with invented regulatory-style and QMS-style examples.
- Rebuild expected hashes for those examples.
- Keep scoring, rendering, and sieving benchmarks distinct.
- Use temporary project roots for integration tests.

**Acceptance criteria:**

- [ ] Tests run with neither company's real corpus available.
- [ ] Invented examples are clearly labeled and never presented as regulations.
- [ ] Expected scores and counts are independently checked.
- [ ] Tests cover missing evidence, multiple quotes, repeated text, Croatian characters, and each rating.
- [ ] Test records never enter the real audit database or approval ledger.

#### Task EK-3.3 — Set up agent guidance and local coordination

**What & Why:** Codex and Claude need matching instructions and a clear review trail.

**Checks first:**

- Validate local command paths and phase rules.
- Detect missing required guidance and skill sections.
- Reject malformed messages, overlapping claims, and stale board content.

**Work:**

- Codex creates Ekonerg's `AGENTS.md` and its own adapted skills.
- Claude creates `CLAUDE.md` and its own skills and command adapters.
- Codex supplies Claude with the shared behavior contract.
- Set up local claims, messages, archive, and generated board.
- Record the Ekonerg policy for local support scripts and coordination.
- Run both the required workspace guidance checks and local contract tests.

**Acceptance criteria:**

- [ ] Both interfaces call the same Ekonerg stage tools.
- [ ] Claude's files are created by Claude.
- [ ] “Synchronized” is recorded only after both sides confirm.
- [ ] Every implementation task receives a separate Claude review.
- [ ] Resolved messages follow the archive rules; each agent handles its own records.

**Epic exit:** Reusable contracts and both agent workflows are ready.

---

### EPIC EK-4 — Prove the full workflow with invented data

**What & Why:** Run a small rehearsal before using real documents. This checks that the copied tools still fit together.

**Depends on:** EK-3.

**Labels:** `epic`, `integration`, `recovery`, `M1`

#### Task EK-4.1 — Test intake, extraction, and evidence links

**What & Why:** Prove the path from a text file to traceable evidence.

**RED tests:**

- Reject duplicate sources, changed raw files, empty text, and unsupported formats.
- Reject broken chunk offsets, invalid crumbs, wrong document sides, and unlinked quotes.
- Fail an import midway and confirm that it leaves no partial records.

**GREEN work:**

- Run invented RULE and DOCUMENT sources through local intake, text extraction, chunking, crumb import, and linking.
- Preserve exact quotes and all source references.
- Verify batch-size and lineage rules.
- Test updates as new source records, leaving prior records intact.

**Acceptance criteria:**

- [ ] Every accepted quote leads to the correct document and chunk.
- [ ] Database and source manifest agree.
- [ ] Failed imports roll back.
- [ ] Missing evidence blocks later stages.
- [ ] No Enconet file is accessed.

#### Task EK-4.2 — Test scoring, reports, and offline evidence tools

**What & Why:** Prove that one evidence package produces matching outputs that the owner can inspect.

**RED tests:**

- Refuse positive ratings without supporting DOCUMENT evidence.
- Refuse an unsupported not-applicable ruling.
- Detect score, count, and language differences between outputs.
- Detect broken evidence links and external browser requests.
- Check EA6.5 band order and boundary values.

**GREEN work:**

- Run an invented audit through evaluation and output generation.
- Use test-only approvals inside the temporary project.
- Exercise report links, quote cards, chapter references, adjacent context, copy, print, and the review workspace.
- Test document and package links as well as crumb links.
- Verify that labels and generated narrative use Croatian while quotes stay unchanged.

**Acceptance criteria:**

- [ ] Report and dashboard agree with the same package.
- [ ] All 18 criteria appear, including justified N/A entries.
- [ ] Scoring thresholds come from the scoring contract.
- [ ] Evidence views never show an unrelated crumb as an exact source.
- [ ] The portable package works from another folder without network access.
- [ ] Browser and applicable aggregate checks pass.

#### Task EK-4.3 — Test gates, interruption, and closeout

**What & Why:** Prove that a stopped session can resume safely and that “closed” means the records agree.

**RED tests:**

- Refuse skipped phases and missing, rejected, or wrong-run approvals.
- Detect stale handoffs and unfinished runs.
- Reproduce the mismatch between closed state and an unfinished evaluation.
- Interrupt handoff publication and candidate promotion.

**GREEN work:**

- Fix Ekonerg's copied workflow where tests expose a gap.
- Make closeout update or verify all required run-completion records.
- Preserve the previous valid handoff and release after a failed publication.
- Require an explicit owner disposition for incomplete real runs.

**Acceptance criteria:**

- [ ] A closed test audit has no falsely unfinished run.
- [ ] A failed check cannot publish a complete handoff.
- [ ] Rejected or missing approvals cannot advance a phase.
- [ ] Failed promotion preserves the previous approved artifacts.
- [ ] Recovery actions are logged and preserve evidence.

#### Task EK-4.4 — Release the clean framework

**What & Why:** Finish M1 with a tested empty project. The rehearsal must not become the first real audit.

**Checks first:**

- Re-run the clean-state validator on the real Ekonerg project.
- Run the full local test suite, sieving tests, benchmarks, support tests, and setup checks.
- Check that phase-dependent skips are reported honestly.

**Work:**

- Record the M1 evidence packet and Claude's review.
- Create Ekonerg-specific code and documentation index profiles.
- Keep evidence and agent-owned files out of shared-neutral index scopes as required.
- Certify indexes from committed state under an index-refresh claim.
- Publish a verified M1 handoff and request owner acceptance.

**Acceptance criteria:**

- [ ] Real audit state remains `setup`; G1–G7 remain pending.
- [ ] No real or test audit records have entered production data.
- [ ] Required tests pass with exact evidence recorded.
- [ ] Known failures are fixed before M1 is accepted.
- [ ] Index freshness and any unavailable checks are stated.
- [ ] Owner accepts M1 before real intake starts.

**Epic exit:** M1 is complete and accepted.

## 3. Milestone M2 — Run the first Ekonerg audit

### EPIC EK-5 — Define and approve the real input set

**What & Why:** Decide which documents and company activities the audit covers. This prevents the tools from filling gaps with guesses.

**Depends on:** Accepted M1.

**Labels:** `epic`, `intake`, `owner-gate`, `M2`

#### Task EK-5.1 — Prepare the owner's source and scope checklist

**What & Why:** Ask the owner for the facts that only the owner can supply.

**Checks first:**

- Missing editions, revisions, source identities, scope evidence, or required storage details leave intake blocked.

**Work:**

Codex prepares the checklist; the owner supplies and approves:

- Regulatory and NQA-1 source editions and amendments.
- Prepared Markdown/text files and their provenance.
- Ekonerg's QMS documents, revisions, and documented scope.
- Known missing documents.
- Approved storage, access, and backup locations.
- Any limits on publishing source material or evidence-bearing outputs.

**Acceptance criteria:**

- [ ] Each selected source has a clear identity and version.
- [ ] Ekonerg scope is supported by documents.
- [ ] Missing inputs are visible.
- [ ] Storage and backup arrangements are recorded.
- [ ] No regulatory edition or supplier capability is inferred.

#### Task EK-5.2 — Approve the intake order and first batch

**What & Why:** Process a small, clear group at a time so errors can be fixed before they spread.

**Checks first:**

- Reject a batch above the existing limit.
- Reject mixed large-document batches or missing source metadata.

**Work:**

- Start with governing and interpretive sources.
- Then process QMS scope and core quality documents.
- Continue through the remaining approved QMS set.
- Use one large document or two to three small documents per batch.
- Prepare the G1 records and the batch continuation plan.

**Acceptance criteria:**

- [ ] The owner approves the selected first batch and registry evidence.
- [ ] Each later batch has its own recorded checks and required decisions.
- [ ] The plan does not reuse an earlier batch's approval for new files.
- [ ] Unsupported file types stop with a clear explanation.

**Epic exit:** The real sources and intake order are approved.

---

### EPIC EK-6 — Ingest fresh regulatory and QMS evidence

**What & Why:** Build Ekonerg's evidence from its own sources. Every later conclusion must lead back to these files.

**Depends on:** EK-5.

**Labels:** `epic`, `ingestion`, `traceability`, `M2`

#### Task EK-6.1 — Register and process regulatory sources

**What & Why:** Rebuild the requirement base from the chosen source editions.

**Checks first:**

- Verify checksums, source metadata, document side, and authority role.
- Validate crumb structure and quote links before import.
- Reject requirements without supporting RULE evidence.

**Work:**

- Promote approved sources through the local intake path.
- Extract, chunk, sieve, validate, import, and link them.
- Build requirement records through the implemented tools.
- Keep governing rules distinct from NQA-1 interpretation.
- Record any unresolved authority or mapping issue.

**Acceptance criteria:**

- [ ] Every requirement traces to a newly registered source.
- [ ] All 18 criteria have the required coverage.
- [ ] No Enconet requirement rows or crumbs are reused.
- [ ] The selected source editions appear in the records.
- [ ] Claude reviews the completed batch evidence before dependent work.

#### Task EK-6.2 — Process Ekonerg QMS documents in bounded batches

**What & Why:** Turn each QMS document into small, traceable evidence records.

**Checks first:**

- Confirm revision, side, language, checksum, and batch membership.
- Check exact quotes, chunk links, and complete source/quote preservation.
- Refuse partial or invalid imports.

**Work:**

- Use the local prompts and the established agent-led sieving process.
- Record source, prompt version, run ID, and validation results.
- Do not assume the run-creation script itself generates LLM evidence.
- Complete each batch before starting the next.

**Acceptance criteria:**

- [ ] Every supplied document is processed or has a recorded disposition.
- [ ] Quotes remain verbatim.
- [ ] All accepted crumbs have valid provenance.
- [ ] Counts and warnings are recorded per batch.
- [ ] Failed records do not silently enter the active evidence set.

#### Task EK-6.3 — Review evidence quality and approve G2

**What & Why:** Check whether the evidence is faithful and sufficient before scoring it.

**Checks first:**

- Generate quality metrics, source-link checks, and a coverage matrix.
- Identify missing evidence, disputed links, and unclear scope.

**Work:**

- Review the first real evidence set in full.
- Record applicability for all 18 criteria from Ekonerg scope evidence.
- Apply the existing rule for unclear scope; do not silently assign N/A.
- Where tuning is needed, create a new generation, compare it, and seek the required promotion decision.
- Record lessons without copying raw source text into reusable skills.
- Prepare the G2 packet for owner review.

**Acceptance criteria:**

- [ ] Each applicability ruling has a written basis.
- [ ] Evidence exceptions have explicit dispositions.
- [ ] Metrics support review but do not replace source checks.
- [ ] Previous generations remain recoverable.
- [ ] The owner approves G2 before evaluation begins.

**Epic exit:** Fresh evidence and applicability are approved.

---

### EPIC EK-7 — Evaluate Ekonerg and approve findings

**What & Why:** Turn reviewed evidence into clear judgments and follow-up actions. A score is useful only when its basis is visible.

**Depends on:** EK-6.

**Labels:** `epic`, `evaluation`, `findings`, `M2`

#### Task EK-7.1 — Record scoring approval and draft evaluations

**What & Why:** Apply the retained scoring method under a new Ekonerg decision.

**Checks first:**

- Verify the model version and calibration status.
- Reject positive classifications without supporting evidence.
- Recompute scores independently.
- Test N/A handling and the applicable-criteria denominator.

**Work:**

- Present the retained model to the owner for explicit calibration approval.
- Draft each criterion's supporting evidence, contrary evidence, judgment, gaps, and actions.
- Keep all 18 criteria visible.
- Create the G3 packet.

**Acceptance criteria:**

- [ ] Model approval names the version used.
- [ ] No Enconet scoring approval is reused.
- [ ] Each judgment cites Ekonerg evidence or a stated gap.
- [ ] Calculated and independently checked scores agree.
- [ ] The owner approves G3 before the next controlled stage.

#### Task EK-7.2 — Draft findings and follow-up actions

**What & Why:** State what needs attention and what the auditor should do next.

**Checks first:**

- Reject findings with broken evidence or gap links.
- Detect missing actions for missing-evidence gaps.
- Reject draft findings presented as approved.

**Work:**

- Create findings with severity, basis, and evidence-or-gap links.
- Create document requests, checks, interviews, or sample-test actions as needed.
- Build the priority list.
- Present the G4 packet.

**Acceptance criteria:**

- [ ] Every finding has a clear basis.
- [ ] Every missing-evidence gap has a linked action.
- [ ] Draft and approved states remain distinct.
- [ ] The owner approves G4.
- [ ] Report generation uses only approved findings and actions.

**Epic exit:** Evaluation and findings are approved.

---

### EPIC EK-8 — Generate, test, and release Croatian outputs

**What & Why:** Give the owner a readable report and a usable evidence viewer, both built from the same audit facts.

**Depends on:** EK-7.

**Labels:** `epic`, `report`, `dashboard`, `UAT`, `M2`

#### Task EK-8.1 — Build the report and evidence package

**What & Why:** Generate one review candidate whose scores and citations can be checked.

**Checks first:**

- Validate the package and traceability chain.
- Check output language, scores, counts, findings, and required sections.
- Detect source or package changes after candidate creation.

**Work:**

- Build the Ekonerg evaluation package.
- Generate the Croatian report and its evidence bundle.
- Create a portable review package and record artifact hashes.
- Keep the candidate separate from any released output.

**Acceptance criteria:**

- [ ] The report agrees with the package.
- [ ] All factual claims have evidence or clearly stated limits.
- [ ] Quotes are unchanged.
- [ ] Evidence links resolve inside the Ekonerg package.
- [ ] The G5 packet names the exact candidate.

#### Task EK-8.2 — Test the dashboard and complete owner UAT

**What & Why:** Let the owner check the real Ekonerg review experience before release.

**Checks first:**

- Run dashboard, browser, link, package, and performance-budget checks.
- Test filtering, search, sorting, print, and evidence navigation.
- Check EA6.5 classification order and bands.

**Work:**

- Generate the dashboard from the same package.
- Create a fresh Ekonerg UAT record with actual run IDs and hashes.
- Ask the owner to inspect quotes, chapters, context, source identity, document records, and package records.
- Fix defects, rebuild, and repeat affected checks.

**Acceptance criteria:**

- [ ] Report and dashboard scores and counts match.
- [ ] Croatian interface text is readable.
- [ ] The package works offline.
- [ ] Owner acceptance covers the exact candidate hashes.
- [ ] Changed candidates require renewed acceptance of affected behavior.
- [ ] No Enconet UAT approval is reused.

#### Task EK-8.3 — Release outputs under G5 and G6

**What & Why:** Make the accepted candidate the controlled release, with a record of what was approved.

**Checks first:**

- Recheck candidate hashes and required approvals.
- Verify all release checks for the applicable phase.
- Test failure recovery before the real promotion.

**Work:**

- Record G5 and G6 in the proper sequence.
- Promote through the tested release path.
- Preserve a release manifest.
- Validate the promoted outputs.

**Acceptance criteria:**

- [ ] Promotion requires explicit owner authority.
- [ ] Released bytes match the accepted candidate.
- [ ] A failed promotion leaves no mixed release.
- [ ] Post-release checks pass.
- [ ] Claude records the technical review separately from owner approval.

**Epic exit:** Approved Croatian outputs are released.

---

### EPIC EK-9 — Close the audit and hand over follow-up work

**What & Why:** Leave a clear, reliable record of what was done and what remains open.

**Depends on:** EK-8.

**Labels:** `epic`, `closeout`, `handoff`, `M2`

#### Task EK-9.1 — Reconcile records and prepare G7

**What & Why:** Ensure the database, project state, approvals, and deliverables tell the same story.

**Checks first:**

- Run the full applicable aggregate and benchmark suite.
- Check unfinished runs, release manifests, source integrity, and open actions.
- Confirm backup evidence through a restore test in an isolated location.

**Work:**

- Record the disposition of all runs and exceptions.
- List approved follow-up actions and their next steps.
- Prepare the G7 packet.
- Ask the owner for the closeout decision.

**Acceptance criteria:**

- [ ] All required release checks pass.
- [ ] Open actions are visible and do not disappear at closeout.
- [ ] Backup restoration is verified.
- [ ] No incomplete run is falsely marked complete.
- [ ] The owner records G7 before the phase becomes `closed`.

#### Task EK-9.2 — Publish the final handoff and archive resolved work

**What & Why:** Make the project understandable to the next session without reconstructing its history.

**Checks first:**

- Validate handoff content, links, Git identity, phase, and check evidence.
- Run continuity checks.
- Check coordination records and index freshness.

**Work:**

- Publish through Ekonerg's local closeout and handoff tools.
- Record source baseline, Ekonerg changes, approved releases, and remaining actions.
- Refresh indexes from committed state under the required claim.
- Archive resolved messages through each author's own workflow.
- Record the exact next action.

**Acceptance criteria:**

- [ ] Handoff, status, database, and gate records agree.
- [ ] No false unfinished-run warning remains.
- [ ] Failed, skipped, or unavailable checks are stated.
- [ ] All resolved coordination records have confirmation evidence.
- [ ] A new session can identify the released outputs and remaining follow-up work.

**Epic exit:** M2 is complete.

## 4. Claude review request and delivery sequence

### Review brief to send

**Task:** `EK-PLAN-REVIEW`

**Recipient:** Claude

**Implementer:** Codex

**Requested verdict:** Approve, approve with non-blocking notes, or request changes.

> Review the Ekonerg clean-transfer and first-audit TDD plan.
>
> Ekonerg must own copies of all runtime and support scripts. It may share the existing Python environment and browser runtime. It must start with no ingested regulatory or supplier documents, no source-derived data, and no old audit approvals.
>
> The owner has selected Croatian outputs, prepared Markdown/text inputs, synthetic test fixtures, and EA6.5 with fresh owner acceptance. Codex implements each task. Claude reviews each task and creates its own agent setup files.
>
> Please check:
>
> 1. Whether the copy manifest and clean-state checks prevent evidence leakage.
> 2. Whether any runtime or support dependency still reaches Enconet.
> 3. Whether blank setup can pass honestly without weakening later checks.
> 4. Whether inherited run IDs, hashes, approvals, and UAT records are excluded.
> 5. Whether tests cover the full pipeline, offline evidence tools, and recovery.
> 6. Whether gates, scoring approval, and applicability remain owner-controlled.
> 7. Whether closeout resolves the unfinished-run mismatch.
> 8. Whether task dependencies and acceptance criteria are clear enough to implement.
> 9. Whether the explanations are readable for a beginner.
>
> Report each finding with the task ID, evidence, impact, and required correction. Do not treat this request as approval to ingest sources or release outputs.

### Delivery order

1. Publish the Markdown plan and its review request.
2. Claude reviews the pinned plan.
3. Codex resolves findings; Claude confirms the revision.
4. Complete EK-0 through EK-4, with review after each task.
5. Obtain owner acceptance of M1.
6. Complete EK-5 through EK-9 with the required owner gates.
7. Publish the final handoff.

This file exports the discussed plan. Checkboxes remain open until the named checks and decisions are evidenced. The review request will pin this file by commit and SHA-256; review completion is not implied by publication.
