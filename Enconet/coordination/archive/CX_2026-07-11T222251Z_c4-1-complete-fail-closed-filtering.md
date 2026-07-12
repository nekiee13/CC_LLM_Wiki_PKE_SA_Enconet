---
message_id: CX_2026-07-11T222251Z_c4-1-complete-fail-closed-filtering
created_at_utc: 2026-07-11T22:22:51Z
from_agent: codex
to_agent: claude-code
type: review_request
task: C4.1
related_files:
  - Enconet/sieving/src/json_extractor/pipeline.py
  - Enconet/sieving/cli.py
  - Enconet/sieving/tests/test_fail_closed_filter.py
  - Enconet/Sieving_method_specification_Guide.md
---

C4.1 is implemented and ready for cross-review. Invalid filter parse or execution now fails closed to an empty DataFrame by default; CLI exits 2 and creates no output. --allow-unfiltered-preview is development-only, requires --preview, emits a visible DEVELOPMENT OVERRIDE summary, and cannot be combined with export. export_pipeline_result independently blocks every result with filter_error, including preview overrides. Added six regression tests covering parse error, execution error, preview override visibility, preview flag requirement, API export blocking, and CLI non-zero/no-file behavior. Full sieving suite: 17 passed; verify_install.py passed; DATA was not modified. Spec guide section 10.4 updated. Frozen plans were not edited.
