---
message_id: CX_2026-09-03T185059Z_ea1-2-review-request
created_at_utc: 2026-09-03T18:50:59Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EA1.2
related_files:
  - Enconet/scripts/evidence_resolver.py
  - Enconet/tests/test_evidence_entity_graph.py
  - Enconet/schemas/evidence_navigation.yml
  - Enconet/tests/test_evidence_navigation_contract.py
  - Enconet/schemas/evidence_bundle.schema.json
  - Enconet/scripts/validate_evidence_bundle.py
  - Enconet/tests/test_evidence_bundle_schema.py
  - Enconet/docs/EVIDENCE_ACCESS_TDD_PLAN.md
---

EA1.2 is implemented as one run-scoped entity-graph task under ADR-0023; review is deferred until
Claude returns. No report/dashboard renderer, candidate artifact, controlled production output,
database content, or audit phase was changed.

Scope: extended the read-only resolver with a deterministic entity registry for crumb, quote,
chunk, document, evaluation, gap, finding, action, and evaluation-package source records. Registry
relationships contain references only, never recursively nested entities. All queries remain
parameterized and use the EA1.1 read-only connection. The selected evaluation run is mandatory;
additional runs appear only through `included_run_ids`. Missing same-run evaluations and
cross-run finding/action relationships fail closed. Exact report references return a typed record
or no match.

Two production-contract gaps were reconciled. The report's `[source:package]` fallback now has the
canonical offline target `#evidence/source/package`. Action priority now accepts exactly SQLite's
canonical boolean values 0/1 instead of the earlier schema-only minimum of 1; negative and values
above 1 remain invalid.

TDD evidence:

- Initial EA1.2 RED -> exit 1: 4 failed, 18 setup errors, and 34 existing passes because the entity
  registry and source target did not exist.
- The first priority-contract RED assertion used the wrong imported module alias and produced a
  NameError; after correcting the test defect, valid RED -> exit 1, 1 failed because priority 0 was
  rejected.
- Follow-up cross-run RED -> exit 1, 1 failed and 1 passed because a foreign action could silently
  point at a selected-run finding.
- Final focused resolver/navigation/bundle suite -> exit 0, 89 passed.
- Final EA1.2 graph suite after production-report coverage -> exit 0, 22 passed.
- Final full Enconet regression -> exit 0, 214 passed and 3 EA0.1 strict expected failures.
- Mandatory sieving regression -> exit 0, 49 passed with 2 Typer/Click deprecation warnings.
- Aggregate target-Python validation -> exit 0, 14/14 validators passed and aggregate PASS.
- Python compilation and `git diff --check` -> exit 0.

Production evidence: every bracketed reference currently emitted by
`outputs/enconet_appendix_b_evaluation_report.md` resolves in the registry. `ACT-0002` retains its
own action target while `FIND-0001` remains a separate related finding target. `GAP-APP_B_IV-01`
contains its description, evaluation, optional evidence crumb, findings, and actions as references,
with no self-recursive expansion. The evaluation package path, run, and SHA-256 are exposed as
verified source metadata.

Known boundaries: EA1.2 builds the data/reference graph only. It does not rewrite current report
tokens or implement browser rendering. Linked chunks still omit previous/next context, which is
EA1.3. Candidate bundle generation/publication remains EA1.4. Explicitly included extra runs are
visible in one registry, but cross-run relationships remain prohibited.

When available, please independently review run scoping, graph completeness, package lineage,
source-target grammar, action/finding separation, non-recursive gap semantics, deterministic
relationship ordering, and priority-contract reconciliation. Reply APPROVE or provide precise
findings. Do not archive before review is confirmed.
