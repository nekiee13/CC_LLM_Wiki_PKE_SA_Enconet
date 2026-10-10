# Owner-approved first publication

The owner answered **yes** to this exact question:

> May I publish the verified report and dashboard now, with Claude's review
> deferred until available?

This permits publication for **RUN-20261008-17** before Claude completes the
technical review. It changes only the timing of the review in ADR-0024 decision 5.
The old ADR and normal replacement policy stay unchanged. Claude review is
pending, not passed or waived. Its requests remain in the active queue.

G5 and G6 were already approved. No score, source, crumb, chapter, finding,
rating, or field action may change. G7 is not approved. Field actions remain open.
The owner also authorizes resuming the recorded findings_approved cycle; the
unfinished run stamp stays intact and is not repaired in place.

## Exact release

The signed owner row is `PUBLICATION-RUN-20261008-17-20261009` in
`manifests/approvals.csv`. It pins the semantic hash of
`schemas/first_release_RUN-20261008-17.json`:

`124a49f4e9e342f63db22d5c9900fe0556e40bd1c06a3af844a6777c639c6b78`

The plan pins every source file and final destination. It publishes the report,
evaluation package, dashboard data, dashboard, wiki copy, and the seven-file
portable review folder. The report and dashboard keep their canonical names.
All bytes are copied from the verified outputs; nothing is regenerated.

## Safety and validation

`scripts/publish_audit_release.py` previews by default. Apply requires the
run's signed G5/G6 rows and this exact signed exception. It rejects paths outside
this project, changed hashes, duplicate targets, and any existing target.

Files are staged on the same volume and installed with atomic no-overwrite
hard links. The immutable result manifest is written last. This is not one
filesystem-wide atomic operation: readers treat the manifest as the commit
marker. A handled failure removes only unchanged files created by this apply.
A crash can leave an incomplete set without a marker; retry refuses that set
and requires investigation. Existing files are never deleted or replaced.

The post-apply validator checks final report links and runs all dashboard-ready
aggregate checks and both benchmarks against a temporary projected state.
It does not advance live state during validation. After successful publication,
the existing state API performs the legal G5 then G6 transitions. No G7 transition
is included. The full isolated regression suite and browser checks are required.

The new publisher is company-neutral; run paths and approvals are explicit in
the release contract. It does not import another company's code or evidence.
Future use still needs that audit's own approvals and publication authority.
