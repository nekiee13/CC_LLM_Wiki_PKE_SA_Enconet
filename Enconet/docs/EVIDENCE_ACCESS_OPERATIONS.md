# Evidence Access operations manual

This manual is the operator-facing procedure for the current offline Evidence Explorer. Run all
commands from the Enconet project root in PowerShell. Candidate work stays under
`outputs/candidates/evidence_access`; it does not overwrite approved outputs.

## Conda environment

The controlled interpreter is `C:\xPY\vEnv\WikiEnconet\python.exe`. Do not substitute the system
Python when creating release evidence. Verify the environment first.

<!-- command:verify-environment -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' sieving\verify_install.py
```

Expected: dependency, structure, and import error counts are all zero. A missing dependency,
encoding error, or wrong interpreter is a failed precondition.

## Open and use

The simplest entry point is the portable landing page. No server or installation is needed.

<!-- command:open-workspace -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' -m webbrowser -t 'file:///C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1/Enconet/outputs/candidates/evidence_access/portable_package/review_workspace.html'
```

Select `RUN-20260728-01`, open its report, and click a crumb. The browser opens the matching
statement, document, exact quote(s), source locator, chapter chunk, adjacent context, and hashes.
Copy citation and Print evidence operate entirely in the browser. From Obsidian, open the portable
`evaluation_report.md`; its links target the sibling `evidence_explorer.html`.

## Artifact map

| Artifact | Purpose | Rebuildable? |
| --- | --- | --- |
| `review_workspace.html` | Human landing page and run selector | Yes |
| `review_catalog.json` | Validated registry projection for available runs | Yes |
| `evaluation_report.md` | Portable report with evidence deep links | Yes |
| `evidence_explorer.html` | Self-contained offline review UI | Yes |
| `evidence_bundle.json` | Typed source-evidence projection | Yes, from controlled DB/package |
| `evaluation_package.json` | Evaluation data used to render the report | Controlled input copy |
| `package_manifest.json` | Complete file inventory and SHA-256 integrity contract | Yes |

The canonical approved report/dashboard remain outside this portable candidate. Their hashes are
protected by `schemas/evidence_access_release_candidate.yml`.

## Build

Build only into an absent or empty scratch directory. Replace `<EMPTY_OUTPUT_DIRECTORY>` with a new
path such as `C:\Temp\enconet-review-rehearsal`; never point it at `outputs/` or the repository root.

<!-- command:build-portable -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\build_review_package.py --catalog outputs\candidates\evidence_access\review_catalog.json --source-root . --output <EMPTY_OUTPUT_DIRECTORY>
```

The builder validates the catalog, copies the fixed run artifacts, regenerates portable report
links, renders the workspace, writes a sorted manifest, then validates the finished package. A
non-empty destination fails closed. Repeating the build from identical inputs must reproduce
manifest SHA-256 `89a55446e4fc0c36952d6020c9bd8baa8a7595d04814bf5f90d91165ea9a7217`.

## Validate

Run the checks in this order. Every command is read-only for controlled outputs.

<!-- command:validate-candidate -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\validate_evidence_access_candidate.py --contract schemas\evidence_access_release_candidate.yml --project-root .
```

<!-- command:validate-package -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\validate_review_package.py outputs\candidates\evidence_access\portable_package
```

<!-- command:validate-uat -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\validate_evidence_access_uat.py --contract schemas\evidence_access_uat.yml --packet docs\acceptance\EA5.4_OWNER_UAT.md --project-root .
```

Run the full phase-aware aggregate last. `--no-record` prevents a validation-history write.

<!-- command:aggregate -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\audit_command.py audit-validate -- --no-record
```

Expected current results: six portable payload files, one run, 18 criteria, 62 crumbs, 200 report
evidence links, an interactive browser check, zero external browser requests, and all aggregate
checks passing. Exact timing values are observations, not stable fingerprints.

Check the protected approved baseline whenever promotion or recovery is discussed.

<!-- command:hash-baseline -->
```powershell
Get-FileHash outputs\enconet_appendix_b_evaluation_report.md -Algorithm SHA256; Get-FileHash outputs\enconet_appendix_b_dashboard.html -Algorithm SHA256
```

Expected report SHA-256: `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175`.
Expected dashboard SHA-256: `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07`.

## Promotion gate

Promotion is a separate Owner decision. Ten-step usability approval and Claude's independent
technical approval prove that the candidate is acceptable to consider; neither authorizes replacing
the five protected report/dashboard copies. The fixed transaction is defined by
`schemas/evidence_access_promotion.yml` and requires both signed approval rows:

- `G5-EVIDENCE-ACCESS-RUN-20260728-01` for the report copies.
- `G6-EVIDENCE-ACCESS-RUN-20260728-01` for the dashboard and wiki-dashboard copies.

Running the command without `--execute` is always a stop-only check and changes nothing.

<!-- command:promotion-stop -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\promote_evidence_access.py --contract schemas\evidence_access_promotion.yml
```

After the Owner explicitly approves the exact EA6.4 packet and both immutable rows have been
recorded in `manifests/approvals.csv`, use the controlled command below. Do not copy the files by
hand.

<!-- command:promotion-execute -->
```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\promote_evidence_access.py --contract schemas\evidence_access_promotion.yml --execute
```

The command rechecks signed approvals, candidate and baseline hashes, UAT, independent review,
portable-package integrity, and the full aggregate before writing. It stages all five files and
keeps byte-for-byte backups. A handled replacement or post-validation failure rolls every changed
destination back. Success additionally reruns final-name link resolution, an interactive zero-network
browser check, package validation, and the aggregate, then writes
`outputs/evidence_access_release_manifest_RUN-20260728-01.json` with the final hashes. An existing
result manifest or unfinished transaction fails closed instead of repeating promotion.

ELI5: two keys are needed to open the official cabinet—one for the report and one for the dashboard.
The tool checks both keys, swaps the whole matched set, inspects it, and puts the old set back if any
inspection fails.

## Transfer

1. Validate the source package.
2. Copy the entire `portable_package` directory, including `package_manifest.json`. Never copy only
   the HTML file: its report, bundle, package, and catalog are part of the integrity contract.
3. Do not rename files inside the copied directory.
4. Validate the copied directory with `validate_review_package.py <copied-directory>`.
5. Open the copied `review_workspace.html` and test one report-to-crumb link.

The package uses relative paths, contains no repository username/drive dependency, and is tested in
a non-ASCII relocation path. Treat email, cloud storage, and removable media as untrusted transport;
validate after receipt before opening.

## Failure guide

| Symptom | Meaning | Safe response |
| --- | --- | --- |
| Manifest/hash mismatch | A file changed, was damaged, or belongs to another package | Stop; recover or rebuild the whole package |
| Missing/unlisted file | Transfer is incomplete or contaminated | Stop; repeat the full-directory transfer |
| Report link fails | Report/viewer/package set is mismatched | Validate links; do not hand-edit the report |
| Unknown crumb | Bundle, viewer, or run identity is inconsistent | Rebuild from the registered candidate inputs |
| Browser page is blank | File blocked, truncated, or script error | Check browser console artifact and package hash |
| External request detected | Offline/security contract violated | Reject the candidate and add a regression test |
| Size or timing budget fails | Package exceeds approved operating limits | Diagnose projection growth; do not raise limits silently |
| UTF-8/Unicode error | Wrong encoding or damaged source | Stop; never “fix” controlled raw files in place |
| Phase refusal | Command is not legal in current audit phase | Run `audit-status`; do not bypass the dispatcher |

## Recovery

The last approved canonical report/dashboard were introduced at commit
`7ecbf4bdef9ab8385bd2157a1b57b067b0e2516a`. Recovery is a controlled replacement, not an ad-hoc
edit and not a destructive Git reset.

1. Stop publication and preserve the failed package plus logs as evidence.
2. Confirm the two expected baseline hashes above.
3. Retrieve the approved file bytes from commit `7ecbf4b...` into a separate recovery directory;
   do not overwrite the worktree during diagnosis.
4. Compare hashes and validate the recovered artifacts.
5. Obtain the applicable Owner gate before replacing any canonical output.
6. Copy atomically through the approved EA6.4 promotion mechanism, rerun aggregate/browser/link
   checks, and record new hashes and the decision reference.

If only a candidate is damaged, delete or quarantine only that explicitly identified candidate and
rebuild it into an empty directory. Approved outputs are not a candidate-rebuild target.

## Documentation self-check

Run `scripts\validate_evidence_access_docs.py` using the command shown in its `--help`. It checks
every command marker, architecture and upgrade topics, candidate/UAT state, and rebuilds the package
in a fresh non-ASCII temporary directory. Documentation is incomplete if that rehearsal fails.
