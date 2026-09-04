# EA6.4 Evidence Access promotion gate

Gate status: **AWAITING OWNER PROMOTION DECISION**

Release: `EA6.4-RUN-20260728-01`

This packet asks one narrow question: may the already accepted Evidence Explorer candidate replace
the five protected canonical report/dashboard copies? It does not authorize a live service and does
not modify the closed audit findings, score, source evidence, or database.

## Exact candidate

- Production run: `RUN-20260728-01`
- Portable-package manifest SHA-256:
  `89a55446e4fc0c36952d6020c9bd8baa8a7595d04814bf5f90d91165ea9a7217`
- Published report SHA-256 after promotion:
  `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94`
- Published dashboard SHA-256 after promotion:
  `74e54dfa2faf6e62f410febdc4d2e729fd6324d8de3edeb1d6d700e734ba04a2`
- Owner UAT: `EA5.4-RUN-20260728-01`, approved 2026-09-04, ten of ten steps passed.
- Independent review: `CC_2026-09-04T185412Z_ea6-3-correction-approve`, approved with no findings.

## Exact replacement set

| Protected destination | Current SHA-256 | Proposed SHA-256 |
| --- | --- | --- |
| `outputs/enconet_appendix_b_evaluation_report.md` | `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175` | `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94` |
| `outputs/enconet_appendix_b_evaluation_report_hr.md` | `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175` | `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94` |
| `outputs/enconet_appendix_b_dashboard.html` | `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07` | `74e54dfa2faf6e62f410febdc4d2e729fd6324d8de3edeb1d6d700e734ba04a2` |
| `outputs/enconet_appendix_b_dashboard_hr.html` | `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07` | `74e54dfa2faf6e62f410febdc4d2e729fd6324d8de3edeb1d6d700e734ba04a2` |
| `wiki/dashboards/enconet_appendix_b_dashboard.html` | `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07` | `74e54dfa2faf6e62f410febdc4d2e729fd6324d8de3edeb1d6d700e734ba04a2` |

No dashboard-data JSON, evaluation package, raw source, database, or Claude-owned file is in the
replacement set.

## Verified release evidence

- Focused EA6.4 TDD suite: 9 passed.
- Full project regression suite: 421 passed; two third-party Typer/Click deprecation warnings.
- Sieving regression suite: 49 passed; the same two third-party deprecation warnings.
- Candidate validator: PASS; six files, 18 criteria, 62 crumbs.
- Corrected Owner UAT validator: PASS; ten steps, four pinned artifacts, decision approve.
- Independent-review validator: PASS; eight commands, ten risk checks, decision approve.
- Portable-package validator: PASS; six files, one run.
- Final-name report-link validator: PASS; 200 evidence links.
- Full phase-aware aggregate: PASS; 21 of 21 checks, including interactive browser and budgets.
- Browser evidence: PASS; one bundle, 124 interactive assertions, zero external requests.

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

## Owner decision required

To approve, the Owner must explicitly authorize both of these immutable decision references:

- `G5-EVIDENCE-ACCESS-RUN-20260728-01` — replace the two canonical report copies.
- `G6-EVIDENCE-ACCESS-RUN-20260728-01` — replace the two canonical dashboard copies and wiki copy.

Suggested unambiguous approval text:

> Owner approves EA6.4 promotion of `EA6.4-RUN-20260728-01` under both
> `G5-EVIDENCE-ACCESS-RUN-20260728-01` and `G6-EVIDENCE-ACCESS-RUN-20260728-01`.

Reject or defer by naming the release and the reason. Until the exact approval is recorded, running
the script without `--execute` stops, and `--execute` fails before changing any protected output.

ELI5: UAT said the new book is easy to read, and Claude said it is correctly made. This final gate
asks whether the new book may now replace the old book on the official shelf.
