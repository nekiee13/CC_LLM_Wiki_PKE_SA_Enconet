# Additive requirement-seeding add-on

Version 1.0.0 is a candidate pending Claude review. It adapts the committed
Ekonerg seeder into a project-local, explicitly selected RULE-run tool.
It needs the neutral foundation db_util, project_paths and ID schema already
installed by the framework. Runtime commands do not import a sibling company.

Preview: `python audit_template/bootstrap_requirement_seed.py --target <project>`.
Apply: add `--apply --run-id <unique-copy-id>`; existing matching files are
preserved and conflicting files are refused. The manifest pins LF bytes.

Inside the chosen project, preview the approved baseline with
`python scripts/seed_requirements.py --run-id <approved-active-RULE-run>`.
Add `--apply` only after reviewing that preview. Retry inserts zero rows.
Existing requirement conflicts fail transactionally; nothing is deleted.
Selecting one run prevents later Part 21 or interpretive sources being
silently mixed into a governing baseline. Selection does not itself grant
source approval, applicability or permission to score an audit.

Tests cover read-only preview, text deduplication, idempotent apply, missing
coverage, explicit selection and foreign database refusal. The bootstrap
and normal CLI matrix uses a name with spaces and a non-ASCII name, with
and without a sibling company, preserving owner/sibling sentinel hashes.
