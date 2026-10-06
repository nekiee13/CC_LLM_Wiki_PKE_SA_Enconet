# Complete manual text review — candidate results

Date: 2026-10-06. Implementer: Codex. Claude review: pending.

## Result

The replacement manual has now had a full, two-pass text review. The first pass
collects stated controls. The second looks for the same control ideas in other
words, tables, definitions, and addenda. No hit quota was used.

The review produced **279 candidate crumbs**, linked to **259 source ranges**,
across all 18 Appendix B criteria. The old active manual has 18 crumbs.
This is a new candidate, not an update to the live audit or its score.

Read all statements and exact quotes in
[the full candidate](../../sieving/candidates/manual-full-20261006/reviewed/candidate.md).
The [JSON payload](../../sieving/candidates/manual-full-20261006/reviewed/candidate.json)
and [source intake preview](../../sieving/candidates/manual-full-20261006/reviewed/intake-preview.json)
are in the same folder. Use `reviewed/`, not the earlier `prepared/` inspection build.

There are 125 direct-pass items and 154 concept-pass items. Their review labels are:

| Evidence in the text | Items | Meaning |
|---|---:|---|
| Concrete documented controls | 156 | The text states a method, duty, check, or condition. This does not prove that work was done. |
| Supporting controls or definitions | 55 | The text supports the control idea, but has less detail or a narrower scope. |
| Leads and references | 68 | Follow the cited document or check the stated limit. These are not proof of a met requirement. |

These labels describe evidence strength during review. They do not replace the
existing five-point audit scale or create new rating classes.

## Criterion coverage

Counts describe evidence items, not scores. A quote may support more than one
control idea. Such links are not separate source documents or independent proof.

| Criterion | Old active manual | New candidate |
|---|---:|---:|
| I — Organization | 3 | 29 |
| II — Quality assurance program | 6 | 42 |
| III — Design control | 1 | 30 |
| IV — Procurement document control | 0 | 10 |
| V — Instructions, procedures, drawings | 0 | 10 |
| VI — Document control | 2 | 28 |
| VII — Purchased items and services | 1 | 15 |
| VIII — Identification | 0 | 6 |
| IX — Special processes | 0 | 8 |
| X — Inspection | 0 | 15 |
| XI — Test control | 0 | 12 |
| XII — Measuring and test equipment | 0 | 10 |
| XIII — Handling, storage, shipping | 0 | 6 |
| XIV — Inspection, test, operating status | 0 | 4 |
| XV — Nonconforming items | 0 | 10 |
| XVI — Corrective action | 2 | 16 |
| XVII — QA records | 2 | 18 |
| XVIII — Audits | 1 | 10 |
| **Total** | **18** | **279** |

## What was read and preserved

The review covers all 3,180 text lines in 55 recorded review sections. Both pass
notes are stored for each section. This includes the main manual, procedure
lists, the nuclear addendum, and the environment and worker-safety addenda.
Image links are present in the source; their image contents were not assessed.

The review preserves the scope of each statement. An environmental control is
not presented as proof of a nuclear control. A definition, heading, or procedure
title is not presented as a completed work record. Conditional wording stays in
the quote and the summary. Eleven repeated source passages have explicit merge
notes; this is not a count of deleted database crumbs.

The owner's five areas now have evidence:

- **VIII:** work-order and document IDs, preservation, and conditional nuclear
  traceability/marking controls.
- **IX:** the special-process definition, conditional validation, and the RVT,
  RPT, RMT, and RUT procedure lists. Qualification records are not supplied by a list.
- **XI:** customer test programs, acceptance criteria, results, and software
  checks. The statement that Ekonerg does not test its own services is retained.
- **XIII:** protection, storage, packaging, transport, special conditions, checks,
  tools, and trained handlers.
- **XIV:** release records, expired-calibration marks, and conditional nuclear
  status-marking documents.

## Issues retained for assessment

These are source-based review leads, not new final audit findings:

- Chapter 7.1.5 allows a commercial-equipment calibration exception. Its basis
  and safe limits need assessment; the wording does not warrant blanket acceptance.
- The nuclear addendum and Prilog 5 use differing RSP/ROS codes and titles.
  For example, nuclear records point to RSP03 while the list names ROS04 for
  backups. Do not silently replace either reference.
- The Appendix B crosswalk points Test Control to 8.1.4, while the nuclear text
  points to 9.1.4. This looks like a cross-reference error.
- Prilog 4 lists PQ10.2-2 revision 9. The supplied procedure's cover states
  revision 10 and approval on 26.02.2024. The manual is an earlier document;
  this difference needs a document-currency check, not an assumed invalid system.
- The safety-addendum register lists PQ5.3 revision 7; the main register lists
  revision 8. This is a further register-currency lead.
- The owner's questions about concrete, coatings, epoxy/cement, non-metal VT,
  and carbon laminates remain questions. The candidate does not assert that
  Ekonerg performs those activities.

## Source identity and safe next step

The replacement is a fuller extraction of declared revision 5. It is not a
vendor-issued revision 6. Its hash is:

`9492b447c386d174ca6fd7a473999a4999899523ae21570a81626ffadfdeae87`

The old registered source remains unchanged:

`cd2e60b5b67229ac02dbd92d6637780d1e12b0491b11a54d37bc78fdd6d635a0`

The logical DOC-0031 label in the candidate identifies its predecessor. It is
**not permission to import it against the old chapters**. The JSON file passes
the strict crumb schema, but schema validity alone does not make it import-ready.

The preview reads the database without writes. It records all 17 old chapters,
active run RUN-20261003-39, inactive candidate RUN-20261005-76, and the new source
hash. Twenty-two of 24 old quote rows remain exact in the replacement. The two
non-matches are contents-list quotes for leadership and planning, not missing
body controls. None were carried into this candidate by copying old crumbs.

Before import, use a tested source-transition path: retain the old source and
history, create source-specific chapter records, and ensure the old and new
manual are not counted twice. Record the source relation and generation choice.
The owner's prior no-local-original-backup choice remains in force; retain old
records and use transactional writes with a before/after journal. No such write
has run in this task. The preview's next document ID is not a reservation.

## All-file progress and remaining work

The [full keyword pass](FULL_KEYWORD_SWEEP_20261006.md) covers all 31 input files:
24 vendor files and 7 rule/reference files. It found 2,892 vendor passage
locations. Those are search leads, not 2,892 accepted crumbs.

This task completes semantic candidate preparation for the replacement manual.
The other 23 vendor documents still need the same uncapped semantic review of
matched and unmatched text. Existing old generations are not proof that this
new full pass is complete. Keep rule sources separate from vendor evidence.

Continue the existing task, with no new scope or human-rating form:

1. Complete tested source intake and chapter linking for this replacement.
2. Finish the other vendor candidates, strict quote checks, and generation diffs.
3. Apply the existing generation controls, then refresh the evidence matrix and
   established five-point scores. Do not hide scores behind a new human-review gate.

The empty evidence matrix is still open. The UMBRA/Astra trial stays paused until
the manual re-sieve is finished. No dashboard changes were made here.

## Verification

- TDD red: the new assembler tests exited 1 before the assembler existed.
- `python -m pytest Ekonerg/scripts/tests/test_build_reviewed_candidate.py Ekonerg/scripts/tests/test_full_keyword_sweep.py -q -p no:cacheprovider`
  exited 0: 28 tests passed. The successful run used permission to access the
  test temporary directory. Tests cover quote fidelity, coverage, invalid input,
  read-only intake, and two synthetic company names with and without a sibling.
- `python Ekonerg/scripts/build_reviewed_candidate.py --review sieving/candidates/manual-full-20261006 --output sieving/candidates/manual-full-20261006/reviewed`
  exited 0: 279 items. The assembler only builds reviewed annotations; it does
  not pretend to perform semantic judgment or import evidence.
- `python Ekonerg/scripts/validate_app_b_json.py sieving/candidates/manual-full-20261006/reviewed/candidate.json --strict`
  exited 0. An earlier command with an extra `Ekonerg/` path prefix was rejected;
  paths for this validator resolve from the project root.
- An independent read-only Python check exited 0: all 279 quotes match their
  exact source offsets; all 3,180 lines have review coverage; all artifact and
  provenance hashes match; rebuilding the payload and preview matches exactly.
- `python Ekonerg/scripts/run_all_validations.py --no-record` exited 0: eight
  phase-applicable checks passed. Evaluation, reports, dashboard, and related
  later-phase checks were skipped under phase `evidence_reviewed`. They are not
  claimed as passes for new audit results.
- The live database still has SHA-256
  `2aba6d844bb609da85eef77aac2b5155d2bc5ccee02a5059af70c50f5e5b231f`.
  No source, active generation, rating, or chapter row was changed.

Hash-bound output and review-input files have narrowly scoped Git attributes
to preserve their exact bytes on checkout. The earlier inspection bundles are
not the published result.

Publication check: `python Ekonerg/scripts/make_handoff.py --validate handoffs/2026-10-06T180011Z-e9ea413.md`
exited 0; `--check-staleness` exited 0 and reported current. An earlier validation
with the extra `Ekonerg/` prefix exited 1 (file not found); the corrected command
above validates the published record. The handoff remains partial because live
intake and the remaining semantic reviews are unfinished, and no Ekonerg index
is configured. The first Git staging attempt was denied access to `index.lock`;
the approved, scoped retry succeeded.
