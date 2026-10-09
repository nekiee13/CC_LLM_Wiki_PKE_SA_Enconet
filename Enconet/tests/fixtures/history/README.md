# Historical regression fixture — not active audit evidence

`enconet-pre-reset-20261007.zip` is a byte-identical copy of the verified reset
archive, SHA256 `38018c13eb9c17172c7c3486b4041dbb54e27618f78cfb9989ebb56cbfcfaedf`.
Owner authorized this isolated regression dependency repair on9October2026.
Original provenance: `docs/ENCONET_RESET_20261007.md` and archive `reset-plan.json`.
The full corpus ZIP is deliberately Git-ignored under ADR-0002, not committed as
a new way to bypass the DATA policy. Provision the verified local copy from the
owner-controlled reset archive before running historical characterization tests.
Missing or changed fixture bytes are an explicit validation failure, never a skip.
All358 manifest payloads must match their archived checksums before use.

The fixture retains historical statements/counts/golden assertions unchanged.
It may only be unpacked into a new test workspace. Never restore it into live
incoming/raw/derived/db/outputs or inherit its approvals for a new audit.
Normal runtime commands do not read this fixture. Claude infrastructure and
agent messages are excluded from test-workspace copying.
