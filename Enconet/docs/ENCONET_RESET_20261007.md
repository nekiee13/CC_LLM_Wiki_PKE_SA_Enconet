# Enconet archived reset - 7 October 2026

Owner authorization: "archiving permission confirmed, reset confirmed.
preserve incoming. proceed" (owner chat; spelling normalized here).

## Result

- 352 prior runtime/source/result files removed after archiving.
- Six mutable ledgers reset to headers, including old ingestion runs and
  quote-link exception candidates.
- 36 incoming files preserved byte-for-byte.
- 1,317 framework/history files hash-checked unchanged immediately after reset.
- Fresh database initialized with 18 common criterion names. No old evidence,
  applicability decisions, evaluations, findings or approvals inherited.
- Project restored to setup; all gates pending and output language unset.

Incoming contains 26 vendor and 7 regulatory Markdown documents. `.gitkeep`,
`desktop.ini` and the conversion-instruction note are not audit source documents.
The earlier count of 27 vendor files included desktop.ini and is corrected here.

## Recovery archive

Local archive outside the target project:

`audit_archives/Enconet/2026-10-07/audit-reset-20261007T132014Z-74f87f121bc8.zip`

- Bytes: 2,376,107.
- SHA-256: `38018c13eb9c17172c7c3486b4041dbb54e27618f78cfb9989ebb56cbfcfaedf`.
- All 358 archived file entries match their pre-reset SHA-256 values.
- ZIP CRC check passed; the ZIP also contains `reset-plan.json`.
- Reviewed external plan: `reset-plans/enconet-reset-20261007-reviewed.json`.
- Plan hash: `74f87f121bc83b5d1024c9c228ebcd0f04fc624a4c8dc0108851592ff5e9a86b`.

The archive includes the owner's previously uncommitted evidence-bundle candidate
bytes. It is local recovery data, excluded from Git, not an issued audit result.
Restore into a separate recovery folder first; never overwrite the new audit.

## Safety checks and code correction

Before apply, live preview exposed 46 read-only Windows raw targets. The reset
was corrected to remove the read-only flag only on an exact fingerprinted target
after the archive is verified. Archive validation now checks CRC and each file's
SHA-256, not names alone. Two missing generated ledgers were added to reset scope.

The reusable corrected source is `audit_template/runtime_v2/reset_audit.py`;
Enconet's local copy matches it. The committed v2 payload remains immutable.
Other vendor resets need this correction in a future reviewed release before use;
their existing folders were not silently patched during this operation.

Commands and integer exit codes:

| Check/action | Command | Exit and result |
|---|---|---|
| Safety regression | `python -m pytest audit_template/tests/test_reset_archive_safety.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/enconet-reset-safety-20261007-a` | 0; two tests passed: read-only deletion and corrupt archive refusal |
| Reset preview | `python Enconet/scripts/reset_audit.py --plan reset-plans/enconet-reset-20261007-reviewed.json` | 0; 352 delete, six truncate, incoming excluded |
| Backed-up reset | `python Enconet/scripts/reset_audit.py --apply --plan reset-plans/enconet-reset-20261007-reviewed.json --backup-dir audit_archives/Enconet/2026-10-07 --confirm RESET-AUDIT` | 0; archive created, 352 deleted, six truncated |
| Fresh database | `python Enconet/scripts/init_db.py` | 0; initialized |
| Status (from Enconet) | `python scripts/audit_command.py audit-status` | 0; setup, all gates pending, zero open actions |
| Aggregate (from Enconet) | `python scripts/run_all_validations.py --no-record` | 0; setup structure passed; later-phase checks explicitly skipped |

An independent post-reset check re-read every archived entry and all incoming
hashes, and compared the protected-file hash snapshot: no differences.

## Next action

Review incoming sources and regulatory editions, then prepare fresh controlled
intake and local v3 calibration. Preserve incoming originals: Enconet's legacy
promotion command moves them, so a preservation-safe intake path must be reviewed
before registration. Old active-prompt configuration is preserved as history;
it is not approved for this cycle. No ingestion or sieving has yet run.
