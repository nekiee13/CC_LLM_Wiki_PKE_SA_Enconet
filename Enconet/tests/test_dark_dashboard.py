"""Dark presentation must preserve the released light page and audit payload."""
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_dark_dashboard as dark

SOURCE = '<!doctype html><html><head><style>@media print{body{background:white}}</style></head><body><main id="criterion-card-container"></main><script id="dashboard-data" type="application/json">{"score":80.6}</script><script>function filterCriteria(){return 18;}</script></body></html>'


def test_original_scripts_and_markup_preserved():
    result = dark.dark_copy(SOURCE)
    for script in re.findall(r'<script.*?</script>', SOURCE, re.S):
        assert script in result
    assert '@media print{body{background:white}}' in result
    assert '<style id="audit-dark-skin" media="screen">' in result
    assert 'id="criterion-card-container"' in result


def test_current_dashboard_has_dark_surface_tokens():
    css = dark.STYLE.read_text(encoding="utf-8")
    assert '--paper:var(--u-bg-0)' in css
    assert '--card:var(--u-surface-1)' in css
    assert '#dashboard-header' in css
    assert '.criterion-card' in css and '.evidence-drawer' in css
    assert 'radial-gradient' in css and 'background-size:54px 54px' in css


def test_reference_grouping_handles_current_and_legacy_containers():
    script = dark.REFERENCE_GROUPS.read_text(encoding="utf-8")
    assert "document.getElementById('criterion-card-container')" in script
    assert 'if (cards)' in script


def test_build_keeps_source_and_refuses_overwrite(tmp_path):
    source = tmp_path / "light.html"
    source.write_bytes(SOURCE.encode())
    before = source.read_bytes()
    output = tmp_path / "dark.html"
    receipt = dark.build(source, output)
    assert source.read_bytes() == before
    assert receipt['source_sha256'] != receipt['dark_sha256']
    with pytest.raises(FileExistsError):
        dark.build(source, output)
    with pytest.raises(ValueError):
        dark.build(source, source)
    with pytest.raises(ValueError, match='already'):
        dark.dark_copy(output.read_text(encoding="utf-8"))


def test_effects_are_decorative_and_print_stays_light():
    result = dark.dark_copy(SOURCE)
    assert '.cursorSpotlight{display:none!important}' in result
    assert "setAttribute('aria-hidden', 'true')" in result
    assert '(prefers-reduced-motion:reduce)' in result
    assert 'pointer-events:none' in result
