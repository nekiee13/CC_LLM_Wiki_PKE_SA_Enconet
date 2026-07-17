# M2 baseline failure set — CC_FIN at `238c207`

Recorded 2026-07-18 from a machine-readable JUnit run of
`PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider
--continue-on-collection-errors` (exit 1) in `C:/xPY/xPrj/CC_FIN` at HEAD
`238c207c73970f3d3c6dc00c2db5932ebeca7be4` (clean worktree before and after; report
written outside the repository). Interpreter: Python 3.13.9 (miniconda), pytest 9.1.1.

Totals: **343 tests — 276 passed, 51 failed, 3 collection errors, 13 skipped.**
Classes: 24 `import-unavailable:torch` (21 failures + 3 collection errors, including 3
subprocess failures whose top-level message is an assertion wrapper while the captured
traceback identifies the missing declared dependency), 11
`import-unavailable:matplotlib`, 19 `assertion`.

## Comparison contract (M2-RR1)

The normative T7.3 comparison unit is the tuple
**`(node_id, outcome, class, normalized_signature)`** — one row per table entry below.
After each support slice, a like-for-like re-run (same interpreter, same flags, report
outside the repository) must satisfy all of:

1. **No new tuple**: every failing/erroring `node_id` in the re-run exists in this
   table.
2. **Surviving tuples match exactly**: for every node still failing/erroring, its
   `outcome`, `class`, and `normalized_signature` equal the recorded values. Any
   mutation — including a changed failure reason on the same node — requires an
   explicit reviewed disposition before the slice may be accepted; silent same-node
   replacement is a stop condition even when counts are unchanged.
3. **Explained disappearance only**: a recorded node may leave the set only with an
   explicit recorded explanation (for example, installing the pinned declared
   dependency), never silently.
4. **All support-specific checks pass**, and date-dependent drift in listed assertion
   nodes is recorded and dispositioned, not averaged away.

## Normalization rule (deterministic; rerun-comparable)

Applied to the concatenation of the JUnit `message` attribute and element text of each
`<failure>`/`<error>`:

1. If the text matches the regex `No module named \W{0,3}<mod>\b` for a declared pinned
   dependency (`torch`, `matplotlib`) — the `\W{0,3}` tolerates quote styles and
   escaped quotes in subprocess-captured tracebacks — the class is
   `import-unavailable:<mod>` and the normalized signature is the canonical string
   `ModuleNotFoundError: No module named '<mod>'`, regardless of the top-level wrapper
   (this is a causal signature, not the literal JUnit first line).
2. Otherwise, if it matches `No module named \W{0,3}([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\b`,
   the class is `import-unavailable:<captured token>` with the analogous canonical
   signature; the captured token grammar is dotted Python-identifier segments and the
   trailing `\b` prevents a prefix match from being classified as an exact module
   name.
3. Otherwise the class is `assertion` and the normalized signature is the JUnit
   `message` attribute's first line, whitespace-collapsed and truncated to 120
   characters.

## Mechanical demonstration of the documented rule (M2-RR3)

The exact patterns above, compiled from this file's own text, classify these four
sample inputs as follows (reproduced by the audit script in the archive message
closing M2-RR3):

| Sample input (abbreviated) | Classified as |
|---|---|
| `ModuleNotFoundError: No module named 'torch'` (normal quotes) | `import-unavailable:torch` |
| `...trainer.py", line 8, in <module>
 import torch
ModuleNotFoundError: No module named \'torch\'` (subprocess-escaped quotes) | `import-unavailable:torch` |
| `ModuleNotFoundError: No module named 'matplotlib'` | `import-unavailable:matplotlib` |
| `AssertionError: assert '2026-03-27' == '2026-03-26'` | `assertion` (rule 3 first-line signature) |

| Node ID | Outcome | Class | Normalized signature |
|---|---|---|---|
| `::tests.test_ann_feature_selection` | error | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `::tests.test_ann_multitask_eval` | error | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `::tests.test_ann_trainer` | error | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_train_cli::test_ann_train_parse_args_defaults_to_all_modes_and_epochs_csv` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_train_cli::test_ann_train_selected_modes_expands_all` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_ann_tune_writes_per_ticker_target_matrix` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_assess_sufficiency_flags_low_magnitude_variance` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_assess_sufficiency_flags_single_class_sgn` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_assess_sufficiency_flags_small_and_unbalanced_sgn` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_baseline_passed_allows_genuine_two_class_sgn` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_baseline_passed_blocks_degenerate_single_class_sgn` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_baseline_passed_magnitude_unchanged_by_oi1` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_baseline_passed_sgn_still_requires_beating_baseline` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_e2e_status_flip_cleared_bar_is_healthy` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_e2e_status_flip_tiny_pool_is_insufficient_data` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_improvement_from_baseline_sgn_clamps_negative_garbage` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_improvement_from_baseline_sgn_delta_is_bounded` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_improvement_from_baseline_sgn_normal_case_unchanged` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_rank_prefers_baseline_improvement_for_sgn` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_rank_prefers_directional_accuracy_for_sgn` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_rank_prefers_rmse_for_magnitude` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_validation_slices_default_fraction_is_fixed_min_fold` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_validation_slices_floor_at_min_fold_for_small_n` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_ann_tune::test_validation_slices_scale_window_with_n` | failure | import-unavailable:torch | `ModuleNotFoundError: No module named 'torch'` |
| `tests.test_app3g_smoke::test_app3g_import_and_startup_smoke` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_badges_panel::test_render_does_not_crash` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_cockpit::test_full_cockpit_renders` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_cockpit::test_meta_panels_render_without_backbone` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_cockpit::test_partial_cockpit_uses_placeholders` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_cone_panel::test_render_and_ann_hook_do_not_crash` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_context_panel::test_render_does_not_crash` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_entrypoints_smoke::test_entrypoints_startup_smoke` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_forest_panel::test_render_does_not_crash` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_heatmap_panel::test_render_does_not_crash` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
| `tests.test_review_streamlit_ann_train_feedback::test_predict_ann_computed_sgn_overrides_uses_suggestion_and_trend` | failure | assertion | `AssertionError: assert '+' == '-'` |
| `tests.test_streamlit_anchored_backfill::test_run_anchored_backfill_returns_error_when_ingest_forecast_missing` | failure | assertion | `AssertionError: assert 'success' == 'error'` |
| `tests.test_streamlit_anchored_backfill::test_run_anchored_backfill_runs_replay_draft_then_ingest_materialize` | failure | assertion | `AssertionError: assert '2025-08-01' == '2025-07-30'` |
| `tests.test_streamlit_pipeline_qa::test_evaluate_pipeline_state_flags_fh3_incomplete_coverage` | failure | assertion | `AssertionError: assert 'QA_FH3_MISSING' == 'QA_FH3_INCOMPLETE'` |
| `tests.test_streamlit_pipeline_qa::test_evaluate_pipeline_state_flags_ingest_missing_when_scores_exist` | failure | assertion | `AssertionError: assert 'QA_FH3_MISSING' == 'QA_VG_INGEST_MISSING'` |
| `tests.test_streamlit_pipeline_qa::test_evaluate_pipeline_state_flags_materialize_missing` | failure | assertion | `AssertionError: assert 'QA_FH3_MISSING' == 'QA_MATERIALIZE_MISSING'` |
| `tests.test_streamlit_pipeline_qa::test_evaluate_pipeline_state_flags_violet_missing` | failure | assertion | `AssertionError: assert 'QA_FH3_MISSING' == 'QA_PARTIAL_SCORES_MISSING'` |
| `tests.test_streamlit_pipeline_qa::test_evaluate_pipeline_state_maps_target_date_from_fh3_asof` | failure | assertion | `AssertionError: assert '2025-08-01' == '2025-07-31'` |
| `tests.test_streamlit_pipeline_qa::test_evaluate_pipeline_state_ok_when_violet_exists` | failure | assertion | `AssertionError: assert 'QA_FH3_MISSING' == 'QA_OK'` |
| `tests.test_streamlit_round_status::test_compute_round_status_uses_fh3_asof_mapping_for_violet_match` | failure | assertion | `AssertionError: assert 'GREEN' == 'BLUE'` |
| `tests.test_streamlit_vg_loader::test_build_ann_t0_p_sgn_rows_active_round_without_plus3_sets_realized_na` | failure | assertion | `AssertionError: assert '+' == 'N/A'` |
| `tests.test_streamlit_vg_loader::test_build_ann_t0_p_sgn_rows_uses_markers_3_days_fallback_when_round_actual_missing` | failure | assertion | `AssertionError: assert '4.3130' == '4.3300'` |
| `tests.test_streamlit_vg_loader::test_build_ann_t0_p_sgn_rows_uses_selected_date_and_round_data` | failure | assertion | `AssertionError: assert '584.9800' == 'N/A'` |
| `tests.test_streamlit_vg_loader::test_materialize_for_selected_date_resolves_from_fh3_when_forecast_missing` | failure | assertion | `AssertionError: assert '2026-03-27' == '2026-03-26'` |
| `tests.test_streamlit_vg_loader::test_pick_anchored_violet_date_uses_file_fallback_when_asof_missing` | failure | assertion | `AssertionError: assert None == '2026-04-15'` |
| `tests.test_streamlit_vg_loader::test_pick_anchored_violet_date_uses_target_when_selected_missing` | failure | assertion | `AssertionError: assert None == '2026-03-02'` |
| `tests.test_streamlit_vg_loader::test_resolve_target_forecast_date_falls_back_to_selected_date` | failure | assertion | `AssertionError: assert '2026-03-27' == '2026-03-24'` |
| `tests.test_streamlit_vg_loader::test_resolve_target_forecast_date_uses_fh3_asof_cutoff` | failure | assertion | `AssertionError: assert '2026-03-27' == '2026-03-26'` |
| `tests.test_streamlit_vg_loader::test_resolve_target_forecast_date_uses_fh3_file_date_when_asof_missing` | failure | assertion | `AssertionError: assert '2026-04-17' == '2026-04-15'` |
| `tests.test_tiles_panel::test_render_does_not_crash` | failure | import-unavailable:matplotlib | `ModuleNotFoundError: No module named 'matplotlib'` |
