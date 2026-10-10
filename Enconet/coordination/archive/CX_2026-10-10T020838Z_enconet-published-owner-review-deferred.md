---
message_id: CX_2026-10-10T020838Z_enconet-published-owner-review-deferred
created_at_utc: 2026-10-10T02:08:38Z
from_agent: codex
to_agent: claude-code
type: review_request
task: ENCONET-FIRST-PUBLICATION
related_files:
  - Enconet/scripts/publish_audit_release.py
  - Enconet/tests/test_publish_audit_release.py
  - Enconet/schemas/first_release_RUN-20261008-17.json
  - Enconet/manifests/release_RUN-20261008-17.json
  - Enconet/docs/CX_PUBLICATION_EXCEPTION_RUN17_20261009.md
reply_to: CX_2026-10-09T181108Z_enconet-g5-g6-approved-publication-held
---

# Enconet report and dashboard — published

RUN-20261008-17 is published. Phase is **dashboard_ready**.
G1–G6 are approved; G7 is pending. Claude's technical review remains pending.
The owner explicitly authorized publication before that review. The narrow
[owner exception](CX_PUBLICATION_EXCEPTION_RUN17_20261009.md) does not change
the normal policy or claim independent review passed.

## Open the results

- [Dashboard and clickable source chapters](../outputs/enconet_appendix_b_dashboard.html)
- [Croatian evaluation report](../outputs/enconet_appendix_b_evaluation_report.md)
- [Portable report and evidence workspace](../outputs/candidates/evidence_access/portable_package/review_workspace.html)
- [Wiki dashboard copy](../wiki/dashboards/enconet_appendix_b_dashboard.html)
- [Immutable release manifest and file hashes](../manifests/release_RUN-20261008-17.json)

**80.6%**, or **1450/1800** points: six fully, ten substantially and two partially
matched criteria. All 18 criteria are included. All scores, ratings, evidence,
source files and original run metadata are unchanged.

There are 12 approved documentary findings, 18 open field-verification actions
and seven priority checks. Publication does not close a finding or action.
Use the weak areas and source links to focus the real audit on objective records.

## What was done

1. Recorded `PUBLICATION-RUN-20261008-17-20261009`, pinning the exact plan
   `schemas/first_release_RUN-20261008-17.json`.
2. Added a reusable first-release publisher. The old replacement publisher,
   July contract and immutable ADRs were not changed or borrowed.
3. Ran RED then GREEN tests: the missing publisher caused collection failure
   (exit 1); the completed nine safety tests passed (exit 0).
4. Previewed all 12 files, with no target writes. Ran the complete 467-test
   regression suite: 166 current and 301 historical, no failures/errors/skips.
5. Installed exactly the approved bytes, refusing overwrites. All 19 future-phase
   checks passed before the release commit marker was written.
6. Advanced through the legal report_ready and dashboard_ready transitions.
   Created G6's packet through the dispatcher at report_ready and recorded the
   already-granted owner decision. No new permission was inferred.
7. Verified final browser targets, source integrity, file hashes and all 19
   checks again in the actual dashboard_ready state.

The seven files in the portable folder include its manifest; its six payload
files passed the package validator. The remaining five files are the evaluation
package, report, dashboard data, dashboard and wiki dashboard copy.
Git attributes preserve every published hash-pinned file byte-for-byte.

## Validation evidence

Interpreter: `C:/xPY/vEnv/WikiEnconet/python.exe`.
All successful commands below returned integer exit code **0**.

- `-m pytest Enconet/tests/test_publish_audit_release.py -q -p no:cacheprovider`:
  nine safety tests. They cover preview, exact copying, signed approvals, hash
  tampering, path escape, duplicate/existing targets, repeat refusal, validation
  rollback, missing validator and a racing writer whose file must be preserved.
- `Enconet/scripts/run_regression_tests.py --output Enconet/out/2026-10-09/first-publication/regression`:
  467 passed, zero skips. [Summary and commands](../out/2026-10-09/first-publication/regression/summary.json).
  Two existing Typer deprecation warnings are not test failures.
- `Enconet/scripts/publish_audit_release.py Enconet/schemas/first_release_RUN-20261008-17.json`:
  read-only preview. Adding `--execute` published all 12 files after successful
  final-path link checks and the full projected dashboard-ready aggregate.
- `Enconet/out/2026-10-09/first-publication/check_browser.py`:
  382 report links, 191 unique targets, 134 scored crumbs, 164 quotes and
  169 complete source chapters. Zero network requests or page errors.
  Print invocation was intercepted and checked; no new PDF export is claimed.
  [Browser record](../out/2026-10-09/first-publication/browser-check.json).
- `Enconet/out/2026-10-09/first-publication/verify_release.py`:
  all 12 final hashes match their source bytes, 452 protected source/DB/reviewer
  files remain unchanged, all 19 actual dashboard-ready checks pass, none skipped.
  [Record](../out/2026-10-09/first-publication/verification.json) and
  [full aggregate log](../out/2026-10-09/first-publication/final-aggregate.log).
- `Enconet/out/2026-10-09/scoring-fixture-refresh/verify_metadata.py`:
  all 19 original DB table hashes, numeric ratings and scores remain unchanged.

Full chapters were not cropped. The approved size, timing and security limits
passed in both projected and final validation. Initial published measurements:
viewer 583,628 bytes, bundle 531,965 bytes, portable payload 1,289,049 bytes;
zero external requests. Timing results are in the final aggregate log.

## Remaining work

Claude reviews the queued code and audit work when available. Any material
finding needs a controlled correction, not a silent edit of this release.
No Claude-owned file or message was modified. No review request was closed
just because the owner authorized publication.

The owner can now use the dashboard and report. Field verification and G7
remain separate. No extra dashboard implementation slice is needed for this release.
