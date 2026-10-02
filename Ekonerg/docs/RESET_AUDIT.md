# Ekonerg audit reset command

## What it does

`reset_audit.py` starts a fresh audit run while keeping the reusable framework
and the owner's source drop. It is useful when an audit is repeated after a
new document revision or when the processing code changes.

ELI5: it empties the audit notebook, but keeps the blank notebook template and
the documents in the incoming tray.

The command does **not** delete:

- `Ekonerg/incoming/`;
- framework code, schemas, prompts, tests, or vendor design assets;
- documentation, coordination messages, claims, archives, or handoffs;
- the database schema; or
- Git history.

Immutable coordination and handoff records are preserved for traceability.
The mutable project state and generated wiki index/status are reset when they
exist; `wiki/log.md` remains as history.

## Preview first

Preview is the default and makes no changes:

```powershell
python Ekonerg/scripts/reset_audit.py `
  --plan C:\Temp\ekonerg-reset-plan.json
```

The plan lists every candidate file, its hash, and its action. A normal
Ekonerg source set currently produces candidates from runtime work, database
backups, sieving runs/outputs, wiki result folders, and mutable CSV manifests.

## Apply only after checking the plan

The plan and backup must be outside the Ekonerg project. The exact confirmation
token is deliberately hard to type by accident:

```powershell
python Ekonerg/scripts/reset_audit.py `
  --apply `
  --plan C:\Temp\ekonerg-reset-plan.json `
  --backup-dir C:\AuditBackups\Ekonerg `
  --confirm RESET-EKONERG
```

Apply will:

1. check that incoming files and all candidate hashes still match the preview;
2. create a ZIP backup outside the project;
3. verify the backup contents;
4. delete only the listed generated files;
5. clear mutable validation manifests back to their headers; and
6. leave incoming documents and framework files untouched.

If anything changed after preview, the command stops before deletion. A wrong
confirmation, an in-project backup path, a missing incoming folder, a link or
reparse point, a hard-linked target, or an unexpected manifest header also
stops the command.

## Important limits

This is an operational reset, not an eraser of audit history. It intentionally
keeps tracked review, coordination, and handoff records. If the owner wants a
legal or records-management purge, that must be a separate, explicitly
approved task; this command will not perform it.

The command does not choose new source editions, approve evidence, or rerun an
audit. After reset, create a new intake register and repeat the normal gates
from G1 onward.
