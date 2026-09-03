# Evidence Access and Review Workspace — TDD Delivery Plan

| Field | Value |
|---|---|
| Status | Reviewed — Claude approved 2026-09-03; owner architecture gate required before implementation |
| Plan ID | EVIDENCE-ACCESS-TDD |
| Created | 2026-09-03 |
| Requested by | Project owner |
| Implementer | Codex |
| Independent reviewer | Claude Code |
| Independent review | Approved with no residual findings (`CC_2026-09-03T133956Z_tdd-plan-final-approve`) |
| Primary production case | `RUN-20260728-01`, Appendix B evaluation |
| Planning style | GitHub Issues: epics, implementation tasks, dependencies, acceptance criteria |
| Delivery method | TDD: RED → GREEN → REFACTOR → full regression |
| Required Conda prefix | `C:\xPY\vEnv\WikiEnconet` |

> **Terminology:** this plan interprets “TTD” in the owner request as **TDD — test-driven
> development**. No production behavior is implemented before a failing test demonstrates the
> missing behavior.

## 1. Problem statement

The approved evaluation report contains reference-looking labels such as
`[crumb:CRUMB-DOC-0021-APP_B_I-0003]`, but they are plain text rather than navigable links.
The offline dashboard also renders crumb identifiers as plain text. The SQLite database already
contains the complete traceability chain:

`evaluation → crumb → original quote(s) → linked chunk → document metadata`

The missing component is a controlled presentation layer that lets the Owner click a report
reference and inspect the exact supporting source information.

### Confirmed baseline

- `scripts/generate_report.py` emits citation labels, not Markdown links.
- `templates/dashboard-template.html` prints `criteria[].refs` as text.
- The production database contains 46 documents, 687 chunks, and 252 active crumbs.
- All 62 distinct crumbs used by the production evaluation resolve to a crumb, quote, and chunk.
- One crumb may contain multiple quotes; the viewer must preserve and show all of them.
- The owner-required Conda prefix `C:\xPY\vEnv\WikiEnconet` was created on 2026-09-03
  with Python 3.13.15 and pip 26.2.1. EA0.6 installed the repository-pinned dependencies into
  that exact prefix. The first isolated `verify_install.py` run remains the recorded RED baseline
  (four missing runtime dependencies); the GREEN rerun reports zero dependency, structure, or
  import errors.
- The generated dashboard is already an approved offline, self-contained browser artifact.
- ADR-0007 retired the separate Streamlit sieving GUI. A new standalone GUI or live service
  requires a superseding owner decision.
- ADR-0011 keeps the Obsidian wiki projection at one page per criterion, not one page per crumb.
- Existing approved reports and dashboards are controlled outputs and must not be silently
  overwritten during development.

## 2. Recommended target

Enhance the existing self-contained offline dashboard into an **Evidence Explorer** and make
report citations deep-link to it. Build the evidence data as a deterministic, validated JSON
projection from the evaluation package and SQLite. Keep Obsidian unchanged.

When the Owner clicks a crumb reference, the browser opens an evidence panel showing:

1. crumb statement, item type, criterion, and document side;
2. every exact original quote and its source locator;
3. document ID, title, filename, language, and source hash;
4. linked chunk ID, heading path, offsets, link method, and confidence;
5. full chunk text with the selected quote highlighted;
6. previous/next chunk navigation where available; and
7. a printable/copyable traceability record.

### Proposed artifact flow

```text
SQLite + approved evaluation package
        |
        v
validated evidence bundle JSON
        |
        +--> offline dashboard / Evidence Explorer
        |        ^
        |        |
        +--> evaluation report deep links
        |
        +--> generated run catalog / landing page
```

### Reference behavior decisions

- **Action rows gain a new primary link.** Today an action line prints a bare `ACT-*` identifier and
  ends with a citation to its related finding. The upgraded report will make the action identifier
  itself a clickable `action` entity link while retaining the separate finding/evidence citation.
  This is an intentional scope addition and requires its own RED test; it is not represented as
  existing behavior.
- **A gap self-reference opens a gap detail view.** Today a gap row ends with
  `[gap:<its-own-ID>]`. That target will open one non-recursive gap panel showing the gap
  description, criterion/evaluation, `missing_evidence_ref`, optional evidence crumb, and related
  findings/actions. It does not pretend that the gap is source evidence, and it does not follow its
  own self-reference recursively.

### Non-goals for the first release

- No write access to SQLite from the browser.
- No editing, approving, rescoring, re-sieving, or prompt tuning in the viewer.
- No per-crumb Obsidian pages; ADR-0011 remains intact.
- No external network calls, CDN assets, telemetry, authentication, or cloud hosting.
- No Streamlit restoration or local server until the Owner separately supersedes ADR-0007.
- No arbitrary output file treated as authoritative input. Selection is by registered audit run
  and its validated package/artifact lineage.

## 3. TDD and tracking rules

Every implementation issue follows this sequence:

1. **RED:** add the smallest test that expresses the missing behavior and record its expected
   failure. A test that passes before implementation is not accepted as RED evidence.
2. **GREEN:** implement only enough production code to pass that test.
3. **REFACTOR:** remove duplication and improve structure while keeping all focused tests green.
4. **REGRESSION:** run the relevant epic suite, then the mandatory aggregate suite at the epic
   boundary.
5. **REVIEW:** Claude independently reviews the diff and reproduces acceptance evidence before
   the epic is marked complete.

Progress markers:

- `[ ]` not started
- `[-]` active
- `[x]` accepted with test/review evidence
- `[!]` blocked; the blocking decision or dependency must be linked in the issue

Each completed issue must record:

- issue/epic ID;
- RED test name and failure reason;
- GREEN command and integer exit code;
- regression command and result;
- changed artifact paths;
- reviewer response; and
- owner gate reference when the issue changes a controlled output.

## 4. Milestones and dependency order

| Milestone | Epics | Exit condition |
|---|---|---|
| M0 — Environment, decision, and contracts | EA0 | Isolated Conda environment passes verification; Owner approves architecture and candidate-output policy |
| M1 — Evidence projection | EA1 | Deterministic bundle resolves all production evaluation references |
| M2 — Clickable review surface | EA2–EA3 | Browser click opens exact source evidence from the report |
| M3 — Multi-run review | EA4 | Owner selects a registered run and receives its matched artifacts |
| M4 — Controlled release | EA5–EA6 | Full validation, independent review, human acceptance, promotion |
| M5 — Optional live service | EA7 | Separate owner decision only; not required for M4 |

Implementation order:

`EA0 → EA1 → EA2 → EA3 → EA4 → EA5 → EA6`

`EA7` is a deferred decision branch and must not block the offline release.

---

# EPIC EA0 — Architecture, governance, and executable contracts

**GitHub issue title:** `EA0: Freeze the evidence-access architecture and acceptance contract`

**Goal:** Remove design ambiguity before UI work and turn the current defect into reproducible
tests.

**Epic acceptance criteria**

- [ ] Owner selects the offline Evidence Explorer as the first delivery target.
- [ ] Candidate artifact naming/promotion policy is recorded without editing the frozen master or
  alignment plans.
- [ ] Current plain-text citations are captured by failing characterization tests.
- [ ] Evidence bundle schema and URI/fragment grammar are machine-readable.
- [ ] No task contradicts ADR-0007, ADR-0008, or ADR-0011.
- [x] Base Conda environment exists at `C:\xPY\vEnv\WikiEnconet` with Python 3.13.15 and
  pip 26.2.1.
- [x] The isolated environment contains declared dependencies and passes installation, focused,
  and aggregate verification without borrowing packages from the base environment.

## Task EA0.1 — Reproduce and characterize the broken navigation

**GitHub issue title:** `EA0.1: Add RED tests for non-navigable report and dashboard citations`

**ELI5:** Before fixing the door, prove that the current handle does not open it.

**Tests first — RED**

- Add a report test asserting that every emitted `crumb`, `document`, `gap`, and `finding`
  reference is a real link with a stable target.
- Add a RED test proving that each current `ACT-*` identifier is bare text, then requiring the
  upgraded report to add a new clickable action-entity link while preserving its related finding
  citation.
- Add a dashboard test asserting that evidence references are buttons/links rather than a single
  text node.
- Add a production-fixture test using `CRUMB-DOC-0021-APP_B_I-0003` and assert that the target can
  resolve three quotes and `CHUNK-DOC-0021-0105`.
- Record that these tests fail against the current implementation for the intended reason.

**Implementation — GREEN**

- No user-facing fix in this task. Add narrowly scoped characterization fixtures and helpers only.

**Acceptance criteria**

- [ ] RED output proves the report uses plain `[type:ID]` text.
- [ ] RED output proves the dashboard renders crumb IDs as non-interactive text.
- [ ] The fixture contains no copied/fabricated evidence; expected values come from controlled test
  data or a stable golden fixture.
- [ ] Existing tests remain green apart from the new expected RED tests on the feature branch.

**Dependencies:** none.

## Task EA0.2 — Record the architecture and controlled-output decision

**GitHub issue title:** `EA0.2: Approve offline Evidence Explorer architecture and candidate-output policy`

**ELI5:** Agree on which house we are building and where the temporary construction copy lives
before anyone pours concrete.

**Tests first — RED**

- Add a governance test that rejects a Streamlit/app-server entry point while ADR-0007 remains
  active.
- Add a release-policy test that refuses to overwrite an approved production report/dashboard
  unless a candidate has passed the required human gate.

**Implementation — GREEN**

- Record an owner-approved ADR or ADR addendum defining:
  - enhancement of the generated offline dashboard, not restoration of the retired sieving GUI;
  - read-only evidence behavior;
  - candidate artifact directory and promotion rules;
  - whether the production report keeps its canonical name after promotion; and
  - future live-service work as a separate decision.

**Acceptance criteria**

- [ ] Owner decision has an immutable reference.
- [ ] Existing approved artifact bytes remain unchanged during development.
- [ ] The decision explicitly states whether a future local web service would supersede ADR-0007.
- [ ] Governance tests pass.

**Dependencies:** EA0.1.

## Task EA0.3 — Define the evidence bundle schema

**GitHub issue title:** `EA0.3: Specify a versioned evidence-bundle contract`

**ELI5:** Define the labeled boxes used to carry evidence from the database to the browser, so
nothing gets lost or mixed up.

**Tests first — RED**

- Add schema tests for missing/extra fields, invalid IDs, wrong types, duplicate quotes, broken
  chunk links, and unsupported schema versions.
- Add a test requiring explicit package hash, database/source lineage, run ID, supplier, framework,
  generation timestamp/date policy, and deterministic record ordering.
- Add a test proving multiple quotes for one crumb are preserved in source order.

**Implementation — GREEN**

- Create a machine-readable schema containing:
  - bundle metadata and lineage;
  - entity indexes for crumbs, documents, gaps, findings, and actions;
  - quotes and source locators;
  - chunks and optional adjacent-chunk summaries;
  - link method/confidence; and
  - canonical viewer target for each reference.

**Acceptance criteria**

- [ ] Schema rejects orphan crumb, quote, chunk, document, and evaluation references.
- [ ] Schema supports Croatian/Slovenian/English Unicode without escaping away the readable text.
- [ ] Schema version is explicit and validated.
- [ ] Ordering rules make equivalent inputs byte-identical.

**Dependencies:** EA0.2.

## Task EA0.4 — Define navigation, safety, and accessibility contracts

**GitHub issue title:** `EA0.4: Specify deep-link, file-safety, and accessible-viewer behavior`

**ELI5:** Decide exactly what every button does, including what happens when something is missing,
before drawing the screen.

**Tests first — RED**

- Parameterized tests for canonical fragments such as `#evidence/crumb/<ID>` and
  `#evidence/document/<ID>`.
- Tests for malformed/unknown IDs, URI encoding, browser back/forward navigation, keyboard access,
  focus placement, and no-script fallback text.
- Security tests rejecting external URLs, executable evidence text, path traversal, and HTML/script
  injection from source data.

**Implementation — GREEN**

- Document the target grammar, error presentation, keyboard behavior, focus rules, escaping rules,
  and print behavior used by later tasks.

**Acceptance criteria**

- [ ] All supported reference types have one unambiguous target grammar.
- [ ] Unknown targets produce a visible “evidence unavailable” state, never a blank panel.
- [ ] Evidence is inserted using safe text APIs, not interpreted as HTML.
- [ ] Minimum accessibility behavior is testable without human guesswork.

**Dependencies:** EA0.3.

## Task EA0.5 — Create and verify the isolated Conda environment

**GitHub issue title:** `EA0.5: Provision C:\xPY\vEnv\WikiEnconet with Conda`

**Status:** Completed by explicit owner instruction on 2026-09-03; dependency installation remains
EA0.6.

**ELI5:** Give this project its own clean toolbox so its tools cannot be confused with tools from
another project.

**Tests first — RED/preflight**

- Verify the exact target path before creation; the target was confirmed absent.
- Confirm the project supports the selected interpreter (`sieving/README.md` requires Python 3.10+;
  the production run was already validated on Python 3.13).
- Define direct executable checks so success does not depend on whichever environment happens to be
  activated in the shell.

**Implementation — GREEN**

- Create the environment with:

  ```powershell
  conda create --prefix C:\xPY\vEnv\WikiEnconet python=3.13 pip -y
  ```

- Verify using the environment's own executables rather than global `python` or `pip`.

**Acceptance criteria**

- [x] Exact directory `C:\xPY\vEnv\WikiEnconet` exists and contains `conda-meta/`.
- [x] `C:\xPY\vEnv\WikiEnconet\python.exe --version` returns Python 3.13.15 with exit code 0.
- [x] `C:\xPY\vEnv\WikiEnconet\python.exe -m pip --version` returns pip 26.2.1 from the same
  environment with exit code 0.
- [x] No existing environment or directory was overwritten.
- [x] Activation command is documented as `conda activate C:\xPY\vEnv\WikiEnconet`.

**Dependencies:** none; explicitly authorized infrastructure prerequisite.

## Task EA0.6 — Declare, install, and verify project dependencies in Conda

**GitHub issue title:** `EA0.6: Make the WikiEnconet Conda environment reproducible and project-ready`

**Status:** Completed by Codex on 2026-09-03; independent Claude review is deferred under ADR-0023.

**ELI5:** The empty toolbox now exists; install the labeled tools and prove every command takes its
tools from that box.

**Tests first — RED**

- Recorded RED command:

  ```powershell
  $env:PYTHONUTF8='1'
  C:\xPY\vEnv\WikiEnconet\python.exe sieving\verify_install.py
  ```

- Recorded result: exit code 1; `pandas`, `openpyxl`, `typer`, and `rich` missing; project imports
  correctly skipped; required repository structure passed.
- Add environment-isolation tests that print `sys.executable`, `sys.prefix`, dependency versions,
  and ensure none resolve from base/user site-packages.
- Add a reproducibility test that compares the installed core dependency versions with the
  repository-controlled specification.

**Implementation — GREEN**

- Add a repository-controlled Conda environment specification with Python 3.13 and pip.
- Install the pinned dependencies declared by `sieving/requirements.txt` into the exact prefix.
- Document both activation and activation-free execution:

  ```powershell
  conda activate C:\xPY\vEnv\WikiEnconet
  conda run --prefix C:\xPY\vEnv\WikiEnconet python <command>
  ```

- Add browser-test dependencies only later under EA5.1 after the owner approves the dependency and
  runtime; do not silently add them in this task.

**Acceptance criteria**

- [x] Environment specification is committed and recreates a clean compatible environment.
- [x] `verify_install.py` passes from `C:\xPY\vEnv\WikiEnconet`.
- [x] Complete existing pytest suite passes from the new environment.
- [x] Aggregate validation passes from the new environment.
- [x] `sys.executable` and `sys.prefix` resolve inside `C:\xPY\vEnv\WikiEnconet`.
- [x] Required package versions match controlled declarations exactly.
- [x] No project dependency was installed into Conda `base` or the user site directory; the
  installation command targeted the exact environment interpreter and the isolation test proves
  all declared modules resolve beneath its prefix.

**Dependencies:** EA0.5; implementation begins after the plan/architecture gate is accepted.

---

# EPIC EA1 — Read-only evidence resolver and deterministic bundle

**GitHub issue title:** `EA1: Build the database-to-browser evidence projection`

**Goal:** Produce one trustworthy, portable bundle from the approved package and SQLite database.

**Epic acceptance criteria**

- [ ] Every evaluation reference resolves or generation fails closed.
- [ ] Production bundle generation is deterministic.
- [ ] SQLite is opened read-only and queried with parameters.
- [ ] Bundle validation is independent of the renderer.

## Task EA1.1 — Implement a read-only crumb resolver

**GitHub issue title:** `EA1.1: Resolve crumb → quotes → chunk → document`

**ELI5:** Given a crumb number, retrieve the note, every highlighted sentence, and the exact source
chapter it came from.

**Tests first — RED**

- Fixture tests for one quote, multiple quotes, multiple chunk links, Unicode, exact and normalized
  link methods, and confidence values.
- Negative tests for unknown crumb, inactive crumb, missing quote, cross-document link, missing
  chunk, and source-hash mismatch.
- Test that SQL-injection-like IDs are treated as values and return no match.

**Implementation — GREEN**

- Add a small query/service module using SQLite read-only mode and parameterized SQL.
- Return typed dictionaries/data objects matching the schema rather than renderer-specific HTML.

**Acceptance criteria**

- [ ] Resolver returns the complete production sample correctly, including all three quotes.
- [ ] Resolver never writes to the database.
- [ ] Cross-document or hash-inconsistent traceability fails closed.
- [ ] Focused unit suite passes.

**Dependencies:** EA0.3–EA0.4, EA0.6.

## Task EA1.2 — Resolve documents, gaps, findings, actions, and package references

**GitHub issue title:** `EA1.2: Complete the report-reference entity graph`

**ELI5:** Some labels point to evidence, while others point to a document, gap, finding, or action;
make every label lead somewhere useful.

**Tests first — RED**

- Add one positive and one missing-reference test per supported type:
  `crumb`, `document`, `gap`, `finding`, `action`, and `source:package`.
- Test forward and reverse lineage, for example finding → gap → evaluation → evidence crumbs.
- Test that an action primary link resolves the action entity while its separate finding citation
  continues to resolve the related finding/evidence lineage.
- Test that a gap's self-citation opens exactly one gap detail target containing description,
  evaluation/criterion, `missing_evidence_ref`, optional evidence crumb, and related
  findings/actions without recursively resolving the same gap again.
- Test that a reference from another evaluation run is rejected unless explicitly included.

**Implementation — GREEN**

- Build a normalized entity registry for the selected run and expose canonical targets. Model an
  action's primary entity link separately from its related finding citation. Model a gap self-link
  as navigation to one non-recursive gap detail entity, not as direct source evidence.

**Acceptance criteria**

- [ ] Every reference type currently emitted by the report has a defined viewer presentation.
- [ ] Newly linked action IDs and their existing finding citations remain distinct and both work.
- [ ] A gap self-link renders missing-evidence and relationship context once, with no recursive UI
  expansion or misleading source-evidence claim.
- [ ] Lineage never silently crosses run boundaries.
- [ ] Circular or duplicate relationships are handled deterministically.

**Dependencies:** EA1.1.

## Task EA1.3 — Add adjacent-chunk context

**GitHub issue title:** `EA1.3: Provide bounded previous/next source context`

**ELI5:** Let the Owner look one page before or after the quoted chapter without dumping the whole
filing cabinet onto the screen.

**Tests first — RED**

- Tests for first, middle, and last chunk in a document.
- Tests that adjacent chunks remain in the same document and preserve stable database ordering.
- Test configurable bounds so the bundle cannot grow without limit.

**Implementation — GREEN**

- Add previous/next chunk identifiers and bounded context to the projection.

**Acceptance criteria**

- [ ] No adjacent navigation crosses a document boundary.
- [ ] First/last chunk behavior is explicit and visible.
- [ ] Context limits are documented and validated.

**Dependencies:** EA1.1.

## Task EA1.4 — Build and validate the evidence bundle CLI

**GitHub issue title:** `EA1.4: Generate a deterministic run-scoped evidence bundle`

**ELI5:** Package all the required evidence into one sealed, labeled box the browser can carry.

**Tests first — RED**

- Golden-file test for canonical JSON bytes.
- Repeat-generation test proving identical output hashes.
- Failure tests for missing package, package/database mismatch, unresolved evidence, invalid output
  path, and attempted overwrite of an approved artifact.
- Production coverage test expecting all 62 production evaluation crumbs to resolve.

**Implementation — GREEN**

- Add a CLI taking explicit package, database, run ID, and candidate output path.
- Validate before writing and use atomic publication for the candidate file.

**Acceptance criteria**

- [ ] Two builds from unchanged inputs are byte-identical.
- [ ] Bundle includes only evidence reachable from the selected run, unless an explicitly approved
  context option says otherwise.
- [ ] Generation fails before publication if one reference is unresolved.
- [ ] Production bundle reports 62/62 evaluation crumbs resolved.

**Dependencies:** EA1.1–EA1.3.

---

# EPIC EA2 — Offline Evidence Explorer

**GitHub issue title:** `EA2: Turn the offline dashboard into a clickable Evidence Explorer`

**Goal:** Let the Owner navigate evidence in a normal browser without running a server.

**Epic acceptance criteria**

- [ ] Clicking any production crumb opens the correct evidence.
- [ ] Deep links work when the HTML is opened from disk (`file://`).
- [ ] Source text is safe, readable, keyboard-accessible, and printable.
- [ ] Existing dashboard filtering/sorting behavior remains intact.

## Task EA2.1 — Integrate the validated evidence payload

**GitHub issue title:** `EA2.1: Embed validated evidence data in the self-contained dashboard`

**ELI5:** Put the sealed evidence box inside the dashboard so it works even with no internet.

**Tests first — RED**

- Renderer test requiring one safely escaped evidence payload and matching bundle hash.
- Tests for `</script>`, HTML tags, control characters, and multilingual source text.
- Test that no external assets or network URLs are introduced.

**Implementation — GREEN**

- Extend the renderer with a safely serialized evidence payload and bundle metadata.

**Acceptance criteria**

- [ ] HTML remains a single self-contained file.
- [ ] Embedded data round-trips without text corruption.
- [ ] Package and bundle hashes are visible in artifact metadata.
- [ ] Existing dashboard validation passes.

**Dependencies:** EA1.4.

## Task EA2.2 — Render clickable evidence controls and detail drawer

**GitHub issue title:** `EA2.2: Open a source-evidence drawer from criterion references`

**ELI5:** Replace each printed file number with a button that opens the correct folder.

**Tests first — RED**

- Browser test: click a crumb under a criterion and assert the correct statement, document, quote,
  heading, chunk, and traceability metadata appear.
- Browser test for multiple quotes and multiple evidence controls on one criterion.
- Tests for close, escape key, focus return, keyboard activation, and unknown target error state.

**Implementation — GREEN**

- Render each reference as a button/link and add a reusable accessible drawer/dialog component.

**Acceptance criteria**

- [ ] Production sample opens the correct chunk and all three quotes.
- [ ] Drawer does not mutate evaluation data.
- [ ] Keyboard-only navigation completes the same workflow as mouse navigation.
- [ ] Existing criterion filter, search, sort, expand, collapse, and print controls still work.

**Dependencies:** EA2.1.

## Task EA2.3 — Highlight quotes and navigate source context

**GitHub issue title:** `EA2.3: Highlight exact quotes and support bounded chunk navigation`

**ELI5:** Open the right chapter and use a yellow marker on the exact words that support the
conclusion.

**Tests first — RED**

- Tests for exact quote highlighting, repeated identical text, overlapping quotes, normalized-link
  quotes, quote not found, and Unicode boundaries.
- Browser tests for previous/next chunk and document-boundary stopping.

**Implementation — GREEN**

- Highlight safely using text nodes/ranges; never inject source text as HTML.
- Clearly distinguish exact from normalized links and show confidence.

**Acceptance criteria**

- [ ] Exact quotes are highlighted without altering displayed source text.
- [ ] Ambiguous/repeated matches are disclosed rather than silently selecting one.
- [ ] A failed highlight still shows the quote, locator, and chunk with a warning.
- [ ] Adjacent navigation stays within the selected document.

**Dependencies:** EA1.3, EA2.2.

## Task EA2.4 — Add owner-friendly citation and print controls

**GitHub issue title:** `EA2.4: Copy and print a complete evidence record`

**ELI5:** Give the Owner a clean evidence card that can be copied into a note or printed for a
meeting.

**Tests first — RED**

- Tests for a deterministic plain-text citation containing IDs, title, heading, locator, quote,
  link method, and hashes.
- Print-layout test ensuring the selected evidence is expanded and controls are hidden.
- Clipboard fallback test for browsers that deny clipboard access on `file://`.

**Implementation — GREEN**

- Add “Copy traceable citation” and “Print evidence” actions with a visible fallback text area.

**Acceptance criteria**

- [ ] Copied citation contains enough stable information to re-query the database.
- [ ] Printed evidence identifies run, package, source, crumb, quote, and chunk.
- [ ] Denied clipboard permission does not lose information.

**Dependencies:** EA2.2–EA2.3.

---

# EPIC EA3 — Real report links and end-to-end navigation

**GitHub issue title:** `EA3: Connect controlled reports to exact browser evidence`

**Goal:** Replace decorative reference labels with validated, portable links.

**Epic acceptance criteria**

- [ ] Every emitted reference is either a valid deep link or explicitly non-navigable by contract.
- [ ] Report-to-viewer links work from the candidate output directory and published directory.
- [ ] Link validation runs before report publication.

## Task EA3.1 — Centralize citation rendering

**GitHub issue title:** `EA3.1: Replace ad-hoc citation strings with a typed citation renderer`

**ELI5:** Use one label maker everywhere so the same evidence never gets two incompatible links.

**Tests first — RED**

- Parameterized tests for each supported entity type, label escaping, URL encoding, relative paths,
  unsupported type, and missing ID.
- Test the intentional new action-ID link independently from the existing action-row finding
  citation.
- Test gap self-links as non-recursive navigation to gap detail rather than source citation.
- Regression test covering criterion rationale, gaps, findings, actions, and evidence matrix.

**Implementation — GREEN**

- Introduce one typed citation renderer shared by all report sections. Add a primary-entity link for
  each action ID while retaining its separate related finding/evidence citation. Render the gap's
  own citation as a single link to the normalized gap detail target.

**Acceptance criteria**

- [ ] No report section constructs `[type:ID]` strings independently.
- [ ] Human-readable stable IDs remain visible in the link text.
- [ ] Action lines expose both action-detail navigation and their existing finding lineage without
  conflating the two.
- [ ] Gap self-links cannot trigger recursive resolution and are labeled/presented as gap context,
  not affirmative evidence.
- [ ] Unsupported references fail report generation rather than becoming dead labels.

**Dependencies:** EA0.4, EA1.2.

## Task EA3.2 — Emit portable deep links

**GitHub issue title:** `EA3.2: Link report citations to Evidence Explorer fragments`

**ELI5:** Put the browser address of the correct drawer behind every report label.

**Tests first — RED**

- Markdown rendering tests for relative links from candidate and published report locations.
- Browser end-to-end test: open report link → open dashboard → display exact evidence.
- Tests for spaces/non-ASCII paths and fragment encoding.

**Implementation — GREEN**

- Emit relative Evidence Explorer links using the canonical target grammar.

**Acceptance criteria**

- [ ] Links do not contain machine-specific absolute paths.
- [ ] Links work after moving the complete output package to another directory/computer.
- [ ] Direct fragment navigation, refresh, and browser back/forward work.
- [ ] English/Croatian report variants target the correct run bundle.

**Dependencies:** EA2.2, EA3.1.

## Task EA3.3 — Add a report-link validator

**GitHub issue title:** `EA3.3: Fail publication on dead or mismatched evidence links`

**ELI5:** Before handing the report to the Owner, automatically click-check every address on the
page.

**Tests first — RED**

- Tests for missing viewer file, unknown target, duplicate target, wrong run, wrong package hash,
  malformed Markdown URL, and stale bundle.
- Positive production test covering every report citation.

**Implementation — GREEN**

- Extend report validation or add a dedicated validator that parses links and resolves them against
  the evidence bundle and viewer metadata.

**Acceptance criteria**

- [ ] Validator reports exact report location and broken target.
- [ ] Zero dead/mismatched links in the production candidate.
- [ ] Validator is deterministic and returns a non-zero exit code on failure.

**Dependencies:** EA1.4, EA3.2.

---

# EPIC EA4 — Registered run catalog and selection

**GitHub issue title:** `EA4: Let the Owner select a registered audit run and its outputs`

**Goal:** Provide clean multi-run navigation without treating arbitrary files as trusted data.

**Epic acceptance criteria**

- [ ] A generated landing page lists only validated, registered run packages.
- [ ] Selecting a run opens its matched report, dashboard, evidence bundle, and metadata.
- [ ] Stale or mismatched artifacts are visibly unavailable, not silently mixed.

## Task EA4.1 — Define and build the review catalog

**GitHub issue title:** `EA4.1: Generate a deterministic catalog of validated review packages`

**ELI5:** Make a trustworthy library index instead of asking the browser to guess which loose files
belong together.

**Tests first — RED**

- Tests for zero, one, and multiple registered runs; missing artifacts; duplicate run IDs; hash
  mismatch; candidate versus approved status; and deterministic ordering.
- Test that unrelated files in `outputs/` are ignored.

**Implementation — GREEN**

- Generate a catalog from controlled run/package/dashboard records and validated artifact metadata.

**Acceptance criteria**

- [ ] Every catalog row has supplier, framework, run ID, status, language, generated date, hashes,
  and artifact links.
- [ ] Catalog cannot advertise an artifact that failed validation.
- [ ] Production run appears exactly once.

**Dependencies:** EA1.4, EA3.3.

## Task EA4.2 — Build the offline run-selection landing page

**GitHub issue title:** `EA4.2: Add a self-contained review workspace landing page`

**ELI5:** Give the Owner one front door with a list of completed audits rather than a folder full of
similarly named files.

**Tests first — RED**

- Browser tests for run filtering, keyboard selection, opening matched artifacts, unavailable-state
  messaging, and operation from `file://`.
- Security test proving the page does not enumerate arbitrary local files.

**Implementation — GREEN**

- Render a static `review_workspace.html` (final name subject to EA0.2) from the validated catalog.

**Acceptance criteria**

- [ ] Owner can select the Enconet Appendix B run and open its evidence explorer in two actions or
  fewer.
- [ ] Page works offline without a server.
- [ ] Candidate and approved artifacts are visually distinct.
- [ ] No local directory-scanning permission is requested.

**Dependencies:** EA4.1.

## Task EA4.3 — Define package portability

**GitHub issue title:** `EA4.3: Verify review package works after controlled relocation`

**ELI5:** Prove the whole review folder still works when copied to the Owner’s computer.

**Tests first — RED**

- Copy the candidate package to a temporary directory and run link/hash/browser smoke tests there.
- Test missing-file and renamed-file failures.

**Implementation — GREEN**

- Add a deterministic package manifest and portability validator.

**Acceptance criteria**

- [ ] Complete package passes after relocation to a path containing spaces and non-ASCII text.
- [ ] No link depends on repository root, drive letter, or developer username.
- [ ] Missing/changed files are detected by manifest validation.

**Dependencies:** EA3.3, EA4.2.

---

# EPIC EA5 — Quality gates, browser verification, and aggregate validation

**GitHub issue title:** `EA5: Make evidence navigation a release-blocking quality contract`

**Goal:** Ensure the feature remains trustworthy after future reports, schemas, and browsers change.

**Epic acceptance criteria**

- [ ] Unit, integration, browser, security, portability, and production checks pass.
- [ ] Aggregate validation fails when evidence navigation is broken.
- [ ] Performance and artifact-size limits are explicit.

## Task EA5.1 — Establish the browser test harness

**GitHub issue title:** `EA5.1: Add reproducible headless browser tests for offline artifacts`

**ELI5:** Use a robot browser to press the same buttons the Owner will press.

**Tests first — RED**

- First browser test opens the current dashboard, looks for an interactive crumb, and fails.
- Add environment preflight tests that report a missing browser/runtime as a failure, not a skip.

**Implementation — GREEN**

- Add the smallest approved browser-test dependency and pin its version/runtime.
- Provide one documented command usable locally and in CI.

**Acceptance criteria**

- [ ] Harness tests `file://` behavior, not only an HTTP test server.
- [ ] Browser/runtime absence produces an actionable non-zero failure.
- [ ] Test artifacts (screenshot/DOM/log) are retained on failure.
- [ ] Dependency choice is owner-approved before installation.

**Dependencies:** EA0.2; may begin before EA2 but must be ready for EA2.2.

## Task EA5.2 — Integrate evidence checks into aggregate validation

**GitHub issue title:** `EA5.2: Add evidence bundle, link, browser, and portability validators`

**ELI5:** Add the new door and keys to the building’s final safety inspection.

**Tests first — RED**

- Aggregate-runner tests proving each new validator is phase-aware, ordered, summarized, and
  failure-propagating.
- Test that a broken report link blocks release even when evaluation scoring is valid.

**Implementation — GREEN**

- Register focused validators in the canonical aggregate runner at the appropriate lifecycle phase.

**Acceptance criteria**

- [ ] Aggregate output preserves exact command, integer exit code, counts, and artifact paths.
- [ ] Validation does not rewrite controlled outputs.
- [ ] Existing 14 checks remain green and new checks are additive.
- [ ] One deliberately broken fixture proves fail-closed behavior.

**Dependencies:** EA3.3, EA4.3, EA5.1.

## Task EA5.3 — Enforce security, encoding, size, and performance budgets

**GitHub issue title:** `EA5.3: Bound and harden the offline evidence package`

**ELI5:** Make sure the evidence box is safe to open and not so large that the Owner’s browser
freezes.

**Tests first — RED**

- Injection corpus covering HTML/script payloads, Markdown-like text, bidi/control characters, and
  malicious-looking file names.
- Tests for maximum bundle/artifact size, initial render time, evidence-open latency, and search
  responsiveness on the production dataset.
- Encoding round-trip tests for Croatian and Slovenian diacritics.

**Implementation — GREEN**

- Add safe rendering, bounded projections, documented budgets, and deterministic measurement.

**Acceptance criteria**

- [ ] No source text executes as markup or script.
- [ ] No external request occurs during browser testing.
- [ ] Owner-approved size and response budgets pass on the production package.
- [ ] All multilingual fixture strings round-trip exactly.

**Dependencies:** EA2.3, EA4.3.

## Task EA5.4 — Conduct Owner usability acceptance

**GitHub issue title:** `EA5.4: Owner UAT for report-to-source evidence navigation`

**ELI5:** Let the real user try the exact job before declaring the feature finished.

**Tests first — RED/UAT script**

- Prepare a fixed acceptance script:
  1. open the report;
  2. click one crumb with multiple quotes;
  3. confirm statement, quote, chapter, and document identity;
  4. navigate adjacent context;
  5. copy a traceable citation;
  6. print/save the evidence card;
  7. return to the report and open another criterion; and
  8. select the run from the landing page.

**Implementation — GREEN**

- Correct only observed usability defects through new failing tests; do not patch around them
  manually in generated HTML.

**Acceptance criteria**

- [ ] Owner completes the script without repository knowledge or command-line use.
- [ ] Every observed defect has a regression test.
- [ ] Owner records approve/reject with date and decision reference.

**Dependencies:** EA2–EA5.3.

---

# EPIC EA6 — Controlled production release and documentation

**GitHub issue title:** `EA6: Publish the reviewed Evidence Explorer without rewriting history`

**Goal:** Promote the candidate through existing audit controls and leave a reproducible operator
record.

**Epic acceptance criteria**

- [ ] Candidate artifacts pass all automated checks and independent review.
- [ ] Owner approves the changed report/dashboard presentation.
- [ ] Promotion is atomic, recorded, and recoverable.
- [ ] Old approved artifacts remain recoverable by commit/hash.

## Task EA6.1 — Generate production candidates

**GitHub issue title:** `EA6.1: Build candidate report, explorer, bundle, catalog, and package manifest`

**ELI5:** Produce a complete dress rehearsal in a separate folder before replacing anything the
Owner already approved.

**Tests first — RED**

- Production-generation test expecting the exact controlled run, package hash, 18 criteria, and
  62 resolvable evidence crumbs.
- Test proving canonical approved output paths are unchanged before promotion.

**Implementation — GREEN**

- Generate all artifacts into the candidate location selected in EA0.2.

**Acceptance criteria**

- [ ] Candidate contains report, evidence explorer/dashboard, evidence bundle, catalog/landing page,
  and package manifest.
- [ ] Candidate lineage points to the exact production run and source hashes.
- [ ] Existing approved output hashes are recorded before promotion.

**Dependencies:** EA5.2–EA5.3.

## Task EA6.2 — Document operation and recovery

**GitHub issue title:** `EA6.2: Document build, validate, open, transfer, and rollback procedures`

**ELI5:** Write the instruction card so the next person can rebuild and open the package without
asking its inventor.

**Tests first — RED**

- Documentation command tests for every executable command.
- Clean-environment rehearsal following only the documented steps.

**Implementation — GREEN**

- Document prerequisites, commands, artifact meanings, failure states, controlled promotion, and
  recovery from the previous approved commit/hash.
- Route a closeout synchronization request to Claude Code for any Claude-owned guidance that still
  names a different/default interpreter. Codex must not edit `CLAUDE.md` or `.claude/`; the plan
  records synchronization as pending until Claude confirms its own update or the owner explicitly
  accepts a documented exception.

**Acceptance criteria**

- [ ] A reviewer can reproduce the candidate from documented commands.
- [ ] Documentation does not advertise Streamlit or an unapproved server.
- [ ] Recovery procedure identifies exact immutable artifacts/commits.
- [ ] Claude-owned interpreter guidance is either synchronized by Claude and confirmed through the
  neutral channel, or an owner-accepted exception is recorded; Codex does not modify it.

**Dependencies:** EA6.1.

## Task EA6.3 — Independent implementation and evidence review

**GitHub issue title:** `EA6.3: Claude independently review and reproduce the complete release`

**ELI5:** Have a second inspector check the wiring and test the buttons without trusting the first
builder’s notes.

**Tests first — reviewer protocol**

- Reviewer receives exact files, commands, expected counts, risk list, and candidate paths.
- Reviewer independently checks code, tests, lineage, generated artifacts, link coverage, browser
  behavior, security fixtures, and controlled-output policy.

**Implementation — GREEN**

- Codex addresses each finding through a new RED test and correction; Claude re-reviews material
  changes.

**Acceptance criteria**

- [ ] Reviewer reproduces aggregate and browser results.
- [ ] Reviewer reports approve or actionable findings in an immutable coordination record.
- [ ] No unresolved high/medium finding remains.

**Dependencies:** EA6.1–EA6.2.

## Task EA6.4 — Human gate, promotion, and closeout

**GitHub issue title:** `EA6.4: Approve and atomically promote the Evidence Explorer release`

**ELI5:** Only after all inspections pass does the Owner authorize moving the candidate onto the
official shelf.

**Tests first — RED**

- Promotion tests for missing owner approval, failed validator, hash drift, partial copy, and stale
  candidate.
- Post-promotion test of every report link from the final published location.

**Implementation — GREEN**

- Route promotion through the applicable audit gate/dispatcher, update manifests and generated wiki
  copies, validate, close coordination, and publish a truthful handoff.

**Acceptance criteria**

- [ ] Explicit human approval reference exists before promotion.
- [ ] Promotion either completes fully or leaves canonical outputs unchanged.
- [ ] Final aggregate, browser, portability, and link-resolution checks pass.
- [ ] Final report and dashboard hashes are recorded.
- [ ] Coordination has zero unresolved review messages/claims at closeout.
- [ ] Claude confirms its interpreter guidance is synchronized, or the owner records an explicit
  accepted exception before “both sides synchronized” is claimed.

**Dependencies:** EA5.4, EA6.3.

---

# EPIC EA7 — Optional live local review service (deferred)

**GitHub issue title:** `EA7: Decide whether a live local review service is justified`

**Status:** Deferred; explicitly outside the offline Evidence Explorer MVP.

**Goal:** Evaluate Streamlit or another local server only if evidence from Owner use shows the static
package cannot meet a defined need.

**Epic acceptance criteria**

- [ ] No implementation begins without a documented limitation of the offline release.
- [ ] Owner makes an explicit superseding/qualifying decision for ADR-0007.
- [ ] Any live service remains read-only unless separately authorized.

## Task EA7.1 — Measure whether a server is necessary

**GitHub issue title:** `EA7.1: Gather unmet-use-case evidence after offline UAT`

**ELI5:** Do not buy and maintain a power tool until the hand tool has actually failed at a real job.

**Tests first — evaluation criteria**

- Define server-only candidate needs: ad-hoc database queries, very large bundle streaming,
  cross-run comparison, controlled export construction, or authenticated multi-user access.
- Compare each need against static alternatives and operational cost.

**Acceptance criteria**

- [ ] Decision record identifies concrete unmet workflows, users, data volume, and risk.
- [ ] “A GUI might be useful” alone is insufficient authorization.
- [ ] Owner chooses reject, defer, prototype, or implement.

**Dependencies:** EA5.4 or later production feedback.

## Task EA7.2 — Supersede ADR-0007 before any live-service prototype

**GitHub issue title:** `EA7.2: Define governance and boundaries for an approved live review service`

**ELI5:** Change the project’s rulebook before rebuilding something the rulebook explicitly retired.

**Tests first — RED**

- Governance test continues rejecting Streamlit/server entry points until the superseding ADR is
  accepted.
- If approved, add tests for localhost-only binding, read-only database access, explicit package
  selection, path confinement, and no uncontrolled writes.

**Implementation — GREEN**

- Record the owner decision, select technology based on requirements, and create a separate TDD
  implementation plan. Do not reuse the retired upstream GUI by default.

**Acceptance criteria**

- [ ] Superseding ADR defines scope, security, lifecycle, ownership, and relationship to the offline
  package.
- [ ] Technology selection follows requirements rather than preference.
- [ ] New work has its own claims, tests, gates, and reviewer.

**Dependencies:** EA7.1 and explicit owner authorization.

---

## 5. Cross-epic Definition of Done

The feature is complete only when all of the following are true:

- [ ] Owner can click a production report citation and see exact source evidence.
- [ ] All 62 production evaluation crumbs resolve through quote, chunk, and document.
- [ ] All other emitted reference types have working, validated targets.
- [ ] Evidence package works offline and after controlled relocation.
- [ ] No source text can execute as HTML/script.
- [ ] Browser keyboard, focus, error, print, and clipboard-fallback behavior passes.
- [ ] Existing evaluation values, approvals, findings, actions, and source bytes are unchanged.
- [ ] All build, test, validation, and generation commands run from the verified
  `C:\xPY\vEnv\WikiEnconet` Conda environment.
- [ ] Existing approved artifacts are not overwritten before the human gate.
- [ ] Aggregate validation and independent Claude review pass.
- [ ] Owner accepts the final user workflow.
- [ ] Codex-side and Claude-side interpreter guidance is confirmed consistent, or the owner accepts
  and records the remaining difference.
- [ ] Promotion, hashes, manifests, coordination resolution, and handoff are recorded.

## 6. Initial GitHub issue backlog

| ID | Issue | Milestone | Depends on | Status |
|---|---|---|---|---|
| EA0.1 | Characterize broken navigation | M0 | — | [ ] |
| EA0.2 | Architecture/output decision | M0 | EA0.1 | [ ] |
| EA0.3 | Evidence bundle schema | M0 | EA0.2 | [ ] |
| EA0.4 | Navigation/safety/accessibility contract | M0 | EA0.3 | [ ] |
| EA0.5 | Create isolated Conda environment | M0 | — | [x] |
| EA0.6 | Install/verify controlled dependencies | M0 | EA0.5 | [x] |
| EA1.1 | Read-only crumb resolver | M1 | EA0.3–EA0.4, EA0.6 | [ ] |
| EA1.2 | Complete reference entity graph | M1 | EA1.1 | [ ] |
| EA1.3 | Adjacent chunk context | M1 | EA1.1 | [ ] |
| EA1.4 | Evidence bundle CLI | M1 | EA1.1–EA1.3 | [ ] |
| EA2.1 | Embed validated payload | M2 | EA1.4 | [ ] |
| EA2.2 | Clickable evidence drawer | M2 | EA2.1, EA5.1 | [ ] |
| EA2.3 | Quote highlight/context navigation | M2 | EA1.3, EA2.2 | [ ] |
| EA2.4 | Copy/print evidence record | M2 | EA2.2–EA2.3 | [ ] |
| EA3.1 | Typed citation renderer | M2 | EA0.4, EA1.2 | [ ] |
| EA3.2 | Portable report deep links | M2 | EA2.2, EA3.1 | [ ] |
| EA3.3 | Report-link validator | M2 | EA1.4, EA3.2 | [ ] |
| EA4.1 | Validated review catalog | M3 | EA1.4, EA3.3 | [ ] |
| EA4.2 | Offline run-selection page | M3 | EA4.1 | [ ] |
| EA4.3 | Portable package manifest | M3 | EA3.3, EA4.2 | [ ] |
| EA5.1 | Headless browser harness | M2 | EA0.2 | [ ] |
| EA5.2 | Aggregate validation integration | M4 | EA3.3, EA4.3, EA5.1 | [ ] |
| EA5.3 | Security/encoding/performance budgets | M4 | EA2.3, EA4.3 | [ ] |
| EA5.4 | Owner usability acceptance | M4 | EA2–EA5.3 | [ ] |
| EA6.1 | Production candidate generation | M4 | EA5.2–EA5.3 | [ ] |
| EA6.2 | Operator/recovery documentation | M4 | EA6.1 | [ ] |
| EA6.3 | Independent Claude review | M4 | EA6.1–EA6.2 | [ ] |
| EA6.4 | Human gate/promotion/closeout | M4 | EA5.4, EA6.3 | [ ] |
| EA7.1 | Measure need for live service | M5 | EA5.4/feedback | [ ] deferred |
| EA7.2 | Superseding ADR and separate plan | M5 | EA7.1 + owner | [ ] deferred |

## 7. Suggested GitHub labels

- `area:evidence-access`
- `area:reporting`
- `area:dashboard`
- `type:epic`
- `type:test`
- `type:governance`
- `risk:controlled-output`
- `risk:traceability`
- `needs:owner-decision`
- `needs:claude-review`
- `status:blocked`

## 8. First actionable issue

EA0.5 is complete under the Owner's explicit environment-creation instruction, and EA0.6 has a
truthful RED baseline but no project dependencies installed. Start **EA0.1** only after the Owner
accepts this plan as the tracking baseline. EA0.1 is allowed to add tests and fixtures but not to
change production rendering. EA0.2 is the first architecture stop: no Evidence Explorer
implementation proceeds until the Owner confirms the offline architecture, candidate-output
location, browser-test dependency policy, and promotion approach.
