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
| 1 | ~~Validation is advisory, not blocking~~ — **resolved 2026-07-11**: fail-closed filtering (C4.1) and blocking ERROR-validation export gate with recorded override reason (C4.2); see `LESSONS-LEARNED.md` | closed (tests `test_fail_closed_filter.py`, `test_blocking_validation.py`) |
| 2 | Unchecked fields: `statement` non-empty, `item_id` uniqueness, `item_type` enum (`record_side` enum is now hard-validated, VAL-SIDE-001, C4.2) | Task 1.4 + 5.3 strict schema tier |
| 3 | First-source scalar flattening hides secondary source locations in tabular review | Task 5.4 (`crumb_sources`, `crumb_quotes`) |
| 4 | No chunk linkage — weak source review | EPIC 6 |
| 5 | DOC prompt runtime-block defect (spec guide §8.4) | Task 5.1 + 5.6 |
| 6 | No prompt versioning / run generations | Task 5.2, EPIC 18.2/18.6 |
| 7 | No sieving effectiveness measurement | EPIC 18.3/18.4/18.5 |
| 8 | No multilingual evidence fields | Task 5.5 (ADR-0009) |
| 9 | Criterion XIII name: system canon uses the Oxford comma vs the official CFR heading | Note in `schemas/app_b_taxonomy.yml` (Task 1.1) |

## Unremediated findings (CX/CC reconciliation, `Enconet/docs/CX_CC_RECONCILIATION.md` §2.3)

1. **Spec guide §10.1 false statement — closed.** Corrected by C1.4 (v1.2,
   2026-07-11); C4.4 then implemented the single-owner contract the correction
   described (v1.3, `schemas/sieving_contract.yml`). Residual nit: the v1.3 footer
   line still reads v1.2 (Codex follow-up, `CX_2026-07-12T053430Z`).
2. **Verifier + repair-script hazard chain — contained by C4.3.** Hazardous and obsolete
   scripts are quarantined under `sieving/tools/_archive/`; the active verifier is
   ASCII-safe, checks dependencies first, distinguishes failure classes, and recommends
   restoration from version control rather than mutation.
3. **Obsolete `check_files.py` manifest — contained by C4.3.** The script is archived
   with the other historical migration tools and is not an active verifier.
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
  the suite passes (48 passed, 2026-07-12) but a deprecation-surface review is prudent
  in later waves.
- ~~Codex-side guidance staleness~~ — **resolved 2026-07-11/12**: Codex refreshed its
  guidance (`CX_2026-07-11T215626Z_c2-1-codex-review-and-refresh-complete`) and the
  obsolete pending `documented_differences` were removed from `GUIDANCE_PAIRS.json`
  (C2.1 follow-up, commit `1c21d85`).

## Deliverable validation hardening

### AFI-DASH-001 — Reject generic external URLs in offline dashboards

- **Status:** open, non-blocking hardening; recorded 2026-07-15 by owner direction.
- **Area:** `Enconet/scripts/validate_dashboard.py` and
  `Enconet/schemas/dashboard_schema.yml`.
- **Observation:** EPIC12's forbidden-pattern contract detects named authentication/CDN
  hosts and several double-quoted HTTP tag forms, but it is host-specific and
  quote-sensitive. An arbitrary external URL or a single-quoted `src`/`href` could fall
  outside those patterns.
- **Current containment:** the independently accepted EPIC12 template contains no external
  references, package-derived values are inserted with `textContent`/`createElement`
  rather than as HTML or attributes, embedded JSON escapes `<`, and no live dashboard has
  been generated. This AFI does not reopen EPIC12 acceptance.
- **Evidence:** Claude Code review
  `Enconet/coordination/archive/CC_2026-07-15T212545Z_dashboard-review-accept.md`,
  Codex acknowledgement and
  resolution manifest `Enconet/coordination/archive/CX_2026-07-15T212847Z_resolved-message-manifest.md`,
  implementation commit `30c51ed`, closure commit `2bd708a`.
- **Planned improvement:** in a future validation-hardening pass, reject generic
  `http://`, `https://`, protocol-relative URLs, and external `src`/`href`/CSS import
  variants regardless of quote style; add negative tests for arbitrary hosts and
  single-quoted attributes. Close only with the new tests and aggregate validation passing.
