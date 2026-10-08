---
record_type: metadata_exception_manifest
created_at_utc: 2026-10-08T15:31:17Z
source_agent: codex
owner_decision_ref: COORD-ENCONET-REPLYTO-20261008
---

# Owner-approved single-field metadata correction

Owner replied **Approved** to the explicit request for this one exception.
This is not a general permission to rewrite immutable coordination records.

- Record: `CX_2026-10-08T145632Z_enconet-referenced-partii-owner-approved.md`.
- Original `reply_to`: `CX_2026-10-08T143356Z_enconet-nqa1-part1-interpretation.md`.
- Corrected `reply_to`: `CX_2026-10-08T143356Z_enconet-nqa1-part1-interpretation`.
- Before SHA256: `ac3d646387ac4187867faf396e327a109844638536a5da36a1bdef406cb8b668`.
- Final after SHA256: `86e40aeb289df413ef4806aae8c3a4d10da7563b0941096e46e176b179c8a9c9`.
- Message body SHA256, unchanged: `d36a43fd1094d03d0738920aaa644f735a7547082492fcbf0c3adf5d9e8fad48`.
- Audit database SHA256, unchanged: `258479e38273b2a6184e71ddaad6f668af6f0d2f416f7d3cee947ac4750d1076`.

The read-only proof reconstructs the original bytes by putting back only the
removed suffix and obtains the exact before-hash. This proves that no other
field, body text or line ending changed. The same check confirms the audit
database is byte-exact.

## Validation evidence

Final command, exit **0**:

~~~~powershell
python -c "import hashlib,json; from pathlib import Path; p=Path('Enconet/coordination/messages/CX_2026-10-08T145632Z_enconet-referenced-partii-owner-approved.md'); b=p.read_bytes(); new=b'reply_to: CX_2026-10-08T143356Z_enconet-nqa1-part1-interpretation'; assert b.count(new)==1; old=b.replace(new+b'\r\n',new+b'.md\r\n',1); assert hashlib.sha256(old).hexdigest()=='ac3d646387ac4187867faf396e327a109844638536a5da36a1bdef406cb8b668'; assert hashlib.sha256(b.split(b'---',2)[2]).hexdigest()=='d36a43fd1094d03d0738920aaa644f735a7547082492fcbf0c3adf5d9e8fad48'; assert hashlib.sha256(Path('Enconet/db/nqa_audit.sqlite').read_bytes()).hexdigest()=='258479e38273b2a6184e71ddaad6f668af6f0d2f416f7d3cee947ac4750d1076'; print(json.dumps({'only_reply_to_changed':True,'body_byte_exact':True,'audit_db_byte_exact':True}))"
~~~~

`python scripts/agent_coord.py status --write` and
`python scripts/agent_coord.py validate` both exited **0** after the correction.
Coordination then had zero errors and zero warnings.

The initial byte-reconstruction check exited **1** because the patch editor
gave the edited header line an LF ending instead of its original CRLF.
Its intermediate file hash was
`6d4c2e7c11bdcef5c6d9981bab7c70bf3456ac7deee5ebb8e1a25168de603173`.
Only that line ending was formatted back to CRLF. The final check above then
passed and reconstructs the original file byte-for-byte by restoring the suffix.
The message body and audit database hashes matched throughout. This draft
manifest was finalized with the verified hash before its first publication.

Earlier messages and evidence reports which describe the defect remain
historical records. This later manifest records its resolution. No substantive
review is closed and no message is archived by this metadata exception.

## Pending publication and next action

Publish the corrected Part II review request and the valid Part 21 review
request `CX_2026-10-08T152235Z_enconet-part21-separate-duties.md` with the
regenerated board. Both reviews remain pending Claude; publication is not
review acceptance. Next substantive work is G2 applicability preparation.
