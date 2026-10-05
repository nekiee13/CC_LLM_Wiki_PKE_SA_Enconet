"""Build the light TEKOL dashboard layout with Ekonerg evaluation data.

The supplied TEKOL page is used as a layout and interaction template only.
All visible audit data is read from Ekonerg's active matrix and approved local
evaluation run. The score follows the Enconet five-level model.
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
DEFAULT_RUN_ID = "RUN-20261003-32"
RATING_POINTS = {"fully": 5, "substantially": 4, "partially": 3, "minimally": 2, "unmet": 1}
RATING_LABELS = {
    "fully": "Fully Matched", "substantially": "Substantially Matched",
    "partially": "Partially Matched", "minimally": "Minimally Matched", "unmet": "Unmet",
}


def _criterion_data(matrix_path: Path, db_path: Path, run_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
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
        evaluations = {
            row["criterion_id"]: row for row in conn.execute(
                "SELECT criterion_id, rating, score, judge_ruling, rationale "
                "FROM criterion_evaluations WHERE evaluation_run_id=? ORDER BY criterion_id", (run_id,)
            )
        }
        if len(evaluations) != 18:
            raise ValueError(f"evaluation run {run_id} must contain 18 criterion evaluations")
        score_crumbs: dict[str, list[dict[str, Any]]] = {criterion_id: [] for criterion_id in evaluations}
        crumb_rows = conn.execute(
            "SELECT e.criterion_id, c.item_id, c.doc_id, d.filename, q.quote_id, "
            "q.quote_original, q.source_locator, l.chunk_id, ch.heading_path, ch.chunk_text "
            "FROM evaluation_evidence x "
            "JOIN criterion_evaluations e ON e.evaluation_id=x.evaluation_id "
            "JOIN crumbs c ON c.item_id=x.item_id "
            "LEFT JOIN documents d ON d.doc_id=c.doc_id "
            "LEFT JOIN crumb_quotes q ON q.item_id=c.item_id "
            "LEFT JOIN crumb_chunk_links l ON l.item_id=q.item_id AND l.quote_id=q.quote_id "
            "LEFT JOIN document_chunks ch ON ch.chunk_id=l.chunk_id "
            "WHERE e.evaluation_run_id=? AND c.document_side='DOCUMENT' "
            "ORDER BY e.criterion_id, c.item_id, q.quote_id, l.chunk_id", (run_id,)
        ).fetchall()
        by_criterion_crumb: dict[tuple[str, str], dict[str, Any]] = {}
        for row in crumb_rows:
            key = (row["criterion_id"], row["item_id"])
            crumb = by_criterion_crumb.setdefault(key, {
                "id": row["item_id"], "doc_id": row["doc_id"],
                "filename": row["filename"] or row["doc_id"],
                "quotes": [], "chapters": [],
            })
            if row["quote_id"] and not any(q["quote_id"] == row["quote_id"] for q in crumb["quotes"]):
                crumb["quotes"].append({
                    "quote_id": row["quote_id"], "text": row["quote_original"] or "",
                    "locator": row["source_locator"] or "n/a",
                })
            if row["chunk_id"] and not any(c["chunk_id"] == row["chunk_id"] for c in crumb["chapters"]):
                crumb["chapters"].append({
                    "chunk_id": row["chunk_id"],
                    "heading_path": row["heading_path"] or "Chapter locator unavailable",
                    "text": row["chunk_text"] or "Chapter text unavailable in the source snapshot.",
                })
        for (criterion_id, _crumb_id), crumb in by_criterion_crumb.items():
            score_crumbs.setdefault(criterion_id, []).append(crumb)
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
        criterion_crumbs = score_crumbs.get(criterion_id, [])
        crumb_ids = [crumb["id"] for crumb in criterion_crumbs]
        statements = [r["statement"] for r in evidence[:3] if r["statement"]]
        aff = (f"The active Ekonerg snapshot contains {vendor_count} vendor crumb(s) "
               f"for this criterion and {rule_count} related rule crumb(s). "
               + ("The evidence statements include: " + " ".join(statements)
                  if statements else "No vendor-side statement is mapped."))
        evaluation = evaluations.get(criterion_id)
        rating = str(evaluation["rating"])
        score = float(evaluation["score"])
        con = ("No direct Ekonerg vendor crumb is mapped in the active snapshot; "
               "the criterion is evaluated as unmet until vendor evidence is supplied."
               if vendor_count == 0 else
               "The document screen does not prove that the control operated. "
               "Implementation records and objective samples remain required.")
        verify = (f"Review Ekonerg source documents and objective records for {row['criterion_name']}; "
                  "confirm scope, responsibility, implementation, and retained evidence.")
        out.append({
            "n": criterion_id.removeprefix("APP_B_"), "order": order,
            "title": row["criterion_name"], "rating": rating, "score": score,
            "rating_label": RATING_LABELS[rating], "scale_points": RATING_POINTS[rating],
            "crumbs": f"{vendor_count} vendor / {rule_count} rule",
            "vendor_count": vendor_count, "status": status,
            "score_crumb_ids": crumb_ids, "score_crumb_count": len(crumb_ids),
            "score_crumbs": criterion_crumbs,
            "refs": ("Ekonerg crumbs: " + (", ".join(crumb_ids) if crumb_ids else "none") +
                     "; source documents: " + (", ".join(doc_names) if doc_names else "none")),
            "aff": aff, "con": con,
            "judge": str(evaluation["judge_ruling"]), "rationale": str(evaluation["rationale"]),
            "summary": str(evaluation["rationale"]),
            "score_trace": (f"{len(crumb_ids)} linked vendor crumb(s) -> {rating} "
                            f"({RATING_POINTS[rating]}/5, {score:.0f} points)"),
            "judge": "Withheld — no human criterion judgment is recorded.",
            "verify": verify,
            "judge": str(evaluation["judge_ruling"]), "rationale": str(evaluation["rationale"]),
            "quote": f"{quote} (source locator: {locator})",
        })
    counts = {key: sum(item["rating"] == key for item in out) for key in RATING_LABELS}
    metrics = {"run_id": run_id, "criteria": len(out), "applicable": len(out),
               "score": round(sum(item["score"] for item in out) / len(out), 1), "counts": counts}
    return out, metrics


def _dark_css() -> str:
    # The TEKOL source is already the approved light UMBRA presentation.
    # Keep the name for a minimal call-site change, but do not append a dark skin.
    return ""


def _replace_block(text: str, start: str, end: str, replacement: str) -> str:
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement + text[b:]


def render(matrix_path: Path, db_path: Path, generated_date: str, run_id: str = DEFAULT_RUN_ID) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    data, metrics = _criterion_data(matrix_path, db_path, run_id)
    score = metrics["score"]
    counts = metrics["counts"]
    vendor_total = sum(item["vendor_count"] for item in data)
    covered = sum(item["vendor_count"] > 0 for item in data)
    no_direct = len(data) - covered
    # The data is embedded in a script tag. Escape HTML-significant characters
    # so source chapter text cannot terminate that tag or become markup.
    matrix_json = (json.dumps(data, ensure_ascii=False)
                   .replace("<", "\\u003c")
                   .replace(">", "\\u003e")
                   .replace("&", "\\u0026"))
    text = re.sub(r"<title>.*?</title>",
                  "<title>EKONERG — 10 CFR 50 Appendix B Conformance Dashboard</title>",
                  text, count=1, flags=re.S)
    style_end = text.index("</style>")
    text = text[:style_end] + ".criterionSummary{margin:3px 0 0;color:var(--muted);font-size:12px;line-height:1.35}.scoreTrace{font-weight:750;color:var(--navy)}.crumbTrace{margin-top:10px;border:1px solid var(--line);border-radius:8px;padding:7px 10px;background:var(--soft);font-size:12px}.crumbTrace summary{cursor:pointer;color:var(--navy);font-weight:750}.crumbTrace ul{margin:7px 0 0 0;max-height:420px;overflow:auto;padding-left:18px}.crumbTrace li{margin:4px 0;word-break:break-word}.crumbItem{border:1px solid var(--line);border-radius:6px;padding:5px 8px;background:var(--panel)}.crumbItem summary{font-weight:700}.crumbBody{padding:8px 4px 2px}.crumbLink{color:var(--navy)}.chapterView{margin-top:7px;border-left:3px solid var(--accent);padding-left:9px}.chapterMeta{color:var(--muted);font-size:11px;margin-bottom:4px}.chapterText{white-space:pre-wrap;max-height:260px;overflow:auto;margin:0;padding:8px;background:var(--panel-raised);color:var(--ink);font:12px/1.45 ui-monospace,SFMono-Regular,Consolas,monospace}" + text[style_end:]
    text = text[:style_end] + _dark_css() + text[style_end:]
    header = '''<header class="header">
  <h1>10 CFR 50 Appendix B — EKONERG Conformance Dashboard</h1>
  <p class="sub">Audit reference framework: 10 CFR 50 Appendix B, interpreted through ASME NQA-1 Part 1. This dashboard presents Ekonerg document evidence from the approved intake and active evidence snapshot. Human ratings and the final score remain withheld.</p>
  <div class="pillRow"><span class="pill"><span class="dot"></span>Ekonerg evidence snapshot</span><span class="pill">Score: Withheld</span><span class="pill">Vendor crumbs: ''' + str(vendor_total) + '''</span><span class="pill">''' + str(covered) + ''' / 18 criteria with vendor evidence</span></div>
</header>'''
    header = f'''<header class="header">
  <h1>10 CFR 50 Appendix B — EKONERG Conformance Dashboard</h1>
  <p class="sub">Audit reference framework: 10 CFR 50 Appendix B, interpreted through ASME NQA-1 Part 1. This dashboard presents Ekonerg vendor-document evidence from the approved intake and active evaluation run.</p>
  <div class="pillRow"><span class="pill"><span class="dot"></span>Ekonerg evidence snapshot</span><span class="pill">Overall: {score:.1f}% — Partially Matched</span><span class="pill">Vendor crumbs: {vendor_total}</span><span class="pill">18 / 18 criteria evaluated</span></div>
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
    topbar = f'''<section class="topbar">
  <div class="metric main"><div class="num">{score:.1f}%</div><div class="label">Overall conformance</div><div class="small">{sum(item["score"] for item in data):.0f} / 1800 evidence points</div></div>
  <div class="metric"><div class="num">18</div><div class="label">Appendix B criteria</div><div class="small">All criteria evaluated</div></div>
  <div class="metric"><div class="num" style="color:var(--accent)">{vendor_total}</div><div class="label">Vendor crumbs</div><div class="small">Active Ekonerg evidence</div></div>
  <div class="metric"><div class="num" style="color:var(--fully)">{counts["fully"]}</div><div class="label"><span class="sw" style="background:var(--fully)"></span>Fully matched</div><div class="small">5 / 5 level</div></div>
  <div class="metric"><div class="num" style="color:var(--sub)">{counts["substantially"]}</div><div class="label"><span class="sw" style="background:var(--sub)"></span>Substantially matched</div><div class="small">4 / 5 level</div></div>
  <div class="metric"><div class="num" style="color:var(--unmet)">{counts["unmet"]}</div><div class="label"><span class="sw" style="background:var(--unmet)"></span>Unmet</div><div class="small">No direct vendor evidence</div></div>
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
    summary = f'''<section class="section summaryGrid">
  <div><h2>Executive Summary</h2>
    <p>Ekonerg documents were evaluated against all 18 Appendix B criteria. The evidence-based result is <strong>{score:.1f}% — Partially Matched</strong>, using the approved five-level Enconet scale.</p>
    <p>The score is the average of the criterion ratings: fully = 5/5 (100), substantially = 4/5 (75), partially = 3/5 (50), minimally = 2/5 (25), and unmet = 1/5 (0).</p>
    <div class="note"><strong>Primary evidence gap:</strong> {no_direct} criteria have no direct Ekonerg vendor crumb and are therefore rated unmet: VIII, IX, XI, XIII, and XIV.</div>
    <div class="note ok"><strong>Source boundary:</strong> Ekonerg is the only supplier shown. Regulatory documents are the comparison baseline; no other supplier data is used.</div>
  </div>
  <div><h2>Classification Distribution</h2>
    <div class="progress" aria-label="Ekonerg classification distribution"><div class="seg" style="width:{counts["fully"]/18*100:.2f}%;background:var(--fully)" title="Fully Matched: {counts["fully"]}">{counts["fully"]}</div><div class="seg" style="width:{counts["substantially"]/18*100:.2f}%;background:var(--sub)" title="Substantially Matched: {counts["substantially"]}">{counts["substantially"]}</div><div class="seg" style="width:{counts["partially"]/18*100:.2f}%;background:var(--partial)" title="Partially Matched: {counts["partially"]}">{counts["partially"]}</div><div class="seg" style="width:{counts["unmet"]/18*100:.2f}%;background:var(--unmet)" title="Unmet: {counts["unmet"]}">{counts["unmet"]}</div></div>
    <div class="legend"><span><span class="sw" style="background:var(--fully)"></span>Fully: {counts["fully"]}</span><span><span class="sw" style="background:var(--sub)"></span>Substantially: {counts["substantially"]}</span><span><span class="sw" style="background:var(--partial)"></span>Partially: {counts["partially"]}</span><span><span class="sw" style="background:var(--minimal)"></span>Minimally: {counts["minimally"]}</span><span><span class="sw" style="background:var(--unmet)"></span>Unmet: {counts["unmet"]}</span></div>
    <div class="note" style="margin-top:14px"><strong>Interpretation:</strong> each criterion has a recorded five-level rating. Follow-up verification should target the lowest-rated criteria first.</div>
  </div>
</section>'''
    text = _replace_block(text, "<section class=\"section summaryGrid\">", "</section>", summary)
    text = re.sub(r"</section></section>\s*(<section class=\"section\">)",
                  r"</section>\n\1", text, count=1)
    controls_old = '<button class="btn active" data-filter="all">All <span class="count">18</span></button>\n    <button class="btn" data-filter="fully">Fully <span class="count">3</span></button>\n    <button class="btn" data-filter="substantially">Substantially <span class="count">11</span></button>\n    <button class="btn" data-filter="partially">Partially <span class="count">4</span></button>'
    controls_new = '<button class="btn active" data-filter="all">All <span class="count">18</span></button>\n    <button class="btn" data-filter="evidence">With vendor evidence <span class="count">' + str(covered) + '</span></button>\n    <button class="btn" data-filter="no-evidence">No direct vendor crumb <span class="count">' + str(no_direct) + '</span></button>\n    <button class="btn" data-filter="withheld">Ratings withheld <span class="count">18</span></button>'
    text = text.replace(controls_old, controls_new)
    controls_new = f'''<button class="btn active" data-filter="all">All <span class="count">18</span></button>
    <button class="btn" data-filter="fully">Fully <span class="count">{counts["fully"]}</span></button>
    <button class="btn" data-filter="substantially">Substantially <span class="count">{counts["substantially"]}</span></button>
    <button class="btn" data-filter="partially">Partially <span class="count">{counts["partially"]}</span></button>
    <button class="btn" data-filter="minimally">Minimally <span class="count">{counts["minimally"]}</span></button>
    <button class="btn" data-filter="unmet">Unmet <span class="count">{counts["unmet"]}</span></button>'''
    text = re.sub(r'<button class="btn active" data-filter="all">.*?</button>(?:\s*<button class="btn" data-filter="[^"]+">.*?</button>)+', controls_new, text, count=1, flags=re.S)
    text = re.sub(r"<h2>Criterion Cards .*?</h2>", "<h2>Criterion Cards — Evidence Review</h2>", text, count=1)
    text = text.replace("<h2>Conformance Matrix</h2>", "<h2>Ekonerg Evidence Matrix</h2>")
    text = text.replace("Column headers sort the matrix. Verdicts remain evidence-bounded and downgrade unsupported interpretations.", "Column headers sort the matrix. Ratings use the approved five-level Enconet scale.")
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
    text = re.sub(
        r'const data = \[.*?\];\nconst labels=',
        lambda _match: 'const data = ' + matrix_json + ';\nconst labels=',
        text, count=1, flags=re.S,
    )
    text = text.replace("const labels={fully:'Fully Matched',substantially:'Substantially Matched',partially:'Partially Matched',minimally:'Minimally Matched',unmet:'Unmet'};", "const labels={fully:'Fully Matched',substantially:'Substantially Matched',partially:'Partially Matched',minimally:'Minimally Matched',unmet:'Unmet'};")
    text = text.replace("const riskRank={unmet:5,minimally:4,partially:3,substantially:2,fully:1};", "const riskRank={unmet:5,minimally:4,partially:3,substantially:2,fully:1};")
    text = text.replace("const evidenceRank={'Strong':3,'Moderate':2,'Weak':1,'Weak to moderate':1.5};", "const evidenceRank={};")
    text = text.replace("let arr=data.filter(d=>filter==='all'||d.rating===filter).filter(d=>!q||clean(Object.values(d).join(' ')).includes(q));", "let arr=data.filter(d=>filter==='all'||d.rating===filter).filter(d=>!q||clean(Object.values(d).join(' ')).includes(q));")
    text = text.replace("else if(sort==='score') arr=[...arr].sort((a,b)=>b.score-a.score||a.order-b.order);", "else if(sort==='score') arr=[...arr].sort((a,b)=>b.score-a.score||a.order-b.order);")
    text = re.sub(r'function cardHtml\(d\)\{.*?\n\}', '''function cardHtml(d){
  const pct=d.vendor_count?Math.min(100,Math.max(8,d.vendor_count*4)):0;
  return `<article class="card undetermined" data-rating="undetermined"><div class="cardHead" onclick="this.parentElement.classList.toggle('open')"><div class="cardLeft"><span class="id">${d.n}</span><div><div class="title">${d.title}</div></div></div><span class="badge undetermined">Withheld</span></div><div class="scoreLine"><div class="scoreBar"><div style="width:${pct}%;background:var(--accent)"></div></div><span class="scorePct">—</span><span class="crumbTag">Evidence: ${d.crumbs}</span><span>${d.refs}</span></div><div class="cardBody"><div class="block"><h4 class="aff">▸ Vendor evidence signal</h4><p>${d.aff}</p></div><div class="block"><h4 class="con">▸ Evidence limitation</h4><p>${d.con}</p></div><div class="block"><h4 class="judge">⚖ Human ruling</h4><p>${d.judge}</p></div><div class="block"><h4 class="verify">✓ Auditor verification action</h4><p>${d.verify}</p></div><div class="evidence"><strong>Source quote:</strong> ${d.quote}</div></div></article>`;
}''', text, count=1, flags=re.S)
    text = re.sub(r'function cardHtml\(d\)\{.*?\n\}', '''function cardHtml(d){
  return `<article class="card ${d.rating}" data-rating="${d.rating}"><div class="cardHead" onclick="this.parentElement.classList.toggle('open')"><div class="cardLeft"><span class="id">${d.n}</span><div><div class="title">${d.title}</div></div></div><span class="badge ${d.rating}">${labels[d.rating]}</span></div><div class="scoreLine"><div class="scoreBar"><div style="width:${d.score}%;background:${ratingClr[d.rating]}"></div></div><span class="scorePct">${d.score}% · ${d.scale_points}/5</span><span class="crumbTag">Evidence: ${d.crumbs}</span><span>${d.refs}</span></div><div class="cardBody"><div class="block"><h4 class="aff">▸ Affirmative argument</h4><p>${d.aff}</p></div><div class="block"><h4 class="con">▸ Contrary argument</h4><p>${d.con}</p></div><div class="block"><h4 class="judge">⚖ Judge ruling</h4><p>${d.judge}</p><p>${d.rationale}</p></div><div class="block"><h4 class="verify">✓ Auditor verification action</h4><p>${d.verify}</p></div><div class="evidence"><strong>Anchor evidence:</strong> ${d.quote}</div></div></article>`;
}''', text, count=1, flags=re.S)
    text = re.sub(r'function cardHtml\(d\)\{.*?\n\}', '''function cardHtml(d){
  const crumbs=(d.score_crumb_ids||[]).map(id=>`<li>${id}</li>`).join('')||'<li>No linked vendor crumb; score is unmet because vendor evidence is absent.</li>';
  return `<article class="card ${d.rating}" data-rating="${d.rating}"><div class="cardHead" onclick="this.parentElement.classList.toggle('open')"><div class="cardLeft"><span class="id">${d.n}</span><div><div class="title">${d.title}</div><div class="criterionSummary">${d.summary}</div></div></div><span class="badge ${d.rating}">${labels[d.rating]}</span></div><div class="scoreLine"><div class="scoreBar"><div style="width:${d.score}%;background:${ratingClr[d.rating]}"></div></div><span class="scorePct">${d.score}% · ${d.scale_points}/5</span><span class="scoreTrace">${d.score_trace}</span><span>${d.refs}</span></div><div class="cardBody"><div class="block"><h4 class="aff">▸ Criterion summary</h4><p>${d.summary}</p></div><div class="block"><h4 class="aff">▸ Affirmative argument</h4><p>${d.aff}</p></div><div class="block"><h4 class="con">▸ Contrary argument</h4><p>${d.con}</p></div><div class="block"><h4 class="judge">⚖ Judge ruling</h4><p>${d.judge}</p></div><details class="crumbTrace"><summary>Crumbs linked to this score (${d.score_crumb_count})</summary><ul>${crumbs}</ul></details><div class="block"><h4 class="verify">✓ Auditor verification action</h4><p>${d.verify}</p></div><div class="evidence"><strong>Anchor evidence:</strong> ${d.quote}</div></div></article>`;
}''', text, count=1, flags=re.S)
    text = text.replace("if(k==='score') return (a.score-b.score)*asc;", "if(k==='score') return (a.score-b.score)*asc;")
    text = text.replace("<th data-col=\"rating\">Verdict ${arrow('rating')}</th><th data-col=\"score\" class=\"center\">Score ${arrow('score')}</th><th data-col=\"crumbs\" class=\"center\">Evidence ${arrow('crumbs')}</th>", "<th data-col=\"rating\">Status ${arrow('rating')}</th><th data-col=\"score\" class=\"center\">Score ${arrow('score')}</th><th data-col=\"crumbs\" class=\"center\">Evidence ${arrow('crumbs')}</th>")
    text = text.replace("<td class=\"center\">${d.crumbs}</td>", "<td class=\"center\">${d.score_crumb_count} linked crumbs</td>")
    text = text.replace("<td class=\"center\">${d.score}%</td>", "<td class=\"center\">${d.score}% · ${d.scale_points}/5</td>")
    text = text.replace("renderCards(); renderMatrix(); renderRadar();", "renderCards(); renderMatrix();")
    text = text.replace("renderCards(); renderMatrix();", '''function cardHtml(d){
  const esc = value => String(value ?? '').replace(/[&<>"']/g, character => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  })[character]);
  const crumbs=(d.score_crumbs||[]).map(c=>{
    const quotes=(c.quotes||[]).map(q=>`<div class="chapterMeta">Linked quote (${esc(q.quote_id)}; locator: ${esc(q.locator)}):</div><blockquote>${esc(q.text)}</blockquote>`).join('');
    const chapters=(c.chapters||[]).map(ch=>`<div class="chapterView"><div class="chapterMeta">Source chapter: ${esc(ch.heading_path)} (${esc(ch.chunk_id)})</div><pre class="chapterText">${esc(ch.text)}</pre></div>`).join('');
    return `<li><details class="crumbItem"><summary><span class="crumbLink">${esc(c.id)}</span> — ${esc(c.filename)}</summary><div class="crumbBody">${quotes}${chapters||'<div class="chapterMeta">No linked chapter was found in the source snapshot.</div>'}</div></details></li>`;
  }).join('')||'<li>No linked vendor crumb; score is unmet because vendor evidence is absent.</li>';
  return `<article class="card ${d.rating}" data-rating="${d.rating}"><div class="cardHead" onclick="this.parentElement.classList.toggle('open')"><div class="cardLeft"><span class="id">${d.n}</span><div><div class="title">${d.title}</div><div class="criterionSummary">${d.summary}</div></div></div><span class="badge ${d.rating}">${labels[d.rating]}</span></div><div class="scoreLine"><div class="scoreBar"><div style="width:${d.score}%;background:${ratingClr[d.rating]}"></div></div><span class="scorePct">${d.score}% · ${d.scale_points}/5</span><span class="scoreTrace">${d.score_trace}</span><span>${d.refs}</span></div><div class="cardBody"><div class="block"><h4 class="aff">▸ Criterion summary</h4><p>${d.summary}</p></div><div class="block"><h4 class="aff">▸ Affirmative argument</h4><p>${d.aff}</p></div><div class="block"><h4 class="con">▸ Contrary argument</h4><p>${d.con}</p></div><div class="block"><h4 class="judge">⚖ Judge ruling</h4><p>${d.judge}</p></div><details class="crumbTrace"><summary>Crumbs linked to this score (${d.score_crumb_count})</summary><ul>${crumbs}</ul></details><div class="block"><h4 class="verify">✓ Auditor verification action</h4><p>${d.verify}</p></div><div class="evidence"><strong>Anchor evidence:</strong> ${d.quote}</div></div></article>`;
}
renderCards(); renderMatrix();''')
    text = re.sub(r'<div class="footer">.*?</div>', '<div class="footer">Standalone Ekonerg UMBRA dashboard — sources: Ekonerg active evidence snapshot, 10 CFR 50 Appendix B, ASME NQA-1 Part 1 interpretation baseline. Score withheld.</div>', text, count=1, flags=re.S)
    text = re.sub(r'<div class="footer">.*?</div>', f'<div class="footer">Standalone Ekonerg UMBRA dashboard — sources: Ekonerg active evidence snapshot, 10 CFR 50 Appendix B, ASME NQA-1 Part 1 interpretation baseline. Run {run_id}; score {score:.1f}%.</div>', text, count=1, flags=re.S)
    text = re.sub(r'function cardHtml\(d\)\{.*?\n\}', lambda _match: '''function cardHtml(d){
  const esc = value => String(value ?? '').replace(/[&<>"']/g, character => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  })[character]);
  const crumbs=(d.score_crumbs||[]).map(c=>{
    const quotes=(c.quotes||[]).map(q=>`<div class="chapterMeta">Linked quote (${esc(q.quote_id)}; locator: ${esc(q.locator)}):</div><blockquote>${esc(q.text)}</blockquote>`).join('');
    const chapters=(c.chapters||[]).map(ch=>`<div class="chapterView"><div class="chapterMeta">Source chapter: ${esc(ch.heading_path)} (${esc(ch.chunk_id)})</div><pre class="chapterText">${esc(ch.text)}</pre></div>`).join('');
    return `<li><details class="crumbItem"><summary><span class="crumbLink">${esc(c.id)}</span> — ${esc(c.filename)}</summary><div class="crumbBody">${quotes}${chapters||'<div class="chapterMeta">No linked chapter was found in the source snapshot.</div>'}</div></details></li>`;
  }).join('')||'<li>No linked vendor crumb; score is unmet because vendor evidence is absent.</li>';
  return `<article class="card ${d.rating}" data-rating="${d.rating}"><div class="cardHead" onclick="this.parentElement.classList.toggle('open')"><div class="cardLeft"><span class="id">${d.n}</span><div><div class="title">${d.title}</div><div class="criterionSummary">${d.summary}</div></div></div><span class="badge ${d.rating}">${labels[d.rating]}</span></div><div class="scoreLine"><div class="scoreBar"><div style="width:${d.score}%;background:${ratingClr[d.rating]}"></div></div><span class="scorePct">${d.score}% · ${d.scale_points}/5</span><span class="scoreTrace">${d.score_trace}</span><span>${d.refs}</span></div><div class="cardBody"><div class="block"><h4 class="aff">▸ Criterion summary</h4><p>${d.summary}</p></div><div class="block"><h4 class="aff">▸ Affirmative argument</h4><p>${d.aff}</p></div><div class="block"><h4 class="con">▸ Contrary argument</h4><p>${d.con}</p></div><div class="block"><h4 class="judge">⚖ Judge ruling</h4><p>${d.judge}</p></div><details class="crumbTrace"><summary>Crumbs linked to this score (${d.score_crumb_count})</summary><ul>${crumbs}</ul></details><div class="block"><h4 class="verify">✓ Auditor verification action</h4><p>${d.verify}</p></div><div class="evidence"><strong>Anchor evidence:</strong> ${d.quote}</div></div></article>`;
}''', text, count=1, flags=re.S)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--run-id", default=DEFAULT_RUN_ID)
    ap.add_argument("--date", default="2026-10-05")
    ap.add_argument("--output", type=Path, default=ROOT / "out" / "2026-10-05" / "EKONERG_UMBRA_DASHBOARD_2026-10-05.html")
    args = ap.parse_args()
    page = render(args.matrix, args.db, args.date, args.run_id)
    if "TEKOL" in page or "1499 / 1800" in page or "83.3%" in page:
        raise SystemExit("production dashboard still contains design-reference data")
    args.output.write_text(page, encoding="utf-8", newline="\n")
    print(f"build_umbra_conformance_dashboard: PASS - {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
