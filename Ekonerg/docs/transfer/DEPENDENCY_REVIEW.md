# EK-0.2 dependency review

This review follows the pinned source at `9f20430`. It identifies what must exist
in the new project, not what already works there. No source tool was executed.

## How the review was done

The inventory reads every tracked blob from Git. All selected text is scanned
for old identities, hashes, paths, and approval terms. Every selected Python
file is parsed, without importing it. The scan records import names, top-level
root assignments, and references to known filenames. Direct inspection covered
the command registry, both aggregate runners, the handoff schema, path helpers,
state checks, schema-folder run records, corpus checks, and quarantine tests.

The scanner uses filename candidates, not full program dataflow. A common name
such as `README.md` can yield several candidates. No local import candidate
group was found with only excluded files. This is a useful check, not proof of
complete import resolution. Dynamic paths and imports still need EK-1.2 tests.

The shared documentation and code indexes were checked. They point to commit
`62a0251` from July, not the required September baseline. They were not used as
current evidence and were not refreshed during this task.

## Dependency groups and their disposition

| Consumer or contract | Dependency | What & Why |
|---|---|---|
| Audit command registry and dispatcher | Local stage scripts, state, gates, ledgers, handoff helper | Keep all stage scripts. Replace `../scripts/make_handoff.py` with the local route. Test phase checks before subprocess launch. |
| Workspace aggregate runner | Five support tools, four support tests, project tests, sieving tests, schemas | All tools and tests are selected as adapt. Repoint each command and working folder; keep skipped distinct from passed. |
| Project aggregate runner | Validator scripts, state, database, output package, browser, benchmark runner | All code is selected. Setup must not need old outputs. Later phases still require real approved inputs. |
| Database creation and migration | `db/schema.sql`, taxonomy and vocabulary | Schema and code are adapted. Create a new database, never copy the live one. Inspect seed statements and assert empty source/run tables. |
| Sieving library and CLI | Local `json_extractor` package, taxonomy, contract, prompts | Keep every package source file and initializer. Do not use an editable install pointing into Enconet. |
| Report and dashboard generators | Local templates and schemas | All templates and framework schemas are selected. Preserve offline evidence behavior and classification bands. |
| Browser harness | Pinned Python package and browser config | Config is adapted. The shared runtime path may remain only after its separate compatibility check. No network request is allowed during browser tests. |
| Candidate, UAT, review and promotion validators | Six run-bound contracts and new packets | Recreate contracts. Change consumers and tests together so blank setup does not look approved and release still fails without real approval. |
| Source and ingest tools | Fresh CSV ledgers, empty raw/derived/DATA roots, batch records | Recreate headers and folders. New batches are created from Owner-approved intake, not copied. |
| Continuity and handoff tools | New state/wiki/handshake records and actual Git root | Keep current Ekonerg planning records. Never import Enconet status, history, or unfinished run IDs. |
| Guidance and interface validators | Codex guidance, Claude setup, local pair map and skill contract | Codex handles its side; Claude supplies its own files. Do not weaken missing-side checks or fabricate synchronization. |
| Benchmark and export tests | Synthetic data and expected values | Recreate fixtures, including XLSX and hashes. Review expectations independently. Keep scoring and dashboard fixtures separate. |

## Specific problems that adaptation must cover

### Old corpus assumptions

`sieving/tests/test_contract_drift.py` expects 68 corpus files and the recorded
old defects. `run_validation.py` also reads the old corpus manifest and migration
record. Recreate those records for an empty corpus. Split empty-setup checks from
synthetic corpus regression tests. Preserve strict rejection and export behavior;
do not merely delete the failing test.

`sieving/src/json_extractor/config.py` builds its default DATA path with
`parents[2]`. The actual project corpus is under `sieving/DATA`. Review the default
and explicit caller configuration together. Do not bless a path just because
it happens to remain inside Ekonerg.

### Retired repair scripts

`sieving/tests/test_tool_quarantine.py` expects nine scripts in `tools/_archive`.
The manifest excludes those scripts. The new tests must prove they are absent,
the quarantine notice is present, and installation checks never suggest running
them. Review `verify_install.py` and documentation-command tests with that change.

### Fixed Enconet paths and values

`audit_command.py` and `session_continuity.py` derive a workspace root outside
the project. Audit closeout and its registry must call the local handoff helper.
Keep the true Git root separate from the runtime root.

`evidence_access_policy.py` names Enconet output baselines. Rebuild that set from
the chosen local company/configuration. Preserve protection of approved outputs.

`validate_evidence_access_docs.py` pins the shared interpreter path and reads
specific old candidate/UAT packet names. A shared interpreter is allowed; old
packets are not. Adapt the contract and documentation checks together. Do not
relax approval or hash checks just to make a blank project pass release checks.

### Tests that read production artifacts

The scan finds old output, source, batch, and finding names in several test modules.
Those modules are adapt, not copy. Replace all production reads with isolated
fixtures. This covers the raw/chunk, requirements, validation, browser, candidate,
promotion, evidence-viewer, and portable-package test families.

The golden evidence-bundle hash and export spreadsheet are recreated. A new hash
must follow an independently reviewed synthetic result, not conceal changed logic.

### Policy and history

Old ADR files and completed review records are excluded. Reusable rules still
apply through workspace guidance and new local documents. In particular preserve
the governing/interpretive source distinction, verbatim quotes, source language,
batched intake, no Streamlit UI, offline evidence, human gates, and agent ownership.
Tests that cite the old evidence-access ADR must point to the new local rule,
not require copied history. The temporary single-agent exception is not carried over.

Provenance text may name the upstream repository and Enconet commit. That is not
an active runtime dependency. Preserve origin and any applicable license notices.
No separate license file appears in the selected baseline inventory; do not
invent a license or claim that this check establishes redistribution rights.

## Imported packages

The non-stdlib imports found are `pandas`, `openpyxl`, `yaml` (PyYAML), `typer`,
`rich`, `pytest`, and `playwright`. Versions are defined by the selected environment
and sieving requirement files; EK-1.3 verifies them without silent upgrades.

The scanner also lists `extract`, `query`, and dotted `json_extractor` or
`src.json_extractor` packages as unresolved candidates. These are local package
routes under selected `sieving/src/`, not extra pip packages. Relative imports,
`__init__.py` exports, and runtime `sys.path` changes need isolated import tests.

No extra owner choice is needed to propose this manifest. Audit scope, source
editions, storage, and backup choices remain the later Owner intake gate. Any new
runtime choice or restored retired tool would need explicit direction.
