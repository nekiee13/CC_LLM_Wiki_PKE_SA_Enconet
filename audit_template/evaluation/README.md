# Evaluation bundle (candidate)

This bundle copies five local scripts into a new audit. It contains no company documents, approval rows, judgments, or scores. The installed scripts use only the target project's `scripts/`, `schemas/`, `manifests/`, `raw/`, and `db/` paths.

Before use, install the neutral state, schema-validation, sieving, and approval-ledger bundles. Register an approved governing source and its unchanged raw file. Load the 18 Appendix B criteria from the local taxonomy. The test suite uses invented records; it does not authorize a live audit.

For a real run, the owner must approve the 18-row scope decision (G2). The G2 import stores the *candidate* scoring-model version in the run, but it does not score anything. Before writing any judgment, the owner must approve that same model version (G3), set `calibration_status: approved`, and name the matching `G3-<run-id>` row in `approval_ref`. The row must be signed and dated and its notes must name the version. A changed model version needs a new run; the scripts will not silently rewrite one.

`rule_applicability.py` and `write_evaluation.py` preview by default and need `--apply` to write. Both refuse conflicting retries. `score_evaluation.py` and `validate_evaluation.py` read only; they refuse an incomplete 18-criterion run. A validator PASS is a structure check, not a human audit conclusion or approval. Positive ratings require an active supplier DOCUMENT crumb for the same criterion. There is no automatic rating downgrade: the auditor must record a new human judgment instead.

The copied scripts do not ingest `incoming/`, initialize a live database, create a G2/G3 approval, or select an ASME NQA-1 edition. This bundle remains a candidate until Claude reviews the queued task-level evidence.
