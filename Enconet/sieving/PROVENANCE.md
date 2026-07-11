# Provenance — sieving/ subsystem

- **Vendored from:** https://github.com/nekiee13/opencode-JSON
- **Upstream commit:** 976eace521f872e22dac3a77d5cf5f401f9d7367
- **Vendored on:** 2026-07-04
- **Decision:** The sieving implementation is an integral part of this project.
  It is implemented, maintained, and modified here (one location), interconnected
  with the Project03 wiki system. The upstream repo is the historical origin only;
  this copy evolves independently under this project's git history and change control
  (see Sieving_method_specification_Guide.md and MASTER_DEVELOPMENT_PLAN.md EPIC 5/15/18).

## Local modifications (divergence log)

| Date | Change | Rationale |
|---|---|---|
| 2026-07-04 | Removed standalone Streamlit GUI: `src/json_extractor/adapters/`, `app.py`, tests `test_filter_logic.py` / `test_view_logic.py` / `test_file_discovery.py`; dropped `streamlit` from requirements.txt | Human decision: sieving has no separate GUI — it is operated through project processes (scripts + slash commands) and reviewed through generated reports/wiki + DB/exports. Library core (`pipeline`, `extract`, `query`, `io`, `templates`) untouched. Recoverable from git history (commit b315f05). |
