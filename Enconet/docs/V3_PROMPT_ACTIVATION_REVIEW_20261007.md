# Enconet v3 readiness and activation decision

## Owner golden approval recorded

The owner approved the 20 expected Nuclear QA Plan examples under
`GOLDEN-ENCONET-NP-V3-20261007`. The expected statements, criterion mappings and
exact quotes are unchanged. Approval status/reference were recorded separately
from applicability, prompt activation, generation promotion and audit results.

## Storage compatibility resolved

The optional v3 context now has a lossless path through validation, import and
retrieval, using the existing Ekonerg-style `crumb_context` model:

- Evidence type; project, contract and supplier references; source revision;
  and evidence date.
- Unknown fields, invalid types and invalid dates fail instead of disappearing.
- Missing optional anchors remain NULL; no project or date is invented.
- Core crumbs and context commit or roll back together.
- Old JSON without context remains compatible.

The new table was added only after preview and regression tests. The CLI target
is guarded by local project paths. A SQLite backup was created before apply:
`db/backups/nqa_audit-20261007T161644Z.sqlite.bak`.

Every pre-existing table's data hash matched before and after migration. The
33 source rows and 922 chapter rows are unchanged. The new context table is
empty, as are live crumbs and evaluation results. Incoming hashes remain intact.

Migration provenance:
`out/2026-10-07/fresh-intake/context-storage-migration.json`.

## Isolated calibration engineering check

`scripts/verify_v3_calibration.py` copied the live database into a fresh local
output folder, imported the approved manual examples there, linked quotes and
checked stored context. It never imported into the live database.

Results:

- 20 example crumbs in the diagnostic copy only.
- 20 exact same-document chapter links; no linking exceptions.
- Evidence type and revision context retained for every example.
- Run metrics generated for the diagnostic copy.
- Live database SHA-256 unchanged during the check.

Report: `out/2026-10-07/v3-calibration-check/report.json`.

This is an engineering test of owner-reviewed manual examples, not an
independent semantic prompt execution or a measured full-corpus recall score.
The earlier draft self-check remains historical and is not relabeled as a new
prompt run. Do not count these diagnostic crumbs as active vendor evidence.

## Validation

- Initial TDD: `python -m pytest Enconet/tests/test_v3_context_storage.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/enconet-context-tdd-20261007-a`, exit 1: five expected failures before the fix.
- Final regression: `python -m pytest Enconet/tests/test_v3_context_storage.py Enconet/tests/test_epic5_sieving.py Enconet/tests/test_db_backbone.py Enconet/tests/test_validate_schemas.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/enconet-context-final-20261007-a`, exit 0: 23 passed.
- Migration preview/apply/re-preview: `python Enconet/scripts/migrate_db.py`; `python Enconet/scripts/migrate_db.py --apply`; `python Enconet/scripts/migrate_db.py`, each exit 0. First plan was only create crumb_context; final plan has no actions.
- Isolated round-trip: `python Enconet/scripts/verify_v3_calibration.py --output out/2026-10-07/v3-calibration-check`, exit 0.
- Aggregate: `python Enconet/scripts/run_all_validations.py --no-record`, exit 0; four checks passed at chunked, later-phase checks skipped.

## Activation choice

The active DOCUMENT selector still names v1. The proposed next action is:

**Activate `appb_document_v3_context_anchors` for this Enconet cycle and begin
full vendor sieving using direct-control and quality-intent passes.**

Keep exact quotes, chapter links, broad recall and unmatched-block review.
The 20 approved examples are a calibration sample, not a crumb quota. The XIII
scope claim remains evidence for a later applicability decision, not automatic
N/A. Parts 2-4 remain supporting material with known conversion warnings.

Owner activation approval is not yet recorded. After approval, record the
selector/CHANGELOG/skill lesson changes and execute real document sieving under
new run IDs. No score or applicability approval is implied by activation.

Claude review is deferred, not claimed complete. Reusable backport sources are
documented in `audit_template/runtime_v2/CONTEXT_BACKPORT.md`; immutable v2 and
other company projects were not changed.
