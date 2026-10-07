"""Live offline checks for the separate light/dark dashboard candidates."""
import argparse
import hashlib
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--light',type=Path,required=True)
    p.add_argument('--dark',type=Path,required=True)
    p.add_argument('--browser-executable',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a = p.parse_args()
    if a.output.exists():
        p.error('Use a fresh check directory')
    a.output.mkdir(parents=True)
    checks = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True,executable_path=str(a.browser_executable))
        for label,path in [('light',a.light),('dark',a.dark)]:
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            page = browser.new_page(viewport=dict(width=1440,height=1000))
            errors,network = [],[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
            page.goto(path.resolve().as_uri())
            def check(name,condition):
                checks.append(dict(theme=label,name=name,passed=bool(condition)))
                if not condition:
                    raise AssertionError(label+': '+name)
            check('18 criterion cards',page.locator('.card').count() == 18)
            check('18 matrix rows',page.locator('#matrix tbody tr').count() == 18)
            check('closed cards hide references',not page.locator('.criterionRefs').first.is_visible())
            page.locator('[data-filter=fully]').click()
            check('rating filter',page.locator('.card').count() == page.evaluate('data.filter(d=>d.rating===\'fully\').length'))
            page.locator('[data-filter=all]').click()
            page.keyboard.press('/')
            check('keyboard search focus',page.locator('#search').evaluate('(e)=>e===document.activeElement'))
            page.locator('#search').fill('NO-SUCH-CRITERION-987654')
            check('empty search',page.locator('.card').count() == 0)
            page.keyboard.press('Escape')
            check('escape resets search',page.locator('.card').count() == 18)
            page.locator('#sort').select_option('risk')
            check('risk sort',page.locator('.card').first.get_attribute('data-rating') == 'partially')
            page.locator('#expandAll').click()
            check('expand all',page.locator('.card.open').count() == 18)
            page.locator('.crumbTrace > summary').first.click()
            page.locator('.crumbItem > summary').first.click()
            check('source chapter opens',page.locator('.chapterText').first.is_visible())
            check('source chapter has text',len(page.locator('.chapterText').first.inner_text()) > 10)
            page.locator('#collapseAll').click()
            check('collapse all',page.locator('.card.open').count() == 0)
            page.locator('#matrix th[data-col=score]').click()
            scores = page.locator('#matrix tbody td:nth-child(4)').all_inner_texts()
            values = [float(s.split('%')[0]) for s in scores]
            check('matrix sorting',values == sorted(values))
            page.evaluate('window.print=()=>window.printCalled=true')
            page.locator('#printBtn').click()
            page.wait_for_timeout(200)
            check('print expands cards',page.evaluate('window.printCalled') and page.locator('.card.open').count() == 18)
            page.emulate_media(media='print')
            check('print is light',page.evaluate('getComputedStyle(document.body).backgroundColor') == 'rgb(255, 255, 255)')
            if label == 'dark':
                check('print hides spotlight',not page.locator('.cursorSpotlight').is_visible())
            page.emulate_media(media='screen')
            page.locator('#collapseAll').click()
            page.screenshot(path=str(a.output/(label+'-desktop.png')))
            page.set_viewport_size(dict(width=390,height=844))
            check('mobile cards visible',page.locator('.card').count() == 18)
            check('mobile no page overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            if label == 'dark':
                page.emulate_media(reduced_motion='reduce')
                check('reduced motion hides spotlight',not page.locator('.cursorSpotlight').is_visible())
            check('no JavaScript errors',not errors)
            check('no external requests',not network)
            check('input HTML unchanged',hashlib.sha256(path.read_bytes()).hexdigest() == before)
            page.close()
        browser.close()
    (a.output/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(passed=len(checks),failed=0,output=str(a.output))))


if __name__ == '__main__':
    main()
