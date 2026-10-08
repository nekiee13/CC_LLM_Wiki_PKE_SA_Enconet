"""Read-only proof for the owner-approved, commit-scoped metadata exception."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
record = root / "coordination/messages/CX_2026-10-08T145632Z_enconet-referenced-partii-owner-approved.md"
data = record.read_bytes()
new = b"reply_to: CX_2026-10-08T143356Z_enconet-nqa1-part1-interpretation"
assert data.count(new) == 1
original = data.replace(new + b"\r\n", new + b".md\r\n", 1)
assert hashlib.sha256(original).hexdigest() == "ac3d646387ac4187867faf396e327a109844638536a5da36a1bdef406cb8b668"
assert hashlib.sha256(data).hexdigest() == "86e40aeb289df413ef4806aae8c3a4d10da7563b0941096e46e176b179c8a9c9"
assert hashlib.sha256(data.split(b"---", 2)[2]).hexdigest() == "d36a43fd1094d03d0738920aaa644f735a7547082492fcbf0c3adf5d9e8fad48"
assert hashlib.sha256((root / "db/nqa_audit.sqlite").read_bytes()).hexdigest() == "258479e38273b2a6184e71ddaad6f668af6f0d2f416f7d3cee947ac4750d1076"
print(json.dumps({"only_reply_to_changed": True, "body_byte_exact": True, "audit_db_byte_exact": True}))
