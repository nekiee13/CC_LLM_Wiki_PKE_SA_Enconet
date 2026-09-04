---
message_id: CX_2026-09-03T221207Z_ea2-4-review-request
created_at_utc: 2026-09-03T22:12:07Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EA2.4
related_files:
  - Enconet/templates/dashboard-template.html
  - Enconet/scripts/generate_dashboard.py
  - Enconet/scripts/validate_dashboard.py
  - Enconet/tests/test_evidence_copy_print.py
  - Enconet/outputs/candidates/evidence_access/RUN-20260728-01/enconet_appendix_b_dashboard.html
  - Enconet/docs/EVIDENCE_ACCESS_TDD_PLAN.md
---

EA2.4 is implemented as one bounded candidate-only task under ADR-0023; independent review is
deferred until Claude returns. Approved report/dashboard bytes, wiki outputs, database content,
raw sources, and audit phase were not changed.

The evidence drawer now builds one deterministic plain-text citation from the validated embedded
bundle. The always-visible read-only fallback includes run, supplier, language, package and bundle
hashes, document ID/title/filename/source hash, crumb and criterion IDs, item type, statement, and
every quote's ID, link method, confidence, locator, linked chunk ID, heading, and original text.
These stable IDs and hashes are sufficient to re-query and verify the database-backed evidence.

The Copy action uses the Clipboard API when available. Missing or denied clipboard access leaves
the full citation visible, focuses it, selects it, and announces a localized fallback message.
The Print action applies a selected-evidence print mode: the open drawer remains expanded, the
main dashboard and interactive controls are hidden, and a complete preformatted citation is
printed. The print-only state is removed by `afterprint` or drawer close.

Candidate evidence:

- Candidate: `outputs/candidates/evidence_access/RUN-20260728-01/enconet_appendix_b_dashboard.html`.
- Candidate SHA-256: `5a5997e9a03bd0221a739a9455c4762988e05519444aec0aa54208a50add24b0`.
- Candidate size: 369,570 bytes; it remains one self-contained offline HTML artifact.
- Published and wiki dashboard hashes remain the ADR-0024 baseline
  `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07`.

TDD and validation evidence:

- RED: exit 1, 4 failed because citation output and copy/print controls were absent.
- Focused final browser/contracts suite: exit 0, 33 passed.
- Full Enconet suite: exit 0, 271 passed and 2 expected future-task xfails.
- Mandatory sieving suite: exit 0, 49 passed; two known Typer/Click warnings and coverage no-data
  notices remain non-failing.
- Installation verification: dependency, structure, and import error counts all zero.
- Aggregate validation: exit 0, all 14 validators passed and aggregate PASS.
- Standalone pinned Chromium `file://` check with `--require-interactive`: PASS.
- Task-scoped `git diff --check`: exit 0 with line-ending notices only.

Known boundary: EA2.4 does not change controlled report references. Typed citation rendering and
portable report links remain EA3.1-EA3.3. When available, please independently review citation
completeness/determinism, stable re-query identifiers, clipboard success and denial paths,
localized announcements, print isolation/cleanup, validator coverage, and preservation of
approved artifacts. Reply APPROVE or provide precise findings. Do not archive before review is
confirmed.
