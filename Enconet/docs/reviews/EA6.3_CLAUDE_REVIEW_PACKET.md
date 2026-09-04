# EA6.3 independent Evidence Access review packet

Review ID: `EA6.3-RUN-20260728-01`

Reviewer: Claude Code

Reviewer decision: **AWAITING CLAUDE**

Codex prepared this packet but cannot perform the independent review.
Claude must execute these checks independently, inspect the implementation rather than trusting prior summaries, and publish
an immutable `CC_` approval or findings record. Codex must not complete the reviewer decision.

## Fixed review boundary

- Implementation base: `34c6351dcf32277b4c5057eda187edb50e3e086d`
- Implementation tip: `e6713769c0206322ab3c31555a77a1ad46600927`
- Production run: `RUN-20260728-01`
- Portable manifest: `efcbada9b59862f8f0ba00c739147a2a5e4076d0009f87b3af539a5cb60a0012`
- Approved report: `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175`
- Approved dashboard: `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07`
- Expected: six package files, one run, 18 criteria, 62 crumbs, and 200 report evidence links.

Later packet-preparation commits are not part of the implementation diff. Review any such commit
only to verify that this protocol accurately describes the pinned implementation tip.

## Independent commands

Run from the Enconet root. Preserve complete outputs or durable summaries with commands, exit codes,
counts, warnings, failures, and artifact paths.

<!-- review-command:implementation-diff -->
```powershell
git diff 34c6351dcf32277b4c5057eda187edb50e3e086d e6713769c0206322ab3c31555a77a1ad46600927 -- .
```

<!-- review-command:validate-candidate -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\validate_evidence_access_candidate.py --contract schemas\evidence_access_release_candidate.yml --project-root .
```

<!-- review-command:validate-documentation -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\validate_evidence_access_docs.py --contract schemas\evidence_access_operations.yml --operations docs\EVIDENCE_ACCESS_OPERATIONS.md --architecture docs\EVIDENCE_ACCESS_ARCHITECTURE.md --upgrade docs\EVIDENCE_ACCESS_UPGRADE_GUIDE.md --project-root .
```

<!-- review-command:full-tests -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' -m pytest -q -p no:cacheprovider
```

<!-- review-command:sieving-tests -->
```powershell
Push-Location sieving; & 'C:\xPY\vEnv\WikiEnconet\python.exe' -m pytest -q -p no:cacheprovider; Pop-Location
```

<!-- review-command:verify-install -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' sieving\verify_install.py
```

<!-- review-command:aggregate -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\audit_command.py audit-validate -- --no-record
```

Replace the browser artifact placeholder with a new empty review directory.

<!-- review-command:browser -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\browser_harness.py check outputs\candidates\evidence_access\portable_package\RUN-20260728-01\evidence_explorer.html --artifacts <REVIEW_ARTIFACT_DIRECTORY> --require-interactive
```

## Mandatory risk review

For each item, inspect code and tests, then mark Pass, Finding, or Not applicable with evidence.

<!-- risk-check:database-read-only -->
### Database read-only

Resolver is read-only/query-only and does not mutate SQLite.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:evidence-lineage -->
### Evidence lineage

Run, document, source, crumb, quote, and chunk identities remain exact.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:report-deep-links -->
### Report deep links

All report entity links open the intended portable viewer target.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:browser-behavior -->
### Browser behavior

Deep links, history, focus, keyboard, search, copy, print, and context work.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:hostile-text -->
### Hostile and multilingual text

Source text cannot execute as HTML or script and Unicode round-trips exactly.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:zero-network -->
### Zero network

Browser review makes no external request.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:safe-paths -->
### Safe paths

Catalog, manifest, contract, and output paths cannot escape their roots.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:deterministic-package -->
### Deterministic package

Clean rebuild reproduces the pinned package manifest and stable counts.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:controlled-outputs -->
### Controlled outputs

Candidate work does not rewrite the approved report or dashboard.

Result: __________ Evidence: ________________________________________________

<!-- risk-check:governance -->
### Governance

Owner UAT is distinct from independent review and promotion remains blocked.

Result: __________ Evidence: ________________________________________________

## Reviewer decision

Claude completes this section in a new immutable `CC_` message, not by editing this Codex packet.

- Decision: APPROVE / FINDINGS
- Reviewed at UTC: ____________________
- `CC_` message ID: ____________________
- Reproduced commands and results: ____________________
- Findings with severity, file/line, evidence, and required correction: ____________________

Approval requires no unresolved high/medium finding. Any correction must begin with a failing
regression test and receive re-review before EA6.3 is closed.
