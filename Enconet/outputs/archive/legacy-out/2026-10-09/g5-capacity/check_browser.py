"""Actual candidate browser proof: every report target and every scored crumb."""
import json
import os
from pathlib import Path
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import browser_harness
import validate_report_links

TARGET = ROOT / "outputs/candidates/evidence_access/RUN-20261008-17"
REPORT = TARGET / "enconet_appendix_b_evaluation_report.md"
VIEWER = TARGET / "enconet_appendix_b_dashboard.html"
BUNDLE = TARGET / "evidence_bundle_report_g5.json"
OUT = Path(__file__).resolve().parent
bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
links, errors = validate_report_links.parse_evidence_links(REPORT.read_text(encoding="utf-8"), REPORT)
assert not errors
targets = sorted({link.target for link in links})
assert not browser_harness.preflight()
config = browser_harness.load_config(browser_harness.DEFAULT_CONFIG)
previous = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = config["browser"]["root"]
external, console_errors = [], []
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width":1440,"height":1000})
            page.on("request", lambda r: external.append(r.url) if r.url.startswith(("http:","https:")) else None)
            page.on("pageerror", lambda e: console_errors.append(str(e)))
            page.goto(VIEWER.resolve().as_uri(), wait_until="load")
            for target in targets:
                page.evaluate("target => openEvidence(target)", target)
                assert page.locator("#evidence-drawer").is_visible(), target
                assert not page.locator("#evidence-error").is_visible(), target
            quotes = {q["quote_id"]:q for q in bundle["quotes"]}
            chunks = {c["chunk_id"]:c for c in bundle["chunks"]}
            for crumb in bundle["crumbs"]:
                page.evaluate("target => openEvidence(target)", crumb["viewer_target"])
                assert page.locator("#evidence-statement").text_content() == crumb["statement"]
                assert page.locator("#evidence-document-id").text_content() == crumb["document_id"]
                actual_ids = page.locator("[data-quote-id]").evaluate_all("els => els.map(e => e.dataset.quoteId)")
                assert set(actual_ids) == set(crumb["quote_ids"])
                for qid in crumb["quote_ids"]:
                    q = quotes[qid]
                    assert q["text_original"] in chunks[q["chunk_id"]]["text"]
                assert page.locator("#evidence-chunk-text").text_content() in [chunks[cid]["text"] for cid in crumb["chunk_ids"]]
            page.evaluate("() => { window.print=()=>{window.__printCalled=true;}; }")
            page.locator("#evidence-print").click()
            assert page.evaluate("window.__printCalled") is True
            assert page.evaluate("document.body.classList.contains('evidence-print')") is True
            page.evaluate("() => { document.body.classList.remove('evidence-print'); window.dispatchEvent(new Event('afterprint')); }")
            page.keyboard.press("Escape")
            page.screenshot(path=str(OUT / "viewer-desktop.png"), full_page=False)
            page.set_viewport_size({"width":390,"height":844})
            page.screenshot(path=str(OUT / "viewer-mobile.png"), full_page=False)
            assert not external and not console_errors
        finally:
            browser.close()
finally:
    if previous is None:
        os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", None)
    else:
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = previous

result = {"report_links":len(links),"unique_targets":len(targets),
          "crumbs_checked":len(bundle["crumbs"]),"quotes":len(bundle["quotes"]),
          "full_chapters":len(bundle["chunks"]),"external_requests":external,
          "page_errors":console_errors,"print_intercept":True,"passed":True}
(OUT / "browser-check.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(result))
