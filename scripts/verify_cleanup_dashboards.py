"""Read-only live Chrome checks for a published standalone audit dashboard.

Requires Playwright and an installed Chrome browser. No audit data is written.
Print keeps the user's selected evidence expansion; the default report includes
all criterion arguments, rulings, verification actions and anchor evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--expected-points', type=int, required=True)
    parser.add_argument('--expected-fully', type=int, required=True)
    parser.add_argument('--expected-percent', required=True)
    parser.add_argument('--supplier', required=True)
    args = parser.parse_args()
    source = args.html.resolve(strict=True)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    results = []
    failures = []
    errors = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(source.as_uri(), wait_until='load')

        def check(name: str, condition: bool) -> None:
            (results if condition else failures).append(name)

        if page.locator('.criterion-card').count() == 18:
            # Enconet's preserved native layout uses a drawer, not inline details.
            check('startup: 18 cards and matrix rows', page.locator('#matrix-body tr').count() == 18)
            check('published evidence-point total', page.evaluate(
                'dashboardData.criteria.reduce((s,d)=>s+d.score,0)') == args.expected_points)
            check('published percentage', page.evaluate('dashboardData.weighted_score') == float(args.expected_percent.rstrip('%')))
            page.locator('#collapse-button').click()
            check('collapse all', all(page.locator('.criterion-body').nth(i).is_hidden() for i in range(18)))
            page.locator('.criterion-card > button').first.click()
            check('individual card expands', page.locator('.criterion-body').first.is_visible())
            page.locator('.criterion-card .evidence-control').first.click()
            check('crumb opens evidence drawer', page.locator('#evidence-drawer').is_visible())
            check('crumb displays source chapter', page.locator('#evidence-chunk-text').inner_text().strip() != '')
            page.keyboard.press('Escape')
            check('escape closes evidence', page.locator('#evidence-drawer').is_hidden())
            page.locator('#rating-filter').select_option('fully')
            check('rating filter', page.locator('.criterion-card').count() == args.expected_fully)
            page.locator('#rating-filter').select_option('')
            page.locator('#criterion-search').focus()
            page.keyboard.type('no-such-criterion-unique-test')
            check('keyboard search empty state', page.locator('.criterion-card').count() == 0)
            page.locator('#criterion-search').fill('')
            check('search clear restores cards', page.locator('.criterion-card').count() == 18)
            first = page.locator('.criterion-card h3').first.inner_text()
            page.locator('#sort-button').click()
            check('order sort reverses cards', page.locator('.criterion-card h3').first.inner_text() != first)
            page.locator('#sort-button').click()
            page.locator('#expand-button').click()
            check('expand all', all(page.locator('.criterion-body').nth(i).is_visible() for i in range(18)))
            page.screenshot(path=str(output / 'desktop.png'), full_page=True)
            for width in (768, 390):
                page.set_viewport_size({'width': width, 'height': 900})
                check(f'{width}px no page overflow', page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                check(f'{width}px 18 cards', page.locator('.criterion-card').count() == 18)
                page.screenshot(path=str(output / f'viewport-{width}.png'), full_page=True)
            page.set_viewport_size({'width': 1440, 'height': 1000})
            page.evaluate('() => {window.__cleanupPrintCount=0;window.print=()=>{window.__cleanupPrintCount+=1};}')
            page.locator('#print-button').click()
            page.wait_for_function('window.__cleanupPrintCount>=1')
            print_calls = page.evaluate('window.__cleanupPrintCount')
            check('print button invokes printing', print_calls == 1)
            page.emulate_media(media='print')
            check('white print background', page.locator('body').evaluate('(el)=>getComputedStyle(el).backgroundColor') == 'rgb(255, 255, 255)')
            check('print hides controls', page.locator('#dashboard-controls').is_hidden())
            check('print contains all 18 criterion bodies', all(page.locator('.criterion-body').nth(i).is_visible() for i in range(18)))
            identifiers = page.evaluate('dashboardData.criteria.map(c=>c.n)')
            page.pdf(path=str(output / 'AUDIT_REPORT.pdf'), format='A4', print_background=True,
                     margin={'top':'12mm','bottom':'12mm','left':'12mm','right':'12mm'})
            with pymupdf.open(output / 'AUDIT_REPORT.pdf') as pdf:
                text = '\n'.join(p.get_text() for p in pdf)
                check('PDF supplier and score', args.supplier.casefold() in text.casefold()
                      and args.expected_percent.rstrip('%') in text)
                check('PDF contains all 18 criterion identifiers', all(name in text for name in identifiers))
                check('PDF text within A4 bounds', all(b[0]>=0 and b[1]>=0 and b[2]<=p.rect.width+1 and b[3]<=p.rect.height+1
                      for p in pdf for b in p.get_text('blocks')))
                pdf_pages = len(pdf)
                pdf[0].get_pixmap().save(str(output / 'pdf-page-1.png'))
            check('no JavaScript errors', not errors)
            version = browser.version
            browser.close()
            assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
            report = dict(source=str(source), sha256=digest, browser=version, passed=results,
                          failed=failures, javascript_errors=errors, pdf_pages=pdf_pages,
                          print_calls=print_calls, profile='preserved-native-Enconet')
            (output / 'checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(json.dumps(dict(passed=len(results), failed=failures, output=str(output), browser=version)))
            if failures:
                raise SystemExit(1)
            return

        check('startup: 18 cards and 18 matrix rows', page.locator('.card').count() == 18
              and page.locator('#matrix tbody tr').count() == 18)
        check(f'published total: {args.expected_points}/1800', page.evaluate('data.reduce((s,d)=>s+d.score,0)') == args.expected_points)
        check('compact cards hide evidence', page.locator('.cardBody').first.is_hidden())
        page.locator('.cardHead').first.click()
        check('individual card expands', page.locator('.cardBody').first.is_visible())
        page.locator('.crumbTrace > summary').first.click()
        page.locator('.crumbItem > summary').first.click()
        check('crumb opens source chapter', page.locator('.chapterText').first.is_visible())
        page.locator('#collapseAll').click()
        check('collapse all', page.locator('.card.open').count() == 0)
        page.locator('#expandAll').click()
        check('expand all', page.locator('.card.open').count() == 18)
        page.locator('[data-filter="fully"]').click()
        check('rating filter', page.locator('.card').count() == args.expected_fully)
        page.locator('[data-filter="all"]').click()
        page.keyboard.press('/')
        check('search shortcut', page.locator('#search').evaluate('(el)=>el===document.activeElement'))
        page.locator('#search').fill('no-such-criterion-unique-test')
        check('empty search result', page.locator('.card').count() == 0)
        page.keyboard.press('Escape')
        check('escape resets search', page.locator('.card').count() == 18)
        page.locator('#sort').select_option('score')
        check('card score sort', page.locator('.card .scorePct').first.inner_text().startswith('100%'))
        page.locator('#sort').select_option('order')
        page.locator('#matrix th[data-col="score"]').click()
        check('matrix ascending score', '50%' in page.locator('#matrix tbody tr').first.inner_text())
        page.locator('#matrix th[data-col="score"]').click()
        check('matrix descending score', '100%' in page.locator('#matrix tbody tr').first.inner_text())
        page.locator('#matrix th[data-col="order"]').click()
        page.locator('#collapseAll').click()
        page.screenshot(path=str(output / 'desktop.png'), full_page=True)
        for width in (768, 390):
            page.set_viewport_size({'width': width, 'height': 900})
            check(f'{width}px no page overflow', page.evaluate(
                'document.documentElement.scrollWidth<=innerWidth'))
            check(f'{width}px cards present', page.locator('.card').count() == 18)
            page.screenshot(path=str(output / f'viewport-{width}.png'), full_page=True)
        page.set_viewport_size({'width': 1440, 'height': 1000})
        # Observe the real button callback without opening an OS print dialog.
        page.evaluate('() => {window.printCalls=0;window.print=()=>{window.printCalls+=1};}')
        page.locator('#printBtn').click()
        page.wait_for_function('window.printCalls===1')
        check('print button expands all cards', page.locator('.card.open').count() == 18)
        page.emulate_media(media='print')
        check('print uses white background', page.locator('body').evaluate(
            '(el)=>getComputedStyle(el).backgroundColor') == 'rgb(255, 255, 255)')
        check('print hides controls', page.locator('.controls').first.is_hidden())
        check('print shows all criterion arguments', all(page.locator('.cardBody').nth(i).is_visible()
                                                       for i in range(18)))
        check('print preserves 18 matrix rows', page.locator('#matrix tbody tr').count() == 18)
        page.pdf(path=str(output / 'AUDIT_REPORT.pdf'), format='A4',
                 print_background=True, margin={'top':'12mm','bottom':'12mm','left':'12mm','right':'12mm'})
        check('real PDF created', (output / 'AUDIT_REPORT.pdf').read_bytes().startswith(b'%PDF-'))
        with pymupdf.open(output / 'AUDIT_REPORT.pdf') as pdf:
            pdf_text = '\n'.join(p.get_text() for p in pdf)
            check('PDF contains score and supplier', args.expected_percent in pdf_text and f'{args.expected_points} / 1800' in pdf_text
                  and args.supplier.casefold() in pdf_text.casefold())
            check('PDF contains all 18 expanded rulings', pdf_text.lower().count('judge ruling') == 18)
            check('PDF contains all 18 anchor evidence blocks', pdf_text.count('Anchor evidence:') == 18)
            check('PDF text stays inside A4 page bounds', all(
                b[0] >= 0 and b[1] >= 0 and b[2] <= p.rect.width + 1 and b[3] <= p.rect.height + 1
                for p in pdf for b in p.get_text('blocks')))
            pdf_pages = len(pdf)
            for number in (0, 3, len(pdf)-1):
                pdf[number].get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2)).save(
                    str(output / f'pdf-page-{number+1}.png'))
        page.screenshot(path=str(output / 'print-layout.png'), full_page=True)
        check('no browser JavaScript errors', not errors)
        browser_version = browser.version
        browser.close()
    check_source = hashlib.sha256(source.read_bytes()).hexdigest()
    assert check_source == digest, 'Dashboard source changed during read-only verification'
    report = {'source': str(source), 'sha256': digest, 'browser': browser_version,
              'passed': results, 'failed': failures, 'javascript_errors': errors, 'pdf_pages': pdf_pages,
              'print_scope': 'All 18 criterion details and matrix; nested source chapters remain click-to-open, as on screen.'}
    (output / 'checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'passed': len(results), 'failed': failures, 'output': str(output), 'browser': browser_version}))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
