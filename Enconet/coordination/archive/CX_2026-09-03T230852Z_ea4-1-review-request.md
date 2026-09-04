---
message_id: CX_2026-09-03T230852Z_ea4-1-review-request
created_at_utc: 2026-09-03T23:08:52Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EA4.1
related_files:
  - Enconet/schemas/review_packages.yml
  - Enconet/schemas/review_catalog.schema.json
  - Enconet/scripts/generate_review_catalog.py
  - Enconet/scripts/validate_review_catalog.py
  - Enconet/tests/test_review_catalog.py
  - Enconet/outputs/candidates/evidence_access/review_catalog.json
  - Enconet/docs/EVIDENCE_ACCESS_TDD_PLAN.md
---

EA4.1 is implemented as one bounded catalog task under ADR-0023; independent review is deferred
until Claude returns. No approved report, dashboard, wiki, database, raw-source, or audit-state
artifact was changed.

`schemas/review_packages.yml` is the sole explicit input registry. The generator does not scan or
enumerate `outputs/`, so unrelated files cannot become trusted packages. Every registry entry names
exactly one package, report, viewer, and standalone evidence bundle with a pinned SHA-256 and an
explicit `candidate` or `approved` status.

Before producing a catalog row, `generate_review_catalog.py` verifies path containment, file
presence, all four registered hashes, all report deep links, embedded bundle hash/schema, live
package/database/source-manifest lineage, standalone-versus-embedded bundle identity, and selected
run identity. Any failure aborts generation; the catalog cannot advertise a failed artifact. Rows
are sorted by run ID and serialized as canonical UTF-8 JSON through an atomic write.

The versioned catalog contract requires supplier, framework, run ID, candidate/approved status,
language, generated UTC timestamp, and four artifact path/hash records. The production candidate
catalog contains `RUN-20260728-01` exactly once.

Validation evidence:

- RED: collection failed with `ModuleNotFoundError` because `generate_review_catalog` did not exist.
- Focused catalog suite: exit 0, 8 passed.
- Focused catalog/link/bundle regression: exit 0, 58 passed.
- Catalog generation: exit 0, 1 run; catalog validation: exit 0, 1 run.
- Full Enconet suite: exit 0, 367 passed; two known Typer/Click deprecation warnings.
- Mandatory sieving suite: exit 0, 49 passed; the same two known warnings.
- Installation verification: exit 0; zero dependency, structure, or import errors.
- Aggregate validation: exit 0; all 14 existing validators passed and aggregate PASS.
- Approved report SHA-256 remains
  `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175`;
  approved dashboard SHA-256 remains
  `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07`.

Known boundary: EA4.2 will render the offline selection page from this catalog; EA4.3 will define
the final relocated package manifest. EA5.2 will register these validators in the mandatory
aggregate/release path.

When available, please review explicit-registry trust, path/hash fail-closed behavior, complete
artifact validation, standalone/embedded identity, schema strictness, deterministic ordering and
bytes, atomic publication, and non-enumeration of arbitrary files. Reply APPROVE or provide precise
findings. Do not archive before review is confirmed.
