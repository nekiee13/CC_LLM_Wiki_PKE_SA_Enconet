"""Upgrade planning is read-only and must not hide local edits."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prepare_vendor
import preview_vendor_upgrade as planner


def install(tmp_path, monkeypatch):
    monkeypatch.setattr(prepare_vendor, 'WORKSPACE', tmp_path)
    target = tmp_path / 'Žuti Vendor'
    prepare_vendor.setup(target, target.name, 'preview-test', release='v2')
    return target


def snapshot(target):
    return {p.relative_to(target).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in target.rglob('*') if p.is_file()}


def test_preview_preserves_target_and_records_exact_hashes(tmp_path, monkeypatch):
    target = install(tmp_path, monkeypatch)
    before = snapshot(target)
    result = planner.preview(target)
    assert not result['blockers']
    assert result['counts']['add'] > 0 and result['counts']['replace'] > 0
    assert result['apply_supported'] is False
    assert snapshot(target) == before
    assert all(row['before_sha256'] for row in result['files'] if row['action'] != 'add')


def test_modified_framework_and_scaffold_are_blockers(tmp_path, monkeypatch):
    target = install(tmp_path, monkeypatch)
    (target / 'scripts/generate_report.py').write_bytes(b'local changes')
    (target / 'project-state.yml').write_bytes(b'phase: evaluated\n')
    result = planner.preview(target)
    assert any('scripts/generate_report.py' in item for item in result['blockers'])
    assert any('project-state.yml' in item for item in result['blockers'])


def test_any_company_input_or_database_stops_clean_upgrade(tmp_path, monkeypatch):
    target = install(tmp_path, monkeypatch)
    (target / 'incoming/owner.md').write_bytes(b'preserve owner document')
    (target / 'db/other.sqlite').write_bytes(b'not a clean scaffold')
    before = snapshot(target)
    assert planner.preview(target)['blockers']
    assert snapshot(target) == before


def test_crlf_is_explicit_equivalence_not_hidden_edit(tmp_path, monkeypatch):
    target = install(tmp_path, monkeypatch)
    path = target / 'scripts/generate_report.py'
    path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
    result = planner.preview(target)
    row = next(row for row in result['files'] if row['path'] == 'scripts/generate_report.py')
    assert row['baseline_match'] == 'crlf-lf-equivalent'
    assert not result['blockers']
