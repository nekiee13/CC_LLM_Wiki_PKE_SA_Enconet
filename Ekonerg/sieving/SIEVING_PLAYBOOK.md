# Sieving playbook

This is the local operating contract, not an approval to process documents.
Read the controlled source, active prompt, and current approvals before a run.
Keep source text and verbatim quotes unchanged. A new RUN-id is required for
each generation. A candidate never overwrites the active generation.

## Required local stages

- `sieve_run.py` starts a generation from a reviewed local document.
- `import_crumbs.py` imports only strictly validated output.
- `link_crumbs.py` links quote text to same-document chunks.
- `resieve_run.py` creates a new inactive candidate.
- `sieve_metrics.py` records quality and rejection counts.
- `sieve_diff.py` compares the candidate to the active generation.
- `score_sieving.py` measures against a human-approved golden set.
- `sieve_generation.py` records promotion, rejection, or rollback.

These names describe the full workflow. A missing local script is a blocker,
not permission to use a sibling project's script. Run validation must fail
closed until each stage, skill, source approval, and decision gate is ready.

## Batch sizing for sieving quality

Batch size is a reading-control rule. It helps keep review depth steady; it
does not change document identity or evidence provenance. Chapter and heading
paths remain the canonical locators. A page count is only a planning estimate.

Aim for about **30–50 pages of reading per batch**:

| Document class | Working rule | Why |
|---|---|---|
| Small, about 10 pages | Three documents per batch | Three small documents give roughly 30 pages. |
| Medium, about 15–30 pages | Two documents per batch | Two documents usually give a useful comparison set. Check the combined estimate against the 30–50 target. |
| Large, over 40 pages | One document per batch | A large document is already a full reading unit. Never add another large document just to fill a target. |
| Very large, 100+ pages | Still one document per batch | The document is user-prepared; do not split or merge it only to meet the page target. |

The ranges are guidance, not a reason to invent a page count. Codex chooses the
final grouping. For a document near the boundary (about 30–40 pages), with no
reliable page estimate, or whose pair would exceed the target, Codex records a
short sizing rationale. Do not silently force it into a triplet or pair.

Every batch record must list the document IDs, estimated pages when known,
class, estimated total, chapter range covered, and any exception. A batch may
be processed only after its source hashes and prompt version are recorded.

## Decision loop

1. Record the local RULE or DOCUMENT source and selected prompt version.
2. Create a new run. Validate strictly before import; unfiltered output is not a fallback.
3. Link quotes, inspect exception candidates, and record metrics plus a diff.
4. Review the golden score. A draft set is diagnostic only.
5. Obtain human approval before promotion. Retain rejected and older runs.
6. Record the decision, reason, and reusable lesson in the prompt CHANGELOG.

The initial `benchmarks/sieving_golden/manifest.yml` is empty and pending human
approval. It is not a calibrated score target or audit evidence.
