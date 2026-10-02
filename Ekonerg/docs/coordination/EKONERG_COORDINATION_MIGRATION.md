# Ekonerg coordination migration

Status: owner-directed migration completed  
Date: 2026-10-02  
Implementer: Codex

## What moved

The Ekonerg project now owns its communication queue under
`Ekonerg/coordination/`.

- 64 active Ekonerg messages moved to `Ekonerg/coordination/messages/`.
- 42 Ekonerg archive records moved to `Ekonerg/coordination/archive/`.
- 49 Ekonerg claim records moved to `Ekonerg/coordination/claims/`.
- The neutral protocol was copied to `Ekonerg/coordination/TEAM_PROTOCOL.md`.
- Ekonerg's board was regenerated with the local script.

The records retain their original filenames, message IDs, timestamps, contents,
and `CX_`/`CC_` ownership prefixes. No source documents, evidence, or audit
database rows were moved.

## What stayed in Enconet

Enconet keeps its own coordination records and generated board. Generic
workspace guidance stays there. One older resolution manifest covers both an
Ekonerg plan-review request and a separate Enconet status acknowledgement, so
it remains in Enconet unchanged. A local Ekonerg resolution manifest preserves
the Ekonerg archive link without rewriting either original record.

## Validation

Run these commands from the workspace root:

```text
python Ekonerg/scripts/agent_coord.py validate
python scripts/agent_coord.py validate
```

Both project queues must validate independently. New Ekonerg messages and claims
must use `Ekonerg/scripts/agent_coord.py`; Enconet messages continue to use the
workspace/Enconet tool.
