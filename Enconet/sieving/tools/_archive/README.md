# Archived sieving tools (C4.3 tombstone)

These scripts are preserved as immutable migration history. They are not active tools and
must not be executed against `sieving/DATA` or the working tree. Several assume an obsolete
root, mutate files in place, synthesize evidence/provenance placeholders, or advertise the
retired Streamlit GUI.

Archived groups:

- `check_files.py`, `fix_files.py`, `fix_structure.py`, `fix_init_files.py`, and
  `print_run_pipeline_sig.py`: obsolete installation/structure diagnostics and mutators.
- `fix_mor_taxonomy_id.py`: repaired MOR taxonomy/criterion naming drift.
- `fix_mor_rule_refs.py` and `fix_rule_refs_from_criterion.py`: synthesized missing
  Appendix B rule-reference join keys from criterion classification.
- `fix_nqa1_to_midlayer.py`: normalized NQA-1 records, including synthesized required
  fields and placeholder evidence/source values; this behavior is unsuitable for controlled
  evidence without an approved migration manifest.

Use Git history and `doc/LESSONS-LEARNED.md` to understand these migrations. Future migrations
require an explicit source/target root, dry-run output, backup/rollback design, fixture tests,
and owner approval. Restoring a script to active use requires a reviewed replacement, not moving
the archived file back.
