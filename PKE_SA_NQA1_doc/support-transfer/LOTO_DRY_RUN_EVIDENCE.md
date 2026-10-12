# CC_Loto Slice 1 disposable dry-run evidence

## Result

The exact eight-file Slice 1 render overlays cleanly on a disposable copy of CC_Loto baseline
`b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`. CC_Loto itself remained clean and unchanged.

Disposable root: `C:\Users\PC\AppData\Local\Temp\loto-s1-84698c0005854998988228cf74c174df`.
The disposable root is evidence workspace only and is not a target path or publication source.

## Overlay checks

| Check | Result | Disposition |
|---|---:|---|
| Rendered support files | 8 | passed |
| Byte mismatches against exact render | 0 | passed |
| Disposable Git porcelain | exactly `?? support/` | passed |
| Tracked product diff | empty | passed |
| Renderer link/sensitivity checks | exit `0` | passed |

The first comparison attempt used unavailable `[System.IO.Path]::GetRelativePath` and therefore
printed an invalid mismatch count of 8 alongside method errors. It is not acceptance evidence.
The compatible substring-based rerun completed with exit code `0` and mismatch count `0`; that
rerun is the result recorded above.

## Native target evidence

A disposable isolated environment installed the exact target `requirements.txt` whose SHA-256 is
`01ACBAB0774D6D0656F89FA24BC4F0F204D8353E74CD5A8621F64100024DB3CD`. Runtime outputs and model
caches were redirected to disposable short paths. No CC_Loto or shared-interpreter dependency
state was changed.

Every completed short layer used the target-native runner and explicit discovery pattern:

```powershell
python run_tests.py --layer <layer> --pattern test*.py --verbosity 1
```

| Layer | Tests | Exit | Result |
|---|---:|---:|---|
| `core-unit` | 42 | 0 | passed |
| `contract` | 25 | 0 | passed outside sandbox |
| `state-integrity` | 3 | 0 | passed outside sandbox |
| Total required short layers | 70 | 0 | passed |
| `webapp` | no final count | terminated after exceeding 120 seconds | unavailable, not failed or passed |

The initial in-sandbox contract and state-integrity attempts failed before assertions with Windows
`PermissionError [WinError 5]` under disposable temp roots. Their outside-sandbox reruns passed
25/25 and 3/3, confirming sandbox artifacts. The target's default full run also produced no final
result within its limit and remains unavailable. The proposed slice changes documentation records
only, so model, optimizer, backtest, integration, and webapp execution are not required acceptance
layers under the approved Loto profile.

## Stop conditions

Do not write CC_Loto if its baseline, branch, upstream relation, or clean status changes; if any
reviewed byte or allowed path changes; if sensitivity/link checks regress; or if the independent
reviewer records a finding. Silence is not acceptance.
