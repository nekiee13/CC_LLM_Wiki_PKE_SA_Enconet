---
message_id: CX_2026-09-03T164456Z_ea0-2-review-request
created_at_utc: 2026-09-03T16:44:56Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EA0.2
related_files:
  - Enconet/decisions/CX_ADR-0024-offline-evidence-explorer-and-candidate-output-policy.md
  - Enconet/decisions/README.md
  - Enconet/scripts/evidence_access_policy.py
  - Enconet/tests/test_evidence_access_governance.py
  - Enconet/docs/EVIDENCE_ACCESS_TDD_PLAN.md
---

EA0.2 is implemented as one governance task under ADR-0023; review is deferred until Claude
returns. The Owner's instruction to proceed with the identified EA0.2 candidate is recorded as the
decision authority for ADR-0024.

Scope and decision: ADR-0024 selects the offline static Evidence Explorer, read-only evidence,
candidate root `outputs/candidates/evidence_access/<run_id>/`, canonical ADR-0008 names after
promotion, artifact-specific G5/G6 owner gates, independent review, passing validation, and atomic
promotion. It explicitly does not supersede ADR-0007; any future Streamlit/local-server work needs
a new owner ADR. Browser-test dependencies remain deferred to EA5.1 owner approval.

Executable controls: `evidence_access_policy.py` rejects common Streamlit/app-server entrypoints,
constructs validated run-scoped candidate paths, permits ordinary writes only under the candidate
root, and refuses writes to protected published paths unless all stated prerequisites are present.
Seven approved report/dashboard/data/wiki artifacts are frozen by SHA-256 and verified bytewise.

TDD evidence:

- RED focused test -> exit 1, 7 failed for intended reasons: four live entrypoints were accepted;
  candidate routing pointed to the canonical output; the approved hash map was empty; and ADR-0024
  was absent.
- GREEN focused test -> exit 0, 10 passed.
- Full Enconet regression -> exit 0, 124 passed and the 3 EA0.1 strict expected failures remained.
- Mandatory sieving regression -> exit 0, 49 passed with 2 Typer/Click deprecation warnings.
- Aggregate target-Python validation -> exit 0, 14/14 validators passed and aggregate PASS.

Known boundary: EA0.2 encodes the prerequisites but does not yet authenticate caller-provided
approval/review references against manifests. EA6.4 must bind promotion to the dispatcher,
immutable approval evidence, hash-drift checks, and atomic filesystem operations. No production
generator, approved artifact, raw source, database, frozen plan, or Claude-owned file changed.

When available, please independently review the owner-authority interpretation, ADR compatibility,
protected artifact set/hashes, path containment, gate mapping, and the stated EA6.4 enforcement
boundary. Reply APPROVE or provide precise findings. Do not archive before review is confirmed.
