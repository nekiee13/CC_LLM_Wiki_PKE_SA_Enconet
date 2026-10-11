# Owner decision — cleanup layout confirmed

Decision: `OWNER-LAYOUT-20261012-CLEANUP`.

Owner statement: “owner confirms layot.”

This confirms the proposed layout in `../Clean-up_Plan.md`, following the
CU-1 inventory and compiled-map review. It clears the layout-choice hold.
It does not turn every proposed file move into an approved operation.

## Confirmed homes

- Workspace documentation: `PKE_SA_NQA1_doc/`, with plans in `plans/` and
  reset plans in `reset-plans/`.
- Supplier working records: `work/`, including benchmarks, derived files,
  manifests, decisions, reviews and existing backups.
- Supplier plans: `docs/plans/`.
- Supplier handoff records: `coordination/handoffs/`; `HANDOFF.md` remains
  a small root pointer.
- Supplier results: one `outputs/` tree, with current results under their
  actual `RUN-...` folder. Keep distinct revisions and unassigned history.
- Light and dark dashboards: separate self-contained HTML files, with no
  required theme-selection landing page.
- Test scratch: workspace or supplier `.tmp/`, not loose root `pytest*` folders.
- One shared structure for Enconet, Ekonerg, the six known future suppliers
  and future unknown suppliers, supplied by a tested new release.
- Keep incoming/raw/DB and sieving evidence/runtime in their current homes.
  Agent infrastructure remains in place; each agent owns its own changes.

## Authority that stays separate

Continue CU-2 test-first code and tooling preparation. Before live application,
review the tool's exact targets, read-only preview, collision/hold handling,
rollback and source-preservation checks as the plan requires.

No blanket deletion, reset, source change, scoring change, gate approval,
publication or overwrite permission is added by this layout decision.
Dirty files, Claude-owned moves and redirected/hardlinked paths remain held.
The empty reset scratch folder needs a safe, explicit disposition before
application. Immutable old records keep their bytes and use the move map.

The compiled map remains `proposal-not-applied`, with file approvals pending.
Its ZIP SHA-256 is
`62031b885242f33b228e19cca5cd38f1f1cd06a5f95c10ec62e08844dbb7db87`.
This decision is not a per-row approval or a claim that cleanup has run.
