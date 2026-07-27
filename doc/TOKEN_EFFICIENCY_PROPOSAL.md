# Token-efficiency proposal

**Status:** non-authoritative engineering proposal; implementation and controlled workflow changes
require the normal owner, gate, and coordination approvals.

**Scope:** token consumption during agent navigation, LLM-assisted source processing, later audit
stages, validation review, and cross-agent handoff across `03_PKE_SA_NQA1`.

## Objective and invariant

Reduce avoidable token consumption without weakening processing quality, evidence integrity,
validation rigor, controlled-document requirements, provenance, or human approval gates.

Incoming controlled sources may require complete reading. The primary optimization opportunity is to
prevent the same source and unchanged downstream evidence from being repeatedly loaded into later
LLM contexts when canonical, traceable projections can answer the task.

No token target may:

- truncate required evidence silently;
- replace a required full-source or full-record review;
- turn a failed, blocked, skipped, or unavailable validation into an implied pass;
- bypass phase controls, human gates, provenance, or immutable-source rules;
- make a summary or index a new evidence authority.

## Evidence status

The prior test run demonstrated high token consumption, but a comparable stage-level measurement
record is not yet present in the workspace. Therefore:

1. do not claim a quantified saving yet;
2. collect a reproducible baseline before selecting a numerical target;
3. compare only runs with equivalent corpus, source revision, model/provider, prompt and schema
   versions, stage boundaries, and quality checks;
4. record any unavoidable comparison difference explicitly.

## Prioritized mitigations

### P0 — Retrieval discipline

Already represented in Codex guidance:

- check index identity and freshness before MCP-heavy exploration;
- prefer indexed section/symbol retrieval and narrow `rg` searches;
- use stable identifiers and bounded context;
- reserve full-file reads for mandatory contracts, required controlled sources, high-risk records,
  ambiguity, conflict, missing context, and other correctness needs;
- summarize routine output while retaining exact decision-relevant evidence.

Additional operational applications:

- do not re-read unchanged content already established in the active session; verify a hash or
  relevant diff first when freshness is uncertain;
- query growing CSV/JSON manifests by stable run/source identifier with jdatamunch or an equivalent
  deterministic row-level tool when a current dataset index exists, instead of loading the entire
  dataset as text;
- read the relevant section or tail of replaceable status and append-only log files during routine
  work; use the full truthful record at closeout/handoff or whenever broader history affects the
  decision;
- inspect unresolved coordination messages and active claims first; do not load the archive unless
  a live reference, lifecycle check, dispute, or historical decision requires it;
- prefer concise test output such as quiet mode and short tracebacks, while expanding the exact
  failing check and preserved full log during diagnosis.

This changes agent navigation, not source authority or validation scope.

### P1 — Stage-level measurement and failure digests

Add a machine-readable record for each LLM-assisted stage with:

- audit/batch/run identifier and stage;
- provider, model, prompt version, schema/contract version, and cache mode;
- input, cached-input, output, and total tokens when the provider exposes them;
- retry count and retry reason;
- document, chunk, crumb, quote, criterion, and evidence-item counts as applicable;
- input and output artifact paths plus hashes;
- validation commands, integer exit codes, counts, warnings, and exact failures;
- wall-clock duration as a secondary operational metric.

Complete logs remain artifacts. Agents may consume a concise failure digest first, then open the
full log whenever the digest is insufficient or a failure requires diagnosis.

### P2 — Canonical criterion-scoped review packets

Create a read-only projection from the canonical database and active generation. A criterion packet
should contain:

- audit/evaluation run, criterion identifier, name, and applicability state;
- active crumb identifiers and document side;
- exact quote identifiers and text;
- linked chunk identifiers, offsets, source identifiers, and provenance hashes;
- compact deterministic metadata and explicit neighboring-context references;
- omissions, unmatched evidence, exceptions, and validation state;
- a packet hash and the query/projection version used to build it.

The packet is a retrieval aid, not an evidence authority. Review escalation is:

1. manifest and counts;
2. criterion packet;
3. exact linked chunk;
4. adjacent chunks or relevant section;
5. complete controlled source.

Ambiguity, conflict, missing context, suspicious extraction, broken traceability, or reviewer need
requires escalation. A token budget must never suppress that escalation.

### P3 — Verified delta review

For repeat sieving, prompt candidates, and revised artifacts:

- review the generation diff and changed crumbs first;
- prove unchanged records with stable identifiers and hashes;
- include additions, removals, changes, authority-side changes, quote/link changes, and validation
  deltas;
- fall back to a full comparison if hashes, lineage, ordering, or diff completeness cannot be
  proven.

Full baseline review remains required at the applicable approval gate and whenever controlled
policy requires it.

### P4 — Deterministic/LLM separation and prefix reuse

Keep deterministic operations outside LLM context:

- parsing and chunking;
- exact/normalized quote linking;
- schema and provenance validation;
- scoring, metrics, matrices, and package construction;
- report/dashboard rendering;
- comparison and failure-digest generation.

Use the LLM for semantic judgment, exception review, and synthesis that actually requires it.
Provider-supported caching may reuse immutable prompts, schemas, rubrics, and authority prefixes
only after cache behavior and version binding are verified. Cache hits are an efficiency metric,
not evidence of correctness.

### P5 — Validation scheduling

During implementation:

- run focused tests and changed-scope lint for rapid feedback;
- run impacted guardrail and negative-path tests whenever their contract is touched;
- run every mandatory aggregate and gate validation at the required controlled boundary.

Targeted checks reduce iteration cost; they never replace the required full suite.

### P6 — Index maintenance

Treat indexes as commit-scoped evidence:

- record index name, source root, indexed revision or truthful dirty state, profile, and timestamp;
- refresh explicit changed paths during active work when supported;
- perform one verified clean-tip reconciliation after publication and bilateral archival;
- rebuild fully when deletion/rename semantics are unproven, scope or ignore rules change, the
  parser/index format changes, integrity verification fails, or Git history cannot be reconciled.

Do not repeatedly rebuild an unchanged complete corpus merely to produce a newer timestamp.

## Quality-preserving acceptance criteria

An optimization is acceptable only when the comparison proves all applicable conditions:

1. identical controlled source revision and provenance;
2. identical required record population, active-generation selection, and stable evidence links;
3. no new unmatched quotes, missing evidence, schema errors, or validation warnings;
4. no reduction in required reviewer context or gate evidence;
5. identical deterministic artifacts where byte identity is expected, or an explicitly reviewed
   semantic diff where it is not;
6. all impacted negative-path tests and required aggregate/gate validations pass with exact command
   and exit-code evidence;
7. a reviewer can navigate every compact claim back to the canonical database and controlled source;
8. measured token consumption is lower on comparable runs, without additional retries or quality
   exceptions that negate the saving.

Until a baseline exists, success is limited to verified instrumentation and retrieval behavior; it
must not be described as a quantified efficiency improvement.

## Stop and fallback conditions

Stop the optimized path and use broader retrieval or full processing when:

- evidence is ambiguous, conflicting, incomplete, or unexpectedly sparse;
- packet/diff hashes or lineage do not verify;
- an index is stale and live-tree verification is unavailable;
- a validator, negative-path test, or human reviewer finds a quality regression;
- the model requests missing context needed for a defensible judgment;
- provider token accounting is absent or internally inconsistent.

Preserve the failed optimized attempt and its metrics. Do not hide the fallback cost when reporting
token usage.

## Candidate implementation slices

These are proposals, not authorization:

1. **Measurement record:** define an append-only token-usage schema and provider-neutral recorder.
2. **Validation digest:** add deterministic JSON output alongside preserved full command logs.
3. **Evidence packet:** add a read-only criterion projection from SQLite/`active_crumbs` with hashes
   and tests for completeness, traceability, inactive-generation exclusion, and escalation metadata.
4. **Delta assurance:** strengthen generation-diff verification with unchanged-record hashes and
   forced full-comparison fallback.
5. **Comparable pilot:** run baseline and optimized processing on the same approved representative
   corpus, then submit metrics and quality evidence for human review.

Each slice requires a scoped claim, tests proportional to audit/data-integrity risk, independent
cross-agent review where the operating mode requires it, and explicit owner decisions at existing
human gates.

## Decision queue

- Select the provider-neutral token measurement fields and storage location.
- Decide whether full prompts may be stored; default to hashes and version identifiers when prompts
  might contain controlled source text.
- Choose the representative approved corpus for the first comparable baseline.
- Define numerical warning thresholds only after baseline variance is known.
- Obtain owner authorization before changing controlled stage behavior or gate criteria.
