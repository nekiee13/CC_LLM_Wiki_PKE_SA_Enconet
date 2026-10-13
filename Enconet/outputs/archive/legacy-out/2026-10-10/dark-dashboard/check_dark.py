"""Verify the separate dark screen, audit/data parity, controls and light print."""
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
import browser_harness
import validate_dashboard
import validate_evidence_bundle

LIGHT = ROOT / 'outputs/enconet_appendix_b_dashboard.html'
DARK = ROOT / 'outputs/candidates/evidence_access/RUN-20261008-17/dark/enconet_appendix_b_dashboard_dark.html'
source, result = LIGHT.read_text(encoding='utf-8'), DARK.read_text(encoding='utf-8')
for script in re.findall(r'<script.*?</script>', source, re.S):
    assert script in result, 'Original audit script/data changed'
data = json.loads(validate_dashboard.DATA_BLOCK.search(source).group(1))
bundle = json.loads(validate_dashboard.EVIDENCE_BLOCK.search(source).group(2))
package = json.loads((ROOT / 'outputs/enconet_appendix_b_evaluation_package.json').read_text(encoding='utf-8'))
errors = validate_dashboard.validate(package, data, result, db=ROOT/'db/nqa_audit.sqlite', evidence_bundle=bundle)
assert not errors, errors
config = browser_harness.load_config(browser_harness.DEFAULT_CONFIG)
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = config['browser']['root']
from playwright.sync_api import sync_playwright
external, page_errors = [], []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width':1440,'height':1050})
    page.on('request', lambda r: external.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.on('pageerror', lambda e: page_errors.append(str(e)))
    page.goto(DARK.resolve().as_uri())
    assert page.locator('.criterion-card').count() == 18
    assert '80.6' in page.locator('#metric-score').inner_text()
    assert 'enconet' in page.title().lower()
    page.locator('#rating-filter').select_option('fully')
    assert page.locator('.criterion-card').count() == 6
    page.locator('#rating-filter').select_option('')
    page.locator('#criterion-search').fill('no-such-audit-criterion')
    assert page.locator('.criterion-card').count() == 0
    page.locator('#criterion-search').fill('')
    page.locator('#sort-button').click()
    expected_last = max(data['criteria'],key=lambda c:c['order'])
    assert page.locator('.criterion-card h3').first.inner_text() == f"{expected_last['n']} — {expected_last['title']}"
    page.locator('#sort-button').click()
    page.locator('#collapse-button').click()
    assert page.locator('.criterion-body:visible').count() == 0
    page.locator('#expand-button').click()
    assert page.locator('.criterion-body:visible').count() == 18
    for crumb in bundle['crumbs']:
        page.evaluate('target => openEvidence(target)', crumb['viewer_target'])
        assert page.locator('#evidence-drawer').is_visible()
        assert page.locator('#evidence-status').is_hidden()
        assert page.locator('#evidence-statement').inner_text() == crumb['statement']
        assert page.locator('#evidence-chunk-text').inner_text()
    page.locator('#evidence-close').click()
    page.mouse.move(900,160)
    page.screenshot(path=str(OUT/'dark-desktop.png'), full_page=False)
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(OUT/'dark-mobile.png'), full_page=False)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Mobile page overflows'
    page.evaluate('window.print=()=>{window.__printed=true;}')
    page.locator('#print-button').click()
    assert page.evaluate('window.__printed')
    page.emulate_media(media='print')
    assert page.evaluate('getComputedStyle(document.body).backgroundColor') == 'rgb(255, 255, 255)'
    assert page.locator('.cursorSpotlight').is_hidden()
    page.pdf(path=str(OUT/'dark-print.pdf'), format='A4', print_background=True)
    assert not external and not page_errors, (external,page_errors)
    browser.close()
record={'light_sha256':hashlib.sha256(LIGHT.read_bytes()).hexdigest(),
        'dark_sha256':hashlib.sha256(DARK.read_bytes()).hexdigest(),
        'criteria':18,'score':data['weighted_score'],'crumbs_checked':len(bundle['crumbs']),
        'print_background':'white','external_requests':external,'page_errors':page_errors,'passed':True}
assert record['light_sha256']=='bf62a3fe044e488a9659c0d74b03df04f40c519c608bfc5b7da81d792ec633f1'
(OUT/'verification.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(record))
