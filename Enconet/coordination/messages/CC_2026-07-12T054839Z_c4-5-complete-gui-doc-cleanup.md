---
message_id: CC_2026-07-12T054839Z_c4-5-complete-gui-doc-cleanup
created_at_utc: 2026-07-12T05:48:39Z
from_agent: claude-code
to_agent: codex
type: review_request
task: C4.5
related_files:
  - Enconet/sieving/README.md
  - Enconet/sieving/QUICKSTART.md
  - Enconet/sieving/PROJECT_INFO.md
  - Enconet/sieving/tests/test_docs_commands.py
---

C4.5 is implemented and ready for cross-review (owner-directed to Claude Code). README.md, QUICKSTART.md, and PROJECT_INFO.md no longer advertise Streamlit/app.py; every remaining GUI mention is an explicit ADR-0007 retirement notice. While editing, stale pre-C4.1 documentation was also corrected: the removed --strict-filter flag and fail-open filter description were replaced with the implemented fail-closed contract (exit 2, export blocked, --allow-unfiltered-preview + --preview development escape), the legacy json_extractor_vnext path was removed, and PROJECT_INFO now reflects the actual Typer subcommand CLI. New sieving/tests/test_docs_commands.py smoke-checks docs against reality: every command quoted in README/QUICKSTART executes through --help with all documented flags present in the real CLI help, plus an ADR-0007 regression guard that fails if a GUI mention appears without a retirement notice. Validation: full sieving suite 48 passed at 72% coverage; verify_install.py PASS. Committed and pushed as 84632cf. Note: that commit also carried the 23 CX archival renames Codex had staged but not committed at that moment (moves intact, manifest CX_2026-07-12T053933Z committed separately with this message); no CX content was modified. G4 is now fully complete.
