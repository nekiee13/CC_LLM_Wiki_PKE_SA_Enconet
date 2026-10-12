# CU-2 pipeline status

The new layout now passes an isolated documentary audit through report and
dashboard generation. CU-2 is still open. No live files have moved, and v4
is still a development candidate, not an installable release.

## What changed and why

- The keyword sweep now accepts `work/validation/`. Its checks still protect
  sources and the database. Explicit root arguments must name the local supplier.
- Candidate results now go directly into `outputs/RUN-ID/`. Flat outputs, the old
  nested candidate tree, foreign supplier paths and nested artifacts are refused.
  This does not mark a result as published. Source and report-gate checks remain.
- Reset no longer targets the whole `work/` folder. That folder now holds code
  and history, so a blanket reset would damage the framework. Reset targets
  `work/derived/`, `work/validation/` and the existing generated-state locations.
  Its four mutable manifest files are reset to their headers under `work/manifests/`.
- New handoffs go into `coordination/handoffs/`. The publisher and board link
  handling use that home. Old immutable handoffs are not rewritten.
- The relocated benchmark uses the correct parent depth to find local scripts
  and schemas. It does not read a sibling supplier.

The builder records these contract adaptations and payload hashes. It still
checks the pinned v3 payload before creating a fresh candidate. Old releases
remain unchanged. Runtime scripts remain local copies.

## Tests

Command, exit code **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu2/pipeline-tests.xml
```

Result: **64 passed**, no skips. Six pipeline/reset tests join the earlier 58.

Four audit cases use two names, with spaces and non-ASCII letters, each with
and without a sibling supplier. All sources, approvals, crumbs and scores in
these cases are test fixtures. They are not real audit decisions.

Each audit case checks:

- Source registration, extraction and chapter storage.
- Keyword sweep, crumb import, exact quote linking and quality metrics.
- Regulatory requirement seeding and applicability/evaluation writes.
- 18 vendor crumbs, 18 rule crumbs and 36 quote-to-chapter links.
- Findings and actions with test-only manifest approvals.
- Raw-source, chapter, traceability, requirement, evaluation and finding checks.
- Report, evidence bundle, dashboard data and both standalone themes.
- The unchanged five-level scoring behavior, using a synthetic 97.2% result.
- Refusal of a report without its required gate approvals.
- Handoff publication, record validation, pointer resolution and board validation.
- Independent scoring/rendering benchmarks in their relocated home.
- No old working directories or `outputs/candidates/` tree.
- No change to sibling source bytes or modification time.

One audit case also runs the pinned browser smoke harness on both standalone
themes. Both load via `file://`, embed one evidence bundle, expose interactive
crumb controls and make no network requests. These are smoke checks, not a
new exhaustive UX or print/PDF review.

Two reset cases apply a test-only reset, with and without a backup. They check
that incoming files, scripts, benchmark code, reviews, decisions, migration
receipts, archive history and handoffs survive unchanged. The backup case checks
each saved target's byte hash. These apply fixtures use writable generated files;
they do not yet prove deletion of registered read-only raw sources on Windows.
The four audit cases also verify that reset preview changes no files.

The first end-to-end run exposed the old sweep output restriction. Later failures
found test CLI arguments that were not supported, an existing fixture directory,
and two guarded source-adapter mistakes. They were corrected before the combined
suite passed. No skipped check is counted as passed.

The protected-file check from
`Ekonerg/handoffs/2026-10-11T234114Z-cdb6634.md` was rerun with elevated read
access for known restricted folders. Exit code **0**: **1,976 files checked,
zero hash mismatches**. Live scores, source bytes, run identities and gate states
are unchanged. The 97.2% figure above belongs only to test data.

## What remains before live moves

1. Finish aggregate-validator and optional catalog/publication path routing.
2. Check remaining configuration/path users and read-only raw reset behavior.
3. Finish Git/history and empty-folder handling in the move workflow.
4. Review the coherent CU-2 batch before any authorized live move.

This is the same CU-2 task, not a new set of per-file slices. The owner's layout
approval still stands. Claude may review later, as the owner allowed.

Record correction: the prior workspace-published handoff at
`Ekonerg/handoffs/2026-10-11T235947Z-fcc8e15.md` used the publisher's default
`PKE_SA_NQA1/Enconet` label despite being stored in Ekonerg and describing this
workspace clean-up. That immutable record stays unchanged. The next record will
use an explicit Ekonerg project ID.
