---
record_type: disposable_dry_run_evidence
target: CC_Loto
slice: 2
recorded_at_utc: 2026-07-19T21:12:37Z
target_parent: 496800dcf499f5bde21e52e1ea6abe917ca22e4f
---

# CC_Loto Slice 2 disposable dry-run evidence

## Result

The exact 14-file coordination-core render overlays cleanly on a disposable tree containing the
published Slice 1 support records. The installed candidate validator returned `0 errors, 0
warnings`; all 14 overlay bytes matched their reviewed sources; the disposable tree was removed.
CC_Loto remained clean, unchanged, and synchronized at `496800dc`.

| Check | Result | Disposition |
|---|---:|---|
| Exact candidate files | 14 | passed |
| Existing-target collisions | 0 | passed |
| Fixed-timestamp rerender hash differences | 0 | passed |
| Overlay byte mismatches | 0 | passed |
| Overlay coordination validation | exit `0`, 0 errors, 0 warnings | passed |
| Target HEAD/origin divergence after checks | `0 0` | passed |
| Target porcelain after checks | empty | passed |

## Native short-layer baseline

The unchanged target tip was tested with the disposable environment created from CC_Loto's own
requirements and its native runner. Output and model-cache paths were redirected outside the
repository.

```powershell
python run_tests.py --layer core-unit --pattern test*.py --verbosity 1
python run_tests.py --layer contract --pattern test*.py --verbosity 1
python run_tests.py --layer state-integrity --pattern test*.py --verbosity 1
```

| Layer | Tests | Exit | Result |
|---|---:|---:|---|
| `core-unit` | 42 | 0 | passed outside sandbox |
| `contract` | 25 | 0 | passed outside sandbox |
| `state-integrity` | 3 | 0 | passed outside sandbox |
| Required short-layer total | 70 | 0 | passed |

The initial in-sandbox runs exited `1` because Windows denied repository output and user-TEMP
directory creation before or during tests. The same commands, with output/cache redirection and
outside-sandbox filesystem access, passed 42/42, 25/25, and 3/3. The failed attempts are not counted
as passes. Product/model/optimizer/webapp layers were not required for this documentation and
support-tool candidate and were not run.

## Preparation failures retained as evidence

Two initial renderer attempts exited `1` before validation because Python-created temporary
directories inherited unusable sandbox permissions. The renderer was corrected to create and
verify a workspace-local disposable root explicitly, clean it after success, and constrain its
render-output cleanup to the Wiki workspace. The corrected fixed-timestamp runs exited `0` and
reproduced all 14 hashes.

The isolated target-requirements environment's support import probe exited `1` because `PyYAML` is
not declared there. This is an explicit reviewer item, not a passed check; no dependency was added.

## Stop conditions

Stop before any CC_Loto write on target drift, dirty status, path collision, byte mismatch,
validator failure, unresolved dependency disposition, native short-layer regression, sensitive
content, unresolved non-template placeholder, dangling/escaping link, or reviewer finding.
