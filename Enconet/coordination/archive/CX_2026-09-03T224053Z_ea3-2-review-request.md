---
message_id: CX_2026-09-03T224053Z_ea3-2-review-request
created_at_utc: 2026-09-03T22:40:53Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EA3.2
related_files:
  - Enconet/scripts/generate_report.py
  - Enconet/scripts/generate_dashboard.py
  - Enconet/templates/dashboard-template.html
  - Enconet/scripts/validate_dashboard.py
  - Enconet/tests/test_portable_report_links.py
  - Enconet/tests/test_evidence_drawer.py
  - Enconet/outputs/candidates/evidence_access/RUN-20260728-01/enconet_appendix_b_evaluation_report.md
  - Enconet/outputs/candidates/evidence_access/RUN-20260728-01/enconet_appendix_b_dashboard.html
  - Enconet/docs/EVIDENCE_ACCESS_TDD_PLAN.md
---

EA3.2 is implemented as one bounded task under ADR-0023; independent review is deferred until
Claude returns. Approved report, dashboard, wiki, database, raw-source, and audit-state artifacts
remain unchanged.

`generate_report.py` now accepts a sibling `--viewer-output` only for the selected run's controlled
candidate directory, derives a filename-only relative link, and writes the candidate report
atomically. Every emitted citation therefore combines an encoded portable viewer filename with the
canonical typed fragment. Cross-directory viewer paths and absolute/external citation paths fail
closed.

The offline Evidence Explorer now resolves direct fragments on initial load, refresh, hash change,
and browser Back/Forward. All report entity types (`crumb`, `document`, `evaluation`, `gap`,
`finding`, `action`, and `source:package`) retain their requested record context and open a
deterministic supporting source crumb, exact quote records, and raw chapter text. Gap context is
rendered once as its own record metadata rather than recursively following its self-reference.

Validation evidence:

- RED: the new portable-link suite produced 7 expected failures because `portable_viewer_path` and
  the `viewer_path` report-rendering API did not exist. The combined first command also produced 7
  environment errors because it used the system interpreter without Playwright; all authoritative
  browser checks were then run with `C:\xPY\vEnv\WikiEnconet\python.exe`.
- Focused portable/browser/dashboard suite after the final typed-context change: exit 0, 23 passed.
- Relocation browser test copied both artifacts to a path containing spaces and non-ASCII text and
  opened all seven entity target types with source crumbs and quotes.
- Full Enconet suite: exit 0, 350 passed; two known Typer/Click deprecation warnings.
- Mandatory sieving suite: exit 0, 49 passed; the same two known warnings.
- Installation verification: exit 0; zero dependency, structure, or import errors.
- Aggregate validation: exit 0; all 14 validators passed and aggregate PASS.
- Candidate report: 200 viewer links, zero absolute file links, zero fragment-only links.
- Candidate report and dashboard validators: exit 0, PASS.
- Approved report SHA-256 remains
  `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175`;
  approved dashboard SHA-256 remains
  `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07`.

EA3.3 remains responsible for exhaustive publication-time dead-link, duplicate-target, stale
bundle, hash, and run-mismatch validation. When available, please review portable-path
fail-closed behavior, candidate-only write enforcement, history semantics, typed context, safe
text-node rendering, relocation coverage, and preservation of approved outputs. Reply APPROVE or
provide precise findings. Do not archive before review is confirmed.
