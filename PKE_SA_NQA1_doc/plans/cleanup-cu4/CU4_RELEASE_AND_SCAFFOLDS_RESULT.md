# CU-4.1 — v4 release and six supplier upgrades

Status: implemented, applied and verified. Claude review remains deferred.
This closes the implementation acceptance criteria for the existing CU-4.1
task. CU-4.2 and overall cleanup closure are still open. No task was added.

## What was done — ELI5

We made one new starter kit, then put the same kit in all six empty audit
folders. Each folder has its own scripts. The old kit was saved, not thrown
away. No company audit was started and no source or result was borrowed.

| Supplier | Installed files | Retained originals | Apply / verify / retry | Startup |
|---|---:|---:|---|---|
| IBE | 170 | 129 | Passed, exit 0 | setup; G1–G7 pending |
| TEKOL | 170 | 129 | Passed, exit 0 | setup; G1–G7 pending |
| IGH | 170 | 129 | Passed, exit 0 | setup; G1–G7 pending |
| IMK | 170 | 129 | Passed, exit 0 | setup; G1–G7 pending |
| KCPG | 170 | 129 | Passed, exit 0 | setup; G1–G7 pending |
| MOR | 170 | 129 | Passed, exit 0 | setup; G1–G7 pending |

Totals: **1,020 installed files and 774 retained originals**. The 170 entries
per supplier include the 164-file release and six local scaffold files.
Incoming content is unchanged. Database files are absent, approval CSVs contain
headers only, and source selection remains `pending-owner`.

The common homes are `work/benchmarks`, `work/manifests`, `work/derived`,
`work/reviews`, `docs/plans`, `coordination/handoffs` and `outputs/RUN-*`.
Unused optional folders are created when needed; no dummy result is generated.
Standalone light and dark dashboards are produced by the tested local tools.

## Immutable release

- Version: **4.0.0**, in `audit_template/framework/v4/`.
- Source tools commit: `5583591`.
- Release manifest SHA-256:
  `2a18e0db61973b3702989de63ebcf9c1a26f6492b6a55cccba30c950c92b2cb4`.
- Review state: `deferred`, not approved or waived.
- Current guide: `docs/FRAMEWORK_METHOD_V4.md` in each supplier.
- Old releases and addons remain unchanged. v2 manifest:
  `e9d3d9e7e79ffa8a28d4e0c0b2a2a55a6427e7e60a4fbcd443babe5c93c09a9d`.
  v3 manifest:
  `16f4015b64cc228d7a9e0537a0ae417dcb7f52c6153f17ba3746a979b698cf1c`.

The release has an empty active-prompt map, not an activated prompt. It has
shared regulatory criteria and synthetic framework benchmarks, not a vendor's
source documents, golden set, approval, audit database or conformance score.

## Retained history and recovery

The run ID is `cleanup-v4-20261013`. Each supplier's journal and originals are
under `work/migrations/framework-v4/cleanup-v4-20261013/`.
The saved external previews are `<supplier>-upgrade-preview.json` beside this
note. They pin the old bytes, the new release and the unchanged incoming files.

Old Git policy files use `.gitattributes.record` in the original archive.
The plan keeps their original identifiers and exact hashes. This makes those
policies inert, so a later Git checkout cannot change the saved file bytes.
Undo restores their original filenames and bytes.

The authority string records the existing owner cleanup authorization and
review deferral. `OWNER-PROCEED-CU4-20261013` labels the owner's chat request to
continue this task; it is not a supplier audit approval or a new gate decision.

## Verification commands and results

`PYTHON` below denotes `C:/xPY/vEnv/WikiEnconet/python.exe`. Commands ran from
the workspace root. `{V}` means each of the six supplier names in the table.

| Check | Command | Exit | Result |
|---|---|---:|---|
| Full release/upgrade suite | `PYTHON -B -m pytest audit_template/tests/test_vendor_upgrade_v4.py audit_template/tests/test_framework_release_v4.py audit_template/tests/test_framework_release_v2.py audit_template/tests/test_framework_release_v3.py audit_template/tests/test_bootstrap_sieving.py -q -p no:cacheprovider --basetemp .tmp/cu4-v4-publication-regression --tb=short --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/v4-publication-regression.xml` | 0 | 46 passed, two subtests passed; no failures, errors or skips |
| Final v4 byte-policy suite | `PYTHON -B -m pytest audit_template/tests/test_vendor_upgrade_v4.py audit_template/tests/test_framework_release_v4.py -q -p no:cacheprovider --basetemp .tmp/cu4-final-byte-policy --tb=short --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/v4-final-byte-policy.xml` | 0 | 17 passed, no skips; includes the final archive fix and full packaged pipeline |
| Freeze release | `PYTHON -B audit_template/prepare_framework_release_v4.py --destination audit_template/framework/v4` | 0 | 164 hash-listed files; source commit and deferred review recorded |
| Saved preview | `PYTHON -B audit_template/upgrade_vendor_v4.py --target {V} --output PKE_SA_NQA1_doc/plans/cleanup-cu4/{V}-upgrade-preview.json` | 0 | Each preview has zero blockers |
| Live apply and retry | `PYTHON -B audit_template/upgrade_vendor_v4.py --mode apply --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/{V}-upgrade-preview.json --run-id cleanup-v4-20261013 --authority "OWNER-LIVE-CLEANUP-20261012; OWNER-CLEANUP-SPRINT-20261012-REVIEW-DEFERRED; OWNER-PROCEED-CU4-20261013"` | 0 | Each reaches complete; repeat is safe |
| Live byte verification | `PYTHON -B audit_template/upgrade_vendor_v4.py --mode verify --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/{V}-upgrade-preview.json --run-id cleanup-v4-20261013` | 0 | All new files, originals, incoming hashes and legacy-home absence verified |
| Local startup | `PYTHON -B {V}/scripts/audit_command.py audit-status` | 0 | setup; seven pending gates; zero actions; no validation or result inherited |
| Local layout | `PYTHON -B {V}/scripts/project_layout.py --describe` | 0 | All six resolve their own v4 paths; no sibling runtime dependency |
| Enconet preservation | `PYTHON -B audit_template/framework_preservation.py --verify PKE_SA_NQA1_doc/plans/cleanup-cu4/enconet-before-scaffold-upgrades.json` | 0 | 2,304 captured files unchanged |
| Ekonerg preservation | `PYTHON -B audit_template/framework_preservation.py --verify PKE_SA_NQA1_doc/plans/cleanup-cu4/ekonerg-before-scaffold-upgrades.json` | 0 | 1,861 captured files unchanged |
| Guidance | `PYTHON -B scripts/check_guidance_drift.py` | 0 | Zero errors; Claude synchronization is explicitly pending |
| Skills | `PYTHON -B scripts/check_skill_structure.py` | 0 | Zero errors; 32 locations checked |
| Fresh Windows Git checkout | `PYTHON -B -m pytest audit_template/tests/test_v4_git_checkout.py -q -p no:cacheprovider --basetemp .tmp/cu4-git-checkout --tb=short --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/v4-git-checkout.xml` | 0 | All 164 installed release files and six scaffold files retain their exact bytes with `core.autocrlf=true` |

Preservation was measured before the new coordination and handoff records were
written. The expected Codex updates to `coordination/BOARD.md`, `HANDOFF.md` and
the append-only `wiki/log.md` are not audit data changes. The original capture
receipts remain unchanged so a reviewer can check this distinction.

The final Git check found missing workspace rules for a few framework contract
formats. Generic supplier-path LF rules were added to the shared workspace
`.gitattributes`; they exclude incoming, raw, DATA, outputs and agent-owned trees.
No supplier runtime or frozen release byte was patched. This remains a workspace
release, as documented in the installer guide; it is not a stand-alone external
ZIP. The new complete checkout test verifies the package and scaffold hashes.

The synthetic pipeline uses two supplier names, including spaces and Unicode,
both with and without a sibling. It runs through intake, chapters, evidence,
evaluation, report, separate dashboards, guarded publication and verification.
Synthetic test data stays in `.tmp/`; it is not installed in the release.

Red runs caught the missing v4 implementation, incomplete interruption undo
and a test UTF-8 assumption. Those were fixed before live use. The first full
compatibility run also found an old test missing the local layout import; the
existing v2 characterization was preserved. Failed runs were not called passes.
Live undo was not run: it was tested on disposable suppliers only.

## Next original task

Continue CU-4.2: remaining required suites, held-file and test-folder cleanup,
final structural checks across eight suppliers, committed shared-index refresh
and one final closure report. Claude post-review and Claude-owned guidance
updates remain pending. No new owner decision is requested here.
