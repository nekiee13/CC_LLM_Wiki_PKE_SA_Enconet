# Optional v3 context backport

Enconet now uses the same optional `crumb_context` storage model as Ekonerg:
evidence_type plus project_ref, contract_ref, supplier_ref, source_revision and
evidence_date. These are source anchors, not new audit ratings or requirements.

Implementation source for the next versioned release:

- `Enconet/sieving/src/json_extractor/evidence_context.py`: contract validation.
- `Enconet/sieving/src/json_extractor/crumb_validation.py`: validation wiring.
- `Enconet/scripts/import_crumbs.py`: transactional context storage.
- `Enconet/db/schema.sql`: fresh-database table.
- `Enconet/scripts/migrate_db.py`: preview, local CLI target guard and backup.
- `Enconet/schemas/evidence_context.yml`: existing optional field contract.
- `Enconet/tests/test_v3_context_storage.py`: round-trip and rollback tests.

Missing optional anchors remain missing. Unknown keys are rejected rather than
silently discarded. No new record, date or identity may be invented to satisfy
an import. This intentionally avoids treating every policy passage as if it
must name a project or contract.

The committed v2 payload and other vendor projects are unchanged. Merge this
backport into a new versioned release and run company-neutral isolation tests
before deploying it elsewhere; do not patch the immutable v2 payload.
