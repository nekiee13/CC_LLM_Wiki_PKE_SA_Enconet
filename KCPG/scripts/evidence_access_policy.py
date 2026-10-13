"""Candidate v4 offline output boundary; files are not a publication marker.

Candidate artifacts belong directly under outputs/RUN-ID. Audit source checks
and manifest-backed report/dashboard gates remain enforced by their generators.
This policy does not authorize result publication or replacement.
"""
from pathlib import Path

from project_layout import path, run_output, guard


class PolicyError(ValueError):
    pass


def candidate_path(run_id, artifact_name):
    if not isinstance(artifact_name, str) or not artifact_name or Path(artifact_name).name != artifact_name:
        raise PolicyError('Candidate requires one filename')
    if (artifact_name in {'.', '..'} or ':' in artifact_name or '\\' in artifact_name
            or artifact_name.endswith((' ', '.')) or any(ord(char) < 32 for char in artifact_name)):
        raise PolicyError('Unsafe candidate filename')
    try:
        return guard(run_output(run_id) / artifact_name)
    except ValueError as exc:
        raise PolicyError(str(exc)) from exc


def require_offline_entrypoint(entrypoint):
    if any(value in entrypoint.casefold() for value in ('streamlit', 'uvicorn', 'flask', 'fastapi', 'http.server')):
        raise PolicyError('Offline delivery does not authorize an app server')


def require_output_target(target, *, owner_approval_ref=None, independent_review_ref=None,
                          validations_passed=False, atomic_promotion=False):
    # No flat published aliases in v4: publication is a separate hash-pinned tool.
    try:
        target = guard(Path(target).absolute())
        relative = target.relative_to(path('outputs'))
        if len(relative.parts) != 2:
            raise ValueError('Use one artifact directly under outputs/RUN-ID')
        if candidate_path(relative.parts[0], relative.parts[1]) != target:
            raise ValueError('Output target differs from candidate path')
    except ValueError as exc:
        raise PolicyError(str(exc)) from exc
