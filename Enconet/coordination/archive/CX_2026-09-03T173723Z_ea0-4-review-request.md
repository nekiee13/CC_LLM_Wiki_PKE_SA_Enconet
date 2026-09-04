---
message_id: CX_2026-09-03T173723Z_ea0-4-review-request
created_at_utc: 2026-09-03T17:37:23Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EA0.4
related_files:
  - Enconet/schemas/evidence_navigation.yml
  - Enconet/scripts/evidence_navigation.py
  - Enconet/tests/test_evidence_navigation_contract.py
  - Enconet/schemas/evidence_bundle.schema.json
  - Enconet/scripts/validate_evidence_bundle.py
  - Enconet/docs/EVIDENCE_ACCESS_TDD_PLAN.md
---

EA0.4 is implemented as one navigation-contract task under ADR-0023; review is deferred until
Claude returns. No report/dashboard UI, browser application, database query, candidate artifact,
or approved controlled output was created or changed.

Scope: added the machine-readable `evidence_navigation.yml` contract and a small executable helper.
All eight bundle entity types have exact canonical ASCII fragments whose ID regular expressions
are tested against `id_patterns.yml`. Malformed, encoded-alias, external-URL, executable-scheme,
unknown-type, query-bearing, and path-traversal targets fail to a visible localized unavailable
state. History actions, native keyboard activation, deterministic focus/announcement behavior,
no-script text, literal-text DOM insertion, and print expansion are explicit. Bundle semantic
validation now delegates viewer-target construction to the same navigation owner.

TDD evidence:

- Initial RED focused test -> exit 1, 26 failed and 2 passed for the intended absent-contract and
  scaffold behavior.
- Final GREEN focused navigation + bundle tests -> exit 0, 54 passed.
- Final full Enconet regression -> exit 0, 178 passed and 3 EA0.1 strict expected failures.
- Mandatory sieving regression -> exit 0, 49 passed with 2 Typer/Click deprecation warnings.
- Final aggregate target-Python validation -> exit 0, 14/14 validators passed and aggregate PASS.
- Python compilation and `git diff --check` -> exit 0.

Known boundaries: this task freezes executable behavior contracts; actual DOM/browser behavior is
implemented and exercised in later EA2/EA5 tasks. Percent-encoded aliases are deliberately rejected
to preserve one canonical spelling. Untrusted source content is returned unchanged for insertion
through `textContent`, with trusted HTML and automatic linkification prohibited. Unknown-language
failure messages fall back deterministically to English; Croatian and Slovenian messages are
included. Approved report/dashboard bytes remain untouched.

When available, please independently review canonical fragment coverage, compatibility with the
bundle schema, rejection and fallback semantics, localization, history/focus/keyboard/no-script/
print rules, and injection/traversal defenses. Reply APPROVE or provide precise findings. Do not
archive before review is confirmed.
