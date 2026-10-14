"""Current v4 output paths; historic behavior is tested by the isolated suite."""
from pathlib import Path
import hashlib
import json
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import evidence_access_policy as policy
import generate_review_catalog as catalog
import generate_review_workspace as workspace
import build_review_package as package


def test_v4_evidence_boundary_is_exact_versioned_local_copy():
    versioned = ROOT.parent / 'audit_template/framework/v4/scripts/evidence_access_policy.py'
    local = ROOT / 'scripts/evidence_access_policy_v4.py'
    assert hashlib.sha256(local.read_bytes()).digest() == hashlib.sha256(versioned.read_bytes()).digest()
    result = policy.candidate_path('RUN-20990101-01', 'evidence_bundle.json')
    assert result == ROOT / 'outputs/RUN-20990101-01/evidence_bundle.json'
    policy.require_output_target(result)
    assert not result.exists()  # Path validation never generates a live artifact.


@pytest.mark.parametrize('name', ['../foreign', '..', 'x:stream', 'x\\y', 'trailing.'])
def test_v4_boundary_refuses_unsafe_artifact_names(name):
    with pytest.raises(policy.PolicyError):
        policy.candidate_path('RUN-20990101-01', name)


def test_old_nested_and_flat_targets_cannot_be_new_v4_outputs():
    for path in ('outputs/candidates/evidence_access/RUN-20990101-01/x.json',
                 'outputs/flat.json', 'outputs/RUN-20990101-01/nested/x.json'):
        with pytest.raises(policy.PolicyError):
            policy.require_output_target(ROOT / path)
    with pytest.raises(policy.PolicyError):
        policy.require_offline_entrypoint('python app.py')


def test_review_defaults_do_not_recreate_candidate_tree():
    reviews = ROOT / 'work/reviews'
    assert catalog.OUTPUT == workspace.CATALOG == package.CATALOG == reviews / 'review_catalog.json'
    assert workspace.OUTPUT == reviews / 'review_workspace.html'
    assert package.OUTPUT == reviews / 'portable_package'


def test_recorded_paths_resolve_without_rewriting_historical_registry():
    registry = ROOT / 'schemas/review_packages.yml'
    before = registry.read_bytes()
    paths = json.loads((ROOT / 'project-file-relocations.json').read_text(encoding='utf-8'))['paths']
    old, new = next((old, new) for old, new in paths.items() if old.startswith('out/'))
    expected = ROOT / new
    digest = hashlib.sha256(expected.read_bytes()).hexdigest()
    row = {'bundle': old, 'bundle_sha256': digest}
    data = catalog._verified_artifact(row, 'bundle', ROOT)
    assert package._source(ROOT, data['path']) == expected
    # A retained pre-reset registry is not an approval to borrow old evidence.
    historical = yaml.safe_load(before)['packages'][0]
    if not catalog._safe_path(ROOT, historical['bundle'], 'bundle').exists():
        with pytest.raises(ValueError, match='missing'):
            catalog._verified_artifact(historical, 'bundle', ROOT)
    assert registry.read_bytes() == before
