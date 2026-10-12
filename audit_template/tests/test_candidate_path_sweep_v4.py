import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_verified_candidate_has_no_direct_operational_legacy_paths(tmp_path):
    target = tmp_path / 'candidate'
    module('prepare_framework_candidate_v4').build(target)
    result = module('check_candidate_paths_v4').scan(target)
    assert result['passed'] and result['verified_files'] == 163
    assert not result['code_findings'] and not result['configuration_findings']


def test_changed_payload_is_refused_before_path_claim(tmp_path):
    target = tmp_path / 'candidate'
    module('prepare_framework_candidate_v4').build(target)
    (target / 'scripts/init_db.py').write_text('old="manifests/legacy.csv"', encoding='utf-8')
    with pytest.raises(ValueError, match='checksum'):
        module('check_candidate_paths_v4').scan(target)
