"""Render the exact first CC_Loto support slice without writing CC_Loto."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

WIKI = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WIKI / "doc" / "support-transfer" / "staged"))
from _shared import scan_sensitive

TEMPLATES = WIKI / "doc" / "support-transfer" / "templates"
OUT = WIKI / "doc" / "support-transfer" / "rendered" / "loto"
LOTO = Path(r"C:\xPY\xPrj\CC_Loto")
BASE = "b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--timestamp", help="fixed UTC timestamp (YYYY-MM-DDTHH:MM:SSZ)")
args = parser.parse_args()
if args.timestamp:
    datetime.strptime(args.timestamp, "%Y-%m-%dT%H:%M:%SZ")
now = args.timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

profile_source = (WIKI / "doc" / "support-transfer" / "CC_LOTO_SUPPORT_PROFILE.md").read_text(
    encoding="utf-8"
)
profile = re.sub(
    r"\A# CC_Loto support profile v1\.0\n\n## Control\n.*?(?=\n## Identity, roles, and authority)",
    """# CC_Loto support profile (target-local controlled authority)

## Control

- Repository: `https://github.com/nekiee13/CC_Loto` (`main`)
- Record class: Controlled (see [RECORD-KEEPING.md](RECORD-KEEPING.md))
- Accepted publication baseline: `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`
- Provenance: profile v1.0 approved by the human owner at M1; FIN accepted and Loto
  publication authorized at M3 on 2026-07-18, conditional on exact target-local review.
- Product authority: `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`.
- This target-local profile governs support workflow only and never replaces product authority.
""".rstrip(),
    profile_source,
    flags=re.S,
)
profile = profile.replace(
    "Loto publication cannot start until FIN acceptance at M3. It then uses small reversible",
    "M3 accepted the FIN pilot and authorized Loto publication. Publication uses small reversible",
)
profile = profile.replace("## M1 acceptance conditions", "## Installation authority")
profile = profile.replace(
    "- The owner accepts this version and exact baseline SHA.",
    "- The owner accepted this version and exact baseline SHA at M1.",
)
profile = profile.replace(
    "- Publication remains deferred until FIN acceptance at M3.",
    "- Publication was authorized at M3 subject to exact-render, dry-run, briefing, and review controls.",
)
profile = profile.replace(
    "- Native `run_tests.py` and optional-layer semantics are accepted.",
    "- Native `run_tests.py` and optional-layer semantics remain mandatory.",
)
profile = profile.replace(
    "- U7 integration, data exclusions, and initially disabled modules are accepted.",
    "- U7 integration, data exclusions, and initially disabled modules remain accepted.",
)
profile = profile.replace(
    "Loto publication cannot start until FIN pilot acceptance at M3. It then uses small reversible\n"
    "commits on `main`, exact-baseline/clean-tree preflight, and independent review before push.",
    "M3 accepted the FIN pilot and authorized Loto publication. Loto uses small reversible\n"
    "commits on `main`, exact-baseline/clean-tree preflight, and independent review before push.",
)

ownership = (
    "Codex owns `AGENTS.md`, `.agents/`, and `CX_` records. Claude owns `CLAUDE.md`, "
    "`.claude/`, and `CC_` records. Neutral coordination, support schemas, decision registers, "
    "logs, handoffs, and generated board/status views are shared by contract. The human owner "
    "decides gates, authority changes, destructive recovery, hosted changes, tags, and releases."
)

authorities = """- Enhanced product plan: `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`
- Architecture: `docs/architecture.md`; dated AS-IS: `docs/AS-IS.md`
- Earlier-plan progress: `docs/PROGRESS.md`; roadmap/history: `docs/ROADMAP.md`
- Packaging: `pyproject.toml`, `requirements.txt`, and `requirements.lock`
- Hosted CI: `.github/workflows/ci.yml`"""

values = {
    "PROJECT_NAME": "CC_Loto",
    "PRODUCT_PLAN_PATH": "docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md",
    "SUPPORT_PROFILE_PATH": "support/PROFILE.md",
    "UTC_TIMESTAMP": now,
    "GIT_HEAD": BASE + " (pre-slice parent; this status first lands in content commit A)",
    "UPSTREAM_RELATION": "synchronized 0 0 with origin/main at observation",
    "WORKTREE_STATE": "clean at observation; no support-transfer target write has occurred",
    "SUPPORT_MILESTONE": (
        "M3 approved FIN acceptance and conditional Loto publication; exact Slice 1 render and "
        "disposable proof are under pre-push review; M4 remains closed"
    ),
    "ACTIVE_WORK_SUMMARY": (
        "- Slice 1 contains exactly eight neutral support records and no existing-file modification.\n"
        "- Coordination, handoff, index closure, Codex guidance, and target-native aggregate remain "
        "later separately reviewed slices."
    ),
    "COORDINATION_SUMMARY": (
        "The target-local coordination core is not installed in Slice 1. Cross-agent preparation "
        "remains in the workspace neutral channel; no target message or claim is implied."
    ),
    "VALIDATION_SUMMARY": (
        "A disposable isolated environment installed the target's declared `requirements.txt`. With "
        "short redirected runtime paths and explicit `--pattern test*.py`, the native runner passed "
        "`core-unit` (42/42), `contract` (25/25), and `state-integrity` (3/3): 70/70 required short-layer "
        "tests. Contract and state-integrity were rerun outside the filesystem sandbox after sandbox-only "
        "Windows temp-directory denials. A separate `webapp` run exceeded 120 seconds without a result and "
        "was terminated; this documentation-only slice does not require webapp execution. The default full "
        "run also has no final result and is recorded as unavailable, not passed. CC_Loto remained clean."
    ),
    "NEXT_ACTION_OWNER": "claude-code (independent reviewer), then codex (implementer)",
    "NEXT_ACTION_PREREQUISITES": "exact render, disposable evidence, and native short-layer evidence accepted",
    "NEXT_ACTION": (
        "Review the eight exact blobs, link/sensitivity checks, disposable overlay, and literal native "
        "baseline. After acceptance, Codex applies only the reviewed Slice 1 "
        "bytes and uses content-A/evidence-B commits."
    ),
    "NEXT_ACTION_STOP_CONDITION": (
        "Any target drift, extra path, byte mismatch, secret/product-data exposure, unresolved link, "
        "unreviewed native-baseline assumption, or reviewer finding"
    ),
    "STATUS_EVIDENCE_LINKS": (
        "- Slice preparation event in [log.md](log.md)\n"
        "- Record classes in [RECORD-KEEPING.md](RECORD-KEEPING.md)\n"
        "- Sensitivity, native-runner, module, and recovery authority in [PROFILE.md](PROFILE.md)"
    ),
    "TARGET_DECISION_AUTHORITIES": authorities,
}


def render(template: str) -> str:
    text = (TEMPLATES / f"{template}.template.md").read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if unresolved:
        raise RuntimeError(f"{template}: unresolved placeholders {unresolved}")
    return text


recordkeeping = render("record-keeping").replace(
    "| `support/README.md` | Controlled |",
    "| `support/README.md` (arrives with the index-closure slice) | Controlled |\n"
    "| `support/PROFILE.md` | Controlled |",
)
log = render("event-log").rstrip("\n") + "\n" + (
    f"support-prepared | {now} | LOTO-SLICE-1 | Eight neutral support records rendered for "
    "the M3-authorized first Loto slice; link/sensitivity/disposable checks are required before "
    "target write; a disposable dependency-complete environment passed the explicitly discovered "
    "core-unit, contract, and state-integrity short layers (70/70), while default-full and webapp "
    "runs produced no final result within their limits and remain unavailable; implementer codex, "
    "reviewer claude-code | codex\n"
)

outputs = {
    "support/PROFILE.md": profile,
    "support/current-status.md": render("current-status"),
    "support/log.md": log,
    "support/RECORD-KEEPING.md": recordkeeping,
    "support/decisions/README.md": render("adr-register"),
    "support/AFI.md": render("afi-ledger"),
    "support/LESSONS-LEARNED.md": render("lessons-ledger"),
    "support/GOOD-PRACTICES.md": render("good-practices-ledger"),
}

errors: list[str] = []
for relative, text in outputs.items():
    hits = scan_sensitive(text)
    if hits:
        errors.append(f"{relative}: sensitive {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "xPY", "C:\\"):
        if token in text:
            errors.append(f"{relative}: forbidden reference {token!r}")
    for match in re.finditer(r"\]\(([^)#\s]+)\)", text):
        link = match.group(1)
        if link.startswith(("http://", "https://")):
            continue
        source_dir = Path(relative).parent
        parts: list[str] = []
        for segment in (source_dir / link).as_posix().split("/"):
            if segment == "..":
                if parts:
                    parts.pop()
            elif segment != ".":
                parts.append(segment)
        normalized = "/".join(parts)
        if normalized not in outputs and not (LOTO / normalized).exists():
            errors.append(f"{relative}: unresolved link {link!r} -> {normalized}")
if errors:
    raise RuntimeError("\n".join(errors))

if OUT.exists():
    shutil.rmtree(OUT)
for relative, text in outputs.items():
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"rendered {relative} ({len(text.splitlines())} lines)")
print("ALL CHECKS PASSED: exact eight files; no sensitive/Wiki/private paths; links resolve")
