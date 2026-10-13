import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
from validate_release_relocations import verify, rehearse


def fixture(root):
    folder = root / 'Vendor Ž/outputs/old'
    folder.mkdir(parents=True)
    data = b'unchanged report\n'
    (folder / 'report.md').write_bytes(data)
    manifest = {'files': [{'path': 'report.md', 'bytes': len(data),
                           'sha256': hashlib.sha256(data).hexdigest()}]}
    (folder / 'release_manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    rows = []
    for name in ('report.md', 'release_manifest.json'):
        source = folder / name
        rows.append({'source': 'Vendor Ž/outputs/old/' + name,
                     'destination': 'Vendor Ž/outputs/RUN-1/revisions/' + name,
                     'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    return {'schema': 'cleanup-file-map-1', 'files': rows}, folder


def test_planned_and_relocated_manifest_use_retained_original(tmp_path):
    plan, folder = fixture(tmp_path)
    original_manifest = (folder / 'release_manifest.json').read_bytes()
    result = verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'planned')
    assert result['passed'] and result['verified'] == 1
    for row in plan['files']:
        target = tmp_path / row['destination']
        target.parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / row['source']).rename(target)
    result = verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'relocated')
    assert result['passed']
    assert (tmp_path / plan['files'][1]['destination']).read_bytes() == original_manifest


def test_hash_failure_is_reported_not_accepted(tmp_path):
    plan, folder = fixture(tmp_path)
    (folder / 'report.md').write_bytes(b'changed')
    result = verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'planned')
    assert not result['passed'] and result['verified'] == 0


def test_wrong_map_hash_and_unsafe_member_rejected(tmp_path):
    plan, folder = fixture(tmp_path)
    plan['files'][0]['sha256'] = '0' * 64
    assert not verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'planned')['passed']
    manifest = json.loads((folder / 'release_manifest.json').read_text())
    manifest['files'][0]['path'] = '../../outside.md'
    (folder / 'release_manifest.json').write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match='unsafe'):
        verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'original')


def test_foreign_map_refused(tmp_path):
    plan, folder = fixture(tmp_path)
    plan['files'][0]['destination'] = 'Other/outputs/report.md'
    with pytest.raises(ValueError, match='foreign'):
        verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'planned')


def test_rehearsal_copies_to_new_homes_without_changing_live_files(tmp_path):
    plan, folder = fixture(tmp_path)
    original = (folder / 'release_manifest.json').read_bytes()
    destination = tmp_path / '.tmp/rehearsal'
    result = rehearse(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, destination)
    assert result['passed'] and result['live_files_unchanged'] and result['copied_files'] == 2
    assert (folder / 'release_manifest.json').read_bytes() == original
    with pytest.raises(ValueError, match='fresh'):
        rehearse(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, destination)


def test_publication_artifact_manifest_uses_supplier_relative_destinations(tmp_path):
    plan, folder = fixture(tmp_path)
    data = {'schema_version': 1, 'run_id': 'RUN-20261013-01', 'artifacts': [{
        'source': 'out/staging/report.md', 'destination': 'outputs/old/report.md',
        'sha256': plan['files'][0]['sha256']}]}
    manifest = folder / 'release_manifest.json'
    manifest.write_text(json.dumps(data), encoding='utf-8')
    plan['files'][1]['sha256'] = hashlib.sha256(manifest.read_bytes()).hexdigest()
    original = manifest.read_bytes()
    assert verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan)['passed']
    for row in plan['files']:
        target = tmp_path / row['destination']
        target.parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / row['source']).rename(target)
    result = verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'relocated')
    assert result['passed'] and result['verified'] == 1
    assert (tmp_path / plan['files'][1]['destination']).read_bytes() == original
    (tmp_path / plan['files'][0]['destination']).write_bytes(b'changed')
    assert not verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'relocated')['passed']


def test_publication_manifest_rejects_unsafe_source_and_ambiguous_schema(tmp_path):
    plan, folder = fixture(tmp_path)
    data = {'schema_version': 1, 'run_id': 'RUN-20261013-01', 'artifacts': [{
        'source': '../outside', 'destination': 'outputs/old/report.md',
        'sha256': plan['files'][0]['sha256']}]}
    manifest = folder / 'release_manifest.json'
    manifest.write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(ValueError, match='unsafe'):
        verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'original')
    data['artifacts'][0]['source'] = 'out/staging/report.md'
    data['files'] = []
    manifest.write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(ValueError, match='manifest'):
        verify(tmp_path, 'Vendor Ž', 'outputs/old/release_manifest.json', plan, 'original')
