"""T6.4 scoped-recovery rehearsal: proof, not restatement.

Runs entirely inside a disposable Git repository seeded with an unrelated
pre-existing product file and a placeholder native check, per
``T6_VALIDATION_RECOVERY_GATE_CONTRACT.md`` Task T6.4 and the scoped-rollback
procedure in ``PUBLICATION_ROLLBACK_MANIFESTS.md``. It publishes a
multi-commit support slice with unrelated concurrent work landing mid-slice,
injects a failure partway through, aborts, and reverts only the slice's own
commits -- then asserts pre-existing and concurrent files are byte-identical,
verifies the recovered state by Git diff against the recovery point, and
re-runs the native check and the coordination validator against the recovered
tree. Nothing here touches CC_FIN or CC_Loto.
"""

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest

import coordination_validator as cv
import handoff_publisher as hp

STAGED_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_COORD = STAGED_DIR.parent / "templates" / "coordination"

pytestmark = pytest.mark.skipif(
    subprocess.run(["git", "--version"], capture_output=True).returncode != 0,
    reason="git is not available",
)


def _git(root: Path, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=root, check=True,
                         capture_output=True, text=True)
    return out.stdout.strip()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_native_check(root: Path) -> tuple[int, str]:
    """Placeholder native check standing in for the target's own test suite."""
    marker = root / "unrelated_product_file.txt"
    if marker.is_file() and marker.read_text(encoding="utf-8").strip() == "pre-existing product content":
        return 0, "placeholder native check: pre-existing product file intact"
    return 1, "placeholder native check: pre-existing product file missing or changed"


def test_scoped_recovery_rehearsal(tmp_path):
    repo = tmp_path / "disposable-target"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "rehearsal@example.com")
    _git(repo, "config", "user.name", "Rehearsal")

    # --- seed: unrelated pre-existing product file (must survive rollback) --
    unrelated = repo / "unrelated_product_file.txt"
    unrelated.write_text("pre-existing product content\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "baseline: pre-existing product state")
    recovery_point = _git(repo, "rev-parse", "HEAD")
    unrelated_hash_before = _sha256(unrelated)

    exit_code, evidence = _run_native_check(repo)
    assert exit_code == 0, evidence

    # --- slice commit 1: neutral coordination skeleton -----------------------
    coord = repo / "coordination"
    for sub in ("messages", "archive", "claims", "schemas"):
        (coord / sub).mkdir(parents=True)
        (coord / sub / ".gitkeep").write_text("", encoding="utf-8")
    for name in ("message.schema.json", "claim.schema.json",
                "resolution-manifest.schema.json"):
        shutil.copy(TEMPLATES_COORD / name, coord / "schemas" / name)
    cv.write_board(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "support slice: neutral coordination skeleton")
    skeleton_commit = _git(repo, "rev-parse", "HEAD")

    # --- concurrent unrelated work landing DURING the slice (T6-R6): a change
    #     introduced after the recovery point, outside the transfer commits;
    #     scoped rollback must preserve it, not sweep it away ------------------
    concurrent = repo / "concurrent_work.txt"
    concurrent.write_text("another actor's change during the slice\n", encoding="utf-8")
    _git(repo, "add", "concurrent_work.txt")
    _git(repo, "commit", "-q", "-m", "unrelated: concurrent product work mid-slice")
    concurrent_hash_before = _sha256(concurrent)

    # --- slice commit 2: one coordination message -----------------------------
    msg_path = coord / "messages" / "CC_20260717T020000Z_rehearsal.md"
    msg_path.write_text(
        "---\n"
        "message_id: CC_20260717T020000Z_rehearsal\n"
        "created_at_utc: 2026-07-17T02:00:00Z\n"
        "from_agent: claude-code\n"
        "to_agent: codex\n"
        "type: note\n"
        "task: T6.4-REHEARSAL\n"
        "related_files: []\n"
        "---\n\n"
        "Scoped-recovery rehearsal in progress.\n",
        encoding="utf-8",
    )
    cv.write_board(repo)
    result = cv.validate(repo)
    assert result.ok, result.errors
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "support slice: coordination message")
    coordination_commit = _git(repo, "rev-parse", "HEAD")

    # --- injected failure before the handoff commit: abort ---------------------
    record = hp.HandoffRecord(
        record_id="2026-07-17T020500Z-abc1234",
        created_at_utc="2026-07-17T02:05:00Z",
        source_agent="claude-code",
        status="complete",
        objective="Rehearsal handoff.",
        checks=[hp.Check(name="native", state="failed", command="run_native_check",
                         exit_code=1, evidence="injected failure for the rehearsal")],
        git_state=hp.GitState(state="current", root=str(repo), branch="master",
                              head=coordination_commit, worktree="dirty"),
        next_action=hp.NextAction(owner="claude-code", action="n/a",
                                  stop_condition="n/a"),
    )
    with pytest.raises(hp.PublishError):
        hp.publish(repo, record)
    assert not (repo / "support").exists()
    assert not (repo / "HANDOFF.md").exists()

    # --- scoped rollback: revert only the slice commits, most-recent first ----
    _git(repo, "revert", "--no-edit", coordination_commit)
    _git(repo, "revert", "--no-edit", skeleton_commit)

    # --- assertions: pre-existing and concurrent files are byte-identical -----
    assert _sha256(unrelated) == unrelated_hash_before
    assert _sha256(concurrent) == concurrent_hash_before
    # Git only guarantees tracked *files* are removed by the revert, not that
    # an emptied directory is pruned from disk; the schema file's absence is
    # what the validator (and the assertion below) actually depends on.
    assert not (coord / "schemas" / "message.schema.json").exists()

    # --- history is preserved, never rewritten ---------------------------------
    log = _git(repo, "log", "--oneline")
    # baseline, skeleton, concurrent, message, 2 reverts
    assert log.count("\n") + 1 == 6
    assert recovery_point in _git(repo, "rev-list", "HEAD")

    # --- Git diff verification of the recovered state (T6-R6): relative to the
    #     recovery point, only the concurrent unrelated work remains -----------
    diff_names = _git(repo, "diff", "--name-only",
                      f"{recovery_point}..HEAD").splitlines()
    assert diff_names == ["concurrent_work.txt"], diff_names
    assert _git(repo, "status", "--porcelain") == ""

    # --- post-rollback verification: native check plus coordination validator -
    exit_code, evidence = _run_native_check(repo)
    assert exit_code == 0, evidence
    recovered_result = cv.validate(repo)
    assert any("missing required schema" in e for e in recovered_result.errors), (
        "coordination/ was fully reverted; validator must report its absence, "
        "not silently pass"
    )
