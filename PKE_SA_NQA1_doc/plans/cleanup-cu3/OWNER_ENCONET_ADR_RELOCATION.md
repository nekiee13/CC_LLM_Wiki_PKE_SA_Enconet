# Enconet: two-file relocation authority

Decision: OWNER-ENCONET-ADR-RELOCATION-20261013.

The owner answered “proceed” to Codex's specific request to move the two
Claude-owned ADR files from `Enconet/decisions/` to `Enconet/work/decisions/`.
This is a narrow exception to the agent ownership boundary. It permits these
two moves only, without changing their contents. Claude retains ownership.
It does not authorize changes to other `CC_` files, Claude guidance or skills.

| File | Original raw SHA256 |
| --- | --- |
| CC_ADR-0016-dual-agent-infrastructure-ban.md | db947dce26552dd93cce5754fbc289bb47188530e2120d17dc9f3558ad8b60d2 |
| CC_ADR-0017-interagent-coordination-protocol.md | da4ba94d6372bc4b2976a34f65f93097b9f3f9062935c37132b016e481c83298 |

Verify both hashes after moving. Do not overwrite existing targets. The moves
are reversible by returning the unchanged files to their original paths.
The existing cleanup scope and deferred post-execution review remain in place.
