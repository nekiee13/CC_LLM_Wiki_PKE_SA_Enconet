# Evidence Access controlled upgrade guide

This guide is for planning a future improvement. It does not authorize a change or promotion.

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
