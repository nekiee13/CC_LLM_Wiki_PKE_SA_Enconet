# EF-3.1 historic-report scope confirmation

**Status:** Owner-directed applicability confirmation; not a conformity result

## What was checked

The two historic Ekonerg audit reports are:

- `docs/audit_report_examples/SA20-1.md`
- `docs/audit_report_examples/SA23-1.md`

Both reports use an activity table that includes material handling/storage/
transport, special processes, and testing/inspection/measuring-equipment
controls. Both reports then discuss these activities in detail.

## Six criteria to keep in scope

| Appendix B criterion | Historic report evidence | Scope decision |
|---|---|---|
| VIII — Identification and Control of Materials, Parts, and Components | SA20-1/SA23-1 activity 6 covers product/material control and handling; the reports discuss supplier and project material control. | Include; verify the exact identification method in current work samples. |
| IX — Control of Special Processes | SA20-1 section 7 and SA23-1 section 7 discuss special processes and supplier oversight. | Include. |
| XI — Test Control | SA20-1 section 8 and SA23-1 section 8 describe FAT and project testing. | Include. |
| XII — Measuring and Test Equipment | Both section 8 discussions cover measuring equipment and calibration/control. | Include. |
| XIII — Handling, Storage, and Shipping | SA20-1/SA23-1 activity 6 explicitly lists handling, storage, packing, and transport. | Include, including supplier-controlled work. |
| XIV — Inspection, Test, and Operating Status | Both section 8 discussions cover inspections, tests, QA/QC hold/witness points, and release/status controls. | Include. |

The historic reports sometimes audit Ekonerg's oversight of subcontractors rather
than Ekonerg performing the physical work itself. That still supports keeping
the controls in scope because the current audit checks whether Ekonerg controls
quality-affecting supplier work.

## Decision and limits

The six criteria were converted from `conditional` to `applicable` for
`RUN-20261003-32` under owner decision
`G2-HISTORIC-SIX-20261004-OWNER`. This does not mean the controls conform. It
only means the audit must ask the questions and collect current evidence.
No criterion is marked final N/A. The matrix now has 18 applicable criteria.

## Source anchors

- SA20-1 lines 238–240: activities 6–8.
- SA20-1 lines 397–434: handling/storage/transport, special processes, and
  testing/measuring equipment.
- SA23-1 lines 242–244: activities 6–8.
- SA23-1 lines 425–487: handling/storage/transport, special processes, and
  testing/inspection/measuring equipment.

The refreshed matrix is `out/2026-10-04/MIN-3.1-evidence-matrix-v2.md`.

The confirmation migration guard and evaluation validator were also corrected
so confirmed rows keep their confirmation reference and signer. The structural
validator now reports only the real remaining blocker: evaluation records have
not yet been created.
