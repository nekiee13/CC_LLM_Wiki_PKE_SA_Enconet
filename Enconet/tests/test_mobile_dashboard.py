"""A mobile correction is additive CSS, never an audit-data rewrite."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_mobile_dashboard as mobile

SOURCE = b'<html>\r\n<head></head><body><section id="artifact-metadata">hash</section><script>{"score":80.6}</script></body></html>'


def test_only_screen_style_is_added():
    revised = mobile.mobile_copy(SOURCE)
    assert revised.replace(mobile.STYLE, b'', 1) == SOURCE
    assert b'media="screen"' in mobile.STYLE
    assert b'#artifact-metadata{overflow-wrap:anywhere}' in mobile.STYLE
    assert b'<script>{"score":80.6}</script>' in revised


def test_build_preserves_source_and_refuses_overwrite(tmp_path):
    source = tmp_path / 'original.html'
    source.write_bytes(SOURCE)
    output = tmp_path / 'revision' / 'dashboard_light.html'
    receipt = mobile.build(source, output)
    assert source.read_bytes() == SOURCE
    assert receipt['original_bytes_preserved'] is True
    assert receipt['source_sha256'] != receipt['output_sha256']
    with pytest.raises(FileExistsError):
        mobile.build(source, output)
    with pytest.raises(ValueError):
        mobile.build(source, source)


def test_refuses_wrong_or_already_corrected_page():
    with pytest.raises(ValueError):
        mobile.mobile_copy(b'<head></head>')
    with pytest.raises(ValueError):
        mobile.mobile_copy(mobile.mobile_copy(SOURCE))


def test_refuses_redirected_destination_parent(tmp_path, monkeypatch):
    source = tmp_path / 'original.html'
    source.write_bytes(SOURCE)
    redirected = tmp_path / 'redirected'
    redirected.mkdir()
    original = Path.is_symlink
    monkeypatch.setattr(Path, 'is_symlink', lambda path: path == redirected or original(path))
    with pytest.raises(ValueError, match='(?i)redirect'):
        mobile.build(source, redirected / 'revision.html')
