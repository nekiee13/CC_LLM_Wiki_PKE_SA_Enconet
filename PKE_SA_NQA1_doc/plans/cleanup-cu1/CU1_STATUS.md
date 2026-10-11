# CU-1 inventory and baseline — review packet

Date: 12 October 2026. Captured Git baseline: `47bde73`.

## Result — ELI5

We counted the contents of the filing cabinet and recorded what the audits say.
We have not moved the boxes. The inventory is a draft move map, not permission
to run a migration. Classification holds and owner layout choices remain open.

The full verified scan lists **77,457 entries**, including folders. It found
zero access failures, zero changed protected inputs, and zero file-destination
collisions. Nested Git stores are recorded but their internal objects are not
walked. Redirected paths are recorded and not followed.

| Audit | Vendor crumbs | Regulatory crumbs | Criterion rows | Score | Database integrity |
| --- | ---: | ---: | ---: | --- | --- |
| Enconet | 2,700 | 298 | 18 | 1,450/1,800 = 80.6% | OK; zero foreign-key errors |
| Ekonerg | 475 | 55 | 18 | 1,400/1,800 = 77.8% | OK; zero foreign-key errors |

The six future-supplier folders have no configured audit database. None was
created. Their current local files are included in the receipt.

## Files to review

- `scan-20261012-verified/inventory.zip`: full machine-readable `inventory.json`.
  Unpack outside the live audit folders for review. It contains path, owner,
  tracked/ignored/untracked status, byte hash, timestamp, attributes, retention,
  proposed destination, holds, collisions and old-path dependency groups.
- `scan-20261012-verified/audit-baselines.json`: read-only DB hashes, row counts
  and complete table-content digests, active-crumb counts, per-run score totals,
  integrity results and hashes for protected local files.
- `db-path-field-check.json`: supplementary path-field check and its limits.
- [Read-only scanner](../../../scripts/cleanup_inventory.py): the workspace
  tool, also shown in the commands below.

The large inventory JSON is compressed for Git storage; it remains available
locally in the verified scan folder. The ZIP is a receipt, not an audit delivery
or a dashboard dependency. The earlier sandbox receipt stays local as history;
its 210 access failures are superseded by the verified elevated scan.

## What remains held

- **962 output entries:** their exact run, result/log purpose, or history home
  needs semantic review. Do not infer a run from a date or directory label.
- **Seven pre-existing dirty files:** validation ledger, wiki log, Enconet
  evidence-access plan, and four support-transfer files. Preserve their edits.
- **Six Claude-owned proposed file moves:** two Enconet ADRs and four shared
  support-transfer records. Codex may not move them or move their parent
  directory wholesale. Claude handles its own part.
- **6,495 redirects/hardlinks:** many are test-fixture `current` links. Do not
  follow, rewrite or remove them through a broad folder operation.
- **Reset scratch:** keep `ekonerg-reset-rk6wsybf` held until purpose is agreed.
- **Plan classification:** this scanner uses conservative filename rules. Some
  root-level/frozen plans remain `retain-or-review-purpose`. Complete their
  explicit `docs/plans` mapping within CU-1 before approving an executable map.

There are 1,028 proposed-move entries and 24,155 retained-scratch entries.
These counts include directories and their children: they are not counts of
independent move operations. CU-2 tooling must compile non-overlapping moves,
not run each inventory row as a shell command.

Old-path references are lexical candidates, grouped by token. They include
history as well as live code and must be checked for actual use. The DB column
name check found no old-location rows in the inspected fields, but does not
prove that every JSON value or file-based ledger is free of stored paths.

## Source and database preservation

The scan opened the two live databases with SQLite `mode=ro` and `query_only`.
It used a read transaction and compared DB byte hashes before/after the reads.
Each table has a row count and an order-independent full-content digest; full
chapter text is represented in those digests, not copied into this report.

Protected-file receipts cover 717 Enconet files, 1,055 Ekonerg files and 34
files for each future supplier. Registered sources, current data, approvals,
calibration and outputs are included. Project-state and immutable release file
hashes are also present in the inventory. No state, approval or score was edited.

Enconet DB SHA-256:
`f17c977f8c5ffec13a279bdb909dd17f38e056e5183812a92ae5810b03251ed1`.

Ekonerg DB SHA-256:
`161c56ff5d457348ec6809c5e6dcc41e2dd09854d4e71cde11d12a2064d387c0`.

## Reproduction and checks

Run from the workspace root with the pinned interpreter. A fresh output name
is required; receipts are never overwritten.

```powershell
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_inventory.py -q -p no:cacheprovider --tb=short
C:/xPY/vEnv/WikiEnconet/python.exe scripts/cleanup_inventory.py --workspace C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1 --suppliers Enconet Ekonerg IBE TEKOL IGH IMK KCPG MOR --output C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1/PKE_SA_NQA1_doc/plans/cleanup-cu1/NEW-RECEIPT-NAME
```

Without `--output`, the tool only prints the scan summary. With it, the only
writes are new receipt files, not changes to inventoried inputs. The CLI has
no move, apply, reset or delete option. Its lexical map is not migration code.

Final focused test result: **exit 0, four passed**, including two synthetic
supplier names, source/DB/sibling preservation, receipt no-clobber and output
path guards. Windows denied pytest Temp access on one rerun; elevated retry
passed. The initial live scan failed on the wrong active-crumb field name;
the corrected `document_side` query is covered by the regression fixture.

Verified live scan: **exit 0**, 77,457 entries, zero access failures and zero
changed protected inputs. Full audit/browser regression was not run: no audit
runtime, dashboard or live layout changed in this task.

## Next step

Claude reviews these receipts and the map's holds. Owner confirms the proposed
layout/retention choices. Finish semantic output/plan classification within
CU-1, then review the final map before CU-2 and any live move. CU-1 is not
declared fully closed while those acceptance items remain open.
