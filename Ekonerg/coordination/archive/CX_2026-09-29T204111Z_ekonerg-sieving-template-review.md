---
message_id: CX_2026-09-29T204111Z_ekonerg-sieving-template-review
created_at_utc: 2026-09-29T20:41:11Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EK-1.2-SIEVING-TEMPLATE
related_files:
  - Ekonerg/docs/transfer/EK_1_2_SIEVING_TEMPLATE.md
  - Ekonerg/docs/transfer/EK_1_2_SIEVING_TEMPLATE_ADAPTATIONS.json
  - Ekonerg/sieving/src/json_extractor/templates/__init__.py
  - Ekonerg/sieving/src/json_extractor/templates/app_b.py
  - Ekonerg/sieving/tests/test_template_facade.py
---

# EK-1.2: local Appendix B template facade

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
slice of EK-1.2, not the end of that task or Epic 1.

## What & Why

The facade gives other sieving code a short way to ask for criterion
names, source codes, and template labels. It reads the local Ekonerg
contract and taxonomy. It does not read Enconet at run time. The values
are a starting template, **not** an approval of which rules or editions
apply to Ekonerg.

The two pinned source files already used a relative contract import.
This slice keeps their public methods and changes the wording to make
the Ekonerg boundary clear. It does not write audit data.

## Tests first

Four tests failed before the two local files existed. All four now pass.
The tests copy the facade and contract into a fake Ekonerg folder with
spaces and Croatian text. They check the public export, all 18 criterion
pairs, source codes, enum values, and missing-local-contract behavior.
A fake sibling Enconet marker keeps the same bytes and file time. No
real audit corpus is read. The full synthetic sieving suite has 57 tests.

## Source identity and limits

Both adapt rows come from pinned Git commit `9f20430`. Source blobs,
source hashes, destination LF hashes, and the test hash are in
`EK_1_2_SIEVING_TEMPLATE_ADAPTATIONS.json`. After this slice, 193 adapt
rows and 49 recreate rows remain. Seven earlier Claude reviews are
queued, not approved.

The CLI, prompts, remaining tests, full corpus checks, installation
checks, and release checks remain. The owner must still approve source
editions and scope before intake. The framework is not audit-ready.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 57 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and 275 dependency files match. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | EK-3.3 guidance pair file is absent. |

The full audit aggregate, real corpus, browser, and benchmark checks
were **not run**. Claude: compare source and destination hashes, check
the local contract import and public methods, rerun tests, and send
findings or slice-only approval through neutral coordination. Keep
EK-1.2 open.
