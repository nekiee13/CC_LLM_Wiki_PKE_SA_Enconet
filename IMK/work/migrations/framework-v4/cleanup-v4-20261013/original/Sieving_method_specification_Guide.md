# Reusable audit method v2

This copy contains tools, not another company's audit. Its approvals are empty.
Sources, editions, supplier scope, applicability, language, and prompt activation
must be recorded for the company that uses it.

## Collect evidence broadly

Read every chapter twice: first for direct controls, then for the intent of each
Appendix B criterion. Use the concept cards and full keyword rules as search aids.
Read unmatched text too. There is no fixed crumb quota. A passage may support
several control ideas; retain a separate, well-explained crumb for each idea.

Keep concrete controls, supporting controls, and candidate leads distinct. A
reference to a standard is a lead, not proof that all its duties are met.
Fuzzy matching applies to meaning. It never relaxes exact quotes or invents facts.
This is not a formal FAHP scoring model.

## Keep the source chain

Store source text by chapter. Each accepted quote must link to its own document's
chapter. Register and verify hashes. A revised manual is a new intake, not an
edit to old raw evidence. Keep rejected and superseded generations for history.

The v3 prompt is supplied as a candidate method. Do not copy another company's
golden fixtures, approval rows, active prompt history, or run decisions. Validate
the local schema and calibrate before activation. No source documents are included.

## Rate the documentation

Use the local five-level scoring contract. Do not raise a rating just because
there are more crumbs. Explain each rating and link the controls that support it.
Written coverage can be full even though work samples must be checked at the real
audit. Real written gaps still matter. An ordinal score is not clause-by-clause
proof of legal compliance. Keep separate regulatory duties explicit in scope.

## Display the results

`build_vendor_dashboard.py` reads a required local run ID and writes a fresh
light candidate under `out/`. `build_dark_dashboard.py` makes a separate dark
copy. Both preserve existing controlled reports, scores, and dashboards.
Cards show a short summary when closed; open them to read arguments, score
support, exact quotes, chapters, gaps, and actions. Filters, search, sorting,
expand/collapse, matrix sorting, keyboard shortcuts, and light printing remain.

## Reset only when requested

`reset_audit.py` defaults to preview. It removes known generated audit state,
including `out/` snapshots, and clears known audit manifests. It preserves
incoming documents, framework code, prompts, schemas, docs, coordination, and
handoff history. Reset is destructive; never run it as an upgrade step.

Use an external plan, review its targets, and keep a generated-state backup.
`RESET-AUDIT` confirms a backed-up apply. The separate `RESET-AUDIT-NO-BACKUP`
token is a deliberate owner choice for that reset, not inherited permission.
The v2 plan format rejects older plans. Reinitialize the empty database after
reset and start intake again. Prompt approval and source decisions must be
reviewed for the new audit, not silently reused.
