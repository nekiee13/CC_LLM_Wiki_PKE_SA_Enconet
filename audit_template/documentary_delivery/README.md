# Documentary packaging add-on v1

This pinned, tested add-on prepares a **candidate** portable delivery from a
company's existing scored documentation review. It does not issue a G5/G6
release, bypass the formal report generator, reset a project, or approve sources.

Both payload files are local runtime copies. Do not overwrite an existing
report_stack_core.py with a different hash. The current Ekonerg copies match
the manifest exactly. This add-on is not silently added to immutable v3.
Future integration needs a new reviewed template version.

Requirements: local G2/G3 approvals, an evaluation package, exact current
light/dark data, active score-support crumbs, verbatim quotes and source ranges.
Prepared output must stay under outputs/candidates/evidence_access/<run_id>/.
Use explicit input paths. Preview never writes; --apply creates a fresh directory
and writes its hash marker last. Retry refuses an existing directory.

Normal CLI and sibling preservation tests cover two synthetic names, including
TEKOL Engineering and Žuti dobavljač, with and without another company folder.
No audit sources, database, approvals or result fixtures are in this add-on.
