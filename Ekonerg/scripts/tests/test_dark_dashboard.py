"""A dark skin must not change the working dashboard or its audit payload."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_dark_dashboard import dark_copy, build

ROOT = Path(__file__).resolve().parents[2]
LIGHT = ROOT / 'out/2026-10-07/all18-review/EKONERG_DASHBOARD.html'


def test_only_a_screen_stylesheet_is_added():
    source = LIGHT.read_text(encoding='utf-8')
    result = dark_copy(source)
    assert re.findall(r'<script.*?</script>', result, re.S)[0] == re.findall(r'<script.*?</script>', source, re.S)[0]
    assert 'id="ekonerg-reference-groups"' in result
    assert 'referenceDocuments' in result
    assert '<style id="ekonerg-dark-skin" media="screen">' in result
    assert '--u-bg-0' in result
    assert 'color-scheme:dark' in result


def test_build_keeps_light_bytes_and_records_provenance(tmp_path):
    before = LIGHT.read_bytes()
    output = tmp_path / 'dark.html'
    receipt = build(LIGHT, output)
    assert LIGHT.read_bytes() == before
    assert receipt['source_sha256'] != receipt['dark_sha256']
    assert output.exists()


def test_refuses_to_overwrite_source():
    import pytest
    with pytest.raises(ValueError, match='source'):
        build(LIGHT, LIGHT)


def test_refuses_second_overlay():
    import pytest
    with pytest.raises(ValueError, match='already'):
        dark_copy(dark_copy(LIGHT.read_text(encoding='utf-8')))


def test_score_glow_never_changes_score_length():
    from build_dark_dashboard import STYLE
    css = STYLE.read_text(encoding='utf-8')
    assert '.card::after{display:none;animation:none}' in css
    frames = css.split('@keyframes ekonerg-score-light{',1)[1].split('@media',1)[0]
    assert 'opacity:' in frames
    assert 'width:' not in frames and 'transform:' not in frames
    assert '.scoreBar>div{animation:none!important;opacity:1' in css


def test_cursor_light_is_decorative_and_opt_out_safe():
    from build_dark_dashboard import STYLE, SPOTLIGHT
    css = STYLE.read_text(encoding='utf-8')
    js = SPOTLIGHT.read_text(encoding='utf-8')
    assert 'pointer-events:none' in css.split('.cursorSpotlight{',1)[1]
    assert 'requestAnimationFrame' in js
    assert "setAttribute('aria-hidden', 'true')" in js
    assert '(prefers-reduced-motion:reduce)' in js
    assert 'event.pointerType' in js


def test_grid_is_faint_noninteractive_and_screen_only():
    from build_dark_dashboard import STYLE
    css = STYLE.read_text(encoding='utf-8')
    assert 'background-size:54px 54px' in css
    assert 'rgba(24,194,200,.055)' in css
    assert 'mask-image:linear-gradient(to bottom,#000,transparent 1100px)' in css
    assert 'body::before{' in css
    assert 'media="screen"' in dark_copy(LIGHT.read_text(encoding='utf-8'))
