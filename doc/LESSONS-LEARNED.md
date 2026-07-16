# Lessons learned — defects and traps already paid for

- **Scope:** concrete failures observed in this workspace, what they cost, and the rule
  each one produced. Companion to `AFI.md` (open items) and `GOOD-PRACTICES.md`
  (positive patterns).
- **Authority:** ADR-0021 defines the evidence threshold, stable identifiers for new
  entries, active/superseded lifecycle, and transitions from AFIs and to good practices.
- **Owner:** shared (either agent under the coordination protocol).
- **Update trigger:** a defect is diagnosed with evidence, or an AFI item closes and
  its story belongs here.

## The DOC-prompt runtime-block defect (spec guide §8.4)

The captured Transformation prompt — DOC carries a malformed runtime block: a stray
`>` inside the `DOCUMENT_SIDE` enum value and a non-null `SOURCE_RULES` placeholder
where DOCUMENT runs require `null` (verbatim in
`Enconet/Sieving_method_specification_Guide.md` §8.4, sourced from docs/context/31).
Consequence: mislabeled runs and side leakage are possible until Task 5.1 corrects the
prompt and Task 5.6 fixture-tests it. **Lesson:** prompts are code — they need
versioning and fixture tests; this defect class is the origin of the plan's
prompt-versioning requirement (EPIC 18).

## Tools drift history (`sieving/tools/fix_*.py`)

The vendored subsystem repaired pipeline drift post-hoc with mutating scripts whose
root assumptions predate the relocation: `fix_files.py` / `fix_structure.py` compute
wrong roots and would mutate the wrong tree; `check_files.py` validates an obsolete
manifest and prints an old-machine path; `verify_install.py` historically recommended
the wrongly rooted repair script when imports failed (hazard chain, reconciliation
§2.3.3–4). **Lesson:** never run repair/migration scripts before reviewing target
root, dry-run, and backup behavior (now a standing rule in both agents' workspace
guidance); repair-by-script is a symptom that the pipeline lacks a blocking gate.

C4.3 quarantined the complete chain under `Enconet/sieving/tools/_archive/`. The MOR
scripts had repaired taxonomy names and inferred rule-reference join keys; the NQA-1
normalizer also synthesized required fields and placeholder evidence/source values. Those
transformations are historical migration evidence, not safe runtime behavior. Any future
migration must use an explicit root, dry-run, backup/rollback, fixtures, and an approved
migration manifest rather than reactivating the archived scripts.

## Index false-positives and snapshot identity

Two related traps, both observed 2026-07-11 or earlier:

1. **Dead-code heuristics lie through `__init__` re-exports.** Reported dead symbols
   in `sieving/src/json_extractor` were live (`flatten_multiple_files`,
   `export_dataframe`, `discover_json_files`, `QueryEngine`) — reconciliation §2.2.2.
   Rule: reference-check before deletion; never justify deletion by percentage.
2. **Index counts are not stable acceptance criteria.** Section counts changed as
   preparation docs were indexed (reconciliation §2.3.5); and an incremental jdocmunch
   refresh run without the documented root/excludes silently re-roots the profile and
   pollutes it (observed live 2026-07-11 — `sieving/DATA` JSON entered the docs index).
   Rules: acceptance criteria test properties (zero drift, verify_index clean), not
   fixed counts; every refresh re-passes the documented root and ignore patterns
   (`doc/INDEXING.md`).

## Spec-guide false statement (§10.1)

A specification claimed `config.py` obtains canonical criteria/codes through
`AppBTemplate`; the code holds separate tables and imports no template module
(reconciliation §2.3.2). Corrected by C1.4 (v1.2, 2026-07-11), then made true by
C4.4, which implemented the single owner the correction described. **Lesson:** every
specification claim about code behavior must be verified against the code before the
document is promoted to controlled status; "documented" is not "true".

## Hand-written records fail machine contracts

The 2026-07-11 `ff50200` handoff record was written per the skill procedure instead
of published through `make_handoff.py`; it lacks `validation_checks_json` and fails
schema validation — found by the aggregate runner's L5 layer on its first run
(C5.2, 2026-07-12). The record stays immutable; the failure clears when the next
helper-published handoff replaces the pointer. **Lesson:** once a machine contract
and helper exist, prose-procedure output is nonconforming by default — always publish
through the helper, and make the aggregate runner validate the record the pointer
actually names.

## Stale behavior docs survive the code change

C4.1 replaced fail-open filtering, but README/QUICKSTART still taught the removed
`--strict-filter` flag and fail-open semantics until C4.5's docs-vs-reality smoke
test forced the correction (2026-07-12). **Lesson:** behavior changes must grep the
user-facing docs for the old contract; a smoke test that executes every documented
command against the real CLI keeps them honest permanently.

## Guidance staleness is real drift

Within one day of C0.1/C5.3, both guidance trees carried false environment claims
(dependencies "absent" after they were installed; Git "unverified" after the repo was
established). **Lesson:** constraints that describe mutable environment state must
carry their date and verification command, and the drift check must flag one-sided
refreshes (now enforced via `doc/GUIDANCE_PAIRS.json` documented-difference entries
that get deleted once both sides refresh).

## LL-RAW-001 — Direct placement in `raw/` bypasses the provenance boundary

- **Status:** active
- **Date recorded:** 2026-07-16
- **Scope/area:** Enconet raw-source intake and provenance
- **Observation:** A user placed the complete requirements-document set directly in
  `Enconet/raw/`. That action triggered the raw-source rule because existence in
  `raw/` is not acceptance: direct copying bypasses the sole controlled doorway.
- **Evidence:** Owner-reported intake incident; `Enconet/docs/RAW_INTAKE.md` steps 1–4;
  `Enconet/scripts/validate_raw_sources.py` rejects unregistered, writable,
  checksum-mismatched, missing, and DB/manifest-divergent raw files;
  `Enconet/tests/test_raw_intake.py::test_validator_names_tamper_unregistered_and_missing`
  proves the fail-closed behavior. After the incident, `python
  Enconet/scripts/validate_raw_sources.py` returned exit code 0 on 2026-07-16, proving
  the current controlled set is reconciled, not that direct copying is permitted.
- **Consequence:** Direct-to-`raw/` files have no guaranteed human review, allocated
  `DOC-nnnn`, SHA-256 identity, synchronized SQLite/CSV provenance, duplicate check,
  or write lock. Downstream chunks, crumbs, evidence, and reports therefore cannot
  prove which controlled source bytes they used.
- **Reusable rule:** Never populate `raw/` with a file copy, bulk extraction, sync, or
  manual save. Stage each stable, uniquely named, reviewed source in `incoming/`, then
  promote it with `scripts/promote_source.py` and complete extraction and raw-source
  validation. If files were already copied directly, stop downstream processing; do
  not edit, overwrite, or silently register them in place. Inventory and preserve the
  bytes, apply a reviewed correction that returns unregistered inputs to `incoming/`,
  and promote them through the same controlled path.
- **Owner/next action:** All source-intake operators; follow `RAW_INTAKE.md` for every
  source and require `validate_raw_sources.py` to pass before downstream use.
- **Links:** ADR-0021; EPIC3 Tasks 3.1–3.4; `GP-RAW-001`;
  `Enconet/docs/RAW_INTAKE.md`; `Enconet/AGENTS.md` raw-intake guardrail.
