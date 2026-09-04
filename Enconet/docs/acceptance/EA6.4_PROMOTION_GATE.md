# EA6.4 Evidence Access promotion gate

Gate status: **PROMOTED**

Release: `EA6.4-RUN-20260728-01`

The chapter-reference candidate passed renewed Owner UAT and independent Claude review. The Owner
explicitly approved both G5 and G6 Evidence Access decisions, and the controlled transaction
replaced the five protected canonical report/dashboard copies. This does not authorize a live service and does
not modify the closed audit findings, score, source evidence, or database.

## Exact candidate

- Production run: `RUN-20260728-01`
- Portable-package manifest SHA-256:
  `f3b72fdd381453af69b97e8d6e423c749fdbe045f3b0a55e8c7d43fc22faa95d`
- Published report SHA-256 after promotion:
  `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94`
- Published dashboard SHA-256 after promotion:
  `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d`
- Owner UAT: approved at `2026-09-04T21:52:04Z` for these exact fingerprints.
- Independent review: approved in `CC_2026-09-04T213922Z_chapter-reference-approve-with-observation`.

## Exact replacement set

| Protected destination | Current SHA-256 | Proposed SHA-256 |
| --- | --- | --- |
| `outputs/enconet_appendix_b_evaluation_report.md` | `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175` | `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94` |
| `outputs/enconet_appendix_b_evaluation_report_hr.md` | `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175` | `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94` |
| `outputs/enconet_appendix_b_dashboard.html` | `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07` | `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d` |
| `outputs/enconet_appendix_b_dashboard_hr.html` | `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07` | `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d` |
| `wiki/dashboards/enconet_appendix_b_dashboard.html` | `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07` | `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d` |

No dashboard-data JSON, evaluation package, raw source, database, or Claude-owned file is in the
replacement set.

## Verified release evidence

- Owner chapter-reference UAT: APPROVE; ten steps, four pinned artifacts, no observed defects.
- Independent review: APPROVE; 421 project tests, 49 sieving tests, 21/21 aggregate checks.
- Candidate validator: PASS; six files, 18 criteria, 62 crumbs.
- Portable-package validator: PASS; six files, one run.
- Report-link validator: PASS; 200 evidence links.
- Browser evidence: PASS; one bundle, 124 interactive targets, zero external requests.

## Transaction and recovery behavior

The controlled script refuses missing approvals, rejected/unsigned decisions, candidate drift,
baseline drift, paths outside the project, sources outside the candidate root, non-protected
destinations, an existing release manifest, or an unfinished transaction. It stages and hashes all
five replacements before the first swap. Any handled partial replacement or failed post-check
restores every changed destination from its byte-for-byte backup. If rollback itself cannot finish,
the transaction directory is preserved and the command reports manual recovery instead of claiming
success.

Promotion success is recorded at
`outputs/evidence_access_release_manifest_RUN-20260728-01.json`; it includes timestamp, approval
references, independent-review identity, candidate-manifest hash, and all five final hashes.

## Owner promotion decision — approved and executed

The Owner explicitly authorized both immutable decision references:

- `G5-EVIDENCE-ACCESS-RUN-20260728-01` — replace the two canonical report copies.
- `G6-EVIDENCE-ACCESS-RUN-20260728-01` — replace the two canonical dashboard copies and wiki copy.

Recorded approval text:

> Owner approves EA6.4 promotion of `EA6.4-RUN-20260728-01` under both
> `G5-EVIDENCE-ACCESS-RUN-20260728-01` and `G6-EVIDENCE-ACCESS-RUN-20260728-01`.

Execution completed at `2026-09-04T22:10:23Z`. The immutable result is
`outputs/evidence_access_release_manifest_RUN-20260728-01.json`; all five recorded destination
hashes match the approved candidate. Post-promotion aggregate validation passed 21/21 and all 200
canonical report evidence links resolved.

ELI5: the exact new book passed both inspections, the Owner approved the shelf replacement, and the
new book is now on the official shelf with a signed receipt recording exactly what changed.
