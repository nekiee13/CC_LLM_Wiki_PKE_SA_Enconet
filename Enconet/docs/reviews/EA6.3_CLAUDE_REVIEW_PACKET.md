# EA6.3 independent Evidence Access review packet

Review ID: `EA6.3-RUN-20260728-01`

Reviewer: Claude Code

Reviewer decision: **APPROVED**

Claude approved the prior corrected viewer and later approved the promotion guardrails. The Owner
then requested the corresponding source chapter on every displayed quote. Codex added that
presentation using the already linked chunk `heading_path`, rebuilt the sealed candidate, and
reopened Owner UAT because the artifact fingerprints changed. Claude must now perform a focused
re-review of these exact bytes and publish a new immutable `CC_` decision. Claude must execute these checks independently.
Codex must not complete the reviewer decision.

## Fixed review boundary

- Correction base: `3a44479c7a083366683bc81652b6916c8807e542`
- Correction tip: `1dcc54f4886f7d267b37ffb4643b2569688ce48d`
- Production run: `RUN-20260728-01`
- Portable manifest: `f3b72fdd381453af69b97e8d6e423c749fdbe045f3b0a55e8c7d43fc22faa95d`
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
git diff 3a44479c7a083366683bc81652b6916c8807e542 1dcc54f4886f7d267b37ffb4643b2569688ce48d -- .
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

Codex must not complete the reviewer decision itself.

- Decision: **APPROVE**
- Reviewed at UTC: `2026-09-04T21:39:22Z`
- `CC_` message ID: `CC_2026-09-04T213922Z_chapter-reference-approve-with-observation`
- Reproduced results: full suite 421 passed; sieving suite 49 passed; aggregate 21/21 PASS;
  focused suite 39 passed; live chapter labels and exact candidate fingerprints verified.
- Findings: none.

### Non-blocking observation

Claude observed that the defensive cross-document quote check inside the `quotes.forEach` callback
cannot exit the enclosing `renderEvidenceCrumb` function. The validated resolver rejects such a
cross-document bundle before rendering, so the branch is unreachable for pipeline-produced
artifacts and does not block this approval. Preserve the approved bytes for UAT and promotion;
address the dead defensive branch as a separately tested hardening change after this release.

Approval requires no unresolved high/medium finding. Any correction must begin with a failing
regression test and receive re-review before EA6.3 is closed.
