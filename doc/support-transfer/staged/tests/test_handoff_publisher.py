"""Positive and fault-injection tests for handoff_publisher.py.

Every failure mode names the T5_HANDOFF_CONTINUITY_CONTRACT.md "Test
contract" bullet it proves. All fixtures run in pytest's disposable
``tmp_path``; nothing here touches CC_FIN or CC_Loto.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

import handoff_publisher as hp

VALID_HEAD_1 = "a" * 40
VALID_HEAD_2 = "b" * 64
SCHEMA_SRC = (Path(__file__).resolve().parent.parent.parent / "templates" / "handoff"
              / "handoff.schema.json")


def make_target(tmp_path: Path, name: str = "target") -> Path:
    """A disposable target root with the shipped handoff schema installed at
    its clone-complete location (publication refuses to run without it)."""
    root = tmp_path / name
    (root / "support" / "schemas").mkdir(parents=True, exist_ok=True)
    shutil.copy(SCHEMA_SRC, root / "support" / "schemas" / "handoff.schema.json")
    return root


def make_record(**overrides) -> hp.HandoffRecord:
    defaults = dict(
        record_id="2026-07-17T010000Z-abc1234",
        created_at_utc="2026-07-17T01:00:00Z",
        source_agent="claude-code",
        status="complete",
        objective="Prove the staged handoff publisher against a disposable root.",
        checks=[hp.Check(name="unit", state="passed", command="pytest -q", exit_code=0,
                         evidence="12 passed")],
        git_state=hp.GitState(state="current", root="/r", branch="main",
                              head=VALID_HEAD_1, upstream_relation="synchronized",
                              worktree="clean"),
        next_action=hp.NextAction(owner="claude-code", action="Continue T6",
                                  stop_condition="Codex review complete"),
        work_completed=["Built the staged publisher."],
        remaining_work=["Independent review."],
        decisions=["Use disposable git repos for staleness tests."],
        blockers=[],
        artifacts=["doc/support-transfer/staged/handoff_publisher.py"],
        follow_up_queue=["Request Codex review."],
    )
    defaults.update(overrides)
    return hp.HandoffRecord(**defaults)


# --------------------------------------------------------------- positive

def test_positive_publish_lifecycle(tmp_path):
    root = make_target(tmp_path)
    record = make_record()
    result = hp.publish(root, record)
    assert result.exit_code == 0
    assert not result.adopted_existing
    assert result.record_path.is_file()
    assert result.pointer_path.is_file()
    assert record.record_id in result.pointer_path.read_text(encoding="utf-8")
    log_lines = result.log_path.read_text(encoding="utf-8").splitlines()
    assert len(log_lines) == 1
    assert record.record_id in log_lines[0]

    reread = hp.parse_record(result.record_path.read_text(encoding="utf-8"))
    assert reread.record_id == record.record_id
    assert reread.status == record.status
    assert reread.checks[0].name == "unit"
    assert reread.git_state.state == "current"
    assert reread.git_state.head == VALID_HEAD_1


def test_positive_partial_and_blocked_status(tmp_path):
    for status in ("partial", "blocked"):
        root = make_target(tmp_path, status)
        record = make_record(status=status,
                             checks=[hp.Check(name="unit", state="failed",
                                              command="pytest -q", exit_code=1,
                                              evidence="1 failed")])
        result = hp.publish(root, record)
        assert result.exit_code == 0


# --------------------------------------------------------------- interruption

def test_fault_before_record_write_leaves_no_trace(tmp_path):
    root = make_target(tmp_path)
    record = make_record()
    with pytest.raises(hp.FaultInjected):
        hp.publish(root, record, fault_at="before-record-write")
    assert not (root / "support" / "handoffs" / f"{record.record_id}.md").exists()
    assert not (root / "HANDOFF.md").exists()


def test_fault_after_record_before_pointer_then_retry_adopts(tmp_path):
    root = make_target(tmp_path)
    record = make_record()
    with pytest.raises(hp.FaultInjected):
        hp.publish(root, record, fault_at="after-record-before-pointer")
    record_path = root / "support" / "handoffs" / f"{record.record_id}.md"
    assert record_path.is_file()
    assert not (root / "HANDOFF.md").exists()
    before = record_path.read_text(encoding="utf-8")

    result = hp.publish(root, record)
    assert result.adopted_existing is True
    assert record_path.read_text(encoding="utf-8") == before
    assert (root / "HANDOFF.md").is_file()


def test_fault_after_pointer_before_log_then_retry_logs_once(tmp_path):
    root = make_target(tmp_path)
    record = make_record()
    with pytest.raises(hp.FaultInjected):
        hp.publish(root, record, fault_at="after-pointer-before-log")
    assert (root / "support" / "handoffs" / f"{record.record_id}.md").is_file()
    assert (root / "HANDOFF.md").is_file()
    assert not (root / "support" / "log.md").exists()

    result = hp.publish(root, record)
    log_lines = result.log_path.read_text(encoding="utf-8").splitlines()
    assert len(log_lines) == 1


def test_duplicate_id_different_content_refused(tmp_path):
    root = make_target(tmp_path)
    record = make_record()
    hp.publish(root, record)
    changed = make_record(objective="A different objective for the same record id.")
    with pytest.raises(hp.PublishError, match="already exists with different content"):
        hp.publish(root, changed)


# --------------------------------------------------------------- truthful checks

@pytest.mark.parametrize("check", [
    pytest.param(hp.Check(name="c", state="passed", command="x", exit_code=1, evidence="e"),
                id="passed-with-nonzero-exit"),
    pytest.param(hp.Check(name="c", state="passed", command=None, exit_code=0, evidence="e"),
                id="passed-without-command"),
    pytest.param(hp.Check(name="c", state="failed", command="x", exit_code=0, evidence="e"),
                id="failed-with-zero-exit"),
    pytest.param(hp.Check(name="c", state="skipped", command="x", exit_code=0, evidence="e"),
                id="skipped-with-exit-code"),
    pytest.param(hp.Check(name="c", state="not-run", command=None, exit_code=None, evidence=""),
                id="missing-evidence"),
])
def test_malformed_check_state_rejected(tmp_path, check):
    record = make_record(checks=[check])
    with pytest.raises(hp.PublishError):
        hp.publish(make_target(tmp_path), record)


def test_complete_status_with_failed_check_rejected(tmp_path):
    record = make_record(status="complete",
                         checks=[hp.Check(name="c", state="failed", command="x",
                                          exit_code=1, evidence="e")])
    with pytest.raises(hp.PublishError, match="never complete with an implied pass"):
        hp.publish(make_target(tmp_path), record)


# --------------------------------------------------------------- Git fabrication

def test_absent_git_state_with_fabricated_head_rejected(tmp_path):
    record = make_record(git_state=hp.GitState(state="absent", root=None, branch=None,
                                               head=VALID_HEAD_1))
    with pytest.raises(hp.PublishError, match="no fabricated Git identity"):
        hp.publish(make_target(tmp_path), record)


def test_unknown_git_state_with_fabricated_head_rejected(tmp_path):
    record = make_record(git_state=hp.GitState(state="unknown", root="/r", branch="main",
                                               head=VALID_HEAD_1))
    with pytest.raises(hp.PublishError, match="no fabricated HEAD"):
        hp.publish(make_target(tmp_path), record)


@pytest.mark.parametrize("head", [VALID_HEAD_1, VALID_HEAD_2])
def test_current_git_state_accepts_sha1_and_sha256(tmp_path, head):
    record = make_record(git_state=hp.GitState(state="current", root="/r", branch="main",
                                               head=head, worktree="clean"))
    result = hp.publish(make_target(tmp_path, f"target-{len(head)}"), record)
    assert result.exit_code == 0


def test_current_git_state_with_short_head_rejected(tmp_path):
    record = make_record(git_state=hp.GitState(state="current", root="/r", branch="main",
                                               head="deadbeef"))
    with pytest.raises(hp.PublishError, match="40- or 64-hex HEAD"):
        hp.publish(make_target(tmp_path), record)


@pytest.mark.parametrize("git_state", [
    pytest.param(hp.GitState(state="absent"), id="complete-with-absent"),
    pytest.param(hp.GitState(state="unknown", root="/r", branch="main"),
                id="complete-with-unknown"),
])
def test_complete_status_with_absent_or_unknown_git_rejected(tmp_path, git_state):
    record = make_record(git_state=git_state)
    with pytest.raises(hp.PublishError, match="use partial or blocked"):
        hp.publish(make_target(tmp_path), record)


def test_absent_git_supported_with_partial_status(tmp_path):
    record = make_record(status="partial", git_state=hp.GitState(state="absent"))
    assert hp.publish(make_target(tmp_path), record).exit_code == 0


def test_code_and_shipped_schema_agree_on_probes():
    """The publisher's handwritten checks and templates/handoff/handoff.schema.json
    must give the same verdict on the review's probe cases (T6-R2/T6-R2b)."""
    import json

    schema = json.loads(SCHEMA_SRC.read_text(encoding="utf-8"))

    def schema_ok(record):
        return not hp.schema_errors(record, schema)

    probes = [
        make_record(),                                                   # SHA-1, complete
        make_record(git_state=hp.GitState(state="current", root="/r", branch="main",
                                          head=VALID_HEAD_2, worktree="clean")),  # SHA-256
        make_record(git_state=hp.GitState(state="absent")),              # complete+absent
        make_record(status="partial", git_state=hp.GitState(state="absent")),
        make_record(git_state=hp.GitState(state="absent", head=VALID_HEAD_1)),  # fabricated head
        # T6-R2b's unprobed divergence: absent with a fabricated root
        make_record(status="partial",
                    git_state=hp.GitState(state="absent", root="/fabricated-root")),
        # complete with a failed check must be rejected by both sides
        make_record(checks=[hp.Check(name="c", state="failed", command="x",
                                     exit_code=1, evidence="e")]),
        make_record(status="partial",
                    git_state=hp.GitState(state="unknown", root="/r", branch="main")),
    ]
    for record in probes:
        code_ok = not hp.validate_record(record)
        assert code_ok == schema_ok(record), (
            f"code={code_ok} schema={schema_ok(record)} for status={record.status} "
            f"git={vars(record.git_state)}")


def test_absent_with_fabricated_root_rejected_by_both(tmp_path):
    """T6-R2b regression: absent Git state carrying a fabricated root is
    refused by the handwritten checks, the shipped schema, and publication."""
    import json

    record = make_record(status="partial",
                         git_state=hp.GitState(state="absent", root="/fabricated-root"))
    assert any("no fabricated Git identity" in e for e in hp.validate_record(record))
    schema = json.loads(SCHEMA_SRC.read_text(encoding="utf-8"))
    assert hp.schema_errors(record, schema)
    with pytest.raises(hp.PublishError):
        hp.publish(make_target(tmp_path), record)


def test_publication_requires_target_local_schema(tmp_path):
    """T6-R2b: publication without the clone-complete schema is refused, not
    degraded to the handwritten checks alone."""
    root = tmp_path / "bare-target"
    root.mkdir()
    with pytest.raises(hp.PublishError, match="missing target-local handoff schema"):
        hp.publish(root, make_record())
    assert not (root / "HANDOFF.md").exists()
    assert not (root / "support" / "handoffs").exists()


def test_schema_verdict_alone_blocks_publication(tmp_path):
    """T6-R2b: the shipped schema is authoritative at publication — a record
    the handwritten checks accept cannot publish if the target-local schema
    rejects it (modeled by a target whose installed schema is stricter)."""
    import json

    root = make_target(tmp_path)
    schema_file = root / "support" / "schemas" / "handoff.schema.json"
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    schema["properties"]["objective"] = {"type": "string", "minLength": 500}
    schema_file.write_text(json.dumps(schema), encoding="utf-8")

    record = make_record()
    assert hp.validate_record(record) == []
    with pytest.raises(hp.PublishError, match="schema validation failed"):
        hp.publish(root, record)
    assert not (root / "support" / "handoffs" / f"{record.record_id}.md").exists()


# --------------------------------------------------------------- boundaries

def test_sensitive_content_in_objective_rejected(tmp_path):
    record = make_record(objective="Rotate api_key: sk_live_abcdef1234567890 before merge.")
    with pytest.raises(hp.PublishError, match="sensitive content"):
        hp.publish(make_target(tmp_path), record)


def test_path_traversal_artifact_rejected(tmp_path):
    record = make_record(artifacts=["../../etc/passwd"])
    with pytest.raises(hp.PublishError, match="unsafe path"):
        hp.publish(make_target(tmp_path), record)


def test_missing_headings_on_parse_rejected(tmp_path):
    root = make_target(tmp_path)
    record = make_record()
    hp.publish(root, record)
    record_path = root / "support" / "handoffs" / f"{record.record_id}.md"
    corrupted = record_path.read_text(encoding="utf-8").replace("## Follow-up queue", "")
    with pytest.raises(hp.PublishError, match="missing required heading"):
        hp.parse_record(corrupted)


# --------------------------------------------------------------- Git collection

def _git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def test_collect_git_state_absent_for_non_repo(tmp_path):
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    state = hp.collect_git_state(plain)
    assert state.state == "absent"
    assert state.root is None and state.branch is None and state.head is None


@pytest.mark.skipif(subprocess.run(["git", "--version"], capture_output=True).returncode != 0,
                    reason="git is not available")
def test_collect_git_state_does_not_adopt_enclosing_repo(tmp_path):
    """T6-R1: a target root that merely sits inside some parent repository's
    worktree must report absent, not the parent's identity."""
    repo = tmp_path / "outer"
    repo.mkdir()
    _git(repo, "init", "-q")
    inner = repo / "not-a-repo-itself"
    inner.mkdir()
    state = hp.collect_git_state(inner)
    assert state.state == "absent"
    assert state.root is None and state.head is None


def test_atomic_write_no_clobber_never_overwrites(tmp_path):
    """T6-R7: finalization of an immutable record must fail, not overwrite,
    when the ID appeared concurrently."""
    target = tmp_path / "support" / "handoffs" / "2026-07-17T010000Z-abc1234.md"
    target.parent.mkdir(parents=True)
    target.write_text("first-writer content\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        hp._atomic_write(target, "second-writer content\n", no_clobber=True)
    assert target.read_text(encoding="utf-8") == "first-writer content\n"
    assert list(target.parent.glob(".*.tmp-*")) == []


def test_staleness_reports_upstream_and_worktree_divergence():
    """T6-R3: identical HEAD but changed upstream relation or worktree must
    still report divergence."""
    recorded = hp.GitState(state="current", root="/r", branch="main", head=VALID_HEAD_1,
                           upstream_relation="synchronized", worktree="clean")
    current = hp.GitState(state="current", root="/r", branch="main", head=VALID_HEAD_1,
                          upstream_relation="ahead-behind:1\t0", worktree="dirty")
    diffs = hp.compare_staleness(recorded, current)
    assert any(d.startswith("upstream_relation:") for d in diffs)
    assert any(d.startswith("worktree:") for d in diffs)


@pytest.mark.skipif(subprocess.run(["git", "--version"], capture_output=True).returncode != 0,
                    reason="git is not available")
def test_collect_git_state_and_staleness_on_real_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    (repo / "a.txt").write_text("one\n", encoding="utf-8")
    _git(repo, "add", "a.txt")
    _git(repo, "commit", "-q", "-m", "first")

    recorded = hp.collect_git_state(repo)
    assert recorded.state == "current"
    assert recorded.head is not None
    assert hp.compare_staleness(recorded, hp.collect_git_state(repo)) == []

    (repo / "b.txt").write_text("two\n", encoding="utf-8")
    _git(repo, "add", "b.txt")
    _git(repo, "commit", "-q", "-m", "second")
    current = hp.collect_git_state(repo)
    diffs = hp.compare_staleness(recorded, current)
    assert any(d.startswith("head:") for d in diffs)
