"""Company-neutral offline candidate and controlled-publication boundary."""
from pathlib import Path
import re
import yaml

PROJECT = Path(__file__).resolve().parents[1]
CANDIDATE_ROOT = PROJECT/'outputs/candidates/evidence_access'


class PolicyError(ValueError):
    pass


def candidate_path(run_id, artifact_name):
    if not re.fullmatch(r'RUN-[0-9]{8}-[0-9]{2}',run_id):
        raise PolicyError('Invalid local run identity')
    if not artifact_name or Path(artifact_name).name != artifact_name:
        raise PolicyError('Candidate requires one filename')
    return CANDIDATE_ROOT/run_id/artifact_name


def require_offline_entrypoint(entrypoint):
    if any(v in entrypoint.casefold() for v in ('streamlit','uvicorn','flask','fastapi','http.server')):
        raise PolicyError('Offline delivery does not authorize an app server')


def require_output_target(target, *, owner_approval_ref=None, independent_review_ref=None,
                          validations_passed=False, atomic_promotion=False):
    target = Path(target).resolve()
    if target.is_relative_to(CANDIDATE_ROOT.resolve()):
        return
    state = yaml.safe_load((PROJECT/'project-state.yml').read_text(encoding='utf-8'))
    supplier = re.sub(r'[^a-z0-9_-]+','-',state['supplier'].casefold()).strip('-')
    reports = {PROJECT/f'outputs/{supplier}_appendix_b_evaluation_report.md'}
    dashboards = {PROJECT/f'outputs/{supplier}_appendix_b_dashboard.html',
                  PROJECT/f'outputs/{supplier}_appendix_b_dashboard_data.json',
                  PROJECT/f'wiki/dashboards/{supplier}_appendix_b_dashboard.html'}
    if target not in reports|dashboards:
        raise PolicyError('Output is outside local candidates or controlled paths')
    gate = 'G5' if target in reports else 'G6'
    if not owner_approval_ref or not owner_approval_ref.startswith(gate+'-'):
        raise PolicyError(f'{gate} owner approval required')
    if not independent_review_ref or not validations_passed or not atomic_promotion:
        raise PolicyError('Controlled publication requires review, validation and atomic promotion')
