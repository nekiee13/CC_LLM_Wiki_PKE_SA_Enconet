import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import prepare_supplier_runtime_install as preparation


def synthetic(root):
    supplier = 'Synthetic Ž'
    original = root / supplier / 'scripts/runtime.py'
    original.parent.mkdir(parents=True)
    original.write_bytes(b'original\n')
    old = root / supplier / 'out/old/file.json'
    old.parent.mkdir(parents=True)
    old.write_bytes(b'{}')
    overlay = root / '.tmp/overlay'
    bodies = {'scripts/runtime.py': b'updated\n', 'scripts/helper.py': b'helper\n',
              'project-layout.json': b'{"schema_version":1,"layout":"v4"}',
              'project-file-relocations.json': b'{"schema_version":1,"paths":{}}'}
    for name, body in bodies.items():
        target = overlay / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
    sha = lambda body: hashlib.sha256(body).hexdigest()
    manifest = {'source_supplier': supplier, 'holds': [], 'install_paths': list(bodies),
                'files': [{'path': name, 'sha256': sha(body)} for name, body in bodies.items()],
                'changes': [{'path': 'scripts/runtime.py', 'before_sha256': sha(original.read_bytes())}]}
    (overlay / 'candidate-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    file_map = root / '.tmp/map.json'
    file_map.write_text(json.dumps({'schema': 'cleanup-file-map-1', 'files': [
        {'source': supplier + '/out/old/file.json', 'destination': supplier + '/outputs/RUN-1/file.json',
         'sha256': sha(old.read_bytes()), 'owner': 'shared-or-owner'}], 'collisions': []}), encoding='utf-8')
    return supplier, overlay, file_map, original


def test_preparation_binds_actual_install_manifest_and_aliases(tmp_path, monkeypatch):
    monkeypatch.setattr(preparation, 'WORKSPACE', tmp_path)
    supplier, overlay, file_map, original = synthetic(tmp_path)
    destination = tmp_path / '.tmp/installation'
    result = preparation.prepare(supplier, overlay, file_map, destination, 'work/migrations/test/originals')
    assert result['files'] == 4
    assert original.read_bytes() == b'original\n'
    assert not (tmp_path / supplier / 'work').exists()
    plan = json.loads((destination / 'installation-plan.json').read_text(encoding='utf-8'))
    assert plan['files'][-1]['target'] == supplier + '/project-layout.json'
    assert preparation.installer.preview(tmp_path, plan)['files'] == 4
    aliases = json.loads((destination / 'payload/project-file-relocations.json').read_text(encoding='utf-8'))
    assert aliases['paths']['work/validation/old/file.json'] == 'outputs/RUN-1/file.json'


def test_runtime_drift_refused_before_scratch_creation(tmp_path, monkeypatch):
    monkeypatch.setattr(preparation, 'WORKSPACE', tmp_path)
    supplier, overlay, file_map, original = synthetic(tmp_path)
    original.write_bytes(b'owner edit')
    destination = tmp_path / '.tmp/installation'
    with pytest.raises(ValueError, match='runtime differs'):
        preparation.prepare(supplier, overlay, file_map, destination, 'work/migrations/test/originals')
    assert not destination.exists()
