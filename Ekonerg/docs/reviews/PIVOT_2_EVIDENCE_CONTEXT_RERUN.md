# PIVOT-2 evidence-context rerun

## Targeted context checks

```text
python -m pytest Ekonerg/scripts/tests/test_evidence_context.py \
  Ekonerg/scripts/tests/test_context_storage.py -q -p no:cacheprovider
exit 0
3 passed in 0.07s
```

The schema and additive `crumb_context` storage checks pass.

## Aggregate suite rerun

The aggregate scripts and sieving suites were rerun after the v3 active-prompt
assertion was updated:

```text
python -m pytest Ekonerg/scripts/tests -q
exit 0
76 passed in 11.24s

python -m pytest Ekonerg/scripts/tests Ekonerg/sieving/tests -q
exit 0
168 passed, 11 subtests passed in 33.53s
```

The earlier temporary-directory, symlink, and stale-v2 assertion failures did
not recur in this rerun. The v3 active-prompt assertion is green.

No audit database, crumbs, or source files were changed by this rerun.
