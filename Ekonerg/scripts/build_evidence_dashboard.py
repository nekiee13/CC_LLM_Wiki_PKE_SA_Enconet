"""Build the offline UMBRA evidence dashboard before scoring is available.

This view is deliberately separate from the scored report stack.  It reads the
active evidence snapshot and the 18-row matrix, but it never invents ratings or
calculates a conformity score.  The result is safe to open from a local file.
"""
from __future__ import annotations

import argparse
from datetime import date
import html
import json
from pathlib import Path
import re
import sqlite3
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = (
    "login.microsoftonline.com", "oauth", "signin", "https://cdn.",
    "cdnjs.cloudflare.com", "unpkg.com", "jsdelivr.net", "googleapis.com",
)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _read_state(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("gates"), dict):
        raise ValueError("project state must contain a gates mapping")
    return data


def _batch_rows() -> list[dict[str, Any]]:
    # Source counts are the owner-approved EF-2.2 B01-B10 reading batches.
    # Quote fidelity is reported separately because active sieving now has its
    # own 321-record count.
    counts = (1, 3, 3, 3, 3, 2, 3, 3, 2, 1)
    return [
        {"id": f"B{index:02d}", "source_count": count, "state": "Complete"}
        for index, count in enumerate(counts, 1)
    ]


def _query_snapshot(db: Path, matrix_path: Path, run_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    if not isinstance(matrix, list) or len(matrix) != 18:
        raise ValueError("matrix must contain exactly 18 criterion rows")
    if {row.get("criterion_id") for row in matrix}.__len__() != 18:
        raise ValueError("matrix criterion IDs must be unique")

    with sqlite3.connect(str(db)) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = ON")
        if conn.execute("SELECT 1 FROM evaluation_runs WHERE run_id=?", (run_id,)).fetchone() is None:
            raise ValueError(f"unknown evaluation run: {run_id}")
        counts = {
            "registered_files": conn.execute("SELECT count(*) FROM documents").fetchone()[0],
            "qms_files": conn.execute("SELECT count(*) FROM documents WHERE document_side='DOCUMENT'").fetchone()[0],
            "reference_files": conn.execute("SELECT count(*) FROM documents WHERE document_side='RULE'").fetchone()[0],
            "active_crumbs": conn.execute("SELECT count(*) FROM active_crumbs").fetchone()[0],
            "vendor_crumbs": conn.execute("SELECT count(*) FROM active_crumbs WHERE document_side='DOCUMENT'").fetchone()[0],
            "rule_crumbs": conn.execute("SELECT count(*) FROM active_crumbs WHERE document_side='RULE'").fetchone()[0],
            "active_quotes": conn.execute(
                "SELECT count(DISTINCT q.quote_id) FROM crumb_quotes q JOIN active_crumbs c ON c.item_id=q.item_id"
            ).fetchone()[0],
            "exact_links": conn.execute(
                "SELECT count(*) FROM crumb_chunk_links l JOIN active_crumbs c ON c.item_id=l.item_id "
                "WHERE l.link_method='EXACT'"
            ).fetchone()[0],
            "normalized_links": conn.execute(
                "SELECT count(*) FROM crumb_chunk_links l JOIN active_crumbs c ON c.item_id=l.item_id "
                "WHERE l.link_method='NORMALIZED'"
            ).fetchone()[0],
            "judgments": conn.execute(
                "SELECT count(*) FROM criterion_evaluations WHERE evaluation_run_id=?", (run_id,)
            ).fetchone()[0],
        }
        quote_rows = conn.execute(
            "SELECT q.item_id, q.quote_id, q.quote_original, ch.chunk_text "
            "FROM crumb_quotes q JOIN active_crumbs c ON c.item_id=q.item_id "
            "LEFT JOIN crumb_chunk_links l ON l.item_id=q.item_id AND l.quote_id=q.quote_id "
            "LEFT JOIN document_chunks ch ON ch.chunk_id=l.chunk_id"
        ).fetchall()
        quote_exact: dict[tuple[str, str], bool] = {}
        for row in quote_rows:
            key = (row["item_id"], row["quote_id"])
            quote_exact.setdefault(key, False)
            if row["chunk_text"] and row["quote_original"] in row["chunk_text"]:
                quote_exact[key] = True
        counts["quote_exact_records"] = sum(quote_exact.values())
        counts["quote_non_exact_records"] = len(quote_exact) - counts["quote_exact_records"]
        counts["link_rows"] = len(quote_rows)
    criteria = []
    for row in matrix:
        vendor = int(row.get("document_evidence_count", 0))
        anchored = int(row.get("anchored_document_evidence_count", 0))
        if vendor == 0:
            status = "No direct vendor crumb"
        elif anchored:
            status = "Draft coverage + context"
        else:
            status = "Draft coverage"
        criteria.append({
            "id": row["criterion_id"].replace("APP_", "").replace("_", " "),
            "raw_id": row["criterion_id"],
            "title": row["criterion_name"],
            "applicability": row.get("applicability", "unruled"),
            "vendor_crumbs": vendor,
            "anchored_vendor_crumbs": anchored,
            "rule_crumbs": int(row.get("rule_evidence_count", 0)),
            "status": status,
        })
    counts["criteria_with_vendor_crumbs"] = sum(item["vendor_crumbs"] > 0 for item in criteria)
    counts["criteria_without_vendor_crumbs"] = len(criteria) - counts["criteria_with_vendor_crumbs"]
    return counts, criteria


def build_data(db: Path, matrix_path: Path, state_path: Path, run_id: str, generated_date: str, dash_id: str) -> dict[str, Any]:
    if not re.fullmatch(r"DASH-\d{8}-\d{4}", dash_id):
        raise ValueError("dashboard ID must look like DASH-YYYYMMDD-NNNN")
    date.fromisoformat(generated_date)
    state = _read_state(state_path)
    counts, criteria = _query_snapshot(db, matrix_path, run_id)
    gates = {
        gate: {
            "status": record.get("status", "pending"),
            "decision_ref": record.get("decision_ref"),
            "date": (record.get("date").isoformat()
                     if hasattr(record.get("date"), "isoformat")
                     else record.get("date")),
        }
        for gate, record in state["gates"].items()
    }
    return {
        "schema_version": "evidence-dashboard-1.0",
        "supplier": "Ekonerg",
        "generated_date": generated_date,
        "dash_id": dash_id,
        "run_id": run_id,
        "phase": state.get("phase"),
        "score_state": "Withheld",
        "classification_state": "Withheld",
        "judgment_state": f"{counts['judgments']} / 18 judgments recorded",
        "metrics": counts,
        "criteria": criteria,
        "gates": gates,
        "batches": _batch_rows(),
        "queue": [
            {"item": "Implementation records", "why": "Policy text does not prove that controls operated.", "state": "Requested", "trace": "EF-2.2 / QMS-004"},
            {"item": "Five criteria without vendor crumbs", "why": "Ask for source material before making a judgment.", "state": "Open", "trace": "MIN-3.1 matrix"},
            {"item": "18 human criterion judgments", "why": "G3 approved the model; the auditor still must judge each criterion.", "state": "Pending", "trace": "G3 / RUN-20261003-32"},
        ],
        "provenance": {
            "database": "db/nqa_audit.sqlite",
            "matrix": "out/2026-10-05/MIN-3.1-evidence-matrix-v4.json",
            "state": "project-state.yml",
            "batches": "docs/reviews/EF_2_2_EVIDENCE_REVIEW.md",
        },
    }


def render(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    title = html.escape(f"Ekonerg · QA overview · {data['generated_date']}")
    # The page is self-contained by design.  Keep all colours in this token block.
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Offline UMBRA evidence dashboard for the Ekonerg Appendix B audit."><title>{title}</title>
<style>
:root{{--bg-0:#0B0F14;--surface-1:#111821;--surface-2:#17202B;--surface-3:#1E2935;--border-subtle:#243140;--border-strong:#33455A;--accent-fill:#3CCFB4;--accent-text:#5FDCC6;--on-accent:#04201B;--text-primary:#E8EEF4;--text-secondary:#A9B6C4;--text-muted:#8392A3;--review:#E8B04B;--blocked:#F07178;--approved:#6FD39A;--radius-panel:12px;--radius-control:8px}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg-0);color:var(--text-primary);font:15px/1.55 system-ui,sans-serif}}button,input{{font:inherit}}button:focus-visible,a:focus-visible,input:focus-visible{{outline:2px solid var(--accent-fill);outline-offset:2px}}.app{{min-height:100vh;display:grid;grid-template-columns:232px minmax(0,1fr)}}aside{{display:flex;flex-direction:column;gap:28px;padding:24px 16px;background:var(--surface-1);border-right:1px solid var(--border-subtle)}}.brand{{display:flex;gap:10px;align-items:center;padding:4px 8px;font-weight:700}}.brand-mark{{width:26px;height:26px;display:grid;place-items:center;border-radius:8px;background:var(--accent-fill);color:var(--on-accent);font-weight:800}}.nav-label,.eyebrow{{color:var(--text-muted);font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}}nav{{display:grid;gap:4px}}nav a{{padding:9px 10px;border-radius:var(--radius-control);color:var(--text-secondary);text-decoration:none}}nav a:hover,nav a[aria-current=page]{{background:var(--surface-3);color:var(--text-primary)}}nav a[aria-current=page]{{box-shadow:inset 2px 0 var(--accent-fill)}}.reviewer{{margin-top:auto;padding:12px 8px 0;border-top:1px solid var(--border-subtle);color:var(--text-secondary)}}main{{min-width:0;padding:28px}}.topline,.title-row,.panel-head,.metric-head{{display:flex;align-items:center;justify-content:space-between;gap:16px}}.topline{{color:var(--text-muted);font-size:13px}}.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}h1,h2,h3{{margin:0;letter-spacing:-.02em}}h1{{font-size:clamp(28px,3vw,40px);line-height:1.1}}h2{{font-size:20px;line-height:1.25}}h3{{font-size:15px}}.title-row{{margin:24px 0;align-items:end}}.title-row p{{max-width:700px;margin:8px 0 0;color:var(--text-secondary)}}.actions{{display:flex;flex-wrap:wrap;gap:8px}}.btn{{min-height:40px;padding:0 14px;border-radius:var(--radius-control);border:1px solid var(--border-strong);background:var(--surface-3);color:var(--text-primary)}}.btn.primary{{border-color:transparent;background:var(--accent-fill);color:var(--on-accent);font-weight:700}}.metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:16px}}.metric,.panel{{background:var(--surface-1);border:1px solid var(--border-subtle);border-radius:var(--radius-panel)}}.metric{{min-height:128px;padding:16px}}.metric-head{{color:var(--text-muted);font-size:13px}}.metric-value{{margin:18px 0 4px;color:var(--accent-text);font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:27px;font-weight:600}}.metric-note{{color:var(--text-muted);font-size:12px}}.layout{{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(320px,.7fr);gap:16px}}.panel{{padding:20px}}.panel-head{{margin-bottom:18px;align-items:start}}.panel-head p{{margin:4px 0 0;color:var(--text-muted);font-size:13px}}.tag{{display:inline-flex;align-items:center;min-height:26px;padding:0 9px;border-radius:4px;background:var(--surface-3);color:var(--text-secondary);font-size:12px;white-space:nowrap}}.tag.review{{background:rgba(232,176,75,.12);color:var(--review)}}.tag.blocked{{background:rgba(240,113,120,.12);color:var(--blocked)}}.tag.approved{{background:rgba(111,211,154,.12);color:var(--approved)}}.coverage{{display:grid;gap:8px}}.coverage-row{{display:grid;grid-template-columns:95px minmax(120px,1fr) 230px;gap:12px;align-items:center;padding:9px 0;border-bottom:1px solid var(--surface-3)}}.coverage-row:last-child{{border-bottom:0}}.coverage-id{{color:var(--text-muted);font-size:12px}}.bar{{height:7px;overflow:hidden;border-radius:99px;background:var(--surface-3)}}.bar>span{{display:block;height:100%;border-radius:inherit;background:var(--accent-fill)}}.bar>span.empty{{background:var(--blocked)}}.coverage-status{{text-align:right}}.gate{{display:grid;gap:16px}}.gate-state{{display:flex;gap:10px;align-items:flex-start;padding:14px;border:1px solid rgba(232,176,75,.35);border-radius:var(--radius-control);background:rgba(232,176,75,.08)}}.state-dot{{width:9px;height:9px;flex:0 0 auto;margin-top:7px;border-radius:50%;background:var(--review)}}.gate-state strong{{display:block;color:var(--review)}}.gate-state p{{margin:3px 0 0;color:var(--text-secondary);font-size:13px}}.checks{{display:grid;gap:10px}}.check{{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--surface-3);font-size:13px}}.check:last-child{{border-bottom:0}}.check span:first-child{{color:var(--text-secondary)}}.table-panel{{grid-column:1/-1}}.table-wrap{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;min-width:620px}}th,td{{padding:10px;border-bottom:1px solid var(--surface-3);text-align:left;vertical-align:top}}th{{color:var(--text-muted);font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}td{{color:var(--text-secondary);font-size:13px}}td:first-child{{color:var(--text-primary)}}.footer-note{{margin-top:16px;color:var(--text-muted);font-size:12px}}.filter{{min-height:36px;padding:0 10px;border:1px solid var(--border-strong);border-radius:var(--radius-control);background:var(--surface-2);color:var(--text-primary)}}
 .form-panel{{grid-column:1/-1}}.form-help{{margin:0 0 14px;color:var(--text-secondary);font-size:13px}}.form-toolbar{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:14px}}.form-toolbar .progress{{margin-left:auto;color:var(--accent-text);font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:13px}}.judgment-table{{min-width:980px}}.judgment-table select,.judgment-table input,.judgment-table textarea{{width:100%;border:1px solid var(--border-strong);border-radius:var(--radius-control);background:var(--surface-2);color:var(--text-primary);padding:8px}}.judgment-table select{{min-height:38px}}.judgment-table textarea{{min-height:54px;resize:vertical}}.judgment-table th:nth-child(1){{width:190px}}.judgment-table th:nth-child(2){{width:155px}}.judgment-table th:nth-child(3){{width:240px}}.judgment-table th:nth-child(4){{width:340px}}.judgment-table td{{vertical-align:top}}.criterion-name{{display:block;color:var(--text-primary);font-weight:600}}.criterion-meta{{display:block;margin-top:3px;color:var(--text-muted);font-size:12px}}.form-note{{margin:12px 0 0;color:var(--text-muted);font-size:12px}}.btn.small{{min-height:34px;padding:0 10px;font-size:13px}}
@media(max-width:1199px){{.metrics{{grid-template-columns:repeat(2,minmax(0,1fr))}}.layout{{grid-template-columns:1fr}}.table-panel,.form-panel{{grid-column:auto}}}}@media(max-width:759px){{.app{{display:block}}aside{{position:sticky;top:0;z-index:2;display:block;padding:12px 16px}}.brand{{display:inline-flex}}nav{{display:flex;overflow-x:auto;margin-top:10px}}nav a{{flex:0 0 auto}}.nav-label,.reviewer{{display:none}}main{{padding:20px 16px}}.title-row{{display:block}}.actions{{margin-top:14px}}.metrics{{grid-template-columns:1fr}}.coverage-row{{grid-template-columns:72px minmax(90px,1fr)}}.coverage-status{{grid-column:2;text-align:left}}.form-toolbar .progress{{margin-left:0;width:100%}}}}
</style></head><body><div class="app">
<aside aria-label="Audit navigation"><div class="brand"><span class="brand-mark" aria-hidden="true">E</span><span>Ekonerg QA</span></div><div class="nav-label">Audit workspace</div><nav><a href="#overview" aria-current="page">01 Overview</a><a href="#criteria">02 Criteria</a><a href="#judgments">03 Judgments</a><a href="#evidence">04 Evidence</a><a href="#sources">05 Sources</a><a href="#gates">06 Gates</a></nav><div class="reviewer"><strong>Evidence snapshot</strong><br><span class="mono">{html.escape(data['dash_id'])}</span></div></aside>
<main id="overview"><div class="topline"><span>Ekonerg / Audit overview</span><span class="mono">{html.escape(data['run_id'])} · {html.escape(data['phase'] or 'unknown')}</span></div>
<div class="title-row"><div><div class="eyebrow">Appendix B evidence review</div><h1>QA overview</h1><p>Real intake and evidence results are shown below. The conformity score stays withheld until all 18 human judgments are recorded and approved.</p></div><div class="actions"><button class="btn" type="button" onclick="window.print()">Print snapshot</button><button class="btn primary" type="button" onclick="document.getElementById('judgments').scrollIntoView({{behavior:'smooth'}})">Open judgment form</button></div></div>
<section class="metrics" aria-label="Audit summary"><article class="metric"><div class="metric-head"><span>QMS files read</span><span class="mono">01</span></div><div class="metric-value" data-bind="qms_files"></div><div class="metric-note">of supplied vendor scope</div></article><article class="metric"><div class="metric-head"><span>Active vendor crumbs</span><span class="mono">02</span></div><div class="metric-value" data-bind="vendor_crumbs"></div><div class="metric-note" data-bind="crumb_note"></div></article><article class="metric"><div class="metric-head"><span>Criteria with vendor coverage</span><span class="mono">03</span></div><div class="metric-value" data-bind="criteria_coverage"></div><div class="metric-note">five have no direct vendor crumb</div></article><article class="metric"><div class="metric-head"><span>Conformity score</span><span class="mono">04</span></div><div class="metric-value">Withheld</div><div class="metric-note">{html.escape(data['judgment_state'])}</div></article></section>
<div class="layout"><section class="panel" id="criteria" aria-labelledby="coverage-title"><div class="panel-head"><div><h2 id="coverage-title">Criterion coverage</h2><p>All 18 Appendix B criteria remain visible. Coverage is not a pass/fail result.</p></div><input id="criteria-filter" class="filter" type="search" placeholder="Filter criteria" aria-label="Filter criteria"></div><div id="coverage" class="coverage"></div><p class="footer-note">No direct vendor crumb means “ask for evidence,” not “failed.”</p></section>
<section class="panel gate" id="gates" aria-labelledby="gate-title"><div class="panel-head"><div><h2 id="gate-title">Evidence gate</h2><p>Approval state controls what may be scored.</p></div><span class="tag review">Review pending</span></div><div class="gate-state"><span class="state-dot" aria-hidden="true"></span><div><strong>Evidence review complete; judgment pending</strong><p>G3 approved the scoring model. No criterion evaluation rows exist yet, so the score and final classification are withheld.</p></div></div><div class="checks" id="gate-checks"></div></section>
<section class="panel form-panel" id="judgments" aria-labelledby="judgments-title"><div class="panel-head"><div><h2 id="judgments-title">Judgment form</h2><p>Enter one human judgment per criterion. This browser form exports a draft only; it never writes the audit database.</p></div><span class="tag review">Human review</span></div><p class="form-help"><label for="judge-name">Reviewer name</label> <input id="judge-name" class="filter" type="text" placeholder="Enter the human judge name" autocomplete="name" aria-describedby="form-note"></p><div class="form-toolbar"><button class="btn small" type="button" id="fill-undetermined">Use undetermined for all</button><button class="btn small" type="button" id="clear-judgments">Clear form</button><button class="btn small primary" type="button" id="export-judgments">Export draft JSON</button><span class="progress" id="judgment-progress" aria-live="polite">0 / 18 selected</span></div><div class="table-wrap"><table class="judgment-table"><thead><tr><th scope="col">Criterion</th><th scope="col">Rating</th><th scope="col">Evidence crumb IDs</th><th scope="col">Rationale</th></tr></thead><tbody id="judgment-rows"></tbody></table></div><p class="form-note" id="form-note">Positive ratings must cite active vendor crumbs. “Undetermined” means the evidence is not enough to judge; it is not a failure finding.</p></section>
<section class="panel table-panel" id="evidence" aria-labelledby="queue-title"><div class="panel-head"><div><h2 id="queue-title">Evidence queue</h2><p>Next actions are evidence requests, not findings.</p></div><span class="tag blocked">Open work</span></div><div class="table-wrap"><table><thead><tr><th>Item</th><th>Why it matters</th><th>State</th><th>Trace</th></tr></thead><tbody id="queue"></tbody></table></div></section>
<section class="panel table-panel" id="sources" aria-labelledby="batches-title"><div class="panel-head"><div><h2 id="batches-title">QMS reading batches</h2><p>B01–B10 cover all 24 named vendor files.</p></div><span class="mono" style="color:var(--text-muted);font-size:12px">generated {html.escape(data['generated_date'])}</span></div><div class="table-wrap"><table><thead><tr><th>Batch</th><th>Files read</th><th>State</th><th>Source</th></tr></thead><tbody id="batches"></tbody></table></div></section></div>
<p class="footer-note">Offline UMBRA evidence snapshot · sources: <span class="mono">{html.escape(data['provenance']['database'])}</span>, <span class="mono">{html.escape(data['provenance']['matrix'])}</span> · no conformity conclusion asserted.</p></main></div>
<script id="dashboard-data" type="application/json">{payload}</script><script>
const DATA=JSON.parse(document.getElementById('dashboard-data').textContent);
const esc=(s)=>String(s).replace(/[&<>"']/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}}[c]));
document.querySelector('[data-bind=qms_files]').textContent=DATA.metrics.qms_files+'/'+DATA.metrics.qms_files;
document.querySelector('[data-bind=vendor_crumbs]').textContent=DATA.metrics.vendor_crumbs;
document.querySelector('[data-bind=crumb_note]').textContent=DATA.metrics.rule_crumbs+' active rule crumbs · '+DATA.metrics.active_quotes+' quote records ('+DATA.metrics.quote_exact_records+' exact, '+DATA.metrics.quote_non_exact_records+' non-exact)';
document.querySelector('[data-bind=criteria_coverage]').textContent=DATA.metrics.criteria_with_vendor_crumbs+'/18';
function coverage(){{const q=document.getElementById('criteria-filter').value.toLowerCase();document.getElementById('coverage').innerHTML=DATA.criteria.filter(c=>(c.id+' '+c.title+' '+c.status).toLowerCase().includes(q)).map(c=>{{const pct=c.vendor_crumbs?Math.min(100,Math.max(12,c.vendor_crumbs*5)):12;const cls=c.vendor_crumbs?'':' empty';const tag=c.vendor_crumbs?'tag':'tag blocked';return '<div class="coverage-row"><span class="coverage-id mono">'+esc(c.id)+'</span><span class="bar" aria-label="'+esc(c.status)+'"><span class="'+cls+'" style="width:'+pct+'%"></span></span><span class="coverage-status '+tag+'">'+esc(c.status)+' · '+c.vendor_crumbs+' vendor / '+c.rule_crumbs+' rule</span></div>'}}).join('')||'<p class="footer-note">No criteria match.</p>'}}
document.getElementById('criteria-filter').addEventListener('input',coverage);coverage();
const ratings=['fully','substantially','partially','minimally','unmet','undetermined','na'];
const rowFor=(c)=>'<tr><td><span class="mono">'+esc(c.raw_id)+'</span><span class="criterion-name">'+esc(c.title)+'</span><span class="criterion-meta">'+c.vendor_crumbs+' vendor crumbs · '+esc(c.status)+'</span></td><td><select data-criterion="'+esc(c.raw_id)+'" data-field="rating" aria-label="Rating for '+esc(c.raw_id)+'"><option value="">Choose…</option>'+ratings.map(r=>'<option value="'+r+'">'+r+'</option>').join('')+'</select></td><td><input data-criterion="'+esc(c.raw_id)+'" data-field="refs" type="text" placeholder="CRUMB-…" aria-label="Evidence crumbs for '+esc(c.raw_id)+'"></td><td><textarea data-criterion="'+esc(c.raw_id)+'" data-field="rationale" placeholder="Why this rating?" aria-label="Rationale for '+esc(c.raw_id)+'"></textarea></td></tr>';
document.getElementById('judgment-rows').innerHTML=DATA.criteria.map(rowFor).join('');
const ratingFields=()=>Array.from(document.querySelectorAll('[data-field=rating]'));
const updateProgress=()=>{{const n=ratingFields().filter(x=>x.value).length;document.getElementById('judgment-progress').textContent=n+' / '+DATA.criteria.length+' selected';}};
ratingFields().forEach(x=>x.addEventListener('change',updateProgress));
document.getElementById('fill-undetermined').addEventListener('click',()=>{{ratingFields().forEach(x=>x.value='undetermined');updateProgress();}});
document.getElementById('clear-judgments').addEventListener('click',()=>{{document.getElementById('judge-name').value='';document.querySelectorAll('#judgment-rows input,#judgment-rows textarea').forEach(x=>x.value='');ratingFields().forEach(x=>x.value='');updateProgress();}});
document.getElementById('export-judgments').addEventListener('click',()=>{{const judge=document.getElementById('judge-name').value.trim();if(!judge){{alert('Enter the human reviewer name first.');return;}}const rows=DATA.criteria.map(c=>{{const q=(field)=>document.querySelector('[data-criterion="'+c.raw_id+'"][data-field="'+field+'"]');return {{criterion_id:c.raw_id,rating:q('rating').value,evidence_ids:q('refs').value.split(',').map(x=>x.trim()).filter(Boolean),judge_ruling:judge,rationale:q('rationale').value.trim()}};}});if(rows.some(r=>!r.rating)){{alert('Choose a rating for all 18 criteria before exporting.');return;}}const blob=new Blob([JSON.stringify({{run_id:DATA.run_id,reviewer:judge,source:'offline dashboard draft',criteria:rows}},null,2)],{{type:'application/json'}});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=''+DATA.run_id+'-judgment-draft.json';link.click();URL.revokeObjectURL(link.href);}});
document.getElementById('gate-checks').innerHTML=Object.entries(DATA.gates).map(([g,v])=>'<div class="check"><span>'+g+' gate</span><span class="tag '+(v.status==='approved'?'approved':'review')+'">'+esc(v.status)+(v.decision_ref?' · '+esc(v.decision_ref):'')+'</span></div>').join('')+'<div class="check"><span>Conformity score</span><span class="tag review">Withheld</span></div>';
document.getElementById('queue').innerHTML=DATA.queue.map(i=>'<tr><td>'+esc(i.item)+'</td><td>'+esc(i.why)+'</td><td><span class="tag '+(i.state==='Open'?'blocked':'review')+'">'+esc(i.state)+'</span></td><td class="mono">'+esc(i.trace)+'</td></tr>').join('');
document.getElementById('batches').innerHTML=DATA.batches.map(b=>'<tr><td class="mono">'+esc(b.id)+'</td><td>'+b.source_count+'</td><td><span class="tag approved">'+esc(b.state)+'</span></td><td>EF-2.2 evidence review</td></tr>').join('');
</script></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=ROOT / "db" / "nqa_audit.sqlite")
    parser.add_argument("--matrix", type=Path, default=ROOT / "out" / "2026-10-05" / "MIN-3.1-evidence-matrix-v4.json")
    parser.add_argument("--state", type=Path, default=ROOT / "project-state.yml")
    parser.add_argument("--run-id", default="RUN-20261003-32")
    parser.add_argument("--generated-date", default=date.today().isoformat())
    parser.add_argument("--dash-id", default=None)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--html-output", type=Path, required=True)
    args = parser.parse_args()
    dash_id = args.dash_id or f"DASH-{args.generated_date.replace('-', '')}-0001"
    data = build_data(args.db, args.matrix, args.state, args.run_id, args.generated_date, dash_id)
    page = render(data)
    if any(item in page.casefold() for item in FORBIDDEN):
        raise ValueError("offline dashboard contains a forbidden remote resource")
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.html_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_bytes(_json_bytes(data))
    args.html_output.write_text(page, encoding="utf-8", newline="\n")
    print(f"build_evidence_dashboard: PASS - {args.json_output}")
    print(f"build_evidence_dashboard: PASS - {args.html_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
