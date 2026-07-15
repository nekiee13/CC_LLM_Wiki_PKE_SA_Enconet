# Audit lifecycle and human gates

EPIC14 establishes a fail-closed state machine. It does not authorize a live audit run.
`project-state.yml` remains the authoritative state record.

## Session start

Read, in order: active agent guidance; the latest immutable handoff through `HANDOFF.md`;
`wiki/current-status.md`; `wiki/index.md`; and `project-state.yml`. Then run:

```powershell
python scripts/session_continuity.py
python scripts/audit_state.py --status
```

The continuity check reports disagreement among the handoff Git revision, actual Git HEAD,
the current-status phase, and project state. An in-progress phase or unfinished evaluation
run requires a human to choose **resume** or **rollback**. Neither command changes state.
Rollback is deliberately not implemented as an ordinary transition; it requires an approved,
run-specific recovery procedure and evidence-preserving correction.

## Human gate protocol

1. Create exactly one packet for a gate, supplier, and decision reference with
   `scripts/gate_packet.py create`. Packet creation stops without changing project state.
2. A human chooses approve, reject, or defer and signs one immutable row in
   `manifests/approvals.csv`.
3. Run `scripts/gate_packet.py record <packet>`. This mirrors the signed choice into the
   packet and `project-state.yml`, and appends a log entry. It does not advance the phase.
4. Only an approved gate permits `scripts/audit_state.py --transition <next-state>`.
   The state machine rechecks the signed CSV decision before changing the phase and logging it.

The human decides; the machine records and verifies. A rejection or deferral never advances.
Gate mapping is G1 registered, G2 evidence reviewed, G3 evaluated, G4 findings approved,
G5 report ready, G6 dashboard ready, and G7 closed.

## Session end and future closeout (Codex and Claude Code)

Run the aggregate validator with `python scripts/run_all_validations.py --no-record`, update
`wiki/current-status.md` so it names the exact next action, then invoke the shared `/handoff`
workflow and publish it with `../scripts/make_handoff.py`. EPIC17 `/audit-close` must call this
same validation-and-handoff sequence; it may not bypass it or manufacture a successful check.
Codex updates only its `AGENTS.md` integration; synchronization of Claude-owned guidance or
skills remains pending for Claude Code under the dual-agent boundary.
