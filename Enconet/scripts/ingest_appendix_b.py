#!/usr/bin/env python3
"""Deterministically ingest the 18 Appendix B criteria as RULE crumbs and requirements."""
from __future__ import annotations

import argparse, re, sys
from dataclasses import dataclass
from pathlib import Path
import yaml

import db_util

ENCONET=Path(__file__).resolve().parents[1]
DERIVED=ENCONET/"derived"; TAXONOMY=ENCONET/"schemas"/"app_b_taxonomy.yml"
NRC_URL="https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb.html"
ROMAN="I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII"
HEADING=re.compile(rf"(?m)^#\s+(?P<roman>{ROMAN})\.\s+(?P<title>[^\r\n]+)\s*$")

@dataclass(frozen=True)
class Section:
    criterion_id:str; criterion_name:str; text:str; start:int; end:int

def parse(text:str)->list[Section]:
    taxonomy=yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))["criteria"]
    names={c["criterion_id"]:c["criterion_name"] for c in taxonomy}
    matches=list(HEADING.finditer(text)); sections=[]
    for i,m in enumerate(matches):
        cid=f"APP_B_{m['roman']}"; end=matches[i+1].start() if i+1<len(matches) else len(text)
        # Preserve the byte-exact source slice: validate_chunks re-proves that
        # chunk_text == derived_text[char_start:char_end].
        body=text[m.start():end]
        if cid not in names:
            raise ValueError(f"unknown criterion heading: {cid}")
        sections.append(Section(cid,names[cid],body,m.start(),end))
    if [s.criterion_id for s in sections] != list(names):
        raise ValueError(f"expected all 18 criteria in canonical order; found {[s.criterion_id for s in sections]}")
    return sections

def ingest(db:Path, *, doc_id:str="DOC-0019", run_id:str="RUN-20260713-01", derived_root:Path=DERIVED)->int:
    source=derived_root/f"{doc_id}.txt"; text=source.read_text(encoding="utf-8"); sections=parse(text)
    with db_util.connect(db) as c:
        doc=db_util.lookup(c,"documents","doc_id",doc_id)
        if doc is None or doc["document_side"]!="RULE": raise ValueError("Appendix B must be a registered RULE document")
        c.execute("UPDATE documents SET source_url=?, notes=notes || ? WHERE doc_id=?",(NRC_URL,"; public-source retrieval/intake date 2026-07-12",doc_id))
        old=[r[0] for r in c.execute("SELECT item_id FROM crumbs WHERE doc_id=?",(doc_id,))]
        if old:
            c.executemany("DELETE FROM requirements WHERE source_item_id=?",[(x,) for x in old])
        c.execute("DELETE FROM crumbs WHERE doc_id=?",(doc_id,)); c.execute("DELETE FROM sieve_runs WHERE doc_id=?",(doc_id,)); c.execute("DELETE FROM document_chunks WHERE doc_id=?",(doc_id,))
        db_util.insert(c,"sieve_runs",{"run_id":run_id,"doc_id":doc_id,"prompt_version":"appb_rule_v1","document_side":"RULE","source_rule":"10CFR50_APPB"})
        db_util.insert(c,"sieve_run_authorities",{"run_id":run_id,"authority_role":"GOVERNING","source_code":"10CFR50_APPB","source_locator":"Appendix B","applicability":"APPLICABLE"})
        for n,s in enumerate(sections,1):
            chunk=f"CHUNK-{doc_id}-{n:04d}"; crumb=f"CRUMB-{doc_id}-{s.criterion_id}-{n:04d}"; quote=f"QUOTE-{doc_id}-{n:04d}-01"
            db_util.insert(c,"document_chunks",{"chunk_id":chunk,"doc_id":doc_id,"heading_path":s.criterion_id,"chunk_text":s.text,"char_start":s.start,"char_end":s.end,"source_sha256":doc["sha256"]})
            statement=re.sub(r"\s+"," ",s.text.split("\n",1)[-1]).strip()
            db_util.insert(c,"crumbs",{"item_id":crumb,"doc_id":doc_id,"sieve_run_id":run_id,"criterion_id":s.criterion_id,"document_side":"RULE","statement":statement,"item_type":"requirement","quote_language":"en"})
            db_util.insert(c,"crumb_sources",{"item_id":crumb,"source_locator":s.criterion_id,"source_heading_path":s.criterion_name})
            db_util.insert(c,"crumb_quotes",{"quote_id":quote,"item_id":crumb,"quote_original":s.text,"quote_language":"en","source_locator":s.criterion_id})
            db_util.insert(c,"crumb_authority_refs",{"item_id":crumb,"authority_role":"GOVERNING","source_code":"10CFR50_APPB","source_locator":s.criterion_id,"applicability":"APPLICABLE"})
            db_util.insert(c,"crumb_chunk_links",{"item_id":crumb,"quote_id":quote,"chunk_id":chunk,"link_method":"EXACT","confidence":1.0})
            roman=s.criterion_id.removeprefix("APP_B_")
            db_util.insert(c,"requirements",{"requirement_id":f"REQ-APP_B_{roman}-01","criterion_id":s.criterion_id,"requirement_text":statement,"source_item_id":crumb,"is_subrequirement":0})
    return len(sections)

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--db",type=Path,default=db_util.DEFAULT_DB);p.add_argument("--doc-id",default="DOC-0019");p.add_argument("--run-id",default="RUN-20260713-01");a=p.parse_args()
    try: print(f"ingest_appendix_b: PASS - criteria={ingest(a.db,doc_id=a.doc_id,run_id=a.run_id)}");return 0
    except Exception as e: print(f"ingest_appendix_b: FAIL - {e}",file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
