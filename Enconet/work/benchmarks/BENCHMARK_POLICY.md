# Reference benchmark policy

## Scope and authority

This policy governs the supplier-independent EPIC16 fixtures under `benchmarks/`.
They are permanent regression anchors, not live supplier evidence, calibration
approvals, or examples to copy into an audit result. `MASTER_DEVELOPMENT_PLAN.md`
Tasks 16.1–16.4 and ADR-0013 remain authoritative.

## Independent benchmark classes

### Scoring (`scoring/`)

The scoring fixture contains all 18 criteria, every rating, locked per-criterion
scores, classification counts, applicable count, consolidated score, and overall
classification. It tests only the EPIC8 calculator and canonical scoring model. It
must never render a dashboard or be used as dashboard input.

### Dashboard rendering (`dashboard_rendering/`)

The rendering fixture contains a synthetic evaluation package with all 18 criteria
and every rating, plus locked structural and functional expectations. It tests the
EPIC12 data projection, schema validation, offline renderer, consistency validator,
sections, counts, bindings, and JavaScript hooks. It is not a scoring calibration or
scoring regression fixture.

The two distributions intentionally differ. Their values must never be reconciled,
copied, or forced to agree. A test or tool that compares their scores or rating counts
is a policy violation.

## Update and approval procedure

1. Identify exactly one benchmark class and record why its consumer contract changed.
2. Change only that class. Run its focused validator before touching expected output.
3. Review the computed result independently against the governing schema/model.
4. Increment that fixture's `fixture_version` and record approval evidence in the
   change commit or coordination review. Never update expected values merely to make a
   failing implementation pass.
5. Run `python scripts/run_all_validations.py --benchmarks --no-record`, the complete
   Enconet test suite, and the normal phase-aware aggregate validation.
6. Obtain human re-approval before changing the scoring fixture after any
   `scoring_model.yml` version or checksum change. Gate G3 still controls calibration;
   the current placeholder fixture does not approve its numeric model.

Benchmark validation is mandatory from `findings_approved`, before the G5 transition
to `report_ready`, and at every later phase. That also places it before the G6
transition from `report_ready` to `dashboard_ready`. The explicit `--benchmarks` flag
runs both classes earlier without advancing project state.
