# Enconet — Croatian report draft and G5 review

## Current result

Update: the owner approved the size limits and all linked viewer/browser checks
now pass. See [G5 ready package and final measurements](G5_READY_20261009.md).
The blocker section below records the earlier condition; it is now resolved.

The Croatian report is generated and passes report/source validation.
Score stays **80.6%,1450/1800**, with **18 criteria**:6 fully,10 substantially,
two partially. G1–G4 are approved. **G5 remains pending.**

[Open the report draft](../outputs/candidates/evidence_access/RUN-20261008-17/enconet_appendix_b_evaluation_report.md).
[Canonical approved assessment package](../out/2026-10-09/report-run17/enconet_appendix_b_evaluation_package.json).

The report contains the11 required sections, individual criterion points and
five-point ranks, supporting arguments, limitations and judgments,12 approved
documentary findings,18 coverage rows and seven priority actions. All18 actions
remain in the approved package; none is marked completed. Six covered coverage
rows are routine verification anchors, not deficiencies.

The main weak areas remain IX (VT/special-process scope and detailed controls)
and XVIII (audit-cycle coverage). Field verification remains pending.

## What was corrected in one tested report-format change

The old renderer showed historical calculation notes saying G3 was still pending
and omitted stored criterion points and affirmative/contrary summaries. New
`--documentary` presentation uses the approved summaries/judgment and stored
scores, shows current G2/G3/G4 approvals, and orders criteria I–XVIII from the
canonical taxonomy. It does not change the original rationale in the DB/package.
The original0.1-placeholder calculation stamp remains historical provenance;
it is not a claim that current G3 is pending. The numeric model remains approved.

Multiline findings now cite their gap/evidence on the primary finding line,
so the report consistency validator can independently verify the citation.
Legacy default output stays unchanged, preserving historical benchmark bytes.

No score, applicability, source, quote, chapter, run identity or finding/action
content changed. Normal `audit-report` dispatcher routing was used. No protected
published report/dashboard or existing light-mode file was overwritten.

## Important blocker: the linked evidence viewer

The complete companion bundle is **531,965 bytes**. The approved current cap is
**524,288 bytes** (512KiB). It exceeds that cap by **7,677 bytes**.
`generate_dashboard.py` therefore correctly refused to publish the companion
viewer, exit1. Nothing was truncated to make it fit.

The intended sibling file is `enconet_appendix_b_dashboard.html` in the same
candidate directory. It is an evidence companion, not a released G6 dashboard
or GUI redesign. Its report links are already generated, but the viewer does
not yet exist. **Do not treat these source links as operational yet.**

Owner decision requested: bundle and viewer caps1MiB each, total package2MiB.
Keep workspace65,536bytes, all projection-count limits, timing and security
limits unchanged. The relevant policy says not to raise limits silently.
No cap change has been made, and no approval is inferred from `proceed`.

Once approved: apply the reviewed capacity setting, build the viewer, validate
every report target/chapter and run the pinned offline browser checks. Only then
present G5 as ready for report release. G5 approval is not requested before
those checks succeed.

## Audit basis and limits for the owner

- Enconet alone is the supplier boundary; other companies/NEK are not separate
  targets. Supplier controls are checked only within Enconet's responsibility.
- Appendix B is governing; NQA-1:2015 Part1 is the approved interpretation basis.
  Only explicitly invoked PartII2.7/2.14 are included where relevant; other
  PartII and PartsIII–IV remain supporting. No edition was inferred here.
- Part21 remains separate from the18-criterion score. Direct NRC jurisdiction,
  US contract scope or dedication role is not presumed.
- XIII has the approved limited MTE/relevant physical-media scope.
- The source fragment in PartII2.7§201 remains a source limitation, not a vendor
  nonconformance. No missing words were invented.
- This is a documentary pre-flight result to direct a real audit, not a field
  implementation certificate.

See [approved source basis](SOURCE_BASIS_APPROVED_20261007.md),
[G2 scope](G2_APPLICABILITY_APPLIED_20261008.md),
[G3 score/model approval](G3_APPROVAL_20261008.md), and
[G4 findings/action approval](G4_APPROVAL_20261008.md).

## Validation evidence

| Check | Command/result | Exit |
|---|---|---:|
| Current package | `python Enconet/scripts/build_evaluation_package.py --run-id RUN-20261008-17 --output Enconet/out/2026-10-09/report-run17/enconet_appendix_b_evaluation_package.json` | 0 |
| Report | Canonical `audit-report`, with `--documentary` and sibling viewer target | 0 |
| Report/source consistency | `python Enconet/scripts/validate_report.py Enconet/out/2026-10-09/report-run17/enconet_appendix_b_evaluation_package.json Enconet/outputs/candidates/evidence_access/RUN-20261008-17/enconet_appendix_b_evaluation_report.md --no-record` | 0 |
| Full final suite | `C:/xPY/vEnv/WikiEnconet/python.exe Enconet/scripts/run_regression_tests.py --output Enconet/out/2026-10-09/report-run17/regression-final`; **452 passed**,zero failed/errors/skips | 0 |
| Focused report tests | Pinned pytest, `test_epic11_report.py`; **11 passed** | 0 |
| Phase/benchmarks | `python Enconet/scripts/run_all_validations.py --benchmarks --no-record`;11 phase checks and both benchmark classes pass | 0 |
| Report bundle | `python Enconet/scripts/validate_evidence_bundle.py Enconet/outputs/candidates/evidence_access/RUN-20261008-17/evidence_bundle_report_g5.json`;134 unique crumbs,164 quotes,169 chapters,17 docs,18 evaluations/coverage rows,12 findings,18 actions | 0 |
| Viewer build | Existing generator rejects531965>524288bytes | **1** |
| Live source links/browser behavior | **Blocked**,viewer absent pending cap decision; not a pass | not-run |

The test-first stages reproduced the missing documentary format, multiline
citation placement and Roman-numeral sort issues before the fixes. Final suite
tests current code and preserves all legacy assertions/output bytes. Its two
Typer/Click deprecation warnings remain visible.

[Final complete-suite summary and commands](../out/2026-10-09/report-run17/regression-final/summary.json).
[Current test report](../out/2026-10-09/report-run17/regression-final/current.xml).
[Historical test report](../out/2026-10-09/report-run17/regression-final/historical.xml).

Claude review remains deferred. No independent-review acceptance or G5 release
is claimed. Phase remains `findings_approved`.
