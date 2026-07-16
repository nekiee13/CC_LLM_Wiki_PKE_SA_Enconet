# Sieving playbook

This is the mandatory entry point before running sieving, reviewing crumb quality, or
changing a prompt. The contract remains `Sieving_method_specification_Guide.md`; this
playbook defines the operating sequence.

## File map

- `prompts/appb_rule_v*.md`, `prompts/appb_document_v*.md`: immutable prompt versions.
- `prompts/active.yml`: the unambiguous current prompt per RULE/DOCUMENT side.
- `prompts/CHANGELOG.md`: score, decision, reason, and deposited lesson per version.
- `runs/<RUN-id>/`: per-generation metrics and diffs; never overwrite another RUN-id.
- `../benchmarks/sieving_golden/`: versioned calibration excerpt and expected crumbs.
- `../scripts/sieve_*.py`, `resieve_run.py`, `import_crumbs.py`, `link_crumbs.py`:
  generation, measurement, comparison, scoring, and decision mechanics.

## Version and generation rules

1. Copy the applicable active prompt to the next version; never edit an already-used version.
2. Add its CHANGELOG entry before first use, stating what changed and why.
3. Give each attempt a new RUN-id. A candidate never deletes or modifies prior crumbs.
4. Keep the previous generation active while measuring the candidate.
5. Score every new prompt against the approved golden set. A draft golden set is diagnostic only.
6. Promote, reject, or roll back only with a recorded approved decision reference.
7. Record the decision and its lesson in CHANGELOG and the matching skill before closing the loop.

An unchanged prompt version is allowed only as a diagnostic repeat and produces a warning.
Downstream evaluation reads `active_crumbs` only. Generation changes are refused after downstream
evaluation evidence exists; use an owner-approved recovery procedure instead.

## Tuning loop

1. Read `$sieving-run`; prepare a strictly valid crumb JSON for one controlled document.
2. Run `resieve_run.py`; it creates an inactive candidate, imports it, links quotes, and writes
   metrics plus a diff against the previous active generation.
3. Read `$crumb-quality`; review zero-crumb criteria, completeness, quote verification,
   rejected/failed counts, and changed crumb samples.
4. Read `$sieving-tuning`; score against the human-approved golden set.
5. Obtain the human promotion/rejection decision. Promote only a complete, approved,
   promotion-ready score. Otherwise reject or retain the existing active generation.
6. If a promoted generation proves unsuitable before downstream evaluation, roll back by one
   recorded operation. Never delete either generation.
7. Update CHANGELOG and deposit the lesson in the matching skill.

## CLI reference

Run from `Enconet/`. Substitute real controlled IDs and paths.

- Create the first run: `python scripts/sieve_run.py --run-id RUN-20260716-01 --doc-id DOC-0001 --prompt-version appb_document_v1 --document-side DOCUMENT`
- Validate crumbs: `python scripts/validate_app_b_json.py generated.json --strict`
- Import and generate metrics: `python scripts/import_crumbs.py generated.json --run-id RUN-20260716-01 --strict`
- Link quotes and refresh metrics: `python scripts/link_crumbs.py`
- Create a candidate: `python scripts/resieve_run.py --run-id RUN-20260716-02 --doc-id DOC-0001 --prompt-version appb_document_v2 --document-side DOCUMENT --json-file generated-v2.json`
- Regenerate metrics: `python scripts/sieve_metrics.py --run-id RUN-20260716-02`
- Diff runs: `python scripts/sieve_diff.py RUN-20260716-01 RUN-20260716-02 --output-dir sieving/runs/RUN-20260716-02`
- Score candidate: `python scripts/score_sieving.py --golden benchmarks/sieving_golden/manifest.yml --actual generated-v2.json --output sieving/runs/RUN-20260716-02/golden-score.json`
- Promote: `python scripts/sieve_generation.py promote RUN-20260716-02 --decision-ref SIEVE-PROMPT-v2 --reason "Improved approved golden score" --score sieving/runs/RUN-20260716-02/golden-score.json`
- Reject: `python scripts/sieve_generation.py reject RUN-20260716-02 --decision-ref SIEVE-REJECT-v2 --reason "Spurious criterion assignments"`
- Roll back: `python scripts/sieve_generation.py rollback RUN-20260716-01 --decision-ref SIEVE-ROLLBACK-v1 --reason "Regression found before evaluation"`
- Query crumbs: `python scripts/query_crumbs.py --help`
- Validate traceability: `python scripts/validate_traceability.py --no-record`

## Promotion and rollback checks

- Metrics and diff paths belong to the candidate RUN-id.
- Quote-verification exceptions are separately approved.
- The golden manifest is human-approved in `approvals.csv`; draft scoring cannot promote.
- `promotion_ready: true`, a CHANGELOG entry, and an approved decision reference all exist.
- No evaluation evidence exists for the document.
- After the decision, exactly one active generation remains and aggregate validation passes.

The current `benchmarks/sieving_golden/manifest.yml` is deliberately marked
`pending_human_approval`. It proves mechanics only and is not a calibrated target.
