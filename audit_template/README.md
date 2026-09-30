# Candidate audit bootstrap components (v1)

The sieving bundle is a company-neutral, source-free part of the audit framework. It copies
the sieving command, its local Python package, two schemas, and an empty active
prompt list into one chosen project. It does **not** copy company documents,
old extraction results, audit decisions, a database, or approval to use a law.
It is a candidate until Claude reviews the EK-1.2 evidence.

Why copy? The owner requires each audit to have its own scripts. The copied
command reads code and data from its own project, not this template or another
company. All 21 copied files are listed by name, byte count, and SHA-256 in
[`sieving/v1/manifest.json`](sieving/v1/manifest.json). Change a file only by
making a reviewed new template version and updating its tests and hashes.

From the workspace root, preview an **existing** new project folder:

```powershell
python -B audit_template/bootstrap_sieving.py --target "C:\path\to\New Audit"
```

After the plan and target are reviewed, apply to that same folder with a new
run ID:

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

The tests use invented documents and two fake company folders. One has a fake
sibling audit; the other has none. They check that copied commands work from
another working folder and that no sibling files change. No live audit is
created by the tests.
