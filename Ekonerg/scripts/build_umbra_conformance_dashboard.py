"""Build the TEKOL dashboard layout as an Ekonerg UMBRA evidence view.

The supplied TEKOL page is used as a layout and interaction template only.
All visible audit data is read from Ekonerg's active matrix and SQLite snapshot.
No score or human rating is inferred.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "dashboard_example" / "Example_TEKOL_Appendix_B_Conformance_Dashboard.html"
DEFAULT_MATRIX = ROOT / "out" / "2026-10-05" / "MIN-3.1-evidence-matrix-v4.json"
DEFAULT_DB = ROOT / "db" / "nqa_audit.sqlite"


def _criterion_data(matrix_path: Path, db_path: Path) -> list[dict[str, Any]]:
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT c.item_id, c.doc_id, c.criterion_id, c.statement, q.quote_original, "
            "q.source_locator, d.filename FROM active_crumbs c "
            "LEFT JOIN crumb_quotes q ON q.item_id=c.item_id "
            "LEFT JOIN documents d ON d.doc_id=c.doc_id "
            "WHERE c.document_side='DOCUMENT' ORDER BY c.criterion_id, c.item_id"
        ).fetchall()
    by_criterion: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        by_criterion.setdefault(row["criterion_id"], []).append(row)
    out: list[dict[str, Any]] = []
    for order, row in enumerate(matrix, 1):
        criterion_id = row["criterion_id"]
        evidence = by_criterion.get(criterion_id, [])
        vendor_count = int(row.get("document_evidence_count", 0))
        rule_count = int(row.get("rule_evidence_count", 0))
        status = "No direct vendor crumb" if vendor_count == 0 else (
            "Draft coverage + context" if row.get("anchored_document_evidence_count", 0)
            else "Draft coverage"
        )
        first = next((r for r in evidence if r["quote_original"]), None)
        quote = (first["quote_original"] if first else
                 "No linked Ekonerg vendor quote is present in the active snapshot.")
        locator = first["source_locator"] if first else "n/a"
        doc_names = sorted({r["filename"] for r in evidence if r["filename"]})
        crumb_ids = [r["item_id"] for r in evidence[:8]]
        statements = [r["statement"] for r in evidence[:3] if r["statement"]]
        aff = (f"The active Ekonerg snapshot contains {vendor_count} vendor crumb(s) "
               f"for this criterion and {rule_count} related rule crumb(s). "
               + ("The evidence statements include: " + " ".join(statements)
                  if statements else "No vendor-side statement is mapped."))
        con = ("No direct Ekonerg vendor crumb is mapped in the active snapshot; "
               "scope evidence is needed."
               if vendor_count == 0 else
               "The document screen does not prove that the control operated. "
               "Implementation records and objective samples remain required.")
        verify = (f"Review Ekonerg source documents and objective records for {row['criterion_name']}; "
                  "confirm scope, responsibility, implementation, and retained evidence.")
        out.append({
            "n": criterion_id.removeprefix("APP_B_"), "order": order,
            "title": row["criterion_name"], "rating": "undetermined", "score": None,
            "crumbs": f"{vendor_count} vendor / {rule_count} rule",
            "vendor_count": vendor_count, "status": status,
            "refs": ("Ekonerg crumbs: " + (", ".join(crumb_ids) if crumb_ids else "none") +
                     "; source documents: " + (", ".join(doc_names) if doc_names else "none")),
            "aff": aff, "con": con,
            "judge": "Withheld — no human criterion judgment is recorded.",
            "verify": verify,
            "quote": f"{quote} (source locator: {locator})",
        })
    return out


def _dark_css() -> str:
    return """
/* UMBRA dark skin: the source layout and controls remain unchanged. */
:root{color-scheme:dark;--bg:#0b0f14;--panel:#111821;--ink:#e8eef4;--muted:#a9b6c4;--line:#243140;--navy:#8bbcf0;--navy2:#65a7e8;--accent:#3ccfb4;--soft:#17202b;--fully:#6fd39a;--sub:#9dcc65;--partial:#e8b04b;--minimal:#ef8a55;--unmet:#f07178;--und:#a6b0bf;--fullyBg:rgba(111,211,154,.12);--subBg:rgba(157,204,101,.12);--partialBg:rgba(232,176,75,.12);--minimalBg:rgba(239,138,85,.12);--unmetBg:rgba(240,113,120,.12);--undBg:rgba(166,176,191,.12);--fullyBdr:rgba(111,211,154,.38);--subBdr:rgba(157,204,101,.38);--partialBdr:rgba(232,176,75,.40);--minimalBdr:rgba(239,138,85,.40);--unmetBdr:rgba(240,113,120,.40);--shadow:0 12px 28px rgba(0,0,0,.30);--shadow-sm:0 4px 12px rgba(0,0,0,.22)}
body{background:var(--bg);color:var(--ink)} .header{background:linear-gradient(135deg,#08121e,#111f2d 45%,#17344d);border-color:var(--line)} .topbar{background:var(--panel);border-color:var(--line)} .metric,.section,.card{background:var(--panel);border-color:var(--line);box-shadow:var(--shadow-sm)} .metric.main{background:linear-gradient(135deg,#12304a,#1b526f);border-color:var(--line)} .metric .label,.metric .small,.section p,.legend,.riskList,.footer{color:var(--muted)} .section h2{color:var(--navy)} .summaryGrid,.radarBox{background:var(--panel)} .progress{background:var(--soft);border-color:var(--line)} .note{background:rgba(232,176,75,.12);color:var(--ink);border-color:var(--partial)} .note.ok{background:var(--fullyBg);color:var(--ink)} .controls .btn,.search,.select{background:var(--soft);border-color:var(--line);color:var(--ink)} .btn:hover,.cardHead:hover,.matrix tr:hover td{background:var(--panel-hover,#1e2935)} .btn.active{background:var(--navy);color:#07111b;border-color:var(--navy)} .id{background:var(--soft);color:var(--navy)} .title,.scorePct,.block p,.footer strong{color:var(--ink)} .scoreBar{background:var(--soft)} .crumbTag,.evidence{background:var(--soft);color:var(--navy)} .cardBody{background:var(--panel);border-color:var(--line)} .block p{color:var(--muted)} .matrixWrap{border-color:var(--line)} .matrix{background:var(--panel);color:var(--ink)} .matrix th{background:var(--soft);color:var(--navy);border-color:var(--line)} .matrix td{border-color:var(--line);color:var(--muted)} .search:focus,.select:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(60,207,180,.18)}
@media print{body{background:#fff;color:#16212b}.header{background:#0f3358!important}.topbar,.metric,.section,.card,.matrix{background:#fff;color:#16212b;box-shadow:none}.cardBody{display:block!important}.controls,.footer,.btn.utility{display:none!important}}
"""


def _replace_block(text: str, start: str, end: str, replacement: str) -> str:
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement + text[b:]


def render(matrix_path: Path, db_path: Path, generated_date: str) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    data = _criterion_data(matrix_path, db_path)
    vendor_total = sum(item["vendor_count"] for item in data)
    covered = sum(item["vendor_count"] > 0 for item in data)
    no_direct = len(data) - covered
    matrix_json = json.dumps(data, ensure_ascii=False)
    text = re.sub(r"<title>.*?</title>",
                  "<title>EKONERG — 10 CFR 50 Appendix B Conformance Dashboard</title>",
                  text, count=1, flags=re.S)
    style_end = text.index("</style>")
    text = text[:style_end] + _dark_css() + text[style_end:]
    header = '''<header class="header">
  <h1>10 CFR 50 Appendix B — EKONERG Conformance Dashboard</h1>
  <p class="sub">Audit reference framework: 10 CFR 50 Appendix B, interpreted through ASME NQA-1 Part 1. This dashboard presents Ekonerg document evidence from the approved intake and active evidence snapshot. Human ratings and the final score remain withheld.</p>
  <div class="pillRow"><span class="pill"><span class="dot"></span>Ekonerg evidence snapshot</span><span class="pill">Score: Withheld</span><span class="pill">Vendor crumbs: ''' + str(vendor_total) + '''</span><span class="pill">''' + str(covered) + ''' / 18 criteria with vendor evidence</span></div>
</header>'''
    text = _replace_block(text, "<header class=\"header\">", "</header>", header)
    topbar = f'''<section class="topbar">
  <div class="metric main"><div class="num">Withheld</div><div class="label">Conformance score</div><div class="small">0 / 18 human judgments recorded</div></div>
  <div class="metric"><div class="num">18</div><div class="label">Appendix B criteria</div><div class="small">All criteria visible</div></div>
  <div class="metric"><div class="num" style="color:var(--accent)">{vendor_total}</div><div class="label">Vendor crumbs</div><div class="small">Active Ekonerg evidence</div></div>
  <div class="metric"><div class="num" style="color:var(--fully)">{covered}</div><div class="label"><span class="sw" style="background:var(--fully)"></span>Criteria with evidence</div><div class="small">Direct vendor coverage</div></div>
  <div class="metric"><div class="num" style="color:var(--partial)">{no_direct}</div><div class="label"><span class="sw" style="background:var(--partial)"></span>No direct vendor crumb</div><div class="small">Needs scope evidence</div></div>
  <div class="metric"><div class="num" style="color:var(--und)">0 / 18</div><div class="label"><span class="sw" style="background:var(--und)"></span>Judgments recorded</div><div class="small">Human review pending</div></div>
</section>'''
    text = _replace_block(text, "<section class=\"topbar\">", "</section>", topbar)
    text = re.sub(r"</section></section>\s*(<main)", r"</section>\n\1", text, count=1)
    summary = f'''<section class="section summaryGrid">
  <div><h2>Executive Summary</h2>
    <p>Ekonerg documents provide direct vendor evidence for {covered} of 18 Appendix B criteria. The active set contains {vendor_total} vendor crumbs, but document statements alone do not prove that controls operated in practice.</p>
    <p>The dashboard therefore shows evidence coverage only. It does not issue a conformance rating or calculate a score. A named auditor must review each criterion and cite objective Ekonerg records.</p>
    <div class="note"><strong>Primary evidence gap:</strong> {no_direct} criteria have no direct vendor crumb in the active snapshot. These are requests for evidence, not automatic failures.</div>
    <div class="note ok"><strong>Source boundary:</strong> Ekonerg is the only supplier shown in this production dashboard. Regulatory documents are used as the comparison baseline.</div>
  </div>
  <div><h2>Evidence Coverage Distribution</h2>
    <div class="progress" aria-label="Ekonerg evidence coverage distribution"><div class="seg" style="width:{covered/18*100:.2f}%;background:var(--fully)" title="Criteria with vendor evidence: {covered}">{covered}</div><div class="seg" style="width:{no_direct/18*100:.2f}%;background:var(--partial)" title="No direct vendor crumb: {no_direct}">{no_direct}</div></div>
    <div class="legend"><span><span class="sw" style="background:var(--fully)"></span>Vendor evidence: {covered}</span><span><span class="sw" style="background:var(--partial)"></span>No direct vendor crumb: {no_direct}</span><span><span class="sw" style="background:var(--und)"></span>Human ratings: withheld</span></div>
    <div class="note" style="margin-top:14px"><strong>Interpretation:</strong> coverage is not a pass/fail result. The final classification remains withheld until human review.</div>
  </div>
</section>'''
    text = _replace_block(text, "<section class=\"section summaryGrid\">", "</section>", summary)
    text = re.sub(r"</section></section>\s*(<section class=\"section\">)",
                  r"</section>\n\1", text, count=1)
    controls_old = '<button class="btn active" data-filter="all">All <span class="count">18</span></button>\n    <button class="btn" data-filter="fully">Fully <span class="count">3</span></button>\n    <button class="btn" data-filter="substantially">Substantially <span class="count">11</span></button>\n    <button class="btn" data-filter="partially">Partially <span class="count">4</span></button>'
    controls_new = '<button class="btn active" data-filter="all">All <span class="count">18</span></button>\n    <button class="btn" data-filter="evidence">With vendor evidence <span class="count">' + str(covered) + '</span></button>\n    <button class="btn" data-filter="no-evidence">No direct vendor crumb <span class="count">' + str(no_direct) + '</span></button>\n    <button class="btn" data-filter="withheld">Ratings withheld <span class="count">18</span></button>'
    text = text.replace(controls_old, controls_new)
    text = re.sub(r"<h2>Criterion Cards .*?</h2>", "<h2>Criterion Cards — Evidence Review</h2>", text, count=1)
    text = text.replace("<h2>Conformance Matrix</h2>", "<h2>Ekonerg Evidence Matrix</h2>")
    text = text.replace("Column headers sort the matrix. Verdicts remain evidence-bounded and downgrade unsupported interpretations.", "Column headers sort the matrix. Coverage is shown; ratings and verdicts remain withheld.")
    gaps_start = text.index('<section class="section">\n  <h2>Top Gaps Requiring Remediation</h2>')
    actions_start = text.index('<section class="section">\n  <h2>Priority Auditor Verification Actions</h2>', gaps_start)
    gap_items = "".join(f'<li><strong>{html.escape(d["n"])} — {html.escape(d["title"])}:</strong> {html.escape(d["con"])}</li>' for d in data if d["vendor_count"] == 0 or d["vendor_count"] < 5)
    gaps = '<section class="section">\n  <h2>Top Evidence Gaps Requiring Follow-up</h2>\n  <ul class="riskList">' + (gap_items or '<li>No low-coverage criteria identified.</li>') + '</ul>\n</section>\n'
    text = text[:gaps_start] + gaps + text[actions_start:]
    actions_end = text.index('</section>', text.index('<h2>Priority Auditor Verification Actions</h2>')) + len('</section>')
    action_items = "".join(f'<li>{html.escape(d["verify"])}</li>' for d in data[:10])
    actions = '<section class="section">\n  <h2>Priority Auditor Verification Actions</h2>\n  <ol class="riskList" style="columns:2;column-gap:24px;margin-left:18px">' + action_items + '</ol>\n</section>'
    text = text[:text.index('<section class="section">\n  <h2>Priority Auditor Verification Actions</h2>')] + actions + text[actions_end:]
    text = re.sub(r'<div class="radarBox".*?</div>\s*</div>', '</div>', text, flags=re.S)
    text = re.sub(r'function renderRadar\(\)\{.*?\n\}', '', text, flags=re.S)
    text = re.sub(r'[^\n]*radar[^\n]*\n', '', text, flags=re.I)
    text = re.sub(r'const data = \[.*?\];\nconst labels=', 'const data = ' + matrix_json + ';\nconst labels=', text, count=1, flags=re.S)
    text = text.replace("const labels={fully:'Fully Matched',substantially:'Substantially Matched',partially:'Partially Matched',minimally:'Minimally Matched',unmet:'Unmet'};", "const labels={undetermined:'Withheld',evidence:'With vendor evidence',none:'No direct vendor crumb'};")
    text = text.replace("const riskRank={unmet:5,minimally:4,partially:3,substantially:2,fully:1};", "const riskRank={undetermined:1};")
    text = text.replace("const evidenceRank={'Strong':3,'Moderate':2,'Weak':1,'Weak to moderate':1.5};", "const evidenceRank={};")
    text = text.replace("let arr=data.filter(d=>filter==='all'||d.rating===filter).filter(d=>!q||clean(Object.values(d).join(' ')).includes(q));", "let arr=data.filter(d=>filter==='all'||(filter==='evidence'&&d.vendor_count>0)||(filter==='no-evidence'&&d.vendor_count===0)||filter==='withheld').filter(d=>!q||clean(Object.values(d).join(' ')).includes(q));")
    text = text.replace("else if(sort==='score') arr=[...arr].sort((a,b)=>b.score-a.score||a.order-b.order);", "else if(sort==='score') arr=[...arr].sort((a,b)=>(b.vendor_count-a.vendor_count)||a.order-b.order);")
    text = re.sub(r'function cardHtml\(d\)\{.*?\n\}', '''function cardHtml(d){
  const pct=d.vendor_count?Math.min(100,Math.max(8,d.vendor_count*4)):0;
  return `<article class="card undetermined" data-rating="undetermined"><div class="cardHead" onclick="this.parentElement.classList.toggle('open')"><div class="cardLeft"><span class="id">${d.n}</span><div><div class="title">${d.title}</div></div></div><span class="badge undetermined">Withheld</span></div><div class="scoreLine"><div class="scoreBar"><div style="width:${pct}%;background:var(--accent)"></div></div><span class="scorePct">—</span><span class="crumbTag">Evidence: ${d.crumbs}</span><span>${d.refs}</span></div><div class="cardBody"><div class="block"><h4 class="aff">▸ Vendor evidence signal</h4><p>${d.aff}</p></div><div class="block"><h4 class="con">▸ Evidence limitation</h4><p>${d.con}</p></div><div class="block"><h4 class="judge">⚖ Human ruling</h4><p>${d.judge}</p></div><div class="block"><h4 class="verify">✓ Auditor verification action</h4><p>${d.verify}</p></div><div class="evidence"><strong>Source quote:</strong> ${d.quote}</div></div></article>`;
}''', text, count=1, flags=re.S)
    text = text.replace("if(k==='score') return (a.score-b.score)*asc;", "if(k==='score') return (a.vendor_count-b.vendor_count)*asc;")
    text = text.replace("<th data-col=\"rating\">Verdict ${arrow('rating')}</th><th data-col=\"score\" class=\"center\">Score ${arrow('score')}</th><th data-col=\"crumbs\" class=\"center\">Evidence ${arrow('crumbs')}</th>", "<th data-col=\"rating\">Status ${arrow('rating')}</th><th data-col=\"score\" class=\"center\">Score ${arrow('score')}</th><th data-col=\"crumbs\" class=\"center\">Evidence ${arrow('crumbs')}</th>")
    text = text.replace("<td class=\"center\">${d.score}%</td>", "<td class=\"center\">Withheld</td>")
    text = text.replace("renderCards(); renderMatrix(); renderRadar();", "renderCards(); renderMatrix();")
    text = re.sub(r'<div class="footer">.*?</div>', '<div class="footer">Standalone Ekonerg UMBRA dashboard — sources: Ekonerg active evidence snapshot, 10 CFR 50 Appendix B, ASME NQA-1 Part 1 interpretation baseline. Score withheld.</div>', text, count=1, flags=re.S)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--date", default="2026-10-05")
    ap.add_argument("--output", type=Path, default=ROOT / "out" / "2026-10-05" / "EKONERG_UMBRA_DASHBOARD_2026-10-05.html")
    args = ap.parse_args()
    page = render(args.matrix, args.db, args.date)
    if "TEKOL" in page or "1499 / 1800" in page or "83.3%" in page:
        raise SystemExit("production dashboard still contains design-reference data")
    args.output.write_text(page, encoding="utf-8", newline="\n")
    print(f"build_umbra_conformance_dashboard: PASS - {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
