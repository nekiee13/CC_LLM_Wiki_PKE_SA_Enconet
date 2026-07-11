# AFI — Areas for improvement

- **Scope:** known limitations and unremediated findings across the workspace, each
  with its evidence source and planned fix. This is the open-defect ledger; resolved
  items move to `LESSONS-LEARNED.md` with their resolution.
- **Owner:** shared (either agent under the coordination protocol); an item is closed
  only against a command result, test, commit, or ADR — never by assertion.
- **Update trigger:** a new confirmed finding, or evidence that closes an existing one.

## Sieving method baseline gaps (spec guide §11, `Enconet/Sieving_method_specification_Guide.md`)

| # | Limitation | Planned fix (master plan) |
|---|---|---|
| 1 | Validation is advisory, not blocking — ERROR-flagged records still flow into exports (fail-open; known defect, not accepted policy) | Task 5.3/5.4 blocking import gate |
| 2 | Unchecked fields: `statement` non-empty, `item_id` uniqueness, `item_type`/`record_side` enums (invalid side silently skips side checks) | Task 1.4 + 5.3 strict schema tier |
| 3 | First-source scalar flattening hides secondary source locations in tabular review | Task 5.4 (`crumb_sources`, `crumb_quotes`) |
| 4 | No chunk linkage — weak source review | EPIC 6 |
| 5 | DOC prompt runtime-block defect (spec guide §8.4) | Task 5.1 + 5.6 |
| 6 | No prompt versioning / run generations | Task 5.2, EPIC 18.2/18.6 |
| 7 | No sieving effectiveness measurement | EPIC 18.3/18.4/18.5 |
| 8 | No multilingual evidence fields | Task 5.5 (ADR-0009) |
| 9 | Criterion XIII name: system canon uses the Oxford comma vs the official CFR heading | Note in `schemas/app_b_taxonomy.yml` (Task 1.1) |

## Unremediated findings (CX/CC reconciliation, `Enconet/docs/CX_CC_RECONCILIATION.md` §2.3)

1. **Spec guide §10.1 false statement** — claims `config.py` obtains canon via
   `AppBTemplate`; the modules hold separate tables. Correction is Task C1.4
   (`Enconet/docs/ALIGNMENT_PLAN.md`).
2. **Verifier + repair scripts form a hazard chain** — missing dependencies cascade
   into structure errors and the verifier recommends a wrongly rooted mutating script.
   Guardrail in force: never run `sieving/tools/fix_files.py` / `fix_structure.py`
   (`Enconet/CLAUDE.md`, `Enconet/AGENTS.md`).
3. **`check_files.py` validates an obsolete manifest** — expects removed GUI/example
   files; prints an old-machine path.
4. **Index counts need snapshot identity** — controlled criteria must test properties
   (zero drift), not fixed corpus counts.
5. **Dead-code percentages are materially false-positive** — see
   `LESSONS-LEARNED.md`; no deletion may rely on the reported percentage alone.

## Workspace / environment

- **DATA external backup location undesignated** — `Enconet/sieving/DATA` is untracked
  (ADR-0002) and manifest-verified (`Enconet/sieving/DATA_MANIFEST.json`), but the
  owner deferred choosing an external backup target (C0.2, 2026-07-11). Stays flagged.
- **Shared interpreter, no project venv** — dependencies were installed into the
  miniconda base env (C5.3, see `AS-IS.md`); a dedicated `.venv` remains an open
  owner decision.
- **pandas 3.0.3 is a major version ahead** of what `sieving/src` was written against;
  the suite passes (11 passed, 2026-07-11) but a deprecation-surface review is prudent
  in later waves.
- **Codex-side guidance staleness** — workspace `AGENTS.md` still records
  pre-C0.1/C5.3 constraints; tracked as `documented_differences` in
  `GUIDANCE_PAIRS.json` pending a Codex-authored refresh
  (message `CC_2026-07-11T212734Z_c2-1-complete-guidance-drift-validator`).
