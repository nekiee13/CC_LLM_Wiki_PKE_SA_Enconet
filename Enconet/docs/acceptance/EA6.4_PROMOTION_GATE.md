# EA6.4 Evidence Access promotion gate

Gate status: **SUPERSEDED — CHAPTER-REFERENCE CANDIDATE REQUIRES REAPPROVAL**

Release: `EA6.4-RUN-20260728-01`

This packet is retained as historical preparation evidence. It no longer asks for a decision: the
Owner requested explicit corresponding chapter references after it was prepared, changing the
candidate fingerprints and reopening UAT plus independent review. A replacement packet must be
prepared after those gates approve the new bytes. The eventual narrow question remains whether the
accepted Evidence Explorer candidate may replace
the five protected canonical report/dashboard copies? It does not authorize a live service and does
not modify the closed audit findings, score, source evidence, or database.

## Exact candidate

- Production run: `RUN-20260728-01`
- Portable-package manifest SHA-256:
  `f3b72fdd381453af69b97e8d6e423c749fdbe045f3b0a55e8c7d43fc22faa95d`
- Published report SHA-256 after promotion:
  `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94`
- Published dashboard SHA-256 after promotion:
  `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d`
- Owner UAT: reopened for the chapter-reference candidate.
- Independent review: reopened because the viewer and portable-package bytes changed.

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

## Historical release evidence

The earlier candidate passed its focused, full-regression, package, link, aggregate, browser, Owner
UAT, and independent-review checks. Those results remain audit history, but they do **not** approve
the chapter-reference candidate because its viewer and package fingerprints differ. Fresh UAT and
independent review are required before a replacement promotion packet can be created.

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

## No Owner promotion decision is requested by this packet

Do not approve or execute promotion from this superseded packet. First complete the reopened Owner
UAT and independent review for the chapter-reference fingerprints. If both approve, create a new
promotion packet that pins those decisions and the validated artifact hashes.

ELI5: the book gained chapter labels after the old checks. Check that exact new book again before
anyone asks to place it on the official shelf.
