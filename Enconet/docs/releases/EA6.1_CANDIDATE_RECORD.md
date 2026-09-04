# EA6.1 production candidate record

Status: **candidate — not promoted**

Candidate `EA6.1-RUN-20260728-01` is the complete offline evidence-access dress rehearsal for
`RUN-20260728-01`. It was already generated under the candidate root; EA6.1 formalizes its exact
identity and proves that verification does not rewrite it or the approved outputs.

## Candidate contents

The portable package at `outputs/candidates/evidence_access/portable_package` contains:

| Role | Artifact |
| --- | --- |
| Landing page | `review_workspace.html` |
| Run catalog | `review_catalog.json` |
| Evaluation report | `RUN-20260728-01/evaluation_report.md` |
| Evidence Explorer | `RUN-20260728-01/evidence_explorer.html` |
| Evidence projection | `RUN-20260728-01/evidence_bundle.json` |
| Evaluation package | `RUN-20260728-01/evaluation_package.json` |

The package manifest SHA-256 is
`f3b72fdd381453af69b97e8d6e423c749fdbe045f3b0a55e8c7d43fc22faa95d`. It declares all six
payload files and their hashes. The bundle contains 18 criterion evaluations and 62 resolvable
crumbs. The 14 exact source hashes are pinned in `schemas/evidence_access_release_candidate.yml`.

## Protected approved baseline

EA6.1 does not modify or promote these canonical outputs:

- Report: `0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175`
- Dashboard: `15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07`

Run the read-only contract check with:

```powershell
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\validate_evidence_access_candidate.py `
  --contract schemas\evidence_access_release_candidate.yml --project-root .
```

The Owner-requested chapter-reference correction changed the viewer and package fingerprints after
the prior UAT and independent review. UAT and independent review are therefore reopened. Promotion
remains blocked until both approve these exact bytes and a new EA6.4 human gate is prepared. This
record is not promotion authorization.
