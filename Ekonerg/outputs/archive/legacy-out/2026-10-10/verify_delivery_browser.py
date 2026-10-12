"""Read-only UI/portability check of prepared Ekonerg documentary delivery."""
import json
from pathlib import Path
import shutil
import tempfile

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'outputs/candidates/evidence_access/RUN-20261003-32/delivery-20261010'
OUT = ROOT/'out/2026-10-10/delivery-browser-links-final'
OUT.mkdir(exist_ok=False)
run = 'RUN-20261003-32'
records = []
with tempfile.TemporaryDirectory(prefix='portable-delivery-') as folder:
    relocated = Path(folder)/'Vendor review with spaces'
    shutil.copytree(SOURCE/'portable_package',relocated)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome',headless=True)
        page = browser.new_page(viewport={'width':1440,'height':1000})
        errors, external = [], []
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
        for theme in ['evidence_explorer.html','evidence_explorer_dark.html']:
            viewer = relocated/run/theme
            page.goto(viewer.as_uri(),wait_until='load')
            assert page.locator('.card').count()==18
            assert page.evaluate('data.reduce((s,d)=>s+d.score,0)')==1400
            ids = page.evaluate('data.map(d=>d.score_crumb_ids[0]).filter(Boolean)')
            for id in ids:
                page.evaluate('(id)=>{location.hash="crumb:"+encodeURIComponent(id)}',id)
                page.wait_for_function('(id)=>[...document.querySelectorAll(".crumbItem[open] .crumbLink")].some(e=>e.textContent===id)',arg=id)
                assert page.locator('.chapterText:visible').count()>0
            for roman in ['I','IX','XVIII']:
                page.evaluate('(id)=>{location.hash="criterion:"+id}',roman)
                page.wait_for_function('(id)=>[...document.querySelectorAll(".card.open .id")].some(e=>e.textContent===id)',arg=roman)
            page.locator('[data-filter="fully"]').click()
            assert page.locator('.card').count()==3
            page.locator('[data-filter="all"]').click()
            page.locator('#collapseAll').click()
            page.screenshot(path=str(OUT/(theme+'.png')),full_page=True)
            for width in [768,390]:
                page.set_viewport_size({'width':width,'height':900})
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.set_viewport_size({'width':1440,'height':1000})
            page.emulate_media(media='print')
            assert page.locator('body').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(255, 255, 255)'
            page.emulate_media(media='screen')
            records.append(dict(viewer=theme,criterion_deep_links=3,crumb_deep_links=len(ids),
                                relocated=True,mobile=True,light_print=True,score=77.8))
        page.goto((relocated/'review_workspace.html').as_uri())
        for link in page.locator('a').all():
            assert (relocated/link.get_attribute('href')).is_file()
        assert not errors and not external
        browser.close()
(OUT/'verification.json').write_text(json.dumps(dict(passed=True,records=records,
    page_errors=errors,external_requests=external),indent=2),encoding='utf-8')
print(json.dumps(dict(passed=True,records=len(records),relocated=True,external_requests=0)))
