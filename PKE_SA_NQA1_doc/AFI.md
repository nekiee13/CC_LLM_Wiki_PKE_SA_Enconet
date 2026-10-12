# AFI — Areas for improvement

- **Scope:** known limitations and improvement opportunities across the workspace,
  each with its evidence source and planned fix. This is the improvement ledger;
  resolved items are marked resolved in place and dated, with reusable knowledge
  linked to `LESSONS-LEARNED.md`.
- **Authority:** ADR-0021 defines identifiers, evidence fields, statuses, blocking
  semantics, and transitions to lessons learned and good practices.
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

## Token-efficiency future upgrade options

### AFI-TOKEN-001 — Evaluate P0–P6 through a controlled token-efficiency pilot

- **Status:** `deferred-until owner authorizes a controlled A/B pilot and selects its corpus,
  provider/model, prompt/schema versions, repetitions, and evidence-retention conditions`.
- **Date recorded:** 2026-07-27.
- **Severity / blocking:** improvement opportunity; non-blocking. This AFI does not authorize a
  pilot, pipeline changes, token-measurement storage, numerical targets, or controlled-stage/gate
  changes.
- **Scope / area:** workspace agent navigation and Enconet downstream source-processing,
  evaluation, review, validation, and index-maintenance workflows.
- **Observation:** complete reading of incoming controlled sources remains mandatory, but later
  stages may spend avoidable tokens reloading unchanged source, evidence, logs, manifests, and
  validation output. The proposed P0–P6 measures attempt to reduce that repeated context while
  preserving canonical evidence and mandatory full-context fallback.
- **Authoritative boundaries:** controlled sources, current audit state, human gates, validators,
  and approved decisions outrank this AFI and
  [`TOKEN_EFFICIENCY_PROPOSAL.md`](TOKEN_EFFICIENCY_PROPOSAL.md). No summary, packet, index, or
  token target becomes a new evidence authority.

#### Candidate upgrade options

| Option | Future upgrade | Expected value and containment |
|---|---|---|
| P0 | Retrieval discipline | Prefer current symbol/section/row indexes, narrow `rg`, stable identifiers, and bounded context. Escalate to exact evidence, adjacent context, or the complete source whenever correctness requires it. Primarily an operating discipline, not a new subsystem. |
| P1 | Minimal stage-level measurement | Use existing provider counters first, paired with model/prompt/schema versions, item counts, retries, fallback costs, and validation outcomes. Do not build a telemetry schema or store prompt/source content before need, sensitivity, access, and retention are approved. |
| P2 | Criterion-scoped evidence packets | Consider canonical read-only projections with stable crumb/quote/chunk/source references only if measurement proves repeated evidence loading is material. Mandatory traceability and full-source escalation prevent the packet from becoming a second evidence authority. |
| P3 | Verified delta review | Review changed crumbs and generation diffs first only when stable identifiers, hashes, lineage, and diff completeness prove what is unchanged. Fall back to full comparison when proof is incomplete; retain required full-baseline review at approval gates. |
| P4 | Deterministic/LLM separation | Keep parsing, linking, validation, scoring, package construction, and rendering in scripts; reserve LLM context for semantic judgment, exception review, and synthesis. Reuse existing boundaries before building new mechanisms. |
| P5 | Validation scheduling | Continue focused checks during iteration and complete mandatory aggregate/gate validation at controlled boundaries. This is existing discipline; targeted checks never replace required validation. |
| P6 | Commit-scoped index maintenance | Continue changed-path refreshes when safe and full rebuilds for deletion/rename, scope/parser, integrity, or history cases. This is largely existing ADR-0019 discipline, not a standalone implementation slice. |

#### Unverified saving projections

These ranges are planning hypotheses, not targets, measured results, or completion evidence:

| Processing area | Codex planning hypothesis | Independent Claude evaluation |
|---|---:|---|
| Initial complete controlled-source reading | approximately 0% | Defensible as a mandatory scope floor, not a saving claim. |
| Routine code/document navigation | potentially 20–60% fewer context tokens | Plausible order-of-magnitude range but highly task-dependent; describe as meaningful and variable. |
| Later criterion evaluation with source reuse | potentially 30–70% fewer input tokens | Theoretically strongest category, but the upper bound assumes full-source escalation remains uncommon. |
| Diff-first review of mostly unchanged runs | originally estimated 60–90% fewer review-context tokens | Do not retain as a fixed range. Expected saving scales inversely with delta size; large deltas or verification/fallback overhead may erase it or make it negative. Report actual delta size. |
| First-document end-to-end processing | perhaps 10–30% lower token use | Plausible hypothesis because mandatory intake limits the achievable saving. |
| Repeated processing across documents/iterations | potentially 30–60% lower token use | Plausible aggregate hypothesis only if criterion reuse and verified-delta benefits both materialize. |

No quantified efficiency improvement may be claimed until comparable measured runs exist.

#### Independent review findings and risks

Claude Code independently reviewed the complete proposal and approved it as suitable for a
**controlled pilot proposal only**, without implementation authorization. The review added four
required risk controls:

1. **Fallback double-payment:** net savings must include failed lean attempts and subsequent full
   processing; a high fallback rate can make the optimized path more expensive.
2. **Correlated reviewer blind spots:** compact packets may look complete to both agents. A pilot
   requires periodic independent full-baseline spot checks, not escalation triggers alone.
3. **Metric-gaming pressure:** token counts must always be reported with quality, failure, retry,
   escalation, and fallback evidence; no stage is judged on token count alone.
4. **Telemetry sensitivity:** token records may expose document, chunk, criterion, or prompt data
   and must inherit appropriate controlled-evidence access and retention treatment.

The review recommends treating P5/P6 as existing discipline, keeping P1 limited to existing
provider counters, piloting P3/P4 before building new tooling, and deferring P2 until measurement
proves a material repeated-evidence cost.

#### Smallest credible future pilot

- **Candidate corpus:** existing DOC-0021 / RUN-20260723-01 and inactive
  RUN-20260723-02 artifacts may provide a reproducible corpus and generation diff without adding a
  new controlled source. This is not a fully approved downstream baseline: G1 registration is
  approved, while G2 evidence review remains pending.
- **State containment:** any authorized pilot must be isolated/read-only with respect to production
  audit state, must not promote RUN-20260723-02, and must not advance or rely on G2.
- **Measurement limitation:** no historical provider-token baseline was found in these run
  artifacts. Baseline and lean arms must therefore be measured prospectively under equivalent
  corpus/revision/model/prompt/schema/stage conditions.
- **Repetitions:** one paired run is feasibility evidence only; use at least two-to-three comparable
  paired runs before treating a result as a stable signal.
- **Break-even:** net token delta equals all lean-path tokens, including verification, failed
  attempts, retries, and full fallbacks, minus baseline full-path tokens. A positive pilot signal
  requires a negative net delta, all quality-preserving acceptance criteria passing, and reported
  escalation/fallback and delta-size data.

- **Evidence:** [`TOKEN_EFFICIENCY_PROPOSAL.md`](TOKEN_EFFICIENCY_PROPOSAL.md);
  `CX_2026-07-27T211543Z_p0-p6-expectations-review`;
  `CC_2026-07-27T211947Z_pilot-proposal-independent-review`;
  `Enconet/wiki/gates/G1-20260723-SRC001-enconet.md`;
  `Enconet/wiki/gates/G2-20260723-ING001-enconet.md`;
  `Enconet/sieving/runs/RUN-20260723-02/diff-RUN-20260723-01-to-RUN-20260723-02.json`.
- **Consequence / value:** a small comparable pilot can determine whether repeated-context savings
  exceed measurement, verification, review, retry, and fallback costs before the workspace invests
  in evidence-packet or telemetry infrastructure.
- **Owner / next action:** owner decides whether to authorize the isolated pilot and its exact
  conditions. If authorized, Codex implements under a scoped claim and Claude independently
  reviews. Until then, no implementation task exists.
- **Resolution criteria:** mark `resolved` only with an owner disposition or comparable pilot
  evidence showing the net result and all quality checks. If the pilot yields reusable evidence,
  create or update the linked lesson/practice record required by ADR-0021.

## Deliverable validation hardening

### AFI-DASH-001 — Reject generic external URLs in offline dashboards

- **Status:** `open`; non-blocking hardening; recorded 2026-07-15 by owner direction.
- **Owner / next action:** unassigned; schedule in a future validation-hardening pass.
- **Governing ADR:** ADR-0021.
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
