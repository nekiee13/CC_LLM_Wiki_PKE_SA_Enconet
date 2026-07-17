"""Positive and fault-injection tests for coordination_validator.py.

Every failure mode names the T4_COORDINATION_BOOTSTRAP_CONTRACT.md
"Validator and test contract" bullet it proves. All fixtures run in
pytest's disposable ``tmp_path``; nothing here touches CC_FIN or CC_Loto.
"""

from pathlib import Path

import coordination_validator as cv

MSG_TMPL = """---
message_id: {mid}
created_at_utc: {ts}
from_agent: {from_agent}
to_agent: {to_agent}
type: {mtype}
task: {task}
related_files: []{reply}
---

{body}
"""

MANIFEST_TMPL = """---
record_type: coordination_resolution_manifest
created_at_utc: {ts}
resolved_by: {resolved_by}
authority: ADR-0018
status: complete
---

# manifest
"""


def write_message(root: Path, filename: str, *, mid: str, from_agent: str,
                   to_agent: str = "both", mtype: str = "note", task: str = "T",
                   ts: str = "2026-07-17T01:00:00Z", reply_to: str | None = None,
                   body: str = "Concise evidence-based message body.",
                   in_archive: bool = False) -> Path:
    reply = f"\nreply_to: {reply_to}" if reply_to else ""
    text = MSG_TMPL.format(mid=mid, ts=ts, from_agent=from_agent, to_agent=to_agent,
                           mtype=mtype, task=task, reply=reply, body=body)
    sub = "archive" if in_archive else "messages"
    path = root / "coordination" / sub / filename
    path.write_text(text, encoding="utf-8")
    return path


def write_manifest(root: Path, filename: str, *, resolved_by: str,
                   resolved_messages: list[dict],
                   ts: str = "2026-07-17T01:05:00Z") -> Path:
    import json
    header = MANIFEST_TMPL.format(ts=ts, resolved_by=resolved_by)
    # Structured resolved_messages must be real YAML in the frontmatter, not
    # prose, so the manifest schema (list of objects) validates it.
    lines = header.splitlines()
    idx = lines.index("status: complete") + 1
    block = ["resolved_messages:"]
    for entry in resolved_messages:
        block.append(f"  - message_id: {entry['message_id']}")
        block.append(f"    disposition: {entry['disposition']}")
        block.append(f"    resolution: {json.dumps(entry.get('resolution', 'ok'))}")
        block.append("    confirmation_evidence:")
        block.append(f"      - {json.dumps(entry.get('evidence', 'evidence'))}")
        if entry.get("deferred_until"):
            block.append(f"    deferred_until: {json.dumps(entry['deferred_until'])}")
        if entry.get("deferral_owner"):
            block.append(f"    deferral_owner: {json.dumps(entry['deferral_owner'])}")
    lines[idx:idx] = block
    path = root / "coordination" / "archive" / filename
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_claim(root: Path, task: str, *, agent: str, status: str = "active",
                claimed: str = "2026-07-17T01:00:00Z",
                renewed: str | None = None, expires: str = "2026-07-18T01:00:00Z",
                released: str | None = None, files: list[str] | None = None,
                note: str = "Bounded scope.", filename: str | None = None) -> Path:
    import json
    renewed = renewed or claimed
    files = files or ["doc/support-transfer/x.md"]
    lines = [f"task: {task}", f"agent: {agent}", f"status: {status}",
             f"claimed_at_utc: {claimed}", f"last_renewed_at_utc: {renewed}",
             f"expires_at_utc: {expires}", "anticipated_files:"]
    lines += [f"  - {f}" for f in files]
    lines.append(f"note: {json.dumps(note)}")
    if released:
        lines.append(f"released_at_utc: {released}")
    path = root / "coordination" / "claims" / f"{filename or task}.yml"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------- positive

def test_empty_root_requires_generated_board(coord_root):
    result = cv.validate(coord_root)
    assert any("BOARD.md missing" in e for e in result.errors)
    cv.write_board(coord_root)
    assert cv.validate(coord_root).ok


def test_positive_message_and_claim_lifecycle(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_note.md",
                  mid="CC_20260717T010000Z_note", from_agent="claude-code")
    write_claim(coord_root, "T-DEMO", agent="claude-code")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert result.ok, result.errors


def test_positive_full_lifecycle_with_archive(coord_root):
    write_message(coord_root, "CX_20260717T010000Z_finding.md",
                  mid="CX_20260717T010000Z_finding", from_agent="codex", to_agent="claude-code",
                  in_archive=True)
    write_manifest(coord_root, "CX_20260717T010500Z_resolved-manifest.md",
                   resolved_by="codex",
                   resolved_messages=[{"message_id": "CX_20260717T010000Z_finding",
                                       "disposition": "resolved"}])
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert result.ok, result.errors


# --------------------------------------------------------------- messages

def test_message_id_filename_mismatch(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_note.md",
                  mid="CC_20260717T010000Z_other", from_agent="claude-code")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("does not match filename" in e for e in result.errors)


def test_duplicate_message_id(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_a.md",
                  mid="CC_20260717T010000Z_dup", from_agent="claude-code")
    (coord_root / "coordination" / "messages" / "CC_20260717T010000Z_dup.md").write_text(
        (coord_root / "coordination" / "messages" / "CC_20260717T010000Z_a.md")
        .read_text(encoding="utf-8"), encoding="utf-8")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("duplicate message_id" in e for e in result.errors)


def test_unknown_author_prefix_rejected_by_schema(coord_root):
    write_message(coord_root, "XX_20260717T010000Z_note.md",
                  mid="XX_20260717T010000Z_note", from_agent="claude-code")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("schema violation" in e for e in result.errors)


def test_invalid_created_at_utc(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_note.md",
                  mid="CC_20260717T010000Z_note", from_agent="claude-code",
                  ts="not-a-timestamp")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("invalid created_at_utc" in e for e in result.errors)


def test_related_files_path_traversal_rejected_by_schema(coord_root):
    text = MSG_TMPL.format(mid="CC_20260717T010000Z_note", ts="2026-07-17T01:00:00Z",
                           from_agent="claude-code", to_agent="both", mtype="note",
                           task="T", reply="", body="body")
    text = text.replace("related_files: []", "related_files:\n  - ../../etc/passwd")
    (coord_root / "coordination" / "messages" / "CC_20260717T010000Z_note.md").write_text(
        text, encoding="utf-8")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("schema violation" in e for e in result.errors)


def test_self_reply(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_note.md",
                  mid="CC_20260717T010000Z_note", from_agent="claude-code",
                  reply_to="CC_20260717T010000Z_note")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("self-reply" in e for e in result.errors)


def test_reply_cycle(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_a.md", mid="CC_20260717T010000Z_a",
                  from_agent="claude-code", reply_to="CX_20260717T010100Z_b")
    write_message(coord_root, "CX_20260717T010100Z_b.md", mid="CX_20260717T010100Z_b",
                  from_agent="codex", reply_to="CC_20260717T010000Z_a")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("cycle" in e for e in result.errors)


def test_unresolved_reply_to(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_a.md", mid="CC_20260717T010000Z_a",
                  from_agent="claude-code", reply_to="CX_20260101T000000Z_missing")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("not found in" in e for e in result.errors)


def test_unacknowledged_active_blocker(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_blk.md", mid="CC_20260717T010000Z_blk",
                  from_agent="claude-code", mtype="blocker")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("unacknowledged active blocker" in e for e in result.errors)


def test_acknowledged_blocker_is_clean(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_blk.md", mid="CC_20260717T010000Z_blk",
                  from_agent="claude-code", mtype="blocker")
    write_message(coord_root, "CX_20260717T010100Z_ack.md", mid="CX_20260717T010100Z_ack",
                  from_agent="codex", mtype="acknowledgement",
                  reply_to="CC_20260717T010000Z_blk")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert result.ok, result.errors


def test_one_sided_synchronization_warning(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_sync.md", mid="CC_20260717T010000Z_sync",
                  from_agent="claude-code",
                  body="Both agents synchronized on the neutral core.")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert result.ok
    assert any("without a confirming reply" in w for w in result.warnings)


def test_sensitive_content_in_message_body(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_leak.md", mid="CC_20260717T010000Z_leak",
                  from_agent="claude-code", body="api_key: sk_live_abcdef123456789")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("prohibited content pattern" in e for e in result.errors)


# --------------------------------------------------------------- archive

def test_archived_message_without_manifest(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_lost.md", mid="CC_20260717T010000Z_lost",
                  from_agent="claude-code", in_archive=True)
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("no same-prefix resolution manifest" in e for e in result.errors)


def test_deferred_until_missing_fields_rejected_by_schema(coord_root):
    write_message(coord_root, "CX_20260717T010000Z_defer.md", mid="CX_20260717T010000Z_defer",
                  from_agent="codex", in_archive=True)
    write_manifest(coord_root, "CX_20260717T010500Z_resolved-manifest.md",
                   resolved_by="codex",
                   resolved_messages=[{"message_id": "CX_20260717T010000Z_defer",
                                       "disposition": "deferred-until"}])
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("schema violation" in e for e in result.errors)


def test_deferred_until_with_required_fields_is_clean(coord_root):
    write_message(coord_root, "CX_20260717T010000Z_defer.md", mid="CX_20260717T010000Z_defer",
                  from_agent="codex", in_archive=True)
    write_manifest(coord_root, "CX_20260717T010500Z_resolved-manifest.md",
                   resolved_by="codex",
                   resolved_messages=[{"message_id": "CX_20260717T010000Z_defer",
                                       "disposition": "deferred-until",
                                       "deferred_until": "M2 approval",
                                       "deferral_owner": "owner"}])
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert result.ok, result.errors


def test_manifest_references_active_unarchived_message(coord_root):
    write_message(coord_root, "CX_20260717T010000Z_live.md", mid="CX_20260717T010000Z_live",
                  from_agent="codex")
    write_manifest(coord_root, "CX_20260717T010500Z_resolved-manifest.md",
                   resolved_by="codex",
                   resolved_messages=[{"message_id": "CX_20260717T010000Z_live",
                                       "disposition": "resolved"}])
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("references active (unarchived) message" in e for e in result.errors)


def test_manifest_references_unknown_message(coord_root):
    write_manifest(coord_root, "CX_20260717T010500Z_resolved-manifest.md",
                   resolved_by="codex",
                   resolved_messages=[{"message_id": "CX_20260101T000000Z_ghost",
                                       "disposition": "resolved"}])
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("references unknown message" in e for e in result.errors)


def test_cross_agent_archival_violation(coord_root):
    write_message(coord_root, "CC_20260717T010000Z_mine.md", mid="CC_20260717T010000Z_mine",
                  from_agent="claude-code", in_archive=True)
    # A CC-prefixed manifest naming codex as resolver is a self-contradicting
    # cross-agent archival: the manifest's own prefix disagrees with resolved_by.
    write_manifest(coord_root, "CC_20260717T010500Z_resolved-manifest.md",
                   resolved_by="codex",
                   resolved_messages=[{"message_id": "CC_20260717T010000Z_mine",
                                       "disposition": "resolved"}])
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("cross-agent archival" in e for e in result.errors)


# --------------------------------------------------------------- claims

def test_overlapping_active_claims_same_task(coord_root):
    # A real claim tool refuses a second agent writing the same task filename
    # (agent_coord.py cmd_claim); this fixture models exactly the fault that
    # refusal exists to prevent -- two distinct claim files that both name
    # task SHARED for a different agent.
    write_claim(coord_root, "SHARED", agent="codex", filename="SHARED")
    write_claim(coord_root, "SHARED", agent="claude-code", filename="SHARED-conflict")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("actively claimed by both agents" in e for e in result.errors)


def test_overlapping_active_claims_file_overlap(coord_root):
    write_claim(coord_root, "TASK-A", agent="codex", files=["shared/path.md"])
    write_claim(coord_root, "TASK-B", agent="claude-code", files=["shared/path.md"])
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("overlap on" in e for e in result.errors)


def test_invalid_renewal_order(coord_root):
    write_claim(coord_root, "T-BAD", agent="codex", claimed="2026-07-17T02:00:00Z",
               renewed="2026-07-17T01:00:00Z")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("invalid renewal order" in e for e in result.errors)


def test_inconsistent_expiry(coord_root):
    write_claim(coord_root, "T-BAD", agent="codex", claimed="2026-07-17T01:00:00Z",
               renewed="2026-07-17T01:00:00Z", expires="2026-07-17T00:00:00Z")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("inconsistent expiry" in e for e in result.errors)


def test_invalid_release_order(coord_root):
    write_claim(coord_root, "T-BAD", agent="codex", status="released",
               claimed="2026-07-17T02:00:00Z", renewed="2026-07-17T02:00:00Z",
               released="2026-07-17T01:00:00Z")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("invalid release order" in e for e in result.errors)


def test_sensitive_content_in_claim_note(coord_root):
    write_claim(coord_root, "T-LEAK", agent="codex",
               note=r"See C:\Users\jdoe\private notes for the password: hunter2xyz")
    cv.write_board(coord_root)
    result = cv.validate(coord_root)
    assert any("prohibited content" in e for e in result.errors)


# --------------------------------------------------------------- board

def test_stale_board(coord_root):
    cv.write_board(coord_root)
    write_message(coord_root, "CC_20260717T010000Z_note.md",
                  mid="CC_20260717T010000Z_note", from_agent="claude-code")
    result = cv.validate(coord_root)
    assert any("BOARD.md is stale" in e for e in result.errors)


def test_missing_schema_directory_is_a_hard_error(tmp_path):
    root = tmp_path / "bare"
    (root / "coordination").mkdir(parents=True)
    result = cv.validate(root)
    assert any("missing required schema" in e for e in result.errors)
