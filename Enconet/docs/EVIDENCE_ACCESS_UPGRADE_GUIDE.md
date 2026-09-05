# Evidence Access controlled upgrade guide

This guide is for planning a future improvement. It does not authorize a change or promotion.

## EA6.5 presentation candidate: ordered classification bands

Owner feedback dated 2026-09-05 identified a presentation-only defect: classification counts were
shown in dictionary/alphabetical order, so lower categories appeared between higher categories.
EA6.5 changes presentation only; it does not change any evaluation, score, count, or threshold.

The display contract is:

| Order | Category | Consolidated-score band |
| ---: | --- | --- |
| 1 | `fully` | `[90–100]` |
| 2 | `substantially` | `[70–<90]` |
| 3 | `partially` | `[40–<70]` |
| 4 | `minimally` | `[10–<40]` |
| 5 | `unmet` | `[0–<10]` |
| 6 | `undetermined` | no consolidated-score band |
| 7 | `na` | no consolidated-score band |

These bands are generated from `schemas/scoring_model.yml`; the HTML renderer does not own a
second copy of the thresholds. The first band includes the scoring maximum. Every later upper
boundary is exclusive because the next-higher category owns that exact threshold. `undetermined`
and `na` are criterion states rather than consolidated-score classifications, so assigning them a
numeric interval would be misleading.

TDD evidence lives in `tests/test_epic12_dashboard.py` and `tests/test_evidence_drawer.py`. The
candidate changes `scripts/generate_dashboard.py` and `templates/dashboard-template.html` only.
Previously promoted HTML remains unchanged until an isolated revised candidate completes browser
testing, independent review, Owner acceptance, and controlled promotion.

Candidate evidence:

- Review file: `outputs/candidates/evidence_access/RUN-20260728-01/enconet_appendix_b_dashboard_EA6-5.html`
- Promoted/prior-candidate dashboard SHA-256: `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d`
- EA6.5 review-file SHA-256: `5bc39042aaaae9d5486e3f468a77984c874234edf91f695a6776d5231dcd93dd`
- Verification: 424 project tests passed; candidate dashboard validation passed; candidate headless-browser
  check passed with one embedded bundle, 124 interactive evidence controls, and zero external requests;
  the phase-aware aggregate passed after Chromium execution was permitted.

## Current approved behavior

The current candidate is a deterministic offline package for `RUN-20260728-01`. It provides a
landing page, portable Markdown report, exact evidence drawer, adjacent chunk navigation, copyable
citation, print view, search/filter controls, multi-run-ready catalog, package manifest, zero-network
browser behavior, and Owner-approved usability. It uses the pinned Conda interpreter and remains a
candidate until EA6.3 review and EA6.4 promotion.

Preserve these invariants unless a new Owner decision explicitly changes them:

- SQLite/source provenance remains authoritative; generated files are projections.
- Stable IDs and hashes provide end-to-end traceability.
- Report links resolve without a repository-specific absolute path.
- Browser source text cannot execute as markup or script.
- Offline use requires no service, account, or network connection.
- Candidate generation never silently overwrites approved outputs.
- Human usability, independent review, and promotion remain distinct gates.

## Upgrade decision gate

Before implementation, write a decision record answering:

1. Which measured user problem cannot be solved by the current static package?
2. Who uses the change, with what data volume, operating system, and security constraints?
3. Is the need presentation-only, a new evidence projection, multi-run scale, collaboration, or a
   live service?
4. What new data enters or leaves the trust boundary?
5. Which current invariant changes, and why is that risk accepted?
6. What is the migration, compatibility, acceptance, and rollback strategy?

A vague preference for “a GUI” is not sufficient: a browser GUI already exists. A live service
requires a separate Owner choice and a superseding ADR because it adds ports, processes, state,
concurrency, and operational security.

## Compatibility contract

An upgrade is compatible only if automated tests prove:

- existing fragment URLs still open the same typed entity, or a versioned redirect map exists;
- bundle schema changes are versioned and old packages remain readable or have a deterministic
  migration tool;
- citations retain run/document/crumb/quote/chunk/source-hash identity;
- catalog and manifest readers reject unknown unsafe structures rather than guessing;
- old approved packages validate independently of the new code where practical;
- multilingual text round-trips exactly;
- no new network request, executable source-text path, or path escape appears;
- performance and size remain within Owner-approved budgets or new budgets are explicitly approved.

## Change matrix

| Proposed change | Minimum synchronized surfaces |
| --- | --- |
| New evidence field | DB query, bundle schema, resolver, validator, renderer, citation if relevant, fixtures |
| New entity/link type | Stable ID rule, schema, graph validation, fragment routing, keyboard/focus tests |
| New run | Artifact generation, registry row/hashes, catalog, workspace, portable manifest |
| New export | Deterministic renderer, MIME/encoding rules, manifest role/schema, portability tests |
| UI redesign | Accessibility, deep-link, history, copy/print, filter/search, browser regression |
| Budget change | Owner authority, budget contract, hostile/large fixtures, measured release evidence |
| Live service | Superseding ADR, threat model, auth, network policy, lifecycle, backup, deployment, audit log |

## TDD upgrade sequence

1. Capture the user problem and current-package fixture.
2. Write a failing test at the lowest stable contract boundary.
3. Implement the smallest compatible change in candidate paths.
4. Add negative tests for malformed data, unsafe paths/text, missing lineage, and partial failure.
5. Run focused tests, then complete Enconet, sieving, installation, aggregate, browser, portability,
   and documentation rehearsals.
6. Compare generated hashes and explain every intended change.
7. Obtain independent review and Owner usability acceptance for changed behavior.
8. Promote atomically only through the approved human gate.

## Migration and versioning

Prefer additive schema evolution. Increment schema versions when consumers must change. Never
reinterpret an existing field silently. Keep a fixture for every supported prior version. Migrations
must be deterministic, input-preserving, separately validated, and write to a new candidate path.
Do not migrate raw sources or approved artifacts in place.

For URL changes, maintain old fragment fixtures and either preserve them or generate an explicit
mapping artifact included in the package manifest. For catalog changes, keep run isolation so one
invalid run cannot cause artifacts from another run to be presented as matched.

## Security and privacy review

Re-run the hostile-source corpus for any renderer or browser change. A service proposal additionally
needs binding-address defaults, authentication/authorization, CSRF and injection controls, file and
database access boundaries, dependency patching, logging, retention, secrets handling, and a clear
shutdown/recovery procedure. Do not expose controlled evidence on a network by default.

## Rollback plan

Every upgrade proposal must record before implementation:

- the last approved commit (`7ecbf4bdef9ab8385bd2157a1b57b067b0e2516a` for the current canonical
  report/dashboard baseline);
- approved report/dashboard hashes and current candidate manifest hash;
- exact files expected to change;
- how to rebuild both old and new candidates;
- the trigger for rollback and the person authorized to decide;
- a rehearsal proving old artifacts still validate after rollback.

Rollback means selecting verified prior bytes and atomically restoring them through governance. It
does not mean destructive reset of the repository or manual editing of generated output.

## Upgrade evidence packet

Before requesting approval, provide: decision/ADR, issue plan, RED test, code diff, schema diff,
generation diff, old/new hashes, focused/full validation logs, browser screenshots/console/network
evidence, portability result, budget measurements, independent review, Owner UAT, and rollback
rehearsal. If any item is not applicable, state why explicitly.
