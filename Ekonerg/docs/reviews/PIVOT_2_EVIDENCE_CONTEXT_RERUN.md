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

The aggregate scripts suite was rerun with `TEMP` and `TMP` pointed at a
project-local temporary root so the earlier global-temp permission issue would
not be hidden:

```text
python -m pytest Ekonerg/scripts/tests -q
exit 1
26 passed, 1 failed, 44 errors, 2 warnings in 11.41s
```

The 44 errors are still Windows protected-temp-directory ACL failures while
pytest tries to create numbered temporary folders. The one failure is the
existing symlink-privilege test (`WinError 1314`), which needs Windows
developer-mode or equivalent symlink privilege. This is an environment gate,
not a failed evidence-context assertion.

No audit database, crumbs, or source files were changed by this rerun.
