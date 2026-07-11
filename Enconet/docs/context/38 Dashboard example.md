```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TEKOL — 10 CFR 50 Appendix B Conformance Dashboard</title>
<style>
:root{
  --bg:#eef3f8; --panel:#ffffff; --ink:#17212b; --muted:#647382; --line:#d7e0ea;
  --navy:#17385f; --blue:#2e638d; --cyan:#e8f4fb; --shadow:0 10px 26px rgba(20,40,70,.10);
  --fully:#1f7a3b; --sub:#5a8d24; --partial:#d99100; --minimal:#d85b00; --unmet:#b72424; --und:#697386;
  --fullyBg:#e8f6ec; --subBg:#eef7e8; --partialBg:#fff4d8; --minimalBg:#fff0e5; --unmetBg:#fde8e8; --undBg:#eef0f3;
}
*{box-sizing:border-box} html{scroll-behavior:smooth} body{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI",Arial,system-ui,sans-serif;font-size:14px;line-height:1.45}
.header{background:linear-gradient(135deg,#102e50,#22557e 58%,#2e638d);color:white;padding:28px 34px 22px;border-bottom:1px solid rgba(255,255,255,.18)}
.header h1{margin:0;font-size:25px;letter-spacing:-.3px}.header p{margin:6px 0 0;color:rgba(255,255,255,.82);font-size:13px}.header .pill{display:inline-block;margin-top:12px;padding:5px 10px;border:1px solid rgba(255,255,255,.25);border-radius:99px;background:rgba(255,255,255,.10);font-size:12px;font-weight:700}
.topbar{background:#fff;border-bottom:1px solid var(--line);padding:16px 34px;display:grid;grid-template-columns:repeat(6,minmax(120px,1fr));gap:12px}.metric{border:1px solid var(--line);border-radius:14px;background:#fbfdff;padding:12px 14px;min-height:78px}.metric.main{background:var(--navy);color:#fff;border-color:var(--navy)}.metric .num{font-size:28px;font-weight:850;line-height:1}.metric .label{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-top:6px}.metric.main .label{color:rgba(255,255,255,.78)}.metric .small{font-size:12px;color:var(--muted);margin-top:5px}.metric.main .small{color:rgba(255,255,255,.78)}
.wrap{max-width:1420px;margin:0 auto;padding:20px 24px 44px}.section{background:var(--panel);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);padding:18px;margin-bottom:16px}.section h2{font-size:18px;margin:0 0 10px;color:var(--navy)}.section p{margin:6px 0;color:#344451}.summaryGrid{display:grid;grid-template-columns:1.3fr .9fr;gap:16px}.progress{height:22px;background:#dfe7ef;border-radius:99px;display:flex;overflow:hidden;border:1px solid #cbd6e1}.seg{height:100%}.legend{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:#344451}.sw{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-2px}.riskList{margin:8px 0 0 18px;color:#344451}.riskList li{margin:4px 0}.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px}.btn{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:99px;padding:8px 12px;font-size:12px;font-weight:750;cursor:pointer}.btn:hover{background:#f6f9fc}.btn.active{background:var(--navy);color:white;border-color:var(--navy)}.search{flex:1;min-width:240px;border:1px solid var(--line);border-radius:10px;padding:9px 11px;font-size:13px}.select{border:1px solid var(--line);border-radius:10px;padding:9px 11px;background:white;font-size:13px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:14px}.card{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 4px 12px rgba(20,40,70,.05)}.cardHead{padding:14px 15px 10px;display:flex;justify-content:space-between;gap:10px;align-items:flex-start;cursor:pointer}.id{font-weight:900;color:var(--navy);background:#e7eef6;border-radius:8px;padding:3px 10px;min-width:42px;text-align:center}.title{font-weight:800;font-size:15px;margin-top:7px}.badge{white-space:nowrap;font-size:11px;font-weight:850;text-transform:uppercase;border-radius:99px;padding:5px 10px}.fully{color:var(--fully);background:var(--fullyBg)}.substantially{color:var(--sub);background:var(--subBg)}.partially{color:var(--partial);background:var(--partialBg)}.minimally{color:var(--minimal);background:var(--minimalBg)}.unmet{color:var(--unmet);background:var(--unmetBg)}.undetermined{color:var(--und);background:var(--undBg)}.scoreLine{padding:0 15px 12px;color:var(--muted);font-size:12px}.cardBody{display:none;border-top:1px solid var(--line);padding:13px 15px 15px;background:#fbfdff}.card.open .cardBody{display:block}.block{margin:0 0 12px}.block h4{margin:0 0 4px;font-size:12px;letter-spacing:.25px;text-transform:uppercase}.aff{color:var(--fully)}.con{color:var(--unmet)}.judge{color:var(--navy)}.verify{color:#6b4f00}.block p{margin:0;color:#344451;font-size:13px}.evidence{font-size:12px;color:var(--muted);padding:8px 10px;background:#f0f4f8;border-radius:10px;margin-top:9px}.matrixWrap{overflow:auto}.matrix{width:100%;border-collapse:collapse;font-size:13px}.matrix th,.matrix td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left;vertical-align:top}.matrix th{background:#f3f7fb;color:var(--navy);font-size:12px;text-transform:uppercase;letter-spacing:.35px}.matrix tr:hover td{background:#fbfdff}.footer{font-size:12px;color:var(--muted);text-align:center;margin-top:18px}.note{padding:11px 13px;border-left:4px solid var(--partial);background:#fff8e8;border-radius:8px;color:#3d2b00;margin-top:10px}
@media(max-width:1000px){.topbar{grid-template-columns:repeat(3,1fr)}.summaryGrid{grid-template-columns:1fr}}@media(max-width:620px){.header,.topbar{padding-left:18px;padding-right:18px}.topbar{grid-template-columns:1fr 1fr}.wrap{padding:14px}.grid{grid-template-columns:1fr}.cardHead{display:block}.badge{display:inline-block;margin-top:9px}.controls{align-items:stretch}.search,.select{width:100%;flex:auto}}
@media print{.controls,.footer{display:none}.section,.card{box-shadow:none}.cardBody{display:block}.grid{grid-template-columns:1fr}.topbar{grid-template-columns:repeat(3,1fr)}}
</style>
</head>
<body>
<header class="header">
  <h1>10 CFR 50 Appendix B — TEKOL Conformance Dashboard</h1>
  <p>Document set: PK R8 (PSV) v2, SP 4.1.1 R10, SP 4.1.2 R2, SP 8.2.3 R5, SP 8.2.4 R1, and audit crumbs.</p>
  <span class="pill">Evidence-supported classification: Substantially Matched</span>
</header>

<section class="topbar">
  <div class="metric main"><div class="num">72.2%</div><div class="label">Overall score</div><div class="small">13.0 / 18 weighted units</div></div>
  <div class="metric"><div class="num">18</div><div class="label">Appendix B criteria</div><div class="small">Criteria I–XVIII</div></div>
  <div class="metric"><div class="num">2</div><div class="label">Fully matched</div><div class="small">High evidence support</div></div>
  <div class="metric"><div class="num">12</div><div class="label">Substantially matched</div><div class="small">Minor or record gaps</div></div>
  <div class="metric"><div class="num">4</div><div class="label">Partially matched</div><div class="small">Material evidence gaps</div></div>
  <div class="metric"><div class="num">0</div><div class="label">Unmet</div><div class="small">No criterion rated unmet</div></div>
</section>

<main class="wrap">
  <section class="section summaryGrid">
    <div>
      <h2>Executive Summary</h2>
      <p>TEKOL's document set shows a documented QA system aligned with 10 CFR 50 Appendix B for NEK coating and surface-protection work. The strongest areas are organization, special-process control, inspection planning, nonconformance control, corrective action, and quality records.</p>
      <p>The system is not shown as a complete nuclear Appendix B / NQA-1 program because several implementing procedures and completed records were not included in the reviewed source package.</p>
      <div class="note"><strong>Main audit risk:</strong> documented intent is stronger than directly verified implementation evidence.</div>
    </div>
    <div>
      <h2>Classification Distribution</h2>
      <div class="progress" aria-label="classification distribution">
        <div class="seg" style="width:11.111%;background:var(--fully)" title="Fully Matched: 2"></div>
        <div class="seg" style="width:66.667%;background:var(--sub)" title="Substantially Matched: 12"></div>
        <div class="seg" style="width:22.222%;background:var(--partial)" title="Partially Matched: 4"></div>
      </div>
      <div class="legend">
        <span><span class="sw" style="background:var(--fully)"></span>Fully: 2</span>
        <span><span class="sw" style="background:var(--sub)"></span>Substantially: 12</span>
        <span><span class="sw" style="background:var(--partial)"></span>Partially: 4</span>
        <span><span class="sw" style="background:var(--minimal)"></span>Minimally: 0</span>
        <span><span class="sw" style="background:var(--unmet)"></span>Unmet: 0</span>
      </div>
      <ul class="riskList">
        <li>Design control is narrower than full Appendix B design control.</li>
        <li>Test control is not presented as a full formal test program.</li>
        <li>Operating-status control appears dependent on NEK interface controls.</li>
        <li>Audit-program records require direct verification.</li>
      </ul>
    </div>
  </section>

  <section class="section">
    <h2>Criterion Cards</h2>
    <div class="controls">
      <button class="btn active" data-filter="all">All (18)</button>
      <button class="btn" data-filter="fully">Fully (2)</button>
      <button class="btn" data-filter="substantially">Substantially (12)</button>
      <button class="btn" data-filter="partially">Partially (4)</button>
      <button class="btn" id="expandAll">Expand all</button>
      <button class="btn" id="collapseAll">Collapse all</button>
      <input id="search" class="search" placeholder="Search criterion, evidence, gap, or verification action" />
      <select id="sort" class="select">
        <option value="order">Sort: Criterion order</option>
        <option value="risk">Sort: Highest risk first</option>
        <option value="score">Sort: Highest score first</option>
      </select>
    </div>
    <div class="grid" id="cards"></div>
  </section>

  <section class="section">
    <h2>Conformance Matrix</h2>
    <div class="matrixWrap"><table class="matrix" id="matrix"></table></div>
  </section>

  <section class="section">
    <h2>Priority Verification Actions</h2>
    <ul class="riskList">
      <li>Review missing core procedures: SP 4.2.1, SP 6.2.1, SP 7.4.2, SP 7.5.6, SP 7.6.1, SP 8.2.2, SP 8.3.1, and SP 8.5.1.</li>
      <li>Sample one complete NEK SR work package and one complete NEK AQ work package.</li>
      <li>Trace one coating-material batch from procurement through storage, issue, application, inspection, and final records.</li>
      <li>Verify QA-engineer appointment, authority, independence, and direct access to management.</li>
      <li>Verify audit schedule, audit checklists, trained independent auditors, findings, follow-up, and reaudit evidence.</li>
    </ul>
  </section>
  <div class="footer">Standalone HTML dashboard. No external libraries are required.</div>
</main>

<script>
const data = [
{n:'I',order:1,title:'Organization',rating:'fully',score:1.00,refs:'SP 4.1.1 §3.1–3.2; organizational and functional QA links; audit crumbs',aff:'The document set defines director accountability, QA roles, QA engineer involvement, Appendix B element responsibility mapping, and organizational links. QA independence and direct reporting to management are documented for NEK-related QA functions.',con:'Implementation records such as appointment letters, detailed job descriptions, and examples of QA stop-work or escalation were not included in the reviewed source package.',judge:'Fully Matched. Written responsibility, authority, QA independence, and management access are sufficiently addressed for document-level conformance.',verify:'Verify QA engineer appointment records, job descriptions, reporting line, conflict-of-interest controls, and actual examples of QA escalation.'},
{n:'II',order:2,title:'Quality Assurance Program',rating:'substantially',score:.75,refs:'SP 4.1.1 §1–3; SP 4.1.2 §1; PK R8 quality manual',aff:'A documented QA system is established for NEK work. The program references 10 CFR 50 Appendix B, Regulatory Guide 1.54, SR/AQ/BOP classifications, and key NEK processes.',con:'Several implementing procedures and records for training, regular review, and program adequacy were not directly reviewed.',judge:'Substantially Matched. The QA program is documented and scoped, but full evidence for training, review, and all implementing procedures remains incomplete.',verify:'Verify QA program reviews, training matrices, qualification records, current controlled procedures, and management review records.'},
{n:'III',order:3,title:'Design Control',rating:'partially',score:.50,refs:'SP 4.1.1 §4.3; referenced SP 7.2.2 / SP 7.3.1 / SP 7.3.2',aff:'Technology and specification controls exist for coating work, including NEK consent for coating-material substitution and control of technological specifications.',con:'Full Appendix B design control is broader. Direct evidence was not shown for nuclear design-basis translation, design-interface control, independent design verification, and original-design approval authority.',judge:'Partially Matched. Technical specification control is present, but complete nuclear design-control depth is not demonstrated.',verify:'Review SP 7.2.2, SP 7.3.1, SP 7.3.2, design-change records, independent reviews, interface controls, and NEK approval records.'},
{n:'IV',order:4,title:'Procurement Document Control',rating:'substantially',score:.75,refs:'SP 4.1.1 §4.4; PK R8 supplier-control clauses; referenced SP 7.4.1 / SP 7.4.2',aff:'Procurement requirements are linked to technological specifications, system documents, supplier communication, competence, verification, and quality requirements.',con:'Full SP 7.4.2 and actual purchase-order flowdown evidence were not included. Direct evidence of Appendix B, QS-610, 10 CFR 21, right-of-access, and supplier QA clauses requires sampling.',judge:'Substantially Matched. Procurement document control is addressed, but objective purchase-order evidence must be verified.',verify:'Sample NEK purchase orders, RFQs, supplier specifications, certificate requirements, right-of-access clauses, QA-flowdown clauses, and material substitution approvals.'},
{n:'V',order:5,title:'Instructions, Procedures, and Drawings',rating:'substantially',score:.75,refs:'SP 8.2.3 §1, §4.1.2; SP 8.2.4 §4.1.2; DN 10.01–DN 10.10 references',aff:'Quality-affecting work is prescribed through procedures, work instructions, control plans, technological procedures, inspection methods, and acceptance criteria.',con:'Several lower-level instructions were referenced but not fully uploaded. Drawing control is not a major visible element in the provided document set.',judge:'Substantially Matched. Procedure and acceptance-criteria controls are strong, but full lower-level instruction review is needed.',verify:'Verify current DN 10.01–DN 10.10, work packages, technological instructions, control plans, and field records.'},
{n:'VI',order:6,title:'Document Control',rating:'substantially',score:.75,refs:'PK R8 document-control statements; SP 4.1.2 §7; referenced SP 4.2.1',aff:'Controlled electronic copies, printed-copy validity checks, review/approval, distribution, revision, and archiving rules are documented.',con:'The primary document-control procedure SP 4.2.1 was not uploaded. Records for obsolete-document removal, distribution, and field-use verification remain to be sampled.',judge:'Substantially Matched. Document-control principles are documented, but implementing records are needed.',verify:'Review SP 4.2.1, master document list, obsolete-document controls, revision approvals, and controlled copies at DE Krško.'},
{n:'VII',order:7,title:'Control of Purchased Material, Equipment, and Services',rating:'substantially',score:.75,refs:'SP 4.1.1 §4.7; PK R8 §8.4; referenced SP 7.4.2',aff:'Supplier evaluation, incoming control, material acceptability evidence, storage, and procurement-related records are addressed through referenced procurement and incoming-control procedures.',con:'Direct evidence of supplier QA effectiveness assessment, source inspection, receipt inspection records, and site availability of certificates before use was not included.',judge:'Substantially Matched. Supplier and incoming-control structure exists, but record-based confirmation is required.',verify:'Sample supplier evaluations, incoming inspection reports, certificates, coating batch records, storage release records, and supplier nonconformance records.'},
{n:'VIII',order:8,title:'Identification and Control of Materials, Parts, and Components',rating:'substantially',score:.75,refs:'SP 4.1.1 §4.8; material batch and packaging controls',aff:'Material traceability is maintained by commercial name and batch from need identification to installation. Nonconforming materials are marked and stored separately.',con:'The evidence focuses on coating materials. Actual batch-to-installed-location traceability records were not included.',judge:'Substantially Matched. Traceability controls are suitable for coating materials, with record sampling still required.',verify:'Trace one batch from purchase request through incoming inspection, storage, issue, use, inspection, and final documentation package.'},
{n:'IX',order:9,title:'Control of Special Processes',rating:'fully',score:1.00,refs:'SP 4.1.1 §2 and §4.9; ASTM D4537 / D5498 / D7108 references',aff:'Surface protection is explicitly defined as a special process. Control is based on qualified personnel, NEK procedures, internal standards, and NEK-approved technologies.',con:'Personnel qualification records and procedure qualification records were not fully included, but the documented control model is direct and strong.',judge:'Fully Matched. Criterion IX is directly addressed and highly relevant to TEKOL coating work.',verify:'Verify qualification records for coating personnel, inspectors, QA engineer, and special-process procedure qualification evidence.'},
{n:'X',order:10,title:'Inspection',rating:'substantially',score:.75,refs:'SP 8.2.3 §3.2, §4.1.1–4.1.8; control plans; hold/witness points',aff:'Inspection activities, phase control, interphase control, final control, control methods, criteria, records, hold points, and witness points are defined.',con:'The document set does not always state Appendix B inspection independence in direct terms. Actual control-plan and hold-point records require verification.',judge:'Substantially Matched. Inspection control is operationally strong, but record-based confirmation of independence and hold-point enforcement is needed.',verify:'Review signed control plans, hold-point releases, witness-point notices, inspector independence, and inspection reports.'},
{n:'XI',order:11,title:'Test Control',rating:'partially',score:.50,refs:'SP 8.2.3 §4.1.1–4.1.2; SP 4.1.1 §4.11',aff:'Control methods, equipment, standards, environmental checks, acceptance criteria, and material verification are included in control planning.',con:'A formal Appendix B test program is not shown. Testing is mainly inspection-like and material-verification based.',judge:'Partially Matched. Test-like controls exist, but a complete test-control program is not demonstrated.',verify:'Identify required tests, written test procedures, prerequisites, instrumentation, acceptance limits, test records, and evaluation of results.'},
{n:'XII',order:12,title:'Control of Measuring and Test Equipment',rating:'substantially',score:.75,refs:'SP 4.1.1 §4.12; PK R8 measuring-equipment controls; referenced SP 7.6.1',aff:'Measuring equipment is recorded, periodically checked, calibrated, and traceable to international standards through referenced equipment-control processes.',con:'SP 7.6.1 and calibration records were not included. Out-of-tolerance handling and calibration periodicity require verification.',judge:'Substantially Matched. The requirement is documented, with direct record sampling still needed.',verify:'Sample equipment register, calibration certificates, due dates, labels, out-of-tolerance records, and field-use records.'},
{n:'XIII',order:13,title:'Handling, Storage, and Shipping',rating:'substantially',score:.75,refs:'SP 4.1.1 §4.13; PK R8 preservation controls; DN 15.01 / DN 15.02 references',aff:'Handling, storage, distribution, hazardous-chemical training, container marking, and preservation controls are documented for coating materials and work objects.',con:'Detailed special-environment controls, shelf-life records, humidity/temperature records, and lower-level instructions were not directly reviewed.',judge:'Substantially Matched. Core controls are present, but storage-condition implementation requires sampling.',verify:'Inspect storage areas, shelf-life records, temperature/humidity logs, hazardous-material controls, labeling, segregation, and transport records.'},
{n:'XIV',order:14,title:'Inspection, Test, and Operating Status',rating:'partially',score:.50,refs:'SP 4.1.1 §4.14; SP 8.2.3 control-plan release process',aff:'Inspection status is visible through records and measurement protocols. Unacceptable surfaces are marked and documented. Process release is blocked until control-plan activities are complete.',con:'Operating status of nuclear plant SSCs is not clearly controlled by TEKOL. The interface with NEK tagging, clearance, and operating-status controls is not fully defined.',judge:'Partially Matched. Inspection/test status is partly addressed; operating-status control is unresolved or NEK-dependent.',verify:'Confirm NEK interface controls, lockout/tagout or clearance requirements, rejected-area marking, release records, and TEKOL scope boundaries.'},
{n:'XV',order:15,title:'Nonconforming Materials, Parts, or Components',rating:'substantially',score:.75,refs:'SP 8.2.3 §3.2 and §4.1.9–4.1.16; SP 4.1.1 §4.15',aff:'Nonconformance detection, reporting, analysis, disposition, NEK notification, remediation, review, closure reporting, segregation, and marking are documented.',con:'The process is strongest for coating work. The full nonconformance procedure SP 8.3.1 was not uploaded.',judge:'Substantially Matched. Nonconformance control is robust for TEKOL scope, with full procedure and records still needed.',verify:'Sample nonconformance reports, disposition approvals, segregated materials, NEK notifications, rework/repair records, and exceptional-acceptance approvals.'},
{n:'XVI',order:16,title:'Corrective Action',rating:'substantially',score:.75,refs:'SP 8.2.3 §4.1.10–4.1.16; SP 4.1.2 process monitoring; referenced SP 8.5.1',aff:'Corrective action is linked to nonconformance analysis, causes, consequences, remediation proposals, NEK communication, review, closure, and quality-process monitoring.',con:'The full corrective-action procedure was not uploaded. The terms condition adverse to quality and significant condition adverse to quality are not clearly mapped.',judge:'Substantially Matched. Corrective-action control exists, but significance classification and root-cause depth must be verified.',verify:'Review SP 8.5.1, corrective-action register, root-cause analyses, effectiveness checks, management reporting, and repeat-issue tracking.'},
{n:'XVII',order:17,title:'Quality Assurance Records',rating:'substantially',score:.75,refs:'SP 8.2.3 §5; SP 8.2.4 §5; retention and record tables',aff:'Control plans, execution records, coating-control lists, reports, deviation records, corrective-action registers, complaint registers, and 10 CFR 21 records are defined with storage and retention expectations.',con:'Record retrievability, indexing, and completed record-package quality require sampling. Some records depend on procedures not uploaded.',judge:'Substantially Matched. Records are extensively defined, but completed record-package retrieval must be tested.',verify:'Retrieve one complete NEK work package including control plan, certificates, inspections, calibration, qualifications, nonconformances, corrective actions, and final records.'},
{n:'XVIII',order:18,title:'Audits',rating:'partially',score:.50,refs:'SP 4.1.1 Appendix B element 18 mapping; referenced SP 8.2.2; PK R8 external audit statements',aff:'Audit activity is mapped as Appendix B element 18 and internal audits are referenced through SP 8.2.2. The quality manual recognizes external audit and certification review.',con:'SP 8.2.2 was not uploaded. Audit schedules, checklists, auditor independence, auditor training, audit reports, management review, follow-up, and reaudit records were not directly verified.',judge:'Partially Matched. Audit-program existence is indicated, but full Criterion XVIII evidence is incomplete.',verify:'Verify audit schedule, reports, checklists, auditor competence and independence, management review, corrective actions, follow-up, and reaudit records.'}
];
const labels={fully:'Fully Matched',substantially:'Substantially Matched',partially:'Partially Matched',minimally:'Minimally Matched',unmet:'Unmet',undetermined:'Undetermined'};
const riskRank={unmet:5,minimally:4,partially:3,substantially:2,fully:1};
let filter='all';
function clean(s){return (s||'').toLowerCase()}
function getFiltered(){const q=clean(document.getElementById('search').value);let arr=data.filter(d=>filter==='all'||d.rating===filter).filter(d=>!q||clean(Object.values(d).join(' ')).includes(q));const sort=document.getElementById('sort').value;if(sort==='risk')arr=[...arr].sort((a,b)=>riskRank[b.rating]-riskRank[a.rating]||a.order-b.order);if(sort==='score')arr=[...arr].sort((a,b)=>b.score-a.score||a.order-b.order);if(sort==='order')arr=[...arr].sort((a,b)=>a.order-b.order);return arr}
function cardHtml(d){return `<article class="card" data-rating="${d.rating}"><div class="cardHead" onclick="this.parentElement.classList.toggle('open')"><div><span class="id">${d.n}</span><div class="title">${d.title}</div></div><span class="badge ${d.rating}">${labels[d.rating]}</span></div><div class="scoreLine">Score: ${(d.score*100).toFixed(0)}% | Evidence: ${d.refs}</div><div class="cardBody"><div class="block"><h4 class="aff">Affirmative</h4><p>${d.aff}</p></div><div class="block"><h4 class="con">Contrary</h4><p>${d.con}</p></div><div class="block"><h4 class="judge">Judge ruling</h4><p>${d.judge}</p></div><div class="block"><h4 class="verify">Auditor verification</h4><p>${d.verify}</p></div><div class="evidence">Classification rule applied: no positive rating above Substantially Matched unless direct documentary or crumb-supported evidence exists. Record-only gaps reduce the rating where implementation cannot be confirmed.</div></div></article>`}
function renderCards(){document.getElementById('cards').innerHTML=getFiltered().map(cardHtml).join('')||'<p>No matching criteria found.</p>'}
function renderMatrix(){document.getElementById('matrix').innerHTML='<thead><tr><th>Criterion</th><th>Topic</th><th>Classification</th><th>Key basis</th><th>Primary verification action</th></tr></thead><tbody>'+data.map(d=>`<tr><td><strong>${d.n}</strong></td><td>${d.title}</td><td><span class="badge ${d.rating}">${labels[d.rating]}</span></td><td>${d.judge}</td><td>${d.verify}</td></tr>`).join('')+'</tbody>'}
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.classList.remove('active'));b.classList.add('active');filter=b.dataset.filter;renderCards()}));
document.getElementById('search').addEventListener('input',renderCards);document.getElementById('sort').addEventListener('change',renderCards);document.getElementById('expandAll').addEventListener('click',()=>document.querySelectorAll('.card').forEach(c=>c.classList.add('open')));document.getElementById('collapseAll').addEventListener('click',()=>document.querySelectorAll('.card').forEach(c=>c.classList.remove('open')));
renderCards();renderMatrix();
</script>
</body>
</html>

```