---
message_id: CX_2026-09-29T183312Z_ekonerg-sieving-io-review
created_at_utc: 2026-09-29T18:33:12Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EK-1.2-SIEVING-IO
related_files:
  - Ekonerg/docs/transfer/EK_1_2_SIEVING_IO.md
  - Ekonerg/docs/transfer/EK_1_2_SIEVING_IO_ADAPTATIONS.json
  - Ekonerg/sieving/src/json_extractor/io/__init__.py
  - Ekonerg/sieving/src/json_extractor/io/_paths.py
  - Ekonerg/sieving/src/json_extractor/io/files.py
  - Ekonerg/sieving/src/json_extractor/io/export.py
  - Ekonerg/sieving/tests/test_io_paths.py
---

# EK-1.2: local sieving I/O

Date: 2026-09-29. Codex implements; Claude reviews later. This is one
slice of EK-1.2, not completion of the task or Epic 1.

## What & Why

The source sieving tool can discover JSON files and export tables. Those
functions take paths from callers. In Ekonerg, a caller path must not read
Enconet data or write an Ekonerg result into Enconet. This slice transfers
the three source I/O files and adds a local path guard. It keeps the public
read and CSV/XLSX/Markdown export functions, source column choices, format
selection, and deterministic discovery order.

Relative paths now start at the Ekonerg project root, even when the command
starts in another folder. The guard rejects sibling or nested Enconet paths,
links to outside folders, and existing hard-linked files. Discovery rejects
patterns that climb above the chosen data folder. Foreign paths fail before
reading or writing. The guard is for normal workflows; it cannot stop a
different process changing a path between the check and the file operation.

## Tests first

Before the four local I/O files existed, all eight first tests failed in
fixture setup. After adaptation, 11 I/O tests and the five foundation tests
passed. Fixtures have a path with spaces and Croatian text. They include a
fake sibling and nested Enconet folder, a foreign file and output folder,
symbolic and hard links, invalid JSON, multiple JSON subfolders, and three
synthetic table exports. The tests check foreign marker bytes and timestamps
before and after. No real source document or audit output is used.

## Source identity and remaining work

The three selected manifest rows are pinned to Git commit `9f20430`.
`EK_1_2_SIEVING_IO_ADAPTATIONS.json` lists each source blob, source hash,
destination LF hash, and the two new files. Source and destination differ
because paths and error boundaries changed. After this slice, 204 adapt
rows and 49 recreate rows remain. The pending continuity and foundation
reviews are not counted as approvals.

This I/O package is not a runnable extraction pipeline. The top-level
package, extraction, query, pipeline, CLI, prompts, full corpus tests, and
release checks are still missing. Other entry points can still accept an
unsafe path until they are adapted. Do not ingest documents or treat the
provisional schema codes as approved Ekonerg source editions or scope.

## Checks for this slice

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 16 synthetic tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and the 275-file dependency scan match the pinned source. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured. |
| `python -B -c "import sys,pathlib; sys.path.insert(0,str(pathlib.Path('Ekonerg/sieving').resolve())); import src.json_extractor.io as io; print(pathlib.Path(io.__file__).resolve())"` | 0 | Import resolved to Ekonerg's local I/O package. |

The full audit aggregate, source corpus validation, browser and benchmark
checks are **not run**. They require later EK-1.2 files or fresh owner-approved
inputs. Claude should review only this I/O slice when available: compare the
pinned source and hashes, inspect local path and import behavior, rerun the
synthetic checks, and report findings or slice-only approval. Keep EK-1.2 open.
