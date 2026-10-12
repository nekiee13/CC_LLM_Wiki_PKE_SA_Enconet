import importlib.util
import hashlib
import json
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
    assert result['passed'] and result['verified_files'] == 164
    assert not result['legacy_descriptive_labels']
    assert not result['code_findings'] and not result['configuration_findings']


def test_changed_payload_is_refused_before_path_claim(tmp_path):
    target = tmp_path / 'candidate'
    module('prepare_framework_candidate_v4').build(target)
    (target / 'scripts/init_db.py').write_text('old="manifests/legacy.csv"', encoding='utf-8')
    with pytest.raises(ValueError, match='checksum'):
        module('check_candidate_paths_v4').scan(target)


def test_recorded_lookup_is_visible_but_direct_legacy_access_still_fails(tmp_path):
    target = tmp_path / 'candidate'
    (target / 'scripts').mkdir(parents=True)
    body = (b'from project_records import recorded_path\n'
            b'a = recorded_path("outputs/candidates/old.json")\n'
            b'b = "outputs/candidates/unsafe.json"\n')
    (target / 'scripts/runtime.py').write_bytes(body)
    (target / 'candidate-manifest.json').write_text(json.dumps({'files': [{
        'path': 'scripts/runtime.py', 'bytes': len(body),
        'sha256': hashlib.sha256(body).hexdigest()}]}), encoding='utf-8')
    result = module('check_candidate_paths_v4').scan(target)
    assert not result['passed']
    assert [r['value'] for r in result['code_findings']] == ['outputs/candidates/unsafe.json']
    assert [r['value'] for r in result['legacy_record_lookups']] == ['outputs/candidates/old.json']
