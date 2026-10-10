# Ekonerg packaged documentary delivery

Date: 10 October 2026. Implementer: Codex. Reviewer: Claude, review pending.
State: **prepared and usable**, not issued under formal G5/G6 publication.

## Open or share the results

- [Review workspace](../outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010-final/portable_package/review_workspace.html)
- [Light dashboard](../outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010-final/ekonerg_appendix_b_dashboard.html)
- [Dark dashboard](../outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010-final/ekonerg_appendix_b_dashboard_dark.html)
- [Detailed report](../outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010-final/ekonerg_appendix_b_evaluation_report.md)
- [ZIP for transfer](../out/2026-10-10/Ekonerg_documentary_delivery_RUN-20261003-32.zip)
- [Actual 43-page PDF](../out/2026-10-10/delivery-browser-print-final/EKONERG_AUDIT_REPORT.pdf)
- [Delivery manifest](../outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010-final/release_manifest.json)

Copy the whole delivery folder or extract the ZIP, then open
`portable_package/review_workspace.html`. No database, server, login or network
connection is needed. The PDF is a separately verified print artifact, not part
of the ZIP; printing either dashboard remains available.

## What is preserved

The result is **77.8%**, **1,400/1,800** points: three fully, fourteen
substantially and one partially matched criterion. All 18 existing evaluations,
scope decisions and reasons are preserved. This is packaging, not re-sieving,
re-scoring or a new audit.

There are 475 active vendor crumbs. The score-support bundle contains the
379 vendor crumbs used by this evaluation, 442 exact quotations, and 118 full
linked chapters from 24 documents. These are different counting units, not
missing evidence. Raw sources and the SQLite file are not distributed.

Report links open the matching crumb and its complete source chapter. Both
light and dark copies retain the approved layout, collapsed-card summaries,
filters, search, sorting, keyboard shortcuts, evidence disclosures, matrix,
responsive layout and light printing. The only new dashboard script routes
report hyperlinks. Original audit scripts and data are preserved.

The existing English presentation is retained; quotations keep their original
language. No Enconet language choice, edition, approval or publication exception
is borrowed. Part 21 remains separate from the 18-criterion score.

The older compact-card/document-scoring snapshots show 68.1%, so they were not
used as the release source. The reviewed `all18-review` light and final `grid`
dark snapshots match the current DB at 77.8%. All older snapshots are intact.

## Structure and provenance

The folder has 16 payload files plus its final hash marker: evaluation package,
dashboard data, full report, light/dark dashboards, deduplicated evidence bundle,
and a portable run folder with catalog, workspace and package manifest.
It mirrors Enconet's artifact roles, not Enconet's data or gated-release status.
No wiki dashboard or canonical output was replaced.

Delivery manifest SHA-256:
`b1592b694271ef9ce000629bc19927c424c2ae8181712c947958f9ce84c2870a`.
ZIP: 2,568,952 bytes. ZIP SHA-256:
`8e87b99ed9e80c4220d0f27fe2f9d4abafff8e45d0808b1722a3adf3f5c50899`.
Uncompressed payload is 16,130,106 bytes. Full chapters were not cropped and
Enconet's byte/timing-cap approval was not applied to Ekonerg.

The candidate packager is company-neutral and pinned with its local dependency
in `audit_template/documentary_delivery/v1/`. This new add-on is review-pending;
the immutable v3 release and all other company folders remain unchanged.

## Validation

All successful commands below returned exit 0.

- `C:/xPY/vEnv/WikiEnconet/python.exe -m pytest Ekonerg/scripts/tests/test_package_audit_delivery.py Ekonerg/scripts/tests/test_dark_dashboard.py Ekonerg/scripts/tests/test_umbra_conformance_dashboard.py -q -p no:cacheprovider --tb=short --junitxml=Ekonerg/out/2026-10-10/delivery-focused-tests-final.xml`: **22 passed**. Synthetic CLI cases use spaces/Croatian names, with/without a sibling, and preserve all existing input bytes and timestamps. Safety checks cover stale projections, foreign paths, conflicts, racing writers, tampering and own-file rollback.
- `C:/xPY/vEnv/WikiEnconet/python.exe -B Ekonerg/scripts/package_audit_delivery.py --verify Ekonerg/outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010-final`: all 16 file hashes, sizes and exact inventory match.
- `python Ekonerg/scripts/verify_dashboard_browser.py --html Ekonerg/outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010/ekonerg_appendix_b_dashboard.html --output Ekonerg/out/2026-10-10/delivery-browser-print-final`: **29 checks**, actual 43-page PDF, all 18 rulings, score, mobile and print bounds. This legacy PDF verifier used existing Miniconda with PyMuPDF; the pinned runtime lacked that module. No dependency install or pin change was made.
- `C:/xPY/vEnv/WikiEnconet/python.exe Ekonerg/out/2026-10-10/verify_delivery_browser.py`: relocated light/dark viewers, 18 representative crumb links and three criterion links per viewer, controls, mobile, white printing, zero page errors and external requests. Final payloads are byte-identical to all 16 browser-verified payloads; only the final manifest's generator provenance differs from the intermediate candidate.
- `C:/xPY/vEnv/WikiEnconet/python.exe Ekonerg/scripts/run_all_validations.py --no-record`: eight phase-applicable checks passed. Later formal evaluation/report/release checks were explicitly skipped at `evidence_reviewed`, not claimed passed.
- Independent before/after SHA checks: **117 protected files unchanged**, including Ekonerg incoming/raw/DB/DATA/config/approvals and selected Enconet audit/release files. [Receipt](../out/2026-10-10/delivery-preservation.json).

Initial missing-module TDD, incomplete synthetic-test fixture, missing PyMuPDF,
keyword-only browser-verifier argument and a default-codepage verification read
failed. Corrections and reruns are recorded; none is counted as a pass. Older
candidate and diagnostic folders remain history. Full historical audit regression
was not rerun for this read-only packaging task.

## Publication boundary

Owner requested the package. That does not supply missing G4/G5/G6 records or
waive independent release review. The canonical report generator is unchanged
and still requires G4. This new report is a read-only documentary candidate
export of the already accepted tool result, not an approved formal findings
report. No formal finding/action rows are invented or written.

Next: Claude reviews this one delivery task. Owner then chooses whether to issue
the package through the existing formal release procedure and approves the
applicable records. G7 and real-audit verification remain separate.
