#!/usr/bin/env python3
"""Executable EA0.2 governance contract for evidence-access delivery."""
from __future__ import annotations

import re
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]
CANDIDATE_ROOT = ENCONET / "outputs" / "candidates" / "evidence_access"
APPROVED_ARTIFACT_SHA256 = {
    "outputs/enconet_appendix_b_evaluation_report.md":
        "0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175",
    "outputs/enconet_appendix_b_evaluation_report_hr.md":
        "0af3981811ef13ba942d6ea924f3ab16675326415d2fb10e7c06097663a14175",
    "outputs/enconet_appendix_b_dashboard.html":
        "15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07",
    "outputs/enconet_appendix_b_dashboard_hr.html":
        "15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07",
    "outputs/enconet_appendix_b_dashboard_data.json":
        "528cbe51dc8711f1e93d55f431518eba68425d470bd2df9d32a624ec1abe5b71",
    "outputs/enconet_dashboard_data_hr.json":
        "528cbe51dc8711f1e93d55f431518eba68425d470bd2df9d32a624ec1abe5b71",
    "wiki/dashboards/enconet_appendix_b_dashboard.html":
        "15aced5b1c8237f906e9b1794a19fc06ec39ec9bc8801eba2779e6c207b98e07",
}

_FORBIDDEN_ENTRYPOINT_MARKERS = (
    "streamlit",
    "uvicorn",
    "flask",
    "fastapi",
    "http.server",
    "gunicorn",
    "hypercorn",
    "app.py",
    "evidence_server.py",
    "serve_evidence.py",
)


class PolicyError(ValueError):
    """Raised when evidence-access work would violate an owner decision."""


def require_offline_entrypoint(entrypoint: str) -> None:
    """Reject a live application-server entrypoint while ADR-0007 is active."""
    normalized = entrypoint.casefold()
    if any(marker in normalized for marker in _FORBIDDEN_ENTRYPOINT_MARKERS):
        raise PolicyError(
            "ADR-0007 forbids Streamlit/app-server evidence entrypoints until a superseding ADR"
        )


def candidate_path(run_id: str, artifact_name: str) -> Path:
    """Return the only ordinary write location for an evidence-access artifact."""
    if re.fullmatch(r"RUN-[0-9]{8}-[0-9]{2}", run_id) is None:
        raise PolicyError(f"invalid run ID for candidate output: {run_id}")
    if Path(artifact_name).name != artifact_name or not artifact_name:
        raise PolicyError(f"candidate artifact must be one plain filename: {artifact_name}")
    return CANDIDATE_ROOT / run_id / artifact_name


def _relative_to_project(target: Path) -> str | None:
    try:
        return target.resolve().relative_to(ENCONET.resolve()).as_posix()
    except ValueError:
        return None


def _inside_candidate_root(target: Path) -> bool:
    try:
        target.resolve().relative_to(CANDIDATE_ROOT.resolve())
        return True
    except ValueError:
        return False


def require_output_target(
    target: Path,
    *,
    owner_approval_ref: str | None = None,
    independent_review_ref: str | None = None,
    validations_passed: bool = False,
    atomic_promotion: bool = False,
) -> None:
    """Allow candidate writes; gate every write to an approved published artifact."""
    if _inside_candidate_root(target):
        return

    relative = _relative_to_project(target)
    if relative not in APPROVED_ARTIFACT_SHA256:
        raise PolicyError(
            "output target is neither the evidence-access candidate root nor an approved artifact"
        )

    required_gate = "G5" if "evaluation_report" in relative else "G6"
    if not owner_approval_ref or not owner_approval_ref.startswith(required_gate + "-"):
        raise PolicyError(f"{required_gate} owner approval is required before published overwrite")
    if not independent_review_ref:
        raise PolicyError("independent review is required before published overwrite")
    if not validations_passed:
        raise PolicyError("validation must pass before published overwrite")
    if not atomic_promotion:
        raise PolicyError("atomic promotion is required for published overwrite")
