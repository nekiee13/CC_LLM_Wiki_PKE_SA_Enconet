# Candidate audit bootstrap components (v1)

The sieving runtime reads a project-local taxonomy named by its contract. The
v1 bundle includes and selects the Appendix B criteria because every planned
company audit asks the same question: does that company's own QA system meet
Appendix B requirements, interpreted using ASME NQA-1? A clean copy may keep
this shared criterion baseline. It does not copy company documents, old
extraction results, audit decisions, a database, or source approval. The owner
must still approve the source set and edition for each audit. This bundle is a
candidate until Claude reviews the EK-1.2 evidence.

Why copy? The owner requires each audit to have its own scripts. The copied
command reads code and data from its own project, not this template or another
company. All 21 copied files are listed by name, byte count, and SHA-256 in
[`sieving/v1/manifest.json`](sieving/v1/manifest.json). Change a file only by
making a reviewed new template version and updating its tests and hashes.

From the workspace root, preview an **existing** new project folder:

```powershell
python -B audit_template/bootstrap_sieving.py --target "C:\path\to\New Audit"
```

Only after the plan and target are reviewed, apply to that same folder with a
new run ID. Copying the shared criteria is not source intake or approval:

```powershell
python -B audit_template/bootstrap_sieving.py --target "C:\path\to\New Audit" --apply --run-id first-run
```

Preview writes nothing. Apply checks all source hashes and target conflicts
before it copies. It refuses changed existing files, links, and reused run IDs.
It writes a per-run journal under `.bootstrap/sieving-v1/`. If a run stops part
way, inspect that journal, then use a **new** run ID: same-hash files are kept,
and only missing files are copied. It never removes or overwrites owner files.
The support bundle is a second versioned component. It copies the local
coordination, handoff, guidance, and skill checks, their handoff schema, and
an empty `incoming/` folder marker. Its manifest is
[`support/v1/manifest.json`](support/v1/manifest.json). It uses the same guarded
copy engine, with a separate journal and lock:

```powershell
python -B audit_template/bootstrap_support.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_support.py --target "C:\path\to\New Audit" --apply --run-id support-first
```

Existing owner documents in a project's `incoming/` folder are never listed
in the template manifest, read, or overwritten by this bootstrap. A file's
presence there is not intake approval. The guidance check still fails until
the owner-approved guidance-pair record exists. These are candidate slices;
a full new-audit bootstrap still needs the remaining Epic 1 tools and gates.

The state bundle copies local database and audit-state scripts plus their
schema and empty source vocabularies. It does **not** create a database or a
project-state record during copy. Its manifest is
[`state/v1/manifest.json`](state/v1/manifest.json). Preview and apply use the
same guarded engine and a separate state journal:

```powershell
python -B audit_template/bootstrap_state.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_state.py --target "C:\path\to\New Audit" --apply --run-id state-first
```

Database initialization is a later, explicit local command. It starts with
zero source, company, criterion, or approval rows. Do not run it against the
live Ekonerg project until the clean-state task reaches its gate.

The dispatch bundle adds the local command registry, phase-aware command
router, and layered preflight runner. It depends on the state bundle's local
path, database, and state helpers. This slice does not include the phase-aware
`run_all_validations.py`; `audit-validate` and `audit-close` fail closed until
that tool is separately transferred and tested. Preview before applying:

```powershell
python -B audit_template/bootstrap_dispatch.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_dispatch.py --target "C:\path\to\New Audit" --apply --run-id dispatch-first
```

The phase-validation bundle adds the local aggregate command used by
`audit-validate` and `audit-close`, plus its local Appendix B JSON and
requirement-coverage checks. Those checks cannot create a missing database or
call another company's sieving library. Other child validators are still
missing: a missing required validator is a failure, not a pass. The aggregate
and requirement checks read an existing database in read-only SQLite mode.
This bundle needs the local state and sieving bundles first. Validation records
require an existing, correctly shaped log. Preview and apply are separate:

```powershell
python -B audit_template/bootstrap_phase_validation.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_phase_validation.py --target "C:\path\to\New Audit" --apply --run-id phase-first
```

Do not run the live aggregate until the project state, child validators, and
owner gates are ready. `--no-record` skips the aggregate manifest row; it is
not a general promise that every child validator is read-only.

The setup-validation bundle installs only the neutral wiki folder and page
filename check, a reviewed folder contract, an empty validation-log header,
six empty wiki directory markers, and a local Git rule that keeps copied
framework text and journals at LF on each checkout. The rule does not cover
incoming source documents. The bundle does not approve any criterion or
source. The optional apply uses its own journal and does not overwrite files:

```powershell
python -B audit_template/bootstrap_setup_validation.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_setup_validation.py --target "C:\path\to\New Audit" --apply --run-id setup-first
```

The structure checker depends on the local state bundle for audit phase names.
It can pass on an empty, correctly shaped wiki; that says nothing about audit
evidence, source approval, or the later validation layers.

The tests use invented documents and two fake company folders. One has a fake
sibling audit; the other has none. They check that copied commands work from
another working folder and that no sibling files change. No live audit is
created by the tests.

The source-validation bundle adds the local raw-source registry helper and
two read-only checks. The checks fail when a database or registered source is
missing. The chunk check also fails when there are no chunks. This copy does
not promote files from `incoming/`, create chunks, or approve any source.
It needs the state bundle's local path helper and ID grammar. Preview first:

```powershell
python -B audit_template/bootstrap_source_validation.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_source_validation.py --target "C:\path\to\New Audit" --apply --run-id source-first
```

The evidence-validation bundle adds local quote-to-chunk and wiki-frontmatter
checks. Its exception ledger contains only a header: it does not grant any
exception or approval. The page schemas define shapes, not real pages. The
traceability check reads SQLite in read-only mode and rejects an empty quote
set. Both checks need the state bundle's local path helper; the frontmatter
check also needs the local taxonomy and vocabulary. Preview before copying:

```powershell
python -B audit_template/bootstrap_evidence_validation.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_evidence_validation.py --target "C:\path\to\New Audit" --apply --run-id evidence-first
```

The schema-validation bundle adds the Appendix B JSON shape, offline dashboard
shape, evaluation package shape, placeholder scoring model, and local contract checker. It
compares source codes to the local sieving contract; an empty list means source
selection is still pending, not approved. Numeric scoring values also stay
unapproved until a local G3 decision. The checker needs the state, sieving,
and evidence-validation contracts already copied. Preview before applying:

```powershell
python -B audit_template/bootstrap_schema_validation.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_schema_validation.py --target "C:\path\to\New Audit" --apply --run-id schema-first
```

The sieving-harness bundle adds a local readiness check, a skill-semantics
contract and checker, a neutral playbook, an empty golden-set placeholder,
and two inactive prompt candidates with a blank local history. It does not
install Codex or Claude skills, activate prompts, create a database, or
approve sieving. The normal checker must fail until those prerequisites are
present. `--allow-pending-claude` is diagnostic only and never grants approval.

```powershell
python -B audit_template/bootstrap_sieving_harness.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_sieving_harness.py --target "C:\path\to\New Audit" --apply --run-id harness-first
```

The Codex sieving-skills bundle installs only three project-local Codex
skills and a local LF rule for their files. It does not create Claude-owned
skills, grant source approval, or make a prompt active. The skill-drift check
can report Claude as pending for diagnostics; full readiness still needs
Claude's separate installation and review.

```powershell
python -B audit_template/bootstrap_codex_sieving_skills.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_codex_sieving_skills.py --target "C:\path\to\New Audit" --apply --run-id codex-skills-first
```

The sieving-score bundle installs a local golden-set scoring command and an
empty approval ledger. Strict scoring writes no score when the golden set is
pending or lacks a matching human approval row. `--allow-draft` writes a
diagnostic result that is never promotion-ready. The score command reads only
paths within its project and never changes an existing score file.

```powershell
python -B audit_template/bootstrap_sieving_score.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_sieving_score.py --target "C:\path\to\New Audit" --apply --run-id score-first
```

The sieving-analysis bundle adds local metrics and generation diffs. Both
read an existing local database in SQLite read-only mode; neither creates a
database or changes a run. They reject foreign paths and existing output
files. The diff keeps repeated crumbs distinct rather than merging them.

```powershell
python -B audit_template/bootstrap_sieving_analysis.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_sieving_analysis.py --target "C:\path\to\New Audit" --apply --run-id analysis-first
```

The crumb-import bundle adds strict, transactional import of one local JSON
file into an existing local sieve run. It does not create a database, read
incoming documents, link quotes, or make metrics. A validation or insert
failure leaves the run unchanged. Quote linking and final metrics are later
stages; this import alone is not evidence verification.

```powershell
python -B audit_template/bootstrap_crumb_import.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_crumb_import.py --target "C:\path\to\New Audit" --apply --run-id import-first
```

The crumb-link bundle adds a preview-first script for one completed run. It
links quotes only to chunks of the same registered document. Existing links
are preserved, and a conflict fails instead of replacing them. An unmatched
quote is printed in JSON and makes apply exit with code 2; links alone are
not human approval. Metrics remain a separate step.

```powershell
python -B audit_template/bootstrap_crumb_link.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_crumb_link.py --target "C:\path\to\New Audit" --apply --run-id link-first
```

The resieve bundle adds a preview-first, measured candidate workflow and its
local run-creation dependency. It
requires a completed active generation, strict local JSON, and a reviewed
local prompt. Apply creates an inactive candidate, imports and links quotes,
then writes metrics and a diff only if every quote links. A later error can
leave that candidate in place; inspect it and use a new run ID rather than
overwriting it. Human promotion remains a separate approval step.

```powershell
python -B audit_template/bootstrap_resieve.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_resieve.py --target "C:\path\to\New Audit" --apply --run-id resieve-first
```

The chunking bundle adds a preview-first local command. It reads only a
registered document's derived text and writes chunks once. It refuses a
second write, missing headings, and chunks outside the chosen size bounds.
Apply records offsets in the local database and a new local JSON artifact;
it does not approve source intake or an audit result.

```powershell
python -B audit_template/bootstrap_chunking.py --target "C:\path\to\New Audit"
python -B audit_template/bootstrap_chunking.py --target "C:\path\to\New Audit" --apply --run-id chunk-first
```
