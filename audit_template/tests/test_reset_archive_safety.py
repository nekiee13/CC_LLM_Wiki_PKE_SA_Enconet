"""Live reset prerequisites: exact archive bytes and Windows raw-file removal."""
import importlib.util
from pathlib import Path
import stat
import sys
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Enconet/scripts'))
spec = importlib.util.spec_from_file_location('reset_safety', ROOT / 'audit_template/runtime_v2/reset_audit.py')
reset = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reset)


def fixture(root):
    (root / 'incoming').mkdir()
    (root / 'incoming/keep.md').write_text('owner document')
    (root / 'raw').mkdir()
    (root / 'raw/old.md').write_text('old controlled source')
    (root / 'raw/old.md').chmod(stat.S_IREAD)
    (root / 'manifests').mkdir()
    for name in ('manifests/ingest_runs.csv', 'manifests/link_exception_candidates.csv'):
        (root / name).write_text(reset.RESET_TEXT_FILES[name] + '\nstale\n')
    plan = root.parent / (root.name + '-plan.json')
    reset.write_plan(reset.build_plan(root), plan)
    return plan


def test_readonly_reset_and_fresh_ledgers(tmp_path):
    root = tmp_path / 'Company'
    root.mkdir()
    plan = fixture(root)
    result = reset.apply_plan(plan, root, tmp_path / 'backup', confirmation='RESET-AUDIT')
    assert not (root / 'raw/old.md').exists()
    assert (root / 'incoming/keep.md').read_text() == 'owner document'
    with ZipFile(result['backup']) as archive:
        assert archive.read('raw/old.md') == b'old controlled source'
    for name in ('manifests/ingest_runs.csv', 'manifests/link_exception_candidates.csv'):
        assert (root / name).read_text() == reset.RESET_TEXT_FILES[name] + '\n'


def test_wrong_archived_bytes_stop_before_delete(tmp_path, monkeypatch):
    root = tmp_path / 'Company'
    root.mkdir()
    plan = fixture(root)
    original = ZipFile.write
    def corrupt(self, filename, arcname=None, **kwargs):
        if arcname == 'raw/old.md':
            self.writestr(arcname, b'wrong bytes with correct filename')
        else:
            original(self, filename, arcname, **kwargs)
    monkeypatch.setattr(ZipFile, 'write', corrupt)
    with pytest.raises(reset.ResetError, match='hash mismatch'):
        reset.apply_plan(plan, root, tmp_path / 'backup', confirmation='RESET-AUDIT')
    assert (root / 'raw/old.md').read_text() == 'old controlled source'
    assert 'stale' in (root / 'manifests/ingest_runs.csv').read_text()
