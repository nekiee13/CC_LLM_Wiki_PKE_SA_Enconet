---
message_id: CX_2026-09-30T194707Z_taxonomy-neutral-sieving-runtime-review
created_at_utc: 2026-09-30T19:47:07Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EK-1.2
related_files:
  - audit_template/sieving/v1/sieving/src/json_extractor/contract.py
  - audit_template/sieving/v1/sieving/src/json_extractor/extract/load_and_flatten.py
  - audit_template/sieving/v1/sieving/src/json_extractor/crumb_validation.py
  - audit_template/sieving/v1/schemas/sieving_contract.yml
  - Ekonerg/docs/transfer/EK_1_2_NEUTRAL_SIEVING_RUNTIME.md
---

Please review commit 9ed9521 and its EK-1.2 evidence. This is a runtime-only neutrality candidate: contract.py resolves a configured local taxonomy file and rejects absent, foreign, mismatched, empty, or duplicate criteria; extraction checks local template/taxonomy identity; crumb validation uses the same canonical contract. TDD red showed both synthetic non-APP_B queries blocked, a foreign path accepted, and wrong template identity accepted; green suites: 21 bootstrap, 86 sieving, 40 Ekonerg scripts, 111 tools. Transfer verify still pins 9f20430. Live sieving preview/apply preserved 21 files, setup LF preview/apply preserved 10; incoming 31 untouched, no DATA, DB, or project state. Critical LIMIT: the v1 bundle and Ekonerg config still include/select Appendix B; README warns v1 is not a clean company-neutral bootstrap. This slice does not authorize intake or close EK-1.2. Please review path guards, fail-closed behavior, hashes/journals, and whether the remaining source-specific config should be removed in the next task. Owner clarification on Ekonerg applicability is pending.
