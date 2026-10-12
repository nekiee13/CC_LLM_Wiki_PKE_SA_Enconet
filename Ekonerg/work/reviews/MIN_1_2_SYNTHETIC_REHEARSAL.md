# MIN-1.2 — Synthetic end-to-end rehearsal

**Status:** Codex implementation complete; Claude review pending

## Scope

This sprint covered one task only: run the complete audit conveyor belt with
invented data. The rehearsal used a disposable project named `Ekonerg synthetic
Č audit`. It did not read Ekonerg or Enconet source files and did not change the
real Ekonerg database.

## Chain exercised

1. Fresh database initialization.
2. Repeatable seeding of the 18 Appendix B criteria.
3. Synthetic source registration and hashing.
4. Text extraction and chapter chunking.
5. Local prompt registration and sieve-run creation.
6. Synthetic crumb import and exact quote linking.
7. Synthetic applicability and criterion evaluations.
8. Evaluation package, Markdown report, dashboard data, and dashboard HTML.
9. Report and dashboard validation.

## Acceptance evidence

The direct call to the existing synthetic-chain test completed with exit code 0:

```text
MIN-1.2 synthetic end-to-end rehearsal: PASS
manual_exit_code=0
```

The disposable database contained:

| Record | Count |
|---|---:|
| Documents | 2 |
| Chunks | 2 |
| Crumbs | 1 |
| Crumb-to-chunk links | 1 |
| Criterion evaluations | 18 |

The output directory contained `package.json`, `report.md`, `dashboard.json`, and
`dashboard.html`. The temporary project was removed after verification. The real
Ekonerg database and incoming sources were not modified.

## Boundary

This closes MIN-1.2. The synthetic chain is proven. The next planned work is MIN-2
real-document processing and evidence/applicability completion; this rehearsal is
not an Ekonerg audit result and does not approve any score or finding.

