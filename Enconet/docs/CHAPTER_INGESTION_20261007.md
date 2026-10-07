# Enconet chapter ingestion - 7 October 2026

## Completed

Owner G1 approval is recorded as `G1-ENCONET-20261007-SOURCES`.
The approved source basis, supplier boundary and Croatian report language are
in [SOURCE_BASIS_APPROVED_20261007.md](SOURCE_BASIS_APPROVED_20261007.md).

- All 33 registered sources extracted and stored by chapter/section boundaries.
- 922 database sections: 669 vendor and 253 regulatory.
- Every document reconstructs fully from its ordered sections; offsets match.
- Source hashes and write locks validate; all 36 incoming files are unchanged.
- Phase: chunked. G1 approved; G2-G7 remain pending.
- No new crumbs, evaluations, scores or generation promotions.

Per-document commands, integer exit codes and outputs are preserved in
`out/2026-10-07/fresh-intake/chapter-ingestion-receipt.json`.
`manifests/ingest_runs.csv` records chapter-only results, not completed sieving.
The first source's existing matching extraction was kept rather than rewritten.

## Chapter preservation and warnings

The existing parser uses level-1/2 Markdown boundaries, with numbered-section
fallback. Full chapter text, document ID, source hash and character offsets stay
together. Source text was not edited or cut into arbitrary page-based units.

The normal size guide is 50,000 characters per section. Three supporting ASME
sources contain larger converted sections. They were stored intact using the
existing explicit `--max-chars 250000` setting; this changes the size allowance,
not source text or regulatory status. The warning was not discarded:

| Source | Sections over the normal size guide | Review note |
|---|---|---|
| DOC-0031, ASME Part 2 | 217,302 characters | Converted heading also contains an unusually long text block; locator structure needs review before clause-level use |
| DOC-0032, ASME Part 3 | 85,542 characters | Long supporting section; select narrower exact passages during review |
| DOC-0033, ASME Part 4 | 64,119; 124,001; 239,240; 189,465 characters | Long supporting sections; inspect boundaries before clause-level use |

Those flags do not affect vendor chapter completeness or the mandatory Part 1
source. They do not authorize treating supporting Parts 2-4 as mandatory, or
claim that their converted structure is semantically verified.

## Validation

- `python -m pytest Enconet/tests/test_chunk_pipeline.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/enconet-chapter-regression-20261007-a`: exit 0, five tests passed.
- `python scripts/validate_chunks.py --no-record`, from Enconet: exit 0 after each document; exact per-stage records in the receipt.
- `python scripts/run_all_validations.py --no-record`, from Enconet: exit 0 at chunked; raw sources, chunks, sieving harness and structure passed. Later-phase checks were skipped, not passed.
- Independent whole-document reconstruction: 33 of 33 covered with contiguous offsets and matching registered raw hashes.
- Independent incoming hash comparison: 36 of 36 unchanged.

The harness checks mechanics. Its pass is not a new golden approval or permission
to activate v3. The old prompt selector is still preserved; no prompt was changed.

## Next task

Prepare full keyword/concept recall and Enconet's local v3 golden calibration.
The sweep must honor the already-recorded three non-source exclusions explicitly,
not mistake desktop.ini or the conversion note for QMS evidence. Verify schema
and optional context compatibility before importing new crumbs. Read vendor
chapters for both direct controls and the intent behind each quality requirement.
High recall does not relax verbatim quotes, source links or approval gates.
